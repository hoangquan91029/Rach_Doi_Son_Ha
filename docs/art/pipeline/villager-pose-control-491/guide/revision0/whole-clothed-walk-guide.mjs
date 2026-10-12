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
    feet[id] = { id, laneX: config.physicalLegs[id].laneX, cyclePhase: t, stance, swingT, groundY: n(groundY), lift: n(lift), sole: [config.physicalLegs[id].laneX, n(groundY - lift)], soleLine: [[config.physicalLegs[id].laneX - 10, n(groundY - lift)], [config.physicalLegs[id].laneX + 10, n(groundY - lift)]], calfTopY: n(groundY - lift - 33) };
  }
  const sway = m.bodySwayPx * Math.sin(TAU * p);
  const bob = -m.bodyBobPx * (1 - Math.cos(2 * TAU * p)) / 2;
  return { phase:p, body:{sway:n(sway), bob:n(bob)}, armSwing:n(m.armSwingPx*Math.cos(TAU*p)), clothLag:n(m.clothLagPx*Math.sin(TAU*p-0.45)), feet, depthOrder: Object.values(feet).sort((a,b)=>a.sole[1]-b.sole[1]).map(f=>f.id), pivot:config.layout.workingPivot, authoringOnly:true };
}
const shape = (d, fill, stroke='#554739', width=.8) => `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${width}" stroke-linejoin="round" stroke-linecap="round"/>`;
const line = (d, color='#7a6851', width=.65) => shape(d,'none',color,width);

function leg(f, sway, bob) {
  const x=f.laneX, y=f.sole[1], top=156+bob;
  // Persistent physical lane; garment curves are redrawn from landmarks each phase.
  const kneeY=Math.min(y-38,195+bob), kneeX=x+sway*.6;
  return `<g data-physical-leg="${f.id}">${shape(`M ${x-17+sway} ${top} Q ${x-22} ${top+13} ${kneeX-18} ${kneeY-6} Q ${kneeX-17} ${kneeY+7} ${x-10} ${y-32} Q ${x} ${y-28} ${x+10} ${y-33} Q ${kneeX+20} ${kneeY+5} ${kneeX+17} ${kneeY-8} L ${x+16+sway} ${top} Z`,'#554a41')}
  ${shape(`M ${x-14+sway} ${top+3} Q ${x-17} ${top+22} ${kneeX-12} ${kneeY} Q ${x-5} ${y-31} ${x+3} ${y-33} L ${x+8} ${y-38} Q ${x-3} ${kneeY-5} ${x-4+sway} ${top+2} Z`,'#716356','none')}
  ${line(`M ${x+9+sway} ${top+9} Q ${x+7} ${kneeY-8} ${x+13} ${kneeY+1} M ${x-13} ${kneeY-2} Q ${x-3} ${kneeY+7} ${x+9} ${kneeY+4}`,'#413a35')}
  ${shape(`M ${x-10} ${y-34} Q ${x} ${y-30} ${x+10} ${y-34} L ${x+7} ${y-11} Q ${x} ${y-7} ${x-8} ${y-12} Z`,'#cfc3a6')}
  ${shape(`M ${x-9} ${y-33} Q ${x-2} ${y-29} ${x+8} ${y-31} L ${x+5} ${y-12} L ${x+1} ${y-11} Q ${x-2} ${y-23} ${x-9} ${y-25} Z`,'#e7dcc3','none')}
  ${[-28,-23,-18,-13].map(d=>line(`M ${x-8} ${y+d} Q ${x} ${y+d+3} ${x+7} ${y+d+1}`,'#9d8b70')).join('')}
  ${shape(`M ${x-8} ${y-12} Q ${x-11} ${y-9} ${x-11} ${y-4} Q ${x-10} ${y} ${x} ${y} Q ${x+10} ${y} ${x+11} ${y-4} Q ${x+11} ${y-8} ${x+7} ${y-13} Z`,'#715539','#493a2b')}
  ${shape(`M ${x-6} ${y-13} L ${x+6} ${y-13} Q ${x+7} ${y-9} ${x+9} ${y-5} Q ${x+8} ${y-2} ${x} ${y-2} Q ${x-8} ${y-2} ${x-8} ${y-5} Z`,'#bd865d','#76533c',.6)}
  ${[-5,-2,1,4,7].map((d,i)=>line(`M ${x+d} ${y-5} l ${i===0?-1:0} 2.2`,'#754f36',.5)).join('')}
  ${shape(`M ${x-8} ${y-9} Q ${x} ${y-6} ${x+8} ${y-9} L ${x+8} ${y-7} Q ${x} ${y-4} ${x-8} ${y-7} Z`,'#927147','#4a3929',.5)}
  ${shape(`M ${x-4} ${y-13} L ${x-1} ${y-13} L ${x+2} ${y-7} L ${x-1} ${y-6} Z`,'#927147','#4a3929',.5)}
  </g>`;
}
function arm(side, a, sway, bob) {
  const left=side==='A', sign=left?-1:1, x=131+sway+sign*32, d=(left?1:-1)*a;
  const elbow=x+sign*7+d*.3, wrist=x+sign*9+d*.45, handY=149+bob+d;
  return `<g data-arm="${side}">${shape(`M ${x-sign*4} ${79+bob} Q ${x+sign*8} ${85+bob} ${elbow+sign*5} ${110+bob+d*.4} Q ${elbow+sign*8} ${116+bob+d*.5} ${elbow+sign*4} ${122+bob+d*.5} L ${elbow-sign*9} ${123+bob+d*.5} Q ${x-sign*10} ${110+bob} ${x-sign*11} ${91+bob} Z`,'#cbbda0')}
  ${shape(`M ${x+sign*2} ${86+bob} Q ${elbow+sign*3} ${108+bob+d*.4} ${elbow+sign*3} ${115+bob+d*.5} Q ${elbow-sign*3} ${118+bob+d*.5} ${elbow-sign*10} ${116+bob+d*.5} L ${x-sign*7} ${91+bob} Z`,'#e1d4b5','none')}
  ${shape(`M ${elbow-sign*8} ${121+bob+d*.5} L ${elbow+sign*4} ${121+bob+d*.5} Q ${wrist+sign*1} ${138+bob+d} ${wrist+sign*2} ${handY-5} Q ${wrist+sign*4} ${handY+4} ${wrist-sign*1} ${handY+9} Q ${wrist-sign*5} ${handY+10} ${wrist-sign*8} ${handY+5} L ${wrist-sign*9} ${handY-1} L ${wrist-sign*5} ${handY-5} Q ${elbow-sign*10} ${133+bob+d} ${elbow-sign*8} ${121+bob+d*.5} Z`,'#b57c54')}
  ${line(`M ${wrist-sign*5} ${handY-2} l ${sign*4} 6 M ${wrist-sign*2} ${handY+1} l ${sign*1} 5`,'#7d523b')}
  ${shape(`M ${elbow-sign*10} ${115+bob+d*.5} Q ${elbow-sign*2} ${120+bob+d*.5} ${elbow+sign*7} ${115+bob+d*.5} L ${elbow+sign*6} ${122+bob+d*.5} Q ${elbow-sign*2} ${127+bob+d*.5} ${elbow-sign*10} ${121+bob+d*.5} Z`,'#e0d2b4')}
  ${line(`M ${elbow-sign*9} ${119+bob+d*.5} Q ${elbow-sign*2} ${123+bob+d*.5} ${elbow+sign*5} ${119+bob+d*.5}`)}
  </g>`;
}

