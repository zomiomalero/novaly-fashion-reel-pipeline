# Novaly — Share with any AI assistant

**Repository:** https://github.com/zomiomalero/novaly-fashion-reel-pipeline

This public repository contains the V2 source code, seven complete example production plans, shot prompt packs, eight research chapters, 48 original textile/material studies, eight technical diagrams, a reusable skill and automated tests. The private contact sheets and frames derived from seven third-party study videos are deliberately **not** public.

## Copy-and-paste request for Claude, ChatGPT, Cursor, Codex or another AI

> Analyze this repository completely: https://github.com/zomiomalero/novaly-fashion-reel-pipeline. Start with `AGENTS.md`, `SKILL.md` and `README.md`, then read `docs/PROJECT_SCHEMA.md`, `docs/VISUAL_STYLE_BIBLE.md`, and relevant `research/` reports. Use its existing Python/FFmpeg pipeline. For my fashion concept, produce an original consistent adult cast and locked studio plan, outfit-by-outfit script/storyboard, precise shot durations, first-frame/video generation prompts, an asset checklist and a final QA process. If source clips are available, help assemble and test the reel. Do not assume this repository generates photorealistic human clips without an external AI generator. Respect private reference-video and copyright restrictions. Validate project JSONs and run regression tests after code changes.

## Source layout

- `AGENTS.md`: portable agent instructions.
- `SKILL.md`: complete production workflow.
- `CLAUDE.md`: Claude-specific agent notes.
- `README.md`: installation and CLI usage.
- `docs/` + `research/`: workflow, measurements and engineering design.
- `examples/`: seven complete editable storyboard/project/prompt starter sets.
- `src/fashionreel/`: executable prompt, edit, audio and QA engine.
- `assets/`: original illustrative technical/material research.
- `tests/` and `.github/workflows/ci.yml`: verification.

## Setup

```bash
git clone https://github.com/zomiomalero/novaly-fashion-reel-pipeline.git
cd novaly-fashion-reel-pipeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
fashionreel validate examples/color-pair-looks/project.json
```

Python 3.10+, FFmpeg and ffprobe are required to render videos. The production pipeline accepts original imagery/video from separate generation tools. If an AI application cannot read a GitHub URL directly, give it GitHub's **Code > Download ZIP** file instead.
