import json
import shutil
import tempfile
import unittest
from pathlib import Path
from fashionreel.demo import create_demo
from fashionreel.media import video_props
from fashionreel.qa import check


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg missing")
class TestRender(unittest.TestCase):
    def test_short_smoke(self):
        with tempfile.TemporaryDirectory() as d:
            path = create_demo(Path(d) / "test")
            info = video_props(path)
            self.assertEqual((info["width"], info["height"]), (360, 640))
            self.assertAlmostEqual(info["duration_s"], 3.0, delta=.1)
            qa = check(path, Path(d) / "qa", project_file=path.parent / "project.json")
            self.assertFalse(qa["failures"], qa["failures"])
            self.assertEqual(qa["frame_checks"]["frames_decoded"], 72)


if __name__ == "__main__":
    unittest.main()
