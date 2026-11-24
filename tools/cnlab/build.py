"""Build the Computer Networks lab file.

python tools/cnlab/run_all.py   (runs every program for real, saves transcripts.json)
python tools/cnlab/build.py     (screenshots + cover + experiments -> PDF)
"""
import html, json, pathlib, subprocess
import fitz
from term_shot import shot
from cover import cover

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parents[1] / 'Computer Networks' / 'Lab'
PROG = LAB / 'programs'
SHOTS = HERE / 'shots'
SHOTS.mkdir(exist_ok=True)
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
T = json.loads((HERE / 'transcripts.json').read_text(encoding='utf-8'))
esc = html.escape


def pdf_from_html(page_html, out):
    h = out.with_suffix('.html')
    h.write_text(page_html, encoding='utf-8')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                    f'--print-to-pdf={out}', h.as_uri()], check=True, capture_output=True)
    h.unlink()


# ---------------- screenshots ----------------
def img(name, cap):
    return f'<div class="fig"><img src="{(SHOTS / name).as_uri()}"><div class="cap">{cap}</div></div>'


shots = {}
shot([('python exp1_caesar.py', T['1']['run1']), ('python exp1_caesar.py', T['1']['run2'])], SHOTS / 'e1.png')
shots['1'] = img('e1.png', 'Output (run twice with different keys)')
shot([('python exp2_railfence.py', T['2']['run1']), ('python exp2_railfence.py', T['2']['run2'])], SHOTS / 'e2.png')
shots['2'] = img('e2.png', 'Output')
shot([('python exp3_columnar.py', T['3']['run1'])], SHOTS / 'e3.png')
shots['3'] = img('e3.png', 'Output')
shot([('python exp4_ip_range.py', T['4']['run1'])], SHOTS / 'e4.png')
shots['4'] = img('e4.png', 'Output')

shot([('python exp5_server.py', T['5']['server'])], SHOTS / 'e5s.png', tabs=['python', 'python'], active=0)
shot([('python exp5_client.py', T['5']['client'])], SHOTS / 'e5c.png', tabs=['python', 'python'], active=1)
shots['5'] = img('e5s.png', 'Terminal 1: server process') + img('e5c.png', 'Terminal 2: client process')

tabs = ['python'] * 4
shot([('python exp6_server.py', T['6']['server'])], SHOTS / 'e6s.png', tabs=tabs, active=0, running=True)
parts = [img('e6s.png', 'Terminal 1: server (still running, serving every client in its own thread)')]
for i in (1, 2, 3):
    shot([('python exp6_client.py', T['6'][f'client{i}'])], SHOTS / f'e6c{i}.png', tabs=tabs, active=i)
    parts.append(img(f'e6c{i}.png', f'Terminal {i + 1}: client {i}'))
shots['6'] = ''.join(parts)

for e in ('7', '8'):
    tabs = ['python'] * 3
    shot([(f'python exp{e}_server.py', T[e]['server'])], SHOTS / f'e{e}s.png', tabs=tabs, active=0, running=True)
    shot([(f'python exp{e}_client.py', T[e]['clientA'])], SHOTS / f'e{e}a.png', tabs=tabs, active=1)
    shot([(f'python exp{e}_client.py', T[e]['clientB'])], SHOTS / f'e{e}b.png', tabs=tabs, active=2)
    shots[e] = (img(f'e{e}s.png', 'Terminal 1: server') + img(f'e{e}a.png', 'Terminal 2: client A (shahan)')
                + img(f'e{e}b.png', 'Terminal 3: client B (rahul)'))


# ---------------- experiments ----------------
def code(*files):
    out = ''
    for f in files:
        src = (PROG / f).read_text(encoding='utf-8').rstrip()
        out += f'<div class="fname">{f}</div><pre class="code">{esc(src)}</pre>'
    return out


