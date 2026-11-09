"""Word-time storyboard synchronization from externally verified speech timing JSON.

This module does NOT generate speech-to-text alignments or claim that estimated
word timings match audio. It consumes corrected timestamps from an aligner.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
from .config import read_project,schedule


def load_words(filename:str|Path):
    data=json.loads(Path(filename).read_text(encoding='utf-8'))
    if isinstance(data,dict):data=data.get('words')
    if not isinstance(data,list) or not data:raise ValueError('words JSON must be a nonempty list or {"words": [...]}')
    prev=-1.
    for j,word in enumerate(data):
        if not isinstance(word,dict):raise ValueError(f'word {j} is not an object')
        for name in ('start','end','text'):
            if name not in word:raise ValueError(f'word {j} lacks {name}')
        a,b=float(word['start']),float(word['end'])
        if not(0<=a<=b):raise ValueError(f'word {j} has invalid interval')
        if a<prev-.08:raise ValueError('word starts are not chronological')
        prev=a
    return data


def make_sync_map(project_file:str|Path,words_file:str|Path,out:str|Path):
    project=read_project(project_file)
    words=load_words(words_file)
    timeline=schedule(project)
    fps=project['output']['fps'];out=Path(out).expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
    segments=[]
    for row in timeline:
        a,b=row['start_s'],row['start_s']+row['duration_s']
        hits=[w for w in words if float(w['start']) < b and float(w['end']) > a]
        segments.append({'look':row['id'],'from_frame':row['first_frame'],'to_frame_exclusive':row['end_frame_exclusive'],
            'spoken_words':' '.join(str(w['text']) for w in hits),
            'word_count':len(hits),'first_word_start':hits[0]['start'] if hits else None,
            'last_word_end':hits[-1]['end'] if hits else None})
    end=timeline[-1]['end_frame_exclusive']/fps
    warnings=[]
    if float(words[-1]['end'])>end+.15:warnings.append('Speech extends beyond final video frame')
    if float(words[0]['start'])>.35:warnings.append('Voice starts later than 0.35s; hook may feel delayed')
    result={'fps':fps,'duration_s':end,'segments':segments,'warnings':warnings,
           'source_timing':'External corrected words.json; alignments not generated or verified by this module'}
    (out/'word_sync.json').write_text(json.dumps(result,indent=2)+'\n')
    with (out/'word_sync.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['look','from_frame','to_frame_exclusive','word_count','spoken_words'])
        for s in segments:w.writerow([s[k] for k in ['look','from_frame','to_frame_exclusive','word_count','spoken_words']])
    return result
