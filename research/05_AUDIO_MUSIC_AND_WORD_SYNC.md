# 05 / Narration, music, sound quality and word timing

## What was actually measured

All seven references include AAC audio. The previous FFmpeg EBU R128 runs returned approximately:

| Ref | Integrated LUFS | Loudness range (LU) | Reported true-peak dBTP |
|---:|---:|---:|---:|
| 01 | −16.5 | 6.8 | +0.2 |
| 02 | −16.1 | 5.1 | +0.2 |
| 03 | −16.1 | 4.6 | +0.1 |
| 04 | −16.2 | 5.1 | +0.1 |
| 05 | −16.1 | 4.9 | −0.1 |
| 06 | −16.0 | 4.7 | +0.3 |
| 07 | −16.0 | 5.0 | +0.2 |

LUFS is integrated program loudness, not a measurement of narrator-only loudness or a guarantee of intelligibility. Positive true-peak readings suggest some source audio peaks would be safer with a lower ceiling. The new pipeline targets around −16 LUFS and −1.5 dBTP using FFmpeg `loudnorm`. The target is editable in project JSON; platforms may alter playback loudness.

## The source repository vs original fashion production

The reference cartoon repository synthesizes its own march score and detailed SFX (`music.py`, `instruments.py`, `sfx_gen.py`, `mix.py`) with voice-triggered ducking, exact length and 48kHz stems. Reusing its actual march music and bolt-snap SFX would be absurd in a calm clothing-comparison reel. Reuse the **engineering idea**—independent stems, event timing, voice precedence, measured loudness and final verify—while using suitable ORIGINAL/fully licensed fashion-oriented instrumental beds.

## Narration workflow

1. Write a short human sentence that adds information beyond the label. A useful example: `Keep the trousers soft and choose one tailored upper layer; the contrast does the work.`
2. Confirm words and outfit claims are correct before generating voice.
3. Record or synthesize a natural-sounding original narration outside the editor. Avoid claiming the CLI does TTS.
4. Trim accidental long start delay, breaths that obscure the hook and mouth noises. Do not splice so tightly that words collide unnaturally.
5. Obtain actual word timings from your chosen aligner and correct them by listening. Do not infer timestamps from word count alone.
6. Run `fashionreel word-sync ...`; inspect which words overlap each shot.
7. Put `voice.wav` and licensed `music.wav` in local `assets/` and configure relative paths.
8. Render then run `fashionreel audio-qc final.mp4 --out audio_report` and listen through the full finished clip on a phone-sized player.

## Exact signal-flow outline

```text
source voice (mono/stereo) ─▶ resample 48k, gain and pad to exact video length ───────────────┐
                                                                                              ├─ mix ─▶ EBU R128 loudnorm ─▶ AAC
licensed music ─▶ resample 48k ─▶ gain ─▶ voice-triggered sidechain duck ────────────────────┘
```

The editor creates a silent video master, then muxes the final composed soundtrack. It explicitly maps the created audio stream and never assumes a silent Remotion-like audio stream can be carried through the concat stage. The audio master is trimmed to the frame-scheduled picture duration. The `sidechaincompress` filter attenuates music during voice; static gain alone is not a substitute for listening for masking. The exact rendered loudness can still differ from target because AAC encoding and true-peak reconstruction affect the final result.

## Detailed quality gates

| Gate | Objective signal | Manual follow-up |
|---|---|---|
| Hook begins promptly | `word-sync` first word starts before about 0.35s | Does first word sound natural, not rushed? |
| Voice not cut off | Last word end at or before export end | Is final consonant audible? |
| Music stays under narration | Sidechain compression and listen | Any words masked by midrange instruments? |
| No harsh peak | `audio-qc` true peak around/below −1.0 dBTP | Any crackle/distortion from source? |
| No accidental pauses | `silencedetect` spans >0.32s, flagged for review >0.65s | Intended emphasis vs missing audio? |
| Consistent level | Final integrated near configured target | Does speech sound similar across shots? |
| Clean endpoint | Picture and audio duration align | Does the music end in a deliberate musical place? |

## Troubleshooting

- Music remains too loud: lower `audio.music_gain_db`, consider a voice-centric arrangement, check mastering after ducking.
- Speech rushed: write fewer words or extend related shot; do not artificially speed the narration until it sounds robotic.
- Word-sync mismatches: correct the transcript/timing JSON by listening, regenerate map, then adjust scene durations in frames.
- Unexpected long silence: confirm voice file is not shorter than requested and not padded accidentally.
- Clipped true peak: check source WAV headroom and final limiter/mapping; encoding alone can create overs.

**Tools:** `render.soundtrack`, `word_timing.make_sync_map`, `audio_qc.audio_report`, `qa.check`.
