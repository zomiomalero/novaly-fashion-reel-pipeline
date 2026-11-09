# Cross-video visual reuse audit

A 1fps visual-similarity study for editorial diversity planning. Numbers are not proof of identical source ownership.

| A | B | Closest frame distance (8-bit RGB) | Nearest median | Near-match samples A→B |
|---:|---:|---:|---:|---:|
| 01 | 02 | 3.05 | 12.66 | 9/25 |
| 01 | 03 | 59.95 | 69.82 | 0/25 |
| 01 | 04 | 2.45 | 11.97 | 9/25 |
| 01 | 05 | 15.14 | 21.65 | 0/25 |
| 01 | 06 | 3.01 | 11.17 | 10/25 |
| 01 | 07 | 2.08 | 10.96 | 11/25 |
| 02 | 03 | 60.24 | 70.66 | 0/28 |
| 02 | 04 | 2.85 | 7.93 | 15/28 |
| 02 | 05 | 16.14 | 23.84 | 0/28 |
| 02 | 06 | 0.72 | 0.89 | 25/28 |
| 02 | 07 | 1.78 | 4.79 | 22/28 |
| 03 | 04 | 59.94 | 66.96 | 0/22 |
| 03 | 05 | 58.97 | 68.11 | 0/22 |
| 03 | 06 | 60.23 | 66.87 | 0/22 |
| 03 | 07 | 60.49 | 66.67 | 0/22 |
| 04 | 05 | 15.35 | 26.22 | 0/29 |
| 04 | 06 | 1.56 | 6.59 | 19/29 |
| 04 | 07 | 3.29 | 6.91 | 18/29 |
| 05 | 06 | 15.07 | 21.64 | 0/21 |
| 05 | 07 | 14.73 | 20.81 | 0/21 |
| 06 | 07 | 1.76 | 3.52 | 26/28 |

Lower distance = closer visual sample. Matching samples use **threshold < 8** at 80×142; interpret with caution.

## Why this matters

- Multiple source reels can share the same studio, performers and wardrobe sequence. Do not count them as wholly independent training cases.
- Derive the overall production grammar, then make new original concepts, wardrobe choices and models.
- Use scene-level repeat history and compare your OWN finished reels before publishing.
- A similar studio background alone is not evidence of content theft or identity copying.
