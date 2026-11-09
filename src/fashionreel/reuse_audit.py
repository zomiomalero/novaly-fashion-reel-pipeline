"""Cross-reference near-duplicate visual audit without copying or exposing any source pixels.

Sample one frame per second, normalize to 80×142 RGB, compare nearest sampled
frames in the central garment region. It detects near-identical visual *states*,
not provenance, shared ownership, identical original takes or copyright status.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
import numpy as np
from .media import command, ToolError

W,H=80,142
SAMPLE_FPS=1


def sample_video(path:str|Path,fps:int=SAMPLE_FPS)->np.ndarray:
    path=Path(path).expanduser().resolve()
    z=subprocess.run([command('ffmpeg'),'-hide_banner','-loglevel','error','-i',str(path),
        '-vf',f'fps={fps},scale={W}:{H}:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True)
    if z.returncode:raise ToolError(f'Reuse audit could not decode {path.name}: '+z.stderr.decode(errors='replace')[-500:])
    if len(z.stdout)%(W*H*3):raise ToolError('Truncated frame output in reuse audit')
    return np.frombuffer(z.stdout,np.uint8).reshape(-1,H,W,3)


def compare_arrays(first:np.ndarray,second:np.ndarray,threshold=8.0):
    if not len(first) or not len(second):
        return {'minimum_distance':None,'median_nearest_distance':None,'matching_samples':0,'first_samples':len(first),'second_samples':len(second),'threshold':threshold}
    a=first[:,25:140,:,:].astype(np.int16)
    b=second[:,25:140,:,:].astype(np.int16)
    # Small batches to cap memory for longer videos.
    nearest=[]
    for part in np.array_split(a,max(1,(len(a)+31)//32)):
        dist=np.abs(part[:,None,:,:,:]-b[None,:,:,:,:]).mean(axis=(2,3,4))
        nearest.extend(dist.min(axis=1).tolist())
    nearest=np.asarray(nearest)
    return {'minimum_distance':round(float(nearest.min()),3),
            'median_nearest_distance':round(float(np.median(nearest)),3),
            'matching_samples':int(np.count_nonzero(nearest<threshold)),
            'first_samples':len(first),'second_samples':len(second),'threshold':threshold,
            'interpretation':'Matching sample counts are asymmetric, because each frame in A searches nearest frame in B; study only.'}


def audit_videos(videos:list[str|Path],out:str|Path,threshold=8.0):
    output=Path(out).expanduser().resolve()
    output.mkdir(parents=True,exist_ok=True)
    samples=[sample_video(p) for p in videos]
    pairs=[]
    for i,a in enumerate(samples):
        for j in range(i+1,len(samples)):
            pairs.append({'a_index':i+1,'b_index':j+1,
                **compare_arrays(a,samples[j],threshold=threshold)})
    result={'method':'1fps source-frame sampling, 80x142 RGB normalized, central band y=25:140, per-pixel mean absolute RGB difference',
            'threshold_8bit':threshold,'videos':len(videos),'pairs':pairs,
            'cautions':['This is a similarity heuristic, not a copyright determination.',
                'Shared studio, similar poses or reused garments can create false positives.',
                'Only sampled frames are checked; event order and audio are not compared.']}
    (output/'reuse_matrix.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Cross-video visual reuse audit','',
           'A 1fps visual-similarity study for editorial diversity planning. Numbers are not proof of identical source ownership.',
           '', '| A | B | Closest frame distance (8-bit RGB) | Nearest median | Near-match samples A→B |','|---:|---:|---:|---:|---:|']
    for p in pairs:
        lines.append(f"| {p['a_index']:02} | {p['b_index']:02} | {p['minimum_distance']:.2f} | {p['median_nearest_distance']:.2f} | {p['matching_samples']}/{p['first_samples']} |")
    lines+=['','Lower distance = closer visual sample. Matching samples use **threshold < 8** at 80×142; interpret with caution.','',
        '## Why this matters','',
        '- Multiple source reels can share the same studio, performers and wardrobe sequence. Do not count them as wholly independent training cases.',
        '- Derive the overall production grammar, then make new original concepts, wardrobe choices and models.',
        '- Use scene-level repeat history and compare your OWN finished reels before publishing.',
        '- A similar studio background alone is not evidence of content theft or identity copying.']
    (output/'REUSE_AUDIT.md').write_text('\n'.join(lines)+'\n')
    return result
