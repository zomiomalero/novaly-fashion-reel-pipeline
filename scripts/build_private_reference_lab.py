#!/usr/bin/env python3
"""Create a PRIVATE, reusable reference study, never for GitHub redistribution.

Every decoded frame is measured at 90x160; illustrative visual sheets sample 10 fps.
The input clips are external visual references and are not included in the archive.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

FPS_SHEETS = 10
THUMB_W, THUMB_H = 144, 256
LABEL_H = 21
PER_SHEET = 60
METRIC_W, METRIC_H = 90, 160
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def ffprobe(path: Path):
    proc = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,width,height,r_frame_rate,nb_frames','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(proc.stdout)


def frame_pipe(path: Path, w: int, h: int, fps: int|None = None):
    filt = f'fps={fps},scale={w}:{h}:flags=area' if fps is not None else f'scale={w}:{h}:flags=area'
    p = subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:v:0','-vf',filt,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        while True:
            raw = p.stdout.read(w*h*3)
            if len(raw)==0: break
            if len(raw)!=w*h*3: raise RuntimeError('Truncated raw frame')
            yield np.frombuffer(raw,np.uint8).reshape(h,w,3).copy()
    finally:
        p.stdout.close()
        err=p.stderr.read().decode(errors='replace')
        p.stderr.close()
        rc=p.wait()
        if rc: raise RuntimeError(f'ffmpeg decode failed {path.name}: {err[-700:]}')


def font(size):
    try:return ImageFont.truetype(FONT,size)
    except OSError:return ImageFont.load_default()


def output_sheet(out:Path,frames:list[tuple[int,Image.Image]],idx:int,source:str):
    cols,rows=10,6
    im=Image.new('RGB',(cols*THUMB_W,rows*(THUMB_H+LABEL_H)+52),'#12171c')
    d=ImageDraw.Draw(im)
    d.text((13,9),f'{source}    |    sheet {idx+1}    |    10 samples/second',fill='#f4f6f7',font=font(17))
    for k,(frame,thumb) in enumerate(frames):
        col,row=k%cols,k//cols
        x,y=col*THUMB_W,52+row*(THUMB_H+LABEL_H)
        im.paste(thumb,(x,y))
        d.text((x+7,y+THUMB_H+3),f'{frame/FPS_SHEETS:06.2f}s  #{frame:04d}',fill='#e6e8ea',font=font(12))
    path=out/f'contact_{idx+1:02}.jpg'
    im.save(path,'JPEG',quality=93,subsampling=0,optimize=True)
    return path


def metrics_for(path:Path,sourcefps:float):
    rows=[]
    prev=None
    for frame,im in enumerate(frame_pipe(path,METRIC_W,METRIC_H)):
        a=im.astype(np.float32)/255.
        luminance=a[...,0]*.2126+a[...,1]*.7152+a[...,2]*.0722
        mx=a.max(axis=2); mn=a.min(axis=2)
        saturation=(mx-mn)/np.maximum(mx,1/255)
        grey=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
        edges=cv2.Canny(grey,50,120)
        # Background region deliberately avoids center presenters; can still include foreground props.
        bg=im[round(METRIC_H*.1):round(METRIC_H*.8),:round(METRIC_W*.1),:]
        bgb=bg.mean(axis=(0,1))
        diff=float(np.abs(im.astype(np.int16)-prev.astype(np.int16)).mean()) if prev is not None else 0
        rows.append((frame,frame/sourcefps,round(float(luminance.mean()),5),round(float(saturation.mean()),5),round(float(edges.mean()/255),5),round(diff,3),*[round(float(x),2) for x in bgb]))
        prev=im
    a=np.asarray(rows,dtype=np.float64)
    return rows,a


def write_plot(path:Path,arr:np.ndarray,cuts:list[float],fps:float,video_id:int):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(3,1,figsize=(13,7),sharex=True)
    series=[('Frame-to-frame RGB change',arr[:,5]),('Mean luminance',arr[:,2]),('Edge density',arr[:,4])]
    for ax,(name,data) in zip(axes,series):
        ax.plot(arr[:,1],data,lw=.9)
        for t in cuts:ax.axvline(t,lw=.65,alpha=.35)
        ax.set_ylabel(name)
        ax.grid(alpha=.2)
    axes[-1].set_xlabel('Source timeline, seconds')
    fig.suptitle(f'Reference {video_id:02d} — complete decoded-frame signals (cuts are review candidates)')
    fig.tight_layout()
    fig.savefig(path,dpi=140)
    plt.close(fig)


def make_report(meta:dict,cuts:list[float]):
    fps=meta['source_fps']; n=meta['frames_measured']; dur=meta['duration_seconds']
    intervals=[0.0,*cuts,dur]
    lengths=[round(b-a,2) for a,b in zip(intervals,intervals[1:]) if b-a>.15]
    lines=[f"# Reference {meta['id']:02d} — deep technical study",'',
         '> PRIVATE ANALYSIS. For personal study only. Do not publish these frames, clips, or likenesses.', '',
         f"Original: {meta['width']}×{meta['height']}, {fps:.3f} fps, {dur:.3f}s, {n} measured frames.",
         f"Average frame-change: {meta['mean_rgb_delta']:.3f} on 8-bit RGB; mean luminance: {meta['mean_luminance']:.3f}; saturation: {meta['mean_saturation']:.3f}.",
         f"Sample sheets: {meta['number_of_contact_sheets']} at 10 fps. Single-frame samples: {meta['number_of_keyframes']} at 540×960.", '',
         '## Candidate look boundaries (algorithmic, review manually)', '',
         'These are **not verified cuts**. Motions, hand gestures and overlay changes can trigger false positives.','',
         '| Event | Timestamp | Elapsed since prior |','|---:|---:|---:|']
    last=0
    for j,t in enumerate(cuts,1):
        lines.append(f'| {j} | {t:.2f}s | {t-last:.2f}s |')
        last=t
    lines += ['', '## What each deliverable contains', '',
              '- `metrics_every_frame.csv` samples **all** decoded frames; column descriptions in `FIELDS.md`.',
              '- `contact_*.jpg` each contains up to 60 chronological visual samples at 10 fps.',
              '- `keyframes/frame_*.jpg` are larger source-derived views for comparing wardrobe and framing.',
              '- `timeline_signals.png` shows whole-video frame change, luminance and edges.',
              '- `manifest.json` has source SHA-256 and the sampling configuration.', '',
              '## Interpretation discipline', '',
              '1. Inspect neighboring frames before calling a large pixel difference a cut.',
              '2. Inspect the lower half of the frame for shoe/hem cutoffs, relative actor sizes and garment motion.',
              '3. Inspect the upper corners for set anchors, caption position and background stability.',
              '4. Note how the second presenter reacts; avoid synchronized robotic gestures.',
              '5. Use these references for pacing and framing only; invent new people, outfits and environment.', '',
              '## Human markup', '',
              '| Time | Outfit pair / silhouette | Gesture | Overlay text | Camera / anchor issues |','|---|---|---|---|---|',
              *[f'| {i:02d}:00–{i+2:02d}:00 | | | | |' for i in range(0,int(math.ceil(dur)),2)]]
    return '\n'.join(lines)+'\n'


def run(paths:list[Path],output:Path,pre_cuts:dict[int,list[float]]):
    output.mkdir(parents=True,exist_ok=True)
    root=[]
    for vid,path in enumerate(paths,1):
        info=ffprobe(path)
        stream=next(s for s in info['streams'] if s['codec_type']=='video')
        n,d=map(int,stream['r_frame_rate'].split('/'))
        native_fps=n/d
        duration=float(info['format']['duration'])
        target=output/f'ref_{vid:02d}'
        target.mkdir(exist_ok=True)
        (target/'keyframes').mkdir(exist_ok=True)
        print('VIDEO',vid,path.name[:25],duration,native_fps,flush=True)
        metrics,arr=metrics_for(path,native_fps)
        with (target/'metrics_every_frame.csv').open('w',newline='') as f:
            w=csv.writer(f)
            w.writerow(['source_frame','source_time_seconds','luminance_mean','saturation_mean','edge_fraction','rgb_delta_8bit','background_left_R','background_left_G','background_left_B'])
            w.writerows(metrics)
        cuts=pre_cuts.get(vid,[])
        # Rich sheets sampled 10/s; no source videos saved or redistributed.
        sheets=[]; chunk=[]; keyframes=[]; total=0
        for k,im in enumerate(frame_pipe(path,THUMB_W,THUMB_H,FPS_SHEETS)):
            chunk.append((k,Image.fromarray(im)))
            total+=1
            if len(chunk)==PER_SHEET:
                sheets.append(output_sheet(target,chunk,len(sheets),f'Reference {vid:02d}'))
                chunk=[]
        if chunk:sheets.append(output_sheet(target,chunk,len(sheets),f'Reference {vid:02d}'))
        # Each source contributes 14 larger independent key frames, chronological coverage.
        for idx,second in enumerate(np.linspace(.25,max(.25,duration-.25),14)):
            proc=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',f'{second:.3f}','-i',str(path),'-frames:v','1','-vf','scale=540:960:flags=lanczos','-q:v','2','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True)
            if proc.returncode==0 and proc.stdout:
                out=target/'keyframes'/f'frame_{idx+1:02d}_t{second:.2f}.jpg'
                out.write_bytes(proc.stdout)
                keyframes.append(str(out.relative_to(target)))
        meta={'id':vid,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
              'source_fps':native_fps,'duration_seconds':duration,'width':stream['width'],'height':stream['height'],
              'frames_measured':len(arr),'mean_rgb_delta':round(float(arr[:,5].mean()),4),
              'mean_luminance':round(float(arr[:,2].mean()),4),'mean_saturation':round(float(arr[:,3].mean()),4),
              'number_of_contact_sheets':len(sheets),'number_of_keyframes':len(keyframes),
              'visual_sample_hz':FPS_SHEETS,'candidate_look_boundaries_seconds':cuts,
              'contact_sheets':[x.name for x in sheets],'keyframes':keyframes}
        write_plot(target/'timeline_signals.png',arr,cuts,native_fps,vid)
        (target/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
        (target/'STUDY.md').write_text(make_report(meta,cuts))
        root.append(meta)
    (output/'STUDY_INDEX.md').write_text('# Private seven-video motion and wardrobe study\n\n**Do not publish or push this directory to GitHub.** The frames are taken from user-supplied third-party reference videos for local study, not from original Novaly productions.\n\nThe build measures EVERY decoded native frame at 90×160 for luminance, saturation, edges and RGB difference; creates 10fps chronological contact sheets and 14 larger keyframes per video. It does not claim to recognize faces or identify precise editorial cut points.\n\n'+ '\n'.join(f"- [Reference {m['id']:02d}](ref_{m['id']:02d}/STUDY.md): {m['duration_seconds']:.2f}s; {m['frames_measured']} measured frames; {m['number_of_contact_sheets']} contact sheets" for m in root)+'\n')
    (output/'FIELDS.md').write_text('# Per-frame metric definitions\n\nAll rows correspond to decoded source frames in playback order, without interpolating or dropping frames. `source_time_seconds` equals frame index / nominal stream fps, so VFR source timestamps may differ. `rgb_delta_8bit` is mean absolute RGB difference against the previous frame at 90×160. `luminance_mean` uses Rec.709 weights on gamma-encoded RGB (relative brightness proxy, not calibrated linear luminance). `saturation_mean` is HSV-like channel chroma / max. `edge_fraction` is Canny(50,120) fraction. Background RGB is the average in the leftmost 10% of the image between 10% and 80% height, which is a proxy and may include scene objects. It is NOT a perfect camera stabilization measurement. 10fps sheets deliberately subsample the original source and should not be represented as every frame.\n')
    (output/'metadata.json').write_text(json.dumps(root,indent=2)+'\n')
    print('FINAL',len(root),'videos',sum(x['frames_measured'] for x in root),'frames measured',sum(x['number_of_contact_sheets'] for x in root),'sheets',flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('videos',nargs='+',type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--cuts-json',type=Path)
    a=p.parse_args()
    cuts={}
    if a.cuts_json and a.cuts_json.is_file():
        j=json.loads(a.cuts_json.read_text())
        cuts={int(r['ref']):r['major_visual_transitions_s'] for r in j}
    run(a.videos,a.output,cuts)

if __name__=='__main__':main()
