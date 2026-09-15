"""Generate the [yoe] logo assets in static/images/.

Renders "[yoe]" as embedded glyph outlines (no font dependency in the
SVG) using Fira Code Medium, which matches the site's monospace stack,
in amber like a terminal. The header logo is transparent so it sits on
whatever background the page provides; the square logo carries a black
backdrop because favicons and social cards need an opaque ground.

This is the single source for the [yoe] mark. The yoebuild/yoe repo
carries copies of these files rather than its own generator:

    static/images/yoe-logo-amber-on-black.svg -> docs/yoe-logo-amber-on-black.svg
    static/images/yoe-logo-white-on-black.svg -> docs/yoe-logo-white-on-black.svg
    static/images/yoe-logo-black-on-white.svg -> docs/yoe-logo-black-on-white.svg
    static/images/yoe-logo-square.svg         -> assets/yoe-logo-square.svg, theme/favicon.svg
    static/images/yoe-logo-square.png         -> assets/yoe-logo-square.png, theme/favicon.png

Usage:
    python scripts/gen-logo.py
    rsvg-convert -w 1024 -h 1024 static/images/yoe-logo-square.svg -o static/images/yoe-logo-square.png
    rsvg-convert -w 64 -h 64 static/images/yoe-logo-square.svg -o static/images/favicon.png

Requires fontTools and the Fira Code font (path below).
"""
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = "/usr/share/fonts/TTF/FiraCodeNerdFont-Medium.ttf"
TEXT = "[yoe]"
AMBER = "#e8863a"  # $accent in sass/main.scss
BLACK = "#000000"  # $bg-code in sass/main.scss
WHITE = "#ffffff"

OUT = Path(__file__).resolve().parent.parent / "static" / "images"

font = TTFont(FONT)
cmap = font.getBestCmap()
glyphs = font.getGlyphSet()

# Build one combined path, y-flipped (font coords -> SVG coords), advancing x.
pen = SVGPathPen(glyphs)
bpen = BoundsPen(glyphs)
x = 0
for ch in TEXT:
    g = glyphs[cmap[ord(ch)]]
    t = Transform(1, 0, 0, -1, x, 0)
    g.draw(TransformPen(pen, t))
    g.draw(TransformPen(bpen, t))
    x += g.width
path = pen.getCommands()
xmin, ymin, xmax, ymax = bpen.bounds
w, h = xmax - xmin, ymax - ymin


def svg(width, height, scale, tx, ty, fg, bg=None):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
    )
    if bg:
        parts.append(f'  <rect width="{width}" height="{height}" fill="{bg}"/>')
    parts.append(f'  <g transform="translate({tx:.2f}, {ty:.2f}) scale({scale:.6f})">')
    parts.append(f'    <path d="{path}" fill="{fg}"/>')
    parts.append("  </g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# Wide logos, normalized to 100 px tall. The site header uses the transparent
# one; the variants on a background are for READMEs and other pages whose
# theme we do not control.
pad = 0.30 * h
s = 100.0 / (h + 2 * pad)
W = round((w + 2 * pad) * s, 2)
tx, ty = (pad - xmin) * s, (pad - ymin) * s

for name, fg, bg in [
    ("yoe-logo-amber", AMBER, None),
    ("yoe-logo-amber-on-black", AMBER, BLACK),
    ("yoe-logo-white-on-black", WHITE, BLACK),
    ("yoe-logo-black-on-white", BLACK, WHITE),
]:
    (OUT / f"{name}.svg").write_text(svg(W, 100, s, tx, ty, fg, bg=bg))
    print(f"wrote {name}.svg {W} x 100")

# Square logo: 360x360, text ~78% of width, centered.
SQ = 360
s2 = (SQ * 0.78) / w
tx2 = (SQ - w * s2) / 2 - xmin * s2
ty2 = (SQ - h * s2) / 2 - ymin * s2
(OUT / "yoe-logo-square.svg").write_text(svg(SQ, SQ, s2, tx2, ty2, AMBER, bg=BLACK))
print("wrote yoe-logo-square.svg 360x360")
