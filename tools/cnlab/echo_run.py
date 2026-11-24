"""Run a script so that whatever input() reads from a pipe is echoed to stdout,
the way it would appear when typed into a real terminal."""
import builtins, runpy, sys

def _input(prompt=''):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    line = line.rstrip('\n')
    sys.stdout.write(line + '\n')
    sys.stdout.flush()
    return line

builtins.input = _input
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
