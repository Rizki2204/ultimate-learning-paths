# TEST_READY: Pilot 011 Automated Verification Suite & Test Runner

**Repository**: `ultimate-learning-paths`  
**Target Module**: Topic 011 — *Aljabar Linier & Teori Matriks (Ruang Vektor, Eigenvalues, SVD, Dekomposisi Tensor)*  
**Harness Script**: `scripts/verify_pilot_011.py`  
**Infrastructure Blueprint**: `TEST_INFRA.md`  
**Test Writer Track**: Track A (E2E Test Infrastructure)  
**Status**: **TEST SUITE COMPLETE & READY FOR ACCEPTANCE GATING**

---

## 1. Quick Start: How to Run the Test Harness

The test runner is a standalone, dependency-light CLI utility that tests the Topic 011 Pilot Rebuild against all specifications in `ORIGINAL_REQUEST.md` and `PROJECT.md`.

```bash
# 1. Run Complete E2E Acceptance Suite (Tiers 1-5 with Live HTTP Checks)
python scripts/verify_pilot_011.py

# 2. Run Complete Suite in Offline Mode (Skips Live HTTP Requests)
python scripts/verify_pilot_011.py --skip-network

# 3. Run Specific Verification Tier
python scripts/verify_pilot_011.py --tier 1    # Tier 1: Feature Coverage & Syllabus
python scripts/verify_pilot_011.py --tier 2    # Tier 2: Boundary-Value & Corner Cases
python scripts/verify_pilot_011.py --tier 3    # Tier 3: Repository & Cross-Feature Integration
python scripts/verify_pilot_011.py --tier 4    # Tier 4: Real-World Execution (Code & Links)
python scripts/verify_pilot_011.py --tier 5    # Tier 5: Adversarial Hardening & Anti-Facade

# 4. Generate Machine-Readable JSON Report
python scripts/verify_pilot_011.py --json .agents/teamwork/pilot_011_report.json

# 5. Verbose Diagnostic Mode with Immediate Failure Abort
python scripts/verify_pilot_011.py --verbose --fail-fast
```

---

## 2. Comprehensive Coverage Summary

The test harness evaluates **17 distinct automated test assertions** across 5 progressive tiers:

| Tier | Test Category | Methodology | Key Verifications & Assertions |
|:---:|---|---|---|
| **Tier 1** | **Feature Coverage** | Category-Partition | - Validates existence of Master Gateway `011-aljabar-linier-teori-matriks.md`<br>- Validates Topic Map `011-aljabar-linier-teori-matriks/README.md`<br>- Validates all 9 subtopic chapter files (`01` through `09`)<br>- Enforces all 7 mandatory Indonesian section headers in Gateway<br>- Enforces all 7 mandatory core elements in every subtopic file<br>- Validates comprehensive syllabus coverage (MIT 18.06, MIT 18.065, Strang, Multilinear Algebra, CP & Tucker Decompositions) |
| **Tier 2** | **Boundary & Corner Cases** | Boundary-Value Analysis | - Binary byte scan for zero ASCII control characters (`0x00`–`0x1F` except `\n` and `\r`), eliminating `\x07` (bell), `\x08` (backspace), `\x09` (tab)<br>- KaTeX syntax validation: balanced `$` and `$$`, no empty blocks, no corrupted macros (`\alpha`, `\beta`, `\theta`, `\times`)<br>- Scans for forbidden placeholder tokens (`TODO`, `FIXME`, `TBD`, `lorem ipsum`)<br>- Scans for forbidden scaffolding phrases (`Model formal untuk`, `Implementasi referensi`, etc.)<br>- Detects duplicate exercise blocks and redundant section headers<br>- Enforces minimum file size boundaries (Gateway $\ge 4$KB, README $\ge 2$KB, subtopics $\ge 5$KB) |
| **Tier 3** | **Integration** | Pairwise & Traceability | - Validates that all 13 inbound relative links across `INDEX.md`, `curriculum/`, `tracks/`, and `drills/` resolve cleanly<br>- Validates bidirectional navigation between Gateway, README, and all 9 subtopics<br>- Verifies `drills/tier-01-mathematics-drills.md` includes SVD, Cholesky, and Tensors with collapsible `<details><summary>` keys<br>- Verifies `flashcards/deck-01-cognitive-logic-math` (`.tsv` & `.md`) satisfies 3-column TSV format, cloze syntax `{{c1::...}}`, and 011 concept coverage<br>- Repository Scope Guard: Asserts via `git status` that zero curriculum files outside Topic 011 are modified |
| **Tier 4** | **Workload & Execution** | Empirical Testing | - Extracts executable Python code blocks and executes them in isolated subprocesses (timeout: 15s)<br>- Validates exit code 0 and verifies that actual stdout matches documented textbook output<br>- Discovers all external HTTP(S) links; verifies density ($\ge 2$ links per subtopic heading)<br>- Prohibits bare domain homepages (enforces deep links to specific chapters/lectures/tools)<br>- Conducts live HTTP `HEAD`/`GET` requests with timeout and asserts HTTP 200/300 responses |
| **Tier 5** | **Adversarial Hardening** | White-Box Hardening | - Verifies all Python code blocks parse with `ast.parse`<br>- Guards against hardware register contamination (`0xEA00_0010`, `ALU_OUT`) in mathematics modules<br>- Guards against dummy synthetic strings (`process_critical_payload`, random bit mutation fuzzing)<br>- Rejects C/C++ syntax embedded in Python code fences |

---

## 3. Pass / Fail Acceptance Criteria

- **Success Criteria (`Exit 0`)**:
  - 100% of executed tests in the enabled tiers pass with zero errors.
  - Zero control characters, zero broken links, zero placeholder tokens, zero code execution failures.
  - Baseline repository governance scripts (`verify_curriculum.py`, `verify_ecosystem.py`, `full_audit.py`) exit 0.
- **Failure Criteria (`Exit 1`)**:
  - Any missing file, missing mandatory element, corrupted LaTeX formula, broken inbound link, failed Python execution, or dead external URL triggers an immediate test failure with detailed diagnostics.

---

## 4. Baseline Regression Test Commands

The repository's existing governance and verification suites must be executed alongside `verify_pilot_011.py`:

```bash
# 1. Verify Curriculum Structure & Anti-Facade Rules (17 Tiers, 232 Modules)
python scripts/verify_curriculum.py

# 2. Verify Full Learning Ecosystem (6 Phases: Labs, Tracks, Drills, Flashcards, Cleanliness)
python scripts/verify_ecosystem.py

# 3. Deep Audit of 232 Modules (Directory Modularity Compatible)
python scripts/full_audit.py

# 4. Stage 0 Pilot 011 E2E Acceptance Gate
python scripts/verify_pilot_011.py --skip-network
```

---

## 5. Directory Modularity Compatibility

`scripts/full_audit.py` has been updated with directory modularity support:
- Subtopic files inside `curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks/` are isolated from the top-level 232 topic file counter.
- `full_audit.py` continues to enforce `assert len(topic_files) == 232` against the 232 top-level gateway modules, while `scripts/verify_pilot_011.py` validates all granular subtopic files.
- `python scripts/full_audit.py` passes cleanly with **Exit Code 0**.
