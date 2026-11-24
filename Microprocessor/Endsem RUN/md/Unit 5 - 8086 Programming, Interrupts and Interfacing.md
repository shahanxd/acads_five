# MP Unit 5: 8086 Programming, Software Interrupts and Interfacing

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** writing real 8086 programs with an assembler (**MASM/TASM**): the program skeleton with segments, counting and conversion programs, **software interrupts** (INT 21H for DOS services), mixing **assembly with C**, and how an 8086 system is built from support chips.

**What the endsem asks from here:** Q5 every year: two 8086 programs and the "assembly with C + software interrupts" theory. 2025 asked counting positive/negative numbers and 16-bit binary to BCD. **Both programs were assembled and run on an x86 emulator** (keystone + unicorn) with test data.

---

## 1. MASM / TASM and the program skeleton · Quick

**MASM** (Microsoft Macro Assembler) and **TASM** (Turbo Assembler, Borland) turn 8086 assembly into machine code: `PROG.ASM` → assemble → `PROG.OBJ` → link → `PROG.EXE` → run (debug with DEBUG/TD).

**Directives** are instructions to the assembler, not to the CPU (they produce no machine code):

| Directive | Meaning |
| --- | --- |
| `SEGMENT` / `ENDS` | Start / end a segment |
| `ASSUME CS:CODE, DS:DATA` | Tell the assembler which segment register holds which segment |
| `DB`, `DW`, `DD` | Define byte / word / double word data |
| `DUP` | Repeat: `10 DUP(0)` = ten zeros |
| `EQU` | Name a constant: `N EQU 10` |
| `PROC` / `ENDP` | Start / end a procedure |
| `OFFSET`, `LEA` | Offset of a variable |
| `END label` | End of the program; label = entry point |

**The skeleton every program uses:**

```
DATA SEGMENT
    ; variables here
DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE, DS:DATA
START:  MOV AX, DATA        ; DS can't be loaded with an immediate value,
        MOV DS, AX          ; so go through AX
        ; program here
        MOV AH, 4CH         ; DOS function 4CH: terminate
        INT 21H
CODE ENDS
END START
```

---

## 2. Counting positive and negative numbers · Slow down

