"""Procedural hibiscus -> coloured character art (mostly 0s and 1s) as HTML spans.

render() builds an RGB image plus a 'kind' map (petal, vein, eye, column, pollen, ...);
to_art() samples it on a character grid and picks a glyph per cell.
"""
import math
import numpy as np

W, H = 1100, 1000
CX, CY, R0 = 600, 480, 360

BG, PETAL, VEIN, SEAM, RIM, EYE, COLUMN, POLLEN, STIGMA, LEAF, LVEIN, STEM, BUD = range(13)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    t = np.asarray(t)[..., None]
    return np.asarray(a, float) * (1 - t) + np.asarray(b, float) * t


def render(seed=7):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    img = np.zeros((H, W, 3))
    kind = np.zeros((H, W), np.int8)
    ang = np.zeros((H, W))            # stroke direction for line-like cells

    # ---------------- leaves (behind) ----------------
    def leaf(bx, by, a, L, Wd, dark=1.0):
        ca, sa = math.cos(a), math.sin(a)
        dx, dy = xx - bx, yy - by
        u = (dx * ca + dy * sa) / L
        v = (-dx * sa + dy * ca)
        uu = np.clip(u, 0, 1)
        hw = Wd * np.sin(np.pi * uu ** 0.75) ** 0.9 * (1 - 0.15 * uu)
        hw = hw * (1 + 0.05 * np.sin(uu * 70))                      # serrated edge
        inside = (u > 0) & (u < 1) & (np.abs(v) < hw)
        t = np.abs(v) / np.maximum(hw, 1e-6)
        base = mix((18, 80, 40), (62, 140, 60), uu * 0.7 + 0.3 * (1 - t))
        side = np.where(v > 0, 0.78, 1.0) * dark
        col = base * side[..., None]
        # veins: midrib + side veins sweeping to the tip
        mid = np.abs(v) < 2.2 + 2.5 * (1 - uu)
        sv = np.abs(((uu * L - np.abs(v) * 0.75) % (L / 9)) - L / 18) < 1.6
        sv &= (t < 0.9) & (uu > 0.06) & (uu < 0.93)
        col = np.where((mid | sv)[..., None], mix((110, 170, 90), (150, 200, 120), uu), col)
        m = inside & (kind == BG)
        img[m] = col[m]
        kind[m] = LEAF
        vm = m & sv & ~mid
        kind[vm] = LVEIN
        gap = m & mid
        kind[gap] = BG
        img[gap] = 0
        ang[vm & mid] = a
        ang[vm & ~mid] = a + np.where(v[vm & ~mid] > 0, 0.75, -0.75)

    leaf(CX - 40, CY + 60, math.radians(150), 1.45 * R0, 0.36 * R0)
    leaf(CX + 30, CY + 60, math.radians(28), 1.25 * R0, 0.32 * R0, dark=0.92)
    leaf(CX - 20, CY + 40, math.radians(100), 1.3 * R0, 0.3 * R0, dark=0.85)

    # ---------------- stem + bud (upper left) ----------------
    bx, by = CX - 1.12 * R0, CY - 0.78 * R0
    # stem: quadratic curve from flower centre region to bud
    ts = np.linspace(0, 1, 400)
    ba0 = math.radians(-118)
    p0 = np.array([CX - 0.35 * R0, CY - 0.1 * R0])
    p2 = np.array([bx, by]) - 0.13 * R0 * np.array([math.cos(ba0), math.sin(ba0)])
    p1 = np.array([CX - 1.05 * R0, CY - 0.05 * R0])
    pts = ((1 - ts) ** 2)[:, None] * p0 + (2 * ts * (1 - ts))[:, None] * p1 + (ts ** 2)[:, None] * p2
    for (px, py), t in zip(pts, ts):
        r = 5.5 - 1.5 * t
        m = ((xx - px) ** 2 + (yy - py) ** 2 < r * r) & (kind <= LVEIN)
        img[m] = (45, 120, 55)
        kind[m] = STEM
        if t < 0.999:
            nx, ny = pts[min(len(pts) - 1, int(t * 399) + 1)]
            ang[m] = math.atan2(ny - py, nx - px)
    # bud: teardrop pointing up-left, red petals wrapped in green sepals
    ba = math.radians(-118)
    ca, sa = math.cos(ba), math.sin(ba)
    dx, dy = xx - bx, yy - by
    u = (dx * ca + dy * sa) / (0.42 * R0)
    v = (-dx * sa + dy * ca)
    hw = 0.13 * R0 * np.sqrt(np.clip(1 - ((u - 0.35) / 0.65) ** 2, 0, 1)) * (1 - 0.35 * np.clip(u, 0, 1))
    bud = (u > -0.3) & (u < 1) & (np.abs(v) < hw)
    twist = np.abs(((v / 9 + u * 6) % 2) - 1)
    bcol = mix((150, 10, 40), (235, 60, 85), twist * 0.8 + 0.2 * np.clip(u, 0, 1))
    img[bud] = bcol[bud]; kind[bud] = BUD; ang[bud] = ba + 0.6
    sep = bud & (u < 0.38 + 0.08 * np.sin(v / 4.0))
    img[sep] = mix((30, 100, 45), (80, 150, 70), np.clip((u + 0.3) / 0.7, 0, 1))[sep]
    kind[sep] = LEAF

    # ---------------- flower: five rounded petals overlapping like a pinwheel ----------------
    from scipy.ndimage import binary_dilation
    dx, dy = xx - CX, yy - CY
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    rn = r / R0
    rot = math.radians(-14)
    n = 5
    PA, PB, PC = 0.47, 0.385, 0.55          # petal ellipse: semi-axes and centre distance (x R0)
    sizes = [1.0, 0.96, 1.04, 0.98, 1.02]
    E, DIST, GAPD = [], [], []
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        ca, sa = math.cos(a), math.sin(a)
        u = (dx * ca + dy * sa) / R0
        v = (-dx * sa + dy * ca) / R0
        lu = (u - PC) / (PA * sizes[i])
        lv = v / PB
        phi = np.arctan2(lv, lu)
        e = lu ** 2 + lv ** 2
        thr = 1 + (0.06 * np.sin(phi * 9 + i * 1.7) + 0.035 * np.sin(phi * 17 + i)
                   + 0.02 * np.sin(phi * 29)) * np.clip(lu + 0.3, 0, 1)      # ruffled outer edge
        inside_e = e < thr
        wedge = (u > -0.02) & (u < 0.6) & (np.abs(v) < PB * np.clip(u / 0.42, 0, 1) ** 0.75 + 0.03)
        E.append(inside_e | wedge)
        DIST.append(np.where(inside_e, (1 - np.sqrt(e / thr)) * PB * R0, 30.0))   # px inside own outline
        GAPD.append((np.sqrt(e) - 1) * PB * R0)                                # px outside own outline
    E = np.array(E)
    # pinwheel: petal i+1 lies on top of petal i (and petal 0 on top of petal 4)
    owner = np.full((H, W), -1)
    for i in range(n):
        owner[E[i]] = i
    owner[E[0] & E[n - 1]] = 0
    inside = owner >= 0
    own = np.clip(owner, 0, n - 1)
    dist_own = np.choose(own, DIST)
    under = np.zeros((H, W), bool)
    for i in range(n):
        under |= (owner == i) & E[(i - 1) % n]

    a_own = rot + own * 2 * math.pi / n
    u_own = (dx * np.cos(a_own) + dy * np.sin(a_own)) / R0
    v_own = (-dx * np.sin(a_own) + dy * np.cos(a_own)) / R0
    t = np.clip(u_own / 1.02, 0, 1)

    re = R0 * (0.19 + 0.025 * np.sin(5 * th + 1) + 0.02 * np.sin(13 * th))
    vein_phase = th * 46 + 3 * rn
    v = 0.5 + 0.5 * np.cos(vein_phase)
    vfine = 0.5 + 0.5 * np.cos(th * 120 + 7 * rn)

    col = mix((180, 4, 38), (224, 22, 56), smooth(0.2, 0.7, t))
    col = mix(col, (242, 66, 90), smooth(0.8, 1.0, t) * 0.6)
    sheen = np.exp(-((v_own - 0.08) / 0.13) ** 2) * np.exp(-((t - 0.62) / 0.2) ** 2)
    col = col * (1 + 0.34 * sheen)[..., None]
    light = 0.88 + 0.14 * np.cos(th + 2.3)
    col = col * (light * (0.8 + 0.2 * smooth(0.12, 0.5, t)))[..., None]
    col = col * (1 - 0.10 * vfine ** 6 - 0.14 * v ** 10)[..., None]
    # shadow cast on each petal by the petal lying on top of it
    shade = np.ones((H, W))
    for i in range(n):
        g = GAPD[(i + 1) % n]
        m = (owner == i) & (g > 0) & (g < 34)
        shade[m] = np.minimum(shade[m], 0.45 + 0.55 * smooth(0, 34, g[m]))
    col = col * shade[..., None]
    streak = (v ** 3 > 0.55) & (r < re * (1.6 + 0.5 * np.sin(np.floor(vein_phase / (2 * np.pi)) * 2.1)))
    eye = r < re
    col = np.where((streak & ~eye)[..., None], mix(col, (120, 0, 38), 0.75), col)
    col = np.where(eye[..., None], mix((95, 0, 30), (150, 5, 45), smooth(0, 1, r / re)), col)

    img[inside] = np.clip(col[inside], 0, 255)
    kind[inside] = PETAL
    odd = (np.floor(vein_phase / (2 * np.pi)) % 2 == 0)
    vm = inside & (((v ** 10 > 0.72) & odd & (t > 0.3) & (t < 0.88)) | streak) & ~eye
    kind[vm] = VEIN
    ang[vm] = th[vm] + 0.1
    kind[inside & eye] = EYE
    # gaps: along a petal's edge where it lies over the one beneath, and a ring round the flower
    seam = inside & under & (dist_own < 7.5) & (r > re * 1.2)
    kind[seam] = BG
    img[seam] = 0
    ring = binary_dilation(inside, iterations=9) & ~inside
    kind[ring] = BG
    img[ring] = 0
    rim = inside & binary_dilation(~inside, iterations=5) & (kind != BG)
    kind[rim] = RIM
    img[rim] = np.clip(img[rim] * 0.62, 0, 255)
    from scipy.ndimage import gaussian_filter
    gy, gx = np.gradient(gaussian_filter(inside.astype(float), 7))
    ang[rim] = np.arctan2(gy[rim], gx[rim]) + np.pi / 2

    # ---------------- staminal column ----------------
    a = math.radians(-50)
    L = 1.02 * R0
    perp = np.array([-math.sin(a), math.cos(a)])
    def P(s):
        return np.array([CX, CY]) + s * L * np.array([math.cos(a), math.sin(a)]) - perp * 0.1 * R0 * s * s
    for s in np.linspace(0.12, 1, 300):
        px, py = P(s)
        w = 0.024 * R0 * (1 - 0.35 * s) + 9
        m = ((xx - px) ** 2 + (yy - py) ** 2 < w * w) & (kind != BG)
        kind[m] = BG
        img[m] = 0
    for s in np.linspace(0, 1, 500):
        px, py = P(s)
        w = 0.024 * R0 * (1 - 0.35 * s)
        m = (xx - px) ** 2 + (yy - py) ** 2 < w * w
        shade = 0.85 + 0.15 * np.clip(((xx - px) * perp[0] + (yy - py) * perp[1]) / w, -1, 1)
        img[m] = (np.array([250, 205, 195]) * shade[m][:, None]).clip(0, 255)
        kind[m] = COLUMN
        q = P(min(1, s + 0.01)) - np.array([px, py])
        ang[m] = math.atan2(q[1], q[0])
    # pollen-bearing anthers along the upper half
    for i in range(44):
        s = rng.uniform(0.45, 0.93)
        px, py = P(s)
        off = rng.uniform(0.6, 2.6) * 0.024 * R0 * rng.choice([-1, 1])
        px, py = px + perp[0] * off, py + perp[1] * off
        rr = rng.uniform(0.010, 0.017) * R0
        m = (xx - px) ** 2 + (yy - py) ** 2 < rr * rr
        dd = np.sqrt((xx[m] - px) ** 2 + (yy[m] - py) ** 2) / rr
        img[m] = mix((255, 214, 70), (214, 128, 14), dd)
        kind[m] = POLLEN
    # five stigma pads at the tip
    tip = P(1.0)
    for i in range(5):
        aa = a + math.radians(-60 + 30 * i)
        px, py = tip + 0.06 * R0 * np.array([math.cos(aa), math.sin(aa)])
        rr = 0.024 * R0
        m = (xx - px) ** 2 + (yy - py) ** 2 < rr * rr
        dd = np.sqrt((xx[m] - px) ** 2 + (yy[m] - py) ** 2) / rr
        img[m] = mix((120, 0, 40), (215, 30, 80), dd)
        kind[m] = STIGMA
        # little stalk
        for s in np.linspace(0, 1, 40):
            qx, qy = tip + s * 0.05 * R0 * np.array([math.cos(aa), math.sin(aa)])
            mm = ((xx - qx) ** 2 + (yy - qy) ** 2 < 9) & (kind != STIGMA)
            img[mm] = (230, 120, 130); kind[mm] = COLUMN; ang[mm] = aa
    return img, kind, ang


