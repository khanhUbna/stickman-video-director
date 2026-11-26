"""Twenty-second review sample. Three real OpenAI roles, word-led cuts, body/prop action."""
from pathlib import Path
import json,bisect,math
from PIL import ImageDraw
import artwork as A
P=Path(__file__).resolve().parent
TURNS=json.loads((P/'turns20.json').read_text());WORDS=json.loads((P/'words20.json').read_text());CUES=json.loads((P/'captions20.json').read_text());LEVELS=json.loads((P/'mouth-levels.json').read_text())
SHOTS=[
 {'start':0,'end':1.30,'mode':'live-wide','camera':(1,0,0),'purpose':'Camera tally and Vale waiting beside the stationary belt'},
 {'start':1.30,'end':2.30,'mode':'banner','camera':(1.35,140,50),'purpose':'The announced ancient-cruelty headline'},
 {'start':2.30,'end':5.14,'mode':'step-in','camera':(1.8,380,300),'purpose':'Vale physically walks onto stationary belt; foot contact remains visible'},
 {'start':5.14,'end':6.80,'mode':'solemn-hand','camera':(1.85,400,225),'purpose':'Raised palm, proud expression, actual anticipation and lift'},
 {'start':6.80,'end':9.45,'mode':'vale-speaks','camera':(2.1,420,225),'purpose':'Onyx line with voice-energy mouth and steady raised hand'},
 {'start':9.45,'end':10.814,'mode':'mina-runs','camera':(1.35,380,180),'purpose':'Mina runs left toward Vale, opposing arm swing and planted stance feet'},
 {'start':10.814,'end':13.28,'mode':'warning','camera':(1.8,485,220),'purpose':'Nova warning, Vale lowers hand and looks toward her'},
 {'start':13.28,'end':14.71,'mode':'safety-contact','camera':(2.15,520,225),'purpose':'Hand-to-vest clip contact, release, then button contact'},
 {'start':14.71,'end':16.55,'mode':'question','camera':(1.7,360,230),'purpose':'Moving belt and grounded steps while Vale asks his question'},
 {'start':16.55,'end':17.95,'mode':'reply','camera':(2.05,550,215),'purpose':'Mina dry reply and small palm-up gesture'},
 {'start':17.95,'end':20,'mode':'reaction','camera':(1.6,340,220),'purpose':'Vale discovers he is simply walking; camera/incorrect headline remain live'}]
STARTS=[s['start'] for s in SHOTS]
def speaker(t):
 for r in TURNS:
  if r['start']<=t<=r['end']:return r['speaker']
 return ''
