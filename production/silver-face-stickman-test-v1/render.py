"""Original 20s procedural stickman + retained portrait face. No paid services.
Connected vector limbs replace ALL the rejected leather/pants/body warping.
"""
from pathlib import Path
import math,json,subprocess,sys,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;D=P.parents[1]/'deliveries/silver-face-stickman-test-v1'
W,H,FPS=1280,720,30;S=.36
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=ImageFont.truetype(FONT,23);SMALL=ImageFont.truetype(FONT,15)
INK='#24303a';SKIN='#edb18b';OUTLINE='#654430'
def clamp(t):return max(0.,min(1.,t))
def ease(t):t=clamp(t);return t*t*(3-2*t)
def lerp(a,b,u):return tuple(x+(y-x)*u for x,y in zip(a,b))
def dist(a,b):return math.hypot(b[0]-a[0],b[1]-a[1])
def ik(a,b,l1,l2,side):
 dx=b[0]-a[0];dy=b[1]-a[1];d=math.hypot(dx,dy)
 assert d<l1+l2+.001,(a,b,d,l1+l2)
 d=max(.001,min(d,l1+l2-.0001));q=(l1*l1-l2*l2+d*d)/(2*d);h=math.sqrt(max(0,l1*l1-q*q))
 return(a[0]+dx/d*q-dy/d*h*side,a[1]+dy/d*q+dx/d*h*side)
def hermite(t,keys):
 if t<=keys[0][0]:return keys[0][1]
 if t>=keys[-1][0]:return keys[-1][1]
 for a,b in zip(keys,keys[1:]):
  if a[0]<=t<b[0]:
   h=b[0]-a[0];u=(t-a[0])/h
   return (2*u**3-3*u*u+1)*a[1]+(u**3-2*u*u+u)*h*a[2]+(-2*u**3+3*u*u)*b[1]+(u**3-u*u)*h*b[2]
TRACKS=[{'initial':400,'moves':[(.45,.8,480),(1.35,1.7,560),(2.25,2.6,640),(3.15,3.5,675),(10.1,10.5,620),(11,11.4,595),(16.1,16.5,640),(17,17.4,675)]},
 {'initial':430,'moves':[(.9,1.25,520),(1.8,2.15,600),(2.7,3.05,680),(3.6,3.95,705),(10.55,10.95,590),(11.45,11.85,615),(16.55,16.95,680),(17.45,17.85,705)]}]
ROOT=[(0,415,0),(.30,415,0),(.8,445,80),(1.25,485,89),(1.7,525,89),(2.15,565,89),(2.6,605,89),(3.05,648,70),(3.5,680,30),(3.95,690,0),
 (10,690,0),(10.5,660,-80),(10.95,624,-70),(11.4,605,-20),(11.85,605,0),(16,605,0),(16.5,632,75),(16.95,666,65),(17.4,685,25),(17.85,690,0),(20,690,0)]
def foot(t,i):
 old=TRACKS[i]['initial']
 for start,end,new in TRACKS[i]['moves']:
  if t<start:return(old,613),0.,True
  if t<end:
   u=clamp((t-start)/(end-start));a=old+(new-old)*ease(u)
   lift=(18 if abs(new-old)>35 else 11)*math.sin(math.pi*u)
   return(a,613-lift),-9*math.sin(math.pi*u),False
  old=new
 return(old,613),0.,True
SPEECH=json.loads((P/'assets/speech.json').read_text())
with wave.open(str(P/'assets/demo-audio.wav')) as w:AUDIO=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
def mouth(t):
 if not any(c['start']<=t<c['end'] for c in SPEECH['cues']):return 0.
 q=AUDIO[int(t*24000):int(t*24000)+700]
 return min(1,float(np.sqrt(np.mean(q*q)))*11) if len(q) else 0.
from cartoon_face import draw as draw_cartoon_face
def face(im,t,neck):draw_cartoon_face(im,t,neck,mouth(t))
def stroke(d,points,width,color=INK):
 d.line(points,fill=color,width=width,joint='curve')
 r=width/2
 for x,y in points:d.ellipse((x-r,y-r,x+r,y+r),fill=color)
def open_hand(d,wrist,elbow):
 # Draw palm and fingers in a wrist-local basis; orientation follows the forearm.
 dx=wrist[0]-elbow[0];dy=wrist[1]-elbow[1];ll=math.hypot(dx,dy);u=(dx/ll,dy/ll);v=(-u[1],u[0])
 def p(a,b):return(wrist[0]+u[0]*a+v[0]*b,wrist[1]+u[1]*a+v[1]*b)
 palm=[p(-3,-6),p(12,-8),p(18,-5),p(18,6),p(11,9),p(-3,6)]
 d.polygon(palm,fill=SKIN,outline=OUTLINE)
 for k,bb in enumerate([-5,-1,3,7]):
  finger=[p(10,bb),p(22+(2-abs(k-1.5))*2,bb),p(27+(2-abs(k-1.5))*2,bb+2)]
  stroke(d,finger,4,OUTLINE);stroke(d,finger,2,SKIN)
 stroke(d,[p(5,-6),p(12,-13),p(21,-13)],5,OUTLINE);stroke(d,[p(5,-6),p(12,-13),p(21,-13)],3,SKIN)
