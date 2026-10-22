"""Generates the Fluent-style icons (SVG -> PNG 512 + multi-size ICO).

Usage:
    python generate_icons.py <output_dir> [pdf24|pdfgear]

Requires Pillow (`pip install pillow`) and Inkscape on PATH (used to render the SVGs).
Edit the APPS table to change colours, glyphs or layout ("bands", "quad", "steps").
"""
import os, subprocess, sys, colorsys
from PIL import Image, ImageDraw

OUT = sys.argv[1]
for d in ("svg", "png", "ico"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

# (nombre, claro, medio, oscuro, glifo, composición)
APPS = [
    ("PDF24",     "#FF8A6E", "#E8402F", "#A3121C", "sheep",    "bands"),
    ("Creator",   "#FFC27A", "#F5821F", "#B44A06", "plus",     "steps"),
    ("Toolbox",   "#7CC4FF", "#2B7DF0", "#0E44B0", "grid",     "quad"),
    ("Compress",  "#8BE6A8", "#22A65C", "#0B6236", "compress", "bands"),
    ("OCR",       "#CFA8FF", "#8352E8", "#4A1FA8", "scan",     "steps"),
    ("Reader",    "#6FE3DC", "#13A8AA", "#05636E", "eye",      "quad"),
    ("Fax",       "#FF9FCB", "#DB3A8E", "#8C1257", "send",     "bands"),
    ("Assistant", "#9FB0FF", "#4F5FEA", "#262E9A", "spark",    "steps"),
    ("DocTool",   "#FFDA70", "#EBA614", "#975C00", "pages",    "quad"),
    ("Settings",  "#C3CCD6", "#71808F", "#36414F", "gear",     "bands"),
]
GEAR = [("PDFgear", "#FF7E93", "#E21E3C", "#930823", "g", "steps")]
SET = sys.argv[2] if len(sys.argv) > 2 else "pdf24"
PREFIX = "PDF24" if SET == "pdf24" else "PDFgear"
if SET == "pdfgear":
    APPS = GEAR

def shift(h, deg, dl=0.0):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    H, L, S = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb((H + deg / 360) % 1, min(1, max(0, L + dl)), S)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))

W = "#FFFFFF"
# Glifos dibujados centrados en (82,154), ~64 px de alto
G = {
 "sheep": """
<g fill="#fff">
 <circle cx="82" cy="150" r="27"/>
 <circle cx="82" cy="122" r="12"/><circle cx="101" cy="128" r="12"/><circle cx="109" cy="146" r="12"/>
 <circle cx="104" cy="166" r="12"/><circle cx="60" cy="166" r="12"/><circle cx="55" cy="146" r="12"/><circle cx="63" cy="128" r="12"/>
</g>
<ellipse cx="61" cy="152" rx="10" ry="5.5" fill="#E2BC8C" transform="rotate(28 61 152)"/>
<ellipse cx="103" cy="152" rx="10" ry="5.5" fill="#E2BC8C" transform="rotate(-28 103 152)"/>
<path d="M82 136c11 0 18 8 18 20 0 14-8 26-18 26s-18-12-18-26c0-12 7-20 18-20z" fill="#F6DFBC"/>
<circle cx="75" cy="150" r="7.5" fill="#fff" stroke="#3a2a1a" stroke-width="1.8"/>
<circle cx="89" cy="150" r="7.5" fill="#fff" stroke="#3a2a1a" stroke-width="1.8"/>
<circle cx="76.8" cy="151" r="3.4" fill="#1d1d1d"/><circle cx="87.2" cy="151" r="3.4" fill="#1d1d1d"/>
<ellipse cx="82" cy="168" rx="7.5" ry="4.8" fill="#D59B6E"/>
<path d="M76 176q6 4 12 0" stroke="#8a5530" stroke-width="2.2" fill="none" stroke-linecap="round"/>""",
 "g": '<text x="84" y="183" font-family="Segoe Script" font-weight="700" font-size="92" fill="#fff" text-anchor="middle">g</text>',
 "plus": f'<path d="M82 122v64M50 154h64" stroke="{W}" stroke-width="15" stroke-linecap="round" fill="none"/>',
 "grid": f'<g fill="{W}"><rect x="50" y="122" width="28" height="28" rx="7"/><rect x="86" y="122" width="28" height="28" rx="7" opacity=".65"/><rect x="50" y="158" width="28" height="28" rx="7" opacity=".65"/><rect x="86" y="158" width="28" height="28" rx="7"/></g>',
 "compress": f'<g stroke="{W}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M82 118v26M68 131l14 14 14-14"/><path d="M82 190v-26M68 177l14-14 14 14"/></g>',
 "scan": f'<g stroke="{W}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M50 136v-14h14M100 122h14v14M114 172v14h-14M64 186H50v-14"/></g><path d="M82 132l-15 32h7.5l3-7.5h9l3 7.5h7.5zM78.5 150.5l3.5-9 3.5 9z" fill="{W}" fill-rule="evenodd"/>',
 "eye": f'<path d="M46 154c11-20 23-29 36-29s25 9 36 29c-11 20-23 29-36 29s-25-9-36-29z" stroke="{W}" stroke-width="10" stroke-linejoin="round" fill="none"/><circle cx="82" cy="154" r="12" fill="{W}"/>',
 "send": f'<path d="M48 152l66-28-24 62-13-25z" fill="{W}" stroke="{W}" stroke-width="7" stroke-linejoin="round"/><path d="M77 161l37-37" stroke="url(#bd)" stroke-width="5" stroke-linecap="round"/>',
 "spark": f'<path d="M80 116c3.5 19 10 25.5 29 29-19 3.5-25.5 10-29 29-3.5-19-10-25.5-29-29 19-3.5 25.5-10 29-29z" fill="{W}"/><path d="M108 164c1.2 8 3.5 10.3 11.5 11.5-8 1.2-10.3 3.5-11.5 11.5-1.2-8-3.5-10.3-11.5-11.5 8-1.2 10.3-3.5 11.5-11.5z" fill="{W}" opacity=".85"/>',
 "pages": f'<rect x="48" y="120" width="42" height="50" rx="9" fill="{W}" opacity=".6"/><rect x="74" y="138" width="42" height="50" rx="9" fill="{W}"/>',
 "gear": f'<circle cx="82" cy="154" r="23" stroke="{W}" stroke-width="11" fill="none"/><circle cx="82" cy="154" r="32" stroke="{W}" stroke-width="13" fill="none" stroke-dasharray="12.57 12.57"/>',
}

