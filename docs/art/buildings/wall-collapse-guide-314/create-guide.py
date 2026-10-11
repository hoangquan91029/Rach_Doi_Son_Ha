from pathlib import Path
import json,hashlib
p=Path(__file__).parent
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<!-- Original whole-plane drawing; fixed 234 foundation anchors. Authoring reference only. No embedded raster, transform, or reused source pixels. -->']
def poly(points,color):
 parts.append(f'<polygon points="{points}" fill="{color}"/>')
# Whole continuous foundation remains at original ground axis.
poly('227,640 1027,1040 1063,1022 263,622','#b3a38a')
poly('227,640 1027,1040 1027,1100 227,700','#8c806b')
poly('1027,1040 1063,1022 1063,1082 1027,1100','#6c6252')
# Central timber plane: one coherent tilted surface with hinge at the original foundation.
poly('270,663 405,425 1135,790 1000,1028','#88603d')
poly('405,425 435,410 1165,775 1135,790','#b99765')
poly('1000,1028 1135,790 1165,775 1030,1013','#59432e')
# Only broad boards and rails, all drawn directly in tilted-plane perspective.
for i in range(1,10):
 x=270+73*i; y=663+36.5*i
 parts.append(f'<path d="M{x},{y} L{x+135},{y-238}" stroke="#4e3b2b" stroke-width="8"/>')
for t in (.15,.5,.85):
 ax,ay=270+135*t,663-238*t
 bx,by=1000+135*t,1028-238*t
 parts.append(f'<path d="M{ax},{ay} L{bx},{by}" stroke="#b18c58" stroke-width="23"/>')
# Single broad splintered break near lower middle; not a disconnected second structure.
poly('644,626 668,651 655,681 684,709 674,733 647,714 657,684 631,657','#433122')
# Broken end posts remain rooted at the exact original ends.
poly('227,470 244,457 261,480 276,470 276,679 227,700','#a4967e')
poly('227,470 244,457 279,472 276,486 261,480 244,486','#c4b89e')
poly('276,486 300,474 300,667 276,679','#776c5a')
poly('1009,876 1027,861 1041,878 1052,870 1052,1088 1027,1100 1009,1091','#a4967e')
poly('1009,876 1027,861 1068,878 1052,892 1041,878 1026,885','#c4b89e')
poly('1052,892 1076,880 1076,1076 1052,1088','#776c5a')
# Few coarse foundation fracture stones; no relocated foundation.
poly('243,678 261,670 280,680 266,700','#ab9b81')
poly('1011,1075 1028,1066 1045,1078 1029,1095','#ab9b81')
parts.append('</svg>')
(p/'guide.svg').write_text('\n'.join(parts)+'\n')
