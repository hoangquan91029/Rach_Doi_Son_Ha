#!/usr/bin/env node
/** Whole-clothed contour authoring only. No source image pixels or runtime output. */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const TAU = Math.PI * 2;
const mod = n => ((n % 1) + 1) % 1;
const n = v => Number(v.toFixed(4));

export function guidePose(config, phase) {
  if (!Number.isFinite(phase)) throw new Error('Finite phase required');
  const p = mod(phase), m = config.motion;
  if (config.direction !== 1 || config.layout.canvas.join(',') !== '256,256') throw new Error('This authored contour family supports D1 at fixed 256 canvas only');
  if (!(m.stanceFraction > 0 && m.stanceFraction < 1) || !(m.frontSoleY > m.rearSoleY)) throw new Error('Resolved contact interval and sole endpoints required');
  const feet = {};
  for (const id of ['A', 'B']) {
    const t = mod(p - m.receivingContacts[id]);
    const stance = t < m.stanceFraction;
    const swingT = stance ? null : (t - m.stanceFraction) / (1 - m.stanceFraction);
    const span = m.frontSoleY - m.rearSoleY;
    const tangent = -span * (1 - m.stanceFraction) / m.stanceFraction;
    // Cubic Hermite swing with stance-matched endpoint velocity; small authored overshoot is intentional.
    const h = swingT;
    const groundY = stance ? m.frontSoleY - span * t / m.stanceFraction : (2*h*h*h-3*h*h+1)*m.rearSoleY + (h*h*h-2*h*h+h)*tangent + (-2*h*h*h+3*h*h)*m.frontSoleY + (h*h*h-h*h)*tangent;
    const lift = stance ? 0 : m.swingLiftPx * Math.sin(Math.PI * swingT)**2;
    feet[id] = { id, laneX: config.physicalLegs[id].laneX, cyclePhase: t, stance, swingT, groundY: n(groundY), lift: n(lift), sole: [config.physicalLegs[id].laneX, n(groundY - lift)], soleLine: [[config.physicalLegs[id].laneX - 10, n(groundY - lift)], [config.physicalLegs[id].laneX + 10, n(groundY - lift)]], calfTopY: n(groundY - lift - (stance ? 33 : 22)), projectedCalfLength: stance ? 33 : 22, foreshortening: stance ? 1 : 22/33 };
  }
  const sway = m.bodySwayPx * Math.sin(TAU * p);
  const bob = -m.bodyBobPx * (1 - Math.cos(2 * TAU * p)) / 2;
  return { phase:p, body:{sway:n(sway), bob:n(bob)}, armSwing:n(m.armSwingPx*Math.cos(TAU*p)), clothLag:n(m.clothLagPx*Math.sin(TAU*p-0.45)), feet, depthOrder: Object.values(feet).sort((a,b)=>a.sole[1]-b.sole[1]).map(f=>f.id), pivot:config.layout.workingPivot, authoringOnly:true };
}
const shape = (d, fill, stroke='#554739', width=.8) => `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${width}" stroke-linejoin="round" stroke-linecap="round"/>`;
const line = (d, color='#7a6851', width=.65) => shape(d,'none',color,width);

