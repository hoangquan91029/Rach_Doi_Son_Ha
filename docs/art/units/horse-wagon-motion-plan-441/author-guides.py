from pathlib import Path
import json,hashlib,subprocess,math
P=Path(__file__).parent; root=P.parents[3]
inputs=['AGENTS.md','docs/art/pipeline/GRAPHICS_PRODUCTION_PLAN.md','docs/art/units/supply-wagon-horse-415/raw.png','docs/art/units/supply-wagon-horse-415/working-256.png','docs/art/units/supply-wagon-horse-415/runtime-128.png','docs/art/units/supply-wagon-horse-415/descriptor.json']+[f'docs/qa/{s}/receipt.json' for s in ['horse-wagon-runtime-420','horse-wagon-public-424','unit-scale-runtime-426','unit-scale-clear-travel-430','unit-scale-public-434']]
pins={s:hashlib.sha256((root/s).read_bytes()).hexdigest() for s in inputs}
legs={'LH':(735,785,725,1005,0),'LF':(960,820,950,1100,2),'RH':(820,765,835,1000,4),'RF':(1060,800,1070,1085,6)}
ledger=[]
for f in range(8):
    poses={}; bob=[0,2,0,-2,0,2,0,-2][f]
    for name,(hx,hy,bx,by,offset) in legs.items():
        phase=(f-offset)%8
        # Two-frame swing, six-frame support. All ground travel shares ESE vector.
        if phase==0: d=-32; lift=19; state='toe-off / early swing'
        elif phase==1: d=16; lift=40; state='forward swing'
        else: d=32-(phase-2)*12.8; lift=0; state='touchdown' if phase==2 else 'ground support'
        poses[name]={'phase':phase,'state':state,'hoof':[round(bx+d,2),round(by+d*.45-lift,2)],'support':phase>=2}
    ledger.append({'frame':f,'timeMs':f*125,'durationMs':125,'bodyBobRawPx':bob,'legs':poses,'support':[n for n,p in poses.items() if p['support']],'wheelAngleDegrees':f*45})
    def path(d,fill,stroke='#493321',sw=10):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<ellipse cx="400" cy="784" rx="290" ry="40" fill="#000" opacity=".12"/>','<ellipse cx="920" cy="1100" rx="260" ry="40" fill="#000" opacity=".12"/>']
    # Each SVG is a complete original guide, no image elements or extracted source pixels.
    s+=[path('M80 430 L300 300 L690 480 L710 675 L465 795 L85 620 Z','#9e6c36'),path('M80 430 L460 610 L710 480 L300 300 Z','#bb8649'),path('M95 470 L470 650 L700 530 M95 545 L470 725 L700 605','none','#dab17a',22)]
    s+=[path('M145 405 L225 330 L355 385 L280 470 Z','#a8733d'),path('M280 440 Q330 300 420 365 Q530 280 580 450 Q650 380 665 510 L460 585 Z','#ccb184')]
    for wx,wy,rx,ry in [(610,585,90,145),(235,655,112,150)]:
        s+=[f'<ellipse cx="{wx}" cy="{wy}" rx="{rx}" ry="{ry}" fill="#715336" stroke="#342b23" stroke-width="15"/>',f'<ellipse cx="{wx}" cy="{wy}" rx="{rx-18}" ry="{ry-20}" fill="#bd9256"/>']
        for k in range(8):
            a=math.radians(k*45+f*45);x=wx+(rx-24)*math.cos(a);y=wy+(ry-26)*math.sin(a)
            s+=[f'<path d="M{wx} {wy} L{x:.2f} {y:.2f}" stroke="#59412b" stroke-width="12"/>']
        s+=[f'<ellipse cx="{wx}" cy="{wy}" rx="22" ry="30" fill="#6c5d46"/>']
    # Far legs first, then complete horse body, then near legs: ownership stable.
    for name in ['RH','RF']:
        hx,hy,bx,by,o=legs[name];x,y=poses[name]['hoof'];mx=(hx+x)/2-8;my=(hy+bob+y)/2
        s+=[path(f'M{hx} {hy+bob} Q{mx} {my} {x} {y-14}','none','#765036',35),path(f'M{x-20} {y-14} Q{x} {y-28} {x+23} {y} L{x-18} {y+6} Z','#978269')]
    s+=[path(f'M660 {765+bob} Q645 {650+bob} 770 {620+bob} Q870 {590+bob} 1015 {710+bob} L1070 {625+bob} L1145 {550+bob} Q1210 {590+bob} 1200 {680+bob} L1170 {740+bob} Q1130 {760+bob} 1100 {718+bob} L1035 {900+bob} Q840 {960+bob} 710 {850+bob} Z','#a3663d'),path(f'M1010 {710+bob} Q1050 {580+bob} 1150 {551+bob} L1135 {588+bob} Q1080 {625+bob} 1050 {745+bob} Z','#302b28'),path(f'M1140 {566+bob} L1137 {514+bob} L1157 {548+bob} M1180 {575+bob} L1198 {528+bob} L1195 {590+bob}','#995b33')]
    for name in ['LH','LF']:
        hx,hy,bx,by,o=legs[name];x,y=poses[name]['hoof'];mx=(hx+x)/2-8;my=(hy+bob+y)/2
        s+=[path(f'M{hx} {hy+bob} Q{mx} {my} {x} {y-14}','none','#925937',39),path(f'M{x-20} {y-14} Q{x} {y-28} {x+23} {y} L{x-18} {y+6} Z','#ae9477')]
    s+=[path(f'M670 690 L930 {866+bob} M715 580 L1040 {760+bob}','none','#a87742',22),path(f'M700 {727+bob} Q920 {830+bob} 1040 {785+bob} M1020 {715+bob} Q1000 {820+bob} 1050 {863+bob} Q1110 {830+bob} 1130 {738+bob}','none','#3d2c23',18),path(f'M1165 {620+bob} L1185 {707+bob} L1137 {688+bob} Z','none','#3d2c23',10),'<circle cx="1170" cy="624" r="7" fill="#181b19"/>','</svg>']
    (P/f'F{f}.svg').write_text('\n'.join(s))
(P/'phase-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
(P/'input-pins.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'inputs':pins},indent=2)+'\n')
