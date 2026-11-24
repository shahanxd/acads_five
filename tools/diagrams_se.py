"""Draw the Software Engineering endsem diagrams into 'Software Engineering/Endsem RUN/md/images'."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from diagrams import *

OUT = pathlib.Path(__file__).resolve().parent.parent / 'Software Engineering' / 'Endsem RUN' / 'md' / 'images'

def spiral():
    cx, cy = 360, 300
    b = ''
    b += f'<line x1="40" y1="{cy}" x2="680" y2="{cy}" stroke="#999" stroke-width="1.2"/>'
    b += f'<line x1="{cx}" y1="30" x2="{cx}" y2="570" stroke="#999" stroke-width="1.2"/>'
    # spiral: starts near centre, grows outward, going clockwise from the left
    pts = []
    for i in range(0, 1001):
        t = i / 1000 * 3.7 * math.pi
        r = 14 + 21 * t
        a = math.pi - t                   # start pointing left, rotate clockwise (screen)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    b += line([(round(x, 1), round(y, 1)) for x, y in pts], arrow=True)
    b += text(130, 40, ['1. Determine objectives,', 'alternatives, constraints'], 12.5, bold=True)
    b += text(590, 40, ['2. Evaluate alternatives,', 'identify and resolve RISKS'], 12.5, bold=True)
    b += text(590, 555, ['3. Develop and verify the', 'next-level product'], 12.5, bold=True)
    b += text(130, 555, ['4. Review and plan', 'the next phase'], 12.5, bold=True)
    b += lbl(470, 255, ['prototype', 'risk analysis'], 10.5)
    b += lbl(470, 350, ['design, code,', 'test'], 10.5)
    b += lbl(250, 350, ['customer', 'evaluation'], 10.5)
    b += lbl(250, 255, ['requirements,', 'plan'], 10.5)
    b += text(cx, 590, 'Cumulative cost grows with the radius; each loop = one phase', 11, italic=True)
    return svg(720, 600, b)

def dfd0():
    b = ''
    b += f'<circle cx="360" cy="150" r="80" fill="#fff" stroke="#111" stroke-width="1.5"/>'
    b += text(360, 125, '0', 13, bold=True) + text(360, 158, ['Library', 'Management', 'System'], 12.5)
    b += rect(20, 128, 130, 44, 'Member')
    b += rect(570, 128, 130, 44, 'Librarian')
    b += line([(150, 138), (282, 138)]) + lbl(216, 124, 'Book request, return')
    b += line([(282, 162), (150, 162)]) + lbl(216, 178, 'Issue slip, fine notice')
    b += line([(570, 138), (438, 138)]) + lbl(504, 124, 'Book / member details')
    b += line([(438, 162), (570, 162)]) + lbl(504, 178, 'Reports')
    return svg(720, 300, b)

def dfd1():
    b = ''
    P = {1: (360, 70), 2: (360, 200), 3: (360, 340), 4: (360, 470)}
    b += proc(*P[1], '1.0', ['Manage', 'Members'])
    b += proc(*P[2], '2.0', ['Issue', 'Book'])
    b += proc(*P[3], '3.0', ['Return Book,', 'Fine'])
    b += proc(*P[4], '4.0', ['Manage Books,', 'Reports'])
    b += rect(20, 60, 120, 42, 'Member')
    b += rect(570, 450, 130, 42, 'Librarian')
    b += store(500, 55, 170, 'D1', 'Member records')
    b += store(520, 255, 170, 'D2', 'Book catalogue')
    b += store(30, 255, 170, 'D3', 'Issue records')
    b += line([(140, 72), edge(*P[1], 140, 72)]) + lbl(225, 56, 'Registration')
    b += line([(404, 70), (500, 70)]) + lbl(452, 58, 'Member details', 10)
    b += line([(140, 90), edge(*P[2], 140, 90)]) + lbl(255, 128, 'Book request', 10)
    b += line([edge(*P[2], 120, 102), (120, 102)]) + lbl(190, 150, 'Issue slip', 10)
    b += line([(560, 85), edge(*P[2], 560, 85)]) + lbl(500, 120, 'Membership check', 10)
    b += line([edge(*P[2], 520, 262), (520, 262)], both=True) + lbl(450, 216, 'Availability', 10)
    b += line([edge(*P[2], 200, 262), (200, 262)]) + lbl(262, 222, 'Issue entry', 10)
    b += line([(100, 102), edge(*P[3], 100, 102)]) + lbl(110, 190, 'Returned book', 10, 'start')
    b += line([edge(*P[3], 70, 102), (70, 102)]) + lbl(25, 140, 'Fine receipt', 10, 'start')
    b += line([edge(*P[3], 200, 282), (200, 282)], both=True) + lbl(262, 300, 'Due date', 10)
    b += line([edge(*P[3], 520, 282), (520, 282)]) + lbl(455, 330, 'Mark available', 10)
    b += line([(570, 460), (404, 460)]) + lbl(487, 448, 'New books', 10)
    b += line([(404, 482), (570, 482)]) + lbl(487, 496, 'Reports', 10)
    b += line([edge(*P[4], 600, 285), (600, 285)]) + lbl(560, 400, 'Add / update', 10, 'start')
    return svg(720, 520, b)

def activity():
    b = ''
    X = 360
    b += f'<circle cx="{X}" cy="20" r="11" fill="#111"/>'
    b += line([(X, 31), (X, 50)])
    b += act(X, 50, 220, 'Student enters ID and password')
    b += line([(X, 82), (X, 100)])
    b += diamond(X, 125, 60, 25, 'Valid?')
    b += line([(X + 60, 125), (580, 125), (580, 66), (X + 110, 66)]) + lbl(510, 113, '[No] show error', 10)
    b += line([(X, 150), (X, 170)]) + lbl(X + 8, 160, '[Yes]', 10, 'start')
    b += act(X, 170, 220, 'View instructions, start exam')
    b += line([(X, 202), (X, 222)])
    b += act(X, 222, 220, 'Timer starts, show question')
    b += line([(X, 254), (X, 274)])
    b += act(X, 274, 220, 'Select / change answer')
    b += line([(X, 306), (X, 326)])
    b += diamond(X, 351, 80, 25, 'More questions and time left?', 9.5)
    b += line([(X - 80, 351), (150, 351), (150, 238), (X - 110, 238)]) + lbl(205, 340, '[Yes] next', 10)
    b += line([(X, 376), (X, 398)]) + lbl(X + 8, 387, '[No / time up]', 10, 'start')
    b += act(X, 398, 220, 'Submit (or auto-submit)')
    b += line([(X, 430), (X, 450)])
    b += act(X, 450, 220, 'System evaluates answers')
    b += line([(X, 482), (X, 502)])
    b += act(X, 502, 220, 'Generate and store result')
    b += line([(X, 534), (X, 554)])
    b += act(X, 554, 220, 'Display result, log out')
    b += line([(X, 586), (X, 604)])
    b += f'<circle cx="{X}" cy="617" r="13" fill="#fff" stroke="#111" stroke-width="1.5"/><circle cx="{X}" cy="617" r="8" fill="#111"/>'
    return svg(720, 640, b, maxh=190)

def reverse():
    b = ''
    X = 360
    steps = [('Dirty (unstructured) source code', 30), ('Restructure code', 95), ('Clean source code', 160),
             ('Extract abstractions', 225), ('Initial specification', 360), ('Refine and simplify', 425),
             ('Final specification', 490)]
    for t, y in steps:
        w = 250
        b += rect(X - w / 2, y, w, 40, t, 12.5, r=6)
    for (t1, y1), (t2, y2) in zip(steps, steps[1:]):
        if y1 == 225: continue
        b += line([(X, y1 + 40), (X, y2)])
    # three abstraction branches
    xs = [150, 360, 570]
    names = [['Processing', '(how functions work)'], ['Data', '(structures, ER)'], ['User interface', '(screens, flow)']]
    b += line([(X, 265), (X, 278)], arrow=False)
    b += line([(xs[0], 278), (xs[2], 278)], arrow=False)
    for x, n in zip(xs, names):
        b += line([(x, 278), (x, 286)])
        b += rect(x - 85, 286, 170, 38, n, 10.5, r=4)
        b += line([(x, 324), (x, 340), (X, 340)], arrow=False) if x != X else ''
    b += line([(X, 324), (X, 360)])
    return svg(720, 545, b)

def quickfix():
    b = ''
    nodes = [(360, 60, 'Problem reported'), (590, 190, 'Quick analysis'), (500, 360, 'Change the code'),
             (220, 360, 'Minimal testing'), (130, 190, 'Release (hot-fix)')]
    for x, y, t in nodes:
        b += rect(x - 85, y - 22, 170, 44, t, 12.5, r=20)
    for (x1, y1, _), (x2, y2, _) in zip(nodes, nodes[1:] + nodes[:1]):
        a = math.atan2(y2 - y1, x2 - x1)
        b += line([(round(x1 + 95 * math.cos(a), 1), round(y1 + 30 * math.sin(a), 1)),
                   (round(x2 - 95 * math.cos(a), 1), round(y2 - 30 * math.sin(a), 1))])
    b += text(360, 210, ['System in use', '(problems keep coming)'], 12, italic=True)
    b += text(360, 430, 'Design and documents are usually NOT updated', 11.5, italic=True)
    return svg(720, 450, b)

for name, fn in [('se-spiral', spiral), ('se-library-dfd0', dfd0), ('se-library-dfd1', dfd1),
                 ('se-exam-activity', activity), ('se-reverse-engineering', reverse), ('se-quick-fix', quickfix)]:
    save(OUT / f'{name}.svg', fn())
print('saved to', OUT)
