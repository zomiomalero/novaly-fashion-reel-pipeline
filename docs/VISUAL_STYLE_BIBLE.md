# Visual and editorial style bible - original fashion compare reels

The practical target is a believable short-form styling display, not a visual-effects show. The uploaded references repeatedly show coordinated adult fashion presenters, one fixed room, full-body portraits, gentle body motion, and a new complete outfit every few seconds.

## Canvas and shot geometry

- Default master: **1080x1920**, 30 fps, progressive H.264 MP4; source clips can be 24 or 30 fps and are normalized at render.
- Approximate program length: **20 to 30 seconds** for 6-10 editorial comparisons.
- Keep shoes inside frame at all times; leave lower clearance so a long trouser hem is visible.
- Lock the two presenters' apparent heights and body proportions; maintain the same left-right position in every look.
- Straight-on camera at an editorial full-body height, fixed lens and tripod, no slow camera dolly or virtual crane.
- Reserve the top-center region for minimal color labels; do not place typography over faces. Keep critical content clear of platform-native right-edge UI and lower UI bars.
- A visually calm studio set with consistent surface materials, believable contact shadows, a small simple prop and a neutral curtain or wall.

## Cast and fashion physics

The model identities are *new and original*, defined in `project.cast`. Use one original character sheet per person, including straight-on full body and facial detail, plus one fixed studio master image. Each look starts as a new wardrobe first-frame still. Video models should animate this look, not create a wardrobe transformation.

Good: a tiny palm-up gesture, natural blink, soft smile, head turning 5-10 degrees, relaxed weight shift, blouse folds moving with the torso. Bad: synchronized robotic gestures, stiff facial expression, body twisting while feet stay glued, jewelry or bag melting, trousers clipping through shoes, fingers merging, eyes wandering.

Make a micro-action map: the presenting person can move a hand once per shot; the second model remains a stable visual comparison. Alternate which model is more expressive across looks to avoid repetitive movement.

## Colors and clothing

- Use controlled natural skin and fabric tonality. No cartoon black outlines, emissive glow, plastic skin or aggressive saturation.
- Name the colors accurately in the JSON. Color chips are approximations to the garments, not color-science proof of exact textile dyes.
- Show full outfits, not cropped waist-up frames: trouser silhouette, waist rise and shoe shape matter.
- Avoid presenting every look with an identical gesture or handbag hand position.
- For denim, name the **silhouette**: wide-leg, straight, slim, barrel or bootcut. For couple style comparisons, name the **pairing**: green and cream, navy and camel, black and white.
- Keep fashion guidance practical and nonjudgmental; no unsupported body-type promises or shopping pressure.

## Editorial rhythm

1. Start on a complete image and a useful hook, not a brand animation.
2. A look lasts long enough for a phone user to read one concept and see the pants, shoes and upper garment (often 2-3 seconds).
3. A hard cut signals a new look. Do not ask a video model to morph clothing between scenes.
4. Keep the set constant across wardrobe cuts; this repetition enables direct comparison.
5. Finish after the last clearly demonstrated pairing. Optional subtle saved-look call to action may be in narration; avoid an empty outro.

## Text and graphic system

The renderer draws a small rounded translucent color capsule near 10% of canvas height with physical swatches and plain-language labels. Swatch colors come from `project.scenes[].colors`. For denim-style teaching, a scene can set `formula` to replace swatches with a readable fit-formula label. An optional `emphasis` string is placed near 65% of frame height, away from the bottommost social platform controls. A small optional project brand may appear in the upper-left.

The generator prompt always requests **no embedded text** so labels can be revised without re-generating the people. Avoid more than 3 chips or 45 emphasis characters per scene. Do not use giant captions that hide waist, jeans fit or shoes.

## Audio

Most measured references cluster near -16 LUFS integrated. Use a consistent clean original voiceover and an appropriately licensed bed. The pipeline downmixes to stereo 48 kHz AAC and ducks music using the voice as the sidechain. Aim for readable speech, no harsh peaks, and no perceptible long silent gaps.

## Quality acceptance

Keep the following anchors visibly consistent on every shot: studio curtain folds, plinth side, floor edge, model heights, hair silhouette, facial structure, eye color, shoe contact shadow, camera distance and chest/waist positions. If a model changes identity or a handbag disappears, reject the shot **before** editing it into the master. Use `docs/QUALITY_GATES.md` at final review.

## Originality policy

The reference clips teach editorial grammar, not identities. Use a new studio master and genuinely original adult model identities, wardrobe concepts, scripts and branding. Do not extract reference frames as generation input to clone a real creator, and never place private reference clips in the Git repository.
