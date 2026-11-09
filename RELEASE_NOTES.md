# Novaly Fashion Reel Production Pipeline — V2.0.0

Updated on 2026-11-09 in response to the valid criticism that the previous 101 KB ZIP lacked the upstream repository's deep visual assets and documentation.

## Source and production features

- Added six modules: `preflight`, `continuity`, `prompt_audit`, `word_timing`, `audio_qc`, `reuse_audit`.
- Added five ready-to-use editable series projects beyond the original two, with complete image/video prompts and storyboards.
- Added eight substantial research chapters and a 21-pair near-duplicate video similarity report.
- Added 48 truly original procedural textile/lighting studies and eight technical staging plates, with deterministic generation source.
- Preserved frame-accurate render, separated audio, voice ducking, final FFmpeg QA and source reusability.
- Added asset SHA-256 preflight, manual licensing reminders and background-anchor continuity.

## Full offline research edition (not for public GitHub)

- Seven analyzed user-supplied videos: 4,776 decoded native frames measured; 33 10fps visual contact sheets; 98 larger 540×960 stills.
- Frame-by-frame CSV, chart, candidate-cut annotations and technical study for each supplied video.
- Original source MP4s deliberately excluded from the packages; only derived study grids are in the private edition.
- The original channel's actors and outfits are NOT redistributed in the GitHub public edition.

## Reliability and honest limits

- 32 automated tests pass in the builder environment; multiple example validation subtests also pass. Synthetic FFmpeg smoke still needed no external AI video provider.
- No end-to-end source generation of realistic human footage; only prompt packs, editing and technical QA are automatic.
- No automated identity verification or semantic garment evaluation; this is a manual release gate.
- Automated similarity scores do not prove that two videos share ownership.
- Public GitHub repository creation remains a step the authenticated user must execute in their own CLI.

**Publication:** `./scripts/publish_to_github.sh novaly-fashion-reel-pipeline zomiomalero` from the extracted public project folder. Verify the remote after pushing. Public link is not active until publishing succeeds.
