"""Build a self-contained synthetic SMOKE TEST (not publishable fashion footage)."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from PIL import Image, ImageDraw
from .render import render

COLORS = [("#4E6D63", "#E5D9C5"), ("#813D45", "#DDC5AF"), ("#234B6A", "#EEE5DA")]


def create_demo(folder: str | Path, quick: bool = True) -> Path:
    root = Path(folder).expanduser().resolve()
    (root / "assets").mkdir(parents=True, exist_ok=True)
    width, height, fps = 360, 640, 24
    scenes = []
    for idx, (a, b) in enumerate(COLORS, 1):
        im = Image.new("RGB", (width, height), "#CFC2AF")
        d = ImageDraw.Draw(im)
        for x in range(0, width, 18):
            d.line((x, 0, x, height), fill="#CABCA6", width=2)
        d.rectangle((width - 90, int(height*.55), width, height), fill="#81705E")
        d.ellipse((55, 115, 122, 188), fill="#D5AA90")
        d.ellipse((228, 115, 295, 188), fill="#AC7D61")
        d.rounded_rectangle((40, 185, 136, 400), radius=25, fill=a)
        d.rounded_rectangle((211, 185, 310, 400), radius=25, fill=b)
        d.polygon([(42, 400), (86, 400), (74, 566), (36, 566)], fill="#27272B")
        d.polygon([(95, 400), (132, 400), (144, 566), (101, 566)], fill="#27272B")
        d.polygon([(213, 400), (252, 400), (247, 566), (210, 566)], fill="#343434")
        d.polygon([(271, 400), (310, 400), (318, 566), (281, 566)], fill="#343434")
        d.text((25, 590), "TEST IMAGES ONLY", fill="#4D4137")
        name=f"look_{idx:02d}.png"
        im.save(root / "assets" / name)
        scenes.append({"id": f"look_{idx:02d}", "title": "Synthetic pairing", "duration": 1.0,
                       "asset": f"assets/{name}", "colors": [{"name": "color A", "hex": a}, {"name": "color B", "hex": b}],
                       "woman_outfit": "Placeholder sweater", "man_outfit": "Placeholder trousers"})
    config = {"project": {"title": "Synthetic pipeline smoke test", "brand": ""},
              "output": {"width": width, "height": height, "fps": fps, "crf": 22},
              "cast": {"woman_identity": "Original adult female model", "man_identity": "Original adult male model"},
              "studio": {"description": "Cream pleated fabric, warm studio"}, "audio": {}, "scenes": scenes}
    config_path = root / "project.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return render(config_path, root / "demo.mp4", workdir=root, quick=quick)
