"""Audio QC with FFmpeg's EBU R128 / ebur128 and silencedetect filters.

`Peak` emitted by ebur128 with peak=true is a true-peak (dBFS) estimate.
"""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path
from .media import command,video_props,ToolError


def audio_report(video:str|Path,out:str|Path,expected_lufs=-16.0,peak_limit=-1.0):
    path=Path(video).expanduser().resolve();target=Path(out).expanduser().resolve();target.mkdir(parents=True,exist_ok=True)
    props=video_props(path)
    if not props['has_audio']:
        report={'status':'REVIEW','warnings':['No audio stream'],'lufs':None,'lra':None,'true_peak_dbfs':None,'silences':[]}
    else:
        proc=subprocess.run([command('ffmpeg'),'-hide_banner','-nostats','-i',str(path),'-map','0:a:0',
            '-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True)
        if proc.returncode:raise ToolError('ebur128 analysis failed: '+proc.stderr[-700:])
        summary=proc.stderr.rsplit('Summary:',1)[-1]
        def metric(tag):
            match=re.search(rf'^\s*{re.escape(tag)}:\s*(-?[\d.]+)',summary,re.M)
            return float(match.group(1)) if match else None
        integ=metric('I');lra=metric('LRA');tp=metric('Peak')
        sil=subprocess.run([command('ffmpeg'),'-hide_banner','-nostats','-i',str(path),'-map','0:a:0',
            '-af','silencedetect=n=-45dB:d=0.32','-f','null','-'],capture_output=True,text=True)
        spans=[];start=None
        for line in sil.stderr.splitlines():
            x=re.search(r'silence_start: ([\d.]+)',line)
            if x:start=float(x.group(1))
            x=re.search(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',line)
            if x:spans.append({'start_s':start,'end_s':float(x.group(1)),'duration_s':float(x.group(2))});start=None
        warnings=[]
        if integ is None:warnings.append('Could not parse integrated loudness')
        elif abs(integ-expected_lufs)>2.:warnings.append(f'Integrated loudness {integ} LUFS differs from {expected_lufs} target by >2 LU')
        if tp is not None and tp>peak_limit:warnings.append(f'True peak {tp} dBTP exceeds {peak_limit} dBTP ceiling')
        if any(x['duration_s']>.65 for x in spans):warnings.append('Audio includes silence spans >0.65s; inspect for intentional pauses')
        report={'status':'REVIEW' if warnings else 'PASS_TECHNICAL','warnings':warnings,
                'lufs':integ,'lra':lra,'true_peak_dbfs':tp,'silences':spans,
                'note':'Integrated loudness does not prove voice clarity; listen to the final mix.'}
    (target/'audio_qc.json').write_text(json.dumps(report,indent=2)+'\n')
    (target/'AUDIO_QC.md').write_text('\n'.join(['# Audio quality report','',
        f"Status: {report['status']}",f"Integrated loudness: {report.get('lufs')} LUFS",
        f"Loudness range: {report.get('lra')} LU",f"True peak: {report.get('true_peak_dbfs')} dBTP",'',
        '## Warnings',*(f'- {s}' for s in report['warnings'] or ['- None']),'',
        f"Silence spans: {len(report['silences'])}",'',
        'Manual listening: - [ ] clear first word - [ ] consistent voice - [ ] no clip pops - [ ] natural music ducking.'])+'\n')
    return report
