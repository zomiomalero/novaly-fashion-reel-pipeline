# 08 / Source-repository technical port map

The audited public repository is [`MSLIKTT/claude-animated-shorts`](https://github.com/MSLIKTT/claude-animated-shorts), default branch `main` at the time of inspection (2026-11-09). It has a very different aesthetic target: a historical cartoon short with flat 2D actors embedded in a rendered 3D town. The correct adaptation is to carry over robust production engineering, not literally copy the fictional soldiers, bridge scene, historical script or original reference images.

| Original repository module | Responsibilities inspected | Novaly adaptation | Porting decision |
|---|---|---|---|
| `SKILL.md` | Full ordered workflow, visual criteria, source verification | `SKILL.md`, docs + research chapter navigation | Adapt the workflow structure |
| `templates/bridge/story.ts` | Shot definitions, integer frames, cameras, impacts, DOF | `config.schedule`, `word_timing` | Retain deterministic frame scheduling; discard camera kicks |
| `templates/bridge/Bridge.tsx` | Remotion composition, scene, compositing passes | `render.py` FFmpeg engine | Replace renderer for photographic footage |
| `templates/bridge/world.ts` | Procedural bridge, banks, sky, fog, geometry | Original locked studio master first frame | Do not recreate a stylized 3D city |
| `templates/bridge/build.ts` | Scene prop geometry, object batching, occlusion | Physical studio landmarks and anchor QC | Retain consistent location thinking only |
| `templates/bridge/paint.ts` | Canvas2D painted procedural surfaces | Original materials study library | Recreate original procedural *fabric* studies, not copied textures |
| `templates/bridge/toon.ts` | Cartoon Pen API, bean-head faces, wardrobe uniforms | Original photographic actor identity sheets | Do not port cartoon anatomy |
| `templates/bridge/cast.ts` | Camera-facing cards, crowd animation, blinks | External image-to-video with actor reference anchors | Do not port flat billboards |
| `templates/bridge/cardshade.ts` | Light-responsive shading on 2D cards | Prompt and review for photographic light | Do not use shaders that make people look pasted on |
| `templates/bridge/lights.ts` | Key/fill and scene lighting presets | Locked studio lighting script in project JSON | Retain fixed lighting contract |
| `templates/bridge/shade.ts` | Custom two-tone Lambert shading | Realistic source light and cloth folds | Avoid cartoon two-tone lighting |
| `templates/bridge/ink.ts` | Edge/normal/depth outline post effect | None for photo footage | Deliberately exclude ink shader |
| `templates/bridge/lensblur.ts` | Defocused backgrounds, DOF | Keep modest natural photographic separation | Do not blur garment information |
| `templates/bridge/grade.ts` | LUT-like grading and tone control | Color/material documentation and editor post-processing | Adapt color QA, not literal grade curves |
| `templates/audio/timeline.py` | Shared frame-accurate cue/time constants | Scene schedule and verified word-sync | Retain synchronized time authority |
| `templates/audio/dsp.py` | Signal processing helpers | FFmpeg resampling/mastering + `audio_qc.py` | Use robust FFmpeg rather than copying DSP |
| `templates/audio/music.py` | Original comedic march music | Original licensed instrumental bed | Entirely new music identity |
| `templates/audio/instruments.py` | Procedural music synthesis | Optional external licensed score | Do not port marching arrangement |
| `templates/audio/sfx_gen.py` | Synthesized crowd, chain and water sounds | Optional micro-accent cues, not necessary | Exclude irrelevant historical sound effects |
| `templates/audio/mix.py` | Voice duck, stems, loudness target, peaks | `render.soundtrack`, `audio_qc.audio_report` | Retain voice-first mix and objective QA |
| `templates/scripts/short_qa.py` | Frame-by-frame black/white/frozen/pop detection | `qa.py` | Retain technical QA principles |
| `templates/scripts/bridge-stills.mjs` | Render selected stills | `analyzer.py`, `continuity.py` | Retain still/contact sheet workflow |
| `templates/scripts/sbs_sheet.py` | Side-by-side qualitative check | `continuity.py` contact sheets | Retain comparative look review |
| `templates/scripts/bridge_merge.py` | Owned-file parallel sandbox merge | Conventional Git branches/review, deterministic files | Avoid copying machine-specific paths |
| `references/reports/*` | Seven deep technical areas and measurements | `research/` and private seven-video lab | Retain evidence-first measurement discipline |
| `references/sheets/*` | Twenty 60-frame visual reference sheets | Private 33 10fps chronological sheets | Similar *study depth*, not same source assets |
| `references/frames/*` | Curated source frames | Private 98 larger keyframes | Exclude from public code release |

### Observed weaknesses in the source that should not propagate

- Its still renderer hardcodes a Windows Chrome path (`C:/Program Files/Google/Chrome/...`). The new pipeline is platform-aware using installed FFmpeg and does not assume Windows.
- `bridge_merge.py` uses a placeholder local project root, so it is not a universal turnkey build script. Our scripts calculate paths from the installed package or supplied project file.
- The origin's `short_qa.py` is tailored to the bridge/flash and blends aesthetic metrics with visual anomalies. Our QA explicitly separates technical warnings from artistic approval.
- Source notes record large Remotion bundle temporary directories accumulating on disk. Our pipeline uses an explicitly chosen work folder and scoped TemporaryDirectory cleanup.
- The repo's source imagery is useful for style study but not cleared for redistributing other people's likenesses. Our public archive does not copy its 20 reference sheets or user-provided third-party frames.

### Why a ZIP byte count alone misleads

The source repo's reported GitHub repository size was approximately 17,948 KiB at inspection. Its 20 JPEG contact sheets alone are roughly 0.6–1.1MB each, with dozens of additional JPEG reference frames. The previous Novaly ZIP was mostly text and compressed very efficiently; its 100KB archive did not include comparative visual frames or original visual assets. The v2 deliverables distinguish two needs: a safe-to-publish code repository, and a substantially larger PRIVATE study of provided videos. Neither package is padded with random filler merely to meet a size target.
