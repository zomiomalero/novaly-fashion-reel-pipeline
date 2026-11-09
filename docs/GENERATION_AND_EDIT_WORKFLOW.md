# Production SOP - script to finished reel

## 1. Choose a useful original idea

Select one focused demonstration: `outfit palette pairs`, `jeans silhouette vs top structure`, `seasonal capsules`, `one item styled 6 ways` or `day-to-evening outfits`. The viewer should understand a useful contrast in the first seconds. Avoid fashion shaming, copied claims or presenting taste as a universal rule.

## 2. Build the cast and master plate

Generate or film your own original adult models, or get written permission from cast/creators. Define face, hair, height, physique and wardrobe anchors. Capture one locked *full-body* cast sheet and one untouched studio master image. The same references go to every subsequent look. Use a fixed studio floor mark and a fixed relative left-right layout.

Recommended workflow for an image-to-video provider:

- Create **one still per unique outfit** with the newly chosen garments already worn.
- Include the same original character sheets and studio image alongside the new outfit still.
- Keep the new look's first frame separate from the previous look's final frame; otherwise some generators blend or morph outfits.
- Use the new first frame to generate a scene only, not the whole montage.
- Include no on-screen text, branding, color chips, scores, or subtitles in generated footage.

## 3. Create project metadata and prompts

```bash
fashionreel init "$HOME/Projects/my-fashion-reel" --preset color-pair-looks
fashionreel validate "$HOME/Projects/my-fashion-reel/project.json"
fashionreel prompts "$HOME/Projects/my-fashion-reel/project.json" --out "$HOME/Projects/my-fashion-reel/prompts"
fashionreel storyboard "$HOME/Projects/my-fashion-reel/project.json" --out "$HOME/Projects/my-fashion-reel/STORYBOARD.md"
```

The prompts folder contains one `.txt` per look, an instruction sheet with **recommended duration outside the prompt**, and `SHOT_MANIFEST.csv` with exact start/end frames. This avoids generation prompts that mix narrative, metadata and timing constraints.

## 4. Generate and review in batches

Generate 2 looks first and compare. Confirm identity, studio, camera, clothes, hands and lighting before spending time or credits on all 8-10 looks. Then run remaining shots with the same references and camera. Avoid prompts that ask for dramatic motion or multiple outfit transformations.

For Seedance or Dola-style image-to-video models, attach your original character sheet and the look-specific first frame. Use the `.txt` content for the scene. Set duration in the UI using the separate timing note. Use one generation at a time. After generation, compare the last frame and first frame of each adjacent look: faces, location and model scale should match even though the outfit changes on a hard cut.

### Clip acceptance pass

Reject or regenerate a scene when:
- Woman/man have changed faces, hair, age appearance, body height or relative size.
- Clothing changes shape or color mid-shot, shoes switch, bag disappears or blouse turns plastic.
- Hand contains extra fingers, fabric clips through legs, knees/ankles distort, or feet slide.
- Camera zooms or pans while all other examples remain static.
- Background curtain folds/plinth shift position, floor changes, or key light flips direction.
- Movement is silent/robotic in an intended talking segment or mouth movements do not match speech.

## 5. Narration and editing

Write one compact voiceover that starts on frame one and gives the viewer something beyond the visible outfit. Narration can describe why a pairing works, how to reuse clothes, or what fit to look for. It should not read every palette label mechanically. The example `voiceover.txt` scripts can be used as TTS input, but the CLI does not generate TTS audio.

Record or synthesize original audio, place it in `assets/voice.wav`, and put an original or appropriately licensed instrumental bed in `assets/music.wav`. Update audio paths. Generated clip audio is deliberately excluded to avoid incoherent overlapping voices.

```bash
fashionreel validate project.json --assets
fashionreel render project.json --out final.mp4 --workdir /Volumes/FAST_SSD/reel-temp
fashionreel qa final.mp4 --project project.json --out qa
```

The MP4 has precise hard cuts and crisp independent overlay chips. If voice or music is missing, it produces silent video with a warning: you can use it as a picture-only preview, but it is not automatically a publish-ready vocal short.

## 6. Final sign-off and publication

Watch the exported MP4 through once for narrative, then once with attention to clothes/hands, then once with attention to audio and text. Check social platform safe areas. Read the QA report. Only after approval add the finished look concepts to the repeat-history file:

```bash
fashionreel repeats project.json --history ../brand_look_history.json
fashionreel repeats project.json --history ../brand_look_history.json --register
```

Use a descriptive original title and avoid claims like guaranteed virality. A strong reel is the result of a clear hook, useful information, accurate visuals and repeatable execution; this system cannot guarantee reach.
