# Test Infrastructure & E2E Verification Architecture (Topic 011 Pilot Rebuild)

## 1. Overview & Architectural Principles

The Stage 0 Pilot Rebuild of Topic **011: Aljabar Linier & Teori Matriks (Ruang Vektor, Eigenvalues, SVD, Dekomposisi Tensor)** establishes the foundational gold-standard textbook pattern for the entire `ultimate-learning-paths` ecosystem. 

To ensure absolute pedagogical rigor, mathematical fidelity, zero rendering corruption, authentic executable code, and seamless repository integration, the testing infrastructure adopts an **opaque-box, multi-tier automated test harness**: `scripts/verify_pilot_011.py`.

### 1.1 Dual-Track Governance Principle
In accordance with the Project Pattern Dual-Track specification:
- **Track A (Testing Track)**: Owns test infrastructure, test runners, validation suites, and repository compatibility bridges (`TEST_INFRA.md`, `TEST_READY.md`, `scripts/verify_pilot_011.py`, and `scripts/full_audit.py`).
- **Track B (Content Track)**: Owns textbook authoring, code implementation, drills, and flashcards (`curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md`, subtopic chapters `01` to `09`, `drills/`, `flashcards/`).
- **Separation of Concerns**: Test writers do not author curriculum content; content authors do not weaken test assertions. Tests act as strict, impartial arbiters of all user requirements.

---

## 2. The 4-Tier (+ Tier 5 Adversarial) Verification Methodology

The test suite organizes verification into progressive tiers based on formal software testing methodologies:

```
+-----------------------------------------------------------------------------+
|                      STAGE 0 PILOT ACCEPTANCE HARNESS                       |
|                       (scripts/verify_pilot_011.py)                         |
+-----------------------------------------------------------------------------+
                                      |
      +-------------------------------+-------------------------------+
      |                               |                               |
      v                               v                               v
[TIER 1: FEATURE COVERAGE]    [TIER 2: BOUNDARY & CORNER]    [TIER 3: INTEGRATION]
* Category-Partition Testing  * Boundary-Value Analysis     * Pairwise Integration
* Master Gateway & Subtopics  * Binary Control Chars        * 13 Inbound Repo Links
* 7 Mandatory Elements        * KaTeX Math Syntax & Delim   * Intra-Module Navigation
* Syllabus MIT 18.06/18.065   * Zero Placeholder Tokens     * Tier-1 Drills Sync
* Tensor CP/Tucker Specs      * No Duplicate Sections       * Deck-01 Flashcard TSV
                               * File Size Boundaries        * Scope Diff Guard
                                      |
                                      +-------------------------------+
                                      |                               |
                                      v                               v
                          [TIER 4: REAL-WORLD WORKLOAD]   [TIER 5: ADVERSARIAL]
                          * Subprocess Python Execution   * Mutation Detection
                          * Output Verbatim Matching      * AST Syntax Integrity
                          * Live HTTP Deep Link Audit     * Anti-Facade Guard
                          * 0 Bare Domain Homepages       * Jaccard Uniqueness
```

### 2.1 Tier 1: Feature Coverage & Syllabus Completeness (Category-Partition)
- **Objective**: Ensure 100% of the prescribed curriculum artifacts exist and satisfy structural prerequisites.
- **Artifact Verification**:
  1. `curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md` (Master Gateway).
  2. `curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks/README.md` (Topic Map, Study Plan, DAG).
  3. 9 Subtopic Chapters:
     - `01-vektor-eliminasi-matriks.md` (Elimination, $Ax=b$, $LU$, $LDU$, $PA=LU$)
     - `02-ruang-vektor-subruang-fundamental.md` (Subspaces, 4 Subspaces, FTLA 1 & 2, $A=CR$)
     - `03-ortogonalitas-proyeksi-faktor-qr.md` (Projections, Least Squares, Normal Eq, Gram-Schmidt, $A=QR$)
     - `04-determinan-teori-matriks.md` (Axioms, Leibniz, Laplace, Cramer, Volume/Jacobian)
     - `05-nilai-vektor-eigen-diagonalisasi.md` (Eigendecomposition, $A=X\Lambda X^{-1}$, Powers, $e^{At}$, Markov)
     - `06-matriks-simetris-definit-positif.md` (Spectral Theorem, Quadratic Forms, Sylvester, Cholesky $A=LL^T$)
     - `07-svd-dan-pseudoinverse.md` (SVD $A=U\Sigma V^T$, Eckart-Young, Moore-Penrose $A^+$, Condition Number)
     - `08-pca-analisis-komponen-utama.md` (PCA, Covariance, Rayleigh quotient, Scree plot)
     - `09-aljabar-multilinier-dekomposisi-tensor.md` (Tensors, Fibers/Slices, Matricization, Mode-$n$, CP/ALS/Kruskal, Tucker/HOSVD/HOOI)
