"""Compile (and run, when no input is needed) every complete program in a study markdown file.

Usage: python tools/checkcode.py <file.md> [...]
C++ blocks (```cpp) with 'main(' are compiled with g++ -std=c++17. Java blocks (```java) with
'static void main' are compiled with tools/jdk/*/bin/javac. Programs that read input are only compiled,
unless a comment line '// stdin: ...' gives the input ('\\n' for new lines).
"""
import pathlib, re, subprocess, sys, tempfile, glob

HERE = pathlib.Path(__file__).resolve().parent
JDK = sorted(glob.glob(str(HERE / 'jdk' / '*' / 'bin')))
JAVAC = str(pathlib.Path(JDK[0]) / 'javac') if JDK else None
JAVA = str(pathlib.Path(JDK[0]) / 'java') if JDK else None

def run(cmd, cwd, stdin=None):
    return subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=20)

def check(md):
    text = pathlib.Path(md).read_text(encoding='utf-8')
    blocks = re.findall(r'```(cpp|java)\n(.*?)```', text, flags=re.S)
    n = 0
    for lang, code in blocks:
        if lang == 'cpp' and 'main(' not in code: continue
        if lang == 'java' and 'static void main' not in code: continue
        n += 1
        m = re.search(r'//\s*stdin:\s*(.*)', code)
        stdin = m.group(1).replace('\\n', '\n') + '\n' if m else None
        reads = bool(re.search(r'\bcin\b|Scanner|readLine', code))
        d = pathlib.Path(tempfile.mkdtemp())
        head = code.strip().splitlines()[0][:70]
        if lang == 'cpp':
            src = d / 'a.cpp'; src.write_text(code, encoding='utf-8')
            r = run(['g++', '-std=c++17', '-w', 'a.cpp', '-o', 'a.exe'], d)
            if r.returncode: print(f'[{n}] CPP COMPILE FAIL ({head})\n{r.stderr[:1500]}'); continue
            if reads and stdin is None: print(f'[{n}] cpp compiled (reads input, not run)'); continue
            r = run([str(d / 'a.exe')], d, stdin)
        else:
            if not JAVAC: print(f'[{n}] java skipped (no JDK)'); continue
            pub = re.search(r'public\s+class\s+(\w+)', code)
            mains = re.findall(r'class\s+(\w+)[^{]*\{(?:(?!class\s).)*?static\s+void\s+main', code, flags=re.S)
            fname = (pub.group(1) if pub else 'Main') + '.java'
            (d / fname).write_text(code, encoding='utf-8')
            r = run([JAVAC, '-nowarn', fname], d)
            if r.returncode: print(f'[{n}] JAVA COMPILE FAIL ({head})\n{r.stderr[:1500]}'); continue
            if reads and stdin is None: print(f'[{n}] java compiled (reads input, not run)'); continue
            cls = mains[-1] if mains else fname[:-5]
            r = run([JAVA, '-cp', '.', cls], d, stdin)
        out = (r.stdout + r.stderr).strip().replace('\n', ' | ')
        print(f'[{n}] {lang} OK -> {out[:400]}')
    if n == 0: print('no complete programs')

if __name__ == '__main__':
    for a in sys.argv[1:]:
        print('#####', pathlib.Path(a).name); check(a)
