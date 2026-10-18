import {readFileSync} from 'node:fs';
import {createPixelSpriteBank} from '../../../../client/pixel-sprite-bank.js';
const text=readFileSync('tests/pixel-integration535.test.js','utf8');
const metadata=eval(text.slice(text.indexOf('const metadata=')+15,text.indexOf('\nconst stride=' )).replace(/;$/,''));
const c=metadata('hit');const b=createPixelSpriteBank({fetchImpl:async()=>({ok:true,json:async()=>({schema:'rds-pixel-registry/v1',clips:[c],strides:[]})}),decode:async()=>({width:1024,height:1024})});await b.preload();
const e={id:1,kind:'unit',type:'villager',hp:10,state:'idle',dir:1,x:0,y:0,hitUntil:15};
for(let tick=10;tick<=15;tick++){b.observeEntities([e],{tick,timeMs:tick*50});const s=b.sampleEntity(e);console.log(JSON.stringify({tick,frame:s.frame,complete:s.complete,missing:s.missing,reason:s.reason}));}
