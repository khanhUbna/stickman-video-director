"""20-second cutout puppet film: independently planted feet, IK limbs, hand-bound cup.
The source artwork is composited as articulated pieces for video, never a sprite pan.
"""
from pathlib import Path
import math,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
P=Path(__file__).resolve().parent;D=P.parents[1]/'deliveries'/'silver-jacket-motion-test-v2'
W,H,FPS=1280,720,30;S=.36
SRC=Image.open(P/'assets/character-source.png').convert('RGBA')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=ImageFont.truetype(FONT,23); SMALL=ImageFont.truetype(FONT,15)
def clamp(t):return max(0,min(1,t))
def ease(t):t=clamp(t);return t*t*(3-2*t)
def lerp(a,b,u):return tuple(x+(y-x)*u for x,y in zip(a,b))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def dist(a,b):return math.hypot(b[0]-a[0],b[1]-a[1])
def ik(a,b,l1,l2,side=1):
 dx=b[0]-a[0];dy=b[1]-a[1];d=math.hypot(dx,dy)
 assert d<l1+l2+.5,('unreachable',d,l1+l2)
 d=max(.001,min(d,l1+l2-.01));q=(l1*l1-l2*l2+d*d)/(2*d);h=math.sqrt(max(0,l1*l1-q*q))
 return(a[0]+dx/d*q-dy/d*h*side,a[1]+dy/d*q+dx/d*h*side)
POLYS={
 'head':[(378,12),(636,12),(642,199),(619,292),(568,335),(564,358),(478,358),(468,325),(414,291),(385,228),(366,136)],
 'body':[(363,347),(466,312),(486,353),(550,354),(571,315),(675,351),(678,470),(657,648),(672,785),(350,782),(367,642),(344,470)],
 'ul':[(315,367),(369,391),(345,489),(302,602),(231,571),(270,465)],
 'fl':[(238,563),(307,595),(246,715),(203,795),(143,779),(175,695)],
 'hl':[(149,774),(207,791),(204,853),(197,942),(169,960),(108,927),(107,850),(122,809)],
 'ur':[(659,373),(708,370),(749,468),(786,576),(726,611),(682,507)],
 'fr':[(725,588),(790,564),(846,682),(882,775),(824,801),(773,715)],
 'hr':[(824,779),(880,775),(914,835),(921,921),(890,954),(835,946),(824,885),(809,825)],
 'tl':[(352,765),(514,776),(464,937),(434,1091),(340,1104),(335,1045)],
 'sl':[(340,1057),(437,1074),(408,1191),(405,1320),(413,1407),(294,1413),(304,1316),(319,1187)],
 'footl':[(295,1389),(410,1390),(401,1467),(362,1513),(242,1513),(242,1471)],
 'tr':[(510,773),(665,768),(683,1046),(689,1103),(583,1102),(556,955)],
 'sr':[(581,1072),(687,1066),(704,1200),(710,1317),(732,1414),(618,1414),(605,1310),(593,1199)],
 'footr':[(619,1393),(728,1394),(778,1467),(784,1512),(657,1512),(615,1476)]}
JOINTS={'ul':((333,408),(267,586)),'fl':((267,586),(174,779)),
 'ur':((691,408),(757,586)),'fr':((757,586),(850,779)),
 'tl':((427,802),(391,1081)),'sl':((391,1081),(354,1400)),
 'tr':((590,802),(633,1081)),'sr':((633,1081),(674,1400))}
ASSETS={}
for name,poly in POLYS.items():
 mask=Image.new('L',SRC.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
 # Remove only the white exterior caught by joint overlap margins.
 a=np.array(SRC);m=np.array(mask);white=np.min(a[:,:,:3],axis=2)
 m=(m.astype(float)*np.clip((253-white.astype(float))/10,0,1)).astype('uint8')
 layer=SRC.copy();layer.putalpha(Image.fromarray(m));box=layer.getbbox();layer=layer.crop(box)
 ASSETS[name]=(layer.resize((round(layer.width*S),round(layer.height*S)),Image.Resampling.LANCZOS),box)

def piece(out,name,srcanchor,dst,theta=0,custom=None):
 im,box=ASSETS[name]
 if custom is not None:im=custom
 a=((srcanchor[0]-box[0])*S,(srcanchor[1]-box[1])*S)
 c=(im.width/2,im.height/2);r=math.radians(theta)
 rot=im.rotate(-theta,Image.Resampling.BICUBIC,expand=True)
 off=(math.cos(r)*(a[0]-c[0])-math.sin(r)*(a[1]-c[1]),math.sin(r)*(a[0]-c[0])+math.cos(r)*(a[1]-c[1]))
 pos=(round(dst[0]-rot.width/2-off[0]),round(dst[1]-rot.height/2-off[1]))
 out.alpha_composite(rot,pos)

def bone(out,name,a,b):
 p,q=JOINTS[name];theta=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0])-math.atan2(q[1]-p[1],q[0]-p[0]))
 piece(out,name,p,a,theta)

