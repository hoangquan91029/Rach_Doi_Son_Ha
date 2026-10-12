/** Balance values are gameplay interpretations of the supplied dossier, not historical measurements. */
export const TICK_RATE = 20;
export const BALANCE = Object.freeze({populationCap:120,queueCap:8,carry:20,gatherPerSecond:3,resupplyPerSecond:12,starveGrace:25,starveDamage:0.25,healPerSecond:2,healRadius:5,lowSupply:0.25,commandUnits:120});
const unit=(name,hp,damage,range,speed,wood,food,iron,extra={})=>({name,label:name,hp,damage,range,speed,cost:{wood,food,iron},armor:1,cooldown:1.2,attackWindupTicks:4,attackCueKind:'melee',vision:7,foodMax:40,consumption:0.16,trainTime:9,...extra});
export const UNITS = {
 villager:unit('Villager',65,4,1,2.1,0,45,0,{trainTime:7,vision:6}),
 king:unit('King',320,12,1.2,2,0,0,0,{foodMax:65,vision:8,trainable:false}),
 general:unit('General',360,19,1.3,2.3,0,0,0,{armor:4,foodMax:65,vision:9,trainable:false}),
 infantry:unit('Infantry',125,13,1.15,2.3,25,40,15,{armor:3}),
 spearman:unit('Spearmen',105,11,1.5,2.2,35,35,10,{bonus:{cavalry:2.7},armor:2,attackWindupTicks:6,attackCueKind:'spear'}),
 firearm:unit('Firearm infantry',80,23,5.5,1.9,35,45,30,{cooldown:2.2,armor:0,trainTime:12,attackWindupTicks:6,attackCueKind:'firearm'}),
 cavalry:unit('Cavalry',190,22,1.2,3.8,45,75,40,{consumption:0.3,foodMax:65,trainTime:16}),
 artillery:unit('Artillery',125,60,8,1.1,110,60,90,{cooldown:3.8,trainTime:22,bonus:{building:2},consumption:0.24,splash:1.4,attackWindupTicks:10,attackCueKind:'artillery'}),
 wagon:unit('Supply Wagon',140,0,0,1.9,65,35,0,{capacity:180,trainTime:12,armor:0,vision:5}),
 warship:unit('Warship',340,36,6,2.5,140,70,60,{naval:true,trainTime:23,foodMax:80,consumption:0.3,cooldown:2.5,armor:4,attackWindupTicks:8,attackCueKind:'naval'}),
 transport:unit('Transport',260,0,0,2.5,100,40,10,{naval:true,capacity:12,trainTime:16,foodMax:65,consumption:0.2})
};
const building=(name,hp,wood,food,iron,extra={})=>({name,label:name,hp,cost:{wood,food,iron},buildTime:15,vision:8,armor:5,radius:0.75,...extra});
export const BUILDINGS = {
 residence:building('Main Residence',1100,220,0,30,{trains:['villager'],radius:1.1,buildTime:24,healRadius:BALANCE.healRadius,heal:BALANCE.healPerSecond,capacity:1200}),
 barracks:building('Barracks',650,140,0,20,{trains:['infantry','spearman','firearm']}),
 cavalryCamp:building('Cavalry Camp',600,170,0,35,{trains:['cavalry']}),
 artilleryWorkshop:building('Artillery Workshop',550,190,0,70,{trains:['artillery']}),
 shipyard:building('Shipyard',650,170,0,30,{trains:['transport','warship'],coastal:true}),
 fort:building('Fort',1250,180,0,100,{damage:26,range:7,cooldown:1.8,buildTime:25,attackWindupTicks:6,attackCueKind:'fort'}),
 wall:building('Wall',400,30,0,5,{radius:0.45,buildTime:6}),
 gate:building('Gate',500,45,0,10,{radius:0.45,buildTime:8}),
 depot:building('Supply Depot',480,100,0,0,{trains:['wagon'],capacity:650}),
 granary:building('Granary',450,90,0,0,{capacity:800,resupplyRadius:4})
};
const character=(name,tags,description,passive,ability,weakness)=>({name,label:name,tags,description,passive,ability,weakness});
export const CHARACTERS = {
 han_xin:character('Han Xin',['MANEUVER','DECEPTION'],'Maneuver and information control.',{speed:1.08,vision:1.15},{name:'False Crossing',kind:'deception',duration:15,cooldown:65,description:'Nearby troops conceal themselves at long range and redeploy faster.'},'Remote troops consume more rations.'),
 xiang_yu:character('Xiang Yu',['SHOCK','MORALE'],'Decisive assault and battlefield morale.',{damage:1.08,morale:10,consumption:1.12},{name:'Break the Cauldrons',kind:'shock',duration:12,cooldown:65,description:'+45% damage nearby, consumes 8 rations; retreat orders locked during the assault.'},'High upkeep punishes prolonged war.'),
 napoleon_bonaparte:character('Napoleon Bonaparte',['MANEUVER','MOBILIZATION'],'Separate columns rapidly concentrate.',{train:0.92},{name:'March Separately, Fight Together',kind:'concentrate',duration:16,cooldown:65,description:'Nearby units move 40% faster; artillery fires faster.'},'Units far from food stores consume more rations.'),
 ly_thuong_kiet:character('Lý Thường Kiệt',['FORTIFICATION','PREEMPTION'],'Disrupt preparations; defend the river line.',{fortification:1.15},{name:'Như Nguyệt Line',kind:'riverDefense',duration:20,cooldown:65,description:'Nearby forces gain armor at river crossings and friendly defenses.'},'Defensive benefits require prepared geography.'),
 tran_hung_dao:character('Trần Hưng Đạo',['DEFENSE_IN_DEPTH','SUPPLY_DENIAL','LOGISTICS'],'Preserve the army, raid supplies, exploit prepared river terrain.',{consumption:0.9},{name:'Bạch Đằng Killing Ground',kind:'riverTrap',duration:24,cooldown:75,description:'Prepare a nearby river or ford; enemies entering it take damage. Must be near water.'},'Requires terrain and preparation.'),
 nguyen_hue:character('Nguyễn Huệ / Quang Trung',['SURPRISE','MANEUVER','SHOCK'],'Rapid multi-axis offensive tempo.',{speed:1.08},{name:'Tết Thunderbolt',kind:'tempo',duration:14,cooldown:60,description:'Nearby troops gain speed and first-strike damage while advancing.'},'Momentum bonuses expire during static warfare.'),
 le_thanh_tong:character('Lê Thánh Tông',['ADMINISTRATION','MOBILIZATION'],'Institutions convert the economy into trained armies.',{train:0.82},{name:'State Mobilization',kind:'mobilize',duration:20,cooldown:80,description:'Production progresses twice as fast for 20 seconds.'},'Benefits require developed recruitment infrastructure.'),
 minh_menh:character('Minh Mạng / Minh Mệnh',['ADMINISTRATION','ECONOMY'],'Central administration and inspection.',{gather:1.12},{name:'Imperial Inspection',kind:'inspection',duration:24,cooldown:75,description:'Nearby villagers gather 45% faster; nearby buildings repair gradually.'},'Inspection concentrates benefits near the King.'),
 nguyen_anh:character('Nguyễn Ánh / Gia Long',['LOGISTICS','NAVAL','RESILIENCE'],'Secure bases, naval supply and restoration.',{naval:1.15,rebuild:0.65},{name:'Return from Defeat',kind:'restore',duration:20,cooldown:80,description:'Nearby damaged allies heal; construction proceeds twice as fast.'},'Reconstruction needs a surviving King and resources.'),
 nguyen_phuc_chu:character('Nguyễn Phúc Chu',['NAVAL','LOGISTICS','EXPANSION'],'Maritime networks and frontier settlements.',{naval:1.12,logistics:1.25},{name:'Southern Frontier Network',kind:'network',duration:25,cooldown:75,description:'Wagons move faster and food resupply range increases.'},'Requires physical stores and connected transport.'),
 tran_nhan_tong:character('Trần Nhân Tông',['MORALE','RESILIENCE'],'National cohesion and recovery.',{morale:15,heal:1.2},{name:'Diên Hồng Consensus',kind:'consensus',duration:20,cooldown:70,description:'Nearby forces recover morale and receive gradual healing.'},'Little direct damage burst; strongest with a field commander.'),
 trinh_cuong:character('Trịnh Cương',['ECONOMY','ADMINISTRATION'],'Fiscal institutions and economical military upkeep.',{consumption:0.82},{name:'Fiscal Reorganization',kind:'fiscal',duration:25,cooldown:75,description:'Villagers deliver 35% more wood and iron during the edict.'},'Economic advantages require a functioning gathering network.')
};
export const SYNERGIES = [
 {tags:['MORALE','DEFENSE_IN_DEPTH'],name:'United Resistance',modifiers:{heal:1.25,armor:1,consumption:0.92}},
 {tags:['ADMINISTRATION','MOBILIZATION'],name:'Organized Levy',modifiers:{train:0.9}},
 {tags:['NAVAL','LOGISTICS'],name:'Maritime Supply',modifiers:{naval:1.1,logistics:1.15}},
 {tags:['MANEUVER','SURPRISE'],name:'Rapid Columns',modifiers:{speed:1.08}},
 {tags:['ECONOMY','LOGISTICS'],name:'Sustained Campaign',modifiers:{consumption:0.92}}
];
export const TERRAIN = {
 plain:{speed:1},forest:{speed:0.72,conceal:true},hill:{speed:0.8,vision:2,range:1,armor:1},mountain:{impassable:true},river:{water:true},sea:{water:true},ford:{speed:0.6,water:true,land:true,armor:-1}
};
export const MAPS = [
 {id:'delta',name:'River of Two Kingdoms',description:'Three ford routes across a navigable delta, wooded ambush banks and a southern sea.',width:64,height:48},
 {id:'coast',name:'Coast of the Mountain Pass',description:'Coastal landings, two mountain passes, forest corridors and a northern river.',width:64,height:48}
];
