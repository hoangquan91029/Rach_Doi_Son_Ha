import {UNIT_ART_FAMILIES, LEADER_ART_FAMILIES} from './unit-art.js';
export const DIRECTIONS = Object.freeze([0,1,2,3,4,5,6,7]);
export const ACTION_FRAMES = Object.freeze({idle:4,walk:8,attack:8,hit:4,death:8,gather_wood:8,gather_food:8,gather_iron:8,build:8,ability:6,load:8,unload:8});
// Legacy death frame counts remain available for archived descriptor parsing only.
export const ACTIONS = Object.freeze(Object.keys(ACTION_FRAMES).filter(action=>action!=='death'));
const combat=['idle','walk','attack','hit'];
export function identityActions(identity){
 if(Object.hasOwn(LEADER_ART_FAMILIES,identity))return [...combat,'ability','build'];
 if(identity==='villager')return [...combat,'gather_wood','gather_food','gather_iron','build'];
 if(['wagon','transport'].includes(identity))return ['idle','walk','load','unload','hit'];
 return Object.hasOwn(UNIT_ART_FAMILIES,identity)?[...combat]:[];
}
export function actionSpec(identity,action){
 const aliases={repair:'build',return_wood:'walk',return_food:'walk',return_iron:'walk',destroyed:'death',sink:'death'};
 const permitted=action==='repair'?identity==='villager'||Object.hasOwn(LEADER_ART_FAMILIES,identity):action.startsWith('return_')?identity==='villager':action==='destroyed'?['artillery','wagon'].includes(identity):action==='sink'?['warship','transport'].includes(identity):true;
 const canonical=aliases[action]||action;
 const applicable=permitted&&identityActions(identity).includes(canonical);
 return {action:canonical,alias:canonical!==action,applicable,frames:applicable?ACTION_FRAMES[canonical]:null,roles:applicable?(Object.hasOwn(LEADER_ART_FAMILIES,identity)?canonical==='build'?['king']:['king','general']:[identity]):[],requiresSeparatePoses:applicable&&['ability','load','unload'].includes(canonical)};
}
