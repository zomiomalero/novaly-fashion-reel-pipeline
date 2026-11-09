#!/usr/bin/env python3
"""Generate original reusable technical fashion surface studies and layout plates.

These are PROCEDURAL texture/lighting studies, never claims of photographed fabric
or of any specific product's true color. No copyrighted reference pixels are used.
"""
from __future__ import annotations
import csv
import hashlib
import math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
MATERIALS=('cotton','linen','denim','twill','rib-knit','satin')
COLORS={'ivory':'#E5DAC9','ink':'#20232B','burgundy':'#713744','olive':'#626B4D',
        'navy':'#34465D','camel':'#BB9874','rose':'#C68F99','denim-blue':'#648DB4'}
FNT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def f(size,bold=False):
    try:return ImageFont.truetype(BOLD if bold else FNT,size)
    except OSError:return ImageFont.load_default()

def hexrgb(s):return np.array([int(s[i:i+2],16) for i in (1,3,5)],dtype=np.float32)

def make_texture(name,color,seed,size=1024):
    rng=np.random.default_rng(seed)
    yy,xx=np.mgrid[:size,:size]
    x=xx.astype(np.float32); y=yy.astype(np.float32)
    rx=(x/size);ry=y/size
    # Studio soft key, broad fold, contact shadow and textile microstructure.
    broad=0.82+0.18*np.cos((rx-.32)*np.pi*.76)-.13*(ry-.08)
    fold=(.10*np.sin(2*np.pi*(rx*2.5+0.018*np.sin(ry*7)))
          +.045*np.sin(2*np.pi*(rx*5.1+ry*.2)))
    falloff=-.09*np.maximum(0,1.0-rx/.20)**2-.08*np.maximum(0,(rx-.86)/.14)**2
    grain=rng.normal(0,1,(size,size)).astype(np.float32)
    if name=='cotton':
        weave=.018*np.sin(x*1.55)*np.sin(y*1.50)+.014*np.sin(x*3.1)+.018*grain
        bump=.009*np.cos(x*.28+y*.13)
    elif name=='linen':
        weave=.038*np.sin(x*.78+.3*np.sin(y*.04))+.035*np.sin(y*.81+.24*np.sin(x*.05))+.019*grain
        bump=.01*np.cos(x*.6+y*.08)
    elif name=='denim':
        weave=.045*np.cos((x+y*1.35)*1.1)+.017*np.cos(y*.34)+.033*grain
        bump=.018*np.sin((x-y*.3)*.17)
    elif name=='twill':
        weave=.04*np.sin((x+y*.8)*1.5)+.018*np.sin(y*.22)+.014*grain
        bump=.008*np.cos(x*.47)
    elif name=='rib-knit':
        weave=.063*np.sin(x*.39)+.026*np.cos(x*.83+y*.04)+.027*grain
        bump=.022*np.cos((x-2*y)*.04)
    else:
        # Satin: almost no coarse texture; strong broad specular sheen along silk folds.
        weave=.008*np.sin(x*1.12+y*.12)+.009*grain
        bump=.14*np.exp(-((rx-.51-.065*np.sin(ry*5))/.075)**2)
    lum=np.clip(broad+fold+weave+falloff+bump,.45,1.16)
    base=hexrgb(color)[None,None,:]
    # Preserve shadows with realistic lifted floor rather than simply black-multiplying.
    rgb=base*lum[:,:,None]+np.clip(lum[:,:,None]-1.,0,None)*12
    # Slight left key warmth, right side cool reflected studio light.
    rgb[:,:,0]*=1+.023*(1-rx)
    rgb[:,:,2]*=1+.03*rx
    rgb=np.clip(rgb,0,255).astype(np.uint8)
    im=Image.fromarray(rgb,'RGB')
    return im

def rect(d,xy,fill,outline=None,width=1,radius=0):
    if radius:d.rounded_rectangle(xy,radius,fill=fill,outline=outline,width=width)
    else:d.rectangle(xy,fill=fill,outline=outline,width=width)

def line(d,xy,color='#E4D9CF',width=3):d.line(xy,fill=color,width=width,joint='curve')