# World-space footsteps: each planted foot keeps its own anchor until toe-off.
TRACKS=[{'initial':444,'moves':[(.45,.8,494),(1.35,1.7,544),(2.25,2.6,594),(3.15,3.5,644),(10.1,10.5,599),(11,11.4,554),(16.1,16.5,599),(17,17.4,644)]},
 {'initial':516,'moves':[(.9,1.25,566),(1.8,2.15,616),(2.7,3.05,666),(3.6,3.95,716),(10.55,10.95,671),(11.45,11.85,626),(16.55,16.95,671),(17.45,17.85,716)]}]
def foot(t,i):
 a=TRACKS[i]['initial']
 for start,end,b in TRACKS[i]['moves']:
  if t<start:return(a,613),0,True
  if t<end:
   u=clamp((t-start)/(end-start));x=a+(b-a)*ease(u)
   return(x,613-14*math.sin(math.pi*u)),(-6*math.sin(math.pi*u)),False
  a=b
 return(a,613),0,True

def root(t):
 if t<.25:return 480
 if t<3.95:return 480+200*ease((t-.25)/3.7)
 if t<10:return 680
 if t<11.85:return 680-90*ease((t-10)/1.85)
 if t<16:return 590
 if t<17.85:return 590+90*ease((t-16)/1.85)
 return 680

SPEECH=json.loads((P/'assets/speech.json').read_text())
import wave
with wave.open(str(P/'assets/demo-audio.wav')) as w:AUDIO=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
def mouth(t):
 if not any(c['start']<=t<c['end'] for c in SPEECH['cues']):return 0
 i=int(t*24000);q=AUDIO[i:i+700]
 return min(1,float(np.sqrt(np.mean(q*q)))*13) if len(q) else 0

def hands(t,x,shoulders):
 # The right hand reaches, grasps and lifts, then retains the exact cup transform.
 natural=(x+102,shoulders[1][1]+133)
 if t<4.2:r=natural
 elif t<5.1:r=lerp(natural,(799,385),ease((t-4.2)/.9))
 elif t<5.8:r=lerp((799,385),(x+100,333),ease((t-5.1)/.7))
 elif t<17.95:r=(x+100,333+2*math.sin(t*2))
 elif t<18.4:r=lerp((x+100,333),(799,385),ease((t-17.95)/.45))
 else:r=lerp((799,385),natural,ease((t-18.6)/.8))
 phase=math.sin(t*4.4)
 if 6.2<t<9.8 or 12.2<t<16.3:
  gate=ease((t-6.2)/.3)*(1-ease((t-9.4)/.4)) if t<10 else ease((t-12.2)/.3)*(1-ease((t-15.9)/.4))
  l=lerp((x-100,shoulders[0][1]+133),(x-145,307+12*phase),gate)
 else:l=(x-100+9*phase*(t<4),shoulders[0][1]+133)
 return l,r

def cup(out,center,grasp=False):
 x,y=center;d=ImageDraw.Draw(out)
 # Handle is behind cup; grip is deliberately shown on the near side.
 d.ellipse((x-40,y+9,x-10,y+39),fill='#f9faf5',outline='#25627c',width=4)
 d.rounded_rectangle((x-23,y,x+23,y+49),radius=7,fill='#3b9eb6',outline='#194c66',width=3)
 d.ellipse((x-23,y-5,x+23,y+7),fill='#d9eef0',outline='#194c66',width=2)
 d.ellipse((x-17,y-1,x+17,y+4),fill='#67402b')
 d.line((x+14,y+12,x+14,y+35),fill='#8ed6db',width=3)
 if grasp:
  d.rounded_rectangle((x-36,y+15,x-20,y+34),radius=6,fill='#edaa78',outline='#5a392c',width=2)
  for k in range(3):d.line((x-34,y+20+k*4,x-25,y+21+k*4),fill='#ba7b56',width=1)

