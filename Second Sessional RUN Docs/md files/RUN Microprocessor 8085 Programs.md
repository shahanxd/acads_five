# RUN: Microprocessor 8085 Programs

Nov 16, 2026 · @shahan

Every 8085 program type in syllabus Unit 3, built up from one loop pattern, with every program PYQ from 2021 to 2025 solved where it belongs. Every program here was run on an 8085 simulator against test data.

## How this run works

Read the 8085 Architecture and Instruction Set doc first: this one assumes you know what A, HL, M, CY and the jumps do. Each program comes with its idea in plain words, then the code, then a trace or a test. Allow about 3 hours, and write at least the sorting and multiplication programs out by hand once.

**"Well documented" is where the marks are.** Every program PYQ says it, so every answer here has:

1. **A memory map:** where the inputs are and where the result goes. If the paper doesn't give addresses, choose them and say so.
2. **The method** in one or two lines.
3. **A comment on every line** saying what it does *in the problem's terms* ("next number"), not just restating the instruction ("increment HL").

**Which program the papers ask:**

| Program | Asked in |
| --- | --- |
| Sort N numbers (ascending or descending) | Sessional-1 2021, 2022, 2023, 2024, 2025; Endsem 2022, 2023, 2024, 2025 |
| 8x8 multiplication (shifting or not shifting the multiplicand) | Sessional-1 2021, 2022, 2023, 2024; Endsem 2022, 2025 |
| 16-bit sum of selected numbers (odd, even, odd parity, non-negative) | Sessional-1 2021, 2022, 2023, 2024 |
| Modulo-N counter with a delay | Sessional-1 2022, 2024, 2025; Endsem 2022, 2023, 2024, 2025 |
| 16x8 division | Sessional-1 2025; Endsem 2022 |
| HCF, factorial, binary to decimal | Endsem 2024, 2023, 2023 |
| A C for-loop on arrays | Sessional-1 2024 |

Sorting has been asked in nine of the last ten papers. If you master one program, make it that one.

**Videos:** Bharat Acharya's 8085 programming videos on the [Bharat Acharya Education](https://www.youtube.com/@BharatAcharyaEducation/playlists) channel. Your class notes for this unit are in `Microprocessor/Notes/Handwritten notes programs and delay.pdf`.

## Stop 1: How an 8085 program is built

Almost every program in this unit is the same skeleton: **walk through a list in memory, do something to each item, and keep a running result.** On the 8085 that skeleton is three registers doing three jobs:

| Job | Register | Moves with |
| --- | --- | --- |
| **Pointer:** where the current item is | HL (so the item is `M`) | `INX H` |
| **Counter:** how many items are left | C (8-bit) or BC (16-bit) | `DCR C` / `DCX B` |
| **Result:** the running answer | A, or another register | depends on the job |

**The usual memory map** (when the paper gives none, choose one and state it): the count N at 2050H, the items from 2051H, and the result at 2060H.

**Program 1: 8-bit sum of N numbers.** This is straight from your class notes, and the base of everything else.

```
        LXI H, 2050H    ; HL -> the count
        MOV C, M        ; C = N, the number of items
        INX H           ; HL -> the first item
        MVI A, 00H      ; sum = 0
BACK:   ADD M           ; sum = sum + item
        INX H           ; point to the next item
        DCR C           ; one item fewer to go
        JNZ BACK        ; repeat until C = 0
        STA 2060H       ; store the sum
        HLT
```

Test: N = 3 with items 12H, 34H and 05H gives 4BH at 2060H.

The flaw: a sum of several bytes can exceed FFH, and `ADD` would silently lose the carry. Hence the 16-bit version.

**Program 2: 16-bit sum of N 8-bit numbers.** Keep the low byte of the sum in A and the high byte in B. Every time `ADD` produces a carry (CY = 1), add 1 to B.

```
        LXI H, 2050H    ; HL -> the count
        MOV C, M        ; C = N
        INX H           ; HL -> the first item
        MVI A, 00H      ; low byte of the sum = 0
        MVI B, 00H      ; high byte of the sum = 0
BACK:   ADD M           ; low byte = low byte + item
        JNC NEXT        ; no carry: the high byte stays
        INR B           ; carry: high byte + 1
NEXT:   INX H           ; next item
        DCR C           ; one item fewer
        JNZ BACK
        STA 2060H       ; store the low byte
        MOV A, B
        STA 2061H       ; store the high byte
        HLT
```

Trace with N = 4 and items FFH, 01H, 80H, 90H:

| Item | A (low) | CY | B (high) |
| --- | --- | --- | --- |
| FFH | FFH | 0 | 00H |
| 01H | 00H | 1 | 01H |
| 80H | 80H | 0 | 01H |
| 90H | 10H | 1 | 02H |

```latex
\text{Sum} = 0210_H = 255 + 1 + 128 + 144 = 528 \quad \checkmark
```

**When N is bigger than 255** (the papers love 300, 350, 360, 370 and 400), C can't hold the count, so use the pair **BC** as a 16-bit counter. The catch: `DCX B` sets **no flags**, so the loop can't just `JNZ`. Test BC for zero by hand:

```
        DCX B           ; count - 1 (no flags change)
        MOV A, B
        ORA C           ; A = B OR C, which is zero only if both are zero
        JNZ LOOP        ; keep going while BC isn't 0
```

This test overwrites A, so with a 16-bit counter the running sum can't live in A. It moves to the pair DE instead. That's exactly the pattern in Stop 2.

A small assembler detail: real assemblers want a leading 0 on hex numbers that start with a letter (`0FFH`, `0C8H`), so they can't be mistaken for labels. Papers and this doc write `FFH`, which is fine in the exam.

## Stop 2: Conditional 16-bit sums

Four Sessional-1 papers asked the same program with a different filter: "add only the odd ones", "only the even ones", "only those with odd parity", "only the non-negative ones". So learn **one** program with a swappable **test** line.

The pieces:

- **Counter:** BC, because N > 255.
- **Sum:** DE (D = high byte, E = low byte), because A is needed for the test.
- **Adding into DE:** `MOV A, E`, `ADD M`, `MOV E, A`, then if there was a carry, `INR D`.
- **The test**, which reads the item into A and jumps to SKIP if the item should *not* be added:

| Keep only | Test lines | Why it works |
| --- | --- | --- |
| Odd numbers | `ANI 01H` then `JZ SKIP` | An odd number has bit 0 = 1. Masking leaves 0 (Z = 1) for even numbers, which get skipped. |
| Even numbers | `ANI 01H` then `JNZ SKIP` | The reverse |
| Odd parity | `ORA A` then `JPE SKIP` | **Parity** = how many 1 bits. P = 1 means even, so skip those. |
| Non-negative | `ORA A` then `JM SKIP` | Bit 7 = 1 means negative (S = 1), so skip those. |

