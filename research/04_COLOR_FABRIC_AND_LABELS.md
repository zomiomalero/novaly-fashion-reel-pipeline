# 04 / Color, textile surface and truthful on-screen labels

## Reference observations

The couple-centered reels often show two simple color name chips across the upper portion of the image: e.g., black/white, burgundy/beige, green/cream, navy/camel, pink/grey and red/beige. Reference 03 instead uses short *fit equations* such as `baggy jeans + fitted tops`, `wide-leg jeans + slim tops` and `bootcut jeans + elegant tops`. Reference 05 combines a denim wash name with top colors. That distinction should become different **schema types** rather than one generic label slapped onto every video.

The measured whole-frame saturation proxies (all native frames, 90×160 reduction) are approximately `0.175, 0.154, 0.332, 0.157, 0.184, 0.155, 0.159` for sources 01–07. Source 03 is darker and has a different palette. These are image statistics, not proof that garments have particular physical dye values.

## Separate three concepts

1. **Garment color intention**: the design/specification color as a human-readable fashion category, e.g. olive, black, camel.
2. **Reference chip color**: UI swatch hex value in `project.scenes[].colors`, selected as an approximate visualization of intention.
3. **Actual rendered cloth pixels**: affected by studio key/fill, white balance, camera transfer, compression, material and shadows. They should not be expected to exactly equal the chip hex.

Never validate actual fabric accuracy by simply measuring a random pixel at a fold. Instead compare representative mid-tone textile areas in a few reviewed frames; note highlight, fold, material sheen and backdrop contamination. The source renderer's RGB chips are design aids. If a seller needs product-accurate color, they should use color-calibrated photos and verified product color references.

## Physical textile cues to preserve

| Material | On-screen appearance | Failure to reject | Source study asset |
|---|---|---|---|
| Cotton poplin | Smooth but subtle weave, soft paper-like folds | Plastic shine, repeating shimmering veins | `cotton_*` |
| Linen | Noticeable small slubs, soft irregular creases | Uniform glossy satin | `linen_*` |
| Denim | Dense diagonal weave, substantial seam/hem shape | Jeans turning into soft fluid cloth | `denim_*` |
| Twill | Fine diagonal structure, controlled trouser drape | Color-only shape with no leg volume | `twill_*` |
| Rib-knit | Raised columns, subtle contour around joints | Knitted ribs melting as arms move | `rib-knit_*` |
| Satin | Directional broad specular sheen, fluid drape | Metallic reflective mirror or plastic sheets | `satin_*` |

The 48 procedural material studies are fully original synthetic test surfaces. They support prompt writing, art direction and color swatch exercise; they are NOT photographic evidence of textile quality or licensed product photography.

## Pairing logic grounded in the visible demonstration

- **Dark + light:** outfit parts separate visually; check the light trousers retain fold definition against the pale studio floor.
- **Warm tonal pair:** a rust, burgundy or chocolate upper with beige/oat lower produces a warmer frame; maintain natural skin tone and avoid oversaturating every garment.
- **Cool + warm balance:** navy/camel or slate/sand contrasts hue and value; the rendered wardrobe must actually match the label.
- **Low contrast:** olive/forest with cream or stone can appear sophisticated but needs edge separation against a neutral studio backdrop.
- **Monochrome:** variation in texture and value matters; all-black outfits must keep seam/shape detail rather than collapse into solid black.

These are style concepts, not universal claims that a certain pairing always looks better on every person. Avoid fashion shaming, ungrounded body type prescriptions and absolutist advice.

## Labeling and platform safe zones

The source videos generally put concise chips/words near the top while people remain full height. The package intentionally overlays text in post (`overlays.py`) instead of embedding it into AI images, because baked-in model text can be misspelled, move, or morph. Use one to three color chips with legible text. For denim education, a `formula` string can replace multiple chips; keep it under the schema's existing 55-character limit. Mobile UI can overlap the bottom and right; check preview across Instagram, Facebook and Shorts and adjust brand-specific safe areas.

### Minimum visual QA

- [ ] Every swatch name matches the actual garment family the viewer sees.
- [ ] No chip obscures a model face or important design element.
- [ ] A white garment contains usable seams and folds instead of clipping.
- [ ] A black garment separates from hair, bag and shoes enough to read.
- [ ] A denim silhouette is visible from waistband to shoe.
- [ ] Texture does not crawl or pulse frame-to-frame.
- [ ] No unsupported color-science claims about calibrated textiles.

**Code paths:** `overlays.py`, `prompts.py`, `config.validate`, `assets/original-material-studies/manifest.csv`.
