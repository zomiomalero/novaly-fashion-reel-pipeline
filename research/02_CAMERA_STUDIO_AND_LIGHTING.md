# 02 / Camera, set continuity and realistic light

## The visual families in the supplied reference set

References 01, 02, 04, 05, 06 and 07 repeatedly use an ivory/cream fabric backdrop, a neutral floor, two full-height adult presenters and a small dark plinth on the right side. Reference 03 instead shows two female presenters against dark brown vertical wooden paneling. These are observations from the reference contact sheets, not a claim of camera model, original lens focal length, or exact light wattage. No EXIF or original filming metadata establishes an exact lens or lighting fixture.

The camera is visually close to a neutral, full-body straight-on composition. Preserve stable shoe/floor clearance, headroom, apparent height, left-right relative positioning and cast proximity between every generated look. A dramatically different lens, camera angle, crop or camera distance makes simple outfit comparisons much harder to read.

## Original Novaly set blueprint

Do **not** recreate a source creator's exact studio pixels. Establish one ORIGINAL set with a defined scene graph:

| Landmark | Proposed original location | Continuity duty | Typical rejection |
|---|---|---|---|
| Left wall surface | Upper-left 0–20% frame width | Texture/lighting anchor | Texture folds and edge drift |
| Backdrop | Behind models, 10–82% frame width | Frame-to-frame set identity | Pattern or curtain geometry changes |
| Floor seam | 72–83% frame height | Body height and foot placement | Seam moving vertically, floating shoes |
| Display object | Right third, behind actor silhouette | Depth and spatial anchor | Different prop silhouette or height |
| Female standing mark | Approx. 32% frame width | Cast layout continuity | Horizontal drift / scale change |
| Male standing mark | Approx. 65% frame width | Cast layout continuity | Taller/shorter than original without reason |

Landmark positions are NEW proposed layout ranges for editable design, not measured coordinates in the supplied clips. Reference `assets/technical-plates/plate_01.png` and `plate_03.png` for labeled diagrams.

### Lock the generation environment

Use an empty room master plate independent of character sheets. Attach it, along with both **original** actor identity sheets, to every new outfit still. Keep one camera setting across a full reel. Prefer an eye-level, full-body studio viewpoint with natural perspective; avoid extreme wide-angle distortion, low-angle heroic poses or shallow focus that blurs all garments. A plausible lens-equivalent in a controlled portrait setup can be chosen by the creator and locked for the series; do not claim the input file proves a 35mm, 50mm or 85mm camera.

Define a reproducible `studio` paragraph in every `project.json`: room dimensions/landmarks, backdrop tone, floor material, camera height, focal length intention, camera-to-subject distance, shadow direction, key/fill quality and fixed floor marks. Do not let a video model silently invent a different studio for each look.

## Lighting behavior to reproduce at the principle level

- **Key:** broad, soft source from the front-left to reveal fabric surface and skin shape without hard, wandering shadows.
- **Fill:** weaker, neutral reflected light from opposite side; avoid identical bright sides that flatten folds.
- **Skin:** maintain non-plastic facial texture; a real face has uneven microcontrast, small highlights, subtle shading and human skin tone variation.
- **Contact:** shoes need floor shadows. An actor with no contact shadow reads as composited even if the face looks sharp.
- **Backdrop:** highlight direction and vertical folds must remain stable while outfits change.
- **Color temperature:** lock per scene family. Do not alternate warm amber and cool green between looks unless the editorial premise is a lighting study.
- **Exposure:** bright cream trouser texture must retain seam and fold definition, not clip into undifferentiated white.

The source repo uses directional-light presets, `lights.ts`, `shade.ts`, `cardshade.ts`, DOF and a graded Three.js virtual world. Those are useful conceptual precedents but are NOT evidence that we should use cartoon two-tone lighting or black ink lines on photorealistic people. Use actual stable photographic lighting in generated source clips. The FFmpeg editor intentionally does not apply cartoon outlines.

## Quantitative source-picture context

The private study measured mean gamma-encoded brightness at 90×160 for every decoded frame: refs 01–07 respectively **0.496, 0.537, 0.268, 0.540, 0.503, 0.535, 0.531**. The darker setting of ref 03 explains the unusually low mean. These are whole-frame brightness proxies; they are NOT calibrated sensor exposure, garment reflectance or standardized filmic grading metrics. Avoid copying an average brightness number onto an individual skin tone.

## Automated studio similarity, without false promises

Run `fashionreel continuity project.json --out continuity_review`. The tool extracts the midpoint of each source and compares narrow background anchor rectangles. It records mean absolute luminance difference and normalized high-pass structure correlation against look one. It generates a contact sheet with the exact tested regions highlighted. It does NOT recognize faces, confirm actor identity, or certify that two outfits belong to the same shoot. A source may score poorly because of changing light or compression despite an unchanged set, and may score well while actors have changed.

### Manual visual pass (mandatory)

1. Put all midpoint frames into one contact sheet at the SAME image scale.
2. Draw one horizontal line through actors' eyes and one through the floor seam. Do the lines still make spatial sense?
3. Compare the extreme left and extreme right background; did lighting shadows or folds jump?
4. Compare right prop height and position. Did the pedestal/plant unexpectedly change?
5. Compare bodies: apparent shoulder height, feet, hip width and head size. Identity and anatomy require human review.
6. Inspect first and last **video** frames, not only midpoint stills, for model flicker, garment dissolves or uncontrolled camera pan.

**Acceptance:** stable fixed set; plausible shadows; consistent actor proportions; unchanged shot framing; no clothing morphing; shoes remain visible. `continuity.py` supports the review but is not a substitute for it.