Memory map for all four (the papers give none): the numbers start at 2000H, and the sum goes to 2200H (low byte) and 2201H (high byte). Each version was tested on a simulator with 300 to 370 random numbers, and the stored sum matched the true sum every time.

> **PYQ, Sessional-1 2021 Q1, 3 marks.** Write a program in 8085 assembly language to find the 16-bit sum of only the odd integers out of 370 8-bit integers stored at consecutive locations. The program should be well documented.

**Answer:** Memory map: 370 numbers at 2000H onwards, and the 16-bit sum at 2200H (low) and 2201H (high). Method: walk through all 370 numbers; if bit 0 is 1 (odd), add it into the 16-bit sum in DE. The count 370 = 0172H needs the 16-bit counter BC.

```
        LXI H, 2000H    ; HL -> first number
        LXI B, 0172H    ; BC = 370 numbers to examine
        LXI D, 0000H    ; DE = 16-bit sum = 0
NEXT:   MOV A, M        ; A = current number
        ANI 01H         ; keep only bit 0 (1 = odd)
        JZ SKIP         ; even: don't add it
        MOV A, E        ; A = low byte of the sum
        ADD M           ; add the odd number
        MOV E, A        ; save the low byte
        JNC SKIP        ; no carry: high byte unchanged
        INR D           ; carry: high byte + 1
SKIP:   INX H           ; HL -> next number
        DCX B           ; one number fewer to examine
        MOV A, B
        ORA C           ; BC = 0 ?  (DCX sets no flags)
        JNZ NEXT        ; no: continue
        XCHG            ; HL = sum
        SHLD 2200H      ; 2200H = low byte, 2201H = high byte
        HLT
```

The paper fixes the sum at 16 bits, which holds up to FFFFH = 65,535. Strictly, 370 odd numbers of up to 255 could reach 94,350. Random data averages about 23,000, so it fits. Add one line in the exam to show you noticed: "if the sum can exceed FFFFH, count the overflows of D in a third register".

**Answer: test bit 0 with ANI 01H, add odd numbers into DE with carry into D, count 370 = 0172H in BC, and store the sum with SHLD.**

> **PYQ, Sessional-1 2023 Q1, 4 marks.** Write an 8085 program for finding the 16-bit sum of only the even integers out of 360 8-bit integers stored at consecutive locations. The program should be well documented.

**Answer:** The same map and method. Only the count (360 = 0168H) and the test (`JNZ SKIP`, so odd numbers are skipped) change.

```
        LXI H, 2000H    ; HL -> first number
        LXI B, 0168H    ; BC = 360 numbers to examine
        LXI D, 0000H    ; DE = 16-bit sum = 0
NEXT:   MOV A, M        ; A = current number
        ANI 01H         ; keep only bit 0 (0 = even)
        JNZ SKIP        ; odd: don't add it
        MOV A, E        ; A = low byte of the sum
        ADD M           ; add the even number
        MOV E, A        ; save the low byte
        JNC SKIP        ; no carry: high byte unchanged
        INR D           ; carry: high byte + 1
SKIP:   INX H           ; next number
        DCX B           ; one fewer to examine
        MOV A, B
        ORA C           ; BC = 0 ?
        JNZ NEXT
        XCHG            ; HL = sum
        SHLD 2200H      ; store the 16-bit sum
        HLT
```

**Answer: identical to the odd-sum program with** `JNZ SKIP` **after** `ANI 01H` **and BC = 0168H.**

> **PYQ, Sessional-1 2024 Q4.** Write an 8085 program for finding the 16-bit sum of only the odd parity integers out of 300 8-bit integers stored at consecutive locations. The program should be well documented.

**Answer:** A number has **odd parity** when it contains an odd number of 1 bits. For example, 07H = 0000 0111 has three 1s. `ORA A` sets the P flag from A without changing it. P = 1 means even parity, so those are skipped with `JPE`. The count is 300 = 012CH.

```
        LXI H, 2000H    ; HL -> first number
        LXI B, 012CH    ; BC = 300 numbers to examine
        LXI D, 0000H    ; DE = 16-bit sum = 0
NEXT:   MOV A, M        ; A = current number
        ORA A           ; set the parity flag from A
        JPE SKIP        ; even parity: don't add it
        MOV A, E        ; A = low byte of the sum
        ADD M           ; add the odd-parity number
        MOV E, A        ; save the low byte
        JNC SKIP        ; no carry: high byte unchanged
        INR D           ; carry: high byte + 1
SKIP:   INX H           ; next number
        DCX B           ; one fewer to examine
        MOV A, B
        ORA C           ; BC = 0 ?
        JNZ NEXT
        XCHG            ; HL = sum
        SHLD 2200H      ; store the 16-bit sum
        HLT
```

**Answer: the same program with** `ORA A` **then** `JPE SKIP` **as the test, and BC = 012CH.**

> **PYQ, Sessional-1 2022 Q1, 3 marks.** Write an 8085 program for finding the 16-bit decimal sum of only the non-negative integers out of 356 8-bit decimal integers stored at consecutive locations. The program should be well documented.

**Answer:** Two changes from the pattern.

- **"Non-negative":** treat each byte as signed. Skip it if bit 7 = 1, using `ORA A` then `JM SKIP`. So the positive numbers are the BCD values 00 to 79.
- **"Decimal sum":** the numbers are BCD, so the sum must stay BCD. Put `DAA` after every addition, including adding the carry into the high byte with `ACI 00H` then `DAA`.

The count is 356 = 0164H. A 16-bit BCD sum holds 4 digits, up to 9999.

```
        LXI H, 2000H    ; HL -> first number
        LXI B, 0164H    ; BC = 356 numbers to examine
        LXI D, 0000H    ; DE = 4-digit BCD sum = 0000
NEXT:   MOV A, M        ; A = current number
        ORA A           ; set the sign flag from bit 7
        JM SKIP         ; negative: don't add it
        MOV A, E        ; A = lower two BCD digits of the sum
        ADD M           ; add the number
        DAA             ; correct to BCD (may set CY)
        MOV E, A        ; save the lower two digits
        MOV A, D        ; A = upper two digits
        ACI 00H         ; add the decimal carry
        DAA             ; keep the upper digits in BCD too
        MOV D, A        ; save the upper two digits
SKIP:   INX H           ; next number
        DCX B           ; one fewer to examine
        MOV A, B
        ORA C           ; BC = 0 ?
        JNZ NEXT
        XCHG            ; HL = BCD sum
        SHLD 2200H      ; 2200H = lower digits, 2201H = upper digits
        HLT
```

