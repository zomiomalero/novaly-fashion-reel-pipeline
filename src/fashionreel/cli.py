"""Command line interface for local fashion short production."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from . import __version__
from .analyzer import inspect_one
from .config import ProjectError, read_project, schedule
from .demo import create_demo
from .media import ToolError
from .prompts import build_prompt_pack
from .render import render
from .repeat_guard import review
from .qa import check
from .storyboard import write_storyboard
from .preflight import inspect_assets
from .continuity import compare_project
from .prompt_audit import audit_folder
from .word_timing import make_sync_map
from .audio_qc import audio_report
from .reuse_audit import audit_videos

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fashionreel", description="Original 9:16 editorial fashion reels")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init", help="Copy a ready-made project template into a new local folder")
    init.add_argument("folder")
    init.add_argument("--preset", choices=sorted(x.name for x in EXAMPLES.iterdir() if (x / "project.json").is_file()), default="color-pair-looks")
    check_p = sub.add_parser("validate", help="Validate config, timings and optional source assets")
    check_p.add_argument("project")
    check_p.add_argument("--assets", action="store_true")
    story = sub.add_parser("storyboard", help="Write storyboard, timeline and human QC checklist")
    story.add_argument("project")
    story.add_argument("--out", default="storyboard.md")
    prompts = sub.add_parser("prompts", help="Generate ready-to-use AI image-to-video shot prompts")
    prompts.add_argument("project")
    prompts.add_argument("--out", default="prompt_pack")
    render_p = sub.add_parser("render", help="Render asset clips/stills, labels and optional audio to MP4")
    render_p.add_argument("project")
    render_p.add_argument("--out", default="final.mp4")
    render_p.add_argument("--workdir", default=None, help="Put temporary render files on an external SSD")
    render_p.add_argument("--quick", action="store_true", help="Speed-focused preview only")
    qa = sub.add_parser("qa", help="Check dimensions, frame count, frozen frames and audio")
    qa.add_argument("video")
    qa.add_argument("--project", default=None)
    qa.add_argument("--out", default="qa_report")
    inspect = sub.add_parser("analyze", help="Create contact sheets of original reference videos locally")
    inspect.add_argument("videos", nargs="+")
    inspect.add_argument("--out", default="reference_analysis")
    inspect.add_argument("--frames", type=int, default=12)
    repeat = sub.add_parser("repeats", help="Compare wardrobe and color concepts against past projects")
    repeat.add_argument("project")
    repeat.add_argument("--history", default="look_history.json")
    repeat.add_argument("--register", action="store_true", help="Save project looks to local history only if no repeats")
    demo = sub.add_parser("demo", help="Render a 3-second synthetic end-to-end smoke test")
    demo.add_argument("folder", nargs="?", default="demo_output")
    preflight = sub.add_parser("preflight", help="Technical source and rights-declaration inventory")
    preflight.add_argument("project")
    preflight.add_argument("--out", default="preflight_report")
    continuity = sub.add_parser("continuity", help="Make studio anchor comparison sheets and manual review")
    continuity.add_argument("project")
    continuity.add_argument("--out", default="continuity_review")
    promptcheck = sub.add_parser("prompt-audit", help="Lint model prompts for recurring contradictions")
    promptcheck.add_argument("folder")
    promptcheck.add_argument("--out", default="prompt_audit.json")
    words = sub.add_parser("word-sync", help="Map verified external word timestamps onto shot frames")
    words.add_argument("project")
    words.add_argument("words_json")
    words.add_argument("--out", default="voice_sync")
    audio = sub.add_parser("audio-qc", help="EBU R128 and speech pause audit")
    audio.add_argument("video")
    audio.add_argument("--out", default="audio_report")
    reuse = sub.add_parser("compare-videos", help="Detect near-reused visual states across source or finished reels")
    reuse.add_argument("videos", nargs="+")
    reuse.add_argument("--out", default="reuse_audit")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.cmd == "init":
            dest = Path(args.folder).expanduser().resolve()
            if dest.exists() and any(dest.iterdir()):
                raise ProjectError(f"Folder already contains files: {dest}")
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(EXAMPLES / args.preset / "project.json", dest / "project.json")
            (dest / "assets").mkdir(exist_ok=True)
            print(f"Created {dest}/project.json. Generate the prompts, then populate assets/.")
        elif args.cmd == "validate":
            project = read_project(args.project, require_assets=args.assets)
            shots = schedule(project)
            length = sum(x["frames"] for x in shots) / project["output"]["fps"]
            print(f"PASS: {len(shots)} looks, {length:.2f} seconds, {project['output']['width']}x{project['output']['height']}")
        elif args.cmd == "storyboard":
            print(write_storyboard(read_project(args.project), args.out))
        elif args.cmd == "prompts":
            print(build_prompt_pack(read_project(args.project), args.out))
        elif args.cmd == "render":
            print(render(args.project, args.out, workdir=args.workdir, quick=args.quick))
        elif args.cmd == "qa":
            output = check(args.video, args.out, args.project)
            print(json.dumps({k: output[k] for k in ("status", "failures", "warnings")}, indent=2))
            if output["failures"]: return 2
        elif args.cmd == "analyze":
            for path in args.videos:
                print(json.dumps(inspect_one(path, args.out, args.frames), indent=2))
        elif args.cmd == "repeats":
            print(json.dumps(review(read_project(args.project), args.history, args.register), indent=2))
        elif args.cmd == "demo":
            print(create_demo(args.folder))
        elif args.cmd == "preflight":
            report = inspect_assets(args.project, args.out)
            print(json.dumps({k: report[k] for k in ("status", "errors", "warnings")}, indent=2))
            if report["errors"]: return 2
        elif args.cmd == "continuity":
            report = compare_project(args.project, args.out)
            print(json.dumps({"contact_sheet": report["contact_sheet"],
                              "scenes": len(report["scene_diagnostics"])}, indent=2))
        elif args.cmd == "prompt-audit":
            report = audit_folder(args.folder, args.out)
            print(json.dumps({k: report[k] for k in ("files", "issues")}, indent=2))
            if report["issues"]: return 2
        elif args.cmd == "word-sync":
            report = make_sync_map(args.project, args.words_json, args.out)
            print(json.dumps({"segments": len(report["segments"]),
                              "warnings": report["warnings"]}, indent=2))
        elif args.cmd == "audio-qc":
            report = audio_report(args.video, args.out)
            print(json.dumps(report, indent=2))
        elif args.cmd == "compare-videos":
            report = audit_videos(args.videos, args.out)
            print(json.dumps({"videos": report["videos"], "pairs": len(report["pairs"])}, indent=2))
    except (ProjectError, ToolError, FileNotFoundError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0
