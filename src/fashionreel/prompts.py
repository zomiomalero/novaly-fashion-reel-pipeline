"""Image first-frame and short video prompts for external generative tools."""
from __future__ import annotations
import csv
from pathlib import Path
from .config import schedule


def base_directive(project: dict) -> str:
    people = project.get("cast", {})
    world = project.get("studio", {})
    return (
        "Original photorealistic 9:16 fashion editorial photograph. Two fully original adult models, both head to shoes "
        "in a static straight-on full-body camera view. Preserve the SAME fictional individuals in every outfit. "
        f"WOMAN IDENTITY: {people.get('woman_identity', 'Use the supplied original woman character sheet.')}. "
        f"MAN IDENTITY: {people.get('man_identity', 'Use the supplied original man character sheet.')}. "
        f"STUDIO: {world.get('description', 'A warm ivory editorial studio with soft diffused light.')}. "
        "Same facial identities, realistic skin pores and hands, natural body proportions, authentic woven fabric, "
        "hem lines, properly fitting shoes, soft contact shadows and consistent lighting. "
        "The people stand in their stable left-right floor positions. No writing or graphic overlays."
    )


def still_prompt(project: dict, scene: dict, index: int, total: int) -> str:
    return (base_directive(project) + " "
            f"WARDROBE LOOK {index} OF {total}. "
            f"WOMAN WARDROBE: {scene.get('woman_outfit', 'Original tailored outfit as specified.')}. "
            f"MAN WARDROBE: {scene.get('man_outfit', 'Original complementary outfit as specified.')}. "
            "Fashion catalogue quality, crisp garments, visible shoe silhouettes, calm relaxed expressions. "
            "Create one unambiguous completed outfit photograph as the first frame for this look.")


def scene_prompt(project: dict, scene: dict, index: int, total: int) -> str:
    gestures = scene.get("action") or "Woman makes a small natural hand gesture. Man shifts his weight slightly."
    return (
        "Photorealistic 9:16 fashion video. Animate the ATTACHED original outfit first-frame photograph. "
        "Keep the SAME fictional individuals, exact faces, hair, bodies, outfits and full-body framing from that image. "
        f"WOMAN WARDROBE: {scene.get('woman_outfit', 'Keep the attached completed outfit')}. "
        f"MAN WARDROBE: {scene.get('man_outfit', 'Keep the attached completed outfit')}. "
        f"ACTION: {gestures} "
        "Gentle breathing, real cloth folds, natural hands, subtle facial movement. One fixed front camera, "
        "one continuous shot and unchanged studio. No artificial captions, labels or overlays."
    )


def build_prompt_pack(project: dict, out_dir: str | Path) -> Path:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    images = target / "FIRST_FRAMES"
    images.mkdir(exist_ok=True)
    people = project.get("cast", {})
    studio = project.get("studio", {})
    (target / "ORIGINAL_WOMAN_SHEET.txt").write_text(
        "Create an ORIGINAL fictional adult female model character sheet, full-body front and three-quarter poses "
        "with consistent close facial detail, natural skin and anatomy, simple neutral clothing. "
        f"Identity: {people.get('woman_identity', 'An original adult woman with stable proportions.')}. "
        "Photorealistic editorial photography, no text or logos, 9:16.\n", encoding="utf-8")
    (target / "ORIGINAL_MAN_SHEET.txt").write_text(
        "Create an ORIGINAL fictional adult male model character sheet, full-body front and three-quarter poses "
        "with consistent close facial detail, natural skin and anatomy, simple neutral clothing. "
        f"Identity: {people.get('man_identity', 'An original adult man with stable proportions.')}. "
        "Photorealistic editorial photography, no text or logos, 9:16.\n", encoding="utf-8")
    (target / "STUDIO_MASTER.txt").write_text(
        "Create an ORIGINAL empty fashion studio master reference plate, 9:16 vertical photography. "
        f"Exact locked set: {studio.get('description', 'Warm ivory editorial studio, soft lighting, neutral floor.')}. "
        "Show the full empty two-presenter standing area and visible floor. Unchanged camera position and lens, "
        "natural shadows, no people and no typography.\n", encoding="utf-8")
    timing = schedule(project)
    rows = []
    instructions = [
        "# Original fashion reel production prompt pack",
        "",
        "1. Generate two ORIGINAL adult cast identity sheets using the WOMAN and MAN prompt files.",
        "2. Generate the original empty studio master plate with STUDIO_MASTER.txt.",
        "3. Generate one completed outfit still for each look using FIRST_FRAMES/*.txt plus BOTH cast sheets and studio plate.",
        "4. Generate one video per look using the shorter numbered video prompt and that exact look's still.",
        "5. Set duration separately from the video prompt. See the timing rows below.",
        "6. Do not use the previous OUTFIT's last frame alone as the new outfit reference; this can morph clothes.",
        "7. Keep model-generated videos clean; graphics and voice/audio are handled locally during editing.",
        "",
    ]
    for row, scene in zip(timing, project["scenes"]):
        slug = str(scene["id"])
        video_file = target / f"{row['index']:02d}_{slug}.txt"
        image_file = images / f"{row['index']:02d}_{slug}_FIRST_FRAME.txt"
        video_file.write_text(scene_prompt(project, scene, row["index"], len(timing)) + "\n", encoding="utf-8")
        image_file.write_text(still_prompt(project, scene, row["index"], len(timing)) + "\n", encoding="utf-8")
        instructions.extend([f"## {row['index']:02d}: {scene.get('title', slug)}",
                             f"Set clip length: {row['duration_s']:.2f} seconds at {project['output']['fps']} fps.",
                             f"Expected output: {scene['asset']}", f"First-frame prompt: FIRST_FRAMES/{image_file.name}",
                             f"Video animation prompt: {video_file.name}", ""])
        rows.append([row["index"], scene["id"], row["duration_s"], row["first_frame"],
                     row["end_frame_exclusive"], scene["asset"], scene.get("title", "")])
    (target / "INSTRUCTIONS.md").write_text("\n".join(instructions) + "\n", encoding="utf-8")
    with (target / "SHOT_MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        wr = csv.writer(handle)
        wr.writerow(["look", "id", "duration_s", "first_frame", "end_frame_exclusive", "asset", "title"])
        wr.writerows(rows)
    return target
