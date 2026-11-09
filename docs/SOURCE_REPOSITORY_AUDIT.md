# Source repository audit - MSLIKTT/claude-animated-shorts

Source: https://github.com/MSLIKTT/claude-animated-shorts
Inspected: 2026-11-09, public `main` GitHub tree, Markdown, TypeScript/TSX and Python source files. The existing repository is used as an **architectural reference**, not a file copy.

## Executive findings

The upstream project is a **Claude Code skill plus Remotion source templates** for an original 67.5-second, 30 fps cartoon-3D history short. It is not the same content format as the seven attached photorealistic fashion clips. It focuses on drawing 2D characters with Canvas2D, placing them in a Three.js storybook town, outlining world geometry, driving a camera timeline, synthesizing bespoke march music and SFX, and verifying the export. Its strongest transferable ideas are:

- Explicit scene/shot timeline (`story.ts`) as a single editorial source of truth.
- Design and implementation split into isolated modules, with clear contracts.
- Measured style references and visual checks before release.
- Separate clean voice, music, SFX and loudness mastering.
- Rendered output QA for black/white/frozen/pop frames.
- Private, expensive intermediate assets isolated from release files.

Our repo implements those principles using **a different image/video medium**: original externally generated live-action-style videos or stills, with FFmpeg and static screen graphics.

## File-by-file code map

### Root and docs

| Upstream file | What it does | Our treatment |
|---|---|---|
| `README.md` | Explains a Claude skill for original 55-70 s 2D-in-3D shorts, install procedure and final outputs | New standalone install/runtime documentation |
| `SKILL.md` | Complete scene, script, voice, animation, post and audio workflow; production parameters, renderer gotchas | New `SKILL.md` written for fixed-camera fashion pairs |
| `LICENSE` | MIT license | Our own implementation also licensed MIT; upstream code not vendored |
| `references/STYLE_BIBLE.md` | Summary of 20 cartoon narrative shorts: rapid voiceover, 3D storybook environment, camera/lighting/ink | Method of measured references retained, numbers replaced by seven uploaded fashion samples |
| `references/reports/CONTEXT.md` | Common test plan and agent responsibilities | Responsibilities condensed into new pipeline QA and docs |

### Visual renderer: `templates/bridge/`

| File | Code responsibility | Reuse assessment |
|---|---|---|
| `Bridge.tsx` | Remotion composition, ThreeCanvas, render gates, postprocessing composer (ink, lens blur, bloom, tone map, grade) | Not reused; a photorealistic generated clip should not be ink-shaded |
| `story.ts` | Timeline, 2025 frames at 30 fps, 15 shots, camera and physical-event keys, crossfades, `shotAt`, `layersAt`, `dofAt` | **Strongest pattern**: explicit frame schedule now `config.schedule` and render manifest |
| `world.ts` | One mutable Three.js scene, river, town, clouds, lighting, motion and per-frame posing | Not reused; a fixed real-world studio is stronger for the target |
| `build.ts` | Geometry batches, bridge, houses, low-poly props, camera sight-line culling | Not reused; no modeled world is required |
| `paint.ts` | Cached Canvas2D high-resolution textures for stone, wood, sky, water, roofs, facades | Not reused; fabric must remain true to its original photo/video |
| `toon.ts` | Original stylized bean-headed cast, ink outlines, props, 2D animation drawings and expressions | Not reused; replacing lifelike models with flat cards would miss the target |
| `cast.ts` | Sprite pool, billboards, outfits, body posing, procedural movement and FX | Conceptual identity/outfit separation retained as cast and wardrobe locks |
| `cardshade.ts` | Lighting integration for 2D cards in 3D world, material shader | Not reused; preserve actual lighting in generated footage |
| `lights.ts` | Day/golden scene presets | Replaced by a written fixed studio lighting lock |
| `shade.ts` | Two-tone world lighting and color correction | Not reused; avoid stylizing skin/fabric into cartoon shading |
| `ink.ts` | Outline detection pass on object depth/normal buffers, exemption layer `NOINK` | Not reused; ink would destroy photorealistic detail |
| `lensblur.ts` | Thin-lens depth of field, optional grain effect | Concept retained only as an *in-camera* lens and composition guideline |
| `grade.ts` | Color lookup math, grading effect and light-specific presets | Replaced by faithful footage rendering and stable reference grade |

