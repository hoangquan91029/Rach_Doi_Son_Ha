import {selectBank,matchArtScope} from '../shared/art-bank.js';
/** Encoded route bank survives menu; decoded raster ownership belongs to one match epoch. */
export function createArtBank({maxEncodedBytes=64*1024*1024}={}){
 if(!Number.isSafeInteger(maxEncodedBytes)||maxEncodedBytes<1)throw Error('Invalid encoded bank budget');
 const store={records:new Map(),manifests:new Map(),bytes:0,maxBytes:maxEncodedBytes};let epoch=0,source=null;
 const status={phase:'empty',epoch:0,encodedBytes:0,encodedBudgetBytes:maxEncodedBytes,activeIds:[],availableIds:[],scope:null};
 return {status,attach(pipeline){pipeline.attachEncodedStore(store);return pipeline;},
  async prime(pipeline){try{await pipeline.cacheEncoded();status.phase='menu';}finally{source=pipeline.manifest||source;status.encodedBytes=store.bytes;}},
  selection(state){if(!source)throw Error('Encoded artwork bank is not ready');const definitions=Object.fromEntries(source.assets.map(asset=>[asset.id,{asset}]));const scope=matchArtScope(state);const catalog={definitions,recipes:{match:{assetIds:source.assets.map(a=>a.id)}},portraitDependencies:Object.fromEntries(scope.leaders.map(id=>[id,{id}])),scopePolicy:'Conservative shared world on both legal maps'};return selectBank(catalog,{route:'match',scope});},
  async activate(pipeline,state){const token=++epoch;status.epoch=token;status.phase='loading';if(!source){await this.prime(pipeline);if(token!==epoch)return false;status.phase='loading';}const bank=this.selection(state);status.scope=bank.scope;status.activeIds=bank.assetIds;pipeline.selectAssets(bank.assetIds);await pipeline.preload();if(token!==epoch)return false;if(pipeline.stats.failed||pipeline.stats.skipped||pipeline.stats.ready!==pipeline.stats.eagerDeclared){status.phase='error';throw Error(pipeline.stats.failures[0]?.message||'Selected artwork bank could not decode');}status.availableIds=pipeline.availableIds;status.encodedBytes=store.bytes;status.phase='match';return true;},
  release(){epoch++;status.epoch=epoch;status.phase='menu';status.activeIds=[];status.availableIds=[];status.scope=null;status.encodedBytes=store.bytes;}
 };
}
