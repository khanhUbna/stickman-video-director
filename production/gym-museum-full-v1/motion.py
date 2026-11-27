"""Transforms of the genuinely approved V2 contact choreography; no front-X gait."""
import math
import artwork as A
import gait as G
import locomotion_art as L

def relocate(state,start=490,ground=620,direction=1):
 # Source state faces right at nominal490; mirror/translate actual contact geometry.
 ox,oy=start-490,ground-620
 def p(a):return(start+direction*(a[0]-490),a[1]+oy)
 s=dict(state);s['x'],s['root']=p((state['x'],0))[0],p((state['root'],0))[0];s['hip']=p(state['hip']);s['ground']=ground;s['direction']=direction
 s['feet']=[dict(f,ankle=p(f['ankle']),anchor=p((f['anchor'],0))[0] if f['anchor'] is not None else None,pivot=p(f['pivot']) if f['pivot'] else None,ground=f['ground']+oy,direction=direction) for f in state['feet']]
 return s

def walk(c,elapsed,role,start=490,ground=620,direction=1,talk=False,mood='neutral',bag=False):
 clock=2.30+max(0,min(2.84,elapsed));state=relocate(G.pose(clock,'VALE'),start,ground,direction);hand=None
 if bag:hand=(state['hip'][0]+direction*43,state['hip'][1]+28)
 out=L.render(c,clock,role,talk,mood,hand=hand,state_override=state)
 if bag:
  x,y=out['hands'][1];c.line([(x-12,y+17),(x-10,y+2),(x+10,y+2),(x+12,y+17)],'#785c44',3);c.rect((x-22,y+15,x+22,y+72),'#cba275',r=5);c.line([(x-20,y+33),(x+20,y+33)],'#b68b62',2)
 return out

def belt(c,elapsed,role,x=690,ground=620,talk=False,mood='neutral',grip=False,hand_target=None,left_target=None):
 clock=14.57+max(0,elapsed);state=G.pose(clock,'VALE');dx=x-690;dy=ground-620
 def p(a):return(a[0]+dx,a[1]+dy)
 state=dict(state,x=state['x']+dx,root=state['root']+dx,hip=p(state['hip']),ground=ground,feet=[dict(f,ankle=p(f['ankle']),anchor=f['anchor']+dx if f['anchor'] is not None else None,pivot=p(f['pivot']) if f['pivot'] else None,ground=ground) for f in state['feet']])
 rgoal=(x+80,ground-164);lgoal=(x+20,ground-164)
 if 0<float(grip)<1:
  probe=L.render(A.C(),clock,role,False,mood,state_override=state);rgoal=tuple(G.mix(a,b,float(grip)) for a,b in zip(probe['hands'][1],rgoal));lgoal=tuple(G.mix(a,b,float(grip)) for a,b in zip(probe['hands'][0],lgoal))
 return L.render(c,clock,role,talk,mood,hand=hand_target if hand_target is not None else rgoal if grip else None,left=left_target if left_target is not None else lgoal if grip else None,state_override=state)

def run(c,elapsed,role='MINA',start=1152,ground=626,talk=False):
 clock=9.40+max(0,min(1.414,elapsed));s=G.pose(clock,'MINA');dx=start-1152;dy=ground-626
 def p(a):return(a[0]+dx,a[1]+dy)
 s=dict(s,x=s['x']+dx,root=s['root']+dx,hip=p(s['hip']),ground=ground,feet=[dict(f,ankle=p(f['ankle']),anchor=f['anchor']+dx if f['anchor'] is not None else None,pivot=p(f['pivot']) if f['pivot'] else None,ground=ground) for f in s['feet']])
 return L.render(c,clock,role,talk,'worried',state_override=s)

