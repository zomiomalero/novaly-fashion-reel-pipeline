# Seven user-provided fashion reference videos - measured observations

Analyst date: 2026-11-09. All seven MP4 files were inspected through regular frame samples, clip metadata, frame difference analysis and FFmpeg EBU R128 loudness measurement. The original reference files and frame grids are private and not placed in the GitHub package.

## Measured technical data

| Ref | Duration | Native fps | Source size | Approx. major outfit/visual changes* | Approx. segments* | Audio LUFS (I) |
|---|---:|---:|---|---:|---:|---:|
| 01 | 25.20s | 30 | 720x1280 | 7 | 8 | -16.5 |
| 02 | 27.75s | 24 | 720x1280 | 9 | 10 | -16.1 |
| 03 | 21.54s | 24 | 720x1280 | 5 | 6 | -16.1 |
| 04 | 28.83s | 24 | 720x1280 | 9 | 10 | -16.2 |
| 05 | 21.37s | 30 | 720x1280 | 9 | 10 | -16.1 |
| 06 | 27.88s | 24 | 720x1280 | 9 | 10 | -16.0 |
| 07 | 27.83s | 30 | 720x1280 | 9 | 10 | -16.0 |

*Numbers are **heuristic frame-difference candidates**, not independently hand-annotated editorial cuts. Sudden gestures or text switches can produce false detections, and subtle wardrobe changes can be missed. Use them for scheduling guidance only.

**Audio detail:** each file has stereo AAC audio at 44.1 kHz. The EBU R128 report shows approximately -16 integrated LUFS. Some source true-peak readings approach or slightly exceed 0 dBFS, so the new exporter aims for -1.5 dBTP rather than preserving peak behavior.

## Individual visual analysis

**Reference 01 - 25.20 s.** Two adult presenters, a woman and man, in front of cream drapes with a dark pedestal and small sculpture on screen-right. Outfit progression is grouped into pairs of coordinating colors, including burgundy/black, burgundy/beige, green/black, green/cream, navy/white, navy/camel, black/white, and black/brown. The opening features a small "remember..." hook. Actors make modest gestures and remain full-body in the exact camera area. Strong subject and prop continuity.

**Reference 02 - 27.75 s.** Same two-person studio format; faster sequential comparisons across black/white, black/brown, pink/white, pink/grey, green/black, green/cream, blue/white, blue/beige, red/white, and red/beige. The central device is contrasting outfit palettes presented as an immediate visual answer to a short styling point. Subtle hand movements, very little change to lens or room.

**Reference 03 - 21.54 s.** A different set: two adult female presenters in front of a dark paneled wooden wall. Topic: how denim cut and top structure pair up, for example baggy jeans/fitted tops, skinny jeans/relaxed tops, wide-leg jeans/slim tops, straight-leg jeans/structured tops, barrel jeans/minimal tops and bootcut jeans/elegant tops. Text label is a *clothing silhouette formula*, not just a color chip. Longer holds than the color-pair examples. This supports our second JSON preset.

**Reference 04 - 28.83 s.** Cream drape two-presenter setup. More pair combinations: red/white, red/beige, blue/white, blue/beige, pink/white, pink/grey, black/white, black/brown, green/black, green/cream. Strong continuity in model positions, body proportions and studio geometry across cuts. Edits switch outfits instead of asking the model to transform clothes within a shot.

**Reference 05 - 21.37 s.** Same draped backdrop, focuses specifically on jeans color and complementary tops/layers. Label order shows light jeans with camel or chocolate, black jeans with greys/pinks/blues, and blue jeans with black/burgundy/sage. Repeated body framing makes the trousers easy to compare. The pacing is quick, and the two-presenter format allows contrasting examples at once.

**Reference 06 - 27.88 s.** Colors progress green, red, black, pink and blue in repeated outfit combinations. The woman's short explanatory gestures and the man's mostly held fashion poses create movement without distracting from garment details. Many choices share appearance with References 02, 04 and 07.

**Reference 07 - 27.83 s.** Similar studio and cast to References 02, 04 and 06, reordered to prioritize green/black and green/cream, black/white and black/brown, pink/white and pink/grey, blue/white and blue/beige, red/white and red/beige. A clear example of an efficient reusable shoot system; however, reusing identical looks too often may create repetitive content. Our repeat guard flags recurring exact palette/wardrobe pairs.

## Repeated visual grammar, across all seven

- **Stable full-body framing**: head, hands, handbag, waistband, legs and shoes remain visible. The camera is at a consistent front-on fashion display angle. Outfit comparison is the visual event.
- **Strict static set**: background fabric or wall, floor, studio props, and lighting remain stable within each episode. This is more important than big camera movements.
- **Look changes happen on edits**: an outfit is already completed in its opening frame. Clothing does not visually morph in a long continuous shot.
- **Small natural physicality**: body-weight shifts, one modest hand gesture, subtle facial movement and a small turn. Avoid endlessly waving hands or runway walks that change body scale.
- **One readable visual rule at a time**: usually the color pairing above the models, and sometimes a small short emphasis word. Reference 03 uses fit formulas instead.
- **Quick hook and finish**: starts with the presenters in frame, with no animated logo intro. End on the last clear pairing or statement.
- **Lighting is real and subdued**: neutral soft diffuse sources, controlled shadows, skin texture and garments look photographic, not toon-shaded.

## Measured approximate cut markers (seconds)

These are candidate abrupt visual changes identified at large frame difference peaks separated by at least 0.6 s; not verified as exact editorial hard cuts.

| Ref | Candidate times (s) |
|---|---|
| 01 | 3.90, 6.87, 9.20, 12.40, 15.00, 18.50, 21.13 |
| 02 | 3.46, 7.54, 9.58, 11.88, 14.29, 17.54, 20.08, 22.54, 24.79 |
| 03 | 4.29, 8.12, 11.46, 14.88, 18.29 |
| 04 | 4.17, 7.08, 9.62, 12.08, 14.12, 16.42, 19.04, 23.12, 25.54 |
| 05 | 3.47, 6.17, 7.27, 10.13, 13.17, 14.57, 17.20, 18.23, 19.33 |
| 06 | 3.29, 6.67, 8.92, 11.83, 14.46, 18.54, 20.58, 22.88, 25.42 |
| 07 | 3.30, 6.67, 9.27, 13.37, 15.40, 17.70, 20.23, 22.70, 24.93 |

## Intentional improvements to the target

1. Use *new original* models and set, not copied face identities or asset frames.
2. Maintain original wardrobe and fabric consistency with first-frame outfit stills for each look.
3. Add a per-project color/wardrobe registry to prevent repetitive episodes.
4. Render swatches in graphics rather than requiring a video model to write tiny accurate text.
5. Prefer a credible voiceover rather than forcing a model to lip-sync two humans at once.
6. Do not overuse text, flashy transitions, camera rolls, animated character shaders or novelty effects.
7. Normalize final exported sound and verify every output frame against the project schedule.

## Measurement limitations

No verified word-level transcription is supplied for these references. On-screen visible terms were analyzed visually. Color swatch names in this report reflect frame observations, not color-calibrated source textile measurements. The clip downloads are 720p; their native camera or AI generation resolutions are unknown. The sample alone cannot establish genuine view count, virality, generation software, commercial rights, or whether the actors are generated or filmed.
