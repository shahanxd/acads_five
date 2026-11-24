"""Draw Microprocessor endsem diagrams into 'Microprocessor/Endsem RUN/md/images'."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from diagrams import *

OUT = pathlib.Path(__file__).resolve().parent.parent / 'Microprocessor' / 'Endsem RUN' / 'md' / 'images'

def bus(x0, x1, y, label, h=22, float_=False):
    """A bus value cell: hexagon-ended lane with text."""
    m = 6
    if float_:
        return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#888" stroke-width="1.2" stroke-dasharray="4,3"/>'
    pts = f'{x0},{y} {x0+m},{y-h/2} {x1-m},{y-h/2} {x1},{y} {x1-m},{y+h/2} {x0+m},{y+h/2}'
    return f'<polygon points="{pts}" fill="#fff" stroke="#111" stroke-width="1.3"/>' + text((x0 + x1) / 2, y, label, 10.5)

def timing_lda():
    L, W = 150, 52                      # label column, width of one T-state
    cycles = [('M1: Opcode fetch', 4, '2000H'), ('M2: Memory read', 3, '2001H'),
              ('M3: Memory read', 3, '2002H'), ('M4: Memory read', 3, '2150H')]
    total = sum(c[1] for c in cycles)
    Wd = L + total * W + 20
    rows = {'CLK': 70, 'A15–A8': 115, 'AD7–AD0': 160, 'ALE': 205, 'IO/M̅': 245, 'S1, S0': 285, 'RD̅': 325}
    b = ''
    for name, y in rows.items():
        b += text(L - 12, y, name, 12, anchor='end', bold=True)
    # cycle headers and T labels
    x = L
    starts = []
    for (title, n, addr) in cycles:
        starts.append(x)
        b += f'<rect x="{x}" y="10" width="{n*W}" height="24" fill="#f3efe6" stroke="#999"/>' + text(x + n * W / 2, 22, title, 11, bold=True)
        for k in range(n):
            b += text(x + k * W + W / 2, 45, f'T{k+1}', 10)
        x += n * W
        b += f'<line x1="{x}" y1="10" x2="{x}" y2="345" stroke="#bbb" stroke-dasharray="3,3"/>'
    # clock
    pts = []
    for i in range(total):
        x0 = L + i * W
        pts += [(x0, 80), (x0, 60), (x0 + W / 2, 60), (x0 + W / 2, 80), (x0 + W, 80)]
    b += line(pts, arrow=False)
    # per-cycle signals
    hi = {'2000H': '20H', '2001H': '20H', '2002H': '20H', '2150H': '21H'}
    lo = {'2000H': '00H', '2001H': '01H', '2002H': '02H', '2150H': '50H'}
    data = {'2000H': '3AH (opcode)', '2001H': '50H', '2002H': '21H', '2150H': 'data → A'}
    for (title, n, addr), x0 in zip(cycles, starts):
        b += bus(x0, x0 + 3 * W, rows['A15–A8'], hi[addr])
        if n == 4: b += bus(x0 + 3 * W, x0 + 4 * W, rows['A15–A8'], '', float_=True)
        b += bus(x0, x0 + W, rows['AD7–AD0'], lo[addr])
        b += bus(x0 + W, x0 + 3 * W, rows['AD7–AD0'], data[addr])
        if n == 4: b += bus(x0 + 3 * W, x0 + 4 * W, rows['AD7–AD0'], '', float_=True)
        # ALE: high during first half of T1
        y = rows['ALE']
        b += line([(x0, y + 10), (x0 + 4, y - 10), (x0 + W * 0.6, y - 10), (x0 + W * 0.6 + 4, y + 10), (x0 + n * W, y + 10)], arrow=False)
        # IO/M low
        y = rows['IO/M̅']
        b += line([(x0, y + 10), (x0 + n * W, y + 10)], arrow=False) + text(x0 + n * W / 2, y - 2, '0 (memory)', 10)
        b += bus(x0, x0 + n * W, rows['S1, S0'], '1, 1 (fetch)' if n == 4 else '1, 0 (read)')
        # RD low in T2-T3
        y = rows['RD̅']
        b += line([(x0, y - 10), (x0 + W + 4, y - 10), (x0 + W + 8, y + 10), (x0 + 3 * W, y + 10),
                   (x0 + 3 * W + 4, y - 10), (x0 + n * W, y - 10)], arrow=False)
    b += text(Wd / 2, 365, 'LDA 2150H stored at 2000H: 4 machine cycles, 13 T-states (3AH, 50H, 21H at 2000H–2002H)', 11.5, italic=True)
    return svg(Wd, 380, b)

def io_mapped():
    b = ''
    b += rect(20, 120, 120, 90, ['8085', 'CPU'], 14, bold=True)
    b += rect(560, 40, 140, 60, ['Input port', '(buffer 74LS244)', 'address 84H'], 11)
    b += rect(560, 210, 140, 60, ['Output port', '(latch 74LS373)', 'address 85H'], 11)
    b += rect(330, 120, 140, 90, ['Address', 'decoder', '(A7–A0 → port)'], 11.5)
    b += line([(140, 140), (330, 140)]) + lbl(235, 130, 'A7–A0 (port no.)', 10)
    b += line([(140, 165), (330, 165)]) + lbl(235, 155, 'IO/M̅ = 1', 10)
    b += line([(140, 190), (330, 190)]) + lbl(235, 180, 'RD̅, WR̅', 10)
    b += line([(470, 145), (540, 145), (540, 70), (560, 70)]) + lbl(510, 105, 'enable', 10)
    b += line([(470, 185), (540, 185), (540, 240), (560, 240)])
    b += line([(80, 210), (80, 320), (710, 320), (710, 70)], arrow=False)
    b += line([(710, 70), (700, 70)], both=True)
    b += line([(710, 240), (700, 240)], both=True)
    b += f'<polygon points="80,212 75,222 85,222" fill="#111"/>'
    b += lbl(350, 335, 'Data bus D7–D0 (IN copies port → A, OUT copies A → port)', 10.5)
    b += text(630, 20, 'e.g. switches', 10.5, italic=True) + text(630, 290, 'e.g. LEDs', 10.5, italic=True)
    return svg(730, 350, b)

for name, fn in [('mp-timing-lda', timing_lda), ('mp-io-mapped', io_mapped)]:
    save(OUT / f'{name}.svg', fn())
print('saved', OUT)
