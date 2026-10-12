import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {assembleActionBank} from '../scripts/sprite-action-bank.mjs';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const pin=file=>({path:file,sha256:hash(fs.readFileSync(file))});
// Colored whole canvases are packaging fixtures, never unit artwork or motion proof.
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'sprite-bank485-'));
const rawPins=JSON.parse(execFileSync('python3',['-c','from PIL import Image,ImageDraw; import json,hashlib,sys; from pathlib import Path\np=Path(sys.argv[1]); out=[]\nfor d in range(8):\n im=Image.new("RGBA",(32,32)); ImageDraw.Draw(im).rectangle((8,8,23,23),fill=(d*20,40,60,255)); f=p/("raw"+str(d)+".png"); im.save(f); out.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),rgbaSha256=hashlib.sha256(im.tobytes()).hexdigest(),width=32,height=32))\nprint(json.dumps(out))',dir],{encoding:'utf8'}));
const config={identity:'infantry',action:'idle',outDir:path.join(dir,'bank'),clips:[],dependencies:[]};
const registry={identity:'infantry',masterAuthority:'original',master:rawPins[0],families:['infantry','unit.infantry'],views:rawPins.map((source,direction)=>({direction,status:'selected',source}))};
registry.layoutLock={fixedCanvas:{width:32,height:32},cell:{width:128,height:128},pivot:{space:'source',x:16,y:27},render:{width:42,height:42},contactShadow:{mode:'separate',assetId:'shadow'},padding:2};
for(let d=0;d<8;d++){
 const file=path.join(dir,`job${d}.json`),output=path.join(dir,`D${d}`);
 const job={schemaVersion:2,id:'fixture-D'+d,family:'infantry',action:'idle',direction:d,master:rawPins[d],masterSHA:rawPins[d].sha256,identityMaster:rawPins[0],fixedCanvas:{width:32,height:32},pivot:{space:'source',x:16,y:27},render:{width:42,height:42},cell:{width:128,height:128},contactShadow:{mode:'separate',assetId:'shadow'},callBudget:{limit:0,used:0},loop:true,frameCount:4,frames:Array.from({length:4},(_,i)=>({phase:i/4,durationMs:100,status:'selected',custody:'FIXTURE_ONLY',input:rawPins[d]})),output:{directory:output,runtimePath:'atlas.png'}};
 fs.writeFileSync(file,JSON.stringify(job));execFileSync('python3',[path.resolve('scripts/sprite-production.py'),file,'--mode','selected']);
 config.clips.push({descriptor:pin(path.join(output,'asset.json')),job:pin(file),receipt:pin(path.join(output,'receipt.json'))});
}
const shadow={id:'shadow',kind:'vfx',family:'shadow',state:'idle',direction:null,source:rawPins[0],runtime:{...rawPins[0],derivation:{method:'copy',sourceSha256:rawPins[0].sha256}},cell:{width:32,height:32},pivot:{space:'source',x:16,y:27},render:{width:42,height:42},alphaPolicy:'transparent',contactShadow:{mode:'none'},candidate:true,review:{status:'CANDIDATE'},frames:[{x:0,y:0,width:32,height:32,durationMs:100}]};
fs.writeFileSync(path.join(dir,'shadow.json'),JSON.stringify(shadow));config.dependencies.push({id:'shadow',descriptor:pin(path.join(dir,'shadow.json'))});
test.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
const clone=()=>structuredClone(config);