- **The 7 Mandatory Core Elements**:
  Every subtopic file must contain distinct sections representing:
  1. Intuisi & Motivasi dari Nol (*Zero-Jargon Intuition*)
  2. Definisi Formal & Penurunan Matematis Lengkap (*Rigorous Proofs & Derivations*)
  3. Contoh Soal & Perhitungan Manual Langkah-demi-Langkah (*Fully Worked Examples*)
  4. Kode Program Komputasi Teranotasi (*Runnable Production Code*)
  5. Miskonsepsi Umum & Post-Mortem Kegagalan Nyata (*Pitfalls & Case Studies*)
  6. Latihan Mandiri Berjenjang (Pemula $\to$ Menengah $\to$ Mahir) dengan Kunci Jawaban Lengkap
  7. Tautan Sumber Belajar Standar Emas Terverifikasi (*Verified Deep Links*)

### 2.2 Tier 2: Boundary-Value & Corner Cases (Zero Defect Gate)
- **Objective**: Prevent formatting regressions, syntax corruption, and unrendered math.
- **Control Character Detection**:
  - Binary scan across all Topic 011 files for ASCII control bytes in the range `0x00`–`0x1F` (excluding newline `\n` (`0x0A`) and carriage return `\r` (`0x0D`)).
  - Explicitly flags `\x07` (Bell), `\x08` (Backspace), `\x09` (Tab), and null bytes that historically corrupted LaTeX symbols (`\alpha`, `\beta`, `\theta`, `\times`).
- **KaTeX Syntax Integrity**:
  - Verifies balanced math delimiters: `$ ... $` for inline math and `$$ ... $$` for display math.
  - Ensures no empty math delimiters (`$$` or `$$$$`).
  - Validates that backslashes before common Greek letters and operators are preserved (`\alpha`, `\beta`, `\lambda`, `\Sigma`, `\frac`, `\sum`, `\prod`).
- **Zero Placeholder / Boilerplate Audit**:
  - Scans for forbidden tokens: `TODO`, `FIXME`, `TBD`, `PLACEHOLDER`, `XXX`, `lorem ipsum`.
  - Scans for forbidden scaffolding phrases: `"Model formal untuk"`, `"Implementasi referensi"`, `"Intuisi mendasar mengenai"`, `"Anatomi internal sistem untuk"`, `"Latihan berjenjang tingkat"`.
- **Deduplication Check**:
  - Asserts that no exercise blocks, worked examples, or trace tables are repeated or duplicated within the same file.
- **File Size Thresholds**:
  - Master Gateway: $\ge 4{,}000$ bytes.
  - Subtopic Chapters: $\ge 5{,}000$ bytes each.
  - Topic Map `README.md`: $\ge 2{,}000$ bytes.

### 2.3 Tier 3: Pairwise & Cross-Feature Integration (Repository Governance)
- **Objective**: Guarantee 100% hyperlink resolution, cross-feature synchronization, and zero ripple regressions.
- **13 Inbound Repository Links**:
  - Verifies that all 13 external inbound markdown references across `INDEX.md`, `curriculum/01-fondasi-matematika/README.md`, adjacent modules (`010`, `012`), career tracks (`track-hft`, `track-embedded-robotics`, `track-ai`), and drills (`drills/tier-01-mathematics-drills.md`) resolve to a valid file on disk without broken links.
- **Intra-Module Bidirectional Navigation**:
  - Master Gateway links to `011-aljabar-linier-teori-matriks/README.md` and all 9 subtopics.
  - Every subtopic chapter links back to `../011-aljabar-linier-teori-matriks.md` (Master Gateway) and `./README.md` (Topic Map).
- **Socratic Drills Synchronization (`drills/tier-01-mathematics-drills.md`)**:
  - Confirms the presence of linear algebra questions covering the 4 fundamental subspaces, Cholesky factorization, SVD, and Tensor decompositions.
  - Enforces collapsible solution keys using `<details>` and `<summary>` HTML tags.