def plate(out:Path,title:str,sub:str,which:int):
    W,H=1080,1920
    im=Image.new('RGB',(W,H),'#131925');d=ImageDraw.Draw(im)
    # Original illustrative editorial set. All geometry drawn procedurally, no real models.
    for y in range(H):
        t=y/H
        c=(int(26+t*7),int(34+t*10),int(43+t*8))
        d.line((0,y,W,y),fill=c)
    d.text((78,85),title.upper(),font=f(53,True),fill='#F5E8D8')
    d.text((80,157),sub,font=f(25),fill='#AFC2C2')
    rect(d,(80,270,1000,1670),'#E2DACF',radius=34)
    # Curtain stripes and floor border
    for x in range(105,1000,35):
        line(d,[(x,300),(x+int(12*math.sin(x)),1410)],'#D3C8BB',6)
        line(d,[(x+8,300),(x+8,1410)],'#F1EBE2',6)
    rect(d,(90,1390,989,1650),'#C6B8AB')
    line(d,[(90,1390),(989,1390)],'#B2A79C',5)
    # Two neutral *diagram* figures (not photorealism, not any real people).
    def actor(cx,scale,hue):
        top=482; feet=1400
        k=scale
        head=(cx,top+int(125*k))
        r=int(65*k)
        d.ellipse((head[0]-r,head[1]-r,head[0]+r,head[1]+r),fill=hue)
        d.rounded_rectangle((cx-int(79*k),top+int(190*k),cx+int(79*k),top+int(515*k)),radius=24,fill=hue)
        line(d,[(cx-int(65*k),top+int(515*k)),(cx-int(62*k),feet)],hue,int(43*k))
        line(d,[(cx+int(65*k),top+int(515*k)),(cx+int(62*k),feet)],hue,int(43*k))
        line(d,[(cx-int(75*k),top+int(250*k)),(cx-int(142*k),top+int(570*k))],hue,int(33*k))
        line(d,[(cx+int(75*k),top+int(250*k)),(cx+int(133*k),top+int(570*k))],hue,int(33*k))
    actor(359,.93,'#5B4855');actor(695,1.03,'#364B58')
    # minimal optional prop
    rect(d,(873,1020,969,1400),'#9E7465',radius=9)
    d.ellipse((897,955,949,1055),fill='#6D5852')
    if which==0: # crop guides
        for y in (410,730,1130,1400):line(d,[(102,y),(985,y)],'#3D8F96',3)
        d.text((112,360),'HEADROOM',font=f(23,True),fill='#22626C')
        d.text((117,1314),'SHOES FULLY VISIBLE',font=f(24,True),fill='#22626C')
        for x in (150,540,930):line(d,[(x,430),(x,1440)],'#3D8F96',2)
    elif which==1: # safe areas
        rect(d,(150,480,930,1280),None,outline='#3B8C8C',width=6,radius=20)
        rect(d,(150,500,930,652),'#103F46',radius=15)
        d.text((180,545),'COLOR PALETTE  •  LOOK 03',font=f(31,True),fill='white')
        rect(d,(728,1150,935,1590),'#CA6556',radius=20)
        d.text((735,1175),'SOCIAL',font=f(22,True),fill='white')
        d.text((735,1215),'UI SAFE',font=f(22,True),fill='white')
    elif which==2: # anchor boxes
        for xy in [(95,380,155,1120),(418,286,663,410),(915,400,980,890)]:
            rect(d,xy,None,outline='#45AFA9',width=6)
        d.text((175,405),'BACKGROUND-ONLY AREAS',font=f(26,True),fill='#103B43')
    elif which==3: # wardrobe consistency
        for x in (300,700):
            d.ellipse((x-100,1075,x+100,1185),outline='#1AA4A4',width=8)
        d.text((140,300),'FIXED FACES, NEW GARMENTS',font=f(31,True),fill='#3C454F')
    elif which==4: # timing cuts
        coords=[(140,1060),(430,1060),(735,1060)]
        for j,(x,y) in enumerate(coords):
            rect(d,(x,y,x+200,y+150),['#5D6654','#704D55','#5D7185'][j],radius=17)
            d.text((x+24,y+52),f'LOOK {j+1}',font=f(30,True),fill='white')
        line(d,[(125,1030),(965,1030)],'#165A64',7)
    elif which==5:
        rect(d,(180,350,820,500),'#1E6464',radius=18)
        d.text((215,385),'VOICE FIRST, LABELS SECOND',font=f(28,True),fill='white')
        for j,t in enumerate(('Narration →','Shot timing →','Audio ducking →','Mastering')):
            d.text((195,700+j*125),t,font=f(36,True),fill='#1B3F48')
    elif which==6:
        for j,text in enumerate(('CAST LOCK','STUDIO MASTER','LOOK FIRST-FRAME','VIDEO CLIP','HUMAN QC','FINAL EDIT')):
            x=145;y=320+j*190
            rect(d,(x,y,930,y+135),'#24565D' if j%2==0 else '#3A4659',radius=22)
            d.text((x+37,y+38),f'{j+1:02}  {text}',font=f(35,True),fill='#F5EBDE')
    elif which==7:
        d.text((136,320),'PRODUCTION QUALITY GATES',font=f(35,True),fill='#1D5561')
        for j,t in enumerate(('Audio peaks','Model continuity','Hands and feet','Garment accuracy','Text safe area','Rights review')):
            yy=640+j*125
            rect(d,(160,yy,213,yy+53),None,outline='#23636D',width=5,radius=4)
            d.text((244,yy+8),t,font=f(29,True),fill='#25454B')
    d.text((81,1740),'NOVALY  /  ORIGINAL TECHNICAL PLATE',font=f(28,True),fill='#F3E4D1')
    d.text((81,1790),'Diagram only. Not a generated person or photo.',font=f(22),fill='#A9BABD')
    im.save(out,optimize=True)


