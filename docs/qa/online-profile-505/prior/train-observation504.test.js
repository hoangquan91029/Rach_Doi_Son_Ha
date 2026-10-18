import test from 'node:test';import assert from 'node:assert/strict';import {observeTrain} from '../scripts/qa/train-observation504.mjs';
const q=(unit,remaining,total=10)=>({unit,remaining,total}),s=queue=>({queue,units:[]});
test('specific appended queue accepted',()=>assert.equal(observeTrain(s([]),s([q('villager',9.8)]),'villager').status,'ACCEPTED_QUEUE'));
test('completion plus append at unchanged length accepted',()=>assert.equal(observeTrain(s([q('villager',.1)]),s([q('villager',9.9)]),'villager').status,'ACCEPTED_QUEUE'));
test('old queue merely advances not acceptance',()=>assert.equal(observeTrain(s([q('villager',8)]),s([q('villager',7)]),'villager').status,'PENDING'));
test('different unit append not acceptance',()=>assert.equal(observeTrain(s([]),s([q('infantry',9)]),'villager').status,'PENDING'));
test('unrelated spawn cannot establish acceptance',()=>assert.equal(observeTrain(s([]),{queue:[],units:[{id:12,type:'villager'}]},'villager').status,'PENDING'));
test('explicit rejection retained',()=>assert.equal(observeTrain(s([]),s([]),'villager',['Not enough resources']).status,'REJECTED'));