- **Spaced-Repetition Active Recall Synchronization (`flashcards/deck-01-cognitive-logic-math`)**:
  - Validates `deck-01-cognitive-logic-math.tsv` and `deck-01-cognitive-logic-math.md`.
  - Asserts exactly 3 tab-separated columns (`Text\tExtra\tTags`) per non-empty TSV row.
  - Confirms cloze deletion syntax `{{c1::...}}` in Column 1.
  - Confirms coverage of key Topic 011 concepts (SVD, Cholesky, Spectral Theorem, Tucker, CP, Moore-Penrose).
- **Repository Scope Guard**:
  - Uses `git status --porcelain` to verify that **NO** curriculum files outside `011-aljabar-linier-teori-matriks*` are modified. Topics 001–010 and 012–232 remain 100% untouched.

### 2.4 Tier 4: Real-World Workload & Execution (Empirical Verification)
- **Objective**: Guarantee that all code runs and all web links are live, accessible, and deep.
- **Subprocess Code Execution Engine**:
  - Automatically extracts fenced ````python` code blocks designated as runnable from Master Gateway and subtopic files.
  - Executes each code block in an isolated Python 3 subprocess with a 30-second timeout.
  - Asserts zero uncaught exceptions, zero tracebacks, and exit code `0`.
  - Verifies that the actual standard output matches the expected output documented in the textbook snippet.
- **Live HTTP Deep-Link Audit**:
  - Discovers all HTTP/HTTPS links across Topic 011 files.
  - **Density Assertion**: Confirms $\ge 2$ links adjacent to every subtopic and sub-subtopic heading.
  - **Prohibition of Bare Homepages**: Ensures links are deep links to specific lectures, chapters, papers, or tools, rejecting generic domain roots (e.g., `https://ocw.mit.edu/`, `https://www.youtube.com/`, `https://wikipedia.org/`).
  - **Live HTTP Check**: Performs live HTTP `HEAD` / `GET` requests with a standard browser `User-Agent` and connection timeout (10s).
  - Asserts HTTP response status `200` (or valid redirect `301`/`302`/`307`/`308` resolving to `200`).
  - Supports `--skip-network` CLI flag for isolated/air-gapped CI environments.

### 2.5 Tier 5: Adversarial Coverage Hardening
- **Objective**: Guard against facade implementations, synthetic templates, and ast corruption.
- **AST Parsing**: Validates that all Python code blocks parse cleanly with `ast.parse` without syntax errors.
- **Anti-Facade Checks**: Asserts absence of known dummy phrases (`process_critical_payload`, random fuzzing bit mutations, etc.).

---

## 3. Test Runner CLI Interface & Flags

The test suite is encapsulated in `scripts/verify_pilot_011.py`:

```bash
# Full E2E execution (all Tiers 1-4, including live network check)
python scripts/verify_pilot_011.py

# Offline execution (skips live network requests)
python scripts/verify_pilot_011.py --skip-network

# Run a specific tier only
python scripts/verify_pilot_011.py --tier 1
python scripts/verify_pilot_011.py --tier 2
python scripts/verify_pilot_011.py --tier 3
python scripts/verify_pilot_011.py --tier 4

# Output machine-readable JSON report
python scripts/verify_pilot_011.py --json report.json

# Verbose output with full debugging traces
python scripts/verify_pilot_011.py --verbose

# Abort on first detected failure
python scripts/verify_pilot_011.py --fail-fast
```

---

## 4. Pass / Fail Criteria & Exit Codes

| Result | Exit Code | Description | Action Required |
|---|:---:|---|---|
| **SUCCESS** | `0` | 100% of enabled assertions in Tiers 1–4 passed with zero errors. | Topic 011 is certified ready for review and delivery. |
| **FAILURE** | `1` | One or more assertions failed (e.g., missing mandatory element, control character detected, broken link, code execution failure). | Consult the diagnostic failure report, fix defect, and re-run. |

---

## 5. Ecosystem Compatibility Integration

To guarantee that new modular topic structures do not break existing repository governance scripts:
1. `scripts/full_audit.py`: Enhanced to prune subtopic directories inside tier folders, ensuring `assert len(topic_files) == 232` remains satisfied.
2. `scripts/verify_curriculum.py`: Tests `curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md` as the top-level module (size $\ge 500$B, 7 sections).
3. `scripts/verify_ecosystem.py`: Validates all 232 modules, 8 labs, 6 career tracks, 17 drills, 10 flashcard decks, and 0 placeholders across all repository files.
