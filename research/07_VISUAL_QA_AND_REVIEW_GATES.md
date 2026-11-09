# 07 / Quality gates and release readiness

## Three separate kinds of quality

**Technical validity:** frame count, dimensions, codec, audio presence, black/white/frozen frames, loudness and accidental large frame changes. This can be measured with code.

**Visual production quality:** identity, anatomy, fabric behavior, hand and shoe correctness, color accuracy, camera/room continuity, edited graphic legibility. This requires human visual review and cannot be certified from metadata.

**Editorial quality:** usefulness of the styling lesson, originality, pacing, hook, avoidance of repetitive combinations and responsible claims. This also requires an editor; no objective checker can guarantee it or guarantee virality.

Do not combine those categories into a fake single score that implies objective human-visual correctness.

## Release gates

| Gate | Command or artifact | Auto? | Block release if |
|---|---|---|---|
| 01 / Schema | `fashionreel validate project.json` | Yes | Missing/bad IDs, illegal lengths, invalid swatches |
| 02 / Source | `fashionreel preflight project.json` | Yes | Missing inputs, source much shorter than planned |
| 03 / Prompt audit | `fashionreel prompt-audit prompt_pack/` | Yes (heuristic) | Contradictory duration / outfit morph language |
| 04 / Actor/source | Cast sheets, studio master, outfit first-frames | Human | Identity, camera or garment states not locked |
| 05 / Continuity | `fashionreel continuity project.json` | Mixed | Set landmark and human silhouette drift |
| 06 / Preview edit | `fashionreel render --quick` | Yes | Broken clips, unreadable overlays, timing errors |
| 07 / Audio | `fashionreel audio-qc` + headset check | Mixed | Clipping, masked voice, unintentional silence |
| 08 / Master | Full-quality `fashionreel render` | Yes | Wrong duration/specification or truncated ending |
| 09 / Technical QA | `fashionreel qa final.mp4 --project project.json` | Yes | Wrong dimensions, fps or frame count |
| 10 / Editorial | Reviewer watches in real social-player crop | Human | Poor lesson, repeated looks, illegible garment fit |
| 11 / Reuse | `fashionreel repeats` and `compare-videos` | Mixed | Too similar to recent original Novaly content |
| 12 / Rights | Licenses/consent approvals | Human/legal | Unapproved person's likeness, third-party footage, music |

## Minimum 2-pass human clip QC

**Pass A / scene continuity**

1. Compare the exact same fixed original cast identity sheet against the first/mid/last frame of each look.
2. Compare nose/eye structure, hair part, face silhouette, visible jewelry and model height, taking pose changes into account.
3. Check the studio left anchor and floor seam. Look for prop drift, curtain fold changes and inconsistent lighting.
4. Check shoe contact shadows; crop failures often occur when toes are near frame bottom.
5. Check fabric: no garment changes category, pattern, color or neckline while the model moves.

**Pass B / editorial truth**

1. Watch normally on a phone-sized viewport. Does one viewer understand the idea without pausing?
2. Check every label against the actual source shot; do not trust only metadata.
3. Listen to the voice with eyes closed. Natural phrasing? Abrupt gaps? Audible consonants?
4. Check movement: normal, unforced breathing and gestures; no overly robotic motion or body snaps.
5. Check the ending. End on a complete visual answer, not a random freeze or redundant logo card.

## Thresholds as review triggers, not universal truths

| Signal | Existing automatic behavior | How to interpret |
|---|---|---|
| Whole-frame mean below 0.035 | `qa` near-black frame warning | May be intentional fade, or broken source |
| Whole-frame mean above 0.95 | `qa` near-white warning | May be deliberate flash, or blown image |
| Exactly repeated frames ≥12 | `qa` freeze warning | Intentional stills allowed, talking actor freezing suspicious |
| Unexpected large frame RGB jump | `qa` candidate cut listing | Hard cuts are intentional in fashion editing |
| Voice/program loudness >3 LU from −16 | `qa` warning | Needs listening; context may justify a different target |
| Background anchor correlation <0.72 | `continuity` review region | May be lighting/pose change or set drift |
| Source shorter than scheduled by >0.08s | `preflight` warning | Might freeze last source frame |

Avoid asserting a failure just from a metric. Evaluate signal **at its timestamp** in context.

## Release record fields

Store a lightweight `release_review.json` or internal checklist with `project`, `reviewer`, `date`, `source_hashes`, `human_identity_approved`, `music_rights_approved`, `garment_labels_verified`, `phone_preview_passed`, `technical_qa_file`, `status` and `notes`. Never infer those human approval booleans automatically. This source package provides the checklist pattern but does not silently record a human approval.

## Copyright and privacy

The user-supplied Facebook/downloaded videos are privately analyzed and their image sheets are included **only** in the full offline work bundle. They are excluded from the public-ready GitHub archive and from the installable Skill. The public archive contains original procedural assets and numerical research measurements instead. Do not push the full private work bundle's `private_reference_lab/` to a public repo.
