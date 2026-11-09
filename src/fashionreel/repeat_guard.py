"""Optional content-history guard: flags repeated palettes and wardrobe concepts."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", value.lower())).strip()


def key_for_scene(scene: dict) -> str:
    palette = sorted(c["hex"].lower() for c in scene["colors"])
    outfits = [_clean(scene.get("woman_outfit", "")), _clean(scene.get("man_outfit", ""))]
    raw = "|".join(palette + outfits)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def palette_key(scene: dict) -> str:
    return " + ".join(sorted(c["hex"].upper() for c in scene["colors"]))


def review(project: dict, history_file: str | Path, register: bool = False) -> dict:
    history_path = Path(history_file).expanduser().resolve()
    if history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8"))
        if not isinstance(history, list):
            raise ValueError("History file must contain a JSON array")
    else:
        history = []
    prev_ids = {x.get("key") for x in history}
    prev_palette = {x.get("palette") for x in history}
    findings = []
    rows = []
    for sc in project["scenes"]:
        key, palette = key_for_scene(sc), palette_key(sc)
        if key in prev_ids:
            findings.append(f"Exact wardrobe and colors already used: {sc['id']}")
        elif palette in prev_palette:
            findings.append(f"Color combination already used; differentiate styling: {sc['id']}")
        rows.append({"key": key, "palette": palette, "scene_id": sc["id"],
                     "project": project["project"]["title"]})
    if register:
        if findings:
            raise ValueError("Registration blocked due to repeat findings; review first: " + "; ".join(findings))
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(json.dumps(history + rows, indent=2), encoding="utf-8")
    return {"findings": findings, "new_entries": len(rows), "registered": bool(register),
            "history_file": str(history_path)}
