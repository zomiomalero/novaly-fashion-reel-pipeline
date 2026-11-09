"""Human-readable preproduction timeline and checklist."""
from __future__ import annotations
import json
from pathlib import Path
from .config import schedule


def write_storyboard(project: dict, output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    timeline = schedule(project)
    lines = [f"# {project['project']['title']} - production storyboard", "",
             f"Format: {project['output']['width']}x{project['output']['height']} at {project['output']['fps']} fps",
             f"Runtime: {sum(x['frames'] for x in timeline) / project['output']['fps']:.2f} seconds", "",
             "| Look | Time | Palette | Woman | Man | Shot asset |", "|---|---|---|---|---|---|"]
    for row, s in zip(timeline, project["scenes"]):
        palette = " + ".join(c["name"] for c in s["colors"])
        safe = lambda x: str(x).replace("|", "/").replace("\n", " ")[:100]
        lines.append(f"| {row['index']:02d} | {row['start_s']:.2f}-{(row['start_s'] + row['duration_s']):.2f}s "
                     f"| {safe(palette)} | {safe(s.get('woman_outfit', ''))} | {safe(s.get('man_outfit', ''))} | `{row['asset']}` |")
    lines += ["", "## Original identities and location", "", json.dumps(project.get("cast", {}), indent=2),
              "", json.dumps(project.get("studio", {}), indent=2), "", "## Final human approval gates", "",
              "- [ ] Faces/hair/height/body ratio stay consistent across every scene.",
              "- [ ] Outfit colors, fabrics, shoes and accessories match the wardrobe specification.",
              "- [ ] Framing and background props remain stable at each hard cut.",
              "- [ ] Hands, fingers, facial gestures and garment folds behave naturally.",
              "- [ ] Dialogue/voiceover matches the visible look; no unplanned words.",
              "- [ ] Swatch labels are accurate and do not cover the models.",
              "- [ ] Soundtrack and media are licensed; rights/privacy are cleared.",
              "- [ ] Rendered MP4 passes automated QA and a real phone-screen watch.", ""]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
