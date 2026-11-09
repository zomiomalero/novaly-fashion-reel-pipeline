# 06 / Edit implementation, deterministic export and failure recovery

## What the editing engine actually does

The engine is a reproducible local FFmpeg compositor. It does not synthesize photorealistic people, voice models, or garment change videos. Its contract is to accept already-approved source shots and audio, enforce a frame-level schedule, add editable graphics, and deliver a valid encoded master plus machine-checkable manifest.

### Scene graph

`project.json` → `read_project` (validate all fields) → `schedule` (integer frames) → one normalized, overlayed H.264 clip per look → FFconcat copy → source-independent audio mix → final MP4 → manifest and QA.

Each scene's image or video starts from a separate source. For stills, FFmpeg creates a looping picture track; for footage it decodes from the configured `start` time. `vf()` scales/pads or scales/crops to exactly 9:16, normalizes frame rate, clones the terminal frame only if necessary, trims to exact frame count and resets PTS. A transparent overlay PNG is created per look with text and swatches. Each scene is compressed independently with consistent dimensions/fps/codec so concatenation can use stream copy.

This is deliberately **less complex than a programmable Three.js/Remotion scene graph** because the critical fashion content is realistic human footage from an external generator. Keeping garments and faces in source clips avoids creating faked 3D bodies inside the editor.

## Output presets

| Preset | Dimensions | FPS | Purpose | Suggested CRF |
|---|---|---:|---|---:|
| Technical smoke | 360×640 | 24–30 | Confirm code paths and durations quickly | 24 |
| Editorial draft | 540×960 | 24–30 | Check staging on a phone | 20–24 |
| Production master | 1080×1920 | 30 (or configured 24) | Social export | 16–18 |
| True 2K vertical | 1440×2560 | 30 | Only with sufficiently detailed sources | 16–18 |

A larger pixel count does not recreate details missing from 720×1280 input. A high-resolution export from weak video is mostly upscaling. Check source material before changing from 1080×1920 to 1440×2560. 9:16 dimensions must be even for 4:2:0 H.264 encoding.

## Temporary disk and Mac external SSD

The production work directory is always configurable. On a constrained internal Mac, keep the repository, generated source clips, render intermediates and reference lab on a fast external SSD; pass `--workdir /Volumes/YOUR_SSD/novaly-temp` to `render`. TemporaryDirectory writes only to a newly created child directory and deletes that owned work directory on completion; it does NOT issue a broad `rm` against your drive. Do not pass the system root or an unrelated shared temp folder expecting cleanup of old files.

The original cartoon repo notes Remotion bundle folders and public assets occupying dozens of GB on the system volume. This adapted editor avoids the repeated bundling pattern; every source re-render still consumes CPU, scratch space and decoding time, so manage master/video caches deliberately.

## Audio and video stream mapping

Render first without audio to simplify deterministic source selection. Then use an explicit input mapping:

- Video: `-map 0:v:0`; copy the silent master H.264 stream.
- Audio: `-map [a]`; encode a clean 48 kHz AAC stereo track from independent voice/music inputs.
- Duration: `-t` is the exact sum of scheduled frame durations, not the input WAV or MP4 duration.
- `+faststart` moves MP4 index information to improve playback initialization.

### Known failure modes

**Frozen frame at look end:** source video is shorter than scheduled. `preflight` warns and the editor pads by cloning. Correct this by generating longer footage or shortening the planned look. The pad is a fallback, NOT a true animation feature.

**Audio outlasts picture:** verify that audio filters pad/trim to picture duration, and run word-sync to ensure the last spoken word ends before cut.

**Source colors shift under overlaid graphics:** labels should be independent RGBA images; do not burn them into the generator's source. Preserve original sRGB color intention as far as encoder pipeline allows; do not infer physical garment reflectance from compressed output.

**Different model scale across scenes:** the renderer cannot repair the hallucinated height difference without manual recropping. Resolve at source generation and inspect midpoint contact sheets. Avoid artificial per-shot zoom correction that changes comparison scale.

**Unsupported codec/format:** `ffprobe` and preflight show source codecs. Transcode clips to a supported format if necessary; do not silently skip corrupted inputs.

**Platform crop / social UI:** render safe-area plates and view the actual app preview rather than assuming all interfaces reserve the same margins.

## Reproducible render record

The render writes `final_manifest.json` including project details, exact frame timeline, expected duration and actual probed media metadata. `preflight` records SHA-256 of source assets and source technical properties in `preflight.json`, so later changes to a source clip are detectable. To reproduce an export, save the complete project JSON, original approved media, audio sources, version of the editor and actual render command. Do not commit real cast source images/voices publicly by default.