function leg(f, sway, bob) {
  const x=f.laneX, y=f.sole[1], top=150+bob;
  // Persistent physical lane; garment curves are redrawn from landmarks each phase.
  const calfLength=f.stance ? 33 : 22;
  const cuffY=y-calfLength;
  const kneeY=Math.min(cuffY-7,(f.stance ? 180 : 174)+bob), kneeX=x+sway*.6;
  return `<g data-physical-leg="${f.id}">${shape(`M ${x-17+sway} ${top} Q ${x-22} ${top+13} ${kneeX-18} ${kneeY-6} Q ${kneeX-17} ${kneeY+7} ${x-10} ${cuffY+1} Q ${x} ${cuffY+5} ${x+10} ${cuffY} Q ${kneeX+20} ${kneeY+5} ${kneeX+17} ${kneeY-8} L ${x+16+sway} ${top} Z`,'#554a41')}
  ${shape(`M ${x-14+sway} ${top+3} Q ${x-17} ${top+22} ${kneeX-12} ${kneeY} Q ${x-5} ${cuffY+2} ${x+3} ${cuffY} L ${x+8} ${cuffY-5} Q ${x-3} ${kneeY-5} ${x-4+sway} ${top+2} Z`,'#716356','none')}
  ${line(`M ${x+9+sway} ${top+9} Q ${x+7} ${kneeY-8} ${x+13} ${kneeY+1} M ${x-13} ${kneeY-2} Q ${x-3} ${kneeY+7} ${x+9} ${kneeY+4}`,'#413a35')}
  ${shape(`M ${x-10} ${cuffY-1} Q ${x} ${cuffY+3} ${x+10} ${cuffY-1} L ${x+7} ${y-11} Q ${x} ${y-7} ${x-8} ${y-12} Z`,'#cfc3a6')}
  ${shape(`M ${x-9} ${cuffY} Q ${x-2} ${cuffY+4} ${x+8} ${cuffY+2} L ${x+5} ${y-12} L ${x+1} ${y-11} Q ${x-2} ${y-23} ${x-9} ${cuffY+8} Z`,'#e7dcc3','none')}
  ${[.18,.38,.58,.78].map(t=>line(`M ${x-8} ${cuffY+t*(calfLength-11)} Q ${x} ${cuffY+t*(calfLength-11)+3} ${x+7} ${cuffY+t*(calfLength-11)+1}`,'#9d8b70')).join('')}
  ${shape(`M ${x-8} ${y-12} Q ${x-11} ${y-9} ${x-11} ${y-4} Q ${x-10} ${y} ${x} ${y} Q ${x+10} ${y} ${x+11} ${y-4} Q ${x+11} ${y-8} ${x+7} ${y-13} Z`,'#715539','#493a2b')}
  ${shape(`M ${x-6} ${y-13} L ${x+6} ${y-13} Q ${x+7} ${y-9} ${x+9} ${y-5} Q ${x+8} ${y-2} ${x} ${y-2} Q ${x-8} ${y-2} ${x-8} ${y-5} Z`,'#bd865d','#76533c',.6)}
  ${[-5,-2,1,4,7].map((d,i)=>line(`M ${x+d} ${y-5} l ${i===0?-1:0} 2.2`,'#754f36',.5)).join('')}
  ${shape(`M ${x-8} ${y-9} Q ${x} ${y-6} ${x+8} ${y-9} L ${x+8} ${y-7} Q ${x} ${y-4} ${x-8} ${y-7} Z`,'#927147','#4a3929',.5)}
  ${shape(`M ${x-4} ${y-13} L ${x-1} ${y-13} L ${x+2} ${y-7} L ${x-1} ${y-6} Z`,'#927147','#4a3929',.5)}
  </g>`;
}
function arm(side, a, sway, bob) {
  const left=side==='A', sign=left?-1:1, x=131+sway+sign*32, d=(left?1:-1)*a;
  const elbow=x+sign*7+d*.3, wrist=x+sign*9+d*.45, handY=145.0+bob+d;
  return `<g data-arm="${side}">${shape(`M ${x-sign*4} ${64.0+bob} Q ${x+sign*8} ${70.0+bob} ${elbow+sign*5} ${95.0+bob+d*.4} Q ${elbow+sign*8} ${100.0+bob+d*.5} ${elbow+sign*4} ${106.0+bob+d*.5} L ${elbow-sign*9} ${107.0+bob+d*.5} Q ${x-sign*10} ${95.0+bob} ${x-sign*11} ${78.0+bob} Z`,'#cbbda0')}
  ${shape(`M ${x+sign*2} ${71.333+bob} Q ${elbow+sign*3} ${93.211+bob+d*.4} ${elbow+sign*3} ${99.0+bob+d*.5} Q ${elbow-sign*3} ${102.0+bob+d*.5} ${elbow-sign*10} ${100.0+bob+d*.5} L ${x-sign*7} ${78.0+bob} Z`,'#e1d4b5','none')}
  ${shape(`M ${elbow-sign*8} ${105.0+bob+d*.5} L ${elbow+sign*4} ${105.0+bob+d*.5} Q ${wrist+sign*1} ${135.0+bob+d} ${wrist+sign*2} ${handY-5} Q ${wrist+sign*4} ${handY+4} ${wrist-sign*1} ${handY+9} Q ${wrist-sign*5} ${handY+10} ${wrist-sign*8} ${handY+5} L ${wrist-sign*9} ${handY-1} L ${wrist-sign*5} ${handY-5} Q ${elbow-sign*10} ${125.0+bob+d} ${elbow-sign*8} ${105.0+bob+d*.5} Z`,'#b57c54')}
  ${line(`M ${wrist-sign*5} ${handY-2} l ${sign*4} 6 M ${wrist-sign*2} ${handY+1} l ${sign*1} 5`,'#7d523b')}
  ${shape(`M ${elbow-sign*10} ${99.0+bob+d*.5} Q ${elbow-sign*2} ${104.0+bob+d*.5} ${elbow+sign*7} ${99.0+bob+d*.5} L ${elbow+sign*6} ${106.0+bob+d*.5} Q ${elbow-sign*2} ${111.0+bob+d*.5} ${elbow-sign*10} ${105.0+bob+d*.5} Z`,'#e0d2b4')}
  ${line(`M ${elbow-sign*9} ${103.0+bob+d*.5} Q ${elbow-sign*2} ${107.0+bob+d*.5} ${elbow+sign*5} ${103.0+bob+d*.5}`)}
  </g>`;
}

