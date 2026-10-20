#!/usr/bin/env python3
# scripts/verify_ecosystem.py
"""
Ultimate Learning Paths - Automated Ecosystem Verification Suite (E2E)
Validates all 6 architectural phases across the repository:
  Phase 1: Curriculum & Legacy Structure Integrity (232 topics, 17 tiers, 7 sections, legacy preservation)
  Phase 2: 8 Flagship Laboratories Discovery & Automated Unit Test Execution
  Phase 3: 6 Career Tracks & Cross-Link Resolution (24-week progression, 4-tier rubrics, link integrity)
  Phase 4: Socratic Diagnostic Drills & Technical Interview Simulations (collapsible keys, link integrity)
  Phase 5: Spaced-Repetition Active Recall Flashcards (TSV 3-column, cloze regex, 5 mandatory categories)
  Phase 6: Zero-Placeholder & Cleanliness Audit (TODO, FIXME, TBD, lorem ipsum, PLACEHOLDER, XXX)

Dual-mode execution:
  - Standalone CLI: python scripts/verify_ecosystem.py [--phase <1-6>] [--verbose] [--fail-fast]
  - Standard unittest: python -m unittest scripts.verify_ecosystem
"""

import argparse
import dataclasses
import os
import re
import subprocess
import sys
import time
import unittest
import urllib.parse
from typing import Dict, List, Optional, Set, Tuple

# Ensure stdout/stderr handle UTF-8 cleanly on Windows consoles
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from scripts.tier_definitions import TIERS, TOPICS_METADATA
except ImportError:
    TIERS = []
    TOPICS_METADATA = []


@dataclasses.dataclass
class TestResult:
    phase: int
    name: str
    passed: bool
    duration: float
    details: str = ""
    errors: List[str] = dataclasses.field(default_factory=list)
    warnings: List[str] = dataclasses.field(default_factory=list)


