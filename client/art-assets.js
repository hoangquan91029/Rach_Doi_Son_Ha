import {withLoadingDeadline} from './loading-deadline.js';
import {TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION} from './world-presentation.js';
/** Raster packaging/loading only. Neither successful decode nor hashes grant visual approval. */
const SHA256=/^[a-f0-9]{64}$/i;
const KINDS=new Set(['unit','building','prop','vfx','terrain','ui','portrait']);
const finitePositive=n=>Number.isFinite(n)&&n>0;
const dimensions=(v,label)=>{if(!v||!Number.isSafeInteger(v.width)||!Number.isSafeInteger(v.height)||v.width<1||v.height<1||v.width>16384||v.height>16384||v.width*v.height>32*1024*1024)throw Error(`${label}: invalid dimensions`);};
const samePivot=(a,b)=>a.x===b.x&&a.y===b.y&&a.space===b.space;
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
 const occupied=[];for(const frame of asset.frames){if(![frame.x,frame.y,frame.width,frame.height].every(Number.isSafeInteger)||frame.x<0||frame.y<0||frame.width!==asset.cell.width||frame.height!==asset.cell.height||frame.x+frame.width>asset.runtime.width||frame.y+frame.height>asset.runtime.height||(!finitePositive(frame.durationMs)||frame.durationMs>60000))throw Error('Invalid runtime frame cell');if(occupied.some(r=>frame.x<r.x+r.width&&frame.x+frame.width>r.x&&frame.y<r.y+r.height&&frame.y+frame.height>r.y))throw Error('Overlapping frame cells');occupied.push(frame);if(frame.pivot&&!samePivot(frame.pivot,asset.pivot))throw Error('Per-frame pivot fitting forbidden');if(asset.frames.length>1){dimensions(frame.source,'frame source');if(typeof frame.source.path!=='string'||!frame.source.path||frame.source.width!==asset.source.width||frame.source.height!==asset.source.height||!SHA256.test(frame.source.sha256)||!SHA256.test(frame.source.rgbaSha256))throw Error('Frame source must retain locked canvas/custody');}}
 if(asset.loop!==undefined&&typeof asset.loop!=='boolean')throw Error('Invalid animation loop declaration');
 const derivation=asset.runtime.derivation;if(derivation?.method==='copy'&&(asset.frames.length!==1||asset.cell.width!==asset.source.width||asset.cell.height!==asset.source.height))throw Error('Copy must preserve original canvas');if(derivation?.method==='resize'&&asset.frames.length!==1)throw Error('Multi-frame derivative must declare atlas');if(derivation?.method!=='copy'&&derivation?.filter!=='lanczos')throw Error('Derived raster requires declared lanczos filter');if(!derivation||!['copy','resize','atlas'].includes(derivation.method)||derivation.sourceSha256!==asset.source.sha256)throw Error('Missing runtime derivation provenance');
 return asset;
}
function validateManifest(manifest) {
 if(!manifest||manifest.schemaVersion!==1||!['CANDIDATE','APPROVED'].includes(manifest.status)||!Array.isArray(manifest.assets)||manifest.assets.length>4096)throw Error('Unsupported raster manifest');
 const c=manifest.camera;if(c?.projection!=='dimetric'||JSON.stringify(c.ratio)!=='[2,1]'||JSON.stringify(c.tile)!==JSON.stringify([TILE_WIDTH,TILE_HEIGHT])||(!Number.isFinite(c.elevation)||Math.abs(c.elevation-CAMERA_ELEVATION)>0.001))throw Error('Camera contract mismatch');
 const ids=new Set();for(const a of manifest.assets){if(ids.has(a.id))throw Error(`Duplicate asset ID: ${a.id}`);ids.add(a.id);}
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
export function createArtAssetPipeline({manifestUrl='/assets/art-v1/manifest.json',allowCandidates=false,fetchImpl=globalThis.fetch,onStatus=()=>{},maxImageBytes=32*1024*1024,resourceTimeoutMs=30000,preloadTimeoutMs=60000}={}) {
 const loaded=new Map(),cache=new Map(),fallbacks=new Set(),familyLayouts=new Map();let manifest=null,disposed=false,preloadPromise=null,deadlineAt=Infinity;
 const stats={status:'PLACEHOLDER_ONLY',manifest:'not-loaded',declared:0,ready:0,approved:0,candidates:0,failed:0,skipped:0,fallbacks:0,failures:[]};
 const notify=()=>{stats.fallbacks=fallbacks.size;try{onStatus({...stats,failures:[...stats.failures]});}catch{}};
 const baseUrl=new URL(manifestUrl,globalThis.location?.href||'http://localhost/');
 const runtimeUrl=a=>{if(a.runtime.path.startsWith('/')||a.runtime.path.includes('\\')||a.runtime.path.split('/').includes('..')||/^[a-z]+:/i.test(a.runtime.path))throw Error('Runtime path must be manifest-relative');const url=new URL(a.runtime.path,baseUrl);const directory=new URL('.',baseUrl).pathname;if(url.origin!==baseUrl.origin||!url.pathname.startsWith(directory)||url.search||url.hash)throw Error('Runtime raster must remain within manifest directory');return url.href;};
 const bounded=(label,action)=>withLoadingDeadline(action,{label,timeoutMs:Math.min(resourceTimeoutMs,Math.max(1,deadlineAt-Date.now()))});
 const fetchImage=async a=>{const url=runtimeUrl(a),key=`${url}|${a.runtime.sha256}`;if(!cache.has(key))cache.set(key,bounded(a.id,async signal=>{const response=await fetchImpl(url,{credentials:'same-origin',signal});if(!response.ok)throw Error(`Raster HTTP ${response.status}`);const bytes=await response.arrayBuffer();if(bytes.byteLength>maxImageBytes)throw Error('Raster exceeds byte budget');if(await digest(bytes)!==a.runtime.sha256.toLowerCase())throw Error('Runtime encoded SHA256 mismatch');const image=await decodeImage(bytes,url);if(image.width!==a.runtime.width||image.height!==a.runtime.height){image.close?.();throw Error('Decoded runtime dimensions mismatch');}return image;}));const image=await cache.get(key);if(image.width!==a.runtime.width||image.height!==a.runtime.height)throw Error('Cached runtime dimensions mismatch');return image;};
 const pipeline={stats,get manifest(){return manifest;},
  preload(){if(preloadPromise)return preloadPromise;preloadPromise=(async()=>{deadlineAt=Date.now()+preloadTimeoutMs;stats.manifest='loading';notify();try{const text=await bounded('Manifest',async signal=>{const response=await fetchImpl(baseUrl.href,{credentials:'same-origin',cache:'no-cache',signal});if(!response.ok)throw Error(`Manifest HTTP ${response.status}`);return response.text();});if(text.length>2*1024*1024)throw Error('Manifest exceeds byte budget');manifest=validateManifest(JSON.parse(text));stats.declared=manifest.assets.length;stats.manifest='ready';notify();
    for(let index=0;index<manifest.assets.length;index+=4)await Promise.all(manifest.assets.slice(index,index+4).map(async raw=>{try{const a=validateAsset(raw);if(a.family){const layout=JSON.stringify([a.source.width,a.source.height,a.cell.width,a.cell.height,a.pivot,a.render]);if(familyLayouts.has(a.family)&&familyLayouts.get(a.family)!==layout)throw Error('Family changes fixed canvas/pivot/logical scale');familyLayouts.set(a.family,layout);}if(a.contactShadow.mode==='separate'&&!manifest.assets.some(x=>x.id===a.contactShadow.assetId))throw Error('Missing separate shadow asset');const approved=a.review.status==='APPROVED'&&!a.candidate&&manifest.status==='APPROVED';if(!approved&&!(allowCandidates&&a.candidate&&a.review.status==='CANDIDATE')){stats.skipped++;return;}const image=await fetchImage(a);if(disposed)return;loaded.set(a.id,{asset:a,image,approved});stats.ready++;stats[approved?'approved':'candidates']++;}catch(error){stats.failed++;stats.failures.push({id:raw?.id||'unknown',message:error.message});}finally{notify();}}));
    stats.status=stats.failed||stats.skipped||!stats.ready?'PLACEHOLDER_ONLY':stats.approved===stats.ready&&manifest.status==='APPROVED'?'APPROVED':'CANDIDATE';
   }catch(error){stats.manifest='error';stats.failures.push({id:'manifest',message:error.message});stats.failed++;stats.status='PLACEHOLDER_ONLY';}notify();return pipeline;})();return preloadPromise;},
  get(id,{state,direction,timeMs=0,frame:frameIndex}={}){let entry=loaded.get(id);if(!entry||state!==undefined&&entry.asset.state!==state||direction!==undefined&&entry.asset.direction!==direction)entry=[...loaded.values()].find(e=>e.asset.family===id&&(state===undefined||e.asset.state===state)&&(direction===undefined||e.asset.direction===direction));
   if(!entry){const key=`${id}:${state??''}:${direction??''}`;const isNew=!fallbacks.has(key);fallbacks.add(key);stats.status='PLACEHOLDER_ONLY';if(isNew)notify();return {status:'PLACEHOLDER_ONLY',image:null,reason:'No loaded raster for exact asset/state/direction',id};}
   const {asset:a,image,approved}=entry;let index=0;if(Number.isInteger(frameIndex))index=((frameIndex%a.frames.length)+a.frames.length)%a.frames.length;else{const duration=a.frames.reduce((sum,f)=>sum+f.durationMs,0);const supplied=Number.isFinite(timeMs)?timeMs:0;const loop=a.loop??a.state!=='death';let time=loop?((supplied%duration+duration)%duration):Math.max(0,Math.min(supplied,duration-Number.EPSILON));while(index<a.frames.length-1&&time>=a.frames[index].durationMs){time-=a.frames[index].durationMs;index++;}}
   const f=a.frames[index],scaleX=a.cell.width/a.source.width,scaleY=a.cell.height/a.source.height;
   return {status:approved?'APPROVED':'CANDIDATE',candidate:!approved,approved,id:a.id,family:a.family,image,sx:f.x,sy:f.y,sw:f.width,sh:f.height,frame:index,pivot:{x:a.pivot.x*scaleX,y:a.pivot.y*scaleY},render:{...a.render},contactShadow:{...a.contactShadow},asset:a};},
  dispose(){disposed=true;Promise.allSettled([...cache.values()]).then(results=>results.forEach(r=>{if(r.status==='fulfilled')r.value.close?.();}));loaded.clear();cache.clear();}
 };
 return pipeline;
}
export {validateAsset,validateManifest};
