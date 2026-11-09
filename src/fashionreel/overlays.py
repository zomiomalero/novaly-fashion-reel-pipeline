"""Minimal, retina-sharp overlays composited after model generation."""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONTS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Helvetica Neue.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]


def font(size: int, path: str | None = None) -> ImageFont.ImageFont:
    for candidate in ([path] if path else []) + FONTS:
        try:
            if candidate: return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def overlay(scene: dict, width: int, height: int, index: int, total: int,
            brand: str = "", out_path: str | Path | None = None) -> Image.Image:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    k = width / 1080
    title_font = font(round(34 * k))
    meta_font = font(round(24 * k))
    low_font = font(round(39 * k))
    colors = scene.get("colors", [])
    formula = str(scene.get("formula", "")).strip()
    names = formula if formula else "  +  ".join(c["name"].lower() for c in colors)
    shown_colors = [] if formula else colors
    swatch = round(46 * k)
    spacing = round(16 * k)
    tw = draw.textbbox((0, 0), names, font=title_font)[2]
    capsule_w = max(round(280 * k), tw + 2 * round(42 * k) + len(shown_colors) * (swatch + spacing))
    capsule_w = min(capsule_w, width - round(80 * k))
    cap_h = round(104 * k)
    left = (width - capsule_w) // 2
    top = int(height * 0.103)
    draw.rounded_rectangle((left, top, left + capsule_w, top + cap_h), radius=round(26 * k), fill=(25, 25, 28, 177))
    cursor = left + round(34 * k)
    for c in shown_colors:
        col = c["hex"]
        sy = top + (cap_h - swatch) // 2
        draw.rounded_rectangle((cursor, sy, cursor + swatch, sy + swatch), radius=round(8 * k), fill=col,
                               outline=(245, 245, 245, 210), width=max(1, round(2 * k)))
        cursor += swatch + spacing
    label_x = min(cursor + (round(4 * k) if shown_colors else 0), left + capsule_w - round(20 * k))
    # End labels before the capsule edge; font size drops gracefully for long combinations.
    avail = left + capsule_w - round(20 * k) - label_x
    while tw > avail and getattr(title_font, "size", 18) > 17:
        title_font = font(title_font.size - 1)
        tw = draw.textbbox((0, 0), names, font=title_font)[2]
    draw.text((label_x, top + cap_h // 2), names, font=title_font, anchor="lm", fill=(250, 248, 247, 250))
    if brand:
        brand = brand.upper()[:28]
        draw.text((round(54 * k), round(78 * k)), brand, font=meta_font,
                  fill=(255, 255, 255, 232), stroke_width=max(1, round(2 * k)), stroke_fill=(26, 22, 19, 110))
    if scene.get("emphasis"):
        phrase = str(scene["emphasis"]).strip()[:45]
        bbox = draw.textbbox((0, 0), phrase, font=low_font)
        if bbox[2] < width * 0.88:
            draw.text((width // 2, int(height * 0.65)), phrase, font=low_font, anchor="mm",
                      fill=(250, 250, 250, 245), stroke_width=max(1, round(3 * k)), stroke_fill=(20, 20, 20, 180))
    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
    return image
