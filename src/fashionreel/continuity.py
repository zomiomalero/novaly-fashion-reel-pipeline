"""Conservative studio-layout similarity diagnostics for fixed-camera fashion footage.

Only background anchor regions are compared. A warning means 'visually inspect',
never 'identity mismatch'; real people and garments are outside the metric's scope.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .config import asset_path, read_project, schedule, IMAGE_EXTENSIONS
from .media import command, ToolError


def snapshot(source: Path, time_s: float, dims=(360,640)) -> Image.Image:
    if source.suffix.lower() in IMAGE_EXTENSIONS:
        with Image.open(source) as im:
            return im.convert('RGB').resize(dims, Image.Resampling.LANCZOS)
    args=[command('ffmpeg'),'-hide_banner','-loglevel','error','-ss',f'{max(0,time_s):.3f}',
          '-i',str(source),'-frames:v','1','-vf',f'scale={dims[0]}:{dims[1]}:flags=lanczos',
          '-f','rawvideo','-pix_fmt','rgb24','-']
    result=subprocess.run(args,capture_output=True)
    if result.returncode or len(result.stdout)!=dims[0]*dims[1]*3:
        raise ToolError(f'Could not decode continuity frame: {source.name} at {time_s:.3f}s')
    return Image.frombytes('RGB',dims,result.stdout)


def anchor_metrics(ref:Image.Image,img:Image.Image,region:tuple[float,float,float,float]):
    if ref.size!=img.size:raise ValueError('anchor comparison requires same image size')
    w,h=ref.size
    x0,y0,x1,y1=region
    box=(round(x0*w),round(y0*h),round(x1*w),round(y1*h))
    aa=np.asarray(ref.crop(box).convert('L'),dtype=np.float32)
    bb=np.asarray(img.crop(box).convert('L'),dtype=np.float32)
    if min(aa.shape)<5: raise ValueError('Anchor region is too small')
    # Mean difference is not alignment: record both intensity difference and normalized high-pass agreement.
    d=float(np.mean(abs(aa-bb)))
    ae=aa-aa.mean(); be=bb-bb.mean()
    c=float(np.sum(ae*be)/max(float(np.sqrt(np.sum(ae*ae)*np.sum(be*be))),1e-7))
    return {'mean_abs_difference_8bit':round(d,3),'normalized_structure_correlation':round(c,5)}


def compare_project(project_file:str|Path,out:str|Path,anchors=None):
    p=read_project(project_file,require_assets=True)
    dest=Path(out).expanduser().resolve();dest.mkdir(parents=True,exist_ok=True)
    # Avoid faces, outfits, logos and props when possible: user may customize these regions.
    anchors=anchors or {'left_set':(.02,.14,.12,.78),'top_backdrop':(.36,.02,.62,.09)}
    scenes=[]
    for row,sc in zip(schedule(p),p['scenes']):
        source=asset_path(p,sc['asset']);begin=float(sc.get('start',0))
        t=begin+row['duration_s']*.50
        img=snapshot(source,t)
        scenes.append((sc['id'],img))
    if not scenes:raise ValueError('No scenes')
    first=scenes[0][1]
    width,height=360,640
    sheet=Image.new('RGB',(width*min(len(scenes),5), (height+32)*((len(scenes)+4)//5)), '#172026')
    draw=ImageDraw.Draw(sheet)
    rows=[]
    for j,(name,img) in enumerate(scenes):
        stats={key:anchor_metrics(first,img,tuple(coords)) for key,coords in anchors.items()}
        # warnings deliberately conservative, because backgrounds can change with light or compression.
        warnings=[key for key,s in stats.items() if s['normalized_structure_correlation']<.72 and j>0]
        rows.append({'scene':name,'relative_to':scenes[0][0],'anchor_stats':stats,'review_background_regions':warnings})
        x=j%5*width;y=j//5*(height+32)
        sheet.paste(img,(x,y));draw.text((x+8,y+height+9),f'{j+1:02} {name}',fill='#e9ebee')
        for coords in anchors.values():
            x0,y0,x1,y1=coords
            draw.rectangle((x+round(x0*width),y+round(y0*height),x+round(x1*width),y+round(y1*height)),outline='#79e0d2',width=2)
    sheet_path=dest/'continuity_contact.jpg'
    sheet.save(sheet_path,quality=90,subsampling=0)
    report={'baseline':scenes[0][0],'method':'Mid-shot 360x640 snapshot; restricted background regions only. Not face recognition.',
            'anchor_regions':anchors,'scene_diagnostics':rows,'contact_sheet':str(sheet_path),
            'limitations':['Only selected background anchors are compared, no actor identity metric.',
             'Brightness, compression and motion can lower similarity even with an identical set.',
             'A high similarity score does not prove unchanged props, costumes or set.']}
    (dest/'continuity.json').write_text(json.dumps(report,indent=2)+'\n')
    (dest/'CONTINUITY_REVIEW.md').write_text('\n'.join([
        '# Studio continuity review', '', '## Background anchor diagnostics', '',
        '| Look | Minimum structural correlation | Review regions |','|---|---:|---|',
        *[f"| {r['scene']} | {min(s['normalized_structure_correlation'] for s in r['anchor_stats'].values()):.3f} | {', '.join(r['review_background_regions']) or 'none automatically'} |" for r in rows],
        '', '## Required manual check','',
        '- [ ] Face, hands, height, hair and proportions remain the same original fictional cast',
        '- [ ] Background landmarks and floor line do not jump between cuts',
        '- [ ] Clothes match the scene manifest and do not morph inside a scene',
        '- [ ] Handbags and footwear persist in every frame',
        '- [ ] Camera is static unless the original concept explicitly calls for a move',
        '', '**A correlation number is not proof of actor identity or quality.**'])+'\n')
    return report
