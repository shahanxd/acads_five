"""Draw a VS Code (Dark Modern) integrated-terminal panel as a PNG."""
from PIL import Image, ImageDraw, ImageFont

S = 2                                   # render scale
F = r'C:\Windows\Fonts\consola.ttf'
UI = r'C:\Windows\Fonts\segoeui.ttf'
UIB = r'C:\Windows\Fonts\segoeuib.ttf'
SYM = r'C:\Windows\Fonts\seguisym.ttf'

BG = (24, 24, 24)
BORDER = (43, 43, 43)
FG = (204, 204, 204)
DIM = (157, 157, 157)
YEL = (229, 229, 16)
BLUE = (0, 120, 212)
PROMPT = 'PS C:\\Users\\shaha\\Desktop\\CN Lab> '

mono = ImageFont.truetype(F, 14 * S)
ui = ImageFont.truetype(UI, 11 * S)
uib = ImageFont.truetype(UI, 11 * S)
ui12 = ImageFont.truetype(UI, 13 * S)
CW = mono.getlength('M')
LH = 19 * S


def _wrap(line, cols):
    if not line:
        return ['']
    return [line[i:i + cols] for i in range(0, len(line), cols)]


def shot(runs, out, width=1080, tabs=None, active=0, running=False, min_lines=0, label=None):
    """runs: list of (command, output_text). running=True: last command still running (no final prompt)."""
    list_w = 170 * S if tabs else 0
    W = width * S
    text_x = 22 * S
    cols = int((W - list_w - text_x - 14 * S) // CW)

    # build rows: (kind, text)  kind: 'cmd' | 'out'
    rows = []
    for cmd, outp in runs:
        rows.append(('cmd', cmd))
        lines = outp.rstrip('\n').split('\n')
        for ln in lines:
            for piece in _wrap(ln, cols):
                rows.append(('out', piece))
    if not running:
        rows.append(('cmd', ''))
    else:
        rows.append(('pad', ''))
    rows += [('pad', '')] * max(0, min_lines - len(rows))

    head = 35 * S
    H = head + 8 * S + LH * len(rows) + 12 * S
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # panel header
    d.line([(0, 0), (W, 0)], fill=BORDER, width=S)
    x = 18 * S
    for name in ['PROBLEMS', 'OUTPUT', 'DEBUG CONSOLE', 'TERMINAL', 'PORTS']:
        f = uib if name == 'TERMINAL' else ui
        col = (231, 231, 231) if name == 'TERMINAL' else DIM
        d.text((x, 11 * S), name, font=f, fill=col)
        tw = d.textlength(name, font=f)
        if name == 'TERMINAL':
            d.line([(x, 31 * S), (x + tw, 31 * S)], fill=BLUE, width=S)
        x += tw + 24 * S
    # right-side header icons
    sym = ImageFont.truetype(SYM, 13 * S)
    ix = W - 14 * S
    for ch in ['\u2715', '\u02c4', '\u22ef', '\U0001F5D1', '\u25eb', '\u02c5', '+']:
        try:
            tw = d.textlength(ch, font=sym)
        except Exception:
            continue
        ix -= tw + 14 * S
        d.text((ix, 8 * S), ch, font=sym, fill=DIM)
    if not tabs:
        lab = label or ('python' if running else 'powershell')
        d.text((ix - 24 * S - d.textlength(lab, font=ui12), 9 * S), lab, font=ui12, fill=DIM)

    # terminal tab list on the right
    if tabs:
        lx = W - list_w
        d.line([(lx, head), (lx, H)], fill=BORDER, width=S)
        for i, t in enumerate(tabs):
            y = head + 4 * S + i * 22 * S
            if i == active:
                d.rectangle([lx + S, y, W, y + 22 * S], fill=(55, 55, 61))
                d.line([(lx + S, y), (lx + S, y + 22 * S)], fill=BLUE, width=S)
            # little terminal icon
            d.rectangle([lx + 14 * S, y + 6 * S, lx + 26 * S, y + 16 * S], outline=DIM, width=S)
            d.text((lx + 16 * S, y + 5 * S), '>', font=ImageFont.truetype(F, 8 * S), fill=DIM)
            d.text((lx + 34 * S, y + 3 * S), t, font=ui12, fill=(220, 220, 220) if i == active else DIM)

    # content
    y = head + 8 * S
    for kind, txt in rows:
        if kind == 'cmd':
            # shell-integration decoration dot
            d.ellipse([7 * S, y + 6 * S, 13 * S, y + 12 * S], outline=(120, 120, 120), width=S)
            d.text((text_x, y), PROMPT, font=mono, fill=FG)
            cx = text_x + mono.getlength(PROMPT)
            if txt:
                exe, _, rest = txt.partition(' ')
                d.text((cx, y), exe, font=mono, fill=YEL)
                cx += mono.getlength(exe + ' ')
                d.text((cx, y), rest, font=mono, fill=FG)
                cx += mono.getlength(rest)
            else:
                d.rectangle([cx, y + 1 * S, cx + CW, y + LH - 2 * S], fill=FG)   # cursor
        elif kind == 'out':
            d.text((text_x, y), txt, font=mono, fill=FG)
        y += LH
    if running:
        # cursor sitting after the last line of a still-running server
        d.rectangle([text_x, y - LH + 1 * S, text_x + CW, y - 2 * S], outline=FG, width=S)

    img.save(out, optimize=True)
    return out
