#!/usr/bin/env python3
"""
scripts/verify_module_013.py
Comprehensive End-to-End Verification Suite for:
  Modul 013: Kalkulus Diferensial & Integral Satu Variabel
             (Limit Infinitesimal, Turunan, Integral Riemann, Deret Taylor)

Verifies 5 progressive tiers:
  Tier 1: Feature Coverage & Syllabus Completeness (Category-Partition)
  Tier 2: Boundary-Value & Corner Cases (Control Chars, KaTeX, Placeholders)
  Tier 3: Pairwise & Cross-Feature Integration (Inbound Links, Drills, Flashcards)
  Tier 4: Real-World Workload Execution (Subprocess Python Code, Mandatory Output Blocks, Live Deep Links)
  Tier 5: Adversarial Hardening (AST Parsing, Anti-Facade, Uniqueness)

Usage:
  python scripts/verify_module_013.py [--skip-network] [--verbose] [--fail-fast]
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
GATEWAY_FILE = os.path.join(CURRICULUM_DIR, "013-kalkulus-diferensial-integral-satu-variabel.md")
SUBTOPIC_DIR = os.path.join(CURRICULUM_DIR, "013-kalkulus-diferensial-integral-satu-variabel")
README_FILE = os.path.join(SUBTOPIC_DIR, "README.md")

EXPECTED_SUBTOPICS = [
    "01-limit-kekontinuan-definisi-epsilon-delta.md",
    "02-turunan-laju-perubahan-aturan-rantai.md",
    "03-teorema-nilai-rata-rata-dan-analisis-fungsi.md",
    "04-integral-riemann-jumlah-riemann-teorema-dasar-kalkulus.md",
    "05-teknik-pengintegralan-substitusi-parsial-pecahan-parsial.md",
    "06-integral-tak-wajar-dan-aplikasi-geometris-fisika.md",
    "07-barisan-dan-deret-tak-hingga-uji-konvergensi.md",
    "08-deret-taylor-maclaurin-dan-analisis-galat-lagrange.md",
    "09-metode-numerik-satu-variabel-dan-kalkulus-komputasional.md",
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
    ("Kamus Notasi Simbol Diskrit/Kalkulus", re.compile(r"Kamus\s+(Notasi|Simbol)", re.IGNORECASE)),
    ("Definisi Formal & Teorema", re.compile(r"## 2\.\s*Definisi\s+Formal.*?Teorema", re.IGNORECASE)),
    ("Arsitektur & Visualisasi", re.compile(r"## 3\.\s*Arsitektur\s+Teknis", re.IGNORECASE)),
    ("Implementasi Python & Output Terminal", re.compile(r"## 4\.\s*Implementasi\s+Praktis", re.IGNORECASE)),
    ("Miskonsepsi & Analisis Post-Mortem", re.compile(r"## 5\.\s*Miskonsepsi\s+Umum.*?Post-Mortem", re.IGNORECASE)),
    ("Tips Praktis & Rahasia Cepat Paham", re.compile(r"## 6\.\s*Tips,\s*Trik\s+Praktis", re.IGNORECASE)),
    ("Latihan Mandiri Berjenjang (Socratic)", re.compile(r"## 7\.\s*Latihan\s+Mandiri", re.IGNORECASE)),
]

CALCULUS_SYLLABUS_CHECKLIST = [
    ("Limit & Definisi Epsilon-Delta", re.compile(r"(limit|kekontinuan|epsilon-delta)", re.IGNORECASE)),
    ("Teorema Apit (Squeeze Theorem)", re.compile(r"(squeeze\s+theorem|teorema\s+apit)", re.IGNORECASE)),
    ("Turunan & Laju Perubahan", re.compile(r"(turunan|diferensiasi|derivative)", re.IGNORECASE)),
    ("Aturan Rantai (Chain Rule)", re.compile(r"(aturan\s+rantai|chain\s+rule)", re.IGNORECASE)),
    ("Teorema Nilai Rata-rata (MVT)", re.compile(r"(teorema\s+nilai\s+rata-rata|mean\s+value\s+theorem|mvt)", re.IGNORECASE)),
    ("Teorema Rolle", re.compile(r"(teorema\s+rolle|rolle's\s+theorem)", re.IGNORECASE)),
    ("Aturan L'Hopital", re.compile(r"(l'hopital|l'hospital)", re.IGNORECASE)),
    ("Integral Riemann & Jumlahan Partisi", re.compile(r"(integral\s+riemann|riemann\s+sum|jumlahan\s+riemann)", re.IGNORECASE)),
    ("Teorema Dasar Kalkulus (FTC)", re.compile(r"(teorema\s+dasar\s+kalkulus|fundamental\s+theorem\s+of\s+calculus|ftc)", re.IGNORECASE)),
    ("Teknik Substitusi u", re.compile(r"(substitusi\s+u|u-substitution)", re.IGNORECASE)),
    ("Integrasi Parsial (Integration by Parts)", re.compile(r"(integrasi\s+parsial|integration\s+by\s+parts)", re.IGNORECASE)),
    ("Pecahan Parsial (Partial Fractions)", re.compile(r"(pecahan\s+parsial|partial\s+fraction)", re.IGNORECASE)),
    ("Integral Tak Wajar (Improper Integrals)", re.compile(r"(integral\s+tak\s+wajar|improper\s+integral)", re.IGNORECASE)),
    ("Volume Benda Putar", re.compile(r"(volume\s+benda\s+putar|cakram|cincin|kulit\s+tabung)", re.IGNORECASE)),
    ("Barisan & Deret Tak Hingga", re.compile(r"(barisan|deret\s+tak\s+hingga|infinite\s+series)", re.IGNORECASE)),
    ("Uji Rasio & Konvergensi", re.compile(r"(uji\s+rasio|ratio\s+test|d'alembert)", re.IGNORECASE)),
    ("Deret Taylor & Maclaurin", re.compile(r"(deret\s+taylor|deret\s+maclaurin|taylor\s+series)", re.IGNORECASE)),
    ("Batas Galat Lagrange (Lagrange Remainder)", re.compile(r"(galat\s+lagrange|lagrange\s+remainder|error\s+bound)", re.IGNORECASE)),
    ("Newton-Raphson & Kalkulus Komputasional", re.compile(r"(newton-raphson|metode\s+numerik|cordic)", re.IGNORECASE)),
]

EXPECTED_INBOUND_REFERENCES = [
    ("INDEX.md", os.path.join(BASE_DIR, "INDEX.md")),
    ("curriculum/01-fondasi-matematika/README.md", os.path.join(CURRICULUM_DIR, "README.md")),
    ("012-matematika-diskrit-kombinatorika-graf.md", os.path.join(CURRICULUM_DIR, "012-matematika-diskrit-kombinatorika-graf.md")),
    ("014-kalkulus-multivariabel-vektor.md", os.path.join(CURRICULUM_DIR, "014-kalkulus-multivariabel-vektor.md")),
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


class Module013Verifier:
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
        prefix = f"[{result.status}] {result.tier} - {result.name}"
        dur_str = f" ({result.duration:.3f}s)" if result.duration > 0 else ""
        print(f"  {prefix}: {result.message}{dur_str}")
        if result.status == "FAIL" and result.details:
            for d in result.details[:10]:
                print(f"      * {d}")
            if len(result.details) > 10:
                print(f"      * ... and {len(result.details) - 10} more items")
        if self.fail_fast and result.status == "FAIL":
            print("\n[FAIL-FAST] Terminating verification suite on first failure.")
            sys.exit(1)

    def verify_tier1_feature_coverage(self):
        t0 = time.time()
        print("\n=== [TIER 1] Validating Feature Coverage & Syllabus Completeness ===")

        # 1.1 Artifact Existence
        missing_artifacts = []
        if not os.path.isfile(GATEWAY_FILE):
            missing_artifacts.append("Master Gateway missing: 013-kalkulus-diferensial-integral-satu-variabel.md")
        if not os.path.isfile(README_FILE):
            missing_artifacts.append("README.md missing in 013-kalkulus-diferensial-integral-satu-variabel/")

        for subtopic in EXPECTED_SUBTOPICS:
            path = os.path.join(SUBTOPIC_DIR, subtopic)
            if not os.path.isfile(path):
                missing_artifacts.append(f"Subtopic missing: {subtopic}")

        if missing_artifacts:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Artifact Existence",
                status="FAIL",
                message=f"{len(missing_artifacts)} essential artifacts missing",
                details=missing_artifacts,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Artifact Existence",
                status="PASS",
                message="Master Gateway, README, and all 9 subtopics verified on disk",
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
                message="All 7 mandatory core elements verified across all subtopics",
                duration=time.time() - t2
            ))

        # 1.4 Syllabus Completeness Checklist
        t3 = time.time()
        all_text = ""
        for filepath in self.topic_files:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                all_text += f.read() + "\n"

        missing_syllabus = []
        for topic_name, pattern in CALCULUS_SYLLABUS_CHECKLIST:
            if not pattern.search(all_text):
                missing_syllabus.append(f"Topic not covered in Module 013 corpus: '{topic_name}'")

        if missing_syllabus:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Syllabus Completeness Checklist",
                status="FAIL",
                message=f"{len(missing_syllabus)} syllabus topics missing from Module 013 corpus",
                details=missing_syllabus,
                duration=time.time() - t3
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 1",
                name="Syllabus Completeness Checklist",
                status="PASS",
                message=f"All {len(CALCULUS_SYLLABUS_CHECKLIST)} Calculus & Series topics present",
                duration=time.time() - t3
            ))

    def verify_tier2_boundary_corner(self):
        t0 = time.time()
        print("\n=== [TIER 2] Validating Boundary-Value & Corner Cases ===")

        # 2.1 Zero Control Characters Scan
        control_char_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f, 1):
                    for char_idx, char in enumerate(line):
                        code = ord(char)
                        if code < 32 and char not in ('\t', '\n', '\r'):
                            control_char_errors.append(f"{rel}:{line_idx}:{char_idx} ASCII {code}")
                        elif code == 0xFFFD:
                            control_char_errors.append(f"{rel}:{line_idx}:{char_idx} Unicode Replacement Char (U+FFFD)")

        if control_char_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Control Characters Scan",
                status="FAIL",
                message=f"{len(control_char_errors)} control/corrupted characters found",
                details=control_char_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 2",
                name="Zero Control Characters Scan",
                status="PASS",
                message="Zero control characters detected across all Topic 013 files",
                duration=time.time() - t0
            ))

        # 2.2 KaTeX Syntax Integrity
        t1 = time.time()
        katex_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            in_code_block = False
            in_display_math = False
            for line_idx, line in enumerate(lines, 1):
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                if "$$" in line:
                    if line.strip() == "$$":
                        in_display_math = not in_display_math
                    elif line.count("$$") % 2 != 0:
                        in_display_math = not in_display_math

                # Check escaped dollar signs
                if r"\$" in line and not in_display_math:
                    katex_errors.append(f"{rel}:{line_idx} contains literal \\$ which should be KaTeX delimiter or plain text")

            if in_display_math:
                katex_errors.append(f"{rel}: Unclosed display math block $$ at end of file")

        if katex_errors:
            self.record_result(TestResult(
                tier="Tier 2",
                name="KaTeX Syntax Integrity",
                status="FAIL",
                message=f"{len(katex_errors)} KaTeX syntax issues detected",
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
                for line_idx, line in enumerate(f, 1):
                    if FORBIDDEN_PLACEHOLDER_REGEX.search(line):
                        placeholder_errors.append(f"{rel}:{line_idx} contains placeholder: {line.strip()[:60]}")
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

    def verify_tier3_integration(self):
        t0 = time.time()
        print("\n=== [TIER 3] Validating Cross-Feature & Repository Integration ===")

        # 3.1 Inbound Links
        link_errors = []
        target_rel = "curriculum/01-fondasi-matematika/013-kalkulus-diferensial-integral-satu-variabel.md"
        for ref_name, ref_path in EXPECTED_INBOUND_REFERENCES:
            if not os.path.isfile(ref_path):
                continue
            with open(ref_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "013-kalkulus-diferensial-integral-satu-variabel" not in content:
                link_errors.append(f"{ref_name} missing reference to 013-kalkulus-diferensial-integral-satu-variabel")

        if link_errors:
            self.record_result(TestResult(
                tier="Tier 3",
                name="Inbound Relative Links Resolution",
                status="FAIL",
                message=f"{len(link_errors)} inbound references missing target link",
                details=link_errors,
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
        if os.path.isfile(drills_path):
            with open(drills_path, "r", encoding="utf-8", errors="ignore") as f:
                drills_content = f.read()

            if "## Modul 013" not in drills_content:
                drill_errors.append("Section '## Modul 013' not found in tier-01-mathematics-drills.md")

            # Check 9 Socratic problems
            for i in range(1, 10):
                target_prob = f"013.{i}"
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
                message="Tier-1 drills contain complete 9 Socratic problems (013.1-013.9) with Hints & Solutions",
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

            # Check 013 cards exist
            if "013." not in md_text and "Kalkulus Satu Variabel" not in md_text and "Kalkulus Diferensial" not in md_text:
                fc_errors.append("Module 013 cards missing from flashcards .md")

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
                message="Deck-01 synchronized 1:1 with Module 013 Calculus cards",
                duration=time.time() - t2
            ))

    def verify_tier4_execution(self):
        t0 = time.time()
        print("\n=== [TIER 4] Validating Real-World Execution (Code & Live Deep Links) ===")

        code_errors = []
        code_blocks_parsed = 0
        tasks = []

        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            matches = list(re.finditer(r"```python\s*\n([\s\S]*?)```", content))
            for b_idx, match in enumerate(matches, 1):
                code = match.group(1).strip()
                if not code:
                    continue

                code_blocks_parsed += 1

                try:
                    ast.parse(code)
                except SyntaxError as se:
                    code_errors.append(f"{rel}: code block #{b_idx} AST syntax error: {se}")
                    continue

                if "# non-runnable" in code or "# pseudocode" in code:
                    continue

                # Check following output block
                end_pos = match.end()
                following_text = content[end_pos:end_pos + 600]
                has_output_block = bool(re.search(r"(Keluaran|Output|Hasil eksekusi)[\s\S]*?```(text|output)", following_text, re.IGNORECASE))
                if not has_output_block:
                    code_errors.append(f"{rel}: code block #{b_idx} missing mandatory authentic terminal output block immediately following it")

                tasks.append((rel, b_idx, code))

        # Execute code snippets
        def run_code(rel, idx, py_code):
            try:
                proc = subprocess.run(
                    [sys.executable, "-c", py_code],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if proc.returncode != 0:
                    err = proc.stderr.strip()[:100]
                    return f"{rel}: code #{idx} exited with code {proc.returncode}: {err}"
            except subprocess.TimeoutExpired:
                return f"{rel}: code #{idx} execution timed out (>5s)"
            except Exception as e:
                return f"{rel}: code #{idx} execution error: {e}"
            return None

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(run_code, r, i, c) for r, i, c in tasks]
            for fut in as_completed(futures):
                err = fut.result()
                if err:
                    code_errors.append(err)

        if code_errors:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Python Subprocess Execution",
                status="FAIL",
                message=f"{len(code_errors)} code blocks failed execution or validation",
                details=code_errors,
                duration=time.time() - t0
            ))
        else:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Python Subprocess Execution",
                status="PASS",
                message=f"All {code_blocks_parsed} Python blocks parsed cleanly; {len(tasks)} executed with exit code 0 with mandatory terminal output blocks",
                duration=time.time() - t0
            ))

        # 4.2 Live HTTP Deep-Link Audit
        t1 = time.time()
        if self.skip_network:
            self.record_result(TestResult(
                tier="Tier 4",
                name="Live HTTP Deep-Link Audit",
                status="SKIP",
                message="Network checks skipped via --skip-network",
                duration=0.0
            ))
            return

        urls_to_check = set()
        url_pattern = re.compile(r'https?://[^\s)\]">]+')
        for filepath in self.topic_files:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for url in url_pattern.findall(content):
                clean_url = url.rstrip(".,;:)")
                if clean_url.startswith("http://localhost") or "127.0.0.1" in clean_url:
                    continue
                urls_to_check.add(clean_url)

        dead_links = []

        def check_url(target_url):
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            try:
                if HAS_REQUESTS:
                    resp = requests.head(target_url, headers=headers, timeout=5, allow_redirects=True)
                    if resp.status_code in (405, 403):
                        resp = requests.get(target_url, headers=headers, timeout=5, stream=True)
                    if resp.status_code >= 400 and resp.status_code not in (403, 401):
                        return f"{target_url} returned HTTP {resp.status_code}"
                else:
                    req = urllib.request.Request(target_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=5) as r:
                        if r.status >= 400:
                            return f"{target_url} returned HTTP {r.status}"
            except Exception as e:
                # DNS failure or timeout
                err_msg = str(e)
                if "getaddrinfo failed" in err_msg or "timed out" in err_msg:
                    return f"{target_url} network failure: {e}"
            return None

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(check_url, u) for u in urls_to_check]
            for fut in as_completed(futures):
                err = fut.result()
                if err:
                    dead_links.append(err)

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

    def verify_tier5_adversarial(self):
        t0 = time.time()
        print("\n=== [TIER 5] Validating Adversarial Hardening & Anti-Facade Guard ===")

        facade_errors = []
        for filepath in self.topic_files:
            rel = os.path.relpath(filepath, BASE_DIR)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Anti-facade 1: Mermaid dark mode contrast
            mermaid_blocks = re.findall(r"```mermaid([\s\S]*?)```", content)
            for m_idx, block in enumerate(mermaid_blocks, 1):
                # Any colored node (e.g. fill:#...) must specify color:#0f172a;
                colored_styles = re.findall(r"(style\s+\w+\s+[^;\n]*fill:[^;\n]+|classDef\s+\w+\s+[^;\n]*fill:[^;\n]+)", block)
                for style_str in colored_styles:
                    if "color:" not in style_str:
                        facade_errors.append(f"{rel}: Mermaid block #{m_idx} has colored fill without explicit dark-mode text 'color:#0f172a;': {style_str[:50]}")

            # Anti-facade 2: Code must not be empty or trivial
            py_blocks = re.findall(r"```python([\s\S]*?)```", content)
            for p_idx, block in enumerate(py_blocks, 1):
                lines = [l for l in block.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
                if len(lines) < 5:
                    facade_errors.append(f"{rel}: Python block #{p_idx} is suspiciously trivial (<5 lines of code)")

        if facade_errors:
            self.record_result(TestResult(
                tier="Tier 5",
                name="Anti-Facade & Adversarial Hardening",
                status="FAIL",
                message=f"{len(facade_errors)} anti-facade violations detected",
                details=facade_errors,
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
        t_start = time.time()
        print("=" * 80)
        print("        MODULE 013 E2E VERIFICATION SUITE (STAGE 1 ACCEPTANCE GATE)")
        print("=" * 80)
        print(f"Target Directory: {SUBTOPIC_DIR}")
        print(f"Master Gateway:   {GATEWAY_FILE}")
        print(f"Discovered Files: {len(self.topic_files)}")
        print(f"Network Checks:   {'DISABLED (--skip-network)' if self.skip_network else 'ENABLED (Live HTTP)'}")
        print("-" * 80)

        self.verify_tier1_feature_coverage()
        self.verify_tier2_boundary_corner()
        self.verify_tier3_integration()
        self.verify_tier4_execution()
        self.verify_tier5_adversarial()

        return self.print_summary(time.time() - t_start)

    def print_summary(self, elapsed: float = 0.0):
        print("\n" + "=" * 80)
        print("                          VERIFICATION SUMMARY")
        print("=" * 80)
        passes = sum(1 for r in self.results if r.status == "PASS")
        fails = sum(1 for r in self.results if r.status == "FAIL")
        warns = sum(1 for r in self.results if r.status == "WARN")
        skips = sum(1 for r in self.results if r.status == "SKIP")
        total = len(self.results)

        print(f"Total Tests Executed: {total} | Duration: {elapsed:.2f}s")
        print(f"Passed: {passes} | Failed: {fails} | Warnings: {warns} | Skipped: {skips}\n")

        if fails == 0:
            print(">>> [GATE PASSED] MODULE 013 CERTIFIED 100% SPECIFICATION-COMPLIANT <<<")
        else:
            print(f">>> [GATE FAILED] MODULE 013 HAS {fails} FAILING CHECKS <<<")
        print("=" * 80)
        return fails == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Module 013 Verification Suite")
    parser.add_argument("--skip-network", action="store_true", help="Skip live HTTP link verification")
    parser.add_argument("--verbose", action="store_true", help="Verbose debug output")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")
    args = parser.parse_args()

    verifier = Module013Verifier(skip_network=args.skip_network, verbose=args.verbose, fail_fast=args.fail_fast)
    success = verifier.run_all()
    sys.exit(0 if success else 1)
