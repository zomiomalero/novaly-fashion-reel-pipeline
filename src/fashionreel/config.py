"""Project schema, validation, paths, and deterministic frame scheduling."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
MEDIA_EXTENSIONS = VIDEO_EXTENSIONS | IMAGE_EXTENSIONS
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")

class ProjectError(ValueError):
    pass


def read_project(path: str | Path, require_assets: bool = False) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ProjectError(f"Project not found: {source}")
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProjectError(f"Invalid project JSON: {exc}") from exc
    errors = validate(data, source.parent, require_assets=require_assets)
    if errors:
        raise ProjectError("\n".join("- " + e for e in errors))
    data["_source_path"] = str(source)
    return data


def asset_path(project: dict[str, Any], relative: str) -> Path:
    path = Path(relative).expanduser()
    base = Path(project["_source_path"]).parent
    return (path if path.is_absolute() else base / path).resolve()


def frames(scene: dict[str, Any], fps: int) -> int:
    return max(1, round(float(scene["duration"]) * fps))


def schedule(project: dict[str, Any]) -> list[dict[str, Any]]:
    fps = int(project["output"]["fps"])
    cursor = 0
    timeline = []
    for index, scene in enumerate(project["scenes"], start=1):
        count = frames(scene, fps)
        timeline.append({"index": index, "id": scene["id"], "first_frame": cursor,
                         "end_frame_exclusive": cursor + count, "frames": count,
                         "start_s": round(cursor / fps, 6), "duration_s": round(count / fps, 6),
                         "asset": scene["asset"], "title": scene.get("title", "")})
        cursor += count
    return timeline


def validate(data: Any, base: Path, require_assets: bool = False) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["Root must be a JSON object."]
    info = data.get("project", {})
    if not isinstance(info, dict) or not str(info.get("title", "")).strip():
        errs.append("project.title must be a nonempty string")
    out = data.get("output", {})
    if not isinstance(out, dict):
        errs.append("output must be an object")
        out = {}
    w, h, fps = out.get("width", 1080), out.get("height", 1920), out.get("fps", 30)
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (w, h, fps)):
        errs.append("output width, height and fps must be integers")
        w, h, fps = 1080, 1920, 30
    if w < 360 or h < 640 or w % 2 or h % 2 or abs((w / h) - (9 / 16)) > 0.002:
        errs.append("output must be even dimensions with a 9:16 aspect ratio (e.g. 1080x1920)")
    if fps not in (24, 25, 30, 60):
        errs.append("output.fps must be 24, 25, 30, or 60")
    if out.get("crf", 18) not in range(10, 30):
        errs.append("output.crf must be an integer from 10 to 29")
    scenes = data.get("scenes", [])
    if not isinstance(scenes, list) or not (1 <= len(scenes) <= 50):
        errs.append("scenes must contain between 1 and 50 scene objects")
        scenes = []
    ids: set[str] = set()
    total = 0.0
    for i, sc in enumerate(scenes, start=1):
        if not isinstance(sc, dict):
            errs.append(f"scene {i} must be an object")
            continue
        label = f"scene {i}"
        ident = sc.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", ident):
            errs.append(f"{label}.id must use letters, numbers, dash or underscore")
        elif ident in ids:
            errs.append(f"duplicate scene id: {ident}")
        ids.add(str(ident))
        duration = sc.get("duration")
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not (0.5 <= duration <= 8.0):
            errs.append(f"{label}.duration must be 0.5 to 8.0 seconds")
        else:
            total += duration
        media = sc.get("asset", "")
        if not isinstance(media, str) or not media.strip() or Path(media).suffix.lower() not in MEDIA_EXTENSIONS:
            errs.append(f"{label}.asset must be a video or image filename")
        elif require_assets:
            full = Path(media).expanduser()
            full = (full if full.is_absolute() else base / full).resolve()
            if not full.is_file():
                errs.append(f"{label}.asset is missing: {full}")
        if not isinstance(sc.get("woman_outfit", ""), str) or not isinstance(sc.get("man_outfit", ""), str):
            errs.append(f"{label} wardrobe descriptions must be strings")
        colors = sc.get("colors", [])
        if not isinstance(colors, list) or not (1 <= len(colors) <= 3):
            errs.append(f"{label}.colors must have 1 to 3 swatches")
        else:
            for ci, c in enumerate(colors):
                if not isinstance(c, dict) or not c.get("name") or not isinstance(c.get("hex"), str) or not HEX_COLOR.fullmatch(c["hex"]):
                    errs.append(f"{label}.colors[{ci}] requires name and #RRGGBB")
        if "formula" in sc and (not isinstance(sc["formula"], str) or len(sc["formula"].strip()) > 55):
            errs.append(f"{label}.formula must be at most 55 characters")
        if sc.get("fit", "cover") not in ("cover", "contain"):
            errs.append(f"{label}.fit must be cover or contain")
        for k in ("start",):
            if k in sc and (not isinstance(sc[k], (int, float)) or sc[k] < 0):
                errs.append(f"{label}.{k} must be nonnegative")
    if total > 180:
        errs.append("Total reel duration exceeds 180 seconds")
    sound = data.get("audio", {})
    if not isinstance(sound, dict):
        errs.append("audio must be an object")
        sound = {}
    for key in ("voice", "music"):
        v = sound.get(key)
        if v:
            if not isinstance(v, str) or Path(v).suffix.lower() not in {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".mp4"}:
                errs.append(f"audio.{key} has unsupported format")
            elif require_assets:
                full = Path(v).expanduser()
                full = (full if full.is_absolute() else base / full).resolve()
                if not full.is_file(): errs.append(f"audio.{key} is missing: {full}")
    return errs