def cup(d,center,held):
 x,y=center
 d.ellipse((x-40,y+9,x-10,y+39),fill='#f9faf5',outline='#25627c',width=4)
 d.rounded_rectangle((x-23,y,x+23,y+49),radius=7,fill='#3b9eb6',outline='#194c66',width=3)
 d.ellipse((x-23,y-5,x+23,y+7),fill='#d9eef0',outline='#194c66',width=2)
 d.ellipse((x-17,y-1,x+17,y+4),fill='#67402b');d.line((x+14,y+12,x+14,y+35),fill='#8ed6db',width=3)
 if held:
  d.rounded_rectangle((x-36,y+15,x-20,y+34),radius=6,fill=SKIN,outline=OUTLINE,width=2)
  for k in range(3):d.line((x-34,y+20+k*4,x-25,y+21+k*4),fill='#b27a54',width=1)
def background():
 im=Image.new('RGBA',(W,H),'#eee8dc');d=ImageDraw.Draw(im)
 d.rectangle((0,570,W,H),fill='#cbb69b');d.line((0,570,W,570),fill='#b49b80',width=3)
 d.rounded_rectangle((80,75,320,310),radius=5,fill='#baac95');d.rectangle((90,85,310,300),fill='#d5edf1')
 d.line((200,85,200,300),fill='#fffaf0',width=8);d.line((90,193,310,193),fill='#fffaf0',width=8)
 d.ellipse((250,103,282,135),fill='#fff4c5');d.polygon([(90,265),(170,212),(240,268),(310,232),(310,300),(90,300)],fill='#97b59c')
 d.rounded_rectangle((965,90,1165,230),radius=8,fill='#f8f3e9',outline='#b8a58d',width=4)
 d.text((997,120),'TAKE A',font=F,fill='#746855');d.text((1000,157),'BREAK',font=F,fill='#746855')
 d.line((1120,563,1120,400),fill='#486a4b',width=7)
 for dx,dy in [(-45,-20),(35,-50),(-30,-80),(30,-115)]:d.ellipse((1120+dx-27,470+dy-20,1120+dx+27,470+dy+20),fill='#6c9467')
 d.polygon([(1082,522),(1159,522),(1145,575),(1094,575)],fill='#b37c5c')
 d.text((44,31),'CARTOON STICKMAN · 20 SECOND TEST',font=SMALL,fill='#776f65')
 d.text((44,54),'Original animation · reused demo voice',font=SMALL,fill='#776f65')
 return im
BG=background();LOG=[]
def pose(t):
 x=hermite(t,ROOT);feet=[foot(t,i) for i in range(2)]
 moving=any(not f[2] for f in feet);direction=-1 if 10<=t<16 else 1
 activity=max(ease((t-a)/.2)*(1-ease((t-b)/.2)) for a,b in [(0.35,3.8),(10,11.65),(16,17.65)])
 hy=402+6*activity+1.7*math.sin(t*math.pi*4)*activity
 # Pelvis respects both fixed limb lengths while feet stay independently grounded.
 for i,(ankle,_,_) in enumerate(feet):
  hx=x+(-5 if i==0 else 5);span=ankle[0]-hx
  hy=max(hy,ankle[1]-math.sqrt(max(1,211.7**2-span**2)))
 hips=[(x-5,hy),(x+5,hy)]
 knees=[ik(hips[i],feet[i][0],100,113,-direction) for i in range(2)]
 lean=direction*3.5*activity
 shoulders=[(x-21+lean,hy-139),(x+22+lean,hy-139)]
 phase=math.sin(t*math.pi/0.9)
 natural=(x+76,shoulders[1][1]+126)
 if t<4.2:rh=(natural[0]+8*phase*activity,natural[1])
 elif t<5.1:rh=lerp(natural,(799,385),ease((t-4.2)/.9))
 elif t<5.8:rh=lerp((799,385),(x+100,333),ease((t-5.1)/.7))
 elif t<17.95:rh=(x+100,333+1.3*math.sin(t*2))
 elif t<18.4:rh=lerp((x+100,333),(799,385),ease((t-17.95)/.45))
 else:rh=lerp((799,385),natural,ease((t-18.6)/.8))
 lh=(x-60-10*phase*activity,shoulders[0][1]+128)
 for a,b in [(6.2,9.8),(12.2,16.3)]:
  if a<t<b:lh=lerp(lh,(x-119,319+7*math.sin(t*2.6)),ease((t-a)/.35)*(1-ease((t-(b-.45))/.45)))
 hands=[lh,rh];elbows=[ik(shoulders[i],hands[i],84,88,-1 if i==0 else 1) for i in range(2)]
 return dict(t=t,x=x,hip_y=hy,hips=hips,knees=knees,feet=feet,shoulders=shoulders,hands=hands,elbows=elbows,lean=lean,held=5.1<=t<18.4)