EXPS = [
    ('Caesar Cipher Program',
     'To write a program to encrypt and decrypt a message using the Caesar cipher.',
     '''<p>Caesar cipher is one of the oldest and simplest substitution ciphers. Every letter of the plain text is
     replaced by the letter a fixed number of positions (the <b>key</b>) further down the alphabet, wrapping around
     after Z. With key 3, A becomes D, B becomes E, ..., X becomes A.</p>
     <p>Taking A = 0, B = 1, ..., Z = 25:</p>
     <p class="eq">Encryption: C = (P + k) mod 26 &nbsp;&nbsp;&nbsp; Decryption: P = (C &minus; k) mod 26</p>
     <p>Only 25 keys are possible, so it can be broken easily by trying all of them (brute force). Non-letters
     (spaces, digits) are left as they are, and case is preserved.</p>''',
     ['exp1_caesar.py']),
    ('Rail Fence Cipher Program',
     'To write a program to encrypt and decrypt a message using the rail fence cipher.',
     '''<p>Rail fence is a <b>transposition</b> cipher: the letters stay the same but their order changes. The plain
     text is written in a zig-zag over a number of rows ("rails"), going down and up again, and the cipher text is
     read off row by row.</p>
     <p>Example with 3 rails, WEAREDISCOVERED...:</p>
     <pre class="mini">W . . . E . . . C . . . R . . .
. E . R . D . S . O . E . E . F
. . A . . . I . . . V . . . D .</pre>
     <p>For decryption the same zig-zag pattern is made for the cipher text length, the cipher text is cut into
     pieces (one for each rail, with the right number of letters) and then read back along the zig-zag.</p>''',
     ['exp2_railfence.py']),
    ('Columnar Transposition Cipher Program',
     'To write a program to encrypt and decrypt a message using the columnar transposition cipher.',
     '''<p>In columnar transposition the message is written row by row in a table whose number of columns equals the
     length of the key. The columns are then read out one by one in the <b>alphabetical order of the key letters</b>.
     Empty cells in the last row are padded (here with "_").</p>
     <p>For key ZEBRAS the column order is A(5) B(3) E(2) R(4) S(6) Z(1), so column 5 is read first, then 3, and so on.
     Decryption fills the columns back in the same order and reads the table row-wise.</p>''',
     ['exp3_columnar.py']),
    ('Finding first address, last address and total number of addresses from a given IP address',
     'To write a program that takes an IP address in CIDR notation (a.b.c.d/n) and finds the first address, last '
     'address and total number of addresses in its block.',
     '''<p>In classless addressing an address is written as a.b.c.d/n, where n is the prefix length: the first
     n bits are the network part and the remaining 32 &minus; n bits are for hosts. The mask has n ones followed by
     32 &minus; n zeros.</p>
     <ul><li><b>First address</b> = address AND mask (host bits set to 0)</li>
     <li><b>Last address</b> = first address OR (NOT mask) (host bits set to 1)</li>
     <li><b>Total addresses</b> = 2<sup>32 &minus; n</sup></li></ul>
     <p>Example: 205.16.37.39/28. Mask = 255.255.255.240. Last octet 39 = 00100111; keeping 4 bits gives 00100000 = 32,
     so the block is 205.16.37.32 to 205.16.37.47, which is 2<sup>4</sup> = 16 addresses.</p>''',
     ['exp4_ip_range.py']),
    ('Two Processes interacting with each other Program',
     'To write a program in which two processes communicate with each other using TCP sockets.',
     '''<p>A <b>socket</b> is an end point of a two-way communication link, identified by an IP address and a port
     number. Two separate processes (even on different machines) can talk through a pair of connected sockets.</p>
     <p><b>Server process:</b> socket() &rarr; bind(IP, port) &rarr; listen() &rarr; accept() (waits for a client)
     &rarr; recv()/send() &rarr; close().<br>
     <b>Client process:</b> socket() &rarr; connect(server IP, port) &rarr; send()/recv() &rarr; close().</p>
     <p>Here both processes run on the same machine (127.0.0.1, port 5000) in two terminals and take turns sending
     messages until one of them types "bye". SOCK_STREAM means TCP, so the data arrives reliably and in order.</p>''',
     ['exp5_server.py', 'exp5_client.py']),
    ('One Server multiple Clients Program',
     'To write a server program that can handle many clients at the same time.',
     '''<p>A simple server can only talk to one client, because accept() and recv() block. To serve several clients
     together, the server creates a new <b>thread</b> for every accepted connection. The main thread keeps
     accepting new clients while each client thread handles its own client independently.</p>
     <p>The server below gives every client a number, prints what each client says, and replies to it. Three
     clients were run in three terminals at the same time.</p>''',
     ['exp6_server.py', 'exp6_client.py']),
    ('One Client interacts with other Client through the Server Program',
     'To write a program in which one client sends messages to another client through a server (chat relay).',
     '''<p>Clients do not connect to each other directly. Both connect to the server, and the server keeps a list of
     connected client sockets. Whenever a message arrives from one client, the server <b>forwards</b> it to the
     other connected client(s).</p>
     <p>Each client runs two things at once: the main thread reads from the keyboard and sends, and a separate
     receiving thread prints whatever the server forwards, so messages can arrive while the user is typing.</p>''',
     ['exp7_server.py', 'exp7_client.py']),
    ('One Client interacts with other Client through the Server by using encryption and decryption',
     'To write a program in which two clients chat through a server, with messages encrypted by the sender and '
     'decrypted by the receiver.',
     '''<p>This is experiment 7 with encryption added. The sending client encrypts the message with the
     <b>Caesar cipher</b> (shared key = 3) before sending it, the server only relays the cipher text, and the
     receiving client decrypts it with the same key.</p>
     <p>The server output shows that it only ever sees encrypted text, so even the relay in the middle cannot
     read the conversation (end-to-end encryption). Both clients must agree on the key beforehand.</p>''',
     ['exp8_server.py', 'exp8_client.py']),
]

