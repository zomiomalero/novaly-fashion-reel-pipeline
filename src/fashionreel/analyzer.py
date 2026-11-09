"""Offline reference video inspection without uploading reference material."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from .media import command, video_props, ToolError


def thumbnail(video: Path, second: float, width: int = 180, height: int = 320) -> Image.Image:
    args = [command("ffmpeg"), "-hide_banner", "-loglevel", "error", "-ss", f"{second:.3f}",
            "-i", str(video), "-frames:v", "1", "-vf", f"scale={width}:{height}:flags=lanczos",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.run(args, capture_output=True, check=False)
    if proc.returncode or len(proc.stdout) != width * height * 3:
        raise ToolError(f"Cannot extract reference frame at {second:.2f}s: {video}")
    return Image.frombytes("RGB", (width, height), proc.stdout)


def inspect_one(video: str | Path, destination: str | Path, count: int = 12) -> dict:
    source = Path(video).expanduser().resolve()
    target = Path(destination).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    if not (4 <= count <= 60):
        raise ValueError("count must be between 4 and 60")
    info = video_props(source)
    width, height, label_h = 180, 320, 26
    cols = min(6, count)
    rows = (count + cols - 1) // cols
    sheet = Image.new("RGB", (width * cols, (height + label_h) * rows), (20, 21, 24))
    d = ImageDraw.Draw(sheet)
    times = [max(0, min(info["duration_s"] - .1, (i + .25) / count * info["duration_s"])) for i in range(count)]
    for i, second in enumerate(times):
        img = thumbnail(source, second, width, height)
        x, y = (i % cols) * width, (i // cols) * (height + label_h)
        sheet.paste(img, (x, y))
        d.text((x + 5, y + height + 5), f"{second:.1f}s", fill="white")
    contact = target / (source.stem[:32] + "_contact.jpg")
    sheet.save(contact, quality=88)
    result = {"video": source.name, "duration_s": info["duration_s"], "width": info["width"],
              "height": info["height"], "fps": info["fps"], "has_audio": info["has_audio"],
              "contact_sheet": str(contact), "frames_sampled": count,
              "sample_times_s": [round(x, 3) for x in times]}
    (target / (source.stem[:32] + "_analysis.json")).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
