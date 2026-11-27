"""Simple original cartoon face drawn natively for this vector stickman video.
Silver hair and glasses are style cues; no portrait texture or photo cutout.
"""
from PIL import Image,ImageDraw
import math
def curve(a,b,c,d,n=20):
 return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],(1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1]) for t in [i/n for i in range(n+1)]]
def draw(im,t,anchor,amp):
 ss=3;head=Image.new('RGBA',(200*ss,180*ss));p=ImageDraw.Draw(head)
 ink='#343e48';skin='#edb18b'
 def b(q):return tuple(round(v*ss) for v in q)
 def line(q,fill=ink,width=2):p.line([(round(x*ss),round(y*ss)) for x,y in q],fill=fill,width=round(width*ss),joint='curve')
 def poly(q,fill,outline=ink):p.polygon([(round(x*ss),round(y*ss)) for x,y in q],fill=fill);line(q+[q[0]],outline,2)
 # A single coherent silhouette: ears, head, then swept cartoon hair.
 p.ellipse(b((46,80,65,104)),fill=skin,outline=ink,width=2*ss)
 p.ellipse(b((136,80,155,104)),fill=skin,outline=ink,width=2*ss)
 p.ellipse(b((54,34,147,140)),fill=skin,outline=ink,width=2*ss)
 hair=curve((51,83),(35,42),(61,12),(98,20))+curve((98,20),(118,2),(148,22),(155,50))+curve((155,50),(156,68),(150,80),(144,86))+[(138,62)]+curve((138,62),(124,59),(130,45),(122,43))+curve((122,43),(104,61),(77,49),(64,70))+[(61,87),(51,83)]
 poly(hair,'#b9c0c7')
 line(curve((53,55),(71,31),(100,40),(123,25)),fill='#e7e9eb',width=4)
 line(curve((60,45),(78,22),(106,30),(121,23)),fill='#87939f',width=2)
 line([(146,58),(144,81)],fill='#7f8d98',width=4)
 # Brows and glasses remain readable at the video's actual size.
 line(curve((65,72),(72,67),(81,67),(87,71)),width=2)
 line(curve((112,71),(119,67),(127,68),(134,73)),width=2)
 p.rounded_rectangle(b((60,77,94,99)),radius=7*ss,outline=ink,width=3*ss)
 p.rounded_rectangle(b((105,77,139,99)),radius=7*ss,outline=ink,width=3*ss)
 line([(94,84),(100,82),(105,84)],width=2)
 line([(60,83),(52,80)],width=2);line([(139,83),(149,80)],width=2)
 blink=any(a<t<a+.13 for a in [3.9,11.7,17.7])
 for x in [79,121]:
  if blink:line([(x-4,89),(x+4,89)],width=2)
  else:p.ellipse(b((x-2,84,x+3,91)),fill=ink)
 line([(101,89),(98,103),(105,104)],fill='#ad7352',width=2)
 if amp>.06:
  h=4+amp*13;p.ellipse(b((86,117-h/2,115,117+h/2)),fill='#57372e')
  if h>10:p.rounded_rectangle(b((90,117-h/2,111,120-h/2)),radius=ss,fill='#fff5e4')
 else:line(curve((85,115),(91,123),(106,126),(117,113)),fill='#6e4636',width=2)
 head=head.resize((170,153),Image.Resampling.LANCZOS)
 a=(85,127.5);cx,cy=head.width/2,head.height/2
 ang=1.2*math.sin(t*2.1)-(3*math.sin(math.pi*(t-19)) if t>19 else 0)
 r=math.radians(ang);rot=head.rotate(-ang,Image.Resampling.BICUBIC,expand=True)
 off=(math.cos(r)*(a[0]-cx)-math.sin(r)*(a[1]-cy),math.sin(r)*(a[0]-cx)+math.cos(r)*(a[1]-cy))
 im.alpha_composite(rot,(round(anchor[0]-rot.width/2-off[0]),round(anchor[1]-rot.height/2-off[1])))
