# 01 / Timing, visual beats, and reference structure

## Evidence and limits

The seven clips were decoded from the files supplied in the conversation. The private `private_reference_lab/ref_XX/metrics_every_frame.csv` contains one row per native frame (4,776 in total). The contact sheets illustrate every ~100 ms (10 fps), rather than every frame. Look-boundary timestamps below are earlier **pixel-change heuristic candidates**, not human-certified edit lists. A gesture or subtitle swap may cause a false boundary. Do not present them as authoritative cut timestamps without watching neighboring frames.

| Reference | Runtime | Native fps | Large visual-change candidates | Mean frame-change, 8-bit RGB | Visual family |
|---:|---:|---:|---:|---:|---|
| 01 | 25.20s | 30 | 7 | 1.17 | Adult couple, coordinated palettes, curtain studio |
| 02 | 27.77s | 24 | 9 | 1.70 | Adult couple, expanded palettes, curtain studio |
| 03 | 21.54s | 24 | 5 | 1.14 | Two women, denim silhouettes, dark wood wall |
| 04 | 28.84s | 24 | 9 | 1.67 | Adult couple, reordered palettes |
| 05 | 21.37s | 30 | 9 | 1.13 | Adult couple, jean wash and top-color combinations |
| 06 | 27.89s | 24 | 9 | 1.52 | Adult couple, reordered palette sequence |
| 07 | 27.84s | 30 | 9 | 1.22 | Adult couple, palette sequence with alternate editorial labels |

These metrics describe the samples as received; resolution is 720×1280 in all cases. They do not measure semantic value or audience retention.

## Narrative/visual formula

**Immediate already-dressed hook → sequential outfit comparison → short useful label → modest physical gesture → hard visual wardrobe change → another complete comparison → end on the last useful look.** There is no separate elaborate title sequence. The image is always doing the majority of the explanation. For the new project, write ONE claim about one visually demonstrable styling decision. Use the clothes to demonstrate that claim rather than narrating everything that is already obvious.

Video 03's formula is a strong alternate: one silhouette at a time, then a balancing upper garment, keeping both models in the same set. It deserves its own template instead of being diluted into couple color-pair looks. Video 05 separately tests denim wash against warm/cool upper-color contrasts. Keep these as different series, not just reordered copy of the same idea.

### Start-to-finish structure, recommended (original Novaly editorial defaults)

| Timeline | Role | Viewer sees | Narration function | Internal constraint |
|---|---|---|---|---|
| 0–2.5s | Immediate promise | Fully dressed people / clear silhouette | One useful problem or contrast | Voice begins promptly, avoid logo delay |
| 2.5–7.5s | First proof | Two or three distinct looks | Explain a reusable rule | Shoes visible; change at meaningful beat |
| 7.5–16s | Variety | Different color or silhouette families | What the contrast changes | Keep original cast and locked set |
| 16–24s | Contrast / payoff | Best complementary or surprising look | Transfer lesson to audience | Do not recycle a previously seen look |
| Last 1–3s | Final useful beat | Complete final outfit | Concise closing, no dead outro | Last frame and last word end deliberately |

This is a proposed design grammar for original output, not a claim that each uploaded clip has identical structure.

## Deterministic frame scheduling

Always calculate cut positions as integer frames, not cumulative decimal seconds. In the source project, `config.frames()` rounds scene durations to the chosen frame rate; `schedule()` calculates monotonically increasing `first_frame`, `end_frame_exclusive` and `duration_s`. At 30 fps, a 2.65s shot is 80 frames and lasts 2.6667s—not precisely 2.65s. All overlays and audio should follow the **rounded frame** schedule. Runtime equals `sum(frames)/fps`.

Never generate two wardrobe states in a single model-video scene and hope editing can cut at the exact transformation. Generate each look independently and perform hard cuts in FFmpeg. For speech synchronization, create a corrected word-level JSON file with `[{"text":"...","start":0.12,"end":0.37}]` and run `fashionreel word-sync project.json words.json`. It maps actual words to shot frames and warns about speech beyond the video. This workflow does not generate word timings automatically.

## Failure modes and troubleshooting

- **Hook too slow:** first complete look appears after a title, unrelated b-roll or pause. Fix by showing the finished outfit on frame one and reducing setup language.
- **Cut on an incomplete gesture:** the arm appears to teleport or the hand is cropped mid-motion. Select a stable terminal pose, then cut to the next complete look in the same standing position.
- **Very short comparison (<1.3s):** swatches and garment shape are difficult to understand. Consolidate one look into a longer shot. Shorter beats should be intentional accents, not the norm.
- **Repeated point:** two consecutive looks prove the exact same visual relationship. Reject the redundant variant rather than adding explanatory text.
- **Fake pacing from random zooms:** source videos are predominantly stable-camera content; moving the camera changes the grammar and makes production consistency harder.
- **Inconsistent duration:** source clip shorter than planned edit produces a frozen tail. Run `fashionreel preflight` before the render and regenerate short inputs.

## Pass/fail questions

1. Does the first frame show a real, complete outfit comparison or design solution?
2. Is each look distinguishable on a phone-sized viewport in normal playback?
3. Does any cut unintentionally interrupt a garment fold, sleeve gesture or shoe movement?
4. Do all visual claims match the real clothes the model is wearing in that shot?
5. Does the last visual hold, the last word and the music tail end deliberately rather than drifting into silence?

**Related tools:** `config.schedule`, `word_timing.make_sync_map`, `preflight.inspect_assets`, `qa.check`, `research/reuse/REUSE_AUDIT.md`.