A 16-bit number is **negative** (in two's complement) exactly when its **top bit (bit 15) is 1**. So `CMP AX, 0` followed by `JL` (jump if less, signed) or simply `TEST AX, 8000H` / the sign flag tells them apart.

> **Endsem 2025 · Q5(a) · 4.5 marks**
> Write an 8086 assembly program to find the number of positive numbers and the number of negative numbers among N 16-bit numbers stored at consecutive memory locations.

**Answer.**

**Logic:** walk through the list with SI; for each word, compare with 0: if less (signed), count it as negative; if zero, count separately (zero is neither positive nor negative); otherwise count as positive. LOOP runs it N times. Counters: BX = positive, DX = negative, DI = zero.

```
DATA SEGMENT
    LIST  DW 5, -3, 0, 32767, -32768, 100, -1, 0, 7   ; N 16-bit signed numbers
    N     EQU 9
    POS   DW ?                    ; count of positive numbers
    NEGC  DW ?                    ; count of negative numbers (NEG is a mnemonic)
    ZER   DW ?                    ; count of zeros
DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE, DS:DATA
START:    MOV AX, DATA
          MOV DS, AX              ; initialise DS
          LEA SI, LIST            ; SI -> first number
          MOV CX, N               ; CX = how many numbers
          XOR BX, BX              ; positive count = 0
          XOR DX, DX              ; negative count = 0
          XOR DI, DI              ; zero count = 0
NEXT:     MOV AX, [SI]            ; AX = current number
          CMP AX, 0               ; signed comparison with 0
          JL NEGATIVE             ; AX < 0 (sign bit set)
          JZ ZERO                 ; AX = 0
          INC BX                  ; AX > 0: positive
          JMP CONT
NEGATIVE: INC DX
          JMP CONT
ZERO:     INC DI
CONT:     ADD SI, 2               ; next word (2 bytes)
          LOOP NEXT               ; CX - 1; repeat until CX = 0
          MOV POS, BX             ; store the results
          MOV NEGC, DX
          MOV ZER, DI
          MOV AH, 4CH
          INT 21H                 ; return to DOS
CODE ENDS
END START
```

**Emulator result** for the 9 numbers above: POS = **4** (5, 32767, 100, 7), NEGC = **3** (−3, −32768, −1), ZER = **2**.

**Compare each word with 0 (signed): JL → negative count, JZ → zero count, else positive count; step SI by 2 and LOOP N times.**

(If the question wants zero counted as positive, drop the `JZ ZERO` line.)

---

## 3. Binary to BCD conversion · Slow down

**BCD** stores each decimal digit in 4 bits. A 16-bit binary number goes up to FFFFH = 65,535, which has **5 decimal digits**. The trick: **divide by 10 repeatedly**; each remainder is the next decimal digit, from the units upward. Like peeling the last digit off a number again and again.

> **Endsem 2025 · Q5(c) · 4.5 marks**
> Write an 8086 assembly program to convert a 16-bit binary number into its equivalent BCD number.

**Answer.**

**Logic:**

1. AX = the binary number. Divide DX:AX by 10 five times (DX cleared each time): the remainder (DX, 0–9) is a decimal digit, the quotient (AX) is kept for the next division. Store the 5 digits, units first.
2. **Pack** them: two digits per byte (tens:units, thousands:hundreds, ten-thousands), shifting the higher digit left by 4.

```
DATA SEGMENT
    BIN    DW 0FFFFH          ; 16-bit binary number (65535)
    DIGITS DB 5 DUP(?)        ; unpacked decimal digits, units first
    BCD    DB 3 DUP(?)        ; packed BCD, lowest byte first
DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE, DS:DATA
START:  MOV AX, DATA
        MOV DS, AX
        MOV AX, BIN           ; AX = number to convert
        MOV BX, 10            ; divisor
        LEA SI, DIGITS
        MOV CX, 5             ; 5 decimal digits
NEXTD:  XOR DX, DX            ; DX:AX = number (clear the high word)
        DIV BX                ; AX = quotient, DX = remainder (a digit 0-9)
        MOV [SI], DL          ; save the digit
        INC SI
        LOOP NEXTD
        MOV CL, 4             ; shift count for packing
        MOV AL, DIGITS+1      ; tens
        SHL AL, CL            ; into the upper nibble
        OR  AL, DIGITS        ; + units
        MOV BCD, AL           ; BCD byte 0 = tens:units
        MOV AL, DIGITS+3      ; thousands
        SHL AL, CL
        OR  AL, DIGITS+2      ; + hundreds
        MOV BCD+1, AL         ; BCD byte 1 = thousands:hundreds
        MOV AL, DIGITS+4      ; ten-thousands
        MOV BCD+2, AL         ; BCD byte 2
        MOV AH, 4CH
        INT 21H
CODE ENDS
END START
```

**Trace for FFFFH = 65,535:** 65535 ÷ 10 = 6553 r **5**; 6553 ÷ 10 = 655 r **3**; 655 ÷ 10 = 65 r **5**; 65 ÷ 10 = 6 r **5**; 6 ÷ 10 = 0 r **6**. Digits (units first) 5, 3, 5, 5, 6 → BCD bytes **35H, 55H, 06H**, i.e. 06 55 35 = **065535**.

**Emulator check:** FFFFH → 06 55 35; 04D2H (1234) → 00 12 34; A000H (40960) → 04 09 60; 0 → 00 00 00.

**Repeated DIV by 10 peels off the decimal digits (remainders, units first); pairs of digits are packed with SHL 4 and OR into BCD bytes.**

---

## 4. Software interrupts and assembly with C · Slow down

**8086 interrupts:** **256 types** (0–255) from hardware (NMI, and INTR when IF = 1), software (`INT n`) and CPU exceptions (type 0 divide error, 1 single step, 2 NMI, 3 breakpoint, 4 overflow). The **Interrupt Vector Table (IVT)** in the first 1 KB of memory holds each type's ISR address in 4 bytes (IP, then CS): **IVT address = type × 4** (INT 21H → 84H).

On an interrupt: push flags, clear IF and TF, push CS and IP, load the new IP and CS from the IVT, run the ISR, and `IRET` pops it all back.

> **Endsem 2025 · Q5(b) · 4.5 marks**
> Can assembly language be used with C programming? If yes, discuss how with a suitable example. Also discuss how software interrupts are used in programming, with a suitable example.

**Answer.**

**Yes.** Assembly is mixed with C when part of a program must be very fast or must touch hardware directly (ports, interrupts, special registers), while the rest stays in readable, portable C. Two ways:

**(a) Inline assembly:** assembly instructions written directly inside a C function, using the compiler's `asm` keyword (e.g. Turbo C / Borland C for 16-bit DOS). C variables can be used by name.

```c
#include <stdio.h>
int main() {
    int a = 10, b = 20, sum;
    asm {
        mov ax, a       /* load C variable a */
        add ax, b       /* add C variable b */
        mov sum, ax     /* store into C variable sum */
    }
    printf("Sum = %d", sum);   /* prints: Sum = 30 */
    return 0;
}
```

**(b) Separate assembly module:** write a procedure in a `.ASM` file, declare it `PUBLIC`, assemble it with MASM/TASM, declare it `extern` in C, and **link** the two object files. C passes arguments on the **stack** (right to left) and expects the return value in **AX**; the procedure name gets a leading underscore.

```
; ADD2.ASM  -- called from C as  int add2(int x, int y);
PUBLIC _add2
CODE SEGMENT
    ASSUME CS:CODE
_add2   PROC NEAR
        PUSH BP
        MOV BP, SP
        MOV AX, [BP+4]      ; first argument x
        ADD AX, [BP+6]      ; second argument y
        POP BP
        RET                 ; result returned in AX
_add2   ENDP
CODE ENDS
END
```

```c
extern int add2(int x, int y);
int main() { printf("%d", add2(10, 20)); }   /* prints 30 */
```

**Software interrupts in programming.** The instruction `INT n` works like a call through the IVT: the program only needs the **type number**, not the routine's address, so it can use services provided by the **BIOS** (built-in firmware) and **DOS** without knowing where they are in memory. The service is selected by a value in **AH**:

| Call | Service |
| --- | --- |
| INT 21H, AH = 01H | Read a key (with echo) into AL |
| INT 21H, AH = 02H | Display the character in DL |
| INT 21H, AH = 09H | Display the string at DS:DX, ending with `$` |
| INT 21H, AH = 4CH | Terminate the program |
| INT 10H | BIOS video services (cursor, mode, pixels) |
| INT 16H | BIOS keyboard services |

```
DATA SEGMENT
    MSG DB 'Hello, JMI$'
DATA ENDS
CODE SEGMENT
    ASSUME CS:CODE, DS:DATA
START:  MOV AX, DATA
        MOV DS, AX
        MOV AH, 09H       ; DOS: display string
        LEA DX, MSG       ; DS:DX -> message
        INT 21H           ; prints Hello, JMI
        MOV AH, 4CH       ; DOS: terminate
        INT 21H
CODE ENDS
END START
```

Programs can also **install their own ISR** for a type (change the IVT entry with INT 21H AH = 25H) and trigger it with `INT n`, e.g. for debugging (INT 3 breakpoint).

**Yes: through inline `asm` blocks or separately assembled PUBLIC procedures linked with C (arguments on the stack, result in AX). Software interrupts (INT n) call BIOS/DOS services through the IVT, e.g. INT 21H with AH = 09H to print and 4CH to exit.**

---

## 5. Interfacing with the 8086 and system design · Quick

**A minimum-mode 8086 system** needs these support chips:

- **8284 clock generator:** makes CLK (from a crystal at 3× frequency), and synchronises READY and RESET.
- **Address latches (3 × 74LS373):** grab A19–A0 from the multiplexed AD15–AD0 and A19/S6–A16/S3 lines when ALE is high; BHE̅ is latched too.
- **Data transceivers (2 × 74LS245):** buffer the 16-bit data bus in both directions, controlled by **DT/R̅** (direction) and **DEN̅** (enable).
- **Memory:** two banks: **even bank** enabled by **A0 = 0** (D7–D0), **odd bank** by **BHE̅ = 0** (D15–D8), so a word at an even address is one bus cycle.
- **I/O:** 8255 (parallel ports), 8253/8254 (timers), 8251 (serial), 8259 (interrupt controller), 8257/8237 (DMA), selected by an address decoder (74LS138) using M/IO̅ (1 = memory on the 8086).

**Microprocessor-based system design** steps: understand the requirements (inputs, outputs, speed) → choose the processor and memory size → draw the memory and I/O map → design the address decoding → choose interface chips → write and test the software → integrate and debug. Example: a temperature controller = sensor → ADC → 8255 input port, 8086 program compares with a set point, output port → relay for the heater, a display on another port, and an 8253 timer for sampling every second.

---

## 6. Quick recap

- MASM skeleton: DATA/CODE segments, ASSUME, `MOV AX, DATA` / `MOV DS, AX`, end with `MOV AH, 4CH` + `INT 21H`.
- Negative 16-bit number ⇔ bit 15 = 1; `CMP AX, 0` + `JL` / `JZ`.
- Binary → BCD: DIV by 10 repeatedly (remainders = digits, units first), pack with SHL 4 + OR.
- 256 interrupt types; IVT entry = type × 4; INT 21H services by AH (01, 02, 09, 4CH).
- Assembly + C: inline `asm` blocks, or PUBLIC procedures linked with C (args on stack, result in AX).
- 8086 system: 8284 clock, 74LS373 latches, 74LS245 transceivers, even/odd banks (A0, BHE̅).
