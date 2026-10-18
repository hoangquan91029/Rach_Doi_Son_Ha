from pathlib import Path
import json,hashlib
import gi,cairo
from gi.repository import Rsvg
out=Path(__file__).resolve().parent.parent/'guide'
def svg(a):
    dx=-6*a;dy=-2*a
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><metadata>ROOT_AUTHORING_ONLY; whole-clothed Villager South nonfatal hit recovery. Handmade vector, no original pixels. Both sandals remain planted; same camera/groundpivot. No tool, weapon, death or falling.</metadata>
<ellipse cx="133.5" cy="238" rx="39" ry="5" fill="#5b5548" opacity=".20"/>
<path d="M101 153 Q96 173 98 190 Q110 196 121 188 L133 163 L143 189 Q155 196 166 188 Q164 171 157 153Z" fill="#665447" stroke="#453b31" stroke-width="1.2"/>
<path d="M100 189 L118 191 L115 221 L101 220Z M148 192 L165 188 L165 219 L149 220Z" fill="#e5d8b8" stroke="#9c896d" stroke-width="1.1"/>
<path d="M101 220 Q96 226 92 232 Q86 239 97 241 L116 236 L116 220Z M150 220 L167 220 Q177 232 174 240 L154 239 L147 230Z" fill="#b98861" stroke="#594632" stroke-width="1.2"/>
<path d="M95 230 L113 233 M100 222 L110 236 M153 232 L171 230 M156 222 L166 239" fill="none" stroke="#705d3f" stroke-width="2.2"/>
<path d="M{93+dx} {65+dy} Q{81+dx} {74+dy} {79+dx} 96 L{83+dx} 112 Q{91+dx} 119 {101+dx} 111 L{105+dx} 84 L{108+dx/2} 117 L102 150 Q128 162 158 150 L{154+dx/2} 112 L{158+dx} 83 L{162+dx} 111 Q{172+dx} 118 {179+dx} 110 L{177+dx} 93 Q{176+dx} 76 {164+dx} {65+dy} L{141+dx} {57+dy} L{119+dx} {58+dy}Z" fill="#e8dbc3" stroke="#9e8a6d" stroke-width="1.2"/>
<path d="M{86+dx} 111 L{94+dx} 113 L{91+5*a} {137-14*a} Q{89+9*a} {144-15*a} {82+12*a} {142-14*a} L{82+9*a} {137-14*a}Z M{166+dx} 113 L{174+dx} 111 L{174-12*a} {137-13*a} Q{174-14*a} {145-13*a} {168-13*a} {145-12*a} L{164-9*a} {138-12*a}Z" fill="#bb8762" stroke="#7d5b40" stroke-width="1"/>
<path d="M{119+dx} {59+dy} L{139+dx} {73+dy} L{106+dx/2} 118 L107 134 L{146+dx/2} 83 L{139+dx} {59+dy}" fill="#f2e5cd" stroke="#b6a187" stroke-width="1"/>
<path d="M104 103 Q132 112 158 103 L159 113 Q132 121 105 113Z M146 113 L158 112 L165 157 L148 154Z" fill="#685345" stroke="#453c33" stroke-width="1"/>
<path d="M{116+dx} {44+dy} Q{119+dx} {35+dy} {131+dx} {35+dy} Q{145+dx} {35+dy} {148+dx} {47+dy} L{143+dx} {62+dy} L{132+dx} {70+dy} L{120+dx} {61+dy}Z" fill="#c1926d" stroke="#674d37" stroke-width="1.1"/>
<path d="M{119+dx} {43+dy} Q{123+dx} {35+dy} {141+dx} {36+dy} L{146+dx} {49+dy} L{141+dx} {43+dy} L{132+dx} {42+dy} L{122+dx} {48+dy}Z" fill="#302923"/>
<path d="M{120+dx} {54+dy} L{127+dx} {52+dy} M{137+dx} {52+dy} L{143+dx} {54+dy} M{126+dx} {59+dy} L{137+dx} {59+dy} M{130+dx} {61+dy} L{133+dx} {66+dy} L{137+dx} {61+dy}" fill="none" stroke="#46372c" stroke-width="1.2"/>
<path d="M{130+dx} {10+dy} L{163+dx} {34+dy} Q{174+dx} {42+dy} {157+dx} {47+dy} Q{129+dx} {54+dy} {96+dx} {45+dy} Q{86+dx} {42+dy} {96+dx} {34+dy}Z" fill="#c5a876" stroke="#765a37" stroke-width="1.2"/>
<path d="M{130+dx} {11+dy} L{109+dx} {45+dy} M{130+dx} {11+dy} L{129+dx} {49+dy} M{131+dx} {11+dy} L{153+dx} {47+dy} M{99+dx} {34+dy} Q{129+dx} {39+dy} {161+dx} {35+dy} M{95+dx} {42+dy} Q{129+dx} {47+dy} {166+dx} {42+dy}" fill="none" stroke="#9f8051" stroke-width=".7"/>
</svg>'''
for i,a in enumerate([.3,1,.45,0]):
    target=out/f'F{i}.svg';target.write_text(svg(a));handle=Rsvg.Handle.new_from_data(target.read_bytes());surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,256,256);ctx=cairo.Context(surface);rect=Rsvg.Rectangle();rect.x=0;rect.y=0;rect.width=256;rect.height=256;handle.render_document(ctx,rect);surface.write_to_png(str(out/f'F{i}.png'))
print('4 root whole-vector nonfatalhit guides; sourcePixelUse false; authoring only')
