# SE Unit 2: Project Planning, Requirements, SRS, COCOMO and Risk

*Endsem RUN · about 50 minutes*

**The whole unit in one breath:** before building, you must find out **what** to build (requirements engineering, written up as an **SRS**), estimate **how much effort and time** it needs (**COCOMO**), and plan for what could **go wrong** (risk management).

**What the endsem asks from here:** a COCOMO numerical (almost guaranteed), SRS characteristics, and risk management steps. 2025's whole Q2 came from here.

---

## 1. Requirement engineering · Quick

A **requirement** is a feature or constraint the system must have. **Requirement engineering** is the process of finding, analysing, documenting and checking them. It's the cheapest place to fix mistakes: a wrong requirement found after delivery can cost 100 times more to fix.

**Crucial process steps:**

1. **Requirements elicitation:** gather needs from stakeholders.
2. **Requirements analysis:** remove conflicts and ambiguity, model them (DFDs, use cases).
3. **Requirements documentation:** write the SRS.
4. **Requirements review (validation):** check the SRS with stakeholders.
(Plus **requirements management**: handling changes throughout.)

### Types of requirements

| Type | Meaning | Example (a banking app) |
| --- | --- | --- |
| **Functional** | What the system must **do** | "Transfer money between accounts", "generate a statement" |
| **Non-functional** | How **well** it must do it (quality constraints) | Response time < 2 s, 99.9% uptime, data encrypted |
| **Domain** | Rules from the application domain | RBI's limit on UPI transfers |

Another classic classification (by how obvious they are): **known** (stakeholders say them), **unknown** (stakeholders forgot, but need them) and **undreamt** (nobody imagined them yet).

### Elicitation techniques

- **Interviews** (open-ended or structured): talk to users directly.
- **Brainstorming:** a group throws out ideas freely, then filters them.
- **FAST (Facilitated Application Specification Technique):** a joint meeting of developers and customers with a facilitator, producing lists of objects, services and constraints.
- **QFD (Quality Function Deployment):** turns customer needs into technical requirements, ranking them as normal, expected and exciting.
- **Use case approach:** describe the system through actor–system scenarios.
- **Delphi technique:** experts answer anonymously in rounds until they converge.
- Also: questionnaires, observation, studying existing documents.

---

## 2. The SRS · Slow down

**Exam line:** *A Software Requirements Specification (SRS) is a document that completely describes the expected behaviour of a software system, including its functional and non-functional requirements, interfaces and constraints, and serves as an agreement between the customer and the developers.*

It's the contract: developers build to it, testers test against it, and the customer signs it.

**IEEE 830 outline:** 1. Introduction (purpose, scope, definitions, references, overview) 2. Overall description (product perspective, functions, user characteristics, constraints, assumptions) 3. Specific requirements (functional, external interfaces, performance, design constraints, quality attributes) + appendices and index.

> **Endsem 2025 · Q2(b) · 4.5 marks**
> List and explain the features of a good Software Requirements Specification (SRS).

**Answer.**

A good SRS (per IEEE 830) has these characteristics:

1. **Correct:** every requirement stated is one the software really must meet. Checked by review with the customer.
2. **Unambiguous:** every requirement has exactly **one** interpretation. "The system should be fast" is ambiguous; "search results in under 2 seconds" isn't.
3. **Complete:** includes *all* requirements (functional, performance, interfaces, constraints) and defines the response to *all* inputs, valid and invalid. No "TBD" left.
4. **Consistent:** no two requirements conflict (e.g. one says dates are DD/MM/YYYY, another MM/DD/YYYY).
5. **Ranked for importance and stability:** each requirement is marked essential / desirable / optional, and how likely it is to change, so effort goes to what matters.
6. **Verifiable:** every requirement can be tested by some finite, cost-effective method. "Easy to use" isn't verifiable; "a new user completes checkout in under 3 minutes" is.
7. **Modifiable:** organised (numbered, indexed, no redundancy) so changes can be made easily and consistently.
8. **Traceable:** each requirement's origin is clear (backward traceability) and it can be referenced by later design, code and tests (forward traceability), via unique IDs like FR-12.

Also good to mention: **concise** and **design-independent** (it says *what*, not *how*).

**Correct, unambiguous, complete, consistent, ranked, verifiable, modifiable and traceable.**

---

## 3. COCOMO · Slow down

**COCOMO** (COnstructive COst MOdel, Barry Boehm, 1981) estimates **effort** (person-months), **development time** (months) and **team size** from the project's size in **KLOC** (thousands of lines of code).

**Three project modes:**

| Mode | Description | Example |
| --- | --- | --- |
| **Organic** | Small team, familiar problem, flexible requirements | Payroll, inventory system |
| **Semi-detached** | Medium size, mixed experience, some rigid requirements | Compiler, database system |
| **Embedded** | Tight hardware/software/operational constraints | Flight control, ATM network, real-time systems |

**Three levels:**

- **Basic COCOMO:** effort from size alone.
- **Intermediate COCOMO:** basic, corrected by an **Effort Adjustment Factor (EAF)**, the product of 15 **cost drivers** (product, hardware, personnel and project attributes like required reliability, analyst capability, use of tools), each rated from very low to extra high.
- **Detailed COCOMO:** intermediate, applied phase by phase and module by module.

