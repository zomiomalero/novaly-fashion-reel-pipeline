"""Deterministic FFmpeg edit engine. Does not generate people or clothing."""
from __future__ import annotations
import json
import shutil
import tempfile
from pathlib import Path
from .config import IMAGE_EXTENSIONS, asset_path, read_project, schedule
from .media import command, run, ffconcat_escape, video_props, ToolError
from .overlays import overlay


def vf(width: int, height: int, fps: int, count: int, mode: str) -> str:
    if mode == "cover":
        frame = (f"scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
                 f"crop={width}:{height},setsar=1")
    else:
        frame = (f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
                 f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x1B1918,setsar=1")
    return (frame + f",fps={fps},tpad=stop_mode=clone:stop_duration=10,"
            f"trim=end_frame={count},setpts=PTS-STARTPTS")


def render_scene(project: dict, scene: dict, index: int, total: int,
                 temp: Path, quick: bool = False) -> Path:
    settings = project["output"]
    width, height, fps = (int(settings[k]) for k in ("width", "height", "fps"))
    frames = round(float(scene["duration"]) * fps)
    source = asset_path(project, scene["asset"])
    image = source.suffix.lower() in IMAGE_EXTENSIONS
    if not image:
        props = video_props(source)
        available = max(0, props["duration_s"] - float(scene.get("start", 0)))
        if available < float(scene["duration"]) - 0.35:
            print(f"WARNING: {scene['id']} media is {available:.2f}s; requested {scene['duration']}s. "
                  "The final frame will freeze; generate a longer clip.")
    top_png = temp / f"overlay_{index:02d}.png"
    overlay(scene, width, height, index, total, str(project.get("project", {}).get("brand", "")), top_png)
    video = temp / f"clip_{index:02d}.mp4"
    cmd = [command("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error"]
    if image:
        cmd += ["-loop", "1", "-framerate", str(fps), "-i", str(source)]
    else:
        if scene.get("start"):
            cmd += ["-ss", str(scene["start"])]
        cmd += ["-i", str(source)]
    cmd += ["-loop", "1", "-framerate", str(fps), "-i", str(top_png)]
    flt = vf(width, height, fps, frames, scene.get("fit", "cover"))
    graph = f"[0:v]{flt}[bg];[1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    cmd += ["-filter_complex", graph, "-map", "[v]", "-an", "-frames:v", str(frames),
            "-r", str(fps), "-c:v", "libx264", "-preset", "ultrafast" if quick else "medium",
            "-crf", "24" if quick else str(settings.get("crf", 18)), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-video_track_timescale", str(fps * 1000), str(video)]
    run(cmd)
    return video


def join_scenes(parts: list[Path], temp: Path) -> Path:
    concat = temp / "concat.txt"
    concat.write_text("ffconcat version 1.0\n" + "".join(ffconcat_escape(x) for x in parts), encoding="utf-8")
    out = temp / "silent_master.mp4"
    run([command("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-safe", "0",
         "-f", "concat", "-i", str(concat), "-map", "0:v:0", "-c:v", "copy",
         "-movflags", "+faststart", str(out)])
    return out


def soundtrack(master: Path, project: dict, destination: Path, total_s: float) -> None:
    sound = project.get("audio", {})
    voice = sound.get("voice")
    music = sound.get("music")
    if not voice and not music:
        shutil.copyfile(master, destination)
        return
    cmd = [command("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-i", str(master)]
    vi = mi = None
    idx = 1
    if voice:
        vi = idx
        cmd += ["-i", str(asset_path(project, voice))]
        idx += 1
    if music:
        mi = idx
        cmd += ["-stream_loop", "-1", "-i", str(asset_path(project, music))]
    flt = []
    if vi is not None:
        gain = float(sound.get("voice_gain_db", 0))
        flt.append(f"[{vi}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB,"
                   f"apad,atrim=duration={total_s:.6f},asetpts=N/SR/TB[voice]")
    if mi is not None:
        gain = float(sound.get("music_gain_db", -18))
        flt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB,"
                   f"atrim=duration={total_s:.6f},asetpts=N/SR/TB[music]")
    if vi is not None and mi is not None:
        flt.append("[voice]asplit=2[voice_sc][voice_mix]")
        flt.append("[music][voice_sc]sidechaincompress=threshold=0.03:ratio=5:attack=50:release=350[duck]")
        flt.append("[voice_mix][duck]amix=inputs=2:duration=first:normalize=0[combined]")
    else:
        flt.append("[voice]anull[combined]" if vi is not None else "[music]anull[combined]")
    target = float(sound.get("target_lufs", -16))
    flt.append(f"[combined]loudnorm=I={target}:LRA=8:TP=-1.5[a]")
    cmd += ["-filter_complex", ";".join(flt), "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-t", f"{total_s:.6f}", "-movflags", "+faststart", str(destination)]
    run(cmd)


def render(project_file: str | Path, destination: str | Path,
           workdir: str | Path | None = None, quick: bool = False) -> Path:
    project = read_project(project_file, require_assets=True)
    output = Path(destination).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if workdir:
        work = Path(workdir).expanduser().resolve()
        work.mkdir(parents=True, exist_ok=True)
        # TemporaryDirectory deletes ONLY its own new child directory.
        tmp_context = tempfile.TemporaryDirectory(prefix="fashionreel-", dir=work)
    else:
        tmp_context = tempfile.TemporaryDirectory(prefix="fashionreel-")
    timing = schedule(project)
    with tmp_context as dirname:
        temp = Path(dirname)
        parts = []
        for i, scene in enumerate(project["scenes"], start=1):
            print(f"Rendering {i}/{len(project['scenes'])}: {scene['id']}", flush=True)
            parts.append(render_scene(project, scene, i, len(project["scenes"]), temp, quick=quick))
        master = join_scenes(parts, temp)
        length = sum(x["frames"] for x in timing) / int(project["output"]["fps"])
        soundtrack(master, project, output, length)
    manifest = {"project": project["project"], "output": str(output), "timeline": timing,
                "expected_duration_s": length, "actual": video_props(output)}
    target = output.with_name(output.stem + "_manifest.json")
    target.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {output} ({manifest['actual']['duration_s']:.3f}s)")
    return output
