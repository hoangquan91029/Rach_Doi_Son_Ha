import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,readFileSync,writeFileSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {validateAsset} from '../client/art-assets.js';
import {sampleSpriteAnimation} from '../client/sprite-timing.js';
const compiler=resolve('scripts/sprite-production.py');
function fixture(){
 const dir=mkdtempSync(join(tmpdir(),'sprite471-'));
 const setup=spawnSync('python3',['-c',`from PIL import Image,ImageDraw
import hashlib,json
from pathlib import Path
p=Path(${JSON.stringify(dir)})
im=Image.new('RGBA',(32,32)); ImageDraw.Draw(im).rectangle((8,8,23,23),fill=(90,70,40,255));im.save(p/'raw.png')
pin={'path':'raw.png','sha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest()}
(p/'pin.json').write_text(json.dumps(pin))`],{encoding:'utf8'});
 assert.equal(setup.status,0,setup.stderr);
 const pin=JSON.parse(readFileSync(join(dir,'pin.json')));
 const job={schemaVersion:1,id:'test471',family:'infantry',action:'walk',direction:0,master:pin,masterSHA:pin.sha256,fixedCanvas:{width:32,height:32},pivot:{space:'source',x:16,y:27},render:{width:42,height:42},cell:{width:128,height:128},contactShadow:{mode:'separate',assetId:'shadow'},callBudget:{limit:0,used:0},frameCount:2,frames:[0,0.5].map(phase=>({phase,durationMs:100,status:'held',input:pin})),output:{directory:'output',runtimePath:'atlas.png'}};
 return {dir,job,run(mode='diagnostic'){writeFileSync(join(dir,'job.json'),JSON.stringify(job));return spawnSync('python3',[compiler,join(dir,'job.json'),'--mode',mode],{encoding:'utf8'});},cleanup(){rmSync(dir,{recursive:true,force:true});}};
}
function withFixture(fn){const f=fixture();try{fn(f);}finally{f.cleanup();}}
test('diagnostic whole frames validate against actual runtime schema and preserve input',()=>withFixture(f=>{
 const before=readFileSync(join(f.dir,'raw.png'));const result=f.run();assert.equal(result.status,0,result.stderr);
 const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));assert.equal(validateAsset(asset),asset);
 for(const name of ['preview.html','contact-sheet.png','game-size.png','master-preview.png','preview-config.json'])assert.equal(existsSync(join(f.dir,'output',name)),true);
 assert.match(readFileSync(join(f.dir,'output/preview.html'),'utf8'),/window.previewState/);
 assert.equal(asset.candidate,true);assert.equal(asset.review.status,'CANDIDATE');assert.deepEqual(asset.frames.map(x=>x.x),[2,134]);assert.deepEqual(asset.pivot,f.job.pivot);
 const receipt=JSON.parse(readFileSync(join(f.dir,'output/receipt.json')));assert.ok(receipt.outputPins['working/000.png']);assert.ok(receipt.outputPins['working/001.png']);assert.ok(receipt.outputPins['preview.html']);assert.equal(receipt.visualApproval,false);assert.equal(receipt.installAuthorized,false);assert.deepEqual(receipt.frameStatuses,['held','held']);assert.deepEqual(readFileSync(join(f.dir,'raw.png')),before);
 const raster=spawnSync('python3',['-c',`import importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('validator',${JSON.stringify(resolve('scripts/validate-art-assets.py'))});m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=Path(${JSON.stringify(join(f.dir,'output'))});m.validate_asset(json.loads((p/'asset.json').read_text()),p,p,False)`],{encoding:'utf8'});
 assert.equal(raster.status,0,raster.stderr);
 assert.notEqual(f.run().status,0);
}));
test('selected rejects held, missing custody, and accepts custody without approval',()=>withFixture(f=>{
 assert.match(f.run('selected').stderr,/selected frame/);f.job.frames.forEach(x=>x.status='selected');assert.match(f.run('selected').stderr,/custody/);f.job.frames.forEach(x=>x.custody='record-471');assert.equal(f.run('selected').status,0);
}));
test('encoded and decoded SHA tampering rejected without output',()=>withFixture(f=>{
 const goodSHA=f.job.master.sha256;f.job.master.sha256='0'.repeat(64);assert.match(f.run().stderr,/encoded SHA256/);f.job.master.sha256=goodSHA;
 f.job.masterSHA='0'.repeat(64);assert.match(f.run().stderr,/master SHA/);f.job.masterSHA=f.job.master.sha256;
 f.job.master.rgbaSha256='0'.repeat(64);assert.match(f.run().stderr,/decoded RGBA SHA/);assert.equal(existsSync(join(f.dir,'output')),false);
}));
test('missing frames and per-frame pivot/scale rejected',()=>withFixture(f=>{
 f.job.frames[1].input={...f.job.master,path:'missing.png'};assert.notEqual(f.run().status,0);assert.equal(existsSync(join(f.dir,'output')),false);f.job.frames[1].input=f.job.master;
 f.job.frameCount=3;assert.match(f.run().stderr,/missing frame/);f.job.frameCount=2;f.job.frames[0].pivot={x:12,y:20};assert.match(f.run().stderr,/per-frame/);delete f.job.frames[0].pivot;f.job.render.height=41;assert.match(f.run().stderr,/scale/);
}));
test('decoded budget deduplicates pages but rejects oversized bank',()=>withFixture(f=>{
 const page={path:'same.png',sha256:'a'.repeat(64),width:4096,height:4096};f.job.otherDecodedPages=[page,page];assert.equal(f.run().status,0);
 f.job.output.directory='oversize';f.job.otherDecodedPages.push({...page,path:'second.png'});assert.match(f.run().stderr,/128 MiB/);assert.equal(existsSync(join(f.dir,'oversize')),false);
}));
test('production walk needs qualified record and measured distance',()=>withFixture(f=>{
 f.job.frames.forEach(x=>{x.status='selected';x.custody='selected471';});assert.match(f.run('production').stderr,/qualified record/);
 const qualification={status:'qualified',masterSHA:f.job.masterSHA,family:f.job.family,action:f.job.action,direction:f.job.direction,frameSHAs:f.job.frames.map(x=>x.input.sha256),distancePerCycle:12};
 const record=JSON.stringify(qualification);writeFileSync(join(f.dir,'qualification.json'),record);
 f.job.qualification={status:'qualified',record:'qualification.json',sha256:createHash('sha256').update(record).digest('hex')};
 assert.match(f.run('production').stderr,/measured distance/);
 f.job.locomotion={distancePerCycle:11,measurementRecord:'qualification.json'};assert.match(f.run('production').stderr,/measured distance/);
 f.job.locomotion.distancePerCycle=12;assert.equal(f.run('production').status,0);
 const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));validateAsset(asset);assert.equal(asset.review.status,'CANDIDATE');
 f.job.output.directory='wrong-cycle';f.job.direction=1;assert.match(f.run('production').stderr,/bind this cycle/);
}));
test('death defaults to nonlooping terminal clip and rejects looping or long death',()=>withFixture(f=>{
 f.job.action='death';assert.equal(f.run().status,0);const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));assert.equal(asset.loop,false);validateAsset(asset);assert.equal(sampleSpriteAnimation(asset.frames,{timeMs:9000,loop:asset.loop}).frame,asset.frames.length-1);
 f.job.output.directory='invalid-death';f.job.loop=true;assert.match(f.run().stderr,/death must be nonlooping/);f.job.loop=false;f.job.frames[0].durationMs=4000;assert.match(f.run().stderr,/4000ms/);
}));
test('layout override, frame events and provisional locomotion preserved',()=>withFixture(f=>{
 f.job.layout={columns:1};f.job.frames[0].events=[{name:'CONTACT',offsetMs:99}];f.job.locomotion={distancePerCycle:7};assert.equal(f.run().status,0);
 const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));validateAsset(asset);assert.equal(asset.frames[1].x,2);assert.equal(asset.frames[1].y,134);assert.deepEqual(asset.frames[0].events,f.job.frames[0].events);assert.equal(asset.locomotion.status,'PROVISIONAL');
 f.job.output.directory='invalid-event';f.job.frames[0].events[0].offsetMs=100;assert.match(f.run().stderr,/event marker/);f.job.frames[0].events=[];f.job.layout.columns=17;assert.match(f.run().stderr,/columns/);
}));
test('new schema requires explicit loop and supports ability/load/unload/build/work',()=>withFixture(f=>{
 f.job.schemaVersion=2;assert.match(f.run().stderr,/explicit loop/);f.job.loop=false;
 for(const action of ['ability','load','unload','build','work']){f.job.action=action;f.job.output.directory=action;assert.equal(f.run().status,0);const asset=JSON.parse(readFileSync(join(f.dir,action,'asset.json')));assert.equal(asset.state,action);assert.equal(asset.loop,false);validateAsset(asset);}
}));
test('atlas cap and pinned reusable direction-bank preview',()=>withFixture(f=>{
 f.job.layout={columns:16};assert.match(f.run().stderr,/columns/);f.job.layout={columns:1};f.job.frames=Array.from({length:16},(_,i)=>({...f.job.frames[0],phase:i/16}));f.job.frameCount=16;assert.match(f.run().stderr,/2048px/);
 f.job.frames=f.job.frames.slice(0,2);f.job.frameCount=2;assert.equal(f.run().status,0);
 const descriptor=readFileSync(join(f.dir,'output/asset.json'));f.job.previewBank=[{path:'output/asset.json',sha256:createHash('sha256').update(descriptor).digest('hex')}];f.job.output.directory='bank';f.job.direction=1;assert.equal(f.run().status,0);const config=JSON.parse(readFileSync(join(f.dir,'bank/preview-config.json')));assert.equal(config.bank[0].direction,0);assert.equal(config.bank[0].path,'../output/asset.json');
 f.job.output.directory='tampered-bank';f.job.previewBank[0].sha256='0'.repeat(64);assert.match(f.run().stderr,/bank descriptor SHA/);assert.equal(existsSync(join(f.dir,'tampered-bank')),false);
}));
function differentView(f,size=32){
 const result=spawnSync('python3',['-c',`from PIL import Image
import hashlib,json
from pathlib import Path
p=Path(${JSON.stringify(f.dir)});im=Image.new('RGBA',(${size},${size}),(30,100,160,255));im.save(p/'view.png')
(p/'view-pin.json').write_text(json.dumps({'path':'view.png','sha256':hashlib.sha256((p/'view.png').read_bytes()).hexdigest(),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest()}))`],{encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);return JSON.parse(readFileSync(join(f.dir,'view-pin.json')));
}
test('schema2 shares original identity anchor across distinct directional masters and preview clips',()=>withFixture(f=>{
 f.job.schemaVersion=2;f.job.loop=true;f.job.identityMaster={...f.job.master};
 assert.equal(f.run().status,0);
 const original=readFileSync(join(f.dir,'output/asset.json'));
 const view=differentView(f);f.job.master=view;f.job.masterSHA=view.sha256;f.job.direction=1;f.job.frames.forEach(x=>x.input=view);
 f.job.previewBank=[{path:'output/asset.json',sha256:createHash('sha256').update(original).digest('hex')}];f.job.output.directory='view';
 const result=f.run();assert.equal(result.status,0,result.stderr);
 const asset=JSON.parse(readFileSync(join(f.dir,'view/asset.json')));
 assert.equal(asset.identityMasterSHA,f.job.identityMaster.sha256);assert.equal(asset.directionalMasterSHA,view.sha256);assert.equal(asset.source.sha256,view.sha256);
 const preview=spawnSync('python3',['-c',`from PIL import Image
from pathlib import Path
p=Path(${JSON.stringify(f.dir)});actual=Image.open(p/'view/master-preview.png');original=Image.open(p/'raw.png').resize((128,128),Image.Resampling.LANCZOS);direction=Image.open(p/'view.png').resize((128,128),Image.Resampling.LANCZOS)
assert actual.tobytes()==original.tobytes()
assert actual.tobytes()!=direction.tobytes()`],{encoding:'utf8'});
 assert.equal(preview.status,0,preview.stderr);
 assert.deepEqual(JSON.parse(readFileSync(join(f.dir,'view/receipt.json'))).identityMaster.sha256,f.job.identityMaster.sha256);
 assert.equal(JSON.parse(readFileSync(join(f.dir,'view/preview-config.json'))).bank[0].direction,0);
}));
test('identity anchor rejects bad pins, wrong canvas and schema1 before creating output',()=>withFixture(f=>{
 f.job.identityMaster={...f.job.master};assert.match(f.run().stderr,/requires schema 2/);
 f.job.schemaVersion=2;f.job.loop=true;f.job.identityMaster.sha256='0'.repeat(64);assert.match(f.run().stderr,/encoded SHA256/);
 f.job.identityMaster={...f.job.master,rgbaSha256:'0'.repeat(64)};assert.match(f.run().stderr,/decoded RGBA SHA256/);
 f.job.identityMaster=differentView(f,16);assert.match(f.run().stderr,/fixed canvas/);assert.equal(existsSync(join(f.dir,'output')),false);
}));
test('production qualification binds explicit original identity anchor in addition to directional master',()=>withFixture(f=>{
 f.job.schemaVersion=2;f.job.loop=true;f.job.identityMaster={...f.job.master};const view=differentView(f);f.job.master=view;f.job.masterSHA=view.sha256;f.job.direction=1;
 f.job.frames.forEach(x=>{x.input=view;x.status='selected';x.custody='fixture';});
 const qualification={status:'qualified',masterSHA:view.sha256,family:f.job.family,action:'walk',direction:1,frameSHAs:f.job.frames.map(x=>x.input.sha256),distancePerCycle:1};
 function bind(){const record=JSON.stringify(qualification);writeFileSync(join(f.dir,'qualification.json'),record);f.job.qualification={status:'qualified',record:'qualification.json',sha256:createHash('sha256').update(record).digest('hex')};}
 f.job.locomotion={distancePerCycle:1,measurementRecord:'qualification.json'};bind();assert.match(f.run('production').stderr,/bind identity master/);
 qualification.identityMasterSHA=view.sha256;bind();assert.match(f.run('production').stderr,/bind identity master/);
 qualification.identityMasterSHA=f.job.identityMaster.sha256;bind();const result=f.run('production');assert.equal(result.status,0,result.stderr);
}));
test('legacy master remains identity and directional anchor without optional pin',()=>withFixture(f=>{
 const result=f.run();assert.equal(result.status,0,result.stderr);const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));
 assert.equal(asset.identityMasterSHA,f.job.masterSHA);assert.equal(asset.directionalMasterSHA,f.job.masterSHA);
}));

test('whole baked-shadow candidate preserves its own shadow and rejects missing ground shadow',()=>withFixture(f=>{
 f.job.contactShadow={mode:'baked'};const result=f.run();assert.equal(result.status,0,result.stderr);
 const asset=JSON.parse(readFileSync(join(f.dir,'output/asset.json')));validateAsset(asset);assert.deepEqual(asset.contactShadow,{mode:'baked'});assert.equal(Object.hasOwn(asset.contactShadow,'assetId'),false);
 for(const contactShadow of [{mode:'none'},{mode:'unknown'},{mode:'separate'},{mode:'separate',assetId:''}]){
  f.job.output.directory='invalid-shadow';f.job.contactShadow=contactShadow;assert.match(f.run().stderr,/grounded baked or separate shadow/);assert.equal(existsSync(join(f.dir,'invalid-shadow')),false);
 }
}));
