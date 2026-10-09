import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState} from '../shared/sim.js';
import {UNITS,BUILDINGS,TERRAIN} from '../shared/data.js';
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function arena(primaryType='infantry'){
 const s=createMatch({seed:159}),a=s.entities.find(e=>e.owner===0&&e.type==='infantry'),template=s.entities.find(e=>e.owner===1&&e.type==='infantry');
 for(const e of s.entities){e.hp=0;e.deadTick=0;}a.hp=a.maxHp;a.type='artillery';a.x=10.5;a.y=10.5;a.food=40;a.morale=80;
 s.players[0].modifiers.damage=1;s.players[1].modifiers.armor=0;s.players[1].modifiers.fortification=2;s.players[0].tags=[];
 for(let y=9;y<=13;y++)for(let x=9;x<=15;x++)s.map.tiles[y*s.map.width+x]='plain';
 const add=(type,x=12.5,y=10.5)=>{const building=Boolean(BUILDINGS[type]);const e={...template,id:s.nextId++,owner:1,type,kind:building?'building':'unit',x,y,hp:2000,maxHp:2000,food:40,foodMax:40,morale:80,order:{type:'hold'},path:[],queue:[],cargo:{food:0},cooldown:100,attackReadyTick:10000};delete e.character;delete e.embarked;s.entities.push(e);return e;};
 const primary=add(primaryType,12,10.5),secondary=add('firearm',12.5,11.5);view(s,0);
 assert.equal(command(s,0,{type:'attack',ids:[a.id],target:primary.id}).ok,true);step(s);const impact=a.attackImpactTick;
 const finish=()=>{while(s.tick<impact-1)step(s);const hps=new Map(s.entities.map(e=>[e.id,e.hp]));step(s);return e=>hps.get(e.id)-e.hp;};
 return {s,a,primary,secondary,add,finish,impact};
}
const raw=({s,a},victim)=>UNITS.artillery.damage*s.players[0].modifiers.damage*(UNITS.artillery.bonus?.[victim.type]||UNITS.artillery.bonus?.[victim.kind]||1)*(0.7+a.morale/250);
test('secondary damage is independent of primary armor and primary remains unchanged',()=>{
 const losses=[];for(const type of ['firearm','general']){const f=arena(type),loss=f.finish();losses.push(loss(f.secondary));close(loss(f.primary),Math.max(1,raw(f,f.primary)-UNITS[type].armor));}
 close(losses[0],losses[1]);
});
test('each secondary uses own armor, hill/ford terrain, fortification and river defense',()=>{
 const f=arena(),{s,add}=f,armored=add('general',13.3,10.5),hill=add('firearm',12.5,9.5),ford=add('firearm',11.5,10.5),fort=add('fort',11.5,11.5);
 s.map.tiles[9*s.map.width+12]='hill';s.map.tiles[10*s.map.width+11]='ford';
 s.effects.push({owner:1,kind:'riverDefense',x:ford.x,y:ford.y,radius:0.1,until:100});
 const loss=f.finish();close(loss(f.secondary),Math.max(1,raw(f,f.secondary)*0.35));close(loss(armored),Math.max(1,(raw(f,armored)-4)*0.35));
 close(loss(hill),Math.max(1,(raw(f,hill)-TERRAIN.hill.armor)*0.35));close(loss(ford),Math.max(1,(raw(f,ford)-TERRAIN.ford.armor-6)*0.35));
 close(loss(fort),Math.max(1,(raw(f,fort)-BUILDINGS.fort.armor*2)*0.35));
});
test('mixed unit/building bonuses and supply-denial bonus apply per victim',()=>{
 const f=arena('wall'),{s,add}=f,wagon=add('wagon',13,10.5),granary=add('granary',12.5,9.5);s.players[0].tags=['SUPPLY_DENIAL'];
 const loss=f.finish();close(loss(f.secondary),Math.max(1,raw(f,f.secondary)*0.35));close(loss(wagon),Math.max(1,raw(f,wagon)*1.2*0.35));close(loss(granary),Math.max(1,(raw(f,granary)*1.2-5)*0.35));close(loss(f.primary),Math.max(1,raw(f,f.primary)-10));
});
test('authoritative impact deals nothing early, skips friendly/dead/embarked and floors mitigated splash at one',()=>{
 const f=arena(),{s,add}=f,friendly=add('firearm',13,10.5),dead=add('firearm',12.5,9.5),aboard=add('firearm',11.5,10.5);friendly.owner=0;dead.hp=0;dead.deadTick=s.tick;aboard.embarked=999;
 s.players[1].modifiers.armor=1000;const hp=f.secondary.hp;while(s.tick<f.impact-1)step(s);assert.equal(f.secondary.hp,hp);assert.equal(f.primary.hp,2000);
 step(s);assert.equal(hp-f.secondary.hp,1);assert.equal(f.primary.hp,1999);assert.equal(friendly.hp,2000);assert.equal(dead.hp,0);assert.equal(aboard.hp,2000);assert.equal(f.a.lastAttack,f.impact);assert.equal(f.a.pendingAttack,undefined);
});
test('identical seed/commands produce deterministic complete combat state',()=>{const a=arena(),b=arena();a.finish();b.finish();assert.equal(hashState(a.s),hashState(b.s));});
test('attacker supply, morale, forest, shock and tempo factors are shared across victims',()=>{
 const f=arena(),{s,a}=f;a.food=0;s.map.tiles[Math.floor(a.y)*s.map.width+Math.floor(a.x)]='forest';a.lastMovedTick=s.tick;
 for(const kind of ['shock','tempo'])s.effects.push({owner:0,kind,x:a.x,y:a.y,radius:2,until:100});
 const loss=f.finish(),base=60*0.55*(0.7+a.morale/250)*1.25*1.45*1.3;
 close(loss(f.primary),Math.max(1,base-3));close(loss(f.secondary),Math.max(1,base*0.35));
});
