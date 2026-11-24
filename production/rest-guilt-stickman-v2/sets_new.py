"""New painted story stages; foreground supports share actor contact coordinates."""
from pathlib import Path
from functools import lru_cache
import math
from PIL import Image,ImageDraw
import sets as legacy
from rig import line,poly
B=Path(__file__).resolve().parent
table=legacy.table

def sofa(g):
 poly(g,[(488,460),(493,365),(522,344),(823,347),(852,372),(857,502),(488,502)],'#bb856e','#78594a',4)
 for x in [515,675]:g.rounded_rectangle((x,365,x+144,467),20,fill='#c7937b',outline='#a77660',width=3)
 g.rounded_rectangle((487,458,857,503),16,fill='#d5aa8e',outline='#78594a',width=4)
 for x in [468,838]:g.rounded_rectangle((x,420,x+40,520),15,fill='#b78168',outline='#78594a',width=4)
 for x in [507,812]:line(g,[(x,504),(x,548)],'#705645',7)

@lru_cache(maxsize=20)
def background(name,night=False):
 p=B/f'art/painted-{name}.png'
 if not p.exists():return legacy.background(name,night)
 im=Image.open(p).convert('RGBA');g=ImageDraw.Draw(im)
 if name=='living':
  legacy.rug(g,(365,550,1080,698));sofa(g);table(g,915,440,130)
 elif name=='park':
  for xx in [850,1100]:line(g,[(xx,465),(xx,590)],'#6c6250',8)
  for yy in [380,415,450]:g.rounded_rectangle((825,yy,1132,yy+21),5,fill='#9c7d56',outline='#6e5b43',width=3)
  g.rounded_rectangle((815,475,1142,500),6,fill='#b69870',outline='#6e5b43',width=3)
 return im

def moving_world(im,name,elapsed,night=False):
 if name in ['street','park']:legacy.moving_world(im,name,elapsed,night)
 if name=='laundry':
  # Washer drum motion stays inside the painted circular window; not a full-room zoom.
  g=ImageDraw.Draw(im);x,y=157,444
  for k in range(3):
   a=elapsed*.75+k*math.tau/3
   cx=x+20*math.cos(a);cy=y+20*math.sin(a)
   g.arc((cx-7,cy-7,cx+7,cy+7),20,190,fill=(161,163,142,150),width=2)
 if name=='living':
  # One distant lit window changes; the room and principal actor remain the focus.
  g=ImageDraw.Draw(im)
  if int(elapsed/3)%2==0:g.rectangle((471,211,477,220),fill=(229,189,109,100))