**Formulas:**

```latex
\begin{aligned}
E &= a \cdot (\text{KLOC})^{b} \cdot \text{EAF} \quad \text{person-months} \\
D &= c \cdot E^{\,d} \quad \text{months} \\
\text{Team size} &= \frac{E}{D} \text{ persons}, \qquad \text{Productivity} = \frac{\text{LOC}}{E} \text{ LOC/PM}
\end{aligned}
```

| Mode | Basic a | Intermediate a | b | c | d |
| --- | --- | --- | --- | --- | --- |
| Organic | 2.4 | 3.2 | 1.05 | 2.5 | 0.38 |
| Semi-detached | 3.0 | 3.0 | 1.12 | 2.5 | 0.35 |
| Embedded | 3.6 | 2.8 | 1.20 | 2.5 | 0.32 |

(Basic COCOMO has no EAF, i.e. EAF = 1.)

> **Endsem 2025 · Q2(a) · 4.5 marks**
> A project is estimated at 55 KLOC. Using COCOMO in the Embedded mode, with Effort Adjustment Factor EAF = 1.25, calculate (1) Effort, (2) Development time, (3) Team size, (4) Productivity.

**Answer.**

An EAF is given, so this is **Intermediate COCOMO**, embedded mode: a = 2.8, b = 1.20, c = 2.5, d = 0.32.

```latex
\begin{aligned}
55^{1.20} &= e^{1.20 \ln 55} = e^{1.20 \times 4.0073} = e^{4.8088} = 122.58 \\
E_{nominal} &= 2.8 \times 122.58 = 343.24 \text{ PM} \\
E &= 343.24 \times 1.25 = 429.05 \text{ person-months} \\
D &= 2.5 \times 429.05^{0.32} = 2.5 \times 6.957 = 17.39 \text{ months} \\
\text{Team size} &= \frac{429.05}{17.39} = 24.67 \approx 25 \text{ persons} \\
\text{Productivity} &= \frac{55{,}000}{429.05} = 128.2 \text{ LOC per person-month}
\end{aligned}
```

**Effort ≈ 429 PM, time ≈ 17.4 months, team ≈ 25 people, productivity ≈ 128 LOC/PM.**

(If a teacher treats it as Basic COCOMO scaled by EAF, a = 3.6 gives E ≈ 551.6 PM, D ≈ 18.8 months, team ≈ 29, productivity ≈ 99.7. Say which model you used; with an EAF, intermediate is the correct one.)

---

## 4. Risk management · Slow down

A **risk** is a problem that *might* happen and would hurt the project if it did. Two properties: **probability** (how likely) and **impact** (how bad). Unlike a problem, a risk hasn't happened yet, so you can still prepare. Like checking the weather and carrying an umbrella, instead of drying off after.

**Types:** project risks (schedule, budget, staff leaving), technical risks (new technology, performance), business risks (market changes, losing management support).

**Risk exposure** = probability × loss. E.g. a 30% chance of losing ₹10 lakh → exposure ₹3 lakh.

> **Endsem 2025 · Q2(c) · 4.5 marks**
> What is risk management in software engineering? Write down the steps of risk management.

**Answer.**

**Risk management** is the systematic process of identifying, analysing and controlling the uncertain events that could threaten a software project's schedule, cost or quality, so that their probability or impact is reduced before they turn into problems.

Following Boehm, it has two parts, each with three steps:

**A. Risk assessment**

1. **Risk identification:** list everything that could go wrong, using checklists, brainstorming and past project data. E.g. "key developer may leave", "requirements may change", "new framework may be too slow".
2. **Risk analysis:** estimate each risk's **probability** and **impact** (and so its exposure = probability × loss).
3. **Risk prioritisation:** rank the risks by exposure and focus on the top ones (e.g. the top 10).

**B. Risk control**

4. **Risk management planning:** for each major risk, decide a strategy: **avoid** it (change the plan), **reduce/mitigate** it (e.g. cross-train staff), **transfer** it (insurance, outsourcing) or **accept** it with a contingency plan.
5. **Risk resolution (monitoring and mitigation):** carry out the plans and act when a risk occurs.
6. **Risk monitoring:** keep tracking risks throughout the project, re-assess them, and watch for new ones.

| Risk | Probability | Impact | Plan |
| --- | --- | --- | --- |
| Key developer leaves | Medium | High | Pair programming, documentation, cross-training |
| Requirements change late | High | Medium | Iterative model, change control |
| New library too slow | Low | High | Prototype early, keep a fallback |

**Risk management = assessment (identify, analyse, prioritise) + control (plan, resolve, monitor).**

---

## 5. Quick recap

- RE steps: elicitation → analysis → documentation (SRS) → review.
- Requirements: functional (what), non-functional (how well), domain.
- Elicitation: interviews, brainstorming, FAST, QFD, use cases, Delphi.
- Good SRS: correct, unambiguous, complete, consistent, ranked, verifiable, modifiable, traceable.
- COCOMO: $E = a\,\text{KLOC}^b \cdot \text{EAF}$, $D = 2.5 E^d$, team = E/D; intermediate embedded a = 2.8, b = 1.20, d = 0.32.
- Risk: exposure = probability × loss; identify → analyse → prioritise → plan → resolve → monitor.