export function renderGuide(config, phase) {
 const pose=guidePose(config,phase), {sway:s,bob:b}=pose.body, lag=pose.clothLag;
 // Every path is authored whole-clothing geometry. No <image>, raster, masks or source fragments.
 const garment= `<g data-authoring-layer="whole-tunic">
 ${shape(`M ${115+s} ${74+b} Q ${98+s} ${77+b} ${94+s} ${91+b} L ${104+s} ${123+b} L ${99+s+lag} ${148+b} L ${96+s+lag} ${164+b} L ${108+s+lag} ${167+b} L ${111+s+lag} ${155+b} L ${109+s+lag} ${174+b} Q ${129+s+lag} ${181+b} ${149+s+lag} ${176+b} L ${154+s+lag} ${164+b} L ${162+s+lag} ${173+b} L ${168+s+lag} ${168+b} L ${158+s+lag} ${143+b} L ${157+s} ${123+b} L ${166+s} ${91+b} Q ${160+s} ${78+b} ${146+s} ${74+b} Z`,'#d7c8a8')}
 ${shape(`M ${112+s} ${79+b} L ${104+s} ${91+b} L ${112+s} ${117+b} L ${106+s+lag} ${160+b} L ${111+s+lag} ${160+b} L ${119+s} ${129+b} L ${139+s} ${88+b} Z`,'#eee1c4','none')}
 ${shape(`M ${148+s} ${86+b} L ${155+s} ${91+b} L ${151+s} ${123+b} L ${162+s+lag} ${167+b} L ${156+s+lag} ${164+b} L ${143+s} ${138+b} L ${142+s} ${119+b} Z`,'#b9a788','none')}
 ${shape(`M ${116+s} ${73+b} Q ${122+s} ${83+b} ${130+s} ${92+b} L ${118+s} ${112+b} L ${110+s} ${86+b} Z`,'#f1e5cc')}
 ${shape(`M ${146+s} ${73+b} L ${152+s} ${83+b} Q ${136+s} ${111+b} ${115+s} ${126+b} L ${108+s} ${121+b} Q ${133+s} ${94+b} ${146+s} ${73+b} Z`,'#e9ddc0')}
 ${line(`M ${147+s} ${80+b} Q ${129+s} ${109+b} ${111+s} ${123+b} M ${122+s} ${135+b} Q ${118+s+lag} ${158+b} ${120+s+lag} ${174+b} M ${135+s} ${140+b} Q ${143+s+lag} ${160+b} ${142+s+lag} ${175+b} M ${111+s} ${100+b} l -3 10 M ${150+s} ${99+b} l 3 12`,'#a38d6f')}
 ${shape(`M ${109+s} ${123+b} Q ${130+s} ${129+b} ${154+s} ${123+b} L ${156+s} ${135+b} Q ${131+s} ${143+b} ${107+s} ${135+b} Z`,'#594a41')}
 ${line(`M ${109+s} ${127+b} Q ${134+s} ${136+b} ${153+s} ${127+b} M ${109+s} ${133+b} Q ${128+s} ${130+b} ${151+s} ${133+b}`,'#8a7665',1.2)}
 ${shape(`M ${147+s} ${128+b} Q ${152+s} ${123+b} ${157+s} ${130+b} L ${155+s} ${140+b} L ${164+s+lag} ${164+b} L ${153+s+lag} ${170+b} L ${147+s+lag} ${141+b} L ${141+s+lag} ${168+b} L ${150+s+lag} ${173+b} L ${146+s+lag} ${178+b} L ${136+s+lag} ${174+b} L ${143+s} ${135+b} Z`,'#66564b')}
 ${line(`M ${151+s} ${133+b} Q ${157+s+lag} ${155+b} ${158+s+lag} ${164+b} M ${146+s} ${138+b} l -6 31`,'#8b7867')}
 </g>`;
 const head=`<g data-authoring-layer="head-hat">
 ${shape(`M ${117+s} ${61+b} L ${145+s} ${61+b} L ${143+s} ${78+b} L ${130+s} ${92+b} L ${118+s} ${79+b} Z`,'#ae754e')}
 ${shape(`M ${115+s} ${43+b} Q ${129+s} ${33+b} ${146+s} ${44+b} L ${145+s} ${65+b} Q ${142+s} ${76+b} ${132+s} ${78+b} Q ${120+s} ${75+b} ${117+s} ${65+b} Z`,'#bf855a')}
 ${shape(`M ${116+s} ${43+b} Q ${130+s} ${36+b} ${146+s} ${45+b} L ${144+s} ${52+b} L ${138+s} ${46+b} L ${121+s} ${47+b} L ${118+s} ${60+b} Z`,'#292923')}
 ${line(`M ${121+s} ${55+b} l 6 -1 M ${135+s} ${54+b} l 6 1`,'#322b24',1.2)}
 ${line(`M ${123+s} ${58+b} l 3 0 M ${135+s} ${58+b} l 3 0 M ${131+s} ${57+b} l -2 8 4 0`,'#49392b',.9)}
 ${shape(`M ${125+s} ${68+b} Q ${131+s} ${65+b} ${137+s} ${69+b} L ${135+s} ${70+b} L ${131+s} ${69+b} L ${127+s} ${71+b} Z`,'#302c25','none')}
 ${shape(`M ${126+s} ${74+b} L ${137+s} ${73+b} L ${133+s} ${83+b} L ${129+s} ${79+b} Z`,'#343129','none')}
 ${shape(`M ${92+s} ${39+b} Q ${127+s} ${8+b} ${131+s} ${6+b} Q ${139+s} ${12+b} ${167+s} ${37+b} Q ${170+s} ${47+b} ${133+s} ${49+b} Q ${94+s} ${49+b} ${92+s} ${39+b} Z`,'#736044')}
 ${shape(`M ${92+s} ${39+b} Q ${112+s} ${14+b} ${131+s} ${6+b} Q ${146+s} ${16+b} ${167+s} ${37+b} Q ${132+s} ${30+b} ${92+s} ${39+b} Z`,'#c6a471')}
 ${shape(`M ${102+s} ${35+b} L ${131+s} ${8+b} L ${139+s} ${32+b} Q ${119+s} ${31+b} ${102+s} ${35+b} Z`,'#d6b782','none')}
 ${[101,111,122,139,150,161].map(x=>line(`M ${131+s} ${8+b} L ${x+s} ${36+b}`,'#8b6f4a',.55)).join('')}
 ${[18,23,28,33].map(y=>line(`M ${131-(y-6)*1.22+s} ${y+b} Q ${131+s} ${y-3+b} ${131+(y-6)*1.22+s} ${y+b}`,'#92754e',.5)).join('')}
 ${line(`M ${94+s} ${39+b} Q ${132+s} ${31+b} ${166+s} ${37+b}`,'#ead0a1',1.3)}
 ${line(`M ${98+s} ${44+b} Q ${129+s} ${49+b} ${162+s} ${42+b}`,'#b29363',.7)}
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
