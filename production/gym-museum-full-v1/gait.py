"""Authored foot contact and locomotion poses. No paid services or wall-clock animation.
Floor contacts remain fixed; treadmill contacts advect with the belt. Ankles rock
around heel/toe pivots. Swing phases and COM are authored, not a whole-sprite slide.
"""
import math
from bisect import bisect_right

def clamp(u):return max(0.,min(1.,u))
def ease(u):u=clamp(u);return u*u*(3-2*u)
def mix(a,b,u):return a+(b-a)*u
def hermite(t,keys):
 # keys = time, value, derivative. Clamped on either side.
 if t<=keys[0][0]:return keys[0][1]
 if t>=keys[-1][0]:return keys[-1][1]
 i=bisect_right([r[0] for r in keys],t)-1;a,x,v=keys[i];b,y,w=keys[i+1];h=b-a;u=(t-a)/h
 return (2*u**3-3*u**2+1)*x+(u**3-2*u**2+u)*h*v+(-2*u**3+3*u**2)*y+(u**3-u**2)*h*w

def rotate(p,ang,direction):
 # Local shoe faces +x; reflect for left-facing characters after rotation.
 x,y=p;r=math.radians(ang)
 return (direction*(x*math.cos(r)-y*math.sin(r)),x*math.sin(r)+y*math.cos(r))

def planted(anchor,ground,angle,direction,mode):
 pivot_local=(-10.,5.) if mode=='heel' else (24.,5.) if mode=='toe' else (0.,5.)
 pivot=(anchor+direction*pivot_local[0],ground);off=rotate(pivot_local,angle,direction)
 return {'ankle':(pivot[0]-off[0],pivot[1]-off[1]),'anchor':anchor,'ground':ground,'angle':angle,'contact':mode,'pivot':pivot,'direction':direction}

def stance(anchor,ground,t,touch,toff,direction,run=False):
 load=.075 if run else .12;push=.095 if run else .14
 if t<touch+load:
  a=mix(-10,-0.0,ease((t-touch)/load));return planted(anchor,ground,a,direction,'heel')
 if t>toff-push:
  a=mix(0,31 if run else 25,ease((t-(toff-push))/push));return planted(anchor,ground,a,direction,'toe')
 return planted(anchor,ground,0,direction,'flat')

def swing(t,start,end,old,new,ground,direction,run=False):
 u=clamp((t-start)/(end-start));a=planted(old,ground,31 if run else 25,direction,'toe')['ankle'];b=planted(new,ground,-10,direction,'heel')['ankle']
 # Cubic Bezier: ankle lifts after toe-off, then extends to a soft heel strike.
 height=62 if run else (28 if abs(new-old)>35 else 18)
 c1=(mix(a[0],b[0],.23),ground-height);c2=(mix(a[0],b[0],.76),ground-height*.95)
 v=1-u;p=(v**3*a[0]+3*v*v*u*c1[0]+3*v*u*u*c2[0]+u**3*b[0],v**3*a[1]+3*v*v*u*c1[1]+3*v*u*u*c2[1]+u**3*b[1])
 angle=hermite(u,[(0,31 if run else 25,-28),(.38,5,-70),(.78,-12,0),(1,-10,0)])
 return {'ankle':p,'anchor':None,'ground':ground,'angle':angle,'contact':'air','pivot':None,'direction':direction}

VALE_FEET=[
 {'initial':475,'moves':[(2.48,2.90,555),(3.50,3.94,659),(4.53,4.89,676)]},
 {'initial':505,'moves':[(2.98,3.42,609),(4.02,4.46,705)]}]
MINA_FEET=[
 {'initial':1180,'moves':[(9.40,9.70,1058),(9.87,10.30,897),(10.46,10.80,874)]},
 {'initial':1150,'moves':[(9.60,9.99,973),(10.17,10.56,846)]}]
VALE_ROOT=[(2.30,490,0),(2.48,495,50),(2.90,533,90),(3.42,580,95),(3.94,630,95),(4.46,676,55),(4.89,690,0)]
MINA_ROOT=[(9.40,1152,-230),(9.70,1080,-245),(9.99,1010,-245),(10.30,930,-230),(10.56,874,-120),(10.814,860,0)]