class EcosystemVerifier:
    def __init__(self, verbose: bool = False, fail_fast: bool = False):
        self.base_dir = BASE_DIR
        self.verbose = verbose
        self.fail_fast = fail_fast
        self.results: List[TestResult] = []
        self.total_errors: List[str] = []
        self.total_warnings: List[str] = []

    def log(self, msg: str):
        print(msg)

    def log_verbose(self, msg: str):
        if self.verbose:
            print(f"    [DEBUG] {msg}")

    # =========================================================================
    # Phase 1: Curriculum & Legacy Structure Integrity
    # =========================================================================
    def verify_phase_1_curriculum(self) -> TestResult:
        start_time = time.time()
        phase = 1
        name = "Curriculum & Legacy Structure Integrity"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 1/6] Validating Curriculum & Legacy Structure Integrity...")

        # 1.1 Legacy Preservation
        docs_dir = os.path.join(self.base_dir, "docs")
        domains_dir = os.path.join(self.base_dir, "domains")

        if not os.path.isdir(docs_dir):
            errors.append("Legacy directory 'docs/' not found!")
        if not os.path.isdir(domains_dir):
            errors.append("Legacy directory 'domains/' not found!")
        else:
            domain_count = len(os.listdir(domains_dir))
            if domain_count < 10:
                errors.append(f"Legacy directory 'domains/' has only {domain_count} files (expected > 10)!")
            else:
                self.log_verbose(f"Legacy preservation verified: {domain_count} domain files found.")

        # 1.2 17 Tier Directories & 17 Tier READMEs
        curriculum_dir = os.path.join(self.base_dir, "curriculum")
        if not os.path.isdir(curriculum_dir):
            errors.append("Directory 'curriculum/' not found!")
        elif not TIERS:
            errors.append("TIERS metadata could not be imported from scripts.tier_definitions!")
        else:
            for tier in TIERS:
                t_dir = os.path.join(curriculum_dir, tier["dir_name"])
                if not os.path.isdir(t_dir):
                    errors.append(f"Tier directory missing: {tier['dir_name']}")
                    continue
                readme_path = os.path.join(t_dir, "README.md")
                if not os.path.isfile(readme_path):
                    errors.append(f"Tier README missing in: {tier['dir_name']}")
                elif os.path.getsize(readme_path) < 200:
                    errors.append(f"Tier README too small in {tier['dir_name']} ({os.path.getsize(readme_path)} bytes)")

        # 1.3 232 Topic Modules Validation
        mandatory_sections = [
            "## 1. Intuisi Dasar Tanpa Jargon",
            "## 2. Fondasi Teoretis & Aksiomatik",
            "## 3. Anatomi Teknis & Cara Kerja Internal",
            "## 4. Implementasi Praktis & Kode",
            "## 5. Miskonsepsi & Jebakan Industri",
            "## 6. Proyek Latihan & Rubrik Penilaian Mandiri",
            "## 7. Rekomendasi Sumber Belajar Standar Emas",
        ]

        if len(TOPICS_METADATA) != 232:
            errors.append(f"TOPICS_METADATA count mismatch: expected 232, got {len(TOPICS_METADATA)}")

        for t_id, slug, full_title, tier_idx in TOPICS_METADATA:
            if tier_idx >= len(TIERS):
                errors.append(f"Invalid tier_idx {tier_idx} for topic {t_id:03d}-{slug}")
                continue
            tier = TIERS[tier_idx]
            filename = f"{t_id:03d}-{slug}.md"
            filepath = os.path.join(self.base_dir, "curriculum", tier["dir_name"], filename)

            if not os.path.isfile(filepath):
                errors.append(f"Missing topic file: curriculum/{tier['dir_name']}/{filename}")
                continue

            size = os.path.getsize(filepath)
            if size < 500:
                errors.append(f"Topic {filename} is corrupted or empty ({size} bytes)")
                continue
            elif size < 4000:
                warnings.append(f"Topic {filename} size ({size} bytes) is below recommended 4000 bytes.")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Cannot read topic {filename}: {e}")
                continue

            # Check 7 mandatory sections
            for sec in mandatory_sections:
                if sec not in content:
                    errors.append(f"Topic {filename} missing mandatory section: '{sec}'")

            # Check mermaid diagram
            if "```mermaid" not in content:
                errors.append(f"Topic {filename} missing Mermaid diagram (```mermaid)")

            # Check code block
            has_code = False
            for lang in ["python", "c", "cpp", "rust", "verilog", "sql", "bash", "assembly", "text", ""]:
                fence = f"```{lang}"
                if fence in content:
                    has_code = True
                    break
            if not has_code:
                errors.append(f"Topic {filename} missing valid fenced code block")

            # Check KaTeX math
            if "$" not in content:
                errors.append(f"Topic {filename} missing KaTeX math notation ($)")

            # Check verified external links
            links = re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", content)
            if len(links) < 3:
                errors.append(f"Topic {filename} has insufficient verified links ({len(links)} links found, >= 3 required)")

            # Check empty links
            empty_links = re.findall(r"\[([^\]]+)\]\(\s*\)", content)
            if empty_links:
                errors.append(f"Topic {filename} has empty markdown links: {empty_links}")

            # Anti-facade integrity checks
            if "process_critical_payload" in content:
                errors.append(f"INTEGRITY VIOLATION in {filename}: dummy snippet 'process_critical_payload' detected")
            if tier_idx not in [4, 5] and "IR = 0xEA00_0010" in content:
                errors.append(f"INTEGRITY VIOLATION in {filename}: CPU instruction register trace detected in non-hardware domain")
            if "16 thread pekerja paralel yang secara serempak" in content:
                errors.append(f"INTEGRITY VIOLATION in {filename}: generic boilerplate exercise detected")
            if re.search(r"```python\s*(?:/\*|//|void |int16_t )", content):
                errors.append(f"FENCE MISMATCH in {filename}: C code syntax found inside python code fence")

        # 1.4 Master INDEX.md & Prerequisites DAG
        index_path = os.path.join(self.base_dir, "INDEX.md")
        if not os.path.isfile(index_path):
            errors.append("Master INDEX.md not found at repository root!")
        else:
            with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
                index_content = f.read()
            # Spot check modules in INDEX.md
            for t_id, slug, _, _ in TOPICS_METADATA[:10] + TOPICS_METADATA[-10:]:
                ref = f"{t_id:03d}-{slug}.md"
                if ref not in index_content:
                    errors.append(f"Master INDEX.md missing reference to: {ref}")

        dag_path = os.path.join(self.base_dir, "roadmaps", "prerequisites-dag.md")
        if not os.path.isfile(dag_path):
            errors.append("roadmaps/prerequisites-dag.md not found!")

        readme_path = os.path.join(self.base_dir, "README.md")
        if not os.path.isfile(readme_path):
            errors.append("Root README.md not found!")

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(f"  [PASS] 232 modules, 17 tiers, legacy preservation verified ({duration:.2f}s)")
        else:
            self.log(f"  [FAIL] Phase 1 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details="232 topic modules, 17 tiers, 7 sections, legacy preservation",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Phase 2: 8 Flagship Laboratories Discovery & Automated Unit Test Execution
    # =========================================================================
    def verify_phase_2_laboratories(self) -> TestResult:
        start_time = time.time()
        phase = 2
        name = "8 Flagship Laboratories Discovery & Automated Unit Test Execution"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 2/6] Validating 8 Flagship Laboratories & Automated Unit Tests...")

        labs_dir = os.path.join(self.base_dir, "labs")
        expected_labs = [
            "lab01-riscv-emulator",
            "lab02-mini-kernel-os",
            "lab03-compiler-llvm-jit",
            "lab04-lsm-storage-engine",
            "lab05-tensor-autograd-cuda",
            "lab06-raft-consensus-cluster",
            "lab07-hft-order-matching-engine",
            "lab08-foc-motor-robotics-controller",
        ]

        if not os.path.isdir(labs_dir):
            err = "Laboratories directory 'labs/' does not exist!"
            errors.append(err)
            self.log(f"  [FAIL] {err}")
            duration = time.time() - start_time
            return TestResult(phase=phase, name=name, passed=False, duration=duration, errors=errors)

        for lab_name in expected_labs:
            lab_path = os.path.join(labs_dir, lab_name)
            if not os.path.isdir(lab_path):
                errors.append(f"Laboratory directory missing: labs/{lab_name}")
                continue

            # Architecture files validation
            readme_path = os.path.join(lab_path, "README.md")
            if not os.path.isfile(readme_path):
                errors.append(f"{lab_name}: missing README.md")
            elif os.path.getsize(readme_path) < 1000:
                errors.append(f"{lab_name}: README.md is too short ({os.path.getsize(readme_path)} bytes, >= 1000B expected)")

            starter_path = os.path.join(lab_path, "starter")
            if not os.path.isdir(starter_path):
                errors.append(f"{lab_name}: missing 'starter/' scaffolding directory")

            makefile_path = os.path.join(lab_path, "Makefile")
            if not os.path.isfile(makefile_path):
                errors.append(f"{lab_name}: missing Makefile")

            test_runner_path = os.path.join(lab_path, "run_tests.py")
            if not os.path.isfile(test_runner_path):
                errors.append(f"{lab_name}: missing standalone test runner 'run_tests.py'")
                continue

            # Execute automated test runner
            lab_start = time.time()
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUNBUFFERED"] = "1"

            try:
                proc = subprocess.run(
                    [sys.executable, "run_tests.py"],
                    cwd=lab_path,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    env=env,
                )
                lab_dur = time.time() - lab_start
                combined_output = (proc.stdout + "\n" + proc.stderr).strip()

                if proc.returncode != 0:
                    err_msg = (
                        f"{lab_name}: test runner exited with code {proc.returncode} ({lab_dur:.2f}s)\n"
                        f"OUTPUT:\n{combined_output[-500:]}"
                    )
                    errors.append(err_msg)
                    self.log(f"  [FAIL] {lab_name} (exit code {proc.returncode}, {lab_dur:.2f}s)")
                else:
                    m_ran = re.search(r"Ran (\d+) tests? in", combined_output)
                    test_summary = f"{m_ran.group(1)} tests" if m_ran else "all tests"
                    self.log(f"  [PASS] {lab_name} ({test_summary} passed cleanly in {lab_dur:.2f}s)")
                    self.log_verbose(f"{lab_name} output summary: {combined_output[:150]}")
            except subprocess.TimeoutExpired:
                errors.append(f"{lab_name}: test runner timed out (>60s)!")
                self.log(f"  [FAIL] {lab_name} (timed out >60s)")
            except Exception as e:
                errors.append(f"{lab_name}: execution error: {e}")
                self.log(f"  [FAIL] {lab_name} (error: {e})")

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(f"  [PASS] All 8 flagship laboratories passed automated tests ({duration:.2f}s)")
        else:
            self.log(f"  [FAIL] Phase 2 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err.splitlines()[0]}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details="8 flagship laboratories test execution",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Phase 3: 6 Career Tracks & Cross-Link Resolution
    # =========================================================================
    def verify_phase_3_career_tracks(self) -> TestResult:
        start_time = time.time()
        phase = 3
        name = "6 Career Tracks & Cross-Link Resolution"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 3/6] Validating 6 Career Tracks & Relative Link Integrity...")

        tracks_dir = os.path.join(self.base_dir, "tracks")
        expected_tracks = [
            "track-systems-kernel-engineer.md",
            "track-ai-deep-learning-systems.md",
            "track-hft-low-latency-engineer.md",
            "track-embedded-robotics-engineer.md",
            "track-cybersecurity-pwn-researcher.md",
            "track-distributed-systems-cloud-architect.md",
        ]

        if not os.path.isdir(tracks_dir):
            err = "Career tracks directory 'tracks/' does not exist!"
            errors.append(err)
            self.log(f"  [FAIL] {err}")
            duration = time.time() - start_time
            return TestResult(phase=phase, name=name, passed=False, duration=duration, errors=errors)

        readme_path = os.path.join(tracks_dir, "README.md")
        if not os.path.isfile(readme_path):
            errors.append("tracks/README.md missing!")
        elif os.path.getsize(readme_path) < 500:
            errors.append(f"tracks/README.md is too short ({os.path.getsize(readme_path)} bytes)")

        total_links_verified = 0

        for track_name in expected_tracks:
            track_path = os.path.join(tracks_dir, track_name)
            if not os.path.isfile(track_path):
                errors.append(f"Career track file missing: tracks/{track_name}")
                continue

            size = os.path.getsize(track_path)
            if size < 2000:
                errors.append(f"{track_name}: file too short ({size} bytes, >= 2000B expected)")
                continue

            try:
                with open(track_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Cannot read {track_name}: {e}")
                continue

            # 3.1 24-Week Progression Check
            missing_weeks = []
            for w in range(1, 25):
                pattern = rf"\b(?:Week|Minggu)\s*0?{w}\b"
                if not re.search(pattern, content, re.IGNORECASE):
                    missing_weeks.append(w)
            if missing_weeks:
                errors.append(f"{track_name}: missing week milestones for weeks: {missing_weeks}")

            # 3.2 4-Tier Rubric & Milestone Assessment
            rubric_indicators = ["rubrik", "level 1", "level 2", "level 3", "level 4", "tier 1", "novice", "principal"]
            found_rubrics = sum(1 for ind in rubric_indicators if ind in content.lower())
            if found_rubrics < 3:
                errors.append(f"{track_name}: insufficient milestone rubrics / competency matrix")

            # 3.3 Capstone Project & Historical Post-Mortem
            if not re.search(r"\bcapstone\b", content, re.IGNORECASE) and not re.search(r"\bproyek akhir\b", content, re.IGNORECASE):
                warnings.append(f"{track_name}: capstone project section might be missing")

            if not re.search(r"\bpost-mortem\b", content, re.IGNORECASE) and not re.search(r"\bkegagalan nyata\b", content, re.IGNORECASE):
                warnings.append(f"{track_name}: historical post-mortem failure analysis section might be missing")

            # 3.4 Exhaustive Relative Markdown Link Resolution
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            track_links_count = 0
            for label, target in links:
                target = target.strip()
                if target.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
                    continue

                clean_target = urllib.parse.unquote(target.split("#")[0].strip())
                if not clean_target:
                    continue

                resolved_path = os.path.normpath(os.path.join(tracks_dir, clean_target))
                track_links_count += 1
                total_links_verified += 1

                if not os.path.exists(resolved_path):
                    errors.append(
                        f"{track_name}: broken relative link [{label}]({target}) -> resolved to non-existent '{resolved_path}'"
                    )

            self.log_verbose(f"{track_name}: verified {track_links_count} local links.")

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(f"  [PASS] 6 Career tracks verified ({total_links_verified} relative links resolved, {duration:.2f}s)")
        else:
            self.log(f"  [FAIL] Phase 3 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details=f"6 career tracks, 24-week roadmaps, {total_links_verified} links resolved",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Phase 4: Socratic Diagnostic Drills & Technical Interview Simulations
    # =========================================================================
    def verify_phase_4_diagnostic_drills(self) -> TestResult:
        start_time = time.time()
        phase = 4
        name = "Socratic Diagnostic Drills & Technical Interview Simulations"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 4/6] Validating Diagnostic Drills & Interview Simulations...")

        drills_dir = os.path.join(self.base_dir, "drills")
        if not os.path.isdir(drills_dir):
            err = "Drills directory 'drills/' does not exist!"
            errors.append(err)
            self.log(f"  [FAIL] {err}")
            duration = time.time() - start_time
            return TestResult(phase=phase, name=name, passed=False, duration=duration, errors=errors)

        readme_path = os.path.join(drills_dir, "README.md")
        if not os.path.isfile(readme_path):
            errors.append("drills/README.md missing!")
        elif os.path.getsize(readme_path) < 500:
            errors.append(f"drills/README.md is too short ({os.path.getsize(readme_path)} bytes)")

        expected_tier_drills = [
            "tier-00-cognitive-logic-drills.md",
            "tier-01-mathematics-drills.md",
            "tier-02-physics-semiconductor-drills.md",
            "tier-03-circuits-electronics-drills.md",
            "tier-04-digital-logic-arch-drills.md",
            "tier-05-embedded-rtos-drills.md",
            "tier-06-cs-core-compiler-drills.md",
            "tier-07-os-linux-drills.md",
            "tier-08-dsp-networking-drills.md",
            "tier-09-software-cloud-sre-drills.md",
            "tier-10-databases-data-eng-drills.md",
            "tier-11-cybersecurity-pwn-drills.md",
            "tier-12-ai-deep-learning-drills.md",
            "tier-13-cognitive-nlp-drills.md",
            "tier-14-fintech-hft-drills.md",
            "tier-15-robotics-control-drills.md",
            "tier-16-hpc-quantum-drills.md",
        ]

        expected_interview_sims = [
            "interview-systems-kernel.md",
            "interview-ai-deep-learning.md",
            "interview-hft-low-latency.md",
            "interview-embedded-robotics.md",
            "interview-cybersecurity-pwn.md",
            "interview-distributed-systems.md",
        ]

        all_drill_files = expected_tier_drills + expected_interview_sims
        total_collapsible_solutions = 0
        total_links_verified = 0

        for drill_name in all_drill_files:
            drill_path = os.path.join(drills_dir, drill_name)
            if not os.path.isfile(drill_path):
                errors.append(f"Drill file missing: drills/{drill_name}")
                continue

            size = os.path.getsize(drill_path)
            if size < 1000:
                errors.append(f"{drill_name}: file too short ({size} bytes, >= 1000B expected)")
                continue

            try:
                with open(drill_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Cannot read {drill_name}: {e}")
                continue

            # 4.1 Collapsible Hidden Solution Keys
            details_count = len(re.findall(r"<details\b", content, re.IGNORECASE))
            summary_count = len(re.findall(r"<summary\b", content, re.IGNORECASE))

            if details_count == 0 or summary_count == 0:
                errors.append(f"{drill_name}: missing collapsible solution keys (<details> and <summary>)")
            else:
                total_collapsible_solutions += details_count

            # 4.2 Link Resolution from Drills
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            for label, target in links:
                target = target.strip()
                if target.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
                    continue
                clean_target = urllib.parse.unquote(target.split("#")[0].strip())
                if not clean_target:
                    continue
                resolved_path = os.path.normpath(os.path.join(drills_dir, clean_target))
                total_links_verified += 1
                if not os.path.exists(resolved_path):
                    errors.append(
                        f"{drill_name}: broken relative link [{label}]({target}) -> resolved to non-existent '{resolved_path}'"
                    )

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(
                f"  [PASS] 17 Tier drills & 6 interview simulations verified "
                f"({total_collapsible_solutions} collapsible solutions, {total_links_verified} links, {duration:.2f}s)"
            )
        else:
            self.log(f"  [FAIL] Phase 4 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details=f"17 tier drills, 6 interview sims, {total_collapsible_solutions} solutions",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Phase 5: Spaced-Repetition Active Recall Flashcards
    # =========================================================================
    def verify_phase_5_flashcards(self) -> TestResult:
        start_time = time.time()
        phase = 5
        name = "Spaced-Repetition Active Recall Flashcards"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 5/6] Validating Spaced-Repetition Flashcards Decks & Cloze Syntax...")

        flashcards_dir = os.path.join(self.base_dir, "flashcards")
        if not os.path.isdir(flashcards_dir):
            err = "Flashcards directory 'flashcards/' does not exist!"
            errors.append(err)
            self.log(f"  [FAIL] {err}")
            duration = time.time() - start_time
            return TestResult(phase=phase, name=name, passed=False, duration=duration, errors=errors)

        readme_path = os.path.join(flashcards_dir, "README.md")
        if not os.path.isfile(readme_path):
            errors.append("flashcards/README.md missing!")
        elif os.path.getsize(readme_path) < 500:
            errors.append(f"flashcards/README.md is too short ({os.path.getsize(readme_path)} bytes)")

        expected_deck_names = [
            "deck-01-cognitive-logic-math",
            "deck-02-physics-circuits-semiconductors",
            "deck-03-digital-logic-computer-architecture",
            "deck-04-embedded-rtos-firmware",
            "deck-05-dsa-compilers-pl",
            "deck-06-os-internals-linux-kernel",
            "deck-07-dsp-networking-distributed-systems",
            "deck-08-cybersecurity-cryptography-pwn",
            "deck-09-ai-deep-learning-cuda-nlp",
            "deck-10-fintech-hft-robotics-hpc",
        ]

        total_cards_count = 0
        cloze_pattern = re.compile(r"\{\{c\d+::.*?\}\}")
        found_categories: Set[str] = set()

        for deck_name in expected_deck_names:
            tsv_path = os.path.join(flashcards_dir, f"{deck_name}.tsv")
            md_path = os.path.join(flashcards_dir, f"{deck_name}.md")

            if not os.path.isfile(md_path):
                errors.append(f"Companion markdown missing: flashcards/{deck_name}.md")
            elif os.path.getsize(md_path) < 500:
                errors.append(f"{deck_name}.md is too short ({os.path.getsize(md_path)} bytes)")

            if not os.path.isfile(tsv_path):
                errors.append(f"TSV deck missing: flashcards/{deck_name}.tsv")
                continue

            try:
                with open(tsv_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception as e:
                errors.append(f"Cannot read {deck_name}.tsv: {e}")
                continue

            deck_cards = 0
            for line_idx, line in enumerate(lines, 1):
                raw_line = line.strip("\r\n")
                if not raw_line or raw_line.startswith("#"):
                    continue

                cols = raw_line.split("\t")
                if len(cols) != 3:
                    errors.append(
                        f"{deck_name}.tsv: line {line_idx} has {len(cols)} columns (expected 3: Text, Extra, Tags)"
                    )
                    continue

                text_col, extra_col, tags_col = cols[0], cols[1], cols[2]

                if not cloze_pattern.search(text_col):
                    errors.append(
                        f"{deck_name}.tsv: line {line_idx} missing cloze deletion '{{{{c1::...}}}}' in column 1: {text_col[:40]}"
                    )

                full_card_text = f"{text_col} {extra_col} {tags_col}".lower()
                if any(w in full_card_text for w in ["definisi", "definition"]):
                    found_categories.add("definitions")
                if any(w in full_card_text for w in ["matematika", "math", "rumus", "identity"]):
                    found_categories.add("mathematical_identities")
                if any(w in full_card_text for w in ["konstanta", "constant", "latency", "ns"]):
                    found_categories.add("architecture_constants")
                if any(w in full_card_text for w in ["opcode", "instruksi", "instruction", "assembly"]):
                    found_categories.add("assembly_opcodes")
                if any(w in full_card_text for w in ["heuristik", "heuristic", "hukum", "law", "rule"]):
                    found_categories.add("design_heuristics")

                deck_cards += 1

            if deck_cards < 5:
                errors.append(f"{deck_name}.tsv has only {deck_cards} cards (expected >= 5)")
            total_cards_count += deck_cards

        mandatory_categories = [
            "definitions",
            "mathematical_identities",
            "architecture_constants",
            "assembly_opcodes",
            "design_heuristics",
        ]
        missing_categories = [cat for cat in mandatory_categories if cat not in found_categories]
        if missing_categories:
            warnings.append(
                f"Flashcards category coverage may be incomplete. Missing detected categories: {missing_categories}"
            )

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(
                f"  [PASS] 10 Paired TSV/MD decks verified ({total_cards_count} cloze cards, 3-column syntax valid, {duration:.2f}s)"
            )
        else:
            self.log(f"  [FAIL] Phase 5 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details=f"10 paired TSV/MD decks, {total_cards_count} cards",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Phase 6: Zero-Placeholder & Cleanliness Audit
    # =========================================================================
    def verify_phase_6_zero_placeholders(self) -> TestResult:
        start_time = time.time()
        phase = 6
        name = "Zero-Placeholder & Cleanliness Audit"
        errors: List[str] = []
        warnings: List[str] = []

        self.log("\n[PHASE 6/6] Validating Zero Placeholders across Newly Authored Codebase...")

        target_dirs = ["tracks", "drills", "flashcards", "labs", "curriculum"]
        forbidden_regex = re.compile(r"\b(TODO|FIXME|TBD|PLACEHOLDER|XXX)\b")
        lorem_regex = re.compile(r"lorem\s+ipsum", re.IGNORECASE)
        empty_link_regex = re.compile(r"\[[^\]]*\]\(\s*\)")

        ignored_extensions = {".exe", ".o", ".obj", ".a", ".lib", ".dll", ".so", ".dylib", ".bin", ".pyc", ".png", ".jpg"}
        total_files_scanned = 0

        for tdir in target_dirs:
            full_tdir = os.path.join(self.base_dir, tdir)
            if not os.path.isdir(full_tdir):
                continue

            for root, dirs, files in os.walk(full_tdir):
                dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "build", "dist", ".pytest_cache"}]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ignored_extensions:
                        continue

                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, self.base_dir)
                    total_files_scanned += 1

                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()
                    except Exception as e:
                        warnings.append(f"Cannot read {relpath} for placeholder check: {e}")
                        continue

                    for line_num, line in enumerate(lines, 1):
                        m_forb = forbidden_regex.search(line)
                        if m_forb:
                            errors.append(
                                f"{relpath}:{line_num}: forbidden placeholder '{m_forb.group(0)}' found: {line.strip()[:60]}"
                            )

                        m_lorem = lorem_regex.search(line)
                        if m_lorem:
                            errors.append(
                                f"{relpath}:{line_num}: forbidden placeholder 'lorem ipsum' found: {line.strip()[:60]}"
                            )

                        if ext == ".md":
                            m_empty = empty_link_regex.search(line)
                            if m_empty:
                                errors.append(
                                    f"{relpath}:{line_num}: empty markdown link '[]()' found: {line.strip()[:60]}"
                                )

        duration = time.time() - start_time
        passed = len(errors) == 0

        if passed:
            self.log(f"  [PASS] Cleanliness verified across {total_files_scanned} files (0 placeholders, {duration:.2f}s)")
        else:
            self.log(f"  [FAIL] Phase 6 failed with {len(errors)} error(s) ({duration:.2f}s)")
            for err in errors[:10]:
                self.log(f"    - {err}")
            if len(errors) > 10:
                self.log(f"    ... and {len(errors) - 10} more errors.")

        return TestResult(
            phase=phase,
            name=name,
            passed=passed,
            duration=duration,
            details=f"{total_files_scanned} files scanned, 0 placeholders detected",
            errors=errors,
            warnings=warnings,
        )

    # =========================================================================
    # Runner & Orchestrator
    # =========================================================================
    def run(self, phases: Optional[List[int]] = None) -> bool:
        overall_start = time.time()
        self.log("=" * 80)
        self.log("           ULTIMATE LEARNING PATHS - ECOSYSTEM VERIFICATION SUITE")
        self.log("=" * 80)
        self.log(f"Host: Python {sys.version.split()[0]} | Platform: {sys.platform}")
        self.log(f"Base Directory: {self.base_dir}")
        selected_phases = phases or [1, 2, 3, 4, 5, 6]
        self.log(f"Active Phases: {selected_phases}")
        self.log("-" * 80)

        phase_dispatch = {
            1: self.verify_phase_1_curriculum,
            2: self.verify_phase_2_laboratories,
            3: self.verify_phase_3_career_tracks,
            4: self.verify_phase_4_diagnostic_drills,
            5: self.verify_phase_5_flashcards,
            6: self.verify_phase_6_zero_placeholders,
        }

        all_passed = True

        for p in selected_phases:
            if p in phase_dispatch:
                res = phase_dispatch[p]()
                self.results.append(res)
                if not res.passed:
                    all_passed = False
                    self.total_errors.extend(res.errors)
                    if self.fail_fast:
                        self.log(f"\n[FAIL-FAST] Halting execution early due to failure in Phase {p}.")
                        break
                if res.warnings:
                    self.total_warnings.extend(res.warnings)

        total_duration = time.time() - overall_start

        self.log("\n" + "=" * 80)
        if all_passed:
            self.log(f"VERIFICATION SUMMARY: ALL {len(self.results)} REQUESTED PHASES PASSED (100% SUCCESS)")
            self.log(f"Total Duration: {total_duration:.2f}s | Failures: 0 | Warnings: {len(self.total_warnings)}")
            self.log("EXIT CODE: 0")
            self.log("=" * 80)
            return True
        else:
            self.log("VERIFICATION SUMMARY: TEST SUITE FAILED")
            self.log(
                f"Total Duration: {total_duration:.2f}s | Failures: {len(self.total_errors)} | Warnings: {len(self.total_warnings)}"
            )
            for res in self.results:
                status = "PASS" if res.passed else "FAIL"
                self.log(f"  Phase {res.phase}: {res.name} -> [{status}] ({res.duration:.2f}s)")
            self.log("EXIT CODE: 1")
            self.log("=" * 80)
            return False


# =============================================================================
# Standard unittest integration
# =============================================================================
class TestEcosystemSuite(unittest.TestCase):
    """
    Standard unittest test cases wrapping all 6 verification phases.
    Enables execution via `python -m unittest scripts.verify_ecosystem` or `pytest`.
    """

    @classmethod
    def setUpClass(cls):
        cls.verifier = EcosystemVerifier(verbose=False, fail_fast=False)

    def test_phase_1_curriculum(self):
        res = self.verifier.verify_phase_1_curriculum()
        self.assertTrue(res.passed, f"Phase 1 failed: {res.errors[:5]}")

    def test_phase_2_laboratories(self):
        res = self.verifier.verify_phase_2_laboratories()
        self.assertTrue(res.passed, f"Phase 2 failed: {res.errors[:5]}")

    def test_phase_3_career_tracks(self):
        res = self.verifier.verify_phase_3_career_tracks()
        self.assertTrue(res.passed, f"Phase 3 failed: {res.errors[:5]}")

    def test_phase_4_diagnostic_drills(self):
        res = self.verifier.verify_phase_4_diagnostic_drills()
        self.assertTrue(res.passed, f"Phase 4 failed: {res.errors[:5]}")

    def test_phase_5_flashcards(self):
        res = self.verifier.verify_phase_5_flashcards()
        self.assertTrue(res.passed, f"Phase 5 failed: {res.errors[:5]}")

    def test_phase_6_zero_placeholders(self):
        res = self.verifier.verify_phase_6_zero_placeholders()
        self.assertTrue(res.passed, f"Phase 6 failed: {res.errors[:5]}")


def main():
    parser = argparse.ArgumentParser(description="Ultimate Learning Paths Ecosystem Verification Suite")
    parser.add_argument(
        "--phase",
        "-p",
        type=str,
        default="all",
        help="Specify phase(s) to run (e.g., '1', '2', '1,2,3', or 'all'). Default: 'all'",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debugging output",
    )
    parser.add_argument(
        "--fail-fast",
        "-x",
        action="store_true",
        help="Stop immediately on the first phase failure",
    )

    args = parser.parse_args()

    phases_to_run = None
    if args.phase != "all":
        try:
            phases_to_run = [int(p.strip()) for p in args.phase.split(",") if p.strip()]
        except ValueError:
            print(f"Error: Invalid --phase argument '{args.phase}'. Must be numbers like '1' or '1,2'.")
            sys.exit(1)

    verifier = EcosystemVerifier(verbose=args.verbose, fail_fast=args.fail_fast)
    success = verifier.run(phases=phases_to_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