def background():
 im=Image.new('RGBA',(W,H),'#eee8dc');d=ImageDraw.Draw(im)
 d.rectangle((0,570,W,H),fill='#cbb69b');d.line((0,570,W,570),fill='#b49b80',width=3)
 d.rounded_rectangle((80,75,320,310),radius=5,fill='#baac95')
 d.rectangle((90,85,310,300),fill='#d5edf1');d.line((200,85,200,300),fill='#fffaf0',width=8);d.line((90,193,310,193),fill='#fffaf0',width=8)
 d.ellipse((250,103,282,135),fill='#fff4c5');d.polygon([(90,265),(170,212),(240,268),(310,232),(310,300),(90,300)],fill='#97b59c')
 d.rounded_rectangle((965,90,1165,230),radius=8,fill='#f8f3e9',outline='#b8a58d',width=4)
 d.text((997,120),'TAKE A',font=F,fill='#746855');d.text((1000,157),'BREAK',font=F,fill='#746855')
 d.line((1120,563,1120,400),fill='#486a4b',width=7)
 for dx,dy in [(-45,-20),(35,-50),(-30,-80),(30,-115)]:d.ellipse((1120+dx-27,470+dy-20,1120+dx+27,470+dy+20),fill='#6c9467')
 d.polygon([(1082,522),(1159,522),(1145,575),(1094,575)],fill='#b37c5c')
 d.text((44,31),'2D CHARACTER · MOTION TEST V2',font=SMALL,fill='#776f65')
 d.text((44,54),'Original animation · local demo voice',font=SMALL,fill='#776f65')
 return im
