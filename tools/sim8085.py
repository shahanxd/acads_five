"""Tiny 8085 simulator for checking study-doc programs (common instructions only), with T-state counting.

Usage (Python): from sim8085 import run
    cpu = run(source_text, mem={0x2500: 5}, start=0x2000, max_steps=10**7)
    cpu.mem[...], cpu.r['A'], cpu.t (T-states), cpu.out (list of (port, value))
Labels end with ':'; comments start with ';'. Numbers like 2500H, 0AH, 12 (decimal).
"""
import re

T = {'MOV': 4, 'MOVM': 7, 'MVI': 7, 'MVIM': 10, 'LXI': 10, 'LDA': 13, 'STA': 13, 'LHLD': 16, 'SHLD': 16,
     'LDAX': 7, 'STAX': 7, 'XCHG': 4, 'ADD': 4, 'ADDM': 7, 'ADC': 4, 'ADCM': 7, 'ADI': 7, 'ACI': 7, 'SUB': 4,
     'SUBM': 7, 'SBB': 4, 'SUI': 7, 'SBI': 7, 'INR': 4, 'INRM': 10, 'DCR': 4, 'DCRM': 10, 'INX': 6, 'DCX': 6,
     'DAD': 10, 'ANA': 4, 'ANAM': 7, 'ANI': 7, 'ORA': 4, 'ORAM': 7, 'ORI': 7, 'XRA': 4, 'XRAM': 7, 'XRI': 7,
     'CMP': 4, 'CMPM': 7, 'CPI': 7, 'CMA': 4, 'CMC': 4, 'STC': 4, 'RLC': 4, 'RRC': 4, 'RAL': 4, 'RAR': 4,
     'DAA': 4, 'JMP': 10, 'CALL': 18, 'RET': 10, 'PUSH': 12, 'POP': 10, 'OUT': 10, 'IN': 10, 'HLT': 5, 'NOP': 4}
T.update({j: 10 for j in ('JZ','JNZ','JC','JNC','JM','JP','JPE','JPO')})
JCC = {'JZ': ('Z', 1), 'JNZ': ('Z', 0), 'JC': ('CY', 1), 'JNC': ('CY', 0), 'JM': ('S', 1), 'JP': ('S', 0),
       'JPE': ('P', 1), 'JPO': ('P', 0)}

def num(s, labels):
    s = s.strip()
    if s in labels: return labels[s]
    if s.upper().endswith('H'): return int(s[:-1], 16)
    return int(s)

class CPU:
    def __init__(self):
        self.r = dict.fromkeys('ABCDEHL', 0); self.f = dict(S=0, Z=0, AC=0, P=0, CY=0)
        self.mem = [0] * 65536; self.sp = 0xFFFF; self.t = 0; self.out = []
    def pair(self, p):
        a, b = {'B': 'BC', 'D': 'DE', 'H': 'HL'}[p]
        return (self.r[a] << 8) | self.r[b]
    def setpair(self, p, v):
        if p == 'SP': self.sp = v & 0xFFFF; return
        a, b = {'B': 'BC', 'D': 'DE', 'H': 'HL'}[p]
        self.r[a], self.r[b] = (v >> 8) & 0xFF, v & 0xFF
    def get(self, x): return self.mem[self.pair('H')] if x == 'M' else self.r[x]
    def put(self, x, v):
        if x == 'M': self.mem[self.pair('H')] = v & 0xFF
        else: self.r[x] = v & 0xFF
    def szp(self, v):
        v &= 0xFF; self.f['S'] = v >> 7; self.f['Z'] = int(v == 0); self.f['P'] = int(bin(v).count('1') % 2 == 0)

