"""Fast prompt-pack linting: catches recurring model-instruction contradictions."""
from __future__ import annotations
import json
import re
from pathlib import Path

DURATION_IN_TEXT=re.compile(r'\b\d+(?:\.\d+)?\s*(?:s|sec|secs|seconds|minutes)\b',re.I)
# A few specific contradictions, not a general hallucination detector.
CHANGE_CLOTHES=re.compile(r'\b(?:morph|transform|change|swap)\s+(?:the\s+)?(?:outfit|clothes|clothing|wardrobe)\b',re.I)


def lint(text:str,kind:str='animation'):
    checks=[]
    if kind=='animation' and DURATION_IN_TEXT.search(text):
        checks.append('Duration appears inside model prompt; keep duration in manifest only')
    if CHANGE_CLOTHES.search(text):
        checks.append('Potential wardrobe transformation instruction; prefer one completed look per clip')
    if kind=='animation' and not re.search(r'(?:same|preserve|locked|unchanged|consistent)',text,re.I):
        checks.append('No explicit continuity anchor for original subject/studio')
    if not re.search(r'\b(?:9:16|vertical|portrait)\b',text,re.I):
        checks.append('Vertical framing is not explicitly specified')
    if re.search(r'\b(?:make them look exactly like|clone the person|copy their face)\b',text,re.I):
        checks.append('Potential reference-person likeness copying; use an original or consented cast')
    return checks


def audit_folder(folder:str|Path,out:str|Path|None=None):
    root=Path(folder).expanduser().resolve()
    if not root.is_dir():raise ValueError(f'Prompt folder missing: {root}')
    reports=[]
    for source in sorted(root.rglob('*.txt')):
        if source.name.startswith(('STUDIO_MASTER','ORIGINAL_')):continue
        kind='still' if 'FIRST_FRAME' in source.name else 'animation'
        text=source.read_text(encoding='utf-8')
        reports.append({'file':str(source.relative_to(root)),'kind':kind,'issues':lint(text,kind),'length_chars':len(text)})
    result={'files':len(reports),'issues':sum(len(x['issues']) for x in reports),'results':reports}
    if out:
        target=Path(out).expanduser().resolve();target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result
