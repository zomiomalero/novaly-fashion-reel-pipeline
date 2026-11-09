import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from fashionreel.render import render
from fashionreel.qa import check
from fashionreel.media import video_props


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg not installed")
class TestRealVideoInput(unittest.TestCase):
    def test_video_scene_with_audio_and_trim(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src = root / "source.mp4"
            voice = root / "voice.wav"
            music = root / "music.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                            "testsrc2=size=360x640:rate=24:duration=2.0", "-c:v", "libx264", str(src)], check=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                            "sine=frequency=330:duration=2.0:sample_rate=48000", str(voice)], check=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                            "sine=frequency=220:duration=1.0:sample_rate=48000", str(music)], check=True)
            project = {"project": {"title": "Video source test"},
                       "output": {"width": 360, "height": 640, "fps": 24, "crf": 24},
                       "audio": {"voice": "voice.wav", "music": "music.wav", "target_lufs": -16},
                       "scenes": [{"id": "video_clip", "duration": 1.5, "start": 0.25,
                                   "asset": "source.mp4", "colors": [{"name": "navy", "hex": "#23395D"}]}]}
            path = root / "project.json"
            path.write_text(json.dumps(project), encoding="utf-8")
            final = render(path, root / "final.mp4", workdir=root, quick=True)
            props = video_props(final)
            self.assertTrue(props["has_audio"])
            qa = check(final, root / "qa", project_file=path)
            self.assertFalse(qa["failures"])
            self.assertEqual(qa["frame_checks"]["frames_decoded"], 36)


if __name__ == "__main__":
    unittest.main()
