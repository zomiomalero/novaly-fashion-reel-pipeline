# AGENTS.md — Instructions for AI coding and production assistants

This is the entrypoint for AI agents working with **Novaly Fashion Reel Pipeline**. Read this document, then `SKILL.md`, `README.md`, `docs/PROJECT_SCHEMA.md`, `docs/VISUAL_STYLE_BIBLE.md`, and the relevant `research/` chapter before changing code or producing a fashion video.

## Scope and capabilities

The repository prepares original 9:16 photorealistic fashion reel projects: JSON plans, storyboards, shot-level generation prompts, FFmpeg assembly of approved clips, overlays, voice/music mixing and QA. The local code does **not** generate photorealistic people or clothing video by itself; that requires a separate external video model and user-provided source media. The synthetic demo tests only the technical workflow.

## Project architecture

- `src/fashionreel/cli.py`: source of truth for CLI subcommands and accepted flags.
- `src/fashionreel/config.py`: schema validation and exact scene timing.
- `src/fashionreel/prompts.py`, `prompt_audit.py`: per-look generation prompts and checks.
- `src/fashionreel/storyboard.py`: editorial structure.
- `src/fashionreel/render.py`, `media.py`, `overlays.py`: FFmpeg assembly and graphics.
- `src/fashionreel/qa.py`, `audio_qc.py`, `preflight.py`, `continuity.py`: validation tools.
- `src/fashionreel/repeat_guard.py`, `reuse_audit.py`: duplication heuristics.
- `src/fashionreel/word_timing.py`: mapping human-corrected word timestamps to frames.
- `examples/`: seven production examples with `project.json`, storyboards and prompt packs.
- `docs/`, `research/`: research and operating instructions.
- `assets/`: original procedural material-study imagery and technical diagrams, not real studio model photos.
- `.github/workflows/ci.yml` and `tests/`: regression checks.

## Quick start

Requires Python 3.10+, FFmpeg and ffprobe.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
fashionreel validate examples/color-pair-looks/project.json
fashionreel prompts examples/color-pair-looks/project.json --out /tmp/novaly-prompts
fashionreel storyboard examples/color-pair-looks/project.json --out /tmp/novaly-storyboard.md
fashionreel demo /tmp/novaly-demo
```

## Production contract

1. Use the existing production framework and example schema, not a rewritten editor.
2. Define an original, recurring **adult** cast and fixed studio: camera, crop, floor marks, light, backdrop, hair, face, proportions and garment detail should remain consistent across the series.
3. Prepare a distinct first-frame outfit image for each look; use image-to-video generation with the same original cast/studio references. Clothing changes between clips, never morphs inside clips.
4. Prefer small natural gestures, breathing, fabric movement and restrained camera work; keep complete bodies and outfit colors legible.
5. Place color labels/swatches in editing, not inside the AI video generation prompt.
6. Keep user-provided references and recognizable original creators' likenesses private. Do not reproduce reference clips, proprietary soundtracks or presenter identities.
7. When clips are ready, execute `fashionreel validate --assets`, `preflight`, `continuity`, `render`, `qa` and `audio-qc` using the command forms in README. Always manually check fingers, faces, clothing, footwear, timing and licensing.
8. If original generated clips are missing, deliver the production plan, prompts, storyboard, shot timing and exact missing-asset checklist. Do not present a synthetic demo as the final reel.
9. Run `python -m unittest discover -s tests -v` after code changes; validate all changed example projects.
10. On low-storage Mac computers, put media assets, outputs and temporary render files on an external SSD (see `docs/MAC_EXTERNAL_SSD.md`).

## Public repository restrictions

Do not commit uploaded reference videos, screenshots/contact sheets derived from them, user production media, private faces, paid music, API keys, credentials or output renders. `private_reference_lab/` is intentionally absent from the public repo. `assets/original-material-studies/` and `assets/technical-plates/` contain original design studies and can remain public. Follow `.gitignore` and review staged changes before any push.

Use standard git commit/push/PR commands for future updates. `scripts/publish_to_github.sh` is meant for **initial repository creation**, not for updating an existing repository.

## Definition of done

Project JSON validates; generated or supplied clips have source/rights checks; technical video and audio checks run; human continuity review passes; all relevant tests pass; the final status accurately distinguishes locally automated steps from external AI generation and manual approvals. No system can guarantee virality.
