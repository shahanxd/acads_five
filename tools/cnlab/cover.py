"""Front page for the CN lab file: a large hibiscus in coloured 0/1 character art."""
import base64, pathlib, sys
from hibiscus import to_art, to_html

HERE = pathlib.Path(__file__).resolve().parent
LOGO = HERE / 'jmi_logo.jpeg'

THEMES = {
    'light': dict(bg='#ffffff', uni='#6b6b6b', accent='#9a1b3c', title='#8c0f2f', text='#222', sub='#555',
                  frame='#ecc4cb', rule='#e2c8cd'),
    'dark': dict(bg='#0f0b10', uni='#b9a9ad', accent='#ff7a93', title='#ffd9df', text='#f4eef0', sub='#c9bcc0',
                 frame='#4a1d2a', rule='#3a2a30'),
}


def cover(theme='dark', cols=230, rows=None, art_w=184):
    th = THEMES[theme]
    rows = rows or round(cols / 2)
    fs = art_w / cols / 0.5498            # Consolas advance = 0.5498 em
    art = to_html(to_art(cols, rows, dark=(theme == 'dark')), dark=(theme == 'dark'))
    logo = ''
    if LOGO.exists():
        b = base64.b64encode(LOGO.read_bytes()).decode()
        logo = f'<img class="logo" src="data:image/jpeg;base64,{b}">'
    edge = ''.join('01'[(i * 7 + i // 3) % 2] for i in range(160))
    html = f'''
<div class="cv">
  <div class="frame-t">{edge}</div><div class="frame-b">{edge}</div>
  <div class="cv-top">
    {logo}
    <div class="uni">JAMIA MILLIA ISLAMIA</div>
    <div class="lab">L A B &nbsp; F I L E</div>
    <div class="title">Computer Networks</div>
    <div class="code">CSL-503 &nbsp;·&nbsp; Computer Network Lab</div>
  </div>
  <pre class="art">{art}</pre>
  <div class="cv-bot">
    <div class="who">
      <div><div class="h">submitted to</div><div class="nm">Prof. Hannan Mansoor</div>
        <div class="roll">&nbsp;</div></div>
      <div class="r"><div class="h">submitted by</div><div class="nm">Mohd Shahan Shah Ayyubi</div>
        <div class="roll">24BCS064</div></div>
    </div>
    <div class="dept">B.Tech Computer Engineering &nbsp;·&nbsp; Semester V &nbsp;·&nbsp; 2026–27<br>
      Department of Computer Engineering, Faculty of Engineering and Technology<br>
      Jamia Millia Islamia, New Delhi – 110025</div>
  </div>
</div>'''
    logo_css = 'border-radius: 50%; background: #fff; padding: 1.2mm;' if theme == 'dark' else ''
    css = f'''
.cv {{ position: relative; width: 210mm; height: 297mm; background: {th['bg']}; overflow: hidden;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; page-break-after: always; }}
.cv .frame-t, .cv .frame-b {{ position: absolute; left: 0; right: 0; font: 6pt Consolas, monospace; letter-spacing: 1.2pt;
   color: {th['frame']}; white-space: nowrap; overflow: hidden; text-align: center; }}
.cv .frame-t {{ top: 4mm; }} .cv .frame-b {{ bottom: 4mm; }}
.cv-top {{ text-align: center; padding-top: 14mm; }}
.cv .logo {{ width: 17mm; display: block; margin: 0 auto 2.5mm; {logo_css} }}
.cv .uni {{ font: 600 9pt 'Segoe UI', sans-serif; letter-spacing: 4pt; color: {th['uni']}; }}
.cv .lab {{ font: 10pt Georgia, serif; letter-spacing: 3pt; color: {th['accent']}; margin-top: 4mm; }}
.cv .title {{ font: 32pt Georgia, serif; color: {th['title']}; margin-top: 1mm; letter-spacing: 0.5pt; }}
.cv .code {{ font: italic 11pt Georgia, serif; color: {th['sub']}; margin-top: 1mm; }}
.cv pre.art {{ font-family: Consolas, monospace; font-weight: 700; font-size: {fs:.4f}mm; line-height: 1;
   margin: 0 auto; width: {art_w}mm; white-space: pre; padding: 0; border: none; background: none; }}
.cv pre.art i {{ font-style: normal; }}
.cv-bot {{ position: absolute; left: 18mm; right: 18mm; bottom: 13mm; }}
.cv .who {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.cv .who .h {{ font: 8.5pt 'Segoe UI', sans-serif; letter-spacing: 2.5pt; text-transform: uppercase; color: {th['accent']}; }}
.cv .who .nm {{ font: 14pt Georgia, serif; color: {th['text']}; margin-top: 1.5mm; }}
.cv .who .line {{ border-bottom: 0.6pt solid {th['sub']}; width: 60mm; margin-top: 1mm; }}
.cv .who .r {{ text-align: right; }}
.cv .who .roll {{ font: 11pt Consolas, monospace; color: {th['accent']}; letter-spacing: 1.5pt; margin-top: 0.5mm; }}
.cv .dept {{ text-align: center; font: 9pt Georgia, serif; color: {th['sub']}; line-height: 1.55; margin-top: 6mm;
   border-top: 0.6pt solid {th['rule']}; padding-top: 3mm; }}
'''
    return html, css


if __name__ == '__main__':
    import subprocess, fitz
    CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    for theme in sys.argv[1:] or ['dark']:
        html, css = cover(theme)
        page = (f'<!doctype html><html><head><meta charset="utf-8"><style>@page {{ size: A4; margin: 0; }} '
                f'body {{ margin: 0; }} {css}</style></head><body>{html}</body></html>')
        h = HERE / f'cover_{theme}.html'
        h.write_text(page, encoding='utf-8')
        pdf = HERE / f'cover_{theme}.pdf'
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={pdf}', h.as_uri()], check=True, capture_output=True)
        d = fitz.open(pdf)
        print(theme, 'pages', d.page_count)
        d[0].get_pixmap(dpi=150).save(HERE / f'cover_{theme}.png')
        d[0].get_pixmap(dpi=320, clip=fitz.Rect(170, 300, 420, 470)).save(HERE / f'cover_{theme}_zoom.png')
