---
name: original-fashion-reel-production
description: Produce original photorealistic 9:16 fashion styling shorts with a fixed presenter pair, wardrobe look changes, prompt packs, automated FFmpeg editing, and visual plus technical QC. Use when asked to create a ready-to-produce fashion reel from a set of clothing/colour combinations or to follow the original Novaly reel pipeline.
---

# Original editorial fashion reels

This skill is a workflow runner for the code in this repository. It does not generate new human video footage without an external image/video model. Never imply a generated clip exists before it has been provided and validated.

## Default production contract

- Output 9:16 vertical, 1080x1920, 30 fps, H.264; 24 fps only if user explicitly chooses it.
- Target 20-30 s, about 6-10 looks; first look/hook can be longer.
- Original adults only. Faces, hair, skin texture, body ratios, height difference and proportions locked across every look.
- One fixed full-body front camera, camera height, horizon, studio lighting and environment across every look.
- Use a distinct, original studio design and original scripts and clothing; do not copy any reference person's likeness.
- Generate each outfit as its own short shot, with wardrobe already present in the first frame. Switch looks by a hard cut in editing.
- Use tiny purposeful gestures, natural breathing, authentic hand movement, and subtle weight shifts. Avoid synthetic walking and body morphs.
- Text and swatches are overlays added to the edit, not part of source-generation prompts.
- Voiceover, when present, starts immediately; keep timing close to the beat. Mix at about -16 LUFS with voice intelligibility first.
- Use real technical QA and a human identity/wardrobe continuity review, not only a subjective quality score.

## Steps to perform (in order)

1. Analyze the reference videos or brief. For uploaded clips run `fashionreel analyze <video_paths> --out private-reference-analysis` if paths are available locally. Do not publish their contact sheets.
2. Prepare one concrete 20-30 s idea with a useful hook, list of 6-10 distinct outfit looks, order, color labels and narration. Verify claims where they matter.
3. Create a project JSON from `examples/color-pair-looks/project.json` or `examples/jeans-styling/project.json`. Make wardrobe and gestures precise. Voiceover lines must refer to what is on screen.
4. Make an original female and male model identity sheet (or other user-specified adult cast), then make one *studio master frame*. Both are reused as references on every generation. Do not ask a video model to invent or change an identity per look.
5. Run `fashionreel validate project.json` and `fashionreel prompts project.json --out prompts` and `fashionreel storyboard project.json --out storyboard.md`.
6. For every scene, generate its original outfit first frame. Generate a video from that image plus cast and studio identity refs. The model prompt should contain no numeric duration: set time separately according to the manifest. Do not use a *previous outfit's* final frame as the sole reference for a new outfit.
7. Check source clips one by one: no face drift, extra fingers, wardrobe morphs, frame jumps, disappearing bags, changing shoes, incorrect skin texture or mismatch between colors and color labels.
8. Save clips using manifest names in `assets/`. Add a separately generated/recorded narration WAV and optional licensed music. Prefer voiceover external to model video; clean source clips normally have no baked captions.
9. Run `fashionreel validate project.json --assets` then `fashionreel render project.json --out final.mp4 --workdir <big external SSD dir>`.
10. Run `fashionreel qa final.mp4 --project project.json --out qa`. Inspect QA warnings. Watch final MP4 in a phone-sized player with audio and check every hard cut.
11. Run `fashionreel repeats project.json --history look_history.json` before publishing and `--register` afterward if genuinely new.
12. Deliver the final media, the prompt pack, storyboard and quality report. Do not claim production is complete if assets or generative clips are missing.

## Reference implementation design

- `src/fashionreel/config.py` owns scene start/end frame invariants.
- `prompts.py` owns model-facing shot prompts.
- `overlays.py` owns typography and palette data.
- `render.py` owns FFmpeg clip rendering and audio assembly.
- `qa.py` owns mechanical verification.
- `repeat_guard.py` owns local-only content history.
- `docs/SEVEN_VIDEO_ANALYSIS.md` owns the measurable style observations.

Do not copy the source repository's `toon.ts`, 3D ink shader, marching music and moving camera grammar into a photorealistic fashion reel. They solve a different artistic problem.

## Production honesty

Passing automated QA proves only the properties measured by the script. Human judgement is required for aesthetics, voice sync, facial consistency, leg/hand accuracy, color fidelity, garment texture and copyright/licensing. No tool can guarantee virality.

## V2 research and media inspection extensions

The upgraded package now includes substantive technical and visual references. For every production request, choose only the relevant materials instead of loading all images into context:

- Read `research/01_REFERENCE_TIMING_AND_RHYTHM.md` for picture timing and beat placement.
- Read `research/02_CAMERA_STUDIO_AND_LIGHTING.md` for fixed-camera framing and studio background anchors.
- Read `research/03_CAST_PERFORMANCE_AND_WARDROBE.md` for original cast identity, fabric and movement physics.
- Read `research/04_COLOR_FABRIC_AND_LABELS.md` for chips, denim fit formulas and textile realism.
- Read `research/05_AUDIO_MUSIC_AND_WORD_SYNC.md` for narration, music ducking, true-peak checks and externally corrected word timing.
- Read `research/06_POST_PRODUCTION_AND_EXPORT.md` for the exact FFmpeg edit behavior and SSD work directories.
- Read `research/07_VISUAL_QA_AND_REVIEW_GATES.md` for technical checks versus non-automatable human sign-off.
- Read `research/08_ORIGINAL_REPO_PORTING_MAP.md` for a file-by-file explanation of the upstream cartoon architecture and why parts were adapted or excluded.
- Read `research/reuse/REUSE_AUDIT.md` before treating the seven uploaded references as seven independent styles. Many visual states are closely duplicated/reordered across references 02, 04, 06 and 07.

Use the new commands in this order after clip generation:

```bash
fashionreel prompt-audit prompts-generated/
fashionreel preflight project.json --out preflight
fashionreel continuity project.json --out continuity
fashionreel render project.json --out final.mp4 --workdir /Volumes/FAST_SSD/novaly-tmp
fashionreel qa final.mp4 --project project.json --out qa
fashionreel audio-qc final.mp4 --out audio_qc
```

Optional `word-sync` requires externally obtained and human-checked word timestamps, not guessed speech timings. Optional `compare-videos` is a near-match heuristic and not an originality, ownership or copyright guarantee.

### Asset separation and public publishing

- `assets/original-material-studies/` and `assets/technical-plates/` are original, procedure-generated study art and safe to include in the public code package. They are not photographic model reference images or product photos.
- `private_reference_lab/` exists only in the **full offline study bundle** and contains derived thumbnails from the seven uploaded videos. It must NEVER be pushed to a public GitHub repo, shared as model-training data, or used to clone the original creators' likenesses.
- The public skill edition and public-ready repository exclude the private lab. If this skill is installed on a machine with the private lab absent, perform source analysis only on media the user provides for that specific request.
- Do not claim the GitHub repo is already live unless an authenticated, successful publish operation is confirmed.
