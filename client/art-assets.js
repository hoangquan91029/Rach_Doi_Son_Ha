import {validateFortificationArt,validateFortificationVariants} from './fortification-art.js';
import {withLoadingDeadline} from './loading-deadline.js';
import {sampleSpriteAnimation,validateFrameEvents} from './sprite-timing.js';
import {TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION} from './world-presentation.js';
/** Raster packaging/loading only. Neither successful decode nor hashes grant visual approval. */
const SHA256=/^[a-f0-9]{64}$/i;
const KINDS=new Set(['unit','building','prop','vfx','terrain','ui','portrait']);
const finitePositive=n=>Number.isFinite(n)&&n>0;
const dimensions=(v,label)=>{if(!v||!Number.isSafeInteger(v.width)||!Number.isSafeInteger(v.height)||v.width<1||v.height<1||v.width>16384||v.height>16384||v.width*v.height>32*1024*1024)throw Error(`${label}: invalid dimensions`);};
const samePivot=(a,b)=>a.x===b.x&&a.y===b.y&&a.space===b.space;
// Legacy aliases can have different export resolutions, but cannot change world geometry.
export function familyLayoutIdentity(asset){return `${asset.kind}:${asset.family.replace(new RegExp(`^${asset.kind}\\.`),'')}`;}
const geometryScalars=asset=>[asset.source.width,asset.source.height,asset.pivot.x,asset.pivot.y,asset.pivot.space,asset.render.width,asset.render.height];
const strictFamilyLayout=asset=>JSON.stringify([...geometryScalars(asset),asset.cell.width,asset.cell.height]);
export function logicalFamilyLayout(asset){return JSON.stringify([...geometryScalars(asset),asset.cell.width/asset.cell.height]);}
function validateAsset(asset) {
 if(!asset||typeof asset.id!=='string'||!/^[a-zA-Z0-9_.-]{1,120}$/.test(asset.id)||!KINDS.has(asset.kind))throw Error('Invalid asset ID or kind');
 for(const [label,file] of [['source',asset.source],['runtime',asset.runtime]]){dimensions(file,label);if(typeof file.path!=='string'||!SHA256.test(file.sha256)||!SHA256.test(file.rgbaSha256))throw Error(`${label}: missing path or SHA256 custody`);}
 dimensions(asset.cell,'cell');if(asset.cell.width/asset.source.width!==asset.cell.height/asset.source.height)throw Error('Anisotropic per-asset camera fitting forbidden');if(asset.cell.width>asset.runtime.width||asset.cell.height>asset.runtime.height)throw Error('Cell exceeds runtime sheet');
 if(!asset.pivot||asset.pivot.space!=='source'||![asset.pivot.x,asset.pivot.y].every(Number.isFinite)||asset.pivot.x<0||asset.pivot.y<0||asset.pivot.x>asset.source.width||asset.pivot.y>asset.source.height)throw Error('Invalid fixed source pivot');
 if(!asset.render||!finitePositive(asset.render.width)||!finitePositive(asset.render.height)||Math.abs(asset.render.width/asset.render.height-asset.cell.width/asset.cell.height)>1e-6)throw Error('Invalid or distorted logical render size');
 if(!['transparent','opaque'].includes(asset.alphaPolicy)||(asset.alphaPolicy==='opaque'&&asset.kind!=='terrain'))throw Error('Opaque assets permitted only for terrain material');
 if(!asset.contactShadow||!['baked','separate','none'].includes(asset.contactShadow.mode))throw Error('Missing contact shadow declaration');
 if(['unit','building','prop'].includes(asset.kind)&&asset.contactShadow.mode==='none')throw Error('Grounded art requires a shadow');
 if(asset.contactShadow.mode==='separate'&&typeof asset.contactShadow.assetId!=='string')throw Error('Missing separate shadow asset ID');
 if(!['CANDIDATE','APPROVED','REJECTED','PLACEHOLDER_ONLY'].includes(asset.review?.status)||typeof asset.candidate!=='boolean')throw Error('Explicit review status/candidate flag required');
 if(asset.review.status==='APPROVED'&&(asset.candidate||typeof asset.review.reviewer!=='string'||!asset.review.reviewer||typeof asset.review.receipt!=='string'||!asset.review.receipt))throw Error('Approval requires noncandidate flag, reviewer and receipt');
 if(typeof asset.state!=='string'||!(asset.direction===null||Number.isInteger(asset.direction)&&asset.direction>=0&&asset.direction<=7))throw Error('Explicit state/direction required');
 if(!Array.isArray(asset.frames)||asset.frames.length<1||asset.frames.length>256)throw Error('Missing frames');
 const occupied=[];for(const frame of asset.frames){if(![frame.x,frame.y,frame.width,frame.height].every(Number.isSafeInteger)||frame.x<0||frame.y<0||frame.width!==asset.cell.width||frame.height!==asset.cell.height||frame.x+frame.width>asset.runtime.width||frame.y+frame.height>asset.runtime.height||(!finitePositive(frame.durationMs)||frame.durationMs>60000))throw Error('Invalid runtime frame cell');if(occupied.some(r=>frame.x<r.x+r.width&&frame.x+frame.width>r.x&&frame.y<r.y+r.height&&frame.y+frame.height>r.y))throw Error('Overlapping frame cells');occupied.push(frame);validateFrameEvents(frame);if(frame.pivot&&!samePivot(frame.pivot,asset.pivot))throw Error('Per-frame pivot fitting forbidden');if(asset.frames.length>1){dimensions(frame.source,'frame source');if(typeof frame.source.path!=='string'||!frame.source.path||frame.source.width!==asset.source.width||frame.source.height!==asset.source.height||!SHA256.test(frame.source.sha256)||!SHA256.test(frame.source.rgbaSha256))throw Error('Frame source must retain locked canvas/custody');}}
 if(asset.loadPolicy!==undefined&&!['eager','on-demand'].includes(asset.loadPolicy))throw Error('Invalid raster load policy');
 if(asset.loop!==undefined&&typeof asset.loop!=='boolean')throw Error('Invalid animation loop declaration');
 if(asset.locomotion&&(!(Number.isFinite(asset.locomotion.distancePerCycle)&&asset.locomotion.distancePerCycle>0)||asset.state!=='walk'))throw Error('Invalid locomotion distance cycle');
 const derivation=asset.runtime.derivation;if(derivation?.method==='copy'&&(asset.frames.length!==1||asset.cell.width!==asset.source.width||asset.cell.height!==asset.source.height))throw Error('Copy must preserve original canvas');if(derivation?.method==='resize'&&asset.frames.length!==1)throw Error('Multi-frame derivative must declare atlas');if(derivation?.method!=='copy'&&derivation?.filter!=='lanczos')throw Error('Derived raster requires declared lanczos filter');if(!derivation||!['copy','resize','atlas'].includes(derivation.method)||derivation.sourceSha256!==asset.source.sha256)throw Error('Missing runtime derivation provenance');
 validateFortificationArt(asset);
 return asset;
}
function validateManifest(manifest) {
 if(!manifest||manifest.schemaVersion!==1||!['CANDIDATE','APPROVED'].includes(manifest.status)||!Array.isArray(manifest.assets)||manifest.assets.length>4096)throw Error('Unsupported raster manifest');
 const c=manifest.camera;if(c?.projection!=='dimetric'||JSON.stringify(c.ratio)!=='[2,1]'||JSON.stringify(c.tile)!==JSON.stringify([TILE_WIDTH,TILE_HEIGHT])||(!Number.isFinite(c.elevation)||Math.abs(c.elevation-CAMERA_ELEVATION)>0.001))throw Error('Camera contract mismatch');
 const ids=new Set();for(const a of manifest.assets){if(ids.has(a.id))throw Error(`Duplicate asset ID: ${a.id}`);ids.add(a.id);}
 validateFortificationVariants(manifest.assets);
 return manifest;
}
async function digest(buffer) {
 if(!globalThis.crypto?.subtle)throw Error('Runtime hash verification needs a secure browser context');
 return [...new Uint8Array(await crypto.subtle.digest('SHA-256',buffer))].map(x=>x.toString(16).padStart(2,'0')).join('');
}
async function decodeImage(bytes,url) {
 const blob=new Blob([bytes]);
 if(typeof createImageBitmap==='function')return createImageBitmap(blob);
 const objectUrl=URL.createObjectURL(blob);try{const image=new Image();image.src=objectUrl;await image.decode();return image;}finally{URL.revokeObjectURL(objectUrl);}
}
/** Renderer calls get(id,{state,direction,timeMs}) and draws its image/cell at returned fixed pivot. */
export function createArtAssetPipeline({manifestUrl='/assets/art-v1/manifest.json',allowCandidates=false,fetchImpl=globalThis.fetch,onStatus=()=>{},maxImageBytes=32*1024*1024,maxDecodedBytes=128*1024*1024,resourceTimeoutMs=30000,preloadTimeoutMs=60000,unitActionPolicy='manifest'}={}) {
 if(!['manifest','on-demand'].includes(unitActionPolicy))throw Error('Invalid unit action policy');
 if(!Number.isSafeInteger(maxDecodedBytes)||maxDecodedBytes<1)throw Error('Invalid decoded RGBA byte budget');
 let encodedStore={records:new Map(),manifests:new Map(),bytes:0,maxBytes:64*1024*1024},selectedIds=null;
 const encodedOwner=Symbol('art-pipeline');
 const releaseEncodedOwnership=()=>{for(const record of encodedStore.records.values())record.requiredOwners?.delete(encodedOwner);};
 const available=new Map(),eagerIds=new Set(),eagerKeys=new Set(),pending=new Map(),controllers=new Set(),pinTimers=new Set();let access=0,queue=Promise.resolve();
 const loaded=new Map(),cache=new Map(),fallbacks=new Set(),familyLayouts=new Map(),logicalLayouts=new Map();let manifest=null,disposed=false,preloadPromise=null,deadlineAt=Infinity;
 const stats={unitActionPolicy,status:'PLACEHOLDER_ONLY',manifest:'not-loaded',declared:0,ready:0,approved:0,candidates:0,failed:0,skipped:0,fallbacks:0,decodedBudgetBytes:maxDecodedBytes,retainedDecodedBytes:0,reservedDecodedBytes:0,uniqueDecodedImages:0,encodedReady:0,retainedEncodedBytes:0,encodedBudgetBytes:64*1024*1024,selectedDeclared:0,eagerDeclared:0,deferredDeclared:0,pending:0,pageErrors:[],evictedPages:0,evictedEncodedPages:0,failures:[]};
 const notify=()=>{stats.fallbacks=fallbacks.size;try{onStatus({...stats,failures:[...stats.failures]});}catch{}};
 const baseUrl=new URL(manifestUrl,globalThis.location?.href||'http://localhost/');
 const runtimeUrl=a=>{if(a.runtime.path.startsWith('/')||a.runtime.path.includes('\\')||a.runtime.path.split('/').includes('..')||/^[a-z]+:/i.test(a.runtime.path))throw Error('Runtime path must be manifest-relative');const url=new URL(a.runtime.path,baseUrl);const directory=new URL('.',baseUrl).pathname;if(url.origin!==baseUrl.origin||!url.pathname.startsWith(directory)||url.search||url.hash)throw Error('Runtime raster must remain within manifest directory');return url.href;};
 const bounded=(label,action,{paging=false}={})=>withLoadingDeadline(async signal=>{
  const controller=new AbortController();controllers.add(controller);const abort=()=>controller.abort();signal.addEventListener('abort',abort,{once:true});if(disposed||signal.aborted)controller.abort();
  try{return await action(controller.signal);}finally{controllers.delete(controller);signal.removeEventListener('abort',abort);}
 },{label,timeoutMs:paging?resourceTimeoutMs:Math.min(resourceTimeoutMs,Math.max(1,deadlineAt-Date.now()))});
 const pageKey=a=>`${runtimeUrl(a)}|${a.runtime.sha256.toLowerCase()}`;
 // Encoded menu warming preserves legacy offline coverage independently of match decode policy.
 const mandatoryEager=a=>a.state==='idle'||['terrain','ui','portrait'].includes(a.kind);
 const warmEncoded=a=>a.loadPolicy!=='on-demand'||mandatoryEager(a);
 const decodeEager=a=>mandatoryEager(a)||(warmEncoded(a)&&!(unitActionPolicy==='on-demand'&&a.kind==='unit'));
 const configure=active=>{releaseEncodedOwnership();available.clear();eagerIds.clear();eagerKeys.clear();for(const a of active)available.set(a.id,a);
  for(const a of active)if(decodeEager(a))eagerIds.add(a.id);
  for(const a of available.values())if(a.contactShadow?.mode==='separate'){const shadow=manifest.assets.find(x=>x.id===a.contactShadow.assetId);if(!shadow)throw Error('Missing separate shadow asset');available.set(shadow.id,shadow);eagerIds.add(shadow.id);}
  for(const id of eagerIds)eagerKeys.add(pageKey(available.get(id)));for(const key of eagerKeys){const record=encodedStore.records.get(key);if(record){record.requiredOwners??=new Set();record.requiredOwners.add(encodedOwner);}}stats.eagerDeclared=eagerIds.size;stats.deferredDeclared=available.size-eagerIds.size;
 };
 const evictFor=bytes=>{for(const [key,record] of [...cache].sort((a,b)=>a[1].lastUsed-b[1].lastUsed)){
  if(bytes<=maxDecodedBytes-stats.retainedDecodedBytes-stats.reservedDecodedBytes)break;
  if(eagerKeys.has(key)||!record.image||record.pinned)continue;
  for(const [id,entry] of loaded)if(pageKey(entry.asset)===key){loaded.delete(id);stats.ready--;stats[entry.approved?'approved':'candidates']--;}
  release(record);cache.delete(key);stats.evictedPages++;
 }};
 const release=record=>{if(record.reserved){stats.reservedDecodedBytes-=record.bytes;record.reserved=false;}if(record.image){record.image.close?.();record.image=null;stats.retainedDecodedBytes-=record.bytes;stats.uniqueDecodedImages--;}};
 const touchEncoded=key=>{const record=encodedStore.records.get(key);if(record)record.lastUsed=encodedStore.access=(encodedStore.access||0)+1;};
 const evictEncodedFor=bytes=>{for(const [key,record] of [...encodedStore.records].sort((a,b)=>(a[1].lastUsed||0)-(b[1].lastUsed||0))){
  if(bytes<=encodedStore.maxBytes-encodedStore.bytes)break;
  if(record.requiredOwners?.size||record.loading||record.users||!record.bytes||eagerKeys.has(key)||cache.get(key)?.pinned||[...pending.keys()].some(id=>available.has(id)&&pageKey(available.get(id))===key))continue;
  encodedStore.records.delete(key);encodedStore.bytes-=record.bytes;stats.evictedEncodedPages++;
 }stats.retainedEncodedBytes=encodedStore.bytes;};
 const encoded=async(a,signal)=>{
  const url=runtimeUrl(a),key=`${url}|${a.runtime.sha256.toLowerCase()}`;
  if(!encodedStore.records.has(key)){
   const record={promise:null,bytes:0,loading:true,users:0,requiredOwners:new Set(),lastUsed:0};record.promise=(async()=>{try{const response=await fetchImpl(url,{credentials:'same-origin',signal});if(!response.ok)throw Error(`Raster HTTP ${response.status}`);const bytes=await response.arrayBuffer();if(bytes.byteLength>maxImageBytes)throw Error('Raster exceeds byte budget');if(await digest(bytes)!==a.runtime.sha256.toLowerCase())throw Error('Runtime encoded SHA256 mismatch');if(signal?.aborted||disposed)throw Error('Art pipeline disposed or loading expired');if(bytes.byteLength>encodedStore.maxBytes)throw Error('Encoded bank byte budget exceeded');evictEncodedFor(bytes.byteLength);if(bytes.byteLength>encodedStore.maxBytes-encodedStore.bytes)throw Error('Encoded bank byte budget exceeded');record.bytes=bytes.byteLength;encodedStore.bytes+=bytes.byteLength;record.loading=false;return bytes;}catch(error){if(encodedStore.records.get(key)===record)encodedStore.records.delete(key);throw error;}})();encodedStore.records.set(key,record);
  }
  const record=encodedStore.records.get(key);record.requiredOwners??=new Set();if(eagerKeys.has(key))record.requiredOwners.add(encodedOwner);touchEncoded(key);const bytes=await record.promise;stats.retainedEncodedBytes=encodedStore.bytes;return bytes;
 };
 const prepare=async()=>{
  if(disposed)throw Error('Art pipeline disposed');
  if(!manifest){let text=encodedStore.manifests.get(baseUrl.href);if(!text){text=await bounded('Manifest',async signal=>{const response=await fetchImpl(baseUrl.href,{credentials:'same-origin',cache:'no-cache',signal});if(!response.ok)throw Error(`Manifest HTTP ${response.status}`);return response.text();});if(text.length>2*1024*1024)throw Error('Manifest exceeds byte budget');validateManifest(JSON.parse(text));encodedStore.manifests.set(baseUrl.href,text);}if(disposed)throw Error('Art pipeline disposed');manifest=validateManifest(JSON.parse(text));manifest={...manifest,assets:manifest.assets.filter(a=>!['unit','portrait'].includes(a.kind))};stats.declared=manifest.assets.length;stats.manifest='ready';}
 };
 const fetchImage=async (a,{paging=false}={})=>{
  if(disposed)throw Error('Art pipeline disposed');
  const url=runtimeUrl(a),key=`${url}|${a.runtime.sha256.toLowerCase()}`;
  if(!cache.has(key)){
   const record={bytes:a.runtime.width*a.runtime.height*4,reserved:false,image:null,promise:null,lastUsed:++access,pinned:false};
   record.promise=bounded(a.id,async signal=>{
    try{
     const bytes=await encoded(a,signal);
     const encodedRecord=encodedStore.records.get(key);if(encodedRecord)encodedRecord.users++;
     try{
     if(disposed||signal.aborted)throw Error('Art pipeline disposed or loading expired');
     if(paging)evictFor(record.bytes);
     const used=stats.retainedDecodedBytes+stats.reservedDecodedBytes;
     if(record.bytes>maxDecodedBytes-used)throw Error(`Decoded RGBA budget exceeded: ${a.id} needs ${record.bytes} bytes; ${used} retained/reserved of ${maxDecodedBytes}`);
     stats.reservedDecodedBytes+=record.bytes;record.reserved=true;notify();
     const image=await decodeImage(bytes,url);
     if(disposed||signal.aborted||image.width!==a.runtime.width||image.height!==a.runtime.height){image.close?.();throw Error(disposed||signal.aborted?'Art pipeline disposed or loading expired':'Decoded runtime dimensions mismatch');}
     stats.reservedDecodedBytes-=record.bytes;record.reserved=false;record.image=image;stats.retainedDecodedBytes+=record.bytes;stats.uniqueDecodedImages++;notify();return image;
     }finally{if(encodedRecord)encodedRecord.users--;}
    }catch(error){release(record);if(cache.get(key)===record)cache.delete(key);notify();throw error;}
   },{paging});
   cache.set(key,record);
  }
  const image=await cache.get(key).promise;if(disposed)throw Error('Art pipeline disposed');if(image.width!==a.runtime.width||image.height!==a.runtime.height)throw Error('Cached runtime dimensions mismatch');return image;
 };
 const approvedAsset=a=>a.review.status==='APPROVED'&&!a.candidate&&manifest.status==='APPROVED';
 const queuePage=a=>{if(disposed||!available.has(a.id)||pending.has(a.id)||stats.pageErrors.some(e=>e.id===a.id))return;
  const task=queue.then(async()=>{if(disposed)return;validateAsset(a);const approved=approvedAsset(a);if(!approved&&!(allowCandidates&&a.candidate&&a.review.status==='CANDIDATE'))throw Error('Raster lacks permitted review status');const image=await fetchImage(a,{paging:true});if(disposed)return;loaded.set(a.id,{asset:a,image,approved});stats.ready++;stats[approved?'approved':'candidates']++;});
  pending.set(a.id,task);stats.pending=pending.size;notify();queue=task.catch(error=>{if(!disposed)stats.pageErrors.push({id:a.id,message:error.message});}).finally(()=>{pending.delete(a.id);stats.pending=pending.size;notify();});
 };
 const pipeline={stats,get availableIds(){return [...available.keys()];},whenIdle(){return queue;},retry(id){stats.pageErrors=stats.pageErrors.filter(e=>e.id!==id);const a=available.get(id);if(a&&!loaded.has(id))queuePage(a);return queue;},get manifest(){return manifest;},
  attachEncodedStore(store){if(preloadPromise||manifest)throw Error('Cache must attach before loading');encodedStore=store;stats.encodedBudgetBytes=store.maxBytes;return pipeline;},
  selectAssets(ids){if(preloadPromise)throw Error('Selection must precede decoding');selectedIds=new Set(ids);return pipeline;},
  async cacheEncoded(){deadlineAt=Date.now()+preloadTimeoutMs;stats.manifest='loading';notify();await prepare();configure(manifest.assets);for(const a of available.values()){validateAsset(a);if(!warmEncoded(a)&&!eagerIds.has(a.id))continue;const approved=a.review.status==='APPROVED'&&!a.candidate&&manifest.status==='APPROVED';if(!approved&&!(allowCandidates&&a.candidate&&a.review.status==='CANDIDATE')){stats.skipped++;continue;}await bounded(a.id,signal=>encoded(a,signal));stats.encodedReady++;notify();}return pipeline;},
  preload(){if(preloadPromise)return preloadPromise;preloadPromise=(async()=>{deadlineAt=Date.now()+preloadTimeoutMs;stats.manifest='loading';notify();try{await prepare();const active=selectedIds?manifest.assets.filter(a=>selectedIds.has(a.id)):manifest.assets;configure(active);stats.selectedDeclared=available.size;notify();
    const all=[...available.values()];for(let index=0;index<all.length;index+=4)await Promise.all(all.slice(index,index+4).map(async raw=>{try{const a=validateAsset(raw);if(a.family){const layout=strictFamilyLayout(a);if(familyLayouts.has(a.family)&&familyLayouts.get(a.family)!==layout)throw Error('Family changes fixed canvas/pivot/logical scale');familyLayouts.set(a.family,layout);const key=familyLayoutIdentity(a),logical=logicalFamilyLayout(a);if(logicalLayouts.has(key)&&logicalLayouts.get(key)!==logical)throw Error('Family alias changes fixed canvas/pivot/logical scale');logicalLayouts.set(key,logical);}if(a.contactShadow.mode==='separate'&&!manifest.assets.some(x=>x.id===a.contactShadow.assetId))throw Error('Missing separate shadow asset');const approved=a.review.status==='APPROVED'&&!a.candidate&&manifest.status==='APPROVED';if(!approved&&!(allowCandidates&&a.candidate&&a.review.status==='CANDIDATE')){stats.skipped++;available.delete(a.id);return;}if(!eagerIds.has(a.id))return;const image=await fetchImage(a);if(disposed)return;loaded.set(a.id,{asset:a,image,approved});stats.ready++;stats[approved?'approved':'candidates']++;}catch(error){stats.failed++;stats.failures.push({id:raw?.id||'unknown',message:error.message});}finally{notify();}}));
    stats.status=stats.failed||stats.skipped||!stats.ready?'PLACEHOLDER_ONLY':stats.approved===stats.ready&&manifest.status==='APPROVED'?'APPROVED':'CANDIDATE';
   }catch(error){stats.manifest='error';stats.failures.push({id:'manifest',message:error.message});stats.failed++;stats.status='PLACEHOLDER_ONLY';}notify();return pipeline;})();return preloadPromise;},
  get(id,{state,direction,timeMs=0,frame:frameIndex}={}){let entry=loaded.get(id);if(!entry||state!==undefined&&entry.asset.state!==state||direction!==undefined&&entry.asset.direction!==direction)entry=[...loaded.values()].find(e=>e.asset.family===id&&(state===undefined||e.asset.state===state)&&(direction===undefined||e.asset.direction===direction));
   if(!entry){let requestedId=id;const a=available.get(id)||[...available.values()].find(a=>a.family===id&&(state===undefined||a.state===state)&&(direction===undefined||a.direction===direction));
    if(a&&!eagerIds.has(a.id)&&(state===undefined||a.state===state)&&(direction===undefined||a.direction===direction)){requestedId=a.id;queuePage(a);}
    const key=`${id}:${state??''}:${direction??''}`;const isNew=!fallbacks.has(key);fallbacks.add(key);stats.status='PLACEHOLDER_ONLY';if(isNew)notify();return {status:'PLACEHOLDER_ONLY',image:null,reason:pending.has(requestedId)?'Exact raster page pending':stats.pageErrors.find(e=>e.id===requestedId)?.message||'No loaded raster for exact asset/state/direction',pending:pending.has(requestedId),id};}
   const {asset:a,image,approved}=entry;touchEncoded(pageKey(a));const page=cache.get(pageKey(a));if(page){page.lastUsed=++access;if(!page.pinned){page.pinned=true;const timer=setTimeout(()=>{page.pinned=false;pinTimers.delete(timer);},0);pinTimers.add(timer);}}const timing=sampleSpriteAnimation(a.frames,{timeMs,loop:a.loop??a.state!=='death',frame:frameIndex}),index=timing.frame;
   const f=a.frames[index],scaleX=a.cell.width/a.source.width,scaleY=a.cell.height/a.source.height;
   return {status:approved?'APPROVED':'CANDIDATE',candidate:!approved,approved,id:a.id,family:a.family,image,sx:f.x,sy:f.y,sw:f.width,sh:f.height,frame:index,frameElapsedMs:timing.elapsedMs,animationDurationMs:timing.durationMs,events:timing.events,pivot:{x:a.pivot.x*scaleX,y:a.pivot.y*scaleY},render:{...a.render},contactShadow:{...a.contactShadow},asset:a};},
  dispose(){disposed=true;releaseEncodedOwnership();for(const timer of pinTimers)clearTimeout(timer);pinTimers.clear();for(const controller of controllers)controller.abort();pending.clear();stats.pending=0;available.clear();for(const record of cache.values())release(record);loaded.clear();cache.clear();stats.ready=0;stats.approved=0;stats.candidates=0;notify();}
 };
 return pipeline;
}
export {validateAsset,validateManifest};