def dirchar(a):
    """glyph for a stroke direction (screen coords, y down)."""
    a = a % math.pi
    if a < math.pi / 8 or a >= 7 * math.pi / 8:
        return '-'
    if a < 3 * math.pi / 8:
        return '\\'
    if a < 5 * math.pi / 8:
        return '|'
    return '/'


def cached_render():
    import os
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render_cache.npz')
    src = os.path.getmtime(os.path.abspath(__file__))
    if os.path.exists(f) and os.path.getmtime(f) > src:
        z = np.load(f)
        return z['img'], z['kind'], z['ang']
    img, kind, ang = render()
    np.savez_compressed(f, img=img, kind=kind, ang=ang)
    return img, kind, ang


def to_art(cols=200, rows=100, seed=3, dark=False):
    img, kind, ang = cached_render()
    rng = np.random.default_rng(seed)
    cw, ch = W / cols, H / rows
    cells = []
    for j in range(rows):
        for i in range(cols):
            x, y = int((i + 0.5) * cw), int((j + 0.5) * ch)
            c = img[y, x]
            cells.append((j, i, kind[y, x], c, 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2], ang[y, x]))
    # tone = percentile of brightness within its own kind, so each part uses the full glyph ramp
    tone = {}
    for kd in (PETAL, LEAF, BUD, EYE):
        ls = np.array([c[4] for c in cells if c[2] == kd])
        if len(ls):
            srt = np.sort(ls)
            tone[kd] = lambda v, srt=srt: np.searchsorted(srt, v) / len(srt)
    grid = [[None] * cols for _ in range(rows)]
    for j, i, k, c, lum, a in cells:
        h = rng.random()
        if k == BG:
            g = None
        elif k in (PETAL, BUD, LEAF):
            q = tone[k](lum) + rng.normal(0, 0.06)
            if dark:   # on a dark page dense glyphs read bright
                g = ':' if q < 0.12 else '1' if q < 0.45 else '0' if q < 0.88 else '8'
            else:
                g = '8' if q < 0.1 else '0' if q < 0.5 else '1' if q < 0.9 else ':'
        elif k in (VEIN, SEAM, RIM, LVEIN, STEM, COLUMN):
            g = dirchar(a)
        elif k == EYE:
            g = '@' if h < 0.25 else ('8' if h < 0.5 else '0')
        elif k == POLLEN:
            g = '*' if h < 0.6 else ('o' if h < 0.85 else '@')
        else:  # STIGMA
            g = '@' if h < 0.6 else 'O'
        grid[j][i] = (g, tuple(int(v) for v in c))
    return grid


