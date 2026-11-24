# SE Unit 4: Software Testing

*Endsem RUN · about 55 minutes*

**The whole unit in one breath:** testing means running the software to **find faults**. You either test from the **outside** using the specification (black box: boundary values, equivalence classes, cause-effect graphs) or from the **inside** using the code (white box: paths, data flow, mutation), and you test at **levels**: unit, integration, system, acceptance. Debugging then finds and fixes the cause.

**What the endsem asks from here:** a BVA + ECP test-case question on a range (guaranteed), levels of testing, and black vs white box. 2025's whole Q4 was exactly that.

---

## 1. Terminology · Quick

- **Testing:** executing a program with the intent of **finding faults**. A test that finds a bug is a *successful* test. Testing can show the presence of bugs, never their absence (Dijkstra).
- **Error → fault → failure:** a human mistake causes a fault (bug) in the code, which causes a failure when executed.
- **Test case:** inputs + execution conditions + **expected output**. **Test suite:** a set of test cases.
- **Verification:** "Are we building the product **right**?" (checking against the design/spec: reviews, inspections, static). **Validation:** "Are we building the **right** product?" (checking against the user's real needs: executing tests, acceptance).
- **Static testing** (no execution: reviews, walkthroughs, inspections) vs **dynamic testing** (running the code).

---

## 2. Black box vs white box · Quick

> **Endsem 2025 · Q4(c) · 4.5 marks**
> Explain black box and white box testing with suitable examples.

**Answer.**

**Black box testing (functional / behavioural testing):** the tester treats the program as a **closed box**: they don't look at the code, only at the **specification**. Test cases are designed from the requirements: give inputs, compare outputs with the expected outputs. Like testing a calculator app by pressing buttons, without reading its code.

- Techniques: boundary value analysis, equivalence class partitioning, cause-effect graphing, decision tables.
- Finds: missing or wrong functions, interface errors, behaviour and performance errors.
- Example: for a login screen, test a valid username/password, a wrong password, an empty field and a 100-character username, and check the messages.

**White box testing (structural / glass box testing):** the tester **looks inside the code** and designs test cases to exercise its **structure**: every statement, every branch, every path and loop. Like a mechanic checking every pipe of an engine.

- Techniques: statement/branch/path coverage, basis path testing (cyclomatic complexity), data flow testing, mutation testing.
- Finds: logic errors, unreachable code, wrong conditions, loop-boundary errors.
- Example: for `if (marks >= 40) pass(); else fail();` write two tests, marks = 50 and marks = 30, so **both branches** run.

| Basis | Black box | White box |
| --- | --- | --- |
| Based on | Specification (SRS) | Code structure |
| Code knowledge needed | No | Yes |
| Done by | Testers, users | Developers |
| Level mostly | System, acceptance | Unit, integration |
| Also called | Functional, behavioural | Structural, glass box, clear box |
| Misses | Untested hidden paths | Missing features (code can't show what isn't there) |

**Black box tests what the system does from the spec; white box tests how it does it from the code.**

---

## 3. Boundary value analysis and equivalence classes · Slow down

**Why boundaries?** Programmers love off-by-one bugs: writing `<` instead of `<=`. Errors cluster at the **edges** of input ranges, so BVA tests exactly there.

**Boundary Value Analysis (BVA):** for a range [min, max], test **min, min+1, a nominal value, max−1, max**. For n inputs that's **4n + 1** test cases (each variable takes its five values while the others stay nominal). **Robust BVA** adds the invalid **min−1 and max+1**, giving **6n + 1**.

**Equivalence Class Partitioning (ECP):** split the input domain into classes where every value behaves the same, so **one test per class** is enough. For a range there are three classes: below, inside, above. Like tasting one spoon from each pot instead of every spoonful.

> **Endsem 2025 · Q4(b) · 4.5 marks**
> A system accepts an age between 18 and 60 (valid: 18–60; invalid: less than 18 or greater than 60). Explain (a) Boundary Value Analysis and (b) Equivalence Class Partitioning with test cases for this scenario.

**Answer.**

**(a) Boundary Value Analysis.** Errors are most likely at the edges of the valid range, so we test values **at, just inside and just outside** each boundary. One variable (age), range [18, 60], nominal value ≈ 39.

Normal BVA uses 4n + 1 = **5** cases; robust BVA adds the two outside values for **7**:

| Test case | Age | Why | Expected output |
| --- | --- | --- | --- |
| TC1 | 17 | min − 1 (robust) | Invalid: rejected |
| TC2 | 18 | min | Valid: accepted |
| TC3 | 19 | min + 1 | Valid |
| TC4 | 39 | nominal | Valid |
| TC5 | 59 | max − 1 | Valid |
| TC6 | 60 | max | Valid |
| TC7 | 61 | max + 1 (robust) | Invalid: rejected |

If the code wrongly says `age > 18` instead of `age >= 18`, TC2 catches it.

**(b) Equivalence Class Partitioning.** The input domain is divided into classes whose members are treated the same:

| Class | Range | Type | Representative test | Expected |
| --- | --- | --- | --- | --- |
| EC1 | age < 18 | Invalid | 10 | Rejected |
| EC2 | 18 ≤ age ≤ 60 | Valid | 35 | Accepted |
| EC3 | age > 60 | Invalid | 75 | Rejected |
| EC4 (extra) | non-numeric / empty | Invalid | "abc", blank | Rejected with an error message |

One test per class covers the whole domain: **3 test cases** (4 with the non-numeric class) instead of testing every possible age.

**BVA tests the edges 17, 18, 19, 39, 59, 60, 61; ECP tests one value per class: 10 (invalid), 35 (valid), 75 (invalid).**

---

## 4. Cause-effect graphing and decision tables · Quick

For outputs that depend on **combinations** of input conditions. List the **causes** (input conditions, C1, C2 …) and **effects** (outputs, E1, E2 …), connect them with Boolean logic (identity, NOT, AND, OR), add constraints between causes (E exclusive, I inclusive, O one-and-only-one, R requires) and between effects (M mask), then convert the graph to a **decision table**: **each column = one test case**.

Example (from the Part 2 slides): a loan is approved only if income OK (C1) AND credit good (C2) AND documents verified (C3).

| | R1 | R2 | R3 | R4 |
| --- | --- | --- | --- | --- |
| C1 income OK | 1 | 0 | 1 | 1 |
| C2 credit good | 1 | 1 | 0 | 1 |
| C3 docs verified | 1 | 1 | 1 | 0 |
| E1 approved | ✓ | | | |
| E2 rejected | | ✓ | ✓ | ✓ |

4 rules → 4 test cases.

---

## 5. Structural (white box) techniques · Slow down

**Path testing:** draw the program's **control flow graph** (nodes = statements/blocks, edges = flow) and test every **independent path** at least once. How many? The **cyclomatic complexity**:

```latex
V(G) = E - N + 2 = P + 1 = \text{number of regions}
```

where E = edges, N = nodes, P = predicate (decision) nodes. Example: one `if-else` inside one `while` loop → P = 2 → V(G) = 3 independent paths → 3 test cases. V(G) above 10 means the module is too complex.

**Data flow testing:** follow each **variable** from where it's **defined** (given a value) to where it's **used**, and test those def-use paths. Catches anomalies like **use before definition** (`total = total + price` with `total` never initialised) or a definition never used.

**Mutation testing:** tests the **quality of your test suite**. Make small deliberate changes ("**mutants**", e.g. `>` → `>=`, `+` → `−`) and run the tests. If a test fails, the mutant is **killed** (good); if all pass, it **survived**, so the tests have a blind spot. **Mutation score = killed / total mutants.**

---

## 6. Levels of testing · Slow down

> **Endsem 2025 · Q4(a) · 4.5 marks**
> Explain the different levels of software testing (Unit, Integration, System and Validation testing) with suitable examples.

**Answer.**

Testing is done in levels, from the smallest piece to the whole system, like checking every brick, then each wall, then the whole house, then letting the owner inspect it.

**1. Unit testing:** testing **individual modules/functions** in isolation, usually by the developer, mostly white box. Missing callers and callees are simulated: a **driver** calls the unit, and **stubs** stand in for the modules it calls.
*Example:* testing a `calculateInterest(principal, rate, years)` function alone with several inputs, including 0 years and a negative rate.

**2. Integration testing:** combining tested units and testing their **interfaces**, to find errors in how modules talk (wrong parameters, data format mismatches). Approaches:

- **Big bang:** integrate everything at once (hard to locate faults).
- **Top-down:** start from the main module, add lower ones gradually, using **stubs** for missing ones.
- **Bottom-up:** start from the lowest modules, using **drivers**, and move up.
- **Sandwich (hybrid):** both at once.

*Example:* after the login and dashboard modules pass unit tests, check that a successful login really passes the user's ID to the dashboard and shows their data.

**3. System testing:** testing the **complete integrated system** against the SRS, functional and non-functional, by an independent test team (black box). Types: functional, **performance**, **stress/load** (beyond normal limits), **security**, **recovery** (does it recover after a crash?), usability and compatibility testing.
*Example:* for an online shopping site: the whole flow from search to payment, plus 10,000 simultaneous users (load) and SQL-injection attempts (security).

**4. Validation (acceptance) testing:** checking the software meets the **customer's real needs**, by or with the customer, before it's accepted.

- **Alpha testing:** by users at the **developer's site**, with developers watching.
- **Beta testing:** by real users at **their own sites**, in the real environment, reporting problems back.

*Example:* a bank's staff use the new loan system on real-looking cases and sign off (acceptance); a beta version of an app is released to 1,000 users.

| Level | Tests | Done by | Box |
| --- | --- | --- | --- |
| Unit | One module | Developer | White |
| Integration | Interfaces between modules | Developers / testers | Both |
| System | Whole system vs SRS | Independent testers | Black |
| Validation | Fit to user needs | Customer | Black |

**Unit → integration → system → validation: from one module, to modules together, to the whole system against the SRS, to the customer accepting it (alpha, beta).**

**Regression testing:** re-running old tests after a change, to make sure nothing that worked before is broken. Needed at every level, especially in maintenance.

---

## 7. Debugging · Quick

**Debugging** happens *after* testing finds a failure: reproduce it, **locate** the fault, fix it, and re-test. Testing finds the symptom; debugging finds the cause.

| Approach | How |
| --- | --- |
| **Brute force** | Print statements and memory dumps everywhere, then search the output. Most common, least efficient |
| **Backtracking** | Start where the failure shows up and trace the code **backwards** until the cause is found. Good for small programs |
| **Cause elimination** | List possible causes and eliminate them: **induction** (from the specific clues to a general hypothesis) or **deduction** (from all possible causes, rule out until one remains). Binary partitioning of the code is a form of this |

**Testing tools:** static analysers (SonarQube, PMD), unit-test frameworks (JUnit, PyTest), functional automation (Selenium), performance/load (JMeter, LoadRunner), test management (JIRA, TestRail), defect tracking (Bugzilla) and coverage (JaCoCo). They're fast and repeatable but can't judge usability and only run the tests you design.

---

## 8. Quick recap

- Testing finds faults; verification = built right, validation = right thing built.
- Black box from the spec (BVA, ECP, cause-effect); white box from the code (paths, data flow, mutation).
- BVA: min, min+1, nom, max−1, max (4n+1); robust adds min−1, max+1 (6n+1).
- ECP: one test per class (below / inside / above the range).
- Cyclomatic complexity V(G) = E − N + 2 = P + 1.
- Mutation score = killed / total mutants.
- Levels: unit (stubs, drivers) → integration (big bang, top-down, bottom-up, sandwich) → system → acceptance (alpha, beta).
- Debugging: brute force, backtracking, cause elimination.