# Cuerpo: x 32..224, y 8..248 (vertical, como Microsoft 365)
BX, BY, BW, BH, R = 32, 8, 192, 240, 26

def layers(kind):
    """Capas superpuestas sobre el fondo (relleno, forma)."""
    if kind == "bands":   # como Word
        return [("url(#c2)", f'<rect x="{BX}" y="88" width="{BW}" height="200" rx="{R}"/>'),
                ("url(#c3)", f'<rect x="{BX}" y="168" width="{BW}" height="120" rx="{R}"/>')]
    if kind == "quad":    # como Excel
        return [("url(#c2)", f'<rect x="{BX}" y="88" width="{BW}" height="200" rx="{R}"/>'),
                ("url(#c3)", '<path d="M154 88h70v200H32v-120h96V114a26 26 0 0 1 26-26z"/>'),
                ("url(#c0)", f'<rect x="128" y="-20" width="120" height="108" rx="{R}"/>')]
    if kind == "steps":   # como OneNote
        return [("url(#c2)", f'<rect x="128" y="88" width="140" height="200" rx="{R}"/>'),
                ("url(#c3)", f'<rect x="{BX}" y="168" width="{BW}" height="120" rx="{R}"/>')]

def svg(lt, md, dk, glyph, kind):
    sh = shift(lt, -22, 0.02)     # toque de matiz arriba a la derecha
    sh2 = shift(md, -14)
    hi = shift(lt, 0, 0.08)
    body = "\n ".join(f'<g filter="url(#ls)" fill="{f}">{s}</g>' for f, s in layers(kind))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
<defs>
 <linearGradient id="c1" x1="0" y1="0" x2="1" y2="0.25"><stop offset="0" stop-color="{hi}"/><stop offset=".5" stop-color="{lt}"/><stop offset="1" stop-color="{sh}"/></linearGradient>
 <linearGradient id="c0" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shift(lt,0,0.1)}"/><stop offset="1" stop-color="{sh}"/></linearGradient>
 <linearGradient id="c2" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="{shift(md,0,0.06)}"/><stop offset="1" stop-color="{sh2}"/></linearGradient>
 <linearGradient id="c3" x1="0" y1="0" x2="1" y2="0.5"><stop offset="0" stop-color="{shift(dk,0,-0.03)}"/><stop offset="1" stop-color="{shift(dk,-14,0.08)}"/></linearGradient>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shift(md,6,0.04)}"/><stop offset="1" stop-color="{shift(dk,4,-0.04)}"/></linearGradient>
 <linearGradient id="bh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <filter id="ls" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dy="-3"/><feComponentTransfer><feFuncA type="linear" slope=".28"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dx="2" dy="5"/><feComponentTransfer><feFuncA type="linear" slope=".38"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <clipPath id="pc"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="{R}"/></clipPath>
</defs>
<g clip-path="url(#pc)">
 <rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="url(#c1)"/>
 {body}
</g>
<g filter="url(#sh)">
 <rect x="4" y="116" width="108" height="108" rx="22" fill="url(#bd)"/>
 <rect x="4" y="116" width="108" height="108" rx="22" fill="url(#bh)"/>
