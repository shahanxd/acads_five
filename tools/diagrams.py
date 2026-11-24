"""SVG drawing helpers for study-doc diagrams (boxes, circles, data stores, arrows, actors, diamonds).
Use: from diagrams import *; save("path.svg", svg(w, h, body))"""
import math, html as H, pathlib
# ---------- SVG helpers ----------
FONT = "font-family:Arial,Helvetica,sans-serif"
LBL = "paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round"

def svg(w, h, body, maxh=None):
    st = f'max-height:{maxh}mm;' if maxh else ''
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'style="{st}{FONT}">'
            '<defs><marker id="ar" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="8" markerHeight="8" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker>'
            '<marker id="op" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="9" markerHeight="9" '
            'orient="auto"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#111" stroke-width="1.3"/></marker></defs>'
            f'{body}</svg>')

def text(x, y, lines, size=12, anchor='middle', bold=False, italic=False, label=False):
    if isinstance(lines, str): lines = [lines]
    lh = size * 1.2
    y0 = y - (len(lines) - 1) * lh / 2 + size * 0.35
    st = (LBL if label else '')
    fw = ' font-weight="bold"' if bold else ''
    fs = ' font-style="italic"' if italic else ''
    out = ''
    for i, ln in enumerate(lines):
        out += (f'<text x="{x}" y="{y0 + i*lh:.1f}" font-size="{size}" text-anchor="{anchor}"{fw}{fs} '
                f'style="{st}">{H.escape(ln)}</text>')
    return out

def lbl(x, y, lines, size=10.5, anchor='middle'):
    return text(x, y, lines, size, anchor, label=True)

def line(pts, arrow=True, both=False, dash=False, open_head=False):
    d = ' '.join(f'{x},{y}' for x, y in pts)
    m = ''
    if arrow: m += ' marker-end="url(#op)"' if open_head else ' marker-end="url(#ar)"'
    if both: m += ' marker-start="url(#ar)"'
    da = ' stroke-dasharray="6,4"' if dash else ''
    return f'<polyline points="{d}" fill="none" stroke="#111" stroke-width="1.3"{da}{m}/>'

def rect(x, y, w, h, lines, size=12.5, r=0, bold=False):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#111" stroke-width="1.4"/>'
            + text(x + w/2, y + h/2, lines, size, bold=bold))

def ellipse(cx, cy, rx, ry, lines, size=12):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" stroke="#111" stroke-width="1.3"/>'
            + text(cx, cy, lines, size))

def actor(x, y, name):
    s = '#111'
    return (f'<g stroke="{s}" stroke-width="1.5" fill="none">'
            f'<circle cx="{x}" cy="{y-30}" r="10" fill="#fff"/>'
            f'<line x1="{x}" y1="{y-20}" x2="{x}" y2="{y+10}"/>'
            f'<line x1="{x-16}" y1="{y-10}" x2="{x+16}" y2="{y-10}"/>'
            f'<line x1="{x}" y1="{y+10}" x2="{x-13}" y2="{y+32}"/>'
            f'<line x1="{x}" y1="{y+10}" x2="{x+13}" y2="{y+32}"/></g>'
            + text(x, y + 47, name, 12))

def proc(cx, cy, num, lines, r=44):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#111" stroke-width="1.4"/>'
            f'<line x1="{cx-r+6}" y1="{cy-r*0.42}" x2="{cx+r-6}" y2="{cy-r*0.42}" stroke="#111" stroke-width="0.9"/>'
            + text(cx, cy - r*0.62, num, 11, bold=True)
            + text(cx, cy + r*0.18, lines, 10.5))

def store(x, y, w, did, name, h=30):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="none"/>'
            f'<polyline points="{x+w},{y} {x},{y} {x},{y+h} {x+w},{y+h}" fill="none" stroke="#111" stroke-width="1.4"/>'
            f'<line x1="{x+34}" y1="{y}" x2="{x+34}" y2="{y+h}" stroke="#111" stroke-width="1.1"/>'
            + text(x + 17, y + h/2, did, 11, bold=True)
            + text(x + 34 + (w-34)/2, y + h/2, name, 11.5))

def edge(cx, cy, tx, ty, r=44):
    """Point on circle (cx,cy,r) facing (tx,ty)."""
    a = math.atan2(ty - cy, tx - cx)
    return (round(cx + r*math.cos(a), 1), round(cy + r*math.sin(a), 1))

def act(cx, y, w, lines, h=32):
    return rect(cx - w/2, y, w, h, lines, 11.5, r=12)

def diamond(cx, cy, hw, hh, lines, size=10.5):
    p = f'{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}'
    return f'<polygon points="{p}" fill="#fff" stroke="#111" stroke-width="1.4"/>' + text(cx, cy, lines, size)


def save(path, content):
    """Write an SVG file (standalone, with XML namespace and white background)."""
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(path).write_text(content, encoding='utf-8')

def ell_edge(cx, cy, rx, ry, tx, ty):
    """Point on an ellipse boundary facing (tx, ty)."""
    a = math.atan2((ty - cy) / ry, (tx - cx) / rx)
    return (round(cx + rx * math.cos(a), 1), round(cy + ry * math.sin(a), 1))
