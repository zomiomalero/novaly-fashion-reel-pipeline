import copy
import json
import tempfile
import unittest
from pathlib import Path
from fashionreel.config import read_project, validate, schedule, frames, ProjectError
from fashionreel.repeat_guard import review, key_for_scene
from fashionreel.prompts import scene_prompt, build_prompt_pack
from fashionreel.storyboard import write_storyboard
from fashionreel.overlays import overlay

ROOT = Path(__file__).resolve().parents[1]


class TestFashionReel(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "examples" / "color-pair-looks" / "project.json"
        self.project = read_project(self.path)

    def test_examples_valid(self):
        self.assertEqual(len(self.project["scenes"]), 10)
        self.assertEqual(len(read_project(ROOT / "examples" / "jeans-styling" / "project.json")["scenes"]), 6)

    def test_exact_frames(self):
        timing = schedule(self.project)
        self.assertEqual(timing[0]["first_frame"], 0)
        self.assertEqual(timing[-1]["end_frame_exclusive"], 810)
        self.assertTrue(all(timing[i]["end_frame_exclusive"] == timing[i + 1]["first_frame"] for i in range(9)))

    def test_duplicate_scene_ids_rejected(self):
        project = copy.deepcopy(self.project)
        project["scenes"][1]["id"] = project["scenes"][0]["id"]
        self.assertIn("duplicate scene id", " ".join(validate(project, self.path.parent)))

    def test_invalid_colors_rejected(self):
        project = copy.deepcopy(self.project)
        project["scenes"][0]["colors"][0]["hex"] = "olive"
        self.assertTrue(any("colors[0]" in x for x in validate(project, self.path.parent)))

    def test_asset_required(self):
        self.assertTrue(any("missing" in x for x in validate(self.project, self.path.parent, require_assets=True)))

    def test_prompts_have_continuity(self):
        sample = scene_prompt(self.project, self.project["scenes"][0], 1, 10)
        self.assertIn("SAME fictional individuals", sample)
        self.assertIn("WOMAN WARDROBE", sample)
        self.assertIn("No artificial captions", sample)
        self.assertNotIn("2.65 seconds", sample)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue((build_prompt_pack(self.project, tmp) / "SHOT_MANIFEST.csv").exists())
            self.assertEqual(len(list(Path(tmp).glob("[0-9]*.txt"))), 10)

    def test_formula_overlay(self):
        example = read_project(ROOT / "examples" / "jeans-styling" / "project.json")
        self.assertEqual(example["scenes"][0]["formula"], "wide-leg jeans + fitted tops")
        image = overlay(example["scenes"][0], 360, 640, 1, 6)
        self.assertGreater(image.getpixel((180, 83))[3], 0)

    def test_storyboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            name = write_storyboard(self.project, Path(tmp) / "story.md")
            self.assertIn("Final human approval gates", name.read_text())

    def test_overlay_transparent_outside_label(self):
        image = overlay(self.project["scenes"][0], 360, 640, 1, 10)
        self.assertEqual(image.size, (360, 640))
        self.assertEqual(image.getpixel((0, 0))[3], 0)
        self.assertGreater(image.getpixel((180, 83))[3], 0)

    def test_repeat_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.json"
            first = review(self.project, path, register=True)
            self.assertTrue(first["registered"])
            second = review(self.project, path)
            self.assertEqual(len(second["findings"]), 10)
            with self.assertRaises(ValueError): review(self.project, path, register=True)


if __name__ == "__main__":
    unittest.main()