def stairs(c,elapsed,role='MEMBER',talk=False):
 clock=2.3+max(0,min(2.59,elapsed));source=G.pose(clock,'VALE');state=relocate(source,620,640,1)
 def level(x):return 640-28*max(0,min(4,int((x-650)//55)+1))
 def foot(track):
  anchor=track['initial']+130;touch=-999
  for a,b,new0 in track['moves']:
   new=new0+130
   if clock<a:return G.stance(anchor,level(anchor),clock,touch,a,1)
   if clock<b:
    u=G.clamp((clock-a)/(b-a));aa=G.planted(anchor,level(anchor),25,1,'toe')['ankle'];bb=G.planted(new,level(new),-10,1,'heel')['ankle'];low=min(level(anchor),level(new))-32;v=1-u;c1=(G.mix(aa[0],bb[0],.22),low);c2=(G.mix(aa[0],bb[0],.78),low)
    xy=(v**3*aa[0]+3*v*v*u*c1[0]+3*v*u*u*c2[0]+u**3*bb[0],v**3*aa[1]+3*v*v*u*c1[1]+3*v*u*u*c2[1]+u**3*bb[1]);angle=G.hermite(u,[(0,25,-28),(.38,5,-70),(.78,-12,0),(1,-10,0)])
    return {'ankle':xy,'anchor':None,'ground':level(new),'angle':angle,'contact':'air','pivot':None,'direction':1}
   anchor=new;touch=b
  return G.stance(anchor,level(anchor),clock,touch,999,1)
 state['feet']=[foot(f) for f in G.VALE_FEET];virtual=G.hermite(elapsed,[(0,640,0),(.6,620,-40),(1.15,593,-50),(1.7,565,-50),(2.3,540,-20),(2.59,537,0)])
 hx=state['hip'][0];hy=virtual-125
 for i,f in enumerate(state['feet']):
  span=f['ankle'][0]-(hx+(-3 if i==0 else 3));hy=max(hy,f['ankle'][1]-math.sqrt(max(1,134.5**2-span**2)))
 state.update(hip=(hx,hy),ground=virtual);hand=(hx+43,hy+28);out=L.render(c,clock,role,talk,'happy',hand=hand,state_override=state)
 x,y=out['hands'][1];c.line([(x-12,y+17),(x-10,y+2),(x+10,y+2),(x+12,y+17)],'#785c44',3);c.rect((x-22,y+15,x+22,y+72),'#cba275',r=5)
 return out

def stopped_belt(c,elapsed,settle,role='VALE',talk=False,hand_target=None):
 clock=14.57+elapsed;state=dict(G.pose(clock,'VALE'));u=G.ease(settle/.3);feet=[]
 for i,f in enumerate(state['feet']):
  if f['contact']=='air':
   target=G.planted(690+(-12 if i==0 else 25),620,0,1,'flat');ankle=(G.mix(f['ankle'][0],target['ankle'][0],u),G.mix(f['ankle'][1],target['ankle'][1],u));feet.append(dict(target,ankle=ankle,angle=G.mix(f['angle'],0,u)))
  else:feet.append(G.planted(f['anchor'],620,f['angle']*(1-u),1,f['contact']))
 hx=state['hip'][0];hy=G.mix(state['hip'][1],488,u)
 for i,f in enumerate(feet):hy=max(hy,f['ankle'][1]-math.sqrt(max(1,134.5**2-(f['ankle'][0]-hx)**2)))
 state.update(hip=(hx,hy),feet=feet,moving=False,lean=G.mix(state['lean'],0,u));return L.render(c,clock,role,talk,'neutral',hand=hand_target or (770,456),left=(710,456),state_override=state)

def cruise(c,elapsed,role,start=360,ground=626,direction=1,talk=False,mood='neutral',bag=False,hand_target=None):
 # The approved belt gait converted to floor travel: root velocity cancels stance-foot belt velocity.
 clock=14.57+max(0,elapsed);state=G.pose(clock,'VALE');travel=start+direction*G.BELT_SPEED*max(0,elapsed);dy=ground-620
 def p(a):return(travel+direction*(a[0]-690),a[1]+dy)
 state=dict(state,x=p((state['x'],0))[0],root=travel,hip=p(state['hip']),ground=ground,direction=direction,feet=[dict(f,ankle=p(f['ankle']),anchor=p((f['anchor'],0))[0] if f['anchor'] is not None else None,pivot=p(f['pivot']) if f['pivot'] else None,ground=ground,direction=direction) for f in state['feet']])
 hand=hand_target if hand_target is not None else (state['hip'][0]+direction*43,state['hip'][1]+28) if bag else None
 out=L.render(c,clock,role,talk,mood,hand=hand,state_override=state)
 if bag:
  x,y=out['hands'][1];c.line([(x-12,y+17),(x-10,y+2),(x+10,y+2),(x+12,y+17)],'#785c44',3);c.rect((x-22,y+15,x+22,y+72),'#cba275',r=5)
 return out