test('one portable candidate bank packages all8 locked views and shadow with honest memory/approval',()=>{
 const receipt=assembleActionBank(config,{registry});assert.deepEqual(receipt.packagedDirections,[0,1,2,3,4,5,6,7]);
 assert.equal(receipt.visualApproval,false);assert.equal(receipt.runtimeQualified,false);assert.equal(receipt.installAuthorized,false);
 const manifest=JSON.parse(fs.readFileSync(path.join(config.outDir,'manifest.json')));assert.equal(manifest.assets.length,9);
 assert.equal(manifest.assets.filter(a=>a.kind==='unit').every(a=>a.loadPolicy==='eager'),true);
 for(const a of manifest.assets)assert.equal(hash(fs.readFileSync(path.join(config.outDir,a.runtime.path))),a.runtime.sha256);
 assert.equal(JSON.parse(fs.readFileSync(path.join(config.outDir,'preview-config.json'))).bank.length,8);
 assert.equal(receipt.decodedBytes,8*528*132*4+32*32*4);
 assert.throws(()=>assembleActionBank(config,{registry}),/Refuse overwrite/);
});
test('missing direction, unlocked view, static clip and illegal aliases cannot count complete',()=>{
 let c=clone();c.outDir=path.join(dir,'missing');c.clips.pop();assert.throws(()=>assembleActionBank(c,{registry}),/eight/);
 c=clone();c.outDir=path.join(dir,'unlocked');const r=structuredClone(registry);r.views[7].status='missing';assert.throws(()=>assembleActionBank(c,{registry:r}),/Locked/);
 c=clone();c.outDir=path.join(dir,'static');c.action='attack';assert.throws(()=>assembleActionBank(c,{registry}),/family\/action/);
 c=clone();c.outDir=path.join(dir,'alias');c.aliases=['repair'];assert.throws(()=>assembleActionBank(c,{registry}),/Invalid shared/);
 assert.equal(fs.existsSync(c.outDir),false);
});
test('held sources rejected even when job SHA and receipt were consistently rebound',()=>{
 const c=clone();c.outDir=path.join(dir,'held');const member=c.clips[3],job=JSON.parse(fs.readFileSync(member.job.path));job.frames[2].status='held';
 const file=path.join(dir,'held-job.json');fs.writeFileSync(file,JSON.stringify(job));member.job=pin(file);
 const receipt=JSON.parse(fs.readFileSync(member.receipt.path));receipt.inputJobSHA256=member.job.sha256;
 const receiptFile=path.join(dir,'held-receipt.json');fs.writeFileSync(receiptFile,JSON.stringify(receipt));member.receipt=pin(receiptFile);
 assert.throws(()=>assembleActionBank(c,{registry}),/Held\/phase/);assert.equal(fs.existsSync(c.outDir),false);
});
test('descriptor and decoded image custody tampering fails before creating bank',()=>{
 const c=clone();c.outDir=path.join(dir,'tampered');c.clips[2].descriptor.sha256='0'.repeat(64);assert.throws(()=>assembleActionBank(c,{registry}),/SHA mismatch/);
 const r=structuredClone(registry);r.master.rgbaSha256='0'.repeat(64);
 assert.throws(()=>assembleActionBank({...clone(),outDir:path.join(dir,'rgba')},{registry:r}),/Conflicting source pin|RGBA/);
 assert.equal(fs.existsSync(c.outDir),false);
});
test('explicit excluded raw and rebound baked-shadow package stay rejected',()=>{
 const r=structuredClone(registry);r.excludedReferencePaths=[rawPins[6].path];
 assert.throws(()=>assembleActionBank({...clone(),outDir:path.join(dir,'excluded')},{registry:r}),/Excluded/);
 const c=clone();c.outDir=path.join(dir,'baked');const member=c.clips[2],a=JSON.parse(fs.readFileSync(member.descriptor.path));a.contactShadow={mode:'baked'};
 const file=path.join(path.dirname(member.descriptor.path),'baked.json');fs.writeFileSync(file,JSON.stringify(a));member.descriptor=pin(file);
 const receipt=JSON.parse(fs.readFileSync(member.receipt.path));receipt.outputPins['baked.json']=member.descriptor.sha256;
 const receiptFile=path.join(dir,'baked-receipt.json');fs.writeFileSync(receiptFile,JSON.stringify(receipt));member.receipt=pin(receiptFile);
 assert.throws(()=>assembleActionBank(c,{registry}),/cell\/shadow/);assert.equal(fs.existsSync(c.outDir),false);
});
test('CLI nested config resolves trusted registry sources from project root',()=>{
 const file=path.join(dir,'nested-config.json');fs.writeFileSync(file,JSON.stringify({identity:'infantry',action:'walk',clips:[],outDir:'never-created'}));
 let error;try{execFileSync(process.execPath,[path.resolve('scripts/sprite-action-bank.mjs'),file],{encoding:'utf8',stdio:'pipe'});}catch(e){error=e;}
 assert.ok(error);assert.match(error.stderr,/Exactly eight/);assert.doesNotMatch(error.stderr,/ENOENT/);assert.equal(fs.existsSync(path.join(dir,'never-created')),false);
});
test('original baked shadow bank stays baked without a second shadow dependency',()=>{
 const c=clone();c.outDir=path.join(dir,'baked-family');c.dependencies=[];
 const r=structuredClone(registry);r.layoutLock.contactShadow={mode:'baked'};
 c.clips=c.clips.map((input,d)=>{
  const job=JSON.parse(fs.readFileSync(input.job.path));job.contactShadow={mode:'baked'};
  job.output.directory=path.join(dir,`baked-D${d}`);
  const file=path.join(dir,`baked-job${d}.json`);fs.writeFileSync(file,JSON.stringify(job));
  execFileSync('python3',[path.resolve('scripts/sprite-production.py'),file,'--mode','selected']);
  return {descriptor:pin(path.join(job.output.directory,'asset.json')),job:pin(file),receipt:pin(path.join(job.output.directory,'receipt.json'))};
 });
 const receipt=assembleActionBank(c,{registry:r});
 const manifest=JSON.parse(fs.readFileSync(path.join(c.outDir,'manifest.json')));
 assert.equal(manifest.assets.length,8);assert.ok(manifest.assets.every(a=>a.contactShadow.mode==='baked'));
 assert.equal(receipt.decodedBytes,8*528*132*4);assert.equal(receipt.visualApproval,false);
});