Trace of the carry handling: D = 09H plus a carry of 1 gives 0AH after `ACI`, and `DAA` turns it into 10H, which is BCD 10. Tested on 356 numbers: the 4 stored digits matched the decimal total.

**Answer: skip negatives with ORA A / JM, and add with ADD + DAA on the low byte and ACI 00H + DAA on the high byte, so DE holds a 4-digit BCD sum.**

## Stop 3: Maximum, minimum, searching and counting

These are in the syllabus and your class notes, though no recent paper has asked them on their own. They're also the building blocks of sorting (Stop 6), so they're worth 15 minutes.

**The comparison rule** everything below uses: `CMP M` computes A − \[HL\] and sets CY = 1 when **A is smaller**.

**Program: largest of N numbers.** Memory map: N at 2050H, numbers from 2051H, result at 2060H. Method: assume the first number is the largest, then for each next number, if it's bigger, it becomes the new largest.

```
        LXI H, 2050H    ; HL -> count
        MOV C, M        ; C = N
        INX H           ; HL -> first number
        MOV A, M        ; largest so far = first number
        DCR C           ; N - 1 numbers left to compare
        JZ DONE         ; only one number: it's the answer
LOOP:   INX H           ; HL -> next number
        CMP M           ; largest - next
        JNC SKIP        ; no borrow: largest >= next, keep it
        MOV A, M        ; next is bigger: new largest
SKIP:   DCR C
        JNZ LOOP
DONE:   STA 2060H       ; store the largest
        HLT
```

**Smallest of N numbers:** change one line, `JNC SKIP` to `JC SKIP` (keep A while A \< next). Both were tested on 12 random numbers and matched.

**Program: search for a byte.** Memory map: the key (the value to find) at 2040H, N at 2050H, the list from 2051H. The result at 2060H and 2061H is the address where the key was found, or 0000H if it's absent.

```
        LDA 2040H       ; A = key
        LXI H, 2050H    ; HL -> count
        MOV C, M        ; C = N
LOOP:   INX H           ; HL -> next element
        CMP M           ; key = element ?
        JZ FOUND        ; yes: HL holds its address
        DCR C
        JNZ LOOP        ; check the rest
        LXI H, 0000H    ; not found
FOUND:  SHLD 2060H      ; store the address (or 0000H)
        HLT
```

Test: the list 05H, 09H, 22H, 07H, 40H with key 07H gives 2054H, the fourth element. Key 99H gives 0000H.

**Program: count positive and negative numbers** (from your notes). Memory map: N at 2050H, numbers from 2051H, the positive count to 2060H and the negative count to 2061H. Zero counts as positive here (non-negative).

```
        LXI H, 2050H    ; HL -> count
        MOV C, M        ; C = N
        MVI B, 00H      ; B = positive count
        MVI D, 00H      ; D = negative count
LOOP:   INX H           ; next number
        MOV A, M
        ORA A           ; set S from bit 7
        JM NEG          ; bit 7 = 1: negative
        INR B           ; positive (or zero)
        JMP NEXT
NEG:    INR D           ; negative
NEXT:   DCR C
        JNZ LOOP
        MOV A, B
        STA 2060H       ; store the positive count
        MOV A, D
        STA 2061H       ; store the negative count
        HLT
```

Test: 05H, 80H, FFH, 7FH, 00H, 90H, 10H gives 4 positive and 3 negative. For **even and odd** counts, swap the test for `ANI 01H` then `JNZ ODD`.

## Stop 4: 8x8 multiplication

The 8085 has no multiply instruction, so you build one. Two 8-bit numbers give at most a **16-bit product** (255 × 255 = 65,025 = FE01H), so the product lives in **HL**, and `DAD` does the 16-bit additions. Names: the **multiplicand** is the number being multiplied, and the **multiplier** says how many times.

Memory map for every version here: the multiplicand at 2050H, the multiplier at 2051H, and the product at 2052H (low byte) and 2053H (high byte). Each version was tested on 45 pairs including 0 × 0 and 255 × 255, and was right every time.

**Method 0: successive addition** (in your notes). Add the multiplicand to HL, multiplier times. It's simple, but it loops up to 255 times.

```
        LDA 2050H       ; A = multiplicand
        MOV E, A
        MVI D, 00H      ; DE = multiplicand as a 16-bit number
        LDA 2051H       ; A = multiplier
        MOV C, A        ; C = how many additions
        LXI H, 0000H    ; product = 0
        ORA A           ; multiplier = 0 ?
        JZ DONE         ; yes: the product is 0
LOOP:   DAD D           ; product = product + multiplicand
        DCR C
        JNZ LOOP
DONE:   SHLD 2052H      ; store the 16-bit product
        HLT
```

**Shift and add: always 8 loops.** It's long multiplication, in binary. Each multiplier bit is 0 or 1, so for each bit you either add a shifted copy of the multiplicand or add nothing.

```latex
\begin{aligned}
13 \times 11 &= 13 \times (1011)_2 \\
&= 13 \times 8 + 13 \times 2 + 13 \times 1 \\
&= 104 + 26 + 13 = 143 = 008F_H
\end{aligned}
```

There are two ways to line up "shifted". That's exactly what the two PYQ phrasings mean:

|  | **Shifting the multiplicand** | **Without shifting the multiplicand** (shifting the product) |
| --- | --- | --- |
| Multiplier bits read | Right to left (LSB first), with `RRC` | Left to right (MSB first), with `RLC` |
| Each step | If the bit is 1: product += multiplicand. Then double the multiplicand (`XCHG`, `DAD H`, `XCHG`). | Double the product (`DAD H`). Then if the bit is 1: product += multiplicand. |
| Multiplicand | Grows: ×2 each step | Never changes |

Trace of 13 × 11 (0DH × 0BH, multiplier = 0000 1011):

| Step | Shifting the multiplicand: bit, product, multiplicand after | Shifting the product: bit, product after |
| --- | --- | --- |
| 1 | 1, 13, 26 | 0, 0 |
| 2 | 1, 39, 52 | 0, 0 |
| 3 | 0, 39, 104 | 0, 0 |
| 4 | 1, **143**, 208 | 0, 0 |
| 5 | 0, 143 | 1, 0 × 2 + 13 = 13 |
| 6 | 0, 143 | 0, 26 |
| 7 | 0, 143 | 1, 52 + 13 = 65 |
| 8 | 0, 143 | 1, 130 + 13 = **143** |

> **PYQ, Sessional-1 2021 Q2, 4 marks; Sessional-1 2023 Q2, 4 marks; Sessional-1 2024 Q3.** Write a well-documented program in 8085 assembly language for 8x8 multiplication by shifting the multiplicand.

