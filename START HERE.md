# Sem 5 tracker

Last updated: 2026-11-24

## Now: endsems

All five units of every subject (`Sem 5 Syllabus.pdf`). Second sessionals are over.

Each subject folder has an **`Endsem RUN`** folder with:

- **Unit 1 to Unit 5** PDFs: one exam-focused doc per syllabus unit, written to teach from zero (plain-words explanation first, then the exam definition, examples, and every topic tagged **Quick** or **Slow down**). Every 2025 endsem question sits inside the unit at the topic it belongs to, fully solved.
- **Endsem Solved 2025.pdf**: the whole 2025 endsem paper, every part (OR options included) solved, with a note of which unit teaches each answer.
- `md/`: the editable sources (and `md/images/` for figures). Re-render a PDF with `python tools/md2pdf.py "<file>.md"` from the acads folder.

| Subject | Units | Notes on the 2025 paper |
| --- | --- | --- |
| OOP | 1 Classes and objects, 2 Polymorphism and overloading, 3 Inheritance and virtual functions (+ templates), 4 Java classes and interfaces, 5 Exceptions and generics | All C++ and Java code compiled and run (g++ 16, JDK 21) |
| Computer Networks | 1 Introduction, models, switching, 2 Data link layer, 3 MAC sublayer, 4 IPv4, subnetting, NAT, IPv6, 5 Routing | Q4(a)'s printed options are all false: N and P share a subnet, M doesn't (paper's options look misprinted; correct statement given) |
| Software Engineering | 1 Life cycle models, 2 Requirements, SRS, COCOMO, risk, 3 Analysis, design, reliability, 4 Testing, 5 Maintenance | Unit 4 includes Testing Part 2 and Unit 5 uses sir's Unit 5 slides, both found on Drive (not in the Notes folder) |
| Data Mining | 1 Intro and preprocessing, 2 Association rules, 3 Decision trees and Bayes, 4 Advanced classification, 5 Clustering | Every numerical (PCA, Apriori, Eclat, Naive Bayes, info gain, k-means, dendrogram) checked by computer. Q3(c) uses Han's example, because the paper's data makes every hash bucket survive |
| Microprocessor | 1 Architecture, pins, timing, 2 Instruction sets, 3 8085 programs and delays, 4 Interfacing, interrupts, DMA, 5 8086 programming | 8085 programs run on a simulator (`tools/sim8085.py`), 8086 programs on an x86 emulator; the 50 ms delay is exact to the T-state |
| Automata | 1 Finite automata, 2 Regular expressions and pumping lemma, 3 CFGs, 4 PDAs, 5 Turing machines | Q2(c) is a trap: the language is regular (starts and ends with the same letter). DFA, grammar and TM answers checked by computer |

## Deadlines

- **CSC-504 (SE) sessional make-up, Wednesday 25 Nov, 10:00–11:30.** Faisal sir's notice (23 Nov, SE Classroom) attaches the Sessional 1 and 2 marks. **Mandatory** if you missed either sessional: submit solutions to all Sessional 1 and 2 questions, plus all built-in exercises from Software Testing Part 2 and Unit 5 (Maintenance). **Optional** if you scored under 4 in either. A **viva** on the Sessional 2 syllabus follows. Check your row in `CSC_504_Sessional 1 and 2 Marks.pdf` (handwritten scan, couldn't be read reliably by computer).
- Classroom To-do is otherwise empty (checked 24 Nov).

## Missing on Classroom (all closed, "Not accepting work")

- OOP Lab: Template and Polymorphism (due 28 Oct), Passing Object as argument (due 23 Aug)
- Computer Networks: Sliding Window Protocol assignment (due 13 Oct)

## Labs

- Software Engineering: `Software Engineering/Lab/SE Lab File - 24BCS064.pdf` (all 7 experiments).
- Computer Networks: `Computer Networks/Lab/CN Lab File - 24BCS064.pdf` (all 8 experiments from the practical index, Python, hibiscus character-art cover; a light printer-friendly cover is beside it). Programs are in `Computer Networks/Lab/programs/`; all were actually run, and the screenshots are their real output. "Submitted to" is left blank to fill in by hand. Rebuild with `python tools/cnlab/run_all.py` then `python tools/cnlab/build.py`.
- OOP, Microprocessor: no index for this year's experiments in any folder; only old-batch material in each `Lab` folder.
- [Binary to Decimal lab record (8085)](https://claude.ai/artifact/84XZAzrgmgkE4j8ZNa1fra): run it on the kit once to confirm.

## Folders

Each subject has `Endsem RUN`, `Assignments`, `Notes` and `PYQs`; subjects with a lab also have `Lab`. `tools/` holds the scripts that build and check the docs (renderer, code checker, 8085 simulator, diagram scripts). `Older Mixed Papers` has older combined papers.

The second-sessional RUN docs (and their `Second Sessional RUN Docs` folder) were removed on 24 Nov; they are still in git history and as Claude Docs online.

GitHub: this whole folder is pushed to https://github.com/shahanxd/acads_five (branch `main`). Commit and push again after changes.

Flagged paper errors: CN 2025 Q4(a) options misprinted; CN 2025 Q2(b) has no encoding for D (taken as B) and a 9-bit ESC; Automata S2 2025 Q3(ii) asks for a PDA for wcw, which isn't context-free; Automata S2 2024 Q3 has a variable K with no rules.

## Missing material

- Software Testing Part 2 slides and SE Unit 5 slides exist only on Drive/Classroom (shared by Dr. Faisal Malik), not in `Software Engineering/Notes`
- Data Mining Units 1 and 2 slides (Hannan sir's, on the IDM Classroom) aren't downloaded, but the Unit 1 and 2 docs were checked against them on 24 Nov (attribute types, χ² and covariance examples, binary dissimilarity, sampling added to Unit 1)
- Classroom (checked 24 Nov) has nothing for OOP theory, Microprocessor theory or Automata, and only one assignment for Computer Networks
