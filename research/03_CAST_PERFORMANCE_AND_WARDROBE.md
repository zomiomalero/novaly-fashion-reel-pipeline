# 03 / Cast performance, wardrobe silhouettes and motion physics

## Why the source rendering method should change

The `MSLIKTT/claude-animated-shorts` source uses 2D canvas-drawn cartoon actors (`toon.ts`, `cast.ts`) oriented as camera-facing cards inside a Three.js toon world. These design decisions intentionally produce thick illustrated faces, bean silhouettes and 3.5-head-height bodies. They are appropriate to its historical cartoon example, but inappropriate to your uploaded **realistic fashion presenter** references. Our visuals require adult human anatomy, real fabric geometry and consistent face identity, so we use externally generated/filmed full-body shots then deterministic local editing.

## Actor anchor record: one approved original cast

Before generating any wardrobe clips, create an original actor identity sheet with clear frontal full-body, three-quarter standing and facial detail. Record only visible non-sensitive design anchors useful to appearance consistency:

| Anchor | Woman | Man | Verify each shot |
|---|---|---|---|
| Face silhouette | Fixed original character | Fixed original character | Same brow, jaw and eye geometry |
| Hair | Fixed length, shape and part | Fixed hairline and styling | Stray locks do not grow/disappear |
| Proportions | Set height/limb ratio | Set height/limb ratio | Same relative height in paired frame |
| Pose | Natural leg balance | Natural leg balance | Weight on a plausible supporting foot |
| Hands | Five fingers, consistent joints | Five fingers, consistent joints | No merged palms or sudden extra fingers |
| Foot contact | Sole and shadow meet floor | Sole and shadow meet floor | No sliding shoes or floating heels |
| Textile identity | Colors, seams, folds | Colors, seams, folds | Same garment throughout that clip |

Save approved stills and version them outside the public repository if they include real-person faces or client data. The project JSON can safely retain textual descriptions; private cast images are local work products. Never use the reference people's faces as reusable generation identity sheets unless you have permission.

## The 'already dressed' strategy

The most robust way to avoid outfit morphs is **one complete still per look**. Generate a still that already shows the intended shirt, trousers, belt, bag, outerwear and shoes. Only AFTER the still is approved, animate that exact completed outfit. Hard-cut to a separate shot for the next look; do not animate one outfit turning into another in the same clip. This is different from morph-transition channels and matches the visual comparison objective.

Keep the generated video prompt compact. It should state: original character continuity, attached first-frame preservation, locked studio, natural micro-movement, one continuous full-body scene, no on-screen labels, and one small specific action. Numeric duration belongs OUTSIDE the prompt in the shot manifest. A giant negative prompt with dozens of prohibitions often competes with the actual movement instruction.

## Realistic action grammar

- **Breathing:** tiny rib-cage rise and fall. It is visible in shoulders and cloth folds, not as a mechanical up/down body bob.
- **Weight shift:** move the center of mass over a supporting foot; knees and pelvis should respond. Do not keep both feet perfectly fixed while the upper body drifts sideways.
- **Head turn:** head, neck and gaze move together. A look toward the partner should not leave eyes frozen on camera.
- **Pointing:** one leading hand should change elbow and shoulder naturally; fingers should finish in a recognizable gesture.
- **Pocket gesture:** hand enters a visibly consistent pocket; do not fuse fabric into the forearm.
- **Handbag:** strap is held under gravity; bag does not levitate, swap sides without motion, intersect the leg or disappear at the cut.
- **Jeans:** wide-leg fabric follows knees/ankles; denim hem and silhouette must stay consistent with the label as the person moves.

### Variation matrix for eight shots

| Look | Main action | Secondary reaction | Editing objective |
|---:|---|---|---|
| 01 | Woman small palm-up welcome | Man relaxed half-turn | Hook and first readable outfit |
| 02 | Man one cuff adjustment | Woman holds garment line | Contrast top structure |
| 03 | Woman indicates trouser hem | Man one subtle nod | Silhouette proof |
| 04 | Both neutral, breathing | Minimal blink | Reset movement rhythm |
| 05 | Man gentle shoulder angle | Woman small smile | Tailoring example |
| 06 | Woman touches bag strap | Man stays mostly still | Accessory and cloth physics |
| 07 | Man natural weight shift | Woman keeps feet planted | Demonstrate posture realism |
| 08 | Woman quiet finishing nod | Man natural blink | Final beat without empty outro |

The actions are example directing prompts, not strict evidence of the source videos' exact motions. Their purpose is to avoid synchronized robotic behavior and create variation without risking character drift.

## Human visual gates

Reject source media before rendering if a face changes, hands fuse, the model's height jumps, shoes slide, a top changes fabric type, the backdrop or pedestal moves, or a garment changes color mid-clip. Passing `fashionreel qa` means technical checks passed; it does not guarantee any of these human visible properties. Use `continuity_contact.jpg` plus first/mid/last frame inspection.

**Adapting across tools:** Seedance, Dola and other image-to-video systems accept separate image references and text differently. Preserve exact identities and wardrobe anchors conceptually, but test each provider's reference-image features before using all generation credits. Do not promise automatic lip-sync or audible dialogue for b-roll; this fashion pipeline is designed for separate narrations unless a project explicitly requires a speaking presenter.
