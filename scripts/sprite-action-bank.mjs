/** Portable candidate packaging of ONE action, exactly eight existing whole-frame clips. */
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {actionSpec} from '../shared/unit-action-spec.js';
import {validateAsset,validateManifest} from '../client/art-assets.js';
import {TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION,NORMAL_ZOOM} from '../client/world-presentation.js';

const sha=data=>createHash('sha256').update(data).digest('hex');
const check=(ok,message)=>{if(!ok)throw Error(message);};
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function readPin(pin,base){
 check(pin&&typeof pin.path==='string'&&/^[a-f0-9]{64}$/.test(pin.sha256),'Missing file pin');
 const file=path.resolve(base,pin.path),bytes=fs.readFileSync(file);
 check(sha(bytes)===pin.sha256,'File SHA mismatch: '+file);return {file,bytes};
}
const pngInfo=files=>JSON.parse(execFileSync('python3',['-c',
 'import json,sys,hashlib; from PIL import Image\nr=[]\nfor p in json.loads(sys.argv[1]):\n im=Image.open(p); im.load(); r.append(dict(path=p,width=im.width,height=im.height,mode=im.mode,alphaExtrema=im.convert("RGBA").getchannel("A").getextrema(),rgbaSha256=hashlib.sha256(im.convert("RGBA").tobytes()).hexdigest()))\nprint(json.dumps(r))',JSON.stringify(files)],{encoding:'utf8',maxBuffer:8*1024*1024}));

