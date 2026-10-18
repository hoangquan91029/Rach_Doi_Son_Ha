import {withLoadingDeadline} from './loading-deadline.js';
/** Legacy portraits archived; pixel portrait bank is empty. Fonts remain available. */
export function createBootUiAssets({characters,makeImage=()=>new Image(),fonts=globalThis.document?.fonts,timeoutMs=12000}={}){
 const portraits=new Map();const status={declared:0,ready:0,failures:[],fontWarnings:[]};
 return {portraits,status,async preload(){
  status.failures=[];status.fontWarnings=[];
  const fontLoads=fonts?['400 16px "DM Sans"','500 16px "DM Sans"','600 16px "DM Sans"','700 16px "DM Sans"','500 16px "Playfair Display"','600 16px "Playfair Display"','700 16px "Playfair Display"'].map(font=>withLoadingDeadline(()=>fonts.load(font,'Rạch Đôi Sơn Hà Commander 0123456789'),{timeoutMs,label:font}).catch(error=>status.fontWarnings.push(error.message))):[];
  await Promise.all(fontLoads);
  return this;
 }};
}
