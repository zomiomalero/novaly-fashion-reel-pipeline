"""Checked FFmpeg wrappers, metadata and file handling."""
from __future__ import annotations
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

class ToolError(RuntimeError):
    pass


def command(exe: str) -> str:
    resolved = shutil.which(exe)
    if not resolved:
        raise ToolError(f"Missing {exe}. Install FFmpeg and ensure {exe} is on PATH.")
    return resolved


def run(args: list[str], capture: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(args, text=True, capture_output=capture, check=False)
    except OSError as exc:
        raise ToolError(str(exc)) from exc
    if result.returncode:
        msg = (result.stderr or result.stdout or "command failed")[-3500:]
        raise ToolError(f"Command failed (exit {result.returncode}): {' '.join(args[:6])}\n{msg}")
    return result


def probe(path: str | Path) -> dict[str, Any]:
    result = run([command("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    return json.loads(result.stdout)


def video_props(path: str | Path) -> dict[str, Any]:
    meta = probe(path)
    video = next((s for s in meta["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in meta["streams"] if s["codec_type"] == "audio"), None)
    rate = video.get("avg_frame_rate", "0/1") if video else "0/1"
    parts = rate.split("/")
    fps = float(parts[0]) / float(parts[1]) if len(parts) == 2 and float(parts[1]) else 0
    return {"width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "fps": round(fps, 5), "duration_s": float(meta.get("format", {}).get("duration", 0)),
            "video_codec": video.get("codec_name") if video else None,
            "audio_codec": audio.get("codec_name") if audio else None,
            "has_audio": bool(audio)}


def ffconcat_escape(path: str | Path) -> str:
    # The concat demuxer uses FFmpeg's single-quote escaping, not shell syntax.
    return "file '" + str(Path(path).resolve()).replace("'", "'\\''") + "'\n"
