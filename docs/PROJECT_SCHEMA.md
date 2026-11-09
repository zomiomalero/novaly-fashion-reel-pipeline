# Project JSON contract

One project file is the source of truth for all clip timings, outfits, swatches and file paths. Start with either example in `examples/`. Paths are relative to the JSON file unless absolute paths are explicitly used.

## Top-level keys

- `project.title`: nonempty string. `project.brand` (optional): short logo-like text rendered at top-left; keep it empty for no brand.
- `output.width`, `height`: even positive 9:16 canvas, default 1080 and 1920. `fps`: 24, 25, 30 or 60. `crf`: H.264 quality number 10-29, lower is better but larger.
- `cast.woman_identity` and `cast.man_identity`: precise textual locks for your *new original* adult presenters. The field names are placeholders; for different cast arrangements adjust them and `prompts.py` accordingly.
- `studio.description`: exact reusable environment and camera description. Keep it consistent across each scene.
- `audio.voice`: optional WAV/MP3/M4A/etc path; `audio.music`: optional music path. Blank string disables track. `voice_gain_db` defaults to 0; `music_gain_db` to -18; `target_lufs` to -16. Narration is supplied separately, not synthesized by the CLI.
- `scenes`: ordered list, 1-50 items, each with an exact per-look duration.

## Scene properties

| Key | Required | Example | Meaning |
|---|---|---|---|
| `id` | yes | `01_olive_cream` | Unique safe scene identifier |
| `duration` | yes | `2.65` | Seconds, 0.5-8.0; rounded to nearest full output frame |
| `asset` | yes | `assets/01_olive_cream.mp4` | Video or PNG/JPEG/WebP still path |
| `colors` | yes | `[ {"name":"olive","hex":"#4F5B38"} ]` | 1-3 exact label/color objects |
| `title` | no | `Olive and cream` | Written storyboard title |
| `woman_outfit` | recommended | Specific garments, shoes, bag | Passed directly to the woman video prompt |
| `man_outfit` | recommended | Specific garments, shoes | Passed directly to the man video prompt |
| `action` | recommended | One realistic micro-gesture | Used in the model-facing prompt |
| `emphasis` | no | `easy contrast` | One short lower-middle overlay line |
| `formula` | no | `wide-leg jeans + fitted tops` | Top text formula in place of color-chip graphic |
| `start` | no | `0.5` | Seek seconds into a longer input video |
| `fit` | no | `cover` | `cover` crops center to 9:16; `contain` pads |

## Timing invariants

The timeline uses `frames = round(duration * fps)`, and each new clip starts at the previous clip's `end_frame_exclusive`. At 30 fps a 2.65-second scene becomes 80 frames (2.666667s). This guarantees one continuous, gap-free frame schedule. The renderer emits exactly that number of frames for each scene; the concat stage is lossless copy of the normalized intermediates. A manifest accompanies the master.

The expected total runtime is the sum of frame-rounded durations, **not** the sum of unrounded decimal requests. Do not independently recompute cut points in TTS; anchor the narration to the storyboard's actual frame-based timing.

## Asset rules

Accepted visual formats: MP4, MOV, M4V, WebM, MKV, PNG, JPG/JPEG, WebP, TIFF. `render` checks that required files exist. Original clip audio is dropped; use an explicit voiceover and/or soundtrack. If a generated clip is too short, the final frame is held and a warning is printed: re-generate the short clip if this produces an unwanted freeze.

For still images, `render` loops the image for the scene duration. This is a technical option for previews and photographic lookbooks, but it cannot replace natural human video movement where the brief demands live action.

## Audio timing

Music loops until the end of the reel; voice is padded with silence or trimmed to match picture duration. Two tracks use sidechain compression so that music lowers when narration is active. Then FFmpeg normalizes to -16 LUFS, with a -1.5 dBTP target. End-to-end two-track mixing was tested with synthetic audio; real-world voice intelligibility still needs a listening pass.

## Example minimal single-scene JSON

```json
{
  "project": {"title": "A clean black and cream look", "brand": ""},
  "output": {"width": 1080, "height": 1920, "fps": 30, "crf": 18},
  "cast": {"woman_identity": "Original adult woman, defined in reference sheet", "man_identity": "Original adult man, defined in reference sheet"},
  "studio": {"description": "Locked original fashion studio, frontal full-body camera"},
  "audio": {},
  "scenes": [
    {
      "id": "01_black_cream",
      "duration": 2.5,
      "asset": "assets/01_black_cream.mp4",
      "colors": [{"name":"black","hex":"#1B1A1A"},{"name":"cream","hex":"#F2EDE0"}],
      "woman_outfit": "Black fitted sweater, cream wide trousers, black flats",
      "man_outfit": "Cream knit, black trousers, black leather loafers"
    }
  ]
}
```
