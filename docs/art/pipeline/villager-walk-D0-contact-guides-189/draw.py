from pathlib import Path
import json
p=Path(__file__).parent
# A viewer-left OUTER hip is foreground in BOTH drawings; B inner hip stays behind.
plans=[('F00',(139,185,152,223),(124,169,117,193),-4,4),('F04',(110,172,100,197),(156,187,169,219),4,-4)]
for name,A,B,na,fa in plans:
 def path(d,c,stroke='#4b4032',w=1):return f'<path d="{d}" fill="{c}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'
 def leg(v,isA,advancing):
  kx,ky,ax,ay=v;hx=120 if isA else 145
  base='#6d807a' if isA else '#8c7168';light='#9eada1' if isA else '#af9181';wrap='#b7c5ad' if isA else '#ceb49c'
  s=path(f'M {hx-13} 145 Q {hx+15} 145 {hx+13} 161 Q {kx+14} {ky-9} {kx+12} {ky+3} L {ax+7} {ay-13} Q {ax+10} {ay-5} {ax+3} {ay-4} L {ax-9} {ay-7} L {kx-12} {ky+3} Q {kx-17} {ky-4} {hx-13} 145 Z',base)
  s+=path(f'M {hx-8} 152 Q {kx-7} {ky-7} {kx-5} {ky+2} L {ax-5} {ay-14} L {ax+1} {ay-15} L {kx+5} {ky} Q {kx+8} {ky-8} {hx+2} 153 Z',light,w=0)
  s+=path(f'M {ax-9} {ay-15} Q {ax+1} {ay-12} {ax+7} {ay-14} L {ax+6} {ay-3} Q {ax} {ay+1} {ax-8} {ay-5} Z',wrap)
  # Heel strike: forward heel on its plane, toe four pixels above plane.
  # Trailing push-off: toe on plane, heel seven pixels above its plane.
  heel=(ax-10,ay+3) if advancing else (ax-10,ay-4)
  toe=(ax+12,ay+10) if advancing else (ax+12,ay+14)
  hx0,hy=heel;tx,ty=toe
  s+=path(f'M {ax-8} {ay-4} Q {ax+2} {ay-2} {tx-2} {ty-4} Q {tx+3} {ty-1} {tx} {ty} L {hx0} {hy} Q {hx0-3} {hy-3} {ax-8} {ay-4} Z','#a8865e')
  s+=path(f'M {hx0} {hy} L {tx} {ty} M {ax-3} {ay-3} L {ax+1} {ay+4}','none','#514332',1.4)
  return s
 s='<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
 s+=leg(B,False,name=='F04')+leg(A,True,name=='F00')
 # Background sleeve/forearm; its whole outline overlaps the trunk naturally.
 s+=path(f'M 150 66 Q 171 73 172 95 L {170+fa} 119 L {175+fa} 150 Q {174+fa} 159 {168+fa} 157 L {163+fa} 145 L {159+fa} 120 L 152 98 Z','#a99d84')
 s+=path(f'M {161+fa} 118 L {169+fa} 117 L {174+fa} 150 Q {174+fa} 160 {168+fa} 156 L {163+fa} 145 Z','#aa8260')
 # Connected shoulder/chest/pelvis tunic silhouette, broad canonical mass.
 s+=path('M 115 59 Q 126 54 140 60 L 155 68 Q 166 82 164 106 L 153 117 Q 158 138 166 163 Q 145 171 129 165 L 99 160 Q 103 141 106 119 L 94 107 Q 89 87 99 72 Z','#c5b89b')
 s+=path('M 105 72 Q 108 88 105 111 L 113 120 L 105 156 L 119 161 L 123 117 L 139 67 L 128 63 Z','#e0d1af',w=0)
 s+=path('M 145 69 Q 155 86 149 108 L 140 119 L 151 162 L 165 163 L 153 117 L 163 106 Q 164 81 145 69 Z','#a6987e',w=0)
 s+=path('M 136 67 Q 124 95 109 114 M 117 131 L 113 153 M 144 131 L 153 160','none','#827661',1)
 s+=path('M 105 112 Q 130 118 154 112 L 156 124 Q 128 128 104 122 Z','#655b4e')
 s+=path('M 144 117 L 154 119 L 158 147 L 149 153 L 141 126 Z','#766756')
 # Foreground arm follows independent opposing swing; integrated sleeve rather than capsules.
 s+=path(f'M 102 71 Q 88 74 88 94 L {91+na} 117 Q {98+na} 123 {105+na} 117 L 107 99 L 110 83 Z','#d2c3a2')
 s+=path(f'M {92+na} 116 L {104+na} 117 Q {101+na} 133 {99+na} 146 Q {102+na} 156 {97+na} 159 L {91+na} 155 Q {87+na} 151 {90+na} 143 Z','#b18b65')
 s+=path(f'M 95 80 Q 91 95 {96+na} 112 L {102+na} 115','none','#f0dfb9',2)
 # Neck and ESE face, hat full tonal forms.
 s+=path('M 121 49 L 122 63 L 132 72 L 141 60 L 141 46 Z','#a47d58')
 s+=path('M 117 30 Q 129 24 143 31 L 148 41 L 151 45 L 146 49 L 144 58 L 135 62 L 124 56 L 118 46 Z','#bd956d')
 s+=path('M 139 34 L 146 39 L 147 44 L 142 46 L 144 52 L 136 55 L 132 51 Z','#d2ab7b',w=0)
 s+=path('M 120 34 Q 131 26 142 32 L 133 35 L 123 44 L 120 49 L 116 43 Z','#403b32')
 s+=path('M 105 45 Q 125 27 157 25 Q 169 30 151 43 Q 130 54 105 48 Z','#756044')
 s+=path('M 101 44 L 126 12 Q 150 18 168 29 Q 140 31 101 44 Z','#b99a69')
 s+=path('M 109 37 L 127 16 L 155 26 Q 130 28 109 37 Z','#d8bb85',w=0)
 s+=path('M 102 44 Q 139 29 168 29','none','#e2c898',2)
 s+='</svg>'
 (p/f'{name}-contact.svg').write_text(s)