def to_html(grid, rain=True, seed=5, dark=False):
    rng = np.random.default_rng(seed)
    rows = len(grid); cols = len(grid[0])
    # binary rain in the empty background, falling in a few columns
    rainmap = {}
    if rain:
        for i in rng.choice(cols, size=cols // 6, replace=False):
            start = int(rng.integers(0, rows)); length = int(rng.integers(4, 18))
            for j in range(start, min(rows, start + length)):
                rainmap[(j, int(i))] = (j - start) / length
    out = []
    for j, row in enumerate(grid):
        line, cur, buf = [], None, ''
        for i, (g, c) in enumerate(row):
            if g is None:
                if (j, i) in rainmap:
                    f = rainmap[(j, i)]
                    g = '01'[int(rng.integers(0, 2))]
                    if dark:
                        c = (int(40 + 50 * f), int(14 + 14 * f), int(24 + 20 * f))
                    else:
                        shade = int(250 - 18 * f)
                        c = (shade, int(shade * 0.93), int(shade * 0.94))
                else:
                    g, c = ' ', None
            elif dark:
                c = tuple(min(255, int(v * 1.32 + 26)) for v in c)
            colr = None
            if c is not None:
                colr = '#%02x%02x%02x' % tuple((min(255, v) // 6) * 6 for v in c)
            if colr != cur:
                if buf:
                    line.append(buf if cur is None else f'<i style="color:{cur}">{buf}</i>')
                cur, buf = colr, ''
            buf += {'<': '&lt;', '>': '&gt;', '&': '&amp;'}.get(g, g)
        if buf:
            line.append(buf if cur is None else f'<i style="color:{cur}">{buf}</i>')
        out.append(''.join(line).rstrip())
    return chr(10).join(out)


if __name__ == '__main__':
    from PIL import Image
    img, kind, ang = render()
    Image.fromarray(img.clip(0, 255).astype('uint8')).save('hib_preview.png')
    print('ok')