def frame(t,record=False):
 st=pose(t);x=st['x'];hy=st['hip_y'];lean=st['lean'];im=BG.copy();d=ImageDraw.Draw(im)
 d.ellipse((x-73,628,x+75,645),fill='#b5a18b')
 joints=[]
 for i in range(2):
  hip=st['hips'][i];knee=st['knees'][i];ankle,ang,planted=st['feet'][i]
  stroke(d,[hip,knee,ankle],7 if i==0 else 8,'#40505b' if i==0 else INK)
  ax,ay=ankle
  d.rounded_rectangle((ax-12,ay+1,ax+20,ay+12),radius=5,fill='#28323b')
  d.line((ax-10,ay+11,ax+18,ay+11),fill='#66737b',width=2)
 # Far arm goes behind the torso; no separately rotated sleeve image exists.
 for i in range(2):
  stroke(d,[st['shoulders'][i],st['elbows'][i],st['hands'][i]],7 if i==0 else 8,'#40505b' if i==0 else INK)
  if i==0 or not st['held']:open_hand(d,st['hands'][i],st['elbows'][i])
 d.rounded_rectangle((x-7+lean,hy-170,x+7+lean,hy-139),radius=5,fill=SKIN)
 # Plain narrow jacket-shaped torso, with no long sleeves/pants to deform.
 sy=hy-141;lean=st['lean']
 body=[(x-24+lean,sy),(x-11+lean,sy-9),(x+12+lean,sy-9),(x+25+lean,sy),(x+22,hy-4),(x-22,hy-4)]
 d.polygon(body,fill='#26292d',outline='#131c23');d.line((x+lean,sy+6,x,hy-7),fill='#bdb5a4',width=2)
 d.line((x-11+lean,sy-9,x+lean,sy+9,x+12+lean,sy-9),fill='#707275',width=2)
 d.line((x-17,hy-38,x-7,hy-38),fill='#777d7e',width=2);d.line((x+7,hy-38,x+17,hy-38),fill='#777d7e',width=2)
 face(im,t,(x+lean,hy-150))
 d=ImageDraw.Draw(im)
 d.polygon([(809,409),(1011,409),(998,428),(796,428)],fill='#986c4b',outline='#725139')
 d.rectangle((814,428,829,626),fill='#826249');d.rectangle((981,428,996,626),fill='#826249')
 rh=st['hands'][1];cc=(rh[0]+26,rh[1]-25) if st['held'] else (825,360)
 cup(d,cc,st['held'])
 cap=''
 if 6.2<=t<8:cap='Now, the important part:'
 elif 8<=t<9.571:cap='keep the coffee in the cup.'
 elif 12.2<=t<13.65:cap='Walking is easy.'
 elif 13.65<=t<15.25:cap='Walking with coffee?'
 elif 15.25<=t<16.19:cap='That takes confidence.'
 if cap:
  ww=d.textlength(cap,font=F);d.rounded_rectangle(((W-ww)/2-18,668,(W+ww)/2+18,705),radius=9,fill='#ffffff')
  d.text(((W-ww)/2,672),cap,font=F,fill='#292a2d')
 if record:
  lengths=[]
  for i in range(2):lengths += [dist(st['hips'][i],st['knees'][i]),dist(st['knees'][i],st['feet'][i][0]),dist(st['shoulders'][i],st['elbows'][i]),dist(st['elbows'][i],st['hands'][i])]
  st.update(cup=cc,bone_lengths=lengths);LOG.append(st)
 return im.convert('RGB')
def main():
 D.mkdir(exist_ok=True,parents=True)
 if '--sheets' in sys.argv:
  times=[0,1.5,3,4.8,5.7,7,10.8,14,18.3,19.7]
  sheet=Image.new('RGB',(1280,580),'white');d=ImageDraw.Draw(sheet)
  for i,t in enumerate(times):
   im=frame(t);im.thumbnail((256,144));sheet.paste(im,((i%5)*256,(i//5)*290));d.text(((i%5)*256+8,(i//5)*290+150),f'{t:.1f}s',font=SMALL,fill='black')
  sheet.save(P/'reports/contact-sheet.jpg');return
 video=D/'cartoon-stickman-coffee-20s.mp4'
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(P/'assets/demo-audio.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','20','-movflags','+faststart',str(video)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(600):
  proc.stdin.write(frame(n/FPS,True).tobytes())
  if n%150==0:print(f'rendered {n}/600',flush=True)
 proc.stdin.close();assert proc.wait()==0
 (P/'reports/motion-log.json').write_text(json.dumps(LOG,indent=2));print(video)
if __name__=='__main__':main()