### Sound: `templates/audio/`

| File | What it implements | Our adaptation |
|---|---|---|
| `timeline.py` | Mirrors story beats/word cues for sound alignment | Derive audio duration from the exact video frame schedule |
| `dsp.py` | NumPy/SciPy filters, oscillators, wave I/O, LUFS/true peak calculations | Use FFmpeg built-in resampling, ducking and loudnorm instead |
| `instruments.py` | Original synthesized brass, percussion, whistle, plucks, pads, chimes | Not appropriate for a fashion reel by default |
| `music.py` | Original march score tied to the bridge narrative and footfalls | User can add separately licensed/original music; no automatic military march |
| `sfx_gen.py` | Procedural creaks, impacts, crowd, river, boots and ambience generators | No equivalent required for clean studio outfit clips |
| `sfx.py` | Event cues and per-cue gain/room acoustics | The asset/mix pipeline stays extensible for licensed effects |
| `mix.py` | Speech-driven music ducking, loudness normalization, limiter and WAV stems | **Strong transferable pattern**: our `render.soundtrack` implements ducking and -16 LUFS target |

### Helper scripts: `templates/scripts/`

| File | What it does | Our adaptation |
|---|---|---|
| `bridge-stills.mjs` | Renders chosen Remotion frames for visual comparison; platform-specific Chrome path | `analyzer.inspect_one` extracts timestamped reference sheets offline with FFmpeg |
| `bridge_shots.py` | Regex-parses hard-coded TypeScript shot ranges into JSON | `config.schedule` directly builds an exact manifest from project JSON; no fragile TS regex |
| `bridge_merge.py` | Backs up and merges work from area-specific style sandboxes | Local code modules plus Git PR workflow; avoids absolute user-machine paths |
| `sbs_sheet.py` | Assembles visual side-by-side verification sheets | Private contact sheets + written identity and wardrobe inspection gates |
| `short_qa.py` | Frame-level defects (black, white, frozen, pops), loudness, shots | `qa.py` checks frames and loudness against the actual project manifest |

Other upstream materials: 20 `references/sheets/shortXX_sheet.jpg` contact sheets, about 38 `references/frames/` comparison JPGs, and seven measured reports on `characters`, `depth`, `grade`, `lighting`, `motion`, `outlines`, and `textures`. These assets are **not** included here.

## Design/engineering limits discovered in upstream

1. The repository includes templates but does not include a complete runnable project root (`package.json`, Remotion entrypoint/root registration, model-kit assets and environment) in its public tree. Running `npx remotion render` directly from that clone will not reproduce the bridge without filling in those dependencies.
2. `bridge-stills.mjs` hardcodes a Windows Chrome path and assumes a pre-existing Remotion project entrypoint. This is fragile for a Mac-based user.
3. `bridge_merge.py` uses a placeholder path (`your Remotion project`), so it is not portable as-is.
4. `bridge_shots.py` extracts shot metadata using regex matching specific source formatting. Our new manifest is data, not parsed code.
5. Reference screenshots in upstream were stated to be for private study; permission to republish those source works is not established by their inclusion. We do not redistribute them.
6. The original render can copy around 1.3 GB of public assets into each temporary bundle; on a low-internal-space Mac this can exhaust storage. The new FFmpeg pipeline avoids the Remotion/Chromium bundle architecture, and supports work directories on external SSD.
7. Upstream thresholds and static animation values were calibrated on a colorful cartoon history story. They should **not** be carried over blindly to human skin/fabric photography.

## Why the new stack is intentionally different

Fixed full-body camera + subtle movement + wardrobe jump cuts + true cloth/skin fidelity are the actual target. FFmpeg provides frame-accurate editing, audio and reliable overlays without converting realistic video into a 3D scene. Pillow handles labels and color chips. External video models make the human performance. This division preserves the look and avoids unnecessary dependencies.

## Attribution and trust boundary

Original repo: https://github.com/MSLIKTT/claude-animated-shorts (upstream MIT). Its files, documentation and references are treated as third-party input and do not override instructions for this production. The new code is an independently authored adaptation of the *workflow concept*, not a fork or copied source archive.