export function renderGuide(config, phase) {
 const pose=guidePose(config,phase), {sway:s,bob:b}=pose.body, lag=pose.clothLag;
 // Every path is authored whole-clothing geometry. No <image>, raster, masks or source fragments.
 const garment= `<g data-authoring-layer="whole-tunic">
 ${shape(`M ${115+s} ${59.0+b} Q ${98+s} ${62.176+b} ${94+s} ${77.0+b} L ${104+s} ${105.0+b} L ${99+s+lag} ${135.615+b} L ${96+s+lag} ${159.0+b} L ${108+s+lag} ${162.429+b} L ${111+s+lag} ${149.077+b} L ${109+s+lag} ${170.429+b} Q ${129+s+lag} ${178.0+b} ${149+s+lag} ${172.714+b} L ${154+s+lag} ${159.0+b} L ${162+s+lag} ${169.286+b} L ${168+s+lag} ${163.571+b} L ${158+s+lag} ${126.0+b} L ${157+s} ${105.0+b} L ${166+s} ${77.0+b} Q ${160+s} ${63.235+b} ${146+s} ${59.0+b} Z`,'#d7c8a8')}
 ${shape(`M ${112+s} ${64.294+b} L ${104+s} ${77.0+b} L ${112+s} ${99.75+b} L ${106+s+lag} ${155.0+b} L ${111+s+lag} ${155.0+b} L ${119+s} ${110.5+b} L ${139+s} ${73.824+b} Z`,'#eee1c4','none')}
 ${shape(`M ${148+s} ${71.706+b} L ${155+s} ${77.0+b} L ${151+s} ${105.0+b} L ${162+s+lag} ${162.429+b} L ${156+s+lag} ${159.0+b} L ${143+s} ${119.75+b} L ${142+s} ${101.5+b} Z`,'#b9a788','none')}
 ${shape(`M ${116+s} ${58.0+b} Q ${122+s} ${68.529+b} ${130+s} ${77.875+b} L ${118+s} ${95.375+b} L ${110+s} ${71.706+b} Z`,'#f1e5cc')}
 ${shape(`M ${146+s} ${58.0+b} L ${152+s} ${68.529+b} Q ${136+s} ${94.5+b} ${115+s} ${107.75+b} L ${108+s} ${103.25+b} Q ${133+s} ${79.625+b} ${146+s} ${58.0+b} Z`,'#e9ddc0')}
 ${line(`M ${147+s} ${65.353+b} Q ${129+s} ${92.75+b} ${111+s} ${105.0+b} M ${122+s} ${116.0+b} Q ${118+s+lag} ${153.0+b} ${120+s+lag} ${170.429+b} M ${135+s} ${122.25+b} Q ${143+s+lag} ${155.0+b} ${142+s+lag} ${171.571+b} M ${111+s} ${84.875+b} l -3 10 M ${150+s} ${84.0+b} l 3 12`,'#a38d6f')}
 ${shape(`M ${109+s} ${105.0+b} Q ${130+s} ${110.5+b} ${154+s} ${105.0+b} L ${156+s} ${116.0+b} Q ${131+s} ${126.0+b} ${107+s} ${116.0+b} Z`,'#594a41')}
 ${line(`M ${109+s} ${108.667+b} Q ${134+s} ${117.25+b} ${153+s} ${108.667+b} M ${109+s} ${114.167+b} Q ${128+s} ${111.417+b} ${151+s} ${114.167+b}`,'#8a7665',1.2)}
 ${shape(`M ${147+s} ${109.583+b} Q ${152+s} ${105.0+b} ${157+s} ${111.417+b} L ${155+s} ${122.25+b} L ${164+s+lag} ${159.0+b} L ${153+s+lag} ${165.857+b} L ${147+s+lag} ${123.5+b} L ${141+s+lag} ${163.571+b} L ${150+s+lag} ${169.286+b} L ${146+s+lag} ${175.0+b} L ${136+s+lag} ${170.429+b} L ${143+s} ${116.0+b} Z`,'#66564b')}
 ${line(`M ${151+s} ${114.167+b} Q ${157+s+lag} ${149.077+b} ${158+s+lag} ${159.0+b} M ${146+s} ${119.75+b} l -6 31`,'#8b7867')}
 </g>`;
 const head=`<g data-authoring-layer="head-hat">
 ${shape(`M ${117+s} ${53.0+b} L ${145+s} ${53.0+b} L ${143+s} ${62.0+b} L ${130+s} ${74.0+b} L ${118+s} ${63.0+b} Z`,'#ae754e')}
 ${shape(`M ${115+s} ${37.0+b} Q ${129+s} ${33.0+b} ${146+s} ${38.0+b} L ${145+s} ${55.118+b} Q ${142+s} ${60.941+b} ${132+s} ${62.0+b} Q ${120+s} ${60.412+b} ${117+s} ${55.118+b} Z`,'#bf855a')}
 ${shape(`M ${116+s} ${37.0+b} Q ${130+s} ${36.0+b} ${146+s} ${39.0+b} L ${144+s} ${45.5+b} L ${138+s} ${40.0+b} L ${121+s} ${41.0+b} L ${118+s} ${52.167+b} Z`,'#292923')}
 ${line(`M ${121+s} ${48.0+b} l 6 -1 M ${135+s} ${47.167+b} l 6 1`,'#322b24',1.2)}
 ${line(`M ${123+s} ${50.5+b} l 3 0 M ${135+s} ${50.5+b} l 3 0 M ${131+s} ${49.667+b} l -2 8 4 0`,'#49392b',.9)}
 ${shape(`M ${125+s} ${56.706+b} Q ${131+s} ${55.118+b} ${137+s} ${57.235+b} L ${135+s} ${57.765+b} L ${131+s} ${57.235+b} L ${127+s} ${58.294+b} Z`,'#302c25','none')}
 ${shape(`M ${126+s} ${59.882+b} L ${137+s} ${59.353+b} L ${133+s} ${67.0+b} L ${129+s} ${63.0+b} Z`,'#343129','none')}
 ${shape(`M ${92+s} ${39.0+b} Q ${127+s} ${8.0+b} ${131+s} ${6.0+b} Q ${139+s} ${12.0+b} ${167+s} ${37.0+b} Q ${170+s} ${41.0+b} ${133+s} ${43.0+b} Q ${94+s} ${43.0+b} ${92+s} ${39.0+b} Z`,'#736044')}
 ${shape(`M ${92+s} ${39.0+b} Q ${112+s} ${14.0+b} ${131+s} ${6.0+b} Q ${146+s} ${16.0+b} ${167+s} ${37.0+b} Q ${132+s} ${30.0+b} ${92+s} ${39.0+b} Z`,'#c6a471')}
 ${shape(`M ${102+s} ${35.0+b} L ${131+s} ${8.0+b} L ${139+s} ${32.0+b} Q ${119+s} ${31.0+b} ${102+s} ${35.0+b} Z`,'#d6b782','none')}
 ${[101,111,122,139,150,161].map(x=>line(`M ${131+s} ${8.0+b} L ${x+s} ${36.0+b}`,'#8b6f4a',.55)).join('')}
 ${[18,23,28,33].map(y=>line(`M ${131-(y-6)*1.22+s} ${y+b} Q ${131+s} ${y-3+b} ${131+(y-6)*1.22+s} ${y+b}`,'#92754e',.5)).join('')}
 ${line(`M ${94+s} ${39.0+b} Q ${132+s} ${31.0+b} ${166+s} ${37.0+b}`,'#ead0a1',1.3)}
 ${line(`M ${98+s} ${38.0+b} Q ${129+s} ${43.0+b} ${162+s} ${37.5+b}`,'#b29363',.7)}
 </g>`;
 return `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-label="Unqualified whole clothed Villager D1 authoring guide phase ${pose.phase}"><metadata>AUTHORING_ONLY_UNQUALIFIED; handmade complete garment contours; source inspection only; no final art or runtime qualification.</metadata>${pose.depthOrder.map(id=>leg(pose.feet[id],s,b)).join('')}${arm('A',pose.armSwing,s,b)}${arm('B',pose.armSwing,s,b)}${garment}${head}</svg>`;
}

