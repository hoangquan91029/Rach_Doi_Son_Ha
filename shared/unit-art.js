import {UNITS,CHARACTERS} from './data.js';
const families=identity=>Object.freeze([identity,`unit.${identity}`]);
/** Identity registry only: an entry does not assert that any raster is authored. */
export const UNIT_ART_FAMILIES=Object.freeze(Object.fromEntries(Object.keys(UNITS).filter(id=>!['king','general'].includes(id)).map(id=>[id,families(id)])));
export const LEADER_ART_FAMILIES=Object.freeze(Object.fromEntries(Object.keys(CHARACTERS).map(id=>[id,families(id)])));
/** King/general character identity is authoritative; never substitute another leader or role art. */
export function unitArtFamilies(entity){
 if(!entity||!Object.hasOwn(UNITS,entity.type))return null;
 if(entity.type==='king'||entity.type==='general')return Object.hasOwn(LEADER_ART_FAMILIES,entity.character)?LEADER_ART_FAMILIES[entity.character]:null;
 return UNIT_ART_FAMILIES[entity.type];
}
