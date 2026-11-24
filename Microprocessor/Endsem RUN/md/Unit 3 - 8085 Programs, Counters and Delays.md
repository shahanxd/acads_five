# MP Unit 3: 8085 Programs, Subroutines, Counters and Delays

*Endsem RUN · about 60 minutes*

**The whole unit in one breath:** writing real 8085 programs is about a few repeating patterns: a **pointer** (HL) walking through memory, a **counter** register with `DCR` + `JNZ` for loops, `CMP` + `JC/JNC` for decisions, and **delay loops** whose time you calculate from T-states.

**What the endsem asks from here:** Q3, every part a program: 2025 asked 8×8 multiplication by repeated addition, sorting 300 numbers, and a mod-10 counter with a 50 ms delay. **Every program in this doc was run on an 8085 simulator** (the sort on 300 random bytes, the delay counted to the exact T-state).

**How to write a "well documented" program (marks are given for this):** state the memory map (where the inputs are and where results go), write the algorithm in 3–5 steps, then the code with a comment on every line, and a sample input/output.

---

## 1. Program building blocks · Quick

| Pattern | Code |
| --- | --- |
| Point at an array | `LXI H, 2500H`, then `MOV A, M`, `INX H` |
| Loop N times | `MVI C, N` … `DCR C` / `JNZ LOOP` |
| 16-bit loop counter | `DCX B` / `MOV A, C` / `ORA B` / `JNZ LOOP` (DCX doesn't set flags, so test with ORA) |
| Compare A with M | `CMP M`: A < M → CY = 1; A = M → Z = 1 |
| 16-bit add | `DAD D` (HL ← HL + DE) |
| Subroutine | `CALL SUB` … `RET`; set up `LXI SP, …` first |

---

## 2. Multiplication by repeated addition · Slow down

The 8085 has no MUL. Multiplication is just repeated addition: 5 × 3 = 5 + 5 + 5. "Without shifting the multiplicand" means exactly this: add the multiplicand to a running total, multiplier-many times.

> **Endsem 2025 · Q3(a) · 4.5 marks**
> Write a well-documented 8085 assembly program to perform 8×8 multiplication without shifting the multiplicand.

**Answer.**

**Memory map:** multiplicand at 2500H, multiplier at 2501H; the 16-bit product goes to 2502H (low byte) and 2503H (high byte). (8 bits × 8 bits can need 16 bits: 255 × 255 = 65,025 = FE01H.)

**Algorithm:**

1. Load the multiplicand into DE (D = 00H), so it can be added as a 16-bit number.
2. Load the multiplier into C as the loop counter; clear HL (the product).
3. If the multiplier is 0, the product is 0: skip the loop.
4. Repeat: HL ← HL + DE (`DAD D`); C ← C − 1; until C = 0.
5. Store HL at 2502H–2503H.

```
        LDA 2500H       ; A = multiplicand
        MOV E, A        ; E = multiplicand
        MVI D, 00H      ; DE = 00:multiplicand (16-bit)
        LDA 2501H       ; A = multiplier
        MOV C, A        ; C = multiplier = number of additions
        LXI H, 0000H    ; HL = product = 0
        MOV A, C
        CPI 00H         ; multiplier = 0 ?
        JZ STORE        ; yes: product stays 0
LOOP:   DAD D           ; HL = HL + multiplicand (carries into H automatically)
        DCR C           ; one addition done
        JNZ LOOP        ; repeat until C = 0
STORE:  SHLD 2502H      ; [2502H] = L (low byte), [2503H] = H (high byte)
        HLT             ; stop
```

**Sample run:** [2500H] = 05H, [2501H] = 03H → HL = 0005 + 0005 + 0005 = **000FH** → [2502H] = 0FH, [2503H] = 00H. With FFH × FFH the result is **FE01H** (65,025). Both checked on the simulator, along with 0 × 7 = 0.

**Repeated 16-bit addition (DAD D) of the multiplicand, multiplier-many times, gives the 16-bit product in HL.**

---

## 3. Sorting · Slow down

**Bubble sort** in one picture: walk through the list comparing neighbours, and swap any pair that's in the wrong order. After one pass, the smallest value has sunk to the end (for descending order). Repeat the pass N − 1 times and the list is sorted.

> **Endsem 2025 · Q3(b) · 4.5 marks**
> Write a well-documented 8085 assembly program to arrange 300 integers stored at consecutive memory locations starting at 2200H in descending order.

**Answer.**

**The catch:** 300 is more than 255, so an 8-bit register can't count it. Both counters must be **16-bit** (299 = **012BH** comparisons per pass, 299 passes), and 16-bit counters need `DCX` + `ORA` to test for zero, because `DCX` doesn't set flags.

**Memory map:** the 300 bytes occupy 2200H to 232BH (2200H + 299). The outer (pass) counter is kept at 2100H–2101H, because all the registers are busy.

**Register use:** HL = pointer, DE = comparisons left in this pass, A = current element, B = temporary for the swap.

**Algorithm:**

1. Pass count = 299, saved in memory.
2. For each pass: HL = 2200H, DE = 299.
3. Compare the element at HL with the next one. If current < next, swap them (descending order wants bigger first).
4. Move HL forward; DE − 1; repeat until DE = 0.
5. Pass count − 1; repeat passes until it reaches 0.

```
        LXI H, 012BH    ; 299 passes needed (N - 1)
        SHLD 2100H      ; save pass counter in memory (registers are all in use)
OUTER:  LXI H, 2200H    ; HL -> first element
        LXI D, 012BH    ; DE = 299 comparisons in this pass
INNER:  MOV A, M        ; A = current element
        INX H           ; HL -> next element
        CMP M           ; compare current with next
        JNC SKIP        ; current >= next: order is fine, no swap
        MOV B, M        ; swap: B = next element
        MOV M, A        ;       next position <- current
        DCX H           ;       back to current position
        MOV M, B        ;       current position <- next
        INX H           ;       HL -> next element again
SKIP:   DCX D           ; one comparison done (DCX sets no flags)
        MOV A, D
        ORA E           ; Z = 1 only if DE = 0000H
        JNZ INNER       ; more comparisons in this pass
        LHLD 2100H      ; load pass counter
        DCX H           ; one pass done
        SHLD 2100H      ; save it back
        MOV A, H
        ORA L           ; all passes done?
        JNZ OUTER       ; no: next pass
        HLT             ; sorted in descending order
```

**Check:** run on 300 random bytes, the memory 2200H–232BH came out exactly equal to the bytes sorted in descending order, and the byte after the array was untouched.

**Bubble sort with 16-bit counters (DCX + ORA to test zero), swapping whenever current < next, sorts the 300 bytes in descending order.**

(For **ascending** order, swap when current > next instead: replace `JNC SKIP` with `JC SKIP` followed by `JZ SKIP`. With fewer than 256 elements, plain 8-bit counters with `DCR` + `JNZ` are enough.)

---

## 4. Counters and delay calculation · Slow down

A **delay** is a loop that does nothing useful except burn a known amount of time. To make it exact, count **T-states**.

**Delay with a 16-bit counter** (the usual one, because 8 bits only give ~1.8 ms):

```
DELAY:  LXI B, COUNT    ; 10 T
DLOOP:  DCX B           ;  6 T
        MOV A, C        ;  4 T
        ORA B           ;  4 T
        JNZ DLOOP       ; 10 T if taken, 7 T on the last pass
        RET             ; 10 T
```

Each pass through the loop costs 6 + 4 + 4 + 10 = **24 T** (the last one 21 T):

```latex
T_{\text{delay}} = 10 + 24 \times \text{COUNT} - 3 \quad (\text{+ CALL 18 T and RET 10 T})
```

> **Endsem 2025 · Q3(c) · 4.5 marks**
> Write an 8085 program to generate a modulo-10 counter with a delay of 50 ms between counts, on a system with a 0.5 µs clock period. Show all calculations.

**Answer.**

A **modulo-10 counter** counts 0, 1, 2 … 9 and then wraps back to 0, displaying each count on an output port, with a 50 ms delay between counts.

**Delay calculation.** Clock period T = 0.5 µs (a 2 MHz clock).

```latex
\begin{aligned}
\text{T-states needed} &= \frac{50 \text{ ms}}{0.5\ \mu s} = \frac{50 \times 10^{-3}}{0.5 \times 10^{-6}} = 100{,}000 \\
\text{Loop: } 24 \times \text{COUNT} &\approx 100{,}000 \\
\text{COUNT} &= \frac{100{,}000}{24} = 4166.7 \approx 4167 = 1047_H
\end{aligned}
```

Check with the exact formula (LXI + loops, excluding CALL/RET):

```latex
\begin{aligned}
T &= 10 + 24 \times 4167 - 3 = 100{,}015 \text{ T-states} \\
\text{Delay} &= 100{,}015 \times 0.5\ \mu s = 50.0075 \text{ ms} \approx 50 \text{ ms}
\end{aligned}
```

(Including CALL and RET adds 28 T: 50.02 ms. The error is under 0.05%.)

**Program** (count in D, displayed on port 01H):

```
START:  MVI D, 00H      ; count = 0
NEXT:   MOV A, D
        OUT 01H         ; display the count
        CALL DELAY      ; wait 50 ms
        INR D           ; next count
        MOV A, D
        CPI 0AH         ; reached 10 ?
        JNZ NEXT        ; no: display it
        JMP START       ; yes: wrap around to 0 (modulo 10)

DELAY:  LXI B, 1047H    ; COUNT = 4167 for 50 ms
DLOOP:  DCX B           ; 6 T
        MOV A, C        ; 4 T
        ORA B           ; 4 T  -> Z = 1 when BC = 0
        JNZ DLOOP       ; 10/7 T
        RET             ; 10 T
```

The count is kept in **D**, not A, because the delay routine uses A (`MOV A, C`); otherwise the count would be destroyed. (Alternatively, `PUSH PSW` / `POP PSW` inside DELAY.) Also set the stack pointer (`LXI SP, 27FFH`) at the start in a real kit, since CALL uses the stack.

**Simulator check:** the output port shows 00, 01, 02 … 09, 00 …, and one DELAY takes exactly 100,015 T = 50.0075 ms.

**COUNT = 100,000 / 24 ≈ 4167 = 1047H gives a 50 ms delay; the counter outputs 0–9 on a port and wraps at 0AH.**

---

## 5. More standard programs · Quick

These are the other programs the syllabus names (all simulator-checked).

**Largest of N numbers** (N at 2500H, numbers from 2501H, result at 2600H):

```
        LXI H, 2500H
        MOV C, M        ; C = N
        INX H
        MOV A, M        ; A = first number = largest so far
        DCR C
LOOP:   INX H
        CMP M           ; A < next ?
        JNC SKIP
        MOV A, M        ; yes: new largest
SKIP:   DCR C
        JNZ LOOP
        STA 2600H
        HLT
```

(For the **smallest**, change `JNC SKIP` to `JC SKIP`, so A is replaced when the next number is smaller.)

**8-bit division by repeated subtraction** (dividend 2500H, divisor 2501H → quotient 2502H, remainder 2503H):

```
        LDA 2501H
        MOV B, A        ; B = divisor
        LDA 2500H       ; A = dividend
        MVI C, 00H      ; C = quotient
LOOP:   CMP B           ; A < divisor ?
        JC DONE         ; yes: A is the remainder
        SUB B
        INR C
        JMP LOOP
DONE:   STA 2503H       ; remainder
        MOV A, C
        STA 2502H       ; quotient
        HLT
```

Example: 17 ÷ 5 → quotient 3, remainder 2.

**Binary to BCD (decimal)** (byte at 2500H → hundreds at 2501H, tens-and-units packed at 2502H):

```
        LDA 2500H
        MVI B, 00H      ; hundreds
        MVI C, 00H      ; tens
HUND:   CPI 64H         ; >= 100 ?
        JC TENS
        SUI 64H
        INR B
        JMP HUND
TENS:   CPI 0AH         ; >= 10 ?
        JC UNITS
        SUI 0AH
        INR C
        JMP TENS
UNITS:  MOV D, A        ; units
        MOV A, B
        STA 2501H       ; hundreds digit
        MOV A, C
        RLC
        RLC
        RLC
        RLC             ; tens into the upper nibble
        ORA D           ; + units
        STA 2502H       ; packed BCD tens:units
        HLT
```

Example: FFH = 255 → [2501H] = 02, [2502H] = 55H. (For **ASCII**, add 30H to each digit: '2' = 32H, '5' = 35H.)

---

## 6. Quick recap

- Document programs: memory map, algorithm, commented code, sample run.
- Multiplication: DAD D repeated multiplier times (HL = 16-bit product).
- 300 elements: 16-bit counters; `DCX rp` + `MOV A, low` + `ORA high` + `JNZ`.
- Descending bubble sort: swap when current < next (`JNC SKIP`).
- Delay with BC: 24 T per loop; COUNT = (delay / T) / 24. 50 ms at 0.5 µs → 1047H.
- Keep the counter out of A if the delay uses A.