def run(src, mem=None, start=0x2000, max_steps=10 ** 7):
    lines, labels = [], {}
    for raw in src.splitlines():
        s = raw.split(';')[0].strip()
        if not s: continue
        m = re.match(r'(\w+):\s*(.*)', s)
        if m: labels[m.group(1)] = len(lines); s = m.group(2).strip()
        if s: lines.append(s)
    cpu = CPU()
    for k, v in (mem or {}).items(): cpu.mem[k] = v & 0xFF
    pc, steps, stack = 0, 0, []
    while pc < len(lines) and steps < max_steps:
        steps += 1
        parts = lines[pc].replace(',', ' ').split()
        op, a = parts[0].upper(), [p.upper() for p in parts[1:]]
        pc += 1
        key = op + ('M' if 'M' in a[:2] and op not in ('LXI', 'JMP', 'JM', 'CALL') and not op.startswith('J') else '')
        cpu.t += T.get(key, T.get(op, 4))
        A = cpu.r['A']
        if op == 'MOV': cpu.put(a[0], cpu.get(a[1]))
        elif op == 'MVI': cpu.put(a[0], num(parts[2], labels))
        elif op == 'LXI': cpu.setpair(a[0], num(parts[2], labels))
        elif op == 'LDA': cpu.r['A'] = cpu.mem[num(a[0], labels)]
        elif op == 'STA': cpu.mem[num(a[0], labels)] = A
        elif op == 'LHLD': ad = num(a[0], labels); cpu.r['L'], cpu.r['H'] = cpu.mem[ad], cpu.mem[ad + 1]
        elif op == 'SHLD': ad = num(a[0], labels); cpu.mem[ad], cpu.mem[ad + 1] = cpu.r['L'], cpu.r['H']
        elif op == 'XCHG': d, h = cpu.pair('D'), cpu.pair('H'); cpu.setpair('D', h); cpu.setpair('H', d)
        elif op in ('ADD', 'ADC', 'ADI', 'ACI'):
            v = num(parts[1], labels) if op in ('ADI', 'ACI') else cpu.get(a[0])
            c = cpu.f['CY'] if op in ('ADC', 'ACI') else 0
            res = A + v + c; cpu.f['CY'] = int(res > 0xFF); cpu.f['AC'] = int((A & 15) + (v & 15) + c > 15)
            cpu.r['A'] = res & 0xFF; cpu.szp(res)
        elif op in ('SUB', 'SBB', 'SUI', 'SBI', 'CMP', 'CPI'):
            v = num(parts[1], labels) if op in ('SUI', 'SBI', 'CPI') else cpu.get(a[0])
            c = cpu.f['CY'] if op in ('SBB', 'SBI') else 0
            res = A - v - c; cpu.f['CY'] = int(res < 0); cpu.szp(res)
            if op not in ('CMP', 'CPI'): cpu.r['A'] = res & 0xFF
        elif op in ('INR', 'DCR'):
            v = (cpu.get(a[0]) + (1 if op == 'INR' else -1)) & 0xFF; cpu.put(a[0], v); cpu.szp(v)
        elif op in ('INX', 'DCX'):
            if a[0] == 'SP': cpu.sp = (cpu.sp + (1 if op == 'INX' else -1)) & 0xFFFF
            else: cpu.setpair(a[0], (cpu.pair(a[0]) + (1 if op == 'INX' else -1)) & 0xFFFF)
        elif op == 'DAD':
            res = cpu.pair('H') + cpu.pair(a[0]); cpu.f['CY'] = int(res > 0xFFFF); cpu.setpair('H', res & 0xFFFF)
        elif op in ('ANA', 'ANI', 'ORA', 'ORI', 'XRA', 'XRI'):
            v = num(parts[1], labels) if op[-1] == 'I' else cpu.get(a[0])
            res = {'AN': A & v, 'OR': A | v, 'XR': A ^ v}[op[:2]]
            cpu.r['A'] = res; cpu.szp(res); cpu.f['CY'] = 0
        elif op == 'CMA': cpu.r['A'] = (~A) & 0xFF
        elif op == 'STC': cpu.f['CY'] = 1
        elif op == 'CMC': cpu.f['CY'] ^= 1
        elif op == 'RLC': cpu.f['CY'] = A >> 7; cpu.r['A'] = ((A << 1) | (A >> 7)) & 0xFF
        elif op == 'RRC': cpu.f['CY'] = A & 1; cpu.r['A'] = ((A >> 1) | ((A & 1) << 7)) & 0xFF
        elif op == 'RAL': c = cpu.f['CY']; cpu.f['CY'] = A >> 7; cpu.r['A'] = ((A << 1) | c) & 0xFF
        elif op == 'RAR': c = cpu.f['CY']; cpu.f['CY'] = A & 1; cpu.r['A'] = (A >> 1) | (c << 7)
        elif op == 'JMP': pc = labels[parts[1]]
        elif op in JCC:
            fl, want = JCC[op]
            if cpu.f[fl] == want: pc = labels[parts[1]]
            else: cpu.t -= 3                  # not taken: 7 T instead of 10
        elif op == 'CALL': stack.append(pc); pc = labels[parts[1]]
        elif op == 'RET': pc = stack.pop()
        elif op == 'OUT': cpu.out.append((num(parts[1], labels), A))
        elif op == 'HLT': break
        elif op == 'NOP': pass
        else: raise ValueError('unsupported: ' + lines[pc - 1])
    cpu.steps = steps
    return cpu
