"""Original local props, with explicit physical grip coordinates."""
from pathlib import Path
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from rig import transformed,line,poly,rotate,ip,ease
B=Path(__file__).resolve().parent;GUITAR=Image.open(B/'art/guitar.png').convert('RGBA');FONT=str(B/'fonts/ArchivoBlack.ttf')
def phone(im,center,angle=0,face=True,scroll=0):
 tile=Image.new('RGBA',(80,140));g=ImageDraw.Draw(tile);g.rounded_rectangle((6,3,73,136),12,fill='#283843',outline='#152631',width=4)
 if face:
  g.rounded_rectangle((12,14,67,123),5,fill='#b8d2d4')
  for y,c in [(25,'#d9af80'),(76,'#859f91'),(127,'#bb9990')]:
   yy=y-int(scroll*32)%50;g.rectangle((17,max(20,yy),62,min(119,yy+34)),fill=c) if 20<=yy<=119 else None
  g.line((28,20,51,20),fill='#3d5360',width=3)
 else:g.rounded_rectangle((15,13,36,42),5,fill='#63717a');g.ellipse((20,18,29,27),fill='#192c36')
 rr,pos=transformed(tile,center,[40,70],.5,angle);im.alpha_composite(rr,pos)
def bag(im,center,angle=0):
 tile=Image.new('RGBA',(110,120));g=ImageDraw.Draw(tile);g.rounded_rectangle((15,25,95,110),12,fill='#788b91',outline='#344a53',width=4);g.arc((31,5,80,45),180,360,fill='#344a53',width=7);g.line((25,50,85,50),fill='#9aabb0',width=3)
 rr,pos=transformed(tile,center,[55,65],.82,angle);im.alpha_composite(rr,pos)
def guitar(im,center,angle=0,scale=.62):
 rr,pos=transformed(GUITAR,center,[315,265],scale,angle);im.alpha_composite(rr,pos)
 return {side:np.asarray(center)+rotate(np.asarray(p)*scale,angle) for side,p in {'left':[-185,-157],'right':[0,-10]}.items()}
def stand(im,x=740,y=575):
 g=ImageDraw.Draw(im);line(g,[(x-13,y),(x,y-80),(x+17,y)],'#545b51',5);line(g,[(x-16,y-80),(x+18,y-80)],'#545b51',4)
def book(im,center,opening=1,turn=0):
 x,y=center;g=ImageDraw.Draw(im);w=55*opening
 poly(g,[(x,y-24),(x-w,y-36),(x-w-3,y+32),(x,y+40)],'#eee3c5','#6d5944',3)
 poly(g,[(x,y-24),(x+w,y-36),(x+w+3,y+32),(x,y+40)],'#f4e9cd','#6d5944',3)
 for dx in [-1,1]:
  for yy in [-10,3,16]:line(g,[(x+dx*8,y+yy),(x+dx*(w-9),y+yy-7)],'#b5aa8e',1)
 if 0<turn<1:
  xx=x+w*math.cos(math.pi*turn);poly(g,[(x,y-24),(xx,y-36-12*math.sin(math.pi*turn)),(xx,y+32),(x,y+40)],'#f8efd9','#b7a987',1)
def mug(im,center):
 x,y=center;g=ImageDraw.Draw(im);g.ellipse((x+9,y-12,x+31,y+13),outline='#715f4a',width=5);g.rounded_rectangle((x-18,y-23,x+17,y+22),5,fill='#eee2bd',outline='#715f4a',width=3);g.ellipse((x-17,y-27,x+16,y-17),fill='#a8936b',outline='#715f4a',width=2)
def kettle(im,center,angle=0):
 tile=Image.new('RGBA',(140,110));g=ImageDraw.Draw(tile);g.arc((70,21,126,88),260,100,fill='#4d5e5a',width=8);g.rounded_rectangle((26,24,96,90),18,fill='#8fa79c',outline='#4d5e5a',width=4);poly(g,[(31,40),(4,27),(12,69),(32,76)],'#8fa79c','#4d5e5a',3);g.ellipse((45,12,83,31),fill='#a7b9a5',outline='#4d5e5a',width=3)
 rr,pos=transformed(tile,center,[65,56],.78,angle);im.alpha_composite(rr,pos)
def plate(im,center,dirty=0):
 x,y=center;g=ImageDraw.Draw(im);g.ellipse((x-40,y-18,x+40,y+18),fill='#e7dfc4',outline='#6c7567',width=3);g.ellipse((x-28,y-11,x+28,y+11),outline='#b6b89c',width=2)
 for i in range(dirty):g.ellipse((x-20+i*13,y-4,x-13+i*13,y+1),fill='#9d7e55')
def pot(im,center):
 x,y=center;g=ImageDraw.Draw(im);g.rounded_rectangle((x-42,y-8,x+42,y+33),7,fill='#819a91',outline='#4f6962',width=3);g.ellipse((x-42,y-21,x+42,y+7),fill='#aeaa78',outline='#4f6962',width=3);line(g,[(x-53,y+3),(x-40,y+3)],'#4f6962',5);line(g,[(x+40,y+3),(x+53,y+3)],'#4f6962',5)
def paper(im,center,progress=0):
 x,y=center;g=ImageDraw.Draw(im);poly(g,[(x-70,y-20),(x+70,y-20),(x+85,y+26),(x-81,y+26)],'#f0e5c8','#917b5c',2)
 text='9:00 - PAY BILL';n=round(progress*len(text));g.text((x-54,y-11),text[:n],font=ImageFont.truetype(FONT,13),fill='#52695d')
def shoe(im,center,angle=0):
 tile=Image.new('RGBA',(100,58));g=ImageDraw.Draw(tile);g.rounded_rectangle((6,20,94,50),12,fill='#847457',outline='#424d42',width=3);poly(g,[(10,30),(10,7),(50,8),(65,30)],'#9c8a6b','#424d42',2);line(g,[(9,48),(94,48)],'#dfd4b6',5)
 for x in [29,39,49]:line(g,[(x,17),(x+11,24)],'#e1d5b4',2)
 rr,pos=transformed(tile,center,[50,30],.65,angle);im.alpha_composite(rr,pos)
