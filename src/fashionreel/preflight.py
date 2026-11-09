"""Independent asset preflight and reproducible source inventory for fashion reels.

Preflight does not create or modify clips. It checks technical compatibility and
records SHA-256 for provenance. It cannot certify rights, character identity,
visual correctness or whether an outfit looks good.
"""
from __future__ import annotations
import hashlib
import json
import mimetypes
from pathlib import Path
from PIL import Image
from .config import asset_path, read_project, schedule, IMAGE_EXTENSIONS
from .media import video_props


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inspect_assets(project_file: str | Path, destination: str | Path) -> dict:
    p = read_project(project_file)
    target = Path(destination).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    errors, warnings, entries = [], [], []
    seen = {}
    output = p['output']
    for row, sc in zip(schedule(p), p['scenes']):
        path = asset_path(p, sc['asset'])
        source = {'look':row['index'], 'id':sc['id'],'relative_asset':sc['asset'], 'exists':path.is_file(),
                  'requested_duration_s':row['duration_s'], 'start_s':float(sc.get('start',0)),
                  'declared_rights':sc.get('rights','not_provided'), 'warnings':[]}
        if not path.is_file():
            errors.append(f"{sc['id']}: missing source media {path.name}")
            entries.append(source)
            continue
        source['bytes']=path.stat().st_size
        source['sha256']=sha256_file(path)
        if source['sha256'] in seen:
            warn=f"{sc['id']}: source duplicates {seen[source['sha256']]} byte-for-byte"
            source['warnings'].append(warn); warnings.append(warn)
        seen[source['sha256']]=sc['id']
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            try:
                with Image.open(path) as im:
                    source['kind']='image'
                    source['width'],source['height']=im.size
            except Exception as exc:
                errors.append(f"{sc['id']}: cannot decode still: {exc}")
                entries.append(source); continue
        else:
            try:
                inf=video_props(path)
            except Exception as exc:
                errors.append(f"{sc['id']}: cannot probe video: {exc}")
                entries.append(source);continue
            source.update(kind='video',**inf)
            available=inf['duration_s']-source['start_s']
            if available<row['duration_s']-.08:
                warn=(f"{sc['id']}: source only has {available:.2f}s after start but "
                      f"timeline needs {row['duration_s']:.2f}s; renderer may freeze tail")
                warnings.append(warn);source['warnings'].append(warn)
            if inf['fps'] and inf['fps'] < 20:
                warn=f"{sc['id']}: source frame rate below 20; motion may judder"
                warnings.append(warn);source['warnings'].append(warn)
        if source.get('width') and source.get('height'):
            w,h=source['width'],source['height']
            if min(w/output['width'],h/output['height']) < .66:
                warn=f"{sc['id']}: significant upscale required from {w}x{h} to {output['width']}x{output['height']}"
                warnings.append(warn);source['warnings'].append(warn)
            if abs(w/h-9/16)>.04:
                warn=f"{sc['id']}: source aspect ratio {w/h:.3f}; inspect crop or pillarboxing"
                warnings.append(warn);source['warnings'].append(warn)
        if source['declared_rights']=='not_provided':
            warn=f"{sc['id']}: rights declaration absent (manual clearance required)"
            warnings.append(warn);source['warnings'].append(warn)
        entries.append(source)
    for key in ('voice','music'):
        rel=p.get('audio',{}).get(key)
        if rel and not asset_path(p,rel).is_file():
            errors.append(f"audio.{key} missing: {rel}")
    result={'status':'FAIL' if errors else 'REVIEW' if warnings else 'PASS_TECHNICAL',
            'source_project':str(Path(project_file).resolve()),'scene_count':len(entries),
            'timeline_frames':sum(r['frames'] for r in schedule(p)),
            'timeline_seconds':sum(r['frames'] for r in schedule(p))/output['fps'],
            'sources':entries,'errors':errors,'warnings':warnings,
            'manual_signoff_required':['Rights and original/consented identities', 'Hands and clothing changes during shot',
                'Body proportions and camera height match across all scenes',
                'Studio anchor match and natural shadows', 'Exact garment label and source outfit agreement']}
    (target/'preflight.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (target/'PREFLIGHT.md').write_text('\n'.join([
        '# Asset and rights preflight', '', f"Status: **{result['status']}**; {len(entries)} scenes.", '',
        '## Errors', *(f'- {x}' for x in errors or ['- None']), '', '## Warnings',
        *(f'- {x}' for x in warnings or ['- None']), '',
        '## Manual approvals', *(f'- [ ] {x}' for x in result['manual_signoff_required']), '',
        'This preflight deliberately does not use face recognition or invent licensing approval.'])+'\n',encoding='utf-8')
    return result
