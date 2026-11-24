"""Render a study markdown file to PDF.

Usage: python tools/md2pdf.py <file.md> [more.md ...]
Writes <file>.pdf next to each .md. Maths in ```latex fences or $$...$$ blocks is rendered with KaTeX
(server-side, via node), then the page is printed with headless Chrome.
Needs: pip install markdown; tools/node_modules/katex (npm install katex in tools/).
"""
import html, json, pathlib, re, subprocess, sys, tempfile
import markdown

HERE = pathlib.Path(__file__).resolve().parent
KATEX = HERE / 'node_modules' / 'katex'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

CSS = """
@page { size: A4; margin: 15mm 15mm 16mm 15mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.6pt; line-height: 1.55; color: #1d1d1f; }
h1 { font-family: Georgia, 'Times New Roman', serif; font-size: 22pt; font-weight: 500; margin: 0 0 4px; }
h2 { font-family: Georgia, 'Times New Roman', serif; font-size: 15.5pt; font-weight: 500; margin: 24px 0 6px;
     padding-bottom: 3px; border-bottom: 1.5px solid #e0d9cc; page-break-after: avoid; }
h3 { font-size: 12.2pt; margin: 16px 0 4px; color: #2c2c2c; page-break-after: avoid; }
h4 { font-size: 11pt; margin: 12px 0 3px; page-break-after: avoid; }
p { margin: 6px 0; }
a { color: #2b5fb4; }
blockquote { margin: 12px 0 6px; padding: 8px 13px; background: #f7f3ea; border-left: 3.5px solid #c96442;
             border-radius: 4px; page-break-inside: avoid; }
blockquote p { margin: 3px 0; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 9.3pt; background: #f1efe9; padding: 0 3px; border-radius: 3px; }
pre { background: #f6f5f1; border: 1px solid #e6e2d8; border-radius: 4px; padding: 8px 10px;
      white-space: pre-wrap; word-break: break-word; }
pre code { background: none; padding: 0; font-size: 8.9pt; line-height: 1.36; }
table { border-collapse: collapse; margin: 8px 0; font-size: 9.7pt; page-break-inside: avoid; }
th, td { border: 1px solid #ddd8cc; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #f4f1ea; font-weight: 600; }
img { max-width: 100%; max-height: 200mm; display: block; margin: 8px auto 2px; page-break-inside: avoid; }
.math { margin: 8px 0; padding: 2px 0; overflow-x: hidden; page-break-inside: avoid; }
.katex-display { margin: 0; }
.katex { font-size: 1.07em; }
ul, ol { margin: 4px 0; padding-left: 22px; }
li { margin: 2px 0; }
li > p { margin: 2px 0; }
hr { border: none; border-top: 1px dashed #d8d2c4; margin: 16px 0; }
"""

NODE = r"""
const katex = require(process.argv[2]);
const items = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = items.map(([s, disp]) => { try { return katex.renderToString(s, {displayMode: disp, throwOnError: true, strict: false}); }
  catch (e) { return 'ERR:' + e.message; } });
process.stdout.write(JSON.stringify(out));
"""

def render(md_path):
    md_path = pathlib.Path(md_path).resolve()
    text = md_path.read_text(encoding='utf-8')
    maths = []
    def stash(src, disp):
        maths.append((src.strip(), disp))
        return f'@@MATH{len(maths) - 1}@@'
    text = re.sub(r'```latex\n(.*?)```', lambda m: '\n\n' + stash(m.group(1), True) + '\n\n', text, flags=re.S)
    text = re.sub(r'\$\$(.+?)\$\$', lambda m: '\n\n' + stash(m.group(1), True) + '\n\n', text, flags=re.S)
    # inline $...$ (not inside code); require no space after opening $
    parts = re.split(r'(```.*?```|`[^`\n]*`)', text, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<![\\$\w])\$(?! )([^$\n]+?)(?<! )\$(?!\w)', lambda m: stash(m.group(1), False), parts[i])
    text = ''.join(parts)
    body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists', 'attr_list', 'nl2br'])
    body = re.sub(r'<pre>.*?</pre>', lambda m: m.group(0).replace('<br />', ''), body, flags=re.S)
    errs = []
    if maths:
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(NODE)
        r = subprocess.run(['node', f.name, str(KATEX)], input=json.dumps(maths), capture_output=True, text=True, encoding='utf-8')
        out = json.loads(r.stdout)
        for i, h in enumerate(out):
            if h.startswith('ERR:'):
                errs.append((maths[i][0][:60], h))
                h = '<code>' + html.escape(maths[i][0]) + '</code>'
            disp = maths[i][1]
            rep = f'<div class="math">{h}</div>' if disp else h
            body = body.replace(f'<p>@@MATH{i}@@</p>', rep).replace(f'@@MATH{i}@@', rep)
    css_katex = (KATEX / 'dist' / 'katex.min.css').as_uri()
    title = html.escape(md_path.stem)
    page = (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f'<base href="{md_path.parent.as_uri()}/"><link rel="stylesheet" href="{css_katex}">'
            f'<style>{CSS}</style></head><body>{body}</body></html>')
    tmp = md_path.with_suffix('.render.html')
    tmp.write_text(page, encoding='utf-8')
    # sources kept in an 'md' subfolder print to the folder above it
    out_dir = md_path.parent.parent if md_path.parent.name == 'md' else md_path.parent
    pdf = out_dir / (md_path.stem + '.pdf')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                    f'--print-to-pdf={pdf}', tmp.as_uri()], capture_output=True, check=True)
    tmp.unlink()
    return pdf, len(maths), errs

if __name__ == '__main__':
    for a in sys.argv[1:]:
        pdf, n, errs = render(a)
        print(f'{pdf.name}: math {n}, errors {len(errs)}')
        for e in errs: print('   ', e)