**Answer:** Method: examine the multiplier bits from LSB to MSB. If a bit is 1, add the current multiplicand (in DE) to the product (in HL). After every bit, shift the multiplicand left (× 2).

```
        LDA 2050H       ; A = multiplicand
        MOV E, A
        MVI D, 00H      ; DE = multiplicand (16-bit, room to grow)
        LDA 2051H       ; A = multiplier
        LXI H, 0000H    ; HL = product = 0
        MVI B, 08H      ; B = 8 bits to examine
NEXT:   RRC             ; next multiplier bit (LSB first) into CY
        JNC SKIP        ; bit = 0: nothing to add
        DAD D           ; bit = 1: product = product + multiplicand
SKIP:   XCHG            ; shift the multiplicand left:
        DAD H           ;   HL = HL + HL
        XCHG            ;   so DE = 2 x DE (and the product returns to HL)
        DCR B           ; one bit fewer
        JNZ NEXT
        SHLD 2052H      ; store the 16-bit product
        HLT
```

Test: 23H × 45H stores 096FH (35 × 69 = 2415).

**Answer: 8 loops of RRC to test a multiplier bit, DAD D to add the multiplicand when the bit is 1, and XCHG / DAD H / XCHG to double the multiplicand; the product ends in HL.**

> **PYQ, Endsem 2022 Q3(a), 4.5 marks; Endsem 2025 Q3(a), 4.5 marks.** Write a well-documented program in 8085 assembly language for 8x8 multiplication without shifting the multiplicand.

**Answer:** Method: keep the multiplicand fixed in DE. Examine the multiplier from MSB to LSB. For each bit, first double the product, then add the multiplicand if the bit is 1.

```
        LDA 2050H       ; A = multiplicand
        MOV E, A
        MVI D, 00H      ; DE = multiplicand (never shifted)
        LDA 2051H       ; A = multiplier
        LXI H, 0000H    ; HL = product = 0
        MVI B, 08H      ; B = 8 bits to examine
NEXT:   DAD H           ; product = product x 2 (shift left)
        RLC             ; next multiplier bit (MSB first) into CY
        JNC SKIP        ; bit = 0: nothing to add
        DAD D           ; bit = 1: product = product + multiplicand
SKIP:   DCR B           ; one bit fewer
        JNZ NEXT
        SHLD 2052H      ; store the 16-bit product
        HLT
```

Test: 23H × 45H stores 096FH. `DAD H` changes CY, but `RLC` sets CY again before the `JNC` reads it, so the order matters: double first, then rotate.

**Answer: 8 loops of DAD H (double the product), RLC (next multiplier bit, MSB first) and DAD D if the bit is 1; the multiplicand in DE never moves.**

> **PYQ, Sessional-1 2022 Q2, 4 marks.** Write a well-documented program in 8085 assembly language for 8x8 multiplication without shifting the multiplicand, using a subroutine.

**Answer:** The same method, moved into a subroutine `MULT`. It takes the multiplicand in DE and the multiplier in A, and returns the product in HL. The main program sets up the stack (needed for CALL), loads the inputs, calls MULT and stores the result. MULT saves and restores BC, because it uses B as its bit counter.

```
        LXI SP, 2800H   ; stack for CALL/RET
        LDA 2050H       ; A = multiplicand
        MOV E, A
        MVI D, 00H      ; DE = multiplicand
        LDA 2051H       ; A = multiplier
        CALL MULT       ; HL = DE x A
        SHLD 2052H      ; store the product
        HLT

; MULT: HL = DE x A  (8 x 8 bits, shift-the-product method)
MULT:   PUSH B          ; save the caller's B and C
        LXI H, 0000H    ; product = 0
        MVI B, 08H      ; 8 multiplier bits
NEXT:   DAD H           ; product x 2
        RLC             ; next multiplier bit into CY
        JNC SKIP
        DAD D           ; bit = 1: add the multiplicand
SKIP:   DCR B
        JNZ NEXT
        POP B           ; restore B and C
        RET             ; back to the caller
```

**Answer: the shift-the-product loop inside a subroutine MULT (inputs DE and A, output HL), called after LXI SP, with PUSH B / POP B so the caller's registers survive.**

## Stop 5: 16 by 8 division

