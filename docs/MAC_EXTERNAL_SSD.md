# Mac mini / low internal storage / external SSD setup

This pipeline is designed to avoid the Remotion source repo's giant browser bundle cache. The original project's README warns of roughly 1.3 GB copied `public/` folders per Remotion bundle; our local video editor instead uses FFmpeg scratch clips in one private temporary directory, then deletes that directory after a successful or failed render.

If the Mac's internal storage is nearly full, use the external SSD for the project, Python environment, generation files, FFmpeg temporary files and final MP4s. Prefer an APFS volume for fast native Mac filesystem operations. Keep some internal storage free for macOS swapping; an external SSD does not automatically move all system data off the internal disk.

Example setup, replacing `FAST_SSD` with your actual mounted volume name:

```bash
mkdir -p /Volumes/FAST_SSD/novaly-projects
mkdir -p /Volumes/FAST_SSD/novaly-tmp
cd /Volumes/FAST_SSD/novaly-projects
# Extract this repository ZIP here, or clone after it is published.
cd novaly-fashion-reels
python3 -m venv /Volumes/FAST_SSD/novaly-venv
/Volumes/FAST_SSD/novaly-venv/bin/python -m pip install -e .
export TMPDIR=/Volumes/FAST_SSD/novaly-tmp
/Volumes/FAST_SSD/novaly-venv/bin/fashionreel demo /Volumes/FAST_SSD/novaly-projects/smoke-test
```

For real outputs:

```bash
/Volumes/FAST_SSD/novaly-venv/bin/fashionreel render \
  /Volumes/FAST_SSD/novaly-projects/my-reel/project.json \
  --out /Volumes/FAST_SSD/novaly-projects/my-reel/final.mp4 \
  --workdir /Volumes/FAST_SSD/novaly-tmp
```

Important:
- `ffmpeg` and `ffprobe` must be installed separately. Installing through Homebrew may still require space on the internal system volume, even if the project is external.
- Python dependencies are small compared with a full Three.js/Remotion/Chromium stack, but large videos can still require several gigabytes of temporary space.
- Keep generated videos and reference clips **out of Git** (`.gitignore` covers common media formats). A repository is for source and project recipes, not raw multi-GB media.
- No automation in this project deletes unrelated folders, caches, system files or other video projects. Only its own `TemporaryDirectory` is removed.
- When using an external SSD, ensure it remains attached during an edit. Do not eject until render and QA have finished.