def scheduled_foot(t,track,ground,direction,run=False):
 anchor=track['initial'];touch=-999
 for start,end,new in track['moves']:
  if t<start:return stance(anchor,ground,t,touch,start,direction,run)
  if t<end:return swing(t,start,end,anchor,new,ground,direction,run)
  anchor=new;touch=end
 return stance(anchor,ground,t,touch,999,direction,run)

BELT_SPEED=96.

def belt_foot(t,leg):
 start=14.57;ground=620.;speed=BELT_SPEED;period=1.08;stance_time=.68;launch=.4
 # Match the authored final floor stance, then begin with a single trailing-foot swing.
 if leg==0:
  if t<start+.18:
   return stance(676-speed*max(0,t-start),ground,t,-999,start+.18,1)
  if t<start+.54:
   return swing(t,start+.18,start+.54,676-speed*.18,718,ground,1)
  touch=start+.54;initial=718
 else:
  if t<start+.68:
   return stance(705-speed*max(0,t-start),ground,t,-999,start+.68,1)
  if t<start+period:
   return swing(t,start+.68,start+period,705-speed*.68,718,ground,1)
  touch=start+period;initial=718
 # A planted anchor travels with the belt between touchdown and toe-off.
 while t>=touch+period:touch+=period
 offset=initial # Consistent new touchdown location for this leg every cycle.
 q=t-touch
 if q<stance_time:
  return stance(offset-speed*q,ground,t,touch,touch+stance_time,1)
 # Current toe-off world point and the NEXT landing's world point.
 old=offset-speed*stance_time
 return swing(t,touch+stance_time,touch+period,old,offset,ground,1)

def pose(t,who):
 if who=='VALE':
  if t<14.57:
   x=hermite(t,VALE_ROOT);feet=[scheduled_foot(t,a,620,1) for a in VALE_FEET];direction=1;run=False;moving=2.35<t<4.89
   contacts=[2.90,3.42,3.94,4.46,4.89];phase=(t-2.90)/.52
   activity=ease((t-2.30)/.25)*(1-ease((t-4.46)/.43))
   height=132-(5+3*math.cos(2*math.pi*phase))*activity
   lean=(4+1.2*math.sin(2*math.pi*phase))*activity;arm_phase=2*math.pi*((t-2.48)/1.04)
  else:
   x=690.;feet=[belt_foot(t,i) for i in range(2)];direction=1;run=False;moving=True
   activity=ease((t-14.57)/.38);phase=(t-14.57)/.54
   height=mix(132,130-4*math.cos(2*math.pi*phase),activity);lean=5*activity+1.2*math.sin(math.pi*phase)*activity;arm_phase=math.pi*phase
 else:
  direction=-1;run=True;x=hermite(t,MINA_ROOT);feet=[scheduled_foot(t,a,626,-1,True) for a in MINA_FEET];moving=t<10.814
  settle=ease((t-10.53)/.284);phase=(t-9.40)/.30
  flight=1 if all(f['contact']=='air' for f in feet) else 0
  height=mix(117+3*math.sin(2*math.pi*phase)+4*flight,132,settle)
  lean=mix(14,0,settle);arm_phase=math.pi*phase
 ground=620 if who=='VALE' else 626
 # Small fore/aft pelvis transfer; feet remain independently planted.
 sway=(1.5*math.sin(arm_phase) if moving else 0)
 hipx=x+sway;hipy=ground-height
 # Bound full extension smoothly by actual ankle reach, keeping limb lengths fixed.
 for i,f in enumerate(feet):
  span=abs(f['ankle'][0]-(hipx+(-3 if i==0 else 3)))
  ceiling=math.sqrt(max(1,134.5**2-span**2))
  hipy=max(hipy,f['ankle'][1]-ceiling)
 return {'x':hipx,'root':x,'hip':(hipx,hipy),'feet':feet,'direction':direction,'run':run,'moving':moving,'lean':lean,'arm_phase':arm_phase,'ground':ground}

# Actual impact times for locally re-spotting Foley; no narration timing changes.
WALK_CONTACTS=[2.90,3.42,3.94,4.46,4.89]
RUN_CONTACTS=[9.70,9.99,10.30,10.56,10.80]
BELT_CONTACTS=sorted([14.57+i*1.08 for i in range(6)]+[15.11+i*1.08 for i in range(5)])