def main():
    d=ROOT/'assets/original-material-studies';d.mkdir(parents=True,exist_ok=True)
    rows=[]
    for m in MATERIALS:
        for label,col in COLORS.items():
            seed=int(hashlib.sha256((m+label).encode()).hexdigest()[:8],16)
            dest=d/f'{m}_{label}.jpg'
            im=make_texture(m,col,seed)
            im.save(dest,'JPEG',quality=90,subsampling=0,optimize=True)
            rows.append([dest.name,m,label,col,seed,1024,1024])
    with (d/'manifest.csv').open('w',newline='') as f2:
        writer=csv.writer(f2)
        writer.writerow(['filename','surface_family','palette_name','nominal_hex','seed','width','height'])
        writer.writerows(rows)
    (d/'README.md').write_text('# Original procedural material-study library\n\n'+
        '48 completely original, reproducible 1024x1024 JPEG surface studies (six textile families × eight styling colors). '+
        'Use for palette prototyping, clothing surface briefing, text contrast studies, and procedural shader testing. '+
        '**These are NOT photographed fabric, not product images, and NOT evidence of exact real textile color.** '+
        'Nominal colors are study starting points; lighting and texture alter the sampled pixel values. '+
        'Source generation: `scripts/build_original_visual_library.py` using NumPy and Pillow with hashed deterministic seeds.\n',encoding='utf-8')
    names=[('FULL-BODY FRAMING','Keep heads, hands, trousers and shoes in the master',0),
           ('SOCIAL SAFE ZONES','Protect model faces and platform UI areas',1),
           ('STUDIO ANCHORS','Use stable environment features for continuity review',2),
           ('IDENTITY AND OUTFITS','One original cast identity across distinct completed outfits',3),
           ('BEAT SCHEDULING','Illustrate one clear styling lesson per short beat',4),
           ('AUDIO TIMING','Words and cuts must agree with the finished narration',5),
           ('GENERATION HANDOFF','Lock references before generating individual clips',6),
           ('QUALITY ASSURANCE','Mechanical QA plus human sign-off',7)]
    plates=ROOT/'assets/technical-plates';plates.mkdir(exist_ok=True)
    for i,(title,sub,which) in enumerate(names,1):plate(plates/f'plate_{i:02}.png',title,sub,which)
    (plates/'README.md').write_text('# Original studio-layout technical plates\n\nEight fully original **diagrams** illustrating frame geometry, safe areas, fixed set anchors, wardrobe continuity, timing and quality gates. They are not photos, video clips, cast reference images or copyrighted frames. Use them as briefing/reference layouts only, not literal target actors. The production master is 1080×1920 9:16.\n')
    print('Created',len(rows),'original procedural material studies and',len(names),'technical plates')

if __name__=='__main__':main()
