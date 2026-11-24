"""Actually run every CN lab program (sockets on localhost) with timed keyboard input,
and save each terminal's transcript to transcripts.json."""
import json, pathlib, subprocess, sys, threading, time

HERE = pathlib.Path(__file__).resolve().parent
PROG = HERE.parents[1] / 'Computer Networks' / 'Lab' / 'programs'
ECHO = HERE / 'echo_run.py'


class Term:
    def __init__(self, script):
        self.script = script
        self.out = []
        self.p = subprocess.Popen([sys.executable, '-u', str(ECHO), script], cwd=PROG,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, encoding='utf-8', bufsize=1)
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for ch in iter(lambda: self.p.stdout.read(1), ''):
            self.out.append(ch)

    def type(self, line):
        self.p.stdin.write(line + '\n')
        self.p.stdin.flush()

    def finish(self, kill=False, wait=3):
        if kill:
            time.sleep(0.5)
            self.p.kill()
        else:
            try:
                self.p.wait(timeout=wait)
            except subprocess.TimeoutExpired:
                self.p.kill()
        time.sleep(0.3)
        return ''.join(self.out)


def session(script, steps, kill=False):
    """steps: list of (delay, terminal_key, text). terminals created on first 'start'."""
    terms = {}
    for delay, key, text in steps:
        time.sleep(delay)
        if text is None:
            terms[key] = Term(script[key])
        else:
            terms[key].type(text)
    return terms


def simple(script, lines, gap=0.4):
    t = Term(script)
    time.sleep(0.6)
    for ln in lines:
        t.type(ln)
        time.sleep(gap)
    return t.finish()


res = {}
res['1'] = {'run1': simple('exp1_caesar.py', ['Computer Networks Lab', '3']),
            'run2': simple('exp1_caesar.py', ['Meet me at JMI gate 7', '11'])}
res['2'] = {'run1': simple('exp2_railfence.py', ['WEAREDISCOVEREDFLEEATONCE', '3']),
            'run2': simple('exp2_railfence.py', ['networks lab', '2'])}
res['3'] = {'run1': simple('exp3_columnar.py', ['WEAREDISCOVEREDFLEEATONCE', 'ZEBRAS'])}
res['4'] = {'run1': simple('exp4_ip_range.py', ['205.16.37.39/28', '192.168.10.77/24', '172.16.45.130/20', 'q'])}

# 5: two processes
S = {'server': 'exp5_server.py', 'client': 'exp5_client.py'}
T = session(S, [(0, 'server', None), (1.0, 'client', None),
                (1.0, 'client', 'hello, this is the client process'),
                (1.0, 'server', 'hi client, server process here'),
                (1.0, 'client', 'sending some data: 1011 0110'),
                (1.0, 'server', 'got it, 8 bits received'),
                (1.0, 'client', 'ok thanks'),
                (1.0, 'server', 'bye')])
res['5'] = {k: t.finish() for k, t in T.items()}

# 6: one server, three clients
S = {'server': 'exp6_server.py', 'client1': 'exp6_client.py', 'client2': 'exp6_client.py', 'client3': 'exp6_client.py'}
T = session(S, [(0, 'server', None), (1.0, 'client1', None), (1.5, 'client2', None), (1.5, 'client3', None),
                (1.0, 'client1', 'hello from client one'),
                (0.6, 'client2', 'client two here'),
                (0.6, 'client3', 'is the server busy?'),
                (0.6, 'client1', 'what time is the lab'),
                (0.6, 'client3', 'ok bye'), (0.2, 'client3', 'bye'),
                (0.6, 'client2', 'bye'),
                (0.6, 'client1', 'bye')])
time.sleep(1)
res['6'] = {k: t.finish(kill=(k == 'server')) for k, t in T.items()}

# 7: client to client through server
for exp, srv, cli, msgs in [
        ('7', 'exp7_server.py', 'exp7_client.py',
         [('a', 'hey rahul, you there?'), ('b', 'yes, got your message'), ('a', 'did you finish the CN lab file'),
          ('b', 'almost, only exp 8 left'), ('a', 'cool, see you tomorrow'), ('b', 'bye'), ('a', 'bye')]),
        ('8', 'exp8_server.py', 'exp8_client.py',
         [('a', 'Hello Rahul'), ('b', 'Hi Shahan, message received'), ('a', 'meet at lab 4 at 10'),
          ('b', 'ok done'), ('b', 'bye'), ('a', 'bye')])]:
    S = {'server': srv, 'clientA': cli, 'clientB': cli}
    steps = [(0, 'server', None), (1.0, 'clientA', None), (0.8, 'clientA', 'shahan'),
             (0.6, 'clientB', None), (0.8, 'clientB', 'rahul')]
    steps += [(1.0, 'clientA' if who == 'a' else 'clientB', m) for who, m in msgs]
    T = session(S, steps)
    time.sleep(1)
    res[exp] = {k: t.finish(kill=(k == 'server')) for k, t in T.items()}

(HERE / 'transcripts.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
for e, d in res.items():
    for k, v in d.items():
        print(f'===== exp {e} / {k}\n{v}')
