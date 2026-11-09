# NOVALY Fashion Reel Production Pipeline

**A runnable, local-first production system for original 9:16 photorealistic fashion styling shorts.**

This project was engineered from two separate analyses:
1. A file-by-file architectural review of [MSLIKTT/claude-animated-shorts](https://github.com/MSLIKTT/claude-animated-shorts), especially its timeline, shot planning, sound ducking, and technical QA.
2. Seven user-provided vertical fashion references, measured at 24/30 fps with fixed-camera model pairings, outfit hard cuts, clothing labels, restrained performance, and average audio loudness near -16 LUFS.

The reference repository is a **cartoon Remotion/three.js template**; this repository is a **new, original fashion production pipeline**, not a copy of its cartoon renderer. Our core uses Python, Pillow, and FFmpeg so rendered clips can stay photorealistic. The samples are creative examples, not claims about fashion rules or references to real personalities.

## V2: full research-grade release

The previous release ZIP was 101 KB because it packaged compressed code and text but **no substantial visual study assets**. That was inadequate for a benchmark against an 18 MB, asset-heavy source repository. V2 adds meaningful visual and technical depth:

- **Private, local reference lab:** 4,776 native decoded frames measured, 33 visual chronology sheets (10 fps), 98 540×960 keyframes, seven per-video signal plots, CSVs and study guides. Available **only in the full offline bundle**, not in the public GitHub repository.
- **Original, redistributable visual materials:** 48 procedurally generated textile/color/lighting studies (1024×1024), eight technical diagram plates (1080×1920), their source-generation scripts and manifest. These are diagram/texture studies, not footage or likenesses.
- **More engineering modules:** `preflight.py`, `continuity.py`, `prompt_audit.py`, `word_timing.py`, `audio_qc.py`, `reuse_audit.py` plus a cross-video visual similarity matrix.
- **Deeper editorial and technical research:** eight additional chapters in `research/`, a source-module porting map, and an explicitly limited near-duplicate-reference analysis.
- **Seven editable production examples:** color pairs, denim styling, autumn capsule, smart office outfits, one blazer six ways, denim color matching and travel capsule. Each includes output-ready prompt files and a frame-based storyboard.
- **Expanded regressions:** technical and prompt unit tests plus an end-to-end FFmpeg smoke render. CI runs without requiring copyrighted reference media.

**Two deliberately different archives** are supplied: a GitHub-safe public edition (original source/assets only) and a full offline research edition (plus a private reference folder). Do not publish the private folder. File size is an output of real materials, not a quality guarantee.

## What this actually does

| Phase | Deliverable | Automated? |
|---|---|---|
| Preproduction | Project JSON, exact frame schedule, storyboard, human checklists | Yes |
| Generative prep | Independent per-look image-to-video prompts with identity, camera, studio and outfit locks | Yes |
| AI video generation | Original models/clothing moving in your chosen tool (Seedance, Dola, etc.) | **External model; you provide clips** |
| Assembly | Trims, freezes too-short videos with a warning, scales/crops to 9:16, hard cuts, adds swatches/labels | Yes |
| Audio | Voice, music, voice-triggered music ducking, -16 LUFS target and AAC encoding | Yes, when tracks provided |
| QA | Frame count, dimensions, fps, black/white frames, freezes, candidate cuts, loudness | Yes |
| Editorial sign-off | Visual identity, hands, hair, wardrobe continuity, license checks and voice sync | Human required |
| Reuse guard | Checks wardrobe concepts and 1 fps near-matching video states | Yes (heuristic) |
| Source preflight | Verifies file hashes, length, aspect, upscaling, and manual rights declarations | Yes (technical) |
| Studio continuity | Creates model-size contact sheet and restricted background-region similarity checks | Yes (heuristic) |
| Prompt audit | Flags wardrobe morphing, durations in video prompts, and missing continuity anchors | Yes (heuristic) |
| Word sync | Maps externally corrected word timings to frame-accurate looks | Yes (after supplying timings) |

No cloud uploads, paid APIs, face cloning, reference-video reposting, or generated model subscriptions are required to run the CLI. A separate image/video generator is required if you want newly created photorealistic people and clothes.

## Fastest start (Mac, Linux, Windows with Python)

Requires Python 3.10+, FFmpeg/ffprobe on PATH, and Pillow and NumPy.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
fashionreel validate examples/color-pair-looks/project.json
fashionreel prompts examples/color-pair-looks/project.json --out /tmp/novaly-prompt-pack
fashionreel storyboard examples/color-pair-looks/project.json --out /tmp/novaly-storyboard.md
fashionreel demo /tmp/novaly-demo
fashionreel qa /tmp/novaly-demo/demo.mp4 --project /tmp/novaly-demo/project.json --out /tmp/novaly-demo/qa
```

The `demo` command uses **simple synthetic drawings** to test all video plumbing. It is deliberately **not** a purported photorealistic finished short. It creates a playable 3-second MP4.

### Produce a real fashion reel

```bash
fashionreel init /path/to/my-reel --preset color-pair-looks
fashionreel prompts /path/to/my-reel/project.json --out /path/to/my-reel/prompts
fashionreel storyboard /path/to/my-reel/project.json --out /path/to/my-reel/STORYBOARD.md
```

Create your own original **character identity sheets**, a clean **studio master frame**, and each look's **first-frame outfit image** in the chosen image generator. Then generate one *short, subtle-motion* video per look with the corresponding prompt. Use the model/reference sheets for every shot. Put these files in `assets/`, with names exactly matching `project.json`.

Optionally create narration and background music using your preferred TTS/composition tool. Put them under `assets/`, then edit `audio.voice` and `audio.music` paths in `project.json`. License any music you use.

```bash
fashionreel validate /path/to/my-reel/project.json --assets
fashionreel render /path/to/my-reel/project.json --out /path/to/my-reel/final.mp4 --workdir /path/to/fast-ssd/tmp
fashionreel qa /path/to/my-reel/final.mp4 --project /path/to/my-reel/project.json --out /path/to/my-reel/qa
```

The output is a constant-frame-rate, 1080x1920 H.264 MP4 (default 30 fps), with reliably rendered swatches and optional small emphasis text. The output `.mp4` and `_manifest.json` are reproducible from the same inputs/config.

## The production recipe from the seven references

1. **No elaborate intro**: a short, useful one-line hook begins immediately. The 21-29 s references largely open with "remember..." and show the models at once.
2. **Single controlled studio**: one original female and one original male adult presenter, stable floor marks, lighting and lens for the whole series. One reference features two women; this pipeline can be adapted by changing the cast descriptions.
3. **Hard cuts are intentional wardrobe changes**, not in-shot morphs. Usually 8-10 looks in 21-29 s, approximately 2-3 s per look after the opener. The denim example has six longer looks.
4. **Meaningful pose motion, not artificial camera motion**: small hand gestures, a glance, small weight shift, subtle cloth movement and breathing. Keep both complete bodies in shot.
5. **Add color chips and text in post**: generators are not good typographic compositors. This keeps swatches accurate and editable.
6. **Voice and music mix consistently**: speech remains intelligible; -16 LUFS target. The default mixer ducks music during speech.
7. **Check identity and garment correctness manually**; numerical frame QA cannot reliably verify human faces or true fabric/color consistency.

## Extended V2 production commands

```bash
# Seven presets are now available
fashionreel init /Volumes/FAST_SSD/novaly-reel --preset autumn-capsule
fashionreel validate /Volumes/FAST_SSD/novaly-reel/project.json
fashionreel prompts /Volumes/FAST_SSD/novaly-reel/project.json --out /Volumes/FAST_SSD/novaly-reel/prompts
fashionreel prompt-audit /Volumes/FAST_SSD/novaly-reel/prompts

# After generating/finding approved source clips
fashionreel preflight /Volumes/FAST_SSD/novaly-reel/project.json --out /Volumes/FAST_SSD/novaly-reel/preflight
fashionreel continuity /Volumes/FAST_SSD/novaly-reel/project.json --out /Volumes/FAST_SSD/novaly-reel/continuity
fashionreel render /Volumes/FAST_SSD/novaly-reel/project.json --out /Volumes/FAST_SSD/novaly-reel/final.mp4 --workdir /Volumes/FAST_SSD/novaly-tmp
fashionreel qa /Volumes/FAST_SSD/novaly-reel/final.mp4 --project /Volumes/FAST_SSD/novaly-reel/project.json --out /Volumes/FAST_SSD/novaly-reel/qa
fashionreel audio-qc /Volumes/FAST_SSD/novaly-reel/final.mp4 --out /Volumes/FAST_SSD/novaly-reel/audio_qc

# Optional: only if word-aligned JSON exists (external aligner + human correction)
fashionreel word-sync /Volumes/FAST_SSD/novaly-reel/project.json words.json --out /Volumes/FAST_SSD/novaly-reel/voice_sync
# Optional: near-repeat audit of YOUR OWN finished video files
fashionreel compare-videos reel-a.mp4 reel-b.mp4 --out /Volumes/FAST_SSD/novaly-reel/visual_reuse
```

The privacy distinction is important: `research/reuse/REUSE_AUDIT.md` has numeric comparisons only; the `private_reference_lab/` files in the full offline ZIP contain third-party frame excerpts for local study and must **not** be published.

## CLI reference

```text
fashionreel init DIR --preset color-pair-looks|jeans-styling
fashionreel validate PROJECT [--assets]
fashionreel prompts PROJECT --out PROMPTS_DIR
fashionreel storyboard PROJECT --out FILE.md
fashionreel repeats PROJECT --history HISTORY.json [--register]
fashionreel render PROJECT --out FINAL.mp4 [--workdir SSD_TMP] [--quick]
fashionreel qa FINAL.mp4 [--project PROJECT] --out QA_DIR
fashionreel analyze input1.mp4 input2.mp4 --out REFERENCE_DIR [--frames 12]
fashionreel demo DEMO_DIR
fashionreel preflight PROJECT --out DIR
fashionreel continuity PROJECT --out DIR
fashionreel prompt-audit PROMPT_DIR --out REPORT.json
fashionreel word-sync PROJECT WORDS.json --out DIR
fashionreel audio-qc VIDEO --out DIR
fashionreel compare-videos A.mp4 B.mp4 --out DIR
```

`--quick` is for fast previews only; do not publish its reduced quality. The look history is only saved when `--register` is explicitly passed; the script never silently mutates the database. `analyze` remains offline and puts contact sheets in the directory you specify.

## Project structure

```text
src/fashionreel/
  cli.py           commands
  config.py        schema, validation, accurate frame schedule
  prompts.py       model-neutral prompt pack; identity and set locks
  storyboard.py    shoot plan and final human QC sheet
  overlays.py      original color-chip and text graphics
  render.py        normalize, concatenate, add optional mixed audio
  qa.py            full-frame and loudness checks
  analyzer.py      offline contact sheets for provided references
  repeat_guard.py  optional look-history detection
  demo.py          self-contained synthetic FFmpeg smoke test
  preflight.py     source hashes, availability, resolution, rights-declaration review
  continuity.py    background anchor comparison and source-frame grid
  prompt_audit.py  generation text consistency checks
  word_timing.py   verified word timestamps -> frame-accurate look map
  audio_qc.py      EBU R128 levels, true peak, long audio silence report
  reuse_audit.py   cross-video near-matching visual frames
examples/
  color-pair-looks/project.json  10 looks / 27 s
  jeans-styling/project.json     6 looks / 20.4 s
  autumn-capsule/project.json    8 looks
  office-casual/project.json     8 looks
  one-blazer-six-ways/project.json  6 looks
  denim-color-matching/project.json  8 looks
  weekend-travel-capsule/project.json  7 looks
docs/
  SOURCE_REPOSITORY_AUDIT.md
  SEVEN_VIDEO_ANALYSIS.md
  VISUAL_STYLE_BIBLE.md
  GENERATION_AND_EDIT_WORKFLOW.md
  QUALITY_GATES.md
  MAC_EXTERNAL_SSD.md
  PROJECT_SCHEMA.md
research/
  01_REFERENCE_TIMING_AND_RHYTHM.md to 08_ORIGINAL_REPO_PORTING_MAP.md
  reuse/REUSE_AUDIT.md        seven-video near-repeat matrix; no images
assets/
  original-material-studies/  48 original 1024x1024 study textures
  technical-plates/          eight original 1080x1920 workflow diagrams
private_reference_lab/        FULL OFFLINE PACK ONLY; NEVER PUBLISH
SKILL.md             Claude Code/ChatGPT workflow
scripts/publish_to_github.sh
.github/workflows/ci.yml
```

## Important production boundaries

- **No copying real faces or recreating a real channel's videos.** Use the references for general format and visual techniques; make new original cast, outfits, branding, scripts and studio assets. Keep reference video files private and out of the GitHub repository.
- **This does not automatically generate photorealistic source footage** or word-level ASR transcripts. It prepares prompts and handles assembly/QA after you supply generated footage.
- Automated QA validates video mechanics; it cannot promise viral performance, copyright clearance, social-platform approval, plausible hands, or perfect identity.
- Asset inputs can be PNG/JPEG/WebP or MP4/MOV. Video inputs that are shorter than the requested duration are padded by holding their final frame **with a warning**, rather than silently changing the storyboard timing.
- For the source project's license and file-level assessment, read [SOURCE_REPOSITORY_AUDIT.md](docs/SOURCE_REPOSITORY_AUDIT.md).

## Test / GitHub publication

```bash
python -m unittest discover -s tests -v
# After installing and authorizing the GitHub CLI:
./scripts/publish_to_github.sh novaly-fashion-reel-pipeline zomiomalero
```

The publication helper creates a **public** repository by default, blocks private reference folders and video/audio sources, and allows only reviewed, original image assets from the two declared `assets/` study folders. The public-ready archive contains original procedural textures and diagrams, but **does not** include third-party reference frames, finished clips, personal identity photos or API secrets. GitHub Actions runs schema validation and the end-to-end FFmpeg smoke test on pushes and pull requests.

## Attribution

Original implementation, examples and documentation: 2026 Novaly Studio, MIT license. Source architecture study: [MSLIKTT/claude-animated-shorts](https://github.com/MSLIKTT/claude-animated-shorts), MIT. No code or reference frames from that repository are vendored here.
