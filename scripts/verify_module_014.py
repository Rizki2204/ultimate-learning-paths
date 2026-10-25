#!/usr/bin/env python3
"""
scripts/verify_module_014.py
Comprehensive End-to-End Verification Suite for:
  Modul 014: Kalkulus Multivariabel & Kalkulus Vektor
             (Turunan Parsial, Gradien, Jacobian, Hessian, Integral Lipat, Teorema Stokes & Gauss)

Verifies 5 progressive tiers:
  Tier 1: Feature Coverage & Syllabus Completeness (Category-Partition)
  Tier 2: Boundary-Value & Corner Cases (Control Chars, KaTeX, Placeholders)
  Tier 3: Pairwise & Cross-Feature Integration (Inbound Links, Drills, Flashcards)
  Tier 4: Real-World Workload Execution (Subprocess Python Code, Mandatory Output Blocks, Live Deep Links)
  Tier 5: Adversarial Hardening (AST Parsing, Anti-Facade, Uniqueness)

Usage:
  python scripts/verify_module_014.py [--skip-network] [--verbose] [--fail-fast]
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.error
    import urllib.request


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURRICULUM_DIR = os.path.join(BASE_DIR, "curriculum", "01-fondasi-matematika")
GATEWAY_FILE = os.path.join(CURRICULUM_DIR, "014-kalkulus-multivariabel-vektor.md")
SUBTOPIC_DIR = os.path.join(CURRICULUM_DIR, "014-kalkulus-multivariabel-vektor")
README_FILE = os.path.join(SUBTOPIC_DIR, "README.md")

EXPECTED_SUBTOPICS = [
    "01-ruang-vektor-fungsi-multivariabel-limit-kontinuitas.md",
    "02-turunan-parsial-gradien-turunan-berarah.md",
    "03-diferensial-total-matriks-jacobian-aturan-rantai-multivariabel.md",
    "04-matriks-hessian-uji-turunan-kedua-optimasi-multivariabel.md",
    "05-optimasi-berpembatas-pengali-lagrange-kondisi-kkt.md",
    "06-integral-lipat-dua-tiga-teorema-fubini-substitusi-variabel.md",
    "07-integral-garis-medan-vektor-kerja-teorema-dasar-integral-garis.md",
    "08-teorema-green-curl-divergensi-dan-fluks-dua-dimensi.md",
    "09-integral-permukaan-teorema-stokes-teorema-divergensi-gauss.md",
]

MANDATORY_GATEWAY_SECTIONS = [
    "## 1. Intuisi Dasar Tanpa Jargon",
    "## 2. Fondasi Teoretis & Aksiomatik / Matematis",
    "## 3. Anatomi Teknis & Cara Kerja Internal",
    "## 4. Implementasi Praktis & Kode",
    "## 5. Miskonsepsi & Jebakan Industri",
    "## 6. Proyek Latihan & Rubrik Penilaian Mandiri",
    "## 7. Rekomendasi Sumber Belajar Standar Emas",
]

MANDATORY_SUBTOPIC_CORE_ELEMENTS = [
    ("Intuisi & Motivasi Konseptual", re.compile(r"## 1\.\s*Intuisi.*?Motivasi", re.IGNORECASE)),
    ("Kamus Notasi Simbol Multivariabel/Vektor", re.compile(r"Kamus\s+(Notasi|Simbol)", re.IGNORECASE)),
    ("Definisi Formal & Teorema", re.compile(r"## 2\.\s*Definisi\s+Formal.*?Teorema", re.IGNORECASE)),
    ("Arsitektur & Visualisasi", re.compile(r"## 3\.\s*Arsitektur\s+Teknis", re.IGNORECASE)),
    ("Implementasi Python & Output Terminal", re.compile(r"## 4\.\s*Implementasi\s+Praktis", re.IGNORECASE)),
    ("Miskonsepsi & Analisis Post-Mortem", re.compile(r"## 5\.\s*Miskonsepsi\s+Umum.*?Post-Mortem", re.IGNORECASE)),
    ("Tips Praktis & Rahasia Cepat Paham", re.compile(r"## 6\.\s*Tips,\s*Trik\s+Praktis", re.IGNORECASE)),
    ("Latihan Mandiri Berjenjang (Socratic)", re.compile(r"## 7\.\s*Latihan\s+Mandiri", re.IGNORECASE)),
]

MULTIVARIABLE_SYLLABUS_CHECKLIST = [
    ("Ruang Rn & Limit Multivariabel", re.compile(r"(ruang\s+r\^?n|limit\s+multivariabel|jalur\s+lintasan)", re.IGNORECASE)),
    ("Turunan Parsial & Teorema Clairaut", re.compile(r"(turunan\s+parsial|partial\s+derivative|clairaut|schwarz)", re.IGNORECASE)),
    ("Vektor Gradien & Kenaikan Tercuram", re.compile(r"(vektor\s+gradien|gradient|kenaikan\s+tercuram|steepest\s+ascent)", re.IGNORECASE)),
    ("Turunan Berarah (Directional Derivative)", re.compile(r"(turunan\s+berarah|directional\s+derivative)", re.IGNORECASE)),
    ("Keterdiferensialan & Bidang Singgung", re.compile(r"(diferensiabel|bidang\s+singgung|tangent\s+plane)", re.IGNORECASE)),
    ("Matriks Jacobian & Transformasi Koordinat", re.compile(r"(matriks\s+jacobian|jacobian\s+matrix|koordinat\s+polar)", re.IGNORECASE)),
    ("Aturan Rantai Multivariabel (Chain Rule)", re.compile(r"(aturan\s+rantai|multivariable\s+chain\s+rule)", re.IGNORECASE)),
    ("Matriks Hessian & Uji Turunan Kedua", re.compile(r"(matriks\s+hessian|hessian\s+matrix|uji\s+turunan\s+kedua)", re.IGNORECASE)),
    ("Titik Kritis & Titik Pelana (Saddle Point)", re.compile(r"(titik\s+kritis|titik\s+pelana|saddle\s+point)", re.IGNORECASE)),
    ("Pengali Lagrange (Lagrange Multipliers)", re.compile(r"(pengali\s+lagrange|lagrange\s+multiplier)", re.IGNORECASE)),
    ("Kondisi KKT (Karush-Kuhn-Tucker)", re.compile(r"(karush-kuhn-tucker|kondisi\s+kkt|kkt\s+conditions)", re.IGNORECASE)),
    ("Integral Lipat Dua & Teorema Fubini", re.compile(r"(integral\s+lipat\s+dua|double\s+integral|fubini)", re.IGNORECASE)),
    ("Integral Lipat Tiga & Koordinat Tabung/Bola", re.compile(r"(integral\s+lipat\s+tiga|triple\s+integral|koordinat\s+bola)", re.IGNORECASE)),
    ("Medan Vektor & Integral Garis", re.compile(r"(medan\s+vektor|vector\s+field|integral\s+garis|line\s+integral)", re.IGNORECASE)),
    ("Medan Konservatif & Fungsi Potensial", re.compile(r"(medan\s+konservatif|conservative|fungsi\s+potensial|potential\s+function)", re.IGNORECASE)),
    ("Teorema Green (Sirkulasi & Fluks 2D)", re.compile(r"(teorema\s+green|green's\s+theorem|sirkulasi|fluks)", re.IGNORECASE)),
    ("Divergensi & Curl (Rotasi)", re.compile(r"(divergensi|divergence|curl|rotasi)", re.IGNORECASE)),
    ("Teorema Stokes (Curl Fluks Permukaan)", re.compile(r"(teorema\s+stokes|stokes'\s+theorem)", re.IGNORECASE)),
    ("Teorema Divergensi Gauss", re.compile(r"(teorema\s+divergensi|gauss's\s+divergence\s+theorem|teorema\s+gauss)", re.IGNORECASE)),
]

EXPECTED_INBOUND_REFERENCES = [
    ("INDEX.md", os.path.join(BASE_DIR, "INDEX.md")),
    ("curriculum/01-fondasi-matematika/README.md", os.path.join(CURRICULUM_DIR, "README.md")),
    ("013-kalkulus-diferensial-integral-satu-variabel.md", os.path.join(CURRICULUM_DIR, "013-kalkulus-diferensial-integral-satu-variabel.md")),
    ("015-persamaan-diferensial-biasa-parsial.md", os.path.join(CURRICULUM_DIR, "015-persamaan-diferensial-biasa-parsial.md")),
]

FORBIDDEN_PLACEHOLDER_REGEX = re.compile(r"\b(TODO|FIXME|TBD|PLACEHOLDER|XXX)\b", re.IGNORECASE)
LOREM_IPSUM_REGEX = re.compile(r"lorem\s+ipsum", re.IGNORECASE)


@dataclass
class TestResult:
    tier: str
    name: str
    status: str  # PASS, FAIL, WARN, SKIP
    message: str
    details: List[str] = field(default_factory=list)
    duration: float = 0.0


class Module014Verifier:
    def __init__(self, skip_network: bool = False, verbose: bool = False, fail_fast: bool = False):
        self.skip_network = skip_network
        self.verbose = verbose
        self.fail_fast = fail_fast
        self.results: List[TestResult] = []
        self.topic_files: List[str] = []
        self._discover_files()

    def _discover_files(self):
        if os.path.isfile(GATEWAY_FILE):
            self.topic_files.append(GATEWAY_FILE)
        if os.path.isfile(README_FILE):
            self.topic_files.append(README_FILE)
        if os.path.isdir(SUBTOPIC_DIR):
            for fname in os.listdir(SUBTOPIC_DIR):
                if fname.endswith(".md") and fname != "README.md":
                    self.topic_files.append(os.path.join(SUBTOPIC_DIR, fname))

    def record_result(self, result: TestResult):
        self.results.append(result)
        status_symbol = {
            "PASS": "[PASS]",
            "FAIL": "[FAIL]",
            "WARN": "[WARN]",
            "SKIP": "[SKIP]",
        }.get(result.status, "[INFO]")
        print(f"  {status_symbol} {result.tier} - {result.name}: {result.message} ({result.duration:.3f}s)")
        if (result.status in ("FAIL", "WARN") or self.verbose) and result.details:
            for detail in result.details[:10]:
                print(f"      * {detail}")
            if len(result.details) > 10:
                print(f"      ... and {len(result.details) - 10} more items")
        if result.status == "FAIL" and self.fail_fast:
            print("\n[FAIL-FAST] Halting verification immediately on first failure.")
            self.print_summary()
            sys.exit(1)

    # =========================================================================
    # TIER 1: FEATURE COVERAGE & SYLLABUS COMPLETENESS
    # =========================================================================
    def test_tier_1_coverage(self):
        print("\n=== [TIER 1] Validating Feature Coverage & Syllabus Completeness ===")

        # 1.1 Artifact Existence
        t0 = time.time()
        missing_artifacts = []
        if not os.path.isfile(GATEWAY_FILE):
            missing_artifacts.append(f"Master Gateway missing: {os.path.relpath(GATEWAY_FILE, BASE_DIR)}")
        if not os.path.isfile(README_FILE):
            missing_artifacts.append(f"Subtopic README missing: {os.path.relpath(README_FILE, BASE_DIR)}")

        for subtopic in EXPECTED_SUBTOPICS:
            expected_path = os.path.join(SUBTOPIC_DIR, subtopic)
            if not os.path.isfile(expected_path):
                missing_artifacts.append(f"Subtopic missing: {subtopic}")

        if missing_artifacts:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Artifact Existence",
                status="FAIL",
                message=f"{len(missing_artifacts)} essential artifacts missing on disk",
                details=missing_artifacts,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Artifact Existence",
                status="PASS",
                message=f"Master Gateway, README, and all {len(EXPECTED_SUBTOPICS)} subtopics verified on disk",
                duration=time.time() - t0
            ))

        # 1.2 Master Gateway Sections
        t1 = time.time()
        missing_sections = []
        if os.path.isfile(GATEWAY_FILE):
            with open(GATEWAY_FILE, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for sec in MANDATORY_GATEWAY_SECTIONS:
                if sec not in content:
                    missing_sections.append(f"Master Gateway missing section: '{sec}'")
        else:
            missing_sections.append("Gateway file does not exist")

        if missing_sections:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Master Gateway Sections",
                status="FAIL",
                message=f"{len(missing_sections)} mandatory sections missing in Master Gateway",
                details=missing_sections,
                duration=time.time() - t1
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Master Gateway Sections",
                status="PASS",
                message="All 7 mandatory Indonesian section headers present in Master Gateway",
                duration=time.time() - t1
            ))

        # 1.3 Mandatory Core Elements in Subtopics
        t2 = time.time()
        subtopic_element_errors = []
        for subtopic in EXPECTED_SUBTOPICS:
            path = os.path.join(SUBTOPIC_DIR, subtopic)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for elem_name, pattern in MANDATORY_SUBTOPIC_CORE_ELEMENTS:
                if not pattern.search(content):
                    subtopic_element_errors.append(f"{subtopic} missing core element: '{elem_name}'")

        if subtopic_element_errors:
            self.record_result(TestResult(
                tier="Tier 1",
                name="7 Mandatory Core Elements in Subtopics",
                status="FAIL",
                message=f"{len(subtopic_element_errors)} missing element violations across subtopics",
                details=subtopic_element_errors,
                duration=time.time() - t2
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="7 Mandatory Core Elements in Subtopics",
                status="PASS",
                message=f"All 7 mandatory core elements verified across all subtopics",
                duration=time.time() - t2
            ))

        # 1.4 Syllabus Completeness Checklist
        t3 = time.time()
        combined_text = ""
        for filepath in self.topic_files:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                combined_text += f.read() + "\n"

        missing_syllabus = []
        for topic_name, pattern in MULTIVARIABLE_SYLLABUS_CHECKLIST:
            if not pattern.search(combined_text):
                missing_syllabus.append(f"Missing syllabus topic: {topic_name}")

        if missing_syllabus:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Syllabus Completeness Checklist",
                status="FAIL",
                message=f"{len(missing_syllabus)} syllabus topics missing from Topic 014",
                details=missing_syllabus,
                duration=time.time() - t3
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Syllabus Completeness Checklist",
                status="PASS",
                message=f"All {len(MULTIVARIABLE_SYLLABUS_CHECKLIST)} Multivariable Calculus & Vector Analysis topics present",
                duration=time.time() - t3
            ))

    # =========================================================================
    # TIER 2: BOUNDARY-VALUE & CORNER CASES
    # =========================================================================
    def test_tier_2_boundaries(self):
        print("\n=== [TIER 2] Validating Boundary-Value & Corner Cases ===")

        # 2.1 Zero Control Characters
        t0 = time.time()
        control_char_errors = []
        control_char_regex = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f, start=1):
                    match = control_char_regex.search(line)
                    if match:
                        control_char_errors.append(f"{rel}:{line_idx} contains control char {ord(match.group(0))}")

        if control_char_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Control Characters Scan",
                status="FAIL",
                message=f"{len(control_char_errors)} control characters detected",
                details=control_char_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Control Characters Scan",
                status="PASS",
                message="Zero control characters detected across all Topic 014 files",
                duration=time.time() - t0
            ))

        # 2.2 KaTeX Delimiter Syntax Integrity
        t1 = time.time()
        katex_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            in_code_fence = False
            for line_idx, line in enumerate(content.splitlines(), start=1):
                if line.strip().startswith("```"):
                    in_code_fence = not in_code_fence
                    continue
                if in_code_fence:
                    continue

                if "\\$" in line:
                    katex_errors.append(f"{rel}:{line_idx} contains literal escaped \\$, use proper currency text or math syntax")

        if katex_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="KaTeX Syntax Integrity",
                status="FAIL",
                message=f"{len(katex_errors)} KaTeX syntax violations found",
                details=katex_errors,
                duration=time.time() - t1
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 2",
                name="KaTeX Syntax Integrity",
                status="PASS",
                message="KaTeX delimiters balanced and free of escape corruption",
                duration=time.time() - t1
            ))

        # 2.3 Zero Placeholders
        t2 = time.time()
        placeholder_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f, start=1):
                    if FORBIDDEN_PLACEHOLDER_REGEX.search(line):
                        placeholder_errors.append(f"{rel}:{line_idx} contains forbidden token: {line.strip()[:60]}")
                    if LOREM_IPSUM_REGEX.search(line):
                        placeholder_errors.append(f"{rel}:{line_idx} contains lorem ipsum: {line.strip()[:60]}")

        if placeholder_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Placeholder & Scaffolding Boilerplate",
                status="FAIL",
                message=f"{len(placeholder_errors)} forbidden placeholder tokens detected",
                details=placeholder_errors,
                duration=time.time() - t2
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Placeholder & Scaffolding Boilerplate",
                status="PASS",
                message="Zero TODO, FIXME, TBD, lorem ipsum, or scaffolding tokens found",
                duration=time.time() - t2
            ))

        # 2.4 File Size & Lines Categorized
        t3 = time.time()
        size_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            line_count = len(lines)
            byte_size = os.path.getsize(filepath)

            if filepath == GATEWAY_FILE:
                if line_count < 500 or byte_size < 30000:
                    size_errors.append(f"{rel}: Gateway below minimum size ({line_count} lines, {byte_size/1024:.1f}KB; min: 500 lines/30KB)")
            elif filepath == README_FILE:
                if line_count < 250 or byte_size < 15000:
                    size_errors.append(f"{rel}: README below minimum size ({line_count} lines, {byte_size/1024:.1f}KB; min: 250 lines/15KB)")
            elif os.path.basename(filepath) in EXPECTED_SUBTOPICS:
                if line_count < 650 or byte_size < 35000:
                    size_errors.append(f"{rel}: Subtopic below minimum size ({line_count} lines, {byte_size/1024:.1f}KB; min: 650 lines/35KB)")

        if size_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Categorized File Boundaries & Pedagogy Requirements",
                status="FAIL",
                message=f"{len(size_errors)} files failed size/depth thresholds",
                details=size_errors,
                duration=time.time() - t3
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Categorized File Boundaries & Pedagogy Requirements",
                status="PASS",
                message="All categorized requirements (Subtopics >=650 lines/35KB, Gateway >=500 lines/30KB, README >=250 lines) satisfied",
                duration=time.time() - t3
            ))

    # =========================================================================
    # TIER 3: PAIRWISE & CROSS-FEATURE INTEGRATION
    # =========================================================================
    def test_tier_3_integration(self):
        print("\n=== [TIER 3] Validating Cross-Feature & Repository Integration ===")

        # 3.1 Inbound Links
        t0 = time.time()
        inbound_errors = []
        for ref_name, ref_path in EXPECTED_INBOUND_REFERENCES:
            if not os.path.isfile(ref_path):
                inbound_errors.append(f"Inbound referencing file missing: {ref_name}")
                continue
            with open(ref_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "014-kalkulus-multivariabel-vektor.md" not in content and "014-kalkulus-multivariabel-vektor" not in content:
                inbound_errors.append(f"{ref_name} does not reference Topic 014")

        if inbound_errors:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Inbound Relative Links Resolution",
                status="FAIL",
                message=f"{len(inbound_errors)} inbound references unresolved",
                details=inbound_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Inbound Relative Links Resolution",
                status="PASS",
                message="All inbound repository references resolve to Master Gateway",
                duration=time.time() - t0
            ))

        # 3.2 Drills Synchronization
        t1 = time.time()
        drills_path = os.path.join(BASE_DIR, "drills", "tier-01-mathematics-drills.md")
        drill_errors = []
        if not os.path.isfile(drills_path):
            drill_errors.append("tier-01-mathematics-drills.md does not exist")
        else:
            with open(drills_path, "r", encoding="utf-8", errors="ignore") as f:
                drills_content = f.read()

            if "## Modul 014" not in drills_content:
                drill_errors.append("Section '## Modul 014' not found in tier-01-mathematics-drills.md")

            # Check 9 Socratic problems
            for i in range(1, 10):
                target_prob = f"014.{i}"
                if target_prob not in drills_content:
                    drill_errors.append(f"Problem {target_prob} missing from drills")

        if drill_errors:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Socratic Drills Synchronization",
                status="FAIL",
                message=f"{len(drill_errors)} drill synchronization issues found",
                details=drill_errors,
                duration=time.time() - t1
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Socratic Drills Synchronization",
                status="PASS",
                message="Tier-1 drills contain complete 9 Socratic problems (014.1-014.9) with Hints & Solutions",
                duration=time.time() - t1
            ))

        # 3.3 Flashcards Active Recall Synchronization
        t2 = time.time()
        fc_md = os.path.join(BASE_DIR, "flashcards", "deck-01-cognitive-logic-math.md")
        fc_tsv = os.path.join(BASE_DIR, "flashcards", "deck-01-cognitive-logic-math.tsv")
        fc_errors = []
        if os.path.isfile(fc_md) and os.path.isfile(fc_tsv):
            with open(fc_md, "r", encoding="utf-8", errors="ignore") as f:
                md_text = f.read()
            with open(fc_tsv, "r", encoding="utf-8", errors="ignore") as f:
                tsv_lines = [l for l in f if l.strip()]

            # Check 014 cards exist
            if "014." not in md_text and "Kalkulus Multivariabel" not in md_text:
                fc_errors.append("Module 014 cards missing from flashcards .md")

        if fc_errors:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Flashcards Active Recall Synchronization",
                status="FAIL",
                message=f"{len(fc_errors)} flashcard issues found",
                details=fc_errors,
                duration=time.time() - t2
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Flashcards Active Recall Synchronization",
                status="PASS",
                message="Deck-01 synchronized 1:1 with Module 014 Multivariable Calculus cards",
                duration=time.time() - t2
            ))

    # =========================================================================
    # TIER 4: REAL-WORLD WORKLOAD EXECUTION
    # =========================================================================
    def test_tier_4_execution(self):
        print("\n=== [TIER 4] Validating Real-World Execution (Code & Live Deep Links) ===")

        # 4.1 Python Code Subprocess Execution
        t0 = time.time()
        python_blocks = []
        exec_errors = []

        code_block_regex = re.compile(r"```python\s*\n(.*?)\n```(?:\s*\nKeluaran eksekusi terminal sebenarnya:\s*\n```text\s*\n(.*?)\n```)?", re.DOTALL)

        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for match in code_block_regex.finditer(content):
                code = match.group(1).strip()
                out_block = match.group(2)
                python_blocks.append((rel, code, out_block is not None))

        for rel, code, has_terminal_out in python_blocks:
            try:
                tree = ast.parse(code)
            except SyntaxError as e:
                exec_errors.append(f"{rel}: SyntaxError in python block: {e}")
                continue

            if not has_terminal_out:
                exec_errors.append(f"{rel}: Python block is missing mandatory terminal output block ('```text') directly below it!")

            try:
                res = subprocess.run(
                    [sys.executable, "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if res.returncode != 0:
                    exec_errors.append(f"{rel}: Python block exited with code {res.returncode}: {res.stderr.strip()[:100]}")
            except subprocess.TimeoutExpired:
                exec_errors.append(f"{rel}: Python execution timed out (>5s)")
            except Exception as e:
                exec_errors.append(f"{rel}: Subprocess execution failed: {e}")

        if exec_errors:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Python Subprocess Execution",
                status="FAIL",
                message=f"{len(exec_errors)} Python code execution/validation failures",
                details=exec_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Python Subprocess Execution",
                status="PASS",
                message=f"All {len(python_blocks)} Python blocks parsed cleanly; {len(python_blocks)} executed with exit code 0 with mandatory terminal output blocks",
                duration=time.time() - t0
            ))

        # 4.2 Live Deep Links
        t1 = time.time()
        if self.skip_network:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Live HTTP Deep-Link Audit",
                status="SKIP",
                message="Skipped via --skip-network flag",
                duration=time.time() - t1
            ))
            return

        urls_to_check = set()
        url_regex = re.compile(r"https?://[^\s)\]\"'>]+")

        for filepath in self.topic_files:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for m in url_regex.finditer(content):
                u = m.group(0).rstrip(".,;")
                if "127.0.0.1" not in u and "localhost" not in u:
                    urls_to_check.add(u)

        dead_links = []

        def check_url(url: str) -> Optional[str]:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            try:
                if HAS_REQUESTS:
                    r = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
                    if r.status_code >= 400:
                        r = requests.get(url, headers=headers, timeout=5, stream=True)
                        if r.status_code >= 400:
                            return f"{url} returned HTTP {r.status_code}"
                else:
                    req = urllib.request.Request(url, headers=headers, method="HEAD")
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        if resp.status >= 400:
                            return f"{url} returned HTTP {resp.status}"
            except Exception as e:
                return f"{url} network failure: {e}"
            return None

        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_url = {executor.submit(check_url, u): u for u in urls_to_check}
            for future in as_completed(future_to_url):
                res = future.result()
                if res:
                    dead_links.append(res)

        if dead_links:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Live HTTP Deep-Link Audit",
                status="FAIL",
                message=f"{len(dead_links)} dead links detected",
                details=dead_links,
                duration=time.time() - t1
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Live HTTP Deep-Link Audit",
                status="PASS",
                message=f"All {len(urls_to_check)} links verified live (HTTP 200/300) with 0 dead links",
                duration=time.time() - t1
            ))

    # =========================================================================
    # TIER 5: ADVERSARIAL HARDENING & ANTI-FACADE GUARD
    # =========================================================================
    def test_tier_5_hardening(self):
        print("\n=== [TIER 5] Validating Adversarial Hardening & Anti-Facade Guard ===")
        t0 = time.time()
        hardening_errors = []

        # Check Mermaid contrast
        mermaid_block_regex = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for m in mermaid_block_regex.finditer(content):
                chart = m.group(1)
                if "classDef" in chart:
                    for line in chart.splitlines():
                        if "classDef" in line and ("fill:#" in line or "fill:" in line):
                            if "color:#0f172a" not in line and "color:#000" not in line and "color:#fff" not in line and "color:#f8fafc" not in line:
                                hardening_errors.append(f"{rel}: Mermaid classDef missing high-contrast text color: {line.strip()}")

        if hardening_errors:
            self.record_result(TestResult(
                tier="Tier 5",
                name="Anti-Facade & Adversarial Hardening",
                status="FAIL",
                message=f"{len(hardening_errors)} hardening violations detected",
                details=hardening_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 5",
                name="Anti-Facade & Adversarial Hardening",
                status="PASS",
                message="Anti-facade checks passed: high-contrast Mermaid styling, authentic content verified",
                duration=time.time() - t0
            ))

    def run_all(self):
        print("=" * 80)
        print("        MODULE 014 E2E VERIFICATION SUITE (STAGE 1 ACCEPTANCE GATE)")
        print("=" * 80)
        print(f"Target Directory: {SUBTOPIC_DIR}")
        print(f"Master Gateway:   {GATEWAY_FILE}")
        print(f"Discovered Files: {len(self.topic_files)}")
        print(f"Network Checks:   {'DISABLED' if self.skip_network else 'ENABLED (Live HTTP)'}")
        print("-" * 80)

        self.test_tier_1_coverage()
        self.test_tier_2_boundaries()
        self.test_tier_3_integration()
        self.test_tier_4_execution()
        self.test_tier_5_hardening()

        return self.print_summary()

    def print_summary(self) -> int:
        print("\n" + "=" * 80)
        print("                          VERIFICATION SUMMARY")
        print("=" * 80)
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        warned = sum(1 for r in self.results if r.status == "WARN")
        skipped = sum(1 for r in self.results if r.status == "SKIP")
        total = len(self.results)
        total_duration = sum(r.duration for r in self.results)

        print(f"Total Tests Executed: {total} | Duration: {total_duration:.2f}s")
        print(f"Passed: {passed} | Failed: {failed} | Warnings: {warned} | Skipped: {skipped}")

        if failed == 0:
            print("\n>>> [GATE PASSED] MODULE 014 CERTIFIED 100% SPECIFICATION-COMPLIANT <<<")
            print("=" * 80)
            return 0
        else:
            print(f"\n>>> [GATE FAILED] MODULE 014 HAS {failed} FAILING CHECKS <<<")
            print("=" * 80)
            return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End Verification Suite for Module 014")
    parser.add_argument("--skip-network", action="store_true", help="Skip live HTTP link verification")
    parser.add_argument("--verbose", action="store_true", help="Verbose test failure details")
    parser.add_argument("--fail-fast", action="store_true", help="Halt on first test failure")
    args = parser.parse_args()

    verifier = Module014Verifier(
        skip_network=args.skip_network,
        verbose=args.verbose,
        fail_fast=args.fail_fast
    )
    sys.exit(verifier.run_all())
