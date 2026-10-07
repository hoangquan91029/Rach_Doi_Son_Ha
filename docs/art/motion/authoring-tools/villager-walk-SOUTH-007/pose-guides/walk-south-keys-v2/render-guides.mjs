import {chromium} from '/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright/index.mjs';
import {readFile,writeFile} from 'node:fs/promises';import {createHash} from 'node:crypto';import {fileURLToPath} from 'node:url';
const dir=new URL('./',import.meta.url),browser=await chromium.launch({headless:true}),page=await browser.newPage({deviceScaleFactor:1});
const receipt={status:'MODEL_ONLY_NON_ART_NO_ANIMATION_QUALIFICATION',browser:browser.version(),imageCalls:0,outputs:[]};
async function capture(name,width,height,html){await page.setViewportSize({width,height});await page.setContent('<style>html,body{margin:0;background:#f2efe5;font-family:sans-serif}</style>'+html);const png=await page.screenshot({path:fileURLToPath(new URL(name+'.png',dir))});receipt.outputs.push({file:name+'.png',width,height,sha256:createHash('sha256').update(png).digest('hex')});}
try{for(const index of [0,2,4,6])for(const qa of ['', '-qa']){const name='F'+index+qa;await capture(name,1254,1254,await readFile(new URL(name+'.svg',dir),'utf8'));}
 const imgs=await Promise.all([0,2,4,6].map(async i=>({i,uri:'data:image/png;base64,'+(await readFile(new URL('F'+i+'-qa.png',dir))).toString('base64')})));
 await capture('contact-sheet-50pct',2508,700,'<h2 style="height:40px;margin:12px">MODEL_ONLY / four keys / anatomical ownership / no motion or art qualification</h2><div style="display:flex">'+imgs.map(({i,uri})=>'<div><img width="627" height="627" src="'+uri+'"/></div>').join('')+'</div>');
 await capture('fixed38-keys',800,200,'<h3 style="margin:14px">MODEL_ONLY / whole-canvas38px / STILL keys only</h3><div style="display:flex;gap:75px;padding:14px">'+imgs.map(({i,uri})=>'<div style="width:110px"><img width="38" height="38" src="'+uri+'"/><p style="font-size:12px">F'+i+' '+(i<4?'LEFT':'RIGHT')+' support</p></div>').join('')+'</div>');
 const plan=JSON.parse(await readFile(new URL('coordinate-plan.json',dir),'utf8'));
 const lines=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="520"><rect width="1000" height="520" fill="#f2efe5"/><text x="25" y="28" font-size="18">MODEL_ONLY world-grid contact diagnostic: same sole stays stationary through support</text>'];
 const px=t=>80+t/600*840,py=d=>95+d*.5;
 for(let t=0;t<=600;t+=150)lines.push(`<path d="M${px(t)} 65V430" stroke="#d0d7c9"/><text x="${px(t)-20}" y="450" font-size="15">${t}ms</text>`);
 lines.push(`<path d="M${px(0)} ${py(0)}L${px(600)} ${py(640)}" stroke="#9b514c" stroke-width="4"/><text x="600" y="380" fill="#9b514c">body/root travel +320 projected sourcepx/cycle</text>`);
 for(const side of ['LEFT','RIGHT']){const color=side==='LEFT'?'#3f8064':'#647ea0';const fs=plan.frames.filter(f=>f.support===side);for(const endpoint of ['worldHeel','worldToe']){const coords=fs.map(f=>`${px(f.timeMs)},${py(f.soles[side][endpoint][1])}`).join(' ');lines.push(`<polyline points="${coords}" stroke="${color}" stroke-width="4" fill="none"/>`);for(const f of fs)lines.push(`<circle cx="${px(f.timeMs)}" cy="${py(f.soles[side][endpoint][1])}" r="6" fill="${color}"/>`);}lines.push(`<text x="${px(fs[0].timeMs)+10}" y="${py(fs[0].soles[side].worldToe[1])+25}" fill="${color}">${side} fixed heel+toe world depth / contact z0</text>`);}
 lines.push('<text x="25" y="486" font-size="15">x=time; y=projected world-ground depth. 600ms nominal review speed0.8465world/s; base2.1 needs241.86ms hypothesis.</text><text x="25" y="509" font-size="15">This is a coordinate check, not animated sprite playback or physical/anatomical qualification.</text></svg>');
 const svg=lines.join('');await writeFile(new URL('world-contact-grid.svg',dir),svg);await capture('world-contact-grid',1000,520,svg);
 await writeFile(new URL('render-receipt.json',dir),JSON.stringify(receipt,null,2)+'\n');
}finally{await browser.close();}
