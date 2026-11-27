"""Live sequence extending the approved V2 poses at actual narration cues."""
import math
import artwork as A
import motion as M
import film as F

def cue(phrase):return F.mark(F.BY[(6,4)],phrase)
START=F.SCENE_START[6];DECISION=F.mark(F.BY[(8,4)],'Instead');STOP=F.mark(F.BY[(8,4)],'button');ATTACH=cue('clip');MOTOR=cue('belt');GRIP=cue('grips')
CAMS={'stage-wide':(1,0,0),'stage-banner':(1.35,140,50),'stage-step':(1.8,380,300),'stage-hand':(1.85,400,225),'stage-speech':(2.1,420,225),'stage-run':(1.35,380,180),'stage-warning':(1.8,485,220),'stage-stop':(2.15,520,225),'stage-clip':(2.15,520,225),'stage-start':(2.15,520,225),'stage-walk':(1.65,325,230),'stage-feet':(2.05,425,340),'stage-question':(1.7,360,230),'stage-reply':(2.05,550,215),'stage-reaction':(1.6,340,220),'stage-headline':(1.25,140,80)}

def draw(t,mode,camera=None,extra=None,screen_layer=None):
 local=t-START;cam=camera or CAMS.get(mode,(1.6,340,220));c=A.C(cam)
 A.background(c,'stage',t,title='HUMANS PAID TO BE TORTURED');c.text(640,183,'LIVE DEMONSTRATION',25,'#ddc8a6',anchor='mt');c.text(640,235,'DR. VALE · MUSEUM OF HUMAN HISTORY',16,'#a8c8c9',anchor='mt')
 if screen_layer:screen_layer(c)
 # Broadcast control is a real nearby device within the actor arm reach.
 c.rect((535,400,620,445),'#a75d59',r=5);c.text(578,414,'END LIVE',11,'#fff8df',anchor='mt');c.line([(578,445),(578,626)],A.INK,5)
 walking=MOTOR<=t<STOP;elapsed=max(0,min(t,STOP)-MOTOR);A.treadmill(c,675,620,elapsed,walking)
 if local<2.30:vale=A.person(c,490,ground=620,t=t,role='VALE',talk=F.energy(t,'VALE'),mood='confident',feet_override=[(475,620),(505,620)])
 elif local<5.14:vale=M.walk(c,local-2.3,'VALE',490,620,talk=F.energy(t,'VALE'),mood='confident')
 elif t<MOTOR:
  alpha=A.smooth((local-5.14)/.6) if local<9.24 else 1-A.smooth((local-9.24)/.5);alpha=max(0,min(1,alpha));hand=None
  if local<9.74:hand=(743+35*math.sin(math.pi*alpha)+62*alpha,A.lerp(518,293,alpha))
  vale=A.person(c,690,ground=620,t=t,role='VALE',talk=F.energy(t,'VALE'),mood='confident' if local<11.16 else 'surprised',hand=hand,gaze=3 if local>=10.9 else 0,feet_override=[(676,620),(705,620)])
 else:
  # Keep gait at the accepted natural cadence, never stretch it with the narration.
  reach=F.mark(F.BY[(8,4)],'Vale reaches');choice=None
  if reach<=t<DECISION:
   u=A.smooth((t-reach)/.7);choice=(A.lerp(770,590,u),A.lerp(456,422,u))
  elif DECISION<=t<STOP:
   u=A.smooth((t-DECISION)/max(.2,STOP-DECISION));choice=(A.lerp(590,794,u),A.lerp(422,403,u))
  elif STOP<=t<STOP+.5:choice=(794,403)
  elif STOP+.5<=t<STOP+.9:
   u=A.smooth((t-STOP-.5)/.4);choice=(A.lerp(794,770,u),A.lerp(403,456,u))
  if t<STOP:vale=M.belt(c,elapsed,'VALE',690,620,talk=F.energy(t,'VALE'),mood='worried' if t<F.BY[(6,7)]['start']+.5 else 'neutral',grip=A.smooth((t-GRIP)/.35),hand_target=choice)
  else:vale=M.stopped_belt(c,STOP-MOTOR,t-STOP,talk=F.energy(t,'VALE'),hand_target=choice)
 if local>=9.45:
  if local<10.814:mina=M.run(c,local-9.40,'MINA',1152,626,talk=F.energy(t,'MINA'))
  else:
   lh=None;rh=None
   if 11.16<=local<12.3:
    u=A.smooth((local-11.16)/.28)*(1-A.smooth((local-11.88)/.3));rh=(913+87*u,A.lerp(524,356,u))
   clip=vale.get('clip',(705,411));button=(794,403)
   # Actual full narration explicitly shows stop control BEFORE attaching the clip.
   if t>=cue('shows') and t<cue('attaches'):
    u=A.smooth((t-cue('shows'))/.45);lh=(A.lerp(807,button[0],u),A.lerp(524,button[1],u))
   elif cue('attaches')<=t<ATTACH+.15:
    u=A.smooth((t-cue('attaches'))/max(.2,ATTACH-cue('attaches')));lh=(A.lerp(button[0],clip[0],u),A.lerp(button[1],clip[1],u))
   elif ATTACH+.15<=t<MOTOR+.12:
    u=A.smooth((t-ATTACH-.15)/max(.2,MOTOR-ATTACH-.15));lh=(A.lerp(clip[0],button[0],u),A.lerp(clip[1],button[1],u))
   elif MOTOR+.12<=t<MOTOR+.5:
    u=A.smooth((t-MOTOR-.12)/.38);lh=(A.lerp(button[0],807,u),A.lerp(button[1],524,u))
   if t>=ATTACH:c.line([clip,(768,483),button],'#af5651',3);c.rect((clip[0]-5,clip[1]-5,clip[0]+5,clip[1]+5),'#c55d50',r=2,w=1)
   reply=F.BY[(6,6)]
   if reply['start']-.15<t<reply['end']+.55:
    u=A.smooth((t-reply['start']+.15)/.3)*(1-A.smooth((t-reply['end'])/.55));lh=(A.lerp(807,765,u),A.lerp(524,411,u))
   mina=A.person(c,860,ground=626,t=t,role='MINA',talk=F.energy(t,'MINA'),mood='worried' if t<ATTACH else 'confident',left=lh,hand=rh,gaze=-3)
 if extra:extra(c)
 return c
