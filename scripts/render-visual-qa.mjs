import { chromium } from 'playwright';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const baseUrl = process.argv[2] || 'http://127.0.0.1:5173/';
const outDir = join(process.cwd(), 'artifacts', 'renderer-qa');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
await page.goto(baseUrl, { waitUntil: 'networkidle' });

const sheets = await page.evaluate(async () => {
  const { IsoRenderer } = await import(new URL('/client/renderer.js', location.href).href);
  const { BUILDINGS } = await import(new URL('/shared/data.js', location.href).href);
  document.body.replaceChildren();
  Object.assign(document.body.style, { margin: '0', background: '#1e2823' });

  const leaders = [
    'han_xin', 'xiang_yu', 'napoleon_bonaparte', 'ly_thuong_kiet',
    'tran_hung_dao', 'nguyen_hue', 'le_thanh_tong', 'minh_menh',
    'nguyen_anh', 'nguyen_phuc_chu', 'tran_nhan_tong', 'trinh_cuong'
  ];
  const units = [
    'villager', 'king', 'general', 'infantry', 'spearman', 'firearm',
    'cavalry', 'artillery', 'wagon', 'warship', 'transport'
  ];
  const buildingTypes = Object.keys(BUILDINGS);
  const directions = ['E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE'];
  const poses = ['idle', 'walk', 'attack', 'hit', 'death'];

  function scene(width, height) {
    const canvas = document.createElement('canvas');
    const minimap = document.createElement('canvas');
    canvas.width = width; canvas.height = height;
    canvas.style.cssText = `width:${width}px;height:${height}px`;
    minimap.width = minimap.height = 1;
    document.body.append(canvas, minimap);
    const renderer = new IsoRenderer(canvas, minimap);
    renderer.dpr = 1;
    renderer.camera = { x: 128, y: 128, zoom: 1.08 };
    renderer.drawTile = () => {};
    renderer.drawMinimap = () => {};
    renderer.visible = () => true;
    return { canvas, renderer };
  }
  function addLabels(canvas, groups, groupCols, groupW, groupH, cellW, cellH, headH) {
    const c = canvas.getContext('2d');
    c.textBaseline = 'alphabetic';
    for (let i = 0; i < groups.length; i++) {
      const ox = (i % groupCols) * groupW, oy = Math.floor(i / groupCols) * groupH;
      c.fillStyle = '#ead8ac'; c.font = 'bold 12px sans-serif'; c.textAlign = 'left'; c.fillText(groups[i], ox + 4, oy + 13);
      c.font = '10px sans-serif'; c.textAlign = 'center';
      for (let d = 0; d < 8; d++) c.fillText(directions[d], ox + 16 + d * cellW + cellW / 2, oy + 27);
      c.textAlign = 'left';
      for (let s = 0; s < poses.length; s++) c.fillText(poses[s], ox + 2, oy + headH + s * cellH + cellH - 2);
      c.strokeStyle = 'rgba(232,208,151,.28)'; c.strokeRect(ox, oy, groupW - 4, groupH - 4);
    }
  }
  function entity(renderer, px, py, id, type, dir, pose, character) {
    const p = renderer.unproject(px, py);
    const tick = 100;
    return { id, kind: 'unit', type, character, owner: 0, x: p.x, y: p.y, dir, state: pose,
      hp: pose === 'death' ? 0 : 360, maxHp: 360, deadTick: tick - 2,
      hitUntil: pose === 'hit' ? tick + 3 : 0, lastAttack: tick };
  }
  function render(renderer, entities, width, height) {
    renderer.render({ tick: 100, map: { id: 'qa', width: 256, height: 256,
      tiles: Array(256 * 256).fill('plain'), resources: [] }, entities, fog: null }, 0, [], 0);
  }

  // Contact sheet for every leadership identity, eight directions, and five simulation poses.
  const leaderW = 312, leaderH = 230, leaderCellW = 34, leaderCellH = 36, leaderHead = 45;
  const leadersScene = scene(leaderW * 4, leaderH * 3);
  const leadersEntities = [];
  for (let n = 0; n < leaders.length; n++) {
    const ox = (n % 4) * leaderW, oy = Math.floor(n / 4) * leaderH;
    for (let s = 0; s < poses.length; s++) for (let d = 0; d < 8; d++) {
      const px = ox + 16 + d * leaderCellW + leaderCellW / 2;
      const py = oy + leaderHead + s * leaderCellH + leaderCellH - 3;
      leadersEntities.push(entity(leadersScene.renderer, px, py, 1 + n * 40 + s * 8 + d,
        'general', d, poses[s], leaders[n]));
    }
  }
  render(leadersScene.renderer, leadersEntities, leaderW * 4, leaderH * 3);
  addLabels(leadersScene.canvas, leaders, 4, leaderW, leaderH, leaderCellW, leaderCellH, leaderHead);

  // Generic role sheet; the matching leader sheet above exercises all twelve individual styles.
  const unitW = 416, unitH = 260, unitCellW = 40, unitCellH = 37, unitHead = 39;
  const unitCols = 3, unitRows = Math.ceil(units.length / unitCols);
  const unitsScene = scene(unitW * unitCols, unitH * unitRows);
  const unitEntities = [];
  for (let n = 0; n < units.length; n++) {
    const ox = (n % unitCols) * unitW, oy = Math.floor(n / unitCols) * unitH;
    for (let s = 0; s < poses.length; s++) for (let d = 0; d < 8; d++) {
      const px = ox + 20 + d * unitCellW + unitCellW / 2;
      const py = oy + unitHead + s * unitCellH + unitCellH - 3;
      unitEntities.push(entity(unitsScene.renderer, px, py, 1000 + n * 40 + s * 8 + d,
        units[n], d, poses[s], null));
    }
  }
  render(unitsScene.renderer, unitEntities, unitW * unitCols, unitH * unitRows);
  addLabels(unitsScene.canvas, units, unitCols, unitW, unitH, unitCellW, unitCellH, unitHead);

  // Isometric building silhouette sheet at the same 1.08 gameplay zoom.
  const buildingCols = 5, buildingRows = Math.ceil(buildingTypes.length / buildingCols);
  const buildingW = 140, buildingH = 96;
  const buildingsScene = scene(buildingCols * buildingW, buildingRows * buildingH);
  const buildingEntities = [];
  for (let n = 0; n < buildingTypes.length; n++) {
    const px = (n % buildingCols) * buildingW + buildingW / 2;
    const py = Math.floor(n / buildingCols) * buildingH + 67;
    const p = buildingsScene.renderer.unproject(px, py);
    buildingEntities.push({ id: 5000 + n, kind: 'building', type: buildingTypes[n], owner: 0,
      x: p.x, y: p.y, hp: 900, maxHp: 900 });
  }
  render(buildingsScene.renderer, buildingEntities, buildingCols * buildingW, buildingRows * buildingH);
  const bc = buildingsScene.canvas.getContext('2d');
  bc.font = 'bold 11px sans-serif'; bc.textAlign = 'center';
  for (let n = 0; n < buildingTypes.length; n++) {
    const x = (n % buildingCols) * buildingW, y = Math.floor(n / buildingCols) * buildingH;
    bc.fillStyle = '#ead8ac'; bc.fillText(buildingTypes[n], x + buildingW / 2, y + 13);
    bc.strokeStyle = 'rgba(232,208,151,.28)'; bc.strokeRect(x + 2, y + 2, buildingW - 4, buildingH - 4);
  }

  // Real wall-clock samples at 180 ms spacing, showing walk and attack animation over time.
  const temporalTypes = ['villager', 'infantry', 'firearm', 'cavalry', 'artillery', 'warship'];
  const temporalCanvas = document.createElement('canvas');
  const temporalCellW = 88, temporalCellH = 90, temporalGroupW = 300, temporalGroupH = temporalCellH * 2 + 32;
  temporalCanvas.width = temporalGroupW * 3; temporalCanvas.height = temporalGroupH * 2;
  temporalCanvas.style.cssText = `width:${temporalCanvas.width}px;height:${temporalCanvas.height}px`;
  const temporalMap = document.createElement('canvas'); temporalMap.width = temporalMap.height = 1;
  const animationCanvas = document.createElement('canvas');
  animationCanvas.width = temporalCanvas.width; animationCanvas.height = temporalCanvas.height;
  animationCanvas.style.cssText = `width:${temporalCanvas.width}px;height:${temporalCanvas.height}px`;
  document.body.append(temporalCanvas, temporalMap, animationCanvas);
  const temporalRenderer = new IsoRenderer(animationCanvas, temporalMap);
  temporalRenderer.dpr = 1; temporalRenderer.camera = { x: 128, y: 128, zoom: 1.08 };
  temporalRenderer.drawTile = () => {}; temporalRenderer.drawMinimap = () => {}; temporalRenderer.visible = () => true;
  const tc = temporalCanvas.getContext('2d');
  for (let i = 0; i < temporalTypes.length; i++) {
    const gx = i % 3, gy = Math.floor(i / 3), ox = gx * temporalGroupW, oy = gy * temporalGroupH;
    const type = temporalTypes[i];
    tc.fillStyle = '#ead8ac'; tc.font = 'bold 12px sans-serif'; tc.textAlign = 'left'; tc.fillText(type, ox + 4, oy + 13);
    for (let actionIndex = 0; actionIndex < 2; actionIndex++) {
      const pose = actionIndex === 0 ? 'walk' : 'attack';
      const baseY = oy + 24 + actionIndex * temporalCellH;
      tc.font = '10px sans-serif'; tc.fillText(pose, ox + 2, baseY + 14);
      for (let sample = 0; sample < 3; sample++) {
        const left = ox + 34 + sample * temporalCellW;
        const px = left + 40;
        const py = baseY + 50;
        render(temporalRenderer, [entity(temporalRenderer, px, py, 3000 + i, type, 0, pose, null)], temporalCanvas.width, temporalCanvas.height);
        if (sample < 2) await new Promise(resolve => setTimeout(resolve, 180));
        // Render animation frames on a separate canvas so the contact sheet stays intact.
        tc.drawImage(animationCanvas, px - 40, py - 40, 80, 80,
          left, baseY + 10, 80, 80);
      }
    }
    tc.strokeStyle = 'rgba(232,208,151,.28)'; tc.strokeRect(ox, oy, temporalGroupW - 3, temporalGroupH - 3);
  }
  return {
    leaders: leadersScene.canvas.toDataURL('image/png'),
    units: unitsScene.canvas.toDataURL('image/png'),
    buildings: buildingsScene.canvas.toDataURL('image/png'),
    temporal: temporalCanvas.toDataURL('image/png')
  };
});

for (const [name, data] of Object.entries(sheets)) {
  await writeFile(join(outDir, `${name}-qa.png`), Buffer.from(data.split(',')[1], 'base64'));
}
await browser.close();
console.log(`Saved 4 renderer QA sheets under ${outDir}`);