export function exportGuide(config, output) {
 fs.mkdirSync(output,{recursive:true});
 const poses=Array.from({length:8},(_,i)=>guidePose(config,i/8));
 for(let i=0;i<8;i++) fs.writeFileSync(path.join(output,`F${i}.svg`),renderGuide(config,i/8));
 fs.writeFileSync(path.join(output,'landmarks.json'),JSON.stringify({schema:'rds-clothed-guide-landmarks/v1',status:'AUTHORING_ONLY_UNQUALIFIED',inputPins:{identityMaster:config.identityMaster,view:config.view},canvas:config.layout.canvas,pivot:config.layout.workingPivot,cycleMs:config.motion.cycleMs,solePathSpan:config.motion.frontSoleY-config.motion.rearSoleY,projectedRootTravelPerCycle:(config.motion.frontSoleY-config.motion.rearSoleY)/config.motion.stanceFraction,limitations:config.validationLimits,frames:poses},null,2)+'\n');
 fs.writeFileSync(path.join(output,'preview.html'),`<!doctype html><meta charset="utf-8"><title>Whole clothed authoring guide — unqualified</title><style>body{background:#292b29;color:#eee;font:16px system-ui}canvas{background:#73786d;image-rendering:auto;margin:20px}button{font:inherit}.small{width:${config.layout.presentationCanvasPx}px;height:${config.layout.presentationCanvasPx}px}</style><h1>Whole clothed 2D authoring guide</h1><p>AUTHORING ONLY · no image order · no final art, contact, stride or owner approval.</p><button id="toggle">Pause</button><span id="phase"></span><p>Actual whole canvas ${config.layout.presentationCanvasPx}px and illustrative 256px view. Persistent A/B calf-wrap and sandal lanes; no source pixels.</p><canvas class="small" width="256" height="256"></canvas><canvas width="256" height="256"></canvas><script>const canvases=[...document.querySelectorAll('canvas')], images=Array.from({length:8},(_,i)=>{const a=new Image();a.src='F'+i+'.svg';return a});let running=true,time=0,last;document.querySelector('button').onclick=()=>{running=!running;document.querySelector('button').textContent=running?'Pause':'Resume'};function draw(now){if(last!==undefined&&running)time+=now-last;last=now;const f=Math.floor(time/${config.motion.cycleMs/8})%8;for(const c of canvases){const x=c.getContext('2d');x.clearRect(0,0,256,256);if(images[f].complete)x.drawImage(images[f],0,0)}document.querySelector('#phase').textContent=' F'+f;requestAnimationFrame(draw)}requestAnimationFrame(draw)</script>`);
}
if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
 const args=process.argv.slice(2);if(args.length!==2)throw new Error('Usage: node scripts/whole-clothed-walk-guide.mjs CONFIG_JSON OUTPUT_DIRECTORY');
 const config=JSON.parse(fs.readFileSync(args[0],'utf8'));exportGuide(config,path.resolve(args[1]));
}
