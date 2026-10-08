import {withLoadingDeadline} from './loading-deadline.js';
/** Hold decoded portraits through later setup/panels; preserve their existing public URLs. */
export function createBootUiAssets({characters,makeImage=()=>new Image(),fonts=globalThis.document?.fonts,timeoutMs=12000}={}){
 const portraits=new Map();const status={declared:Object.keys(characters).length,ready:0,failures:[],fontWarnings:[]};
 return {portraits,status,async preload(){
  status.failures=[];status.fontWarnings=[];
  const fontLoads=fonts?['400 16px "DM Sans"','500 16px "DM Sans"','600 16px "DM Sans"','700 16px "DM Sans"','500 16px "Playfair Display"','600 16px "Playfair Display"','700 16px "Playfair Display"'].map(font=>withLoadingDeadline(()=>fonts.load(font,'Rạch Đôi Sơn Hà Commander 0123456789'),{timeoutMs,label:font}).catch(error=>status.fontWarnings.push(error.message))):[];
  await Promise.all([...Object.keys(characters).map(async id=>{
   if(portraits.has(id))return;
   try{const image=await withLoadingDeadline(async signal=>{const image=makeImage();image.decoding='async';const abort=()=>{image.src='';};signal.addEventListener('abort',abort,{once:true});try{image.src=`/assets/leadership/${id}/portrait.webp`;await image.decode();if(signal.aborted)throw Error('Portrait loading aborted');return image;}finally{signal.removeEventListener('abort',abort);}},{timeoutMs,label:`Portrait ${id}`});portraits.set(id,image);status.ready=portraits.size;}catch(error){status.failures.push({id,message:error.message});}
  }),...fontLoads]);
  if(status.failures.length)throw Error(`${status.failures.length} leadership portraits unavailable: ${status.failures[0].message}`);
  return this;
 }};
}
