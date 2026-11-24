"""Build 'Endsem Solved 2025.md' for a subject from the Endsem 2025 questions answered in its unit docs.

Usage: python tools/assemble_solved.py "<Subject>/Endsem RUN/md" "<Title>" "<paper line>" [extra.md]
Each question in a unit doc starts with a blockquote line '> **Endsem 2025 · Q<n>(<part>) ...' and its answer runs
until the next '---', '## ' heading or the next such question. An optional extra.md is appended
(for questions that fit no unit). Output: <md dir>/Endsem Solved 2025.md
"""
import pathlib, re, sys

md_dir = pathlib.Path(sys.argv[1])
title, paper = sys.argv[2], sys.argv[3]
extra = pathlib.Path(sys.argv[4]).read_text(encoding='utf-8') if len(sys.argv) > 4 else ''

items = []
for f in sorted(md_dir.glob('Unit *.md')):
    lines = f.read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r'> \*\*Endsem 2025 · Q(\d+)(?:\(([a-z]+)\))?', lines[i])
        if not m:
            i += 1; continue
        j = i + 1
        while j < len(lines) and not (lines[j].strip() == '---' or lines[j].startswith('## ')
                                      or re.match(r'> \*\*Endsem 2025 · Q', lines[j])):
            j += 1
        block = '\n'.join(lines[i:j]).rstrip()
        unit = f.stem.split(' - ')[0]
        items.append((int(m.group(1)), m.group(2) or '', block, unit))
        i = j

items.sort(key=lambda t: (t[0], t[1]))
out = [f'# {title}', '', paper, '',
       'Every question of the 2025 endsem paper, solved. The same answers sit inside the unit docs at the topic they belong to; '
       'the unit is named under each question so you can jump there for the explanation.', '']
cur = None
for q, part, block, unit in items:
    if q != cur:
        out += ['---', '', f'## Question {q}', '']
        cur = q
    out += [block, '', f'*Taught in {unit}.*', '']
if extra:
    out += ['---', '', extra.strip(), '']
(md_dir / 'Endsem Solved 2025.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('questions:', [(q, p, u) for q, p, _, u in items])