def mouth(t,role):return LEVELS[min(599,int(t*30))] if speaker(t)==role else False
def frame(t,caption=True):
 s=SHOTS[max(0,bisect.bisect_right(STARTS,t)-1)];mode=s['mode'];c=A.C(s['camera']);A.background(c,'stage',t,title='ANCIENT CRUELTY')
 # Add stage-specific depth and a readable second banner line without extra chart clutter.
 c.text(640,182,'LIVE DEMONSTRATION',25,'#ddc8a6',anchor='mt');c.text(640,235,'DR. VALE · MUSEUM OF HUMAN HISTORY',16,'#a8c8c9',anchor='mt')
 walking=t>=14.57;A.treadmill(c,675,620,t-14.57,walking)
 # Vale's grounded approach uses root velocity equal to the gait's stance velocity.
 if 2.30<=t<4.80:
  xx=490+80*(t-2.30);va='walk';speed=80
 elif t<2.30:xx=490;va='stand';speed=0
 else:xx=690;va='belt' if walking else 'stand';speed=72 if walking else 0
 alpha=A.smooth((t-5.14)/.6) if t<9.24 else 1-A.smooth((t-9.24)/.5)
 alpha=max(0,min(1,alpha));hand=None;left=None
 if 5.14<=t<9.74:
  hand=(xx+53+35*math.sin(math.pi*alpha)+62*alpha,A.lerp(518,293,alpha))
 if walking:hand=(770,456);left=(710,456)
 mood='confident' if t<11.16 else 'surprised' if t<14.57 else 'worried' if t<17.76 else 'neutral'
 feet=None;body_t=t
 if 4.8<=t<14.57:
  # Keep the stance foot fixed while the final swing foot lands; no planted-foot reset.
  phase=(4.8/.9+.5)%1;sv=(phase-.6)/.4;oldx=690+(-21.6+43.2*A.smooth(sv))+10;oldy=620-math.sin(math.pi*sv)*20;land=A.smooth((t-4.8)/.23);feet=[(677.6,620),(A.lerp(oldx,713,land),A.lerp(oldy,620,land))]
 if walking:
  body_t=t-14.57+.337037037*.9
  if t<14.77:
   phase=(body_t/.9+.5)%1;sv=(phase-.6)/.4;dx=-19.44+38.88*A.smooth(sv)+10;fy=620-math.sin(math.pi*sv)*20;launch=A.smooth((t-14.57)/.2);feet=[(677.6-72*(t-14.57),620),(A.lerp(713,690+dx,launch),A.lerp(620,fy,launch))]
 vale=A.person(c,xx,ground=620,t=body_t,role='VALE',action=va,talk=mouth(t,'VALE'),mood=mood,hand=hand,left=left,walk_speed=speed,gaze=3 if t>=10.9 else 0,feet_override=feet)
 # Mina enters only when the script calls for her. Cut to a closer reaction as she plants to stop.
 if t>=9.45:
  end=10.814;moving=t<end;mx=1160-220*(t-9.45) if moving else 860
  action='run' if moving else 'stand';lh=None;rh=None;u=0
  if 11.16<=t<12.3:
   u=A.smooth((t-11.16)/.28)*(1-A.smooth((t-11.88)/.3));rh=(mx+53+87*u,A.lerp(524,356,u))
  # Clip is hand-bound until visible attachment; the cord remains when the hand leaves.
  if t>=13.28:
   clip=(705,411);button=(794,403)
   if t<14.04:
    u=A.smooth((t-13.28)/.6);lh=(A.lerp(807,clip[0],u),A.lerp(524,clip[1],u))
   elif t<14.60:
    u=A.smooth((t-14.04)/.51);lh=(A.lerp(clip[0],button[0],u),A.lerp(clip[1],button[1],u))
   elif t<14.95:
    u=A.smooth((t-14.60)/.35);lh=(A.lerp(button[0],807,u),A.lerp(button[1],524,u))
   if t>=13.88:
    c.line([clip,(768,483),button],'#af5651',3);c.rect((clip[0]-5,clip[1]-5,clip[0]+5,clip[1]+5),'#c55d50',r=2,w=1)
  if 16.65<t<18.3:
   u=A.smooth((t-16.65)/.3)*(1-A.smooth((t-17.8)/.5));lh=(A.lerp(807,765,u),A.lerp(524,411,u))
  mina=A.person(c,mx,ground=626,t=t,role='MINA',action=action,talk=mouth(t,'MINA'),mood='worried' if t<13.5 else 'confident',left=lh,hand=rh,walk_speed=-220 if moving else 0,gaze=-3)
 im=c.im
 if caption:
  active=next((cue for cue in CUES if cue['start']<=t<cue['end']),None)
  if active:
   d=ImageDraw.Draw(im);f=A.font(42);bb=d.textbbox((0,0),active['text'],font=f);width=bb[2]-bb[0];assert width<1730,(active['text'],width)
   box=(960-width/2-27,969,960+width/2+27,1045);d.rounded_rectangle(box,12,'#fff6e1',outline=A.INK,width=2)
   col={'NARRATOR':A.TEAL,'VALE':'#795a83','MINA':A.ORANGE}[active['role']];d.rounded_rectangle((box[0]+5,976,box[0]+11,1038),3,col);d.text((960-width/2,981),active['text'],font=f,fill=A.INK)
 return im,s
if __name__=='__main__':
 (P/'timeline.json').write_text(json.dumps({'duration':20,'fps':30,'resolution':[1920,1080],'actual_word_aligned':True,'shots':SHOTS},indent=2)+'\n')
 print('shots',len(SHOTS))
