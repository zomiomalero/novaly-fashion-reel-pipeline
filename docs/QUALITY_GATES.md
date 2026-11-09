# Quality gates and troubleshooting

## Gate A - project specification (automated)

Command: `fashionreel validate project.json`

PASS means a valid JSON structure, unique scene IDs, finite short durations, supported media extension, correct 9:16 target, acceptable fps and valid hex colors. Add `--assets` to also check the media/audio file paths. A PASS does not prove outfit quality.

## Gate B - first-frame reference consistency (manual before video generation)

| Check | Acceptance |
|---|---|
| Female presenter identity | Exactly same facial features, hairstyle, skin texture and relative height in every look |
| Male presenter identity | Same facial features, haircut, proportions and position |
| Background set | Same curtain or wall construction, floor, plinth, decor and shadows |
| Camera | Same focal length, full body view, camera height, shoes visible, no perspective jumps |
| Wardrobe | Requested clothing and accessories visible, no misplaced colors or patterns |
| Hands/feet | Natural digits and anatomy, physically credible garment interaction |
| Independence | New wardrobe fully present before shot starts; no clothing morph |

## Gate C - source clip review (manual after video generation)

- One simple physical action, no loops of identical hand motion.
- Clothing and hair do not transform frame-to-frame.
- Stable face and body scale; no camera shake or unplanned lens push.
- Natural timing and velocity, grounded feet and believable cloth weight.
- No embedded unreadable or misspelled AI-generated text.
- Audio, if present in the generative source, is discarded and handled in the master.

## Gate D - final MP4 technical QA (automated)

Command: `fashionreel qa final.mp4 --project project.json --out qa_report`

Checks and expected results:

- Target dimension/fps match project exactly. Wrong specs = FAIL.
- Decoded frame count within 1 of schedule. Mismatch = FAIL.
- Black/white frame candidates: warnings (intentional very dark outfit footage is possible).
- Exactly frozen frame spans >=12f: warnings; a true still clip is allowed, but a talking presenter should move naturally.
- Abrupt pixel deltas: candidate cuts reported, not automatically marked as failures.
- Audio stream if present: integrated loudness and peak analysis. Warning when far from -16 LUFS or peaks excessive.
- Optional human review: faces/wardrobe, composition, text readability, lip sync, audio licensing and an actual phone screen watch.

Status values: `PASS_TECHNICAL` = no measured issues; `REVIEW` = warnings; `FAIL` = incompatible technical output. None is a copyright/quality/virality guarantee.

## Common failure table

| Symptom | Root cause | Practical fix |
|---|---|---|
| Two faces change between looks | New image created without original identity sheets | Attach original sheets to every new look first-frame |
| Camera jumps or faces change apparent size | Different crop/camera in generated source | Use one locked studio master, consistent frame and camera height |
| One shot shows clothing transforming | Last-frame of old outfit used as new look's sole reference | Generate the new complete outfit as its own first frame and hard cut |
| Hands look rubbery | Ambitious hand/turn/walk actions | Reduce to a single small gesture with stable torso/feet |
| Same outfit appears in multiple videos | No centralized look history | Run `fashionreel repeats` before recording and after publication |
| Swatch label typo | Text generated inside AI video | Source clip must have no text; fix JSON and rerender overlay |
| Final frame holds for too long | Clip shorter than its requested scene duration | Regenerate longer source, or shorten scene duration intentionally |
| Narration covers next outfit | TTS duration not aligned to scene schedule | Use storyboard times; adjust lines and rerender full mix |
| Loud music obscures voice | Music track too high or unlicensed mastering | Reduce `music_gain_db`, review ducking, recheck LUFS and true peaks |
| Output looks cropped | Input frame not truly 9:16 or subjects too wide | Generate native 9:16; use `fit: contain` only as last resort |
| Laptop storage runs out | Temporary renders on system drive | Use `--workdir` on external SSD, direct final output there |
| CI fails without image assets | Tests expect shipped copyrighted clips | Examples validate without assets; demo generates its own synthetic data |

## Signoff worksheet

- [ ] Idea is clear and original, with a genuinely useful first line.
- [ ] Model faces/hair/height and camera match in every outfit.
- [ ] Outfit colors and accessories match the storyboard.
- [ ] No camera jerk or needless movement.
- [ ] All labels fit and are easy to read.
- [ ] Transitions are intentional and easy to follow.
- [ ] Voice is natural and consistently louder than music.
- [ ] The reel has a license/rights trail for all voice, music, footage and imagery.
- [ ] The automated QA report has been read and any warnings addressed.
- [ ] A complete watch-through on a phone screen feels coherent.