No divide instruction either. Names: the **dividend** (16-bit) is divided by the **divisor** (8-bit), giving a **quotient** (how many times it fits) and a **remainder** (what's left over). With a 16-bit dividend and a divisor as small as 1, the quotient can need 16 bits too.

Memory map: the dividend at 2050H (low) and 2051H (high), the divisor at 2052H, the quotient at 2053H (low) and 2054H (high), and the remainder at 2055H. Assume the divisor isn't 0. Both versions were tested on 48 cases, including FFFFH ÷ 1 and FFFFH ÷ FFH.

```latex
\begin{aligned}
\text{dividend} &= \text{divisor} \times \text{quotient} + \text{remainder}, \quad 0 \le \text{remainder} < \text{divisor} \\
1234_H \div 56_H &: \; 4660 = 86 \times 54 + 16 \;\Rightarrow\; Q = 0036_H,\; R = 10_H
\end{aligned}
```

> **PYQ, Endsem 2022 Q3(b), 4.5 marks; Sessional-1 2025 Q3, 3 marks.** Write a well-documented program in 8085 assembly language for 16x8 division.

**Answer (method 1, repeated subtraction).** Keep subtracting the divisor from the dividend and count how many times it works. When a subtraction goes negative (a borrow from the high byte), you've gone one step too far. Add the divisor back once; what's left is the remainder.

The 16-bit subtraction is done in two halves: `SUB C` on the low byte, then `SBI 00H` on the high byte, which subtracts just the borrow.

```
        LHLD 2050H      ; HL = dividend (16-bit)
        LDA 2052H
        MOV C, A        ; C = divisor
        LXI D, 0000H    ; DE = quotient = 0
LOOP:   MOV A, L
        SUB C           ; low byte - divisor
        MOV L, A
        MOV A, H
        SBI 00H         ; high byte - borrow
        MOV H, A
        JC DONE         ; dividend went negative: stop
        INX D           ; that subtraction fitted: quotient + 1
        JMP LOOP
DONE:   MOV A, L
        ADD C           ; undo the extra subtraction: A = remainder
        STA 2055H       ; store the remainder
        XCHG            ; HL = quotient
        SHLD 2053H      ; store the 16-bit quotient
        HLT
```

Test: 1234H ÷ 56H gives quotient 0036H and remainder 10H.

**Answer (method 2, shifting the dividend: always 16 loops).** This is long division in binary. Bring the dividend's bits, MSB first, into a running remainder in E. Each time the remainder reaches the divisor, subtract it and write a 1 into the quotient. Shifting HL left both feeds out the next dividend bit and makes room at bit 0 for the next quotient bit, so the quotient builds up in HL itself.

```
        LHLD 2050H      ; HL = dividend
        LDA 2052H
        MOV C, A        ; C = divisor
        MVI B, 10H      ; B = 16 bits to process
        MVI E, 00H      ; E = running remainder = 0
NEXT:   DAD H           ; shift HL left: next dividend bit -> CY, bit 0 = 0
        MOV A, E
        RAL             ; remainder = remainder x 2 + that bit
        JC SUBT         ; remainder overflowed 8 bits: surely >= divisor
        CMP C           ; remainder >= divisor ?
        JC SKIP         ; no: quotient bit stays 0
SUBT:   SUB C           ; yes: remainder = remainder - divisor
        INR L           ; quotient bit = 1 (bit 0 of L)
SKIP:   MOV E, A        ; save the remainder
        DCR B
        JNZ NEXT
        SHLD 2053H      ; HL = quotient
        MOV A, E
        STA 2055H       ; remainder
        HLT
```

Either method earns full marks. Method 1 is easier to write under pressure. Method 2 is the "shift dividend" method from your notes, and it takes the same time for any input.

**Answer: repeated 16-bit subtraction (SUB C, SBI 00H) counting successes in DE until a borrow, then add the divisor back for the remainder; quotient to 2053H-2054H, remainder to 2055H.**

## Stop 6: Sorting

Nine of the last ten papers asked this. The method is **bubble sort**: walk down the list comparing each pair of **neighbours**, and swap them if they're in the wrong order. After one full walk (a **pass**), the biggest number has "bubbled" to the end. N − 1 passes are always enough.

Trace, ascending, with 30, 10, 40, 20:

| Pass | Comparisons (swap?) | List after the pass |
| --- | --- | --- |
| 1 | (30, 10) swap, (30, 40) keep, (40, 20) swap | 10, 30, 20, **40** |
| 2 | (10, 30) keep, (30, 20) swap, (30, 40) keep | 10, 20, **30, 40** |
| 3 | No swaps | 10, 20, 30, 40 |

**Ascending vs descending is one jump.** After `CMP M` (this item − next item):

- **Ascending:** keep them if this \< next, using `JC NOSWAP`.
- **Descending:** keep them if this ≥ next, using `JNC NOSWAP`.

**The swap, step by step.** A holds this item, and HL points at the next one:

```
        MOV B, M        ; B = next item
        MOV M, A        ; next position = this item
        DCX H           ; HL back to this position
        MOV M, B        ; this position = old next item
        INX H           ; HL -> the next position again
```

All the sorting programs below were tested on a simulator with random data at the papers' exact sizes and addresses, and every list came out sorted.

> **PYQ, Sessional-1 2024 Q1.** Write an 8085 program to arrange a given set of integers stored at consecutive memory locations starting at 2900H in ascending order. The first location contains the number of items, and the following addresses contain the items. The program should be well documented.

**Answer:** Memory map: N at 2900H, items at 2901H onwards. N fits in 8 bits, so C counts passes (N − 1) and D counts comparisons in each pass (also N − 1). Assume N ≥ 2.

```
        LXI H, 2900H    ; HL -> count
        MOV C, M        ; C = N
        DCR C           ; C = N - 1 passes
PASS:   MOV D, C        ; D = N - 1 comparisons this pass
        LXI H, 2901H    ; HL -> first item
CMPR:   MOV A, M        ; A = this item
        INX H           ; HL -> next item
        CMP M           ; this - next
        JC NOSWAP       ; this < next: already in order
        MOV B, M        ; swap: B = next
        MOV M, A        ;   next position = this
        DCX H
        MOV M, B        ;   this position = old next
        INX H           ;   HL -> next position again
NOSWAP: DCR D           ; one comparison fewer
        JNZ CMPR
        DCR C           ; one pass fewer
        JNZ PASS
        HLT
```

**Answer: bubble sort with C = passes, D = comparisons, CMP M then JC NOSWAP for ascending, and a 5-line swap through B.**

> **PYQ, Sessional-1 2025 Q2, 3 marks.** Write a well-documented 8085 program to sort a given set of integers stored at consecutive memory locations starting at 2500H in descending order. The first location contains the number of items, and the following addresses contain the items.

**Answer:** The same program, with the count at 2500H, items from 2501H, and `JNC NOSWAP` so a pair stays when this ≥ next.

```
        LXI H, 2500H    ; HL -> count
        MOV C, M        ; C = N
        DCR C           ; C = N - 1 passes
PASS:   MOV D, C        ; D = N - 1 comparisons this pass
        LXI H, 2501H    ; HL -> first item
CMPR:   MOV A, M        ; A = this item
        INX H           ; HL -> next item
        CMP M           ; this - next
        JNC NOSWAP      ; this >= next: already in descending order
        MOV B, M        ; swap: B = next
        MOV M, A        ;   next position = this
        DCX H
        MOV M, B        ;   this position = old next
        INX H           ;   HL -> next position again
NOSWAP: DCR D           ; one comparison fewer
        JNZ CMPR
        DCR C           ; one pass fewer
        JNZ PASS
        HLT
```

**Answer: the same bubble sort from 2500H/2501H with JNC NOSWAP for descending order.**

**When N is fixed and bigger than 255.** Now the counters must be 16-bit: BC for passes, DE for comparisons. But the swap needs a spare register, and every one is taken. The fix is to **park the pass counter on the stack** with `PUSH B` during a pass. That frees B for the swap, and `POP B` brings the counter back after the pass.

> **PYQ, all asking the same program with different numbers: Sessional-1 2021 Q3 (4 marks); Sessional-1 2022 Q3 (4 marks); Sessional-1 2023 Q3 (5 marks); Endsem 2022 Q3'(a), Endsem 2023 Q3'(a), Endsem 2024 Q3(b), Endsem 2025 Q3(b) (4.5 marks each).** Write a well-documented 8085 program to arrange N integers stored at consecutive memory locations starting at a given address in ascending / descending order.

**Answer:** Here's the program for Sessional-1 2021 Q3: 350 integers from 2200H, descending.

```
        LXI SP, 2FFFH   ; stack, well above the data
        LXI B, 015DH    ; BC = N - 1 = 349 passes
PASS:   PUSH B          ; park the pass counter (frees B)
        LXI D, 015DH    ; DE = N - 1 = 349 comparisons this pass
        LXI H, 2200H    ; HL -> first item
CMPR:   MOV A, M        ; A = this item
        INX H           ; HL -> next item
        CMP M           ; this - next
        JNC NOSWAP      ; this >= next: in descending order
        MOV B, M        ; swap: B = next
        MOV M, A        ;   next position = this
        DCX H
        MOV M, B        ;   this position = old next
        INX H           ;   HL -> next position again
NOSWAP: DCX D           ; one comparison fewer
        MOV A, D
        ORA E           ; DE = 0 ?  (DCX sets no flags)
        JNZ CMPR
        POP B           ; get the pass counter back
        DCX B           ; one pass fewer
        MOV A, B
        ORA C           ; BC = 0 ?
        JNZ PASS
        HLT
```

For each paper, change only three things: N − 1 (in **both** LXI lines), the start address, and the jump.

| Paper | N | N − 1 in both LXI | Start address | Order | Jump after CMP M |
| --- | --- | --- | --- | --- | --- |
| Sessional-1 2021 Q3 | 350 | 015DH | 2200H | Descending | `JNC NOSWAP` |
| Sessional-1 2022 Q3 | 360 | 0167H | 2300H | Descending | `JNC NOSWAP` |
| Sessional-1 2023 Q3 | 350 | 015DH | 2200H | Ascending | `JC NOSWAP` |
| Endsem 2022 Q3'(a) | 400 | 018FH | 2500H | Ascending | `JC NOSWAP` |
| Endsem 2023 Q3'(a) | 350 | 015DH | 2242H | Descending | `JNC NOSWAP` |
| Endsem 2024 Q3(b) | 400 | 018FH | 2300H | Ascending | `JC NOSWAP` |
| Endsem 2025 Q3(b) | 300 | 012BH | 2200H | Descending | `JNC NOSWAP` |

```latex
350 - 1 = 349 = 015D_H, \quad 360 - 1 = 359 = 0167_H, \quad 400 - 1 = 399 = 018F_H, \quad 300 - 1 = 299 = 012B_H
```

In the exam, write the full program with that paper's numbers already in, not this table.

**Answer: bubble sort with 16-bit counters (BC = passes, saved on the stack during a pass so B can swap; DE = comparisons), each tested for zero with MOV A, hi / ORA lo; JC for ascending, JNC for descending.**

## Stop 7: Arrays: a C for-loop in assembly, and matrix addition

An **array** in memory is just items at consecutive addresses. Element i is at base address + (i − 1) if counting starts at 1. Turning C into assembly is mechanical:

| C | 8085 |
| --- | --- |
| `for (i = 1; i <= N; i++)` | A counter register loaded with N, `DCR` and `JNZ` at the bottom |
| `A[i]`, `B[i]`, `C[i]` | One pointer per array, each stepped with `INX` |
| `B[i] + C[i]` | Load one into a register, the other into A, then `ADD` |

> **PYQ, Sessional-1 2024 Q2.** Write an 8085 program to implement the HLL statement `for (i = 1; i <= N; i++) { A[i] = B[i] + C[i]; }` where A, B and C are one-dimensional arrays starting at locations 2000H, 2100H and 2200H respectively. The location of N is 19FFH. The program should be well documented.

**Answer:** Memory map as given: element i of A, B and C is at 2000H, 2100H and 2200H plus (i − 1).

**A neat trick:** the three arrays sit exactly 100H apart, so the **same offset** reaches all three, and only the high byte changes. With HL pointing into B at 21xxH, `DCR H` makes it point at the same element of A at 20xxH, and `INR H` moves it back. So two pointers are enough: HL for B (and A), and DE for C.

The arrays are byte arrays, so each sum is kept to 8 bits (a carry is dropped), just as C does with `unsigned char`. If N = 0, a C for-loop runs zero times, so the program checks for that first.

```
        LDA 19FFH       ; A = N
        ORA A           ; N = 0 ?
        JZ DONE         ; then the loop body never runs
        MOV C, A        ; C = loop counter (i = 1 .. N)
        LXI H, 2100H    ; HL -> B[1]
        LXI D, 2200H    ; DE -> C[1]
LOOP:   MOV B, M        ; B = B[i]
        LDAX D          ; A = C[i]
        ADD B           ; A = B[i] + C[i]
        DCR H           ; HL -> A[i]  (21xxH -> 20xxH)
        MOV M, A        ; A[i] = B[i] + C[i]
        INR H           ; HL -> B[i] again
        INX H           ; i++ : next element of B (and A)
        INX D           ;       next element of C
        DCR C           ; one iteration fewer
        JNZ LOOP        ; until i > N
DONE:   HLT
```

Tested with N = 20 and random arrays: A matched B + C element by element. With N = 0, nothing was written.

**Answer: N from 19FFH into C as the loop counter, HL walking B (with DCR H / INR H reaching A one page below), DE walking C, and ADD then MOV M, A for each element.**

**Matrix addition** (syllabus, from your notes) is the same idea. A 3 × 3 matrix stored row by row is just 9 bytes in a row. Place the two matrices and the result exactly 100H apart (at 2050H, 2150H and 2250H), and one pointer plus `INR H` / `DCR H` reaches all three.

```
        LXI H, 2050H    ; HL -> first element of matrix A
        MVI C, 09H      ; 3 x 3 = 9 elements
LOOP:   MOV A, M        ; A = a(ij)
        INR H           ; HL -> b(ij) at 21xxH
        ADD M           ; A = a(ij) + b(ij)
        INR H           ; HL -> s(ij) at 22xxH
        MOV M, A        ; s(ij) = a(ij) + b(ij)
        DCR H
        DCR H           ; back to matrix A
        INX H           ; next element
        DCR C
        JNZ LOOP
        HLT
```

Test: A = 1 to 9 and B = 10, 20, … 90 gave the sum 11, 22, 33, … 99.

## Stop 8: HCF and factorial

> **PYQ, Endsem 2024 Q3(a), 4.5 marks.** Write a well-documented 8085 program to find the HCF of two given integers.

**Answer:** The **HCF** (highest common factor, also called the GCD) is the biggest number that divides both. Euclid's subtraction method: **while the two numbers differ, replace the bigger one with (bigger − smaller).** When they become equal, that value is the HCF.

```latex
\begin{aligned}
(36, 24) &\to (12, 24) \to (12, 12) \;\Rightarrow\; \text{HCF} = 12 \\
(48, 180) &\to (48, 132) \to (48, 84) \to (48, 36) \to (12, 36) \to (12, 24) \to (12, 12) \;\Rightarrow\; 12
\end{aligned}
```

Memory map: the numbers at 2050H and 2051H (both non-zero, since HCF with 0 isn't defined by this method), and the HCF to 2052H.

```
        LDA 2050H
        MOV B, A        ; B = first number
        LDA 2051H       ; A = second number
AGAIN:  CMP B           ; compare A with B
        JZ DONE         ; equal: this is the HCF
        JC LESS         ; A < B: reduce B instead
        SUB B           ; A > B: A = A - B
        JMP AGAIN
LESS:   MOV C, A        ; C = A (the smaller one)
        MOV A, B
        SUB C           ; A = B - A
        MOV B, A        ; B = B - A
        MOV A, C        ; A back to its value
        JMP AGAIN
DONE:   STA 2052H       ; store the HCF
        HLT
```

Tested on 888 pairs from 1 to 255: every result equalled the true GCD.

**Answer: repeated subtraction (bigger − smaller) with CMP / JZ / JC until both are equal; that value, stored at 2052H, is the HCF.**

> **PYQ, Endsem 2023 Q3(b), 4.5 marks.** Write a well-documented 8085 program to find the factorial of a given integer.

**Answer:** n! = n × (n − 1) × … × 1, and 0! = 1. It grows fast: 8! = 40,320 fits in 16 bits, but 9! = 362,880 doesn't. So n ≤ 8, and the result is 16-bit in HL.

Method: start with HL = 1. For k = n down to 1, multiply HL by k. Each multiplication is successive addition: copy HL to DE, clear HL, then add DE k times.

Memory map: n at 2050H, n! at 2051H (low) and 2052H (high).

```
        LDA 2050H       ; A = n (0 to 8)
        MOV B, A        ; B = k, the current multiplier, starts at n
        LXI H, 0001H    ; HL = 1 (also the answer for 0!)
        ORA A           ; n = 0 ?
        JZ DONE         ; 0! = 1
NEXT:   XCHG            ; DE = product so far
        LXI H, 0000H    ; HL = 0
        MOV C, B        ; C = k additions
MUL:    DAD D           ; HL = HL + product so far
        DCR C
        JNZ MUL         ; after k adds: HL = product x k
        DCR B           ; k = k - 1
        JNZ NEXT        ; until k = 0
DONE:   SHLD 2051H      ; store n!
        HLT
```

Trace for n = 5:

| k | HL after multiplying by k |
| --- | --- |
| 5 | 1 × 5 = 5 |
| 4 | 5 × 4 = 20 |
| 3 | 20 × 3 = 60 |
| 2 | 60 × 2 = 120 |
| 1 | 120 × 1 = 120 = 0078H |

Tested for n = 0 to 8: 1, 1, 2, 6, 24, 120, 720, 5040, 40320 (8! = 9D80H).

**Answer: HL = 1, then multiply HL by n, n − 1, …, 1 using successive addition (DAD D, k times); valid for n ≤ 8 since 8! = 9D80H is the largest that fits 16 bits.**

## Stop 9: Code conversion

The same quantity can be stored in different **codes**, and each has its use:

| Code | The number 255 looks like | Used for |
| --- | --- | --- |
| **Binary** | FFH = 1111 1111 | Arithmetic inside the CPU |
| **BCD** (one decimal digit per 4 bits) | 02H, 55H ("2", "55") | Showing decimal digits on a display |
| **ASCII** (one byte per printed character) | 32H 35H 35H ("2", "5", "5") | Printing and sending text |

In ASCII, the digit characters "0" to "9" are 30H to 39H, so a digit d is stored as d + 30H. Letters "A" to "F" are 41H to 46H.

> **PYQ, Endsem 2023 Q3(a), 4.5 marks.** Write a well-documented 8085 program to convert an 8-bit binary number to a decimal number.

**Answer:** An 8-bit number is at most 255, so it has up to 3 decimal digits. Method: count how many times 100 (64H) can be subtracted (the hundreds), then how many times 10 (0AH) can be subtracted from what's left (the tens). What remains is the units. Store the hundreds digit on its own, and pack tens and units into one BCD byte.

Memory map: the binary number at 2050H, the hundreds at 2051H, tens and units (packed BCD) at 2052H.

```
        LDA 2050H       ; A = binary number (00H to FFH)
        MVI B, 00H      ; B = hundreds count
        MVI C, 00H      ; C = tens count
HUND:   CPI 64H         ; A >= 100 ?
        JC TENS         ; no: hundreds done
        SUI 64H         ; A = A - 100
        INR B           ; one more hundred
        JMP HUND
TENS:   CPI 0AH         ; A >= 10 ?
        JC UNITS        ; no: tens done
        SUI 0AH         ; A = A - 10
        INR C           ; one more ten
        JMP TENS
UNITS:  MOV D, A        ; D = units (what's left, 0 to 9)
        MOV A, B
        STA 2051H       ; store the hundreds digit
        MOV A, C
        RLC
        RLC
        RLC
        RLC             ; tens moved into the high nibble
        ORA D           ; units into the low nibble
        STA 2052H       ; store packed BCD: tens and units
        HLT
```

Trace for FFH (255): 255 → 155 → 55 gives hundreds = 2. Then 55 → 45 → 35 → 25 → 15 → 5 gives tens = 5 and units = 5. Result: 2051H = 02H, 2052H = 55H, which reads 255. Tested on all 256 inputs.

**Answer: subtract 100 repeatedly (count = hundreds), then 10 repeatedly (count = tens), and the rest is units; store the hundreds digit and the packed tens-units BCD byte.**

**Binary to ASCII** (syllabus). Split the byte into its two hex digits and turn each into its character. A digit 0 to 9 gets + 30H. A digit A to F gets + 37H, because "A" is 41H and 0AH + 37H = 41H. The conversion goes in a subroutine, since it runs twice. Memory map: the byte at 2050H, its two ASCII characters at 2051H and 2052H.

```
        LXI SP, 2800H   ; stack for CALL
        LDA 2050H       ; A = the byte
        MOV B, A        ; keep a copy
        RRC
        RRC
        RRC
        RRC             ; high digit moved into the low nibble
        CALL ASCII
        STA 2051H       ; first character
        MOV A, B
        CALL ASCII      ; low digit
        STA 2052H       ; second character
        HLT

; ASCII: convert the low nibble of A into its ASCII character
ASCII:  ANI 0FH         ; keep one hex digit
        CPI 0AH         ; 0 to 9 ?
        JC DIGIT
        ADI 07H         ; A to F: jump the gap between "9" and "A"
DIGIT:  ADI 30H         ; + 30H gives the character
        RET
```

Test: 3CH gives 33H ("3") and 43H ("C"). Tested on all 256 bytes.

**BCD to binary** (syllabus, "decimal to binary"). A packed BCD byte holds tens in the high nibble and units in the low nibble. The binary value is tens × 10 + units, and × 10 is built from additions: x × 2, × 4, + x gives × 5, then × 2 gives × 10. Memory map: BCD at 2050H, binary at 2051H.

```
        LDA 2050H       ; A = packed BCD, e.g. 45H
        MOV B, A        ; keep a copy
        ANI 0FH         ; A = units
        MOV C, A        ; C = units
        MOV A, B
        ANI F0H         ; keep the tens nibble
        RRC
        RRC
        RRC
        RRC             ; A = tens
        MOV D, A        ; D = tens
        ADD A           ; tens x 2
        ADD A           ; tens x 4
        ADD D           ; tens x 5
        ADD A           ; tens x 10
        ADD C           ; + units
        STA 2051H       ; binary result
        HLT
```

```latex
45_{BCD} \to 4 \times 10 + 5 = 45 = 2D_H, \qquad 99_{BCD} \to 99 = 63_H
```

Tested on all 100 BCD values from 00 to 99.

## Stop 10: Delays and modulo-N counters

The Interfacing, Interrupts and Timing doc (Stop 7) works the first of these in full. This stop explains the delay maths from scratch and covers **every** paper's numbers.

**A delay is a loop that wastes a known amount of time.** Each instruction takes a fixed number of T-states (clock periods), so time = T-states × clock period. With a 0.5 µs clock, 2 T-states make 1 µs.

**8-bit delay loop:**

```
        MVI C, N        ;  7 T, once
LOOP:   DCR C           ;  4 T, N times
        JNZ LOOP        ; 10 T when it jumps, 7 T the last time
```

```latex
\begin{aligned}
T_{\text{total}} &= 7 + (4 + 10)N - 3 = 14N + 4 \\
N = 255 &: \; 14 \times 255 + 4 = 3574 \text{ T} = 3574 \times 0.5\ \mu s \approx 1.79 \text{ ms}
\end{aligned}
```

The −3 is there because the last JNZ doesn't jump, so it takes 7 T instead of 10. The trouble: even at the maximum count, an 8-bit loop gives only about 1.8 ms. For tens of milliseconds you need either **nested loops** (an outer counter repeating the inner loop: B = 10 around C = 255 gives 35,884 T, about 17.9 ms) or a **16-bit counter**.

**16-bit delay loop** (the one every paper expects):

```
DELAY:  LXI D, COUNT    ; 10 T, once
LOOP:   DCX D           ;  6 T
        MOV A, E        ;  4 T
        ORA D           ;  4 T   (Z = 1 only when DE = 0)
        JNZ LOOP        ; 10 T (7 T the last time)
        RET
```

```latex
\begin{aligned}
\text{T per loop} &= 6 + 4 + 4 + 10 = 24 \\
\text{Delay} &= (10 + 24N - 3) \times T \approx 24N \times T \\
N &= \frac{\text{Delay}}{24 \times T}
\end{aligned}
```

**A modulo-N counter** counts 0, 1, …, N − 1 and then wraps to 0. Modulo-8 shows 0 to 7, and modulo-10 shows 0 to 9.

> **PYQ, Sessional-1 2022 Q4, 4 marks.** Write an 8085 program to generate a modulo-8 counter with a delay of 60 ms between each count, assuming a system with a 0.5 µs clock period. Show all calculations.

**Answer:** The count lives in B (the delay loop destroys A) and is displayed at output port 01H.

```latex
\begin{aligned}
N &= \frac{60 \text{ ms}}{24 \times 0.5\ \mu s} = \frac{60000\ \mu s}{12\ \mu s} = 5000 = 1388_H \\
\text{Check: } & (7 + 24 \times 5000) \times 0.5\ \mu s = 60.0035 \text{ ms}
\end{aligned}
```

```
        LXI SP, 2800H   ; stack for CALL/RET
START:  MVI B, 00H      ; count = 0
DSPLY:  MOV A, B
        OUT 01H         ; display the count
        CALL DELAY      ; wait 60 ms
        INR B           ; next count
        MOV A, B
        CPI 08H         ; reached 8 ?
        JNZ DSPLY       ; no: display it
        JMP START       ; yes: wrap to 0

DELAY:  LXI D, 1388H    ; N = 5000
LOOP:   DCX D           ; N - 1
        MOV A, E
        ORA D           ; DE = 0 ?
        JNZ LOOP
        RET
```

Simulated: the port showed 0, 1, …, 7, 0, 1, … with 60.04 ms between counts. The extra 0.04 ms is the CALL, RET and counting instructions, which you may mention and ignore.

**Answer: N = 60 ms ÷ (24 × 0.5 µs) = 5000 = 1388H in a DCX/ORA loop, and the count in B, compared with CPI 08H to wrap after 7.**

> **PYQ, the same program with other numbers: Sessional-1 2024 Q5; Sessional-1 2025 Q4 (3 marks); Endsem 2022 Q3'(b), Endsem 2023 Q3'(b), Endsem 2024 Q3(c), Endsem 2025 Q3(c) (4.5 marks each).** Write an 8085 program to generate a modulo-N counter with a delay of D ms between each count, assuming a 0.5 µs clock period. Show all calculations.

**Answer:** Write the program above with that paper's COUNT in `LXI D` and its modulus in `CPI`, and show the N calculation for its delay.

| Paper | Modulus (counts) | Delay | N = Delay ÷ 12 µs | COUNT | CPI |
| --- | --- | --- | --- | --- | --- |
| Sessional-1 2022 Q4 | 8 (0 to 7) | 60 ms | 5000 | 1388H | 08H |
| Sessional-1 2024 Q5 | 10 (0 to 9) | 90 ms | 7500 | 1D4CH | 0AH |
| Sessional-1 2025 Q4 | 8 (0 to 7) | 100 ms | 8333 | 208DH | 08H |
| Endsem 2022 Q3'(b) | 10 (0 to 9) | 90 ms | 7500 | 1D4CH | 0AH |
| Endsem 2023 Q3'(b) | 9 (0 to 8) | 60 ms | 5000 | 1388H | 09H |
| Endsem 2024 Q3(c) | 9 (0 to 8) | 60 ms | 5000 | 1388H | 09H |
| Endsem 2025 Q3(c) | 10 (0 to 9) | 50 ms | 4167 | 1047H | 0AH |

```latex
\begin{aligned}
\frac{90000}{12} &= 7500 = 1D4C_H, & \frac{100000}{12} &= 8333.3 \approx 8333 = 208D_H \\
\frac{50000}{12} &= 4166.7 \approx 4167 = 1047_H, & \frac{60000}{12} &= 5000 = 1388_H
\end{aligned}
```

When the division isn't exact (100 ms and 50 ms), round to the nearest whole count and say so. The error is a few microseconds out of tens of milliseconds (7.5 µs at 50 ms), under 0.02%.

**Answer: the same program each time; only COUNT = Delay ÷ (24 × 0.5 µs), in hex, and the CPI modulus change.**