CSS = '''
@page { size: A4; margin: 17mm 16mm 16mm 16mm; }
body { font-family: 'Times New Roman', Times, serif; font-size: 12pt; color: #000; margin: 0; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h2 { font-size: 16pt; text-decoration: underline; margin: 0 0 4mm; }
h3 { font-size: 13pt; text-decoration: underline; margin: 5mm 0 2mm; page-break-after: avoid; }
p { margin: 1.6mm 0; line-height: 1.45; text-align: justify; }
ul { margin: 1mm 0; padding-left: 7mm; line-height: 1.45; }
.eq { text-align: center; font-style: italic; }
table.idx { width: 100%; border-collapse: collapse; margin-top: 6mm; }
table.idx th, table.idx td { border: 1.3px solid #000; padding: 4mm 3mm; font-size: 12.5pt; vertical-align: top; }
table.idx th { background: #f0f0f0; }
table.idx td.sn { text-align: center; width: 12mm; }
table.idx td.d, table.idx td.s { width: 26mm; }
.fname { font-family: Consolas, monospace; font-size: 9.5pt; margin: 3mm 0 0.5mm; color: #333; page-break-after: avoid; break-after: avoid; }
pre.code { font-family: Consolas, 'Courier New', monospace; font-size: 8.8pt; line-height: 1.3; background: #f6f6f6;
           border: 1px solid #ddd; padding: 2.5mm 3mm; margin: 0 0 2mm; white-space: pre-wrap; }
pre.mini { font-family: Consolas, monospace; font-size: 9.5pt; margin: 1mm 0 1mm 8mm; }
.fig { margin: 2.5mm 0 3mm; text-align: center; page-break-inside: avoid; }
.fig img { width: 100%; }
.cap { text-align: center; font-size: 10.5pt; font-style: italic; margin-top: 1mm; }
'''

def keep_heading(h, figs):
    # glue the heading to the first figure so it never sits alone at a page bottom
    k = figs.find('</div></div>') + len('</div></div>')
    return f'<div style="page-break-inside: avoid"><h3>{h}</h3>{figs[:k]}</div>{figs[k:]}'


pages = []
rows = ''.join(f'<tr><td class="sn">{i:02d}.</td><td>{esc(t)}</td><td class="d"></td><td class="s"></td></tr>'
               for i, (t, *_rest) in enumerate(EXPS, 1))
pages.append(f'<div class="page"><h2 style="text-align:center">INDEX</h2><table class="idx"><tr><th>S.No</th>'
             f'<th>Programs</th><th>Date</th><th>Sign</th></tr>{rows}</table></div>')
for i, (title, aim, theory, files) in enumerate(EXPS, 1):
    pages.append(f'''<div class="page">
<h2>Experiment {i}: {esc(title)}</h2>
<h3>Aim</h3><p>{esc(aim)}</p>
<h3>Theory</h3>{theory}
<h3>Program</h3>{code(*files)}
{keep_heading('Output', shots[str(i)])}
</div>''')

body = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
pdf_from_html(body, HERE / 'body.pdf')

for theme in ('light',):
    chtml, ccss = cover(theme)
    pdf_from_html(f'<!doctype html><html><head><meta charset="utf-8"><style>@page {{ size: A4; margin: 0; }} '
                  f'body {{ margin: 0; }} {ccss}</style></head><body>{chtml}</body></html>', HERE / f'cover_{theme}.pdf')

out = fitz.open()
out.insert_pdf(fitz.open(HERE / 'cover_light.pdf'))
out.insert_pdf(fitz.open(HERE / 'body.pdf'))
final = LAB / 'CN Lab File - 24BCS064.pdf'
out.save(final, garbage=3, deflate=True)
print('pages', out.page_count, '->', final)