/** Registry injection is for fixture tests; the CLI always loads the project registry. */
export function assembleActionBank(config,{registry,base=process.cwd()}={}){
 const spec=actionSpec(config.identity,config.action);
 check(spec.applicable&&!spec.alias,'Assemble the applicable canonical action; declare aliases separately');
 const registryBase=registry?base:fileURLToPath(new URL('../',import.meta.url));
 const registryPath=registry?null:fileURLToPath(new URL(`../docs/art/pipeline/unit-production/${config.identity}/identity.json`,import.meta.url));
 registry??=JSON.parse(fs.readFileSync(new URL(`../docs/art/pipeline/unit-production/${config.identity}/identity.json`,import.meta.url)));
 check(registry.identity===config.identity&&registry.masterAuthority==='original','Verified original identity required');
 check(registry.layoutLock,'Fixed identity family layout required');
 const original=readPin(registry.master,registryBase);
 check(Array.isArray(config.clips)&&config.clips.length===8,'Exactly eight directional clips required');
 const output=path.resolve(base,config.outDir);check(!fs.existsSync(output),'Refuse overwrite');
 const aliases=(config.aliases||[]).map(name=>{const a=actionSpec(config.identity,name);check(a.applicable&&a.alias&&a.action===spec.action,'Invalid shared-clip alias');return {name,canonical:a.action,roles:a.roles};});
 check(new Set(aliases.map(a=>a.name)).size===aliases.length,'Duplicate alias');
 const images=new Map(),pages=new Map(),members=[],directions=new Set(),ids=new Set();let layout;
 const excludedPaths=new Set((registry.excludedReferencePaths||[]).map(p=>path.resolve(registryBase,p)));
 const excludedSHAs=new Set([...excludedPaths].filter(p=>fs.existsSync(p)).map(p=>sha(fs.readFileSync(p))));
 const retainImage=(pin,relativeBase)=>{const p=readPin(pin,relativeBase);check(!excludedPaths.has(p.file)&&!excludedSHAs.has(pin.sha256),'Excluded held/rejected source');const prior=images.get(p.file);check(!prior||prior.sha256===pin.sha256&&prior.rgbaSha256===pin.rgbaSha256&&(prior.width===undefined||pin.width===undefined||prior.width===pin.width&&prior.height===pin.height),'Conflicting source pin');images.set(p.file,{...prior,...pin,path:p.file});return p;};
 retainImage(registry.master,registryBase);
 for(const input of config.clips){
  const descriptor=readPin(input.descriptor,base),jobFile=readPin(input.job,base),receiptFile=readPin(input.receipt,base);
  const asset=validateAsset(JSON.parse(descriptor.bytes)),job=JSON.parse(jobFile.bytes),receipt=JSON.parse(receiptFile.bytes);
  const dir=asset.direction,view=registry.views.find(v=>v.direction===dir);
  check(Number.isInteger(dir)&&dir>=0&&dir<8&&!directions.has(dir),'Missing or duplicate direction');directions.add(dir);
  check(view?.status==='selected'&&view.source,'Locked selected direction required');
  check(asset.kind==='unit'&&registry.families.includes(asset.family)&&asset.state===spec.action&&job.action===spec.action&&job.direction===dir,'Wrong family/action/direction');
  check(!ids.has(asset.id),'Duplicate asset ID');ids.add(asset.id);
  check(asset.identityMasterSHA===registry.master.sha256&&job.masterSHA===view.source.sha256&&job.master?.sha256===view.source.sha256,'Identity/view anchor mismatch');
  check(asset.directionalMasterSHA===undefined?asset.source.sha256===view.source.sha256:asset.directionalMasterSHA===view.source.sha256,'Directional source mismatch');
  check(receipt.mode==='selected'||receipt.mode==='production','Diagnostic or held package cannot join a bank');
  check(receipt.inputJobSHA256===input.job.sha256&&receipt.outputPins?.[path.basename(descriptor.file)]===input.descriptor.sha256,'Compiler receipt binding mismatch');
  check(job.frameCount===asset.frames.length&&job.frames.length===asset.frames.length&&asset.frames.length>=spec.frames,'Static/incomplete clip cannot complete action');
  check(asset.frames.length===spec.frames||typeof config.extraFrameReason==='string'&&config.extraFrameReason.trim(),'Extra frame justification required');
  check(job.frames.every((f,i)=>f.status==='selected'&&f.custody&&f.phase===i/job.frames.length&&f.input.sha256===asset.frames[i].source.sha256&&f.input.rgbaSha256===asset.frames[i].source.rgbaSha256&&f.durationMs===asset.frames[i].durationMs),'Held/phase/source/timing mismatch');
  check(typeof asset.loop==='boolean'&&asset.loop===job.loop&&(spec.action!=='death'||!asset.loop&&asset.frames.reduce((n,f)=>n+f.durationMs,0)<=4000),'Explicit loop/death policy mismatch');
  if(spec.action==='attack')check(asset.frames.flatMap(f=>f.events||[]).filter(e=>['WEAPON_CONTACT','FIRE_PROJECTILE','DEAL_DAMAGE'].includes(e.name)).length===1,'Attack requires one authoritative contact marker');
  check(equal(asset.cell,{width:128,height:128})&&equal(job.cell,asset.cell)&&['separate','baked'].includes(asset.contactShadow.mode)&&equal(job.contactShadow,asset.contactShadow),'Compiler cell/shadow contract mismatch');
  const familyLock=registry.layoutLock;
  check(equal(familyLock.fixedCanvas,job.fixedCanvas)&&equal(familyLock.cell,asset.cell)&&equal(familyLock.pivot,asset.pivot)&&equal(familyLock.render,asset.render)&&equal(familyLock.contactShadow,asset.contactShadow),'Original family layout/shadow mismatch');
  check(asset.runtime.width%132===0&&asset.runtime.height%132===0&&asset.frames.every(f=>f.x%132===2&&f.y%132===2),'Compiler padding/slot contract mismatch');
  const locked=[asset.source.width,asset.source.height,asset.cell,asset.pivot,asset.render,asset.contactShadow,asset.loop,asset.frames.map(f=>[f.durationMs,f.events||[]])];
  check(!layout||equal(layout,locked),'Bank changes family layout/phase timing');layout??=locked;
  check(equal([job.fixedCanvas.width,job.fixedCanvas.height],[asset.source.width,asset.source.height])&&equal(job.pivot,asset.pivot)&&equal(job.render,asset.render),'Job layout mismatch');
  const rawSize={width:asset.source.width,height:asset.source.height};
  retainImage({...registry.master,...rawSize},registryBase);retainImage({...view.source,...rawSize},registryBase);retainImage(asset.source,path.dirname(descriptor.file));const primary=retainImage({...job.master,...rawSize},path.dirname(jobFile.file));check(primary.file===path.resolve(registryBase,view.source.path),'View path mismatch');
  if(job.identityMaster){const anchor=retainImage(job.identityMaster,path.dirname(jobFile.file));check(anchor.file===original.file&&job.identityMaster.sha256===registry.master.sha256,'Original source path mismatch');}
  else check(view.source.sha256===registry.master.sha256,'Directional job requires original anchor');
  for(let i=0;i<job.frames.length;i++){const p=retainImage({...job.frames[i].input,...rawSize},path.dirname(jobFile.file));const source=retainImage(asset.frames[i].source,path.dirname(descriptor.file));check(p.file===source.file,'Frame source path mismatch');}
  const page=retainImage(asset.runtime,path.dirname(descriptor.file));
  check(asset.runtime.width<=2048&&asset.runtime.height<=2048,'Page exceeds 2048');
  check(receipt.outputPins?.[asset.runtime.path]===asset.runtime.sha256,'Atlas receipt mismatch');
  pages.set(asset.runtime.sha256,{...page,width:asset.runtime.width,height:asset.runtime.height});
  members.push({input,asset,descriptorDir:path.dirname(descriptor.file)});
 }
 const shadowIds=[...new Set(members.filter(m=>m.asset.contactShadow.mode==='separate').map(m=>m.asset.contactShadow.assetId))],shadows=[];
 for(const id of shadowIds){const pin=(config.dependencies||[]).find(p=>p.id===id);check(pin,'Missing separate shadow dependency');const desc=readPin(pin.descriptor,base),asset=validateAsset(JSON.parse(desc.bytes));check(asset.id===id&&asset.kind==='vfx'&&asset.direction===null,'Invalid shadow dependency');const page=retainImage(asset.runtime,path.dirname(desc.file));pages.set(asset.runtime.sha256,{...page,width:asset.runtime.width,height:asset.runtime.height});shadows.push(asset);}
 const info=new Map(pngInfo([...images.keys()]).map(i=>[i.path,i]));
 for(const [file,pin] of images){const i=info.get(file);check(i.mode==='RGBA'&&i.rgbaSha256===pin.rgbaSha256,'Decoded RGBA pin mismatch');check(i.alphaExtrema[0]===0&&i.alphaExtrema[1]>0,'Whole transparent nonempty canvas required');if(pin.width!==undefined)check(i.width===pin.width&&i.height===pin.height,'PNG dimensions mismatch');}
 const decodedBytes=[...pages.values()].reduce((n,p)=>n+p.width*p.height*4,0),encodedBytes=[...pages.values()].reduce((n,p)=>n+p.bytes.length,0);
 check(decodedBytes<=128*1024*1024&&encodedBytes<=64*1024*1024,'Action bank exceeds fixed memory budget');
 const assets=[...members.sort((a,b)=>a.asset.direction-b.asset.direction).map(m=>m.asset),...shadows].map(a=>({...a,runtime:{...a.runtime,path:`pages/${a.runtime.sha256}.png`},review:{status:'CANDIDATE'},candidate:true,loadPolicy:a.state==='idle'||shadowIds.includes(a.id)?'eager':'on-demand'}));
 const manifest={schemaVersion:1,status:'CANDIDATE',camera:{projection:'dimetric',ratio:[2,1],tile:[TILE_WIDTH,TILE_HEIGHT],elevation:CAMERA_ELEVATION},assets};validateManifest(manifest);const manifestText=JSON.stringify(manifest,null,2)+'\n';check(Buffer.byteLength(manifestText)<=2*1024*1024,'Manifest exceeds 2MiB');
 fs.mkdirSync(path.dirname(output),{recursive:true});const temp=fs.mkdtempSync(path.join(path.dirname(output),'.sprite-bank-'));
 try{
  fs.mkdirSync(path.join(temp,'pages'));for(const [hash,p] of pages)fs.writeFileSync(path.join(temp,'pages',hash+'.png'),p.bytes);
  fs.writeFileSync(path.join(temp,'manifest.json'),manifestText);
  for(const a of assets.filter(a=>a.kind==='unit'))fs.writeFileSync(path.join(temp,`D${a.direction}.json`),JSON.stringify(a,null,2)+'\n');
  fs.copyFileSync(path.join(temp,'D0.json'),path.join(temp,'asset.json'));
  for(const name of ['master-preview.png','contact-sheet.png']){const pin=JSON.parse(readPin(members[0].input.receipt,base).bytes).outputPins?.[name];check(pin,'Preview custody missing');fs.writeFileSync(path.join(temp,name),readPin({path:path.join(members[0].descriptorDir,name),sha256:pin},base).bytes);}
  fs.copyFileSync(fileURLToPath(new URL('./sprite-preview.html',import.meta.url)),path.join(temp,'index.html'));
  fs.writeFileSync(path.join(temp,'preview-config.json'),JSON.stringify({zoom:NORMAL_ZOOM,mode:'EIGHT_DIRECTION_CANDIDATE',bank:assets.filter(a=>a.kind==='unit').map(a=>({direction:a.direction,path:`D${a.direction}.json`}))})+'\n');
  const outputPins=Object.fromEntries(['manifest.json','asset.json','preview-config.json','index.html','master-preview.png','contact-sheet.png',...assets.filter(a=>a.kind==='unit').map(a=>`D${a.direction}.json`),...[...pages.keys()].map(h=>`pages/${h}.png`)].map(name=>[name,sha(fs.readFileSync(path.join(temp,name)))]));
  const receipt={identity:config.identity,action:spec.action,roles:spec.roles,aliases,packagedDirections:[0,1,2,3,4,5,6,7],visualApproval:false,runtimeQualified:false,installAuthorized:false,decodedBytes,encodedBytes,masterSHA:registry.master.sha256,registryPin:{path:registryPath,sha256:sha(registryPath?fs.readFileSync(registryPath):JSON.stringify(registry)),fixtureOnly:registryPath===null},inputClips:config.clips,outputPins,outputManifestSHA:sha(manifestText)};
  fs.writeFileSync(path.join(temp,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');check(!fs.existsSync(output),'Refuse overwrite');fs.renameSync(temp,output);return receipt;
 }catch(error){fs.rmSync(temp,{recursive:true,force:true});throw error;}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const file=path.resolve(process.argv[2]);console.log(JSON.stringify(assembleActionBank(JSON.parse(fs.readFileSync(file)),{base:path.dirname(file)})));}
 catch(error){console.error(error.message);process.exitCode=1;}
}
