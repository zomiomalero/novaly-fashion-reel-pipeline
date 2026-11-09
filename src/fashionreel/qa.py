"""Automatic technical QA. Manual face/body/wardrobe review remains mandatory."""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path
import numpy as np
from .media import command, run, video_props, ToolError
from .config import read_project, schedule


def _loudness(video: Path) -> dict:
    result = subprocess.run([command("ffmpeg"), "-hide_banner", "-nostats", "-i", str(video),
                             "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"],
                            capture_output=True, text=True)
    if result.returncode:
        return {"error": "Audio analysis failed"}
    tail = result.stderr.split("Summary:")[-1]
    match = re.search(r"^\s*I:\s*([-\d.]+)", tail, re.M)
    peak = re.search(r"^\s*Peak:\s*([-\d.]+)", tail, re.M)
    return {"integrated_lufs": float(match.group(1)) if match else None,
            "peak_dbfs": float(peak.group(1)) if peak else None}


def analyze_frames(path: Path, fps: float) -> dict:
    w, h = 90, 160
    cmd = [command("ffmpeg"), "-hide_banner", "-loglevel", "error", "-i", str(path),
           "-map", "0:v:0", "-vf", f"scale={w}:{h}:flags=area", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    prev = None
    frame = 0
    black, white, frozen, spikes = [], [], [], []
    freeze_start = None
    average_delta = []
    while True:
        block = process.stdout.read(w * h * 3)
        if len(block) < w * h * 3:
            break
        rgb = np.frombuffer(block, np.uint8).reshape((h, w, 3))
        luma = (rgb[..., 0].astype(np.float32) * .2126 + rgb[..., 1] * .7152 + rgb[..., 2] * .0722) / 255
        mean = float(luma.mean())
        if mean < .035: black.append(frame)
        if mean > .95: white.append(frame)
        if prev is not None:
            delta = float(np.abs(rgb.astype(np.int16) - prev).mean())
            average_delta.append(delta)
            if delta < 0.035:
                if freeze_start is None: freeze_start = frame - 1
            elif freeze_start is not None:
                if frame - freeze_start >= 12: frozen.append([freeze_start, frame])
                freeze_start = None
        prev = rgb.copy()
        frame += 1
    process.stdout.close()
    err = process.stderr.read().decode("utf-8", errors="replace")
    process.stderr.close()
    process.wait()
    if process.returncode:
        raise ToolError(f"FFmpeg frame analysis failed: {err[-1000:]}")
    if freeze_start is not None and frame - freeze_start >= 12:
        frozen.append([freeze_start, frame])
    med = float(np.median(average_delta)) if average_delta else 0
    # A large delta can be a deliberate hard cut: report candidates, not failures.
    if med > 0:
        spikes = [i + 1 for i, x in enumerate(average_delta) if x > max(16.0, med * 10)]
    return {"frames_decoded": frame, "black_frames": black[:60], "white_frames": white[:60],
            "frozen_spans_frames": frozen[:40], "candidate_cut_frames": spikes[:100],
            "mean_frame_delta": round(float(np.mean(average_delta)), 3) if average_delta else 0}


def check(video: str | Path, output_dir: str | Path,
          project_file: str | Path | None = None) -> dict:
    source = Path(video).expanduser().resolve()
    target = Path(output_dir).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    media = video_props(source)
    frames = analyze_frames(source, media["fps"])
    warnings = []
    failures = []
    if not media["has_audio"]:
        warnings.append("No audio stream. Add voice or original licensed music before publishing.")
    if media["width"] is None or media["height"] is None:
        failures.append("Missing video stream")
    elif abs(media["width"] / media["height"] - 9 / 16) > .002:
        failures.append("Video is not in vertical 9:16 format")
    if frames["black_frames"]:
        warnings.append(f"Found {len(frames['black_frames'])} near-black frames (sample listing capped)")
    if frames["white_frames"]:
        warnings.append(f"Found {len(frames['white_frames'])} near-white frames (sample listing capped)")
    if frames["frozen_spans_frames"]:
        warnings.append(f"Found {len(frames['frozen_spans_frames'])} spans with exactly repeated frames. "
                        "A still photo is allowed, but a talking video must not be frozen.")
    if project_file:
        project = read_project(project_file)
        timeline = schedule(project)
        expected_frames = sum(s["frames"] for s in timeline)
        if media["width"] != project["output"]["width"] or media["height"] != project["output"]["height"]:
            failures.append("Video dimensions differ from output specification")
        if abs(media["fps"] - project["output"]["fps"]) > .1:
            failures.append("Video frame rate differs from output specification")
        if abs(frames["frames_decoded"] - expected_frames) > 1:
            failures.append(f"Frame count mismatch: expected {expected_frames}, got {frames['frames_decoded']}")
        else:
            frames["expected_frames"] = expected_frames
    sound = _loudness(source) if media["has_audio"] else None
    if sound and sound.get("integrated_lufs") is not None:
        if abs(sound["integrated_lufs"] - (-16)) > 3:
            warnings.append("Integrated loudness is over 3 LU away from the -16 LUFS target")
        if sound.get("peak_dbfs", -100) > -0.5:
            warnings.append("Audio peak above -0.5 dBFS; inspect clipping and true peak")
    output = {"status": "FAIL" if failures else "REVIEW" if warnings else "PASS_TECHNICAL",
              "video": str(source), "technical_properties": media, "frame_checks": frames,
              "audio_loudness": sound, "failures": failures, "warnings": warnings,
              "human_review_required": ["presenter identity and hands", "wardrobe colors and cloth motion",
                                        "consistent background and camera", "rights and licensing", "audio sync"]}
    (target / "qa.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    report = ["# Video technical QA", "", f"Status: **{output['status']}**", "",
              f"Dimensions: {media['width']}x{media['height']} / {media['fps']} fps",
              f"Duration: {media['duration_s']:.3f}s / {frames['frames_decoded']} decoded frames", "",
              "## Failures", *(f"- {f}" for f in failures or ["None"]), "",
              "## Warnings", *(f"- {w}" for w in warnings or ["None"]), "",
              "## Human sign-off (cannot be proven by this script)",
              *(f"- [ ] {f}" for f in output["human_review_required"]), ""]
    (target / "qa.md").write_text("\n".join(report), encoding="utf-8")
    return output