from mesh import Skin
SKIN=Skin(P/'assets/character-source.png')
BG=background();log=[]
def frame(t,record=False):
 im=BG.copy();d=ImageDraw.Draw(im);x=root(t)
 feet=[foot(t,i) for i in range(2)]
 moving=any(not f[2] for f in feet)
 # Squash/bob from step phase while respecting reach of both fixed-length legs.
 hy=392+2*math.sin(t*math.pi*4)*(moving)
 hips=[(x-29,hy),(x+30,hy)]
 for i,(ankle,_,_) in enumerate(feet):
  l1=dist(*JOINTS['tl' if i==0 else 'tr'])*S;l2=dist(*JOINTS['sl' if i==0 else 'sr'])*S
  dx=ankle[0]-hips[i][0];hy=max(hy,ankle[1]-math.sqrt(max(1,(l1+l2-1)**2-dx*dx)))
 hips=[(x-29,hy),(x+30,hy)]
 d.ellipse((x-100,638,x+100,655),fill='#b5a18b')
 legs=[]
 for i,(ankle,angle,planted) in enumerate(feet):
  upper='tl' if i==0 else 'tr';lower='sl' if i==0 else 'sr'
  knee=ik(hips[i],ankle,dist(*JOINTS[upper])*S,dist(*JOINTS[lower])*S,side=1 if i==0 else -1)
  legs.append((hips[i],knee,ankle,angle))
 shoulders=[(x+(333-512)*S,hy+(408-802)*S),(x+(691-512)*S,hy+(408-802)*S)]
 lh,rh=hands(t,x,shoulders)
 arms=[]
 for i,(sh,hand) in enumerate(zip(shoulders,[lh,rh])):
  up='ul' if i==0 else 'ur';lo='fl' if i==0 else 'fr'
  elbow=ik(sh,hand,dist(*JOINTS[up])*S,dist(*JOINTS[lo])*S,side=-1 if i==0 else 1)
  arms.append((sh,elbow,hand))
 vertices=SKIN.deform(x,hy,arms,legs)
 actor,offset=SKIN.render(vertices,hide_right_hand=5.08<t<18.45)
 im.alpha_composite(actor,offset)
 if record:
  joints=[*shoulders,*[a[1] for a in arms],*hips,*[leg[1] for leg in legs],*[leg[2] for leg in legs]]
  alpha=np.array(actor.getchannel('A'))
  from mesh import cv2
  _,_,stats,_=cv2.connectedComponentsWithStats((alpha>127).astype('uint8'),8)
  detached_components=int(sum(v>50 for v in stats[1:,cv2.CC_STAT_AREA]))-1
  coverage=[]
  for j in joints:
   jx,jy=round(j[0]-offset[0]),round(j[1]-offset[1])
   region=alpha[max(0,jy-2):jy+3,max(0,jx-2):jx+3]
   coverage.append(float(np.mean(region>127)))
 # Head pivots at the neck, with RMS-driven mouth poses.
 head,box=ASSETS['head'];head=head.copy();md=ImageDraw.Draw(head)
 amp=mouth(t)
 for bt in (3.9,11.7,17.7):
  if bt<t<bt+.13:
   for ex in (474,559):
    cx=(ex-box[0])*S;cy=(175-box[1])*S
    md.ellipse((cx-7,cy-2,cx+7,cy+3),fill='#dfa06d');md.line((cx-6,cy+1,cx+6,cy+1),fill='#5a3e30',width=1)
 if amp>.06:
  def b(coords):return tuple(round((q-(box[0] if i%2==0 else box[1]))*S) for i,q in enumerate(coords))
  md.ellipse(b((483,230,578,266)),fill='#eca574')
  h=7+amp*27;md.ellipse(b((500,244-h/2,563,244+h/2)),fill='#4d261f')
  md.rounded_rectangle(b((505,243-h/2,558,248-h/2)),radius=1,fill='#fff4de')
 neck=(x,hy+(330-802)*S)
 nod=1.7*math.sin(t*2.1)+(-4*math.sin((t-19)*math.pi) if t>19 else 0)
 piece(im,'head',(512,330),neck,nod,head)
 # Background table top and legs are drawn before cup, in front of the actor's far reach.
 d=ImageDraw.Draw(im)
 d.polygon([(809,414),(1011,414),(998,433),(796,433)],fill='#986c4b',outline='#725139')
 d.rectangle((814,433,829,626),fill='#826249');d.rectangle((981,433,996,626),fill='#826249')
 held=5.1<=t<18.4
 cc=(rh[0]+26,rh[1]-25) if held else (825,360)
 cup(im,cc,grasp=held)
 # Caption is split by clause, remains below the visible feet.
 cap=''
 if 6.2<=t<8.0:cap='Now, the important part:'
 elif 8<=t<SPEECH['cues'][0]['end']+.15:cap='keep the coffee in the cup.'
 elif 12.2<=t<13.65:cap='Walking is easy.'
 elif 13.65<=t<15.25:cap='Walking with coffee?'
 elif 15.25<=t<SPEECH['cues'][1]['end']+.15:cap='That takes confidence.'
 if cap:
  width=d.textlength(cap,font=F);d.rounded_rectangle(((W-width)/2-18,668,(W+width)/2+18,705),radius=9,fill='#ffffffed')
  d.text(((W-width)/2,672),cap,font=F,fill='#292a2d')
 if record:log.append(dict(t=t,root=x,hip_y=hy,feet=[dict(x=f[0][0],y=f[0][1],planted=f[2]) for f in feet],hand=rh,cup=cc,held=held,joint_core_coverage=coverage,detached_large_components=detached_components,joints=joints))
 return im.convert('RGB')

def main():
 D.mkdir(parents=True,exist_ok=True);(P/'.cache').mkdir(exist_ok=True)
 if '--sheets' in sys.argv:
  times=[0,1,2,3.8,4.7,5.5,6.9,9,10.7,12.7,14.5,16.6,18.2,18.8,19.7]
  sheet=Image.new('RGB',(1280,3*260),'white');dr=ImageDraw.Draw(sheet)
  for i,t in enumerate(times):
   im=frame(t,True);im.thumbnail((256,240));sheet.paste(im,((i%5)*256,(i//5)*260));dr.text(((i%5)*256+5,(i//5)*260+150),f'{t:.1f}s',font=SMALL,fill='black')
  sheet.save(P/'reports/contact-sheet.jpg');print('sheet ready');return
 out=D/'silver-jacket-coffee-test-20s-v2.mp4'
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(P/'assets/demo-audio.wav'),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','20','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(FPS*20):
  im=frame(n/FPS,True);proc.stdin.write(im.tobytes())
  if n%150==0:print(f'rendered {n}/600',flush=True)
 proc.stdin.close();assert proc.wait()==0
 (P/'reports/contact-log.json').write_text(json.dumps(log,indent=2))
 print(out)
if __name__=='__main__':main()
