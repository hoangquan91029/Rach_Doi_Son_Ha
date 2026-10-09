import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState} from '../shared/sim.js';
import {BALANCE,TICK_RATE,UNITS} from '../shared/data.js';
const advance=(s,seconds)=>{for(let i=0;i<seconds*TICK_RATE&&s.winner===null;i++)step(s);};
const entity=(s,type,owner=0)=>s.entities.find(e=>e.owner===owner&&e.type===type&&e.hp>0);
function aboard(type='infantry'){
 const s=createMatch({seed:156}),yard=entity(s,'barracks');yard.type='shipyard';yard.x=10.5;yard.y=38.5;
 assert.equal(command(s,0,{type:'train',building:yard.id,unit:'transport'}).ok,true);advance(s,20);
 const ship=entity(s,'transport'),u=entity(s,type);assert.ok(ship);u.x=ship.x;u.y=39.5;
 assert.equal(command(s,0,{type:'load',ids:[ship.id],target:u.id}).ok,true);advance(s,1);assert.equal(u.embarked,ship.id);
 return {s,ship,u};
}
test('ordinary embarked zero-food passenger shares land grace, morale and 30-second attrition',()=>{
 const {s,ship,u}=aboard();const land=entity(s,'spearman');land.x=20.5;land.y=25.5;land.order={type:'hold'};
 for(const e of [u,land]){e.food=0;e.starving=0;e.morale=80;}const hp=u.hp,landHp=land.hp;
 advance(s,24);assert.equal(u.hp,hp);assert.equal(land.hp,landHp);assert.ok(Math.abs(u.starving-24)<1e-8);assert.ok(Math.abs(u.morale-68)<1e-8);
 advance(s,6);assert.ok(Math.abs(u.starving-30)<1e-8);assert.ok(u.hp<hp);assert.ok(Math.abs((hp-u.hp)-(landHp-land.hp))<1e-8);assert.ok(u.morale<68);
 assert.equal(u.x,ship.x);assert.equal(u.y,ship.y);assert.equal(view(s,0).entities.find(e=>e.id===u.id).embarked,ship.id);
 assert.equal(command(s,0,{type:'move',ids:[u.id],x:15,y:20}).ok,false);
});
test('fed passenger consumes finite own rations without ship, wagon or store resupply',()=>{
 const {s,ship,u}=aboard();for(const e of s.entities)if(e!==u){e.food=(e.foodMax??0)+1;if(e.cargo)e.cargo.food=0;}
 const wagon=entity(s,'wagon'),granary=entity(s,'granary');for(const e of [wagon,granary]){e.x=ship.x;e.y=ship.y;e.cargo.food=50;}
 ship.cargo.food=50;u.food=10;u.starving=9;u.morale=60;const hp=u.hp,pool={...s.players[0].resources},rate=UNITS[u.type].consumption*s.players[0].modifiers.consumption;
 advance(s,5);assert.ok(Math.abs(u.food-(10-rate*5))<1e-8);assert.equal(u.starving,0);assert.equal(u.hp,hp);assert.ok(u.morale>60);
 for(const e of [ship,wagon,granary])assert.equal(e.cargo.food,50);assert.equal(s.players[0].resources.wood,pool.wood);assert.equal(s.players[0].resources.iron,pool.iron);assert.ok(s.players[0].resources.food<=pool.food);assert.equal(s.players[0].resources.food,50);
});
test('starving boarded General dies through authoritative defeat and freezes simulation',()=>{
 const {s,ship,u}=aboard('general');u.food=0;u.starving=0;u.hp=0.5;advance(s,30);
 assert.equal(u.hp,0);assert.equal(u.state,'death');assert.equal(s.winner,1);assert.equal(s.reason,'Enemy General defeated');assert.ok(ship.hp>0);assert.equal(s.players[0].stats.lost,1);
 const hash=hashState(s);step(s);assert.equal(hashState(s),hash);
});
test('unloading hungry passenger preserves accrued physiology and restores ordinary land handling',()=>{
 const {s,ship,u}=aboard();u.food=0;u.starving=0;advance(s,26);const starving=u.starving,hp=u.hp;
 assert.equal(command(s,0,{type:'unload',ids:[ship.id],target:entity(s,'king').id}).ok,true);advance(s,1);
 assert.equal(u.embarked,null);assert.ok(u.starving>starving);assert.ok(u.hp<hp);assert.ok(!ship.cargo.units.includes(u.id));
 assert.equal(command(s,0,{type:'move',ids:[u.id],x:15,y:20}).ok,true);
});
test('transport death still kills hungry embarked passenger through ordinary enemy attack',()=>{
 const {s,ship,u}=aboard();u.food=0;u.starving=0;advance(s,26);
 const yard=entity(s,'barracks',1);yard.type='shipyard';yard.x=50.5;yard.y=38.5;
 assert.equal(command(s,1,{type:'train',building:yard.id,unit:'warship'}).ok,true);advance(s,24);const enemy=entity(s,'warship',1);assert.ok(enemy);
 ship.hp=1;enemy.x=ship.x+1;enemy.y=ship.y;view(s,1);assert.equal(command(s,1,{type:'attack',ids:[enemy.id],target:ship.id}).ok,true);
 advance(s,(UNITS.warship.attackWindupTicks+1)/TICK_RATE);assert.equal(ship.hp,0);assert.equal(u.hp,0);assert.equal(u.state,'death');assert.equal(s.winner,null);
});