</g>
<g transform="translate(58 170) scale(.98) translate(-82 -154)">{G[glyph]}</g>
</svg>'''

SIZES = [16, 24, 32, 48, 64, 128, 256]

def doc_svg(lt, md, dk, glyph):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
<defs>
 <linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF0F3"/></linearGradient>
 <linearGradient id="fd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4E7EB"/><stop offset="1" stop-color="#C9CED5"/></linearGradient>
 <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shift(md,6,0.04)}"/><stop offset="1" stop-color="{shift(dk,4,-0.04)}"/></linearGradient>
 <linearGradient id="bh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <filter id="ps" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="4"/><feOffset dy="3"/><feComponentTransfer><feFuncA type="linear" slope=".22"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dx="2" dy="5"/><feComponentTransfer><feFuncA type="linear" slope=".38"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g filter="url(#ps)">
 <path d="M56 8h114l58 58v164a18 18 0 0 1-18 18H56a18 18 0 0 1-18-18V26A18 18 0 0 1 56 8z" fill="url(#pg)" stroke="#C3C8CF" stroke-width="2"/>
</g>
<path d="M170 8v40a18 18 0 0 0 18 18h40z" fill="url(#fd)" stroke="#C3C8CF" stroke-width="2" stroke-linejoin="round"/>
<g fill="{md}">
 <rect x="128" y="96" width="74" height="12" rx="6" opacity=".9"/>
 <rect x="128" y="124" width="74" height="12" rx="6" opacity=".55"/>
 <rect x="128" y="152" width="74" height="12" rx="6" opacity=".55"/>
 <rect x="128" y="180" width="54" height="12" rx="6" opacity=".55"/>
</g>
<g filter="url(#sh)">
 <rect x="4" y="116" width="108" height="108" rx="22" fill="url(#bd)"/>
 <rect x="4" y="116" width="108" height="108" rx="22" fill="url(#bh)"/>
</g>
<g transform="translate(58 170) scale(.98) translate(-82 -154)">{G[glyph]}</g>
</svg>'''
tiles = []
for name, lt, md, dk, gl, kind in APPS:
    p = f"{OUT}/svg/{PREFIX}-{name}.svg".replace("PDFgear-PDFgear","PDFgear")
    open(p, "w", encoding="utf-8").write(svg(lt, md, dk, gl, kind))
    png = f"{OUT}/png/{PREFIX}-{name}.png".replace("PDFgear-PDFgear","PDFgear")
    subprocess.run(["inkscape", p, "-o", png, "-w", "1024", "-h", "1024"], check=True, capture_output=True, shell=True)
    im = Image.open(png).convert("RGBA")
    im.save(f"{OUT}/ico/{PREFIX}-{name}.ico".replace("PDFgear-PDFgear","PDFgear"), sizes=[(s, s) for s in SIZES])
    im.resize((512, 512), Image.LANCZOS).save(png)
    tiles.append((name, im))
    print("ok", name, flush=True)

if SET == "pdfgear":
    name, lt, md, dk, gl, kind = GEAR[0]
    p = f"{OUT}/svg/PDFgear-Documento-PDF.svg"
    open(p, "w", encoding="utf-8").write(doc_svg(lt, md, dk, gl))
    png = f"{OUT}/png/PDFgear-Documento-PDF.png"
    subprocess.run(["inkscape", p, "-o", png, "-w", "1024", "-h", "1024"], check=True, capture_output=True, shell=True)
    im = Image.open(png).convert("RGBA")
    im.save(f"{OUT}/ico/PDFgear-Documento-PDF.ico", sizes=[(s, s) for s in SIZES])
    im.resize((512, 512), Image.LANCZOS).save(png)
    tiles.append(("Documento .pdf", im))

cols, cell = min(5, len(tiles)), 220
rows = (len(tiles) + cols - 1) // cols
for tag, bg, fg in (("claro", (243, 243, 243), (40, 40, 40)), ("oscuro", (32, 32, 32), (230, 230, 230))):
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 24)), bg)
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(tiles):
        x, y = (i % cols) * cell, (i // cols) * (cell + 24)
        t = im.resize((176, 176), Image.LANCZOS)
        sheet.paste(t, (x + 22, y + 10), t)
        d.text((x + 22, y + 192), n, fill=fg)
    sheet.save(f"{OUT}/Vista-previa-{tag}.png")
small = Image.new("RGB", (cols * 120, rows * 70), (243, 243, 243))
for i, (n, im) in enumerate(tiles):
    x, y = (i % cols) * 120 + 10, (i // cols) * 70 + 10
    for k, s in enumerate((48, 32, 16)):
        t = im.resize((s, s), Image.LANCZOS)
        small.paste(t, (x + [0, 52, 90][k], y + 8), t)
small.save(f"{OUT}/Vista-previa-pequenos.png")
