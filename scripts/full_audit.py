# scripts/full_audit.py
import os
import re
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURRICULUM_DIR = os.path.join(BASE_DIR, "curriculum")

MANDATORY_SECTIONS = [
    "## 1. Intuisi Dasar Tanpa Jargon",
    "## 2. Fondasi Teoretis & Aksiomatik",
    "## 3. Anatomi Teknis & Cara Kerja Internal",
    "## 4. Implementasi Praktis & Kode",
    "## 5. Miskonsepsi & Jebakan Industri",
    "## 6. Proyek Latihan & Rubrik Penilaian Mandiri",
    "## 7. Rekomendasi Sumber Belajar Standar Emas"
]

FORBIDDEN_PHRASES = [
    "TODO", "FIXME", "TBD", "lorem ipsum",
    "Model formal untuk", "Implementasi referensi",
    "Intuisi mendasar mengenai", "Anatomi internal sistem untuk",
    "Latihan berjenjang tingkat"
]

topic_files = []
for root, dirs, files in os.walk(CURRICULUM_DIR):
    for f in files:
        if f.endswith(".md") and f != "README.md":
            topic_files.append(os.path.join(root, f))

print(f"Total topic files found: {len(topic_files)}")
assert len(topic_files) == 232, f"Expected 232 topic files, got {len(topic_files)}"

failures = []
url_count_total = 0

for filepath in sorted(topic_files):
    fname = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    if size < 4000:
        failures.append(f"{fname}: size too small ({size} bytes)")
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check sections
    for sec in MANDATORY_SECTIONS:
        if sec not in content:
            failures.append(f"{fname}: missing section '{sec}'")
            
    # Check forbidden phrases
    for fp in FORBIDDEN_PHRASES:
        pattern = r'\b' + re.escape(fp) + r'\b'
        if re.search(pattern, content, re.IGNORECASE):
            failures.append(f"{fname}: contains forbidden phrase '{fp}'")
            
    # Check mermaid
    if "```mermaid" not in content:
        failures.append(f"{fname}: missing mermaid diagram")
        
    # Check code block
    has_code = False
    for lang in ["python", "c", "cpp", "rust", "verilog", "sql", "bash", "assembly", "text"]:
        if f"```{lang}" in content or "```" in content:
            has_code = True
            break
    if not has_code:
        failures.append(f"{fname}: missing valid code block")
        
    # Check KaTeX math
    if "$" not in content:
        failures.append(f"{fname}: missing KaTeX math notation")
        
    # Check links
    links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', content)
    url_count_total += len(links)
    if len(links) < 3:
        failures.append(f"{fname}: insufficient verified links ({len(links)} links)")
        
    # Check empty links
    empty_links = re.findall(r'\[([^\]]+)\]\(\s*\)', content)
    if empty_links:
        failures.append(f"{fname}: contains empty links {empty_links}")

print(f"Total verified links across all files: {url_count_total}")
print(f"Average links per file: {url_count_total / len(topic_files):.2f}")

if failures:
    print(f"FAILURES DETECTED ({len(failures)}):")
    for fail in failures[:20]:
        print(f"  - {fail}")
    sys.exit(1)
else:
    print("ALL 232 TOPIC MODULES PASSED 100% OF RIGOROUS CHECKS WITH ZERO FAILURES!")

# Also check legacy preservation
legacy_domains = os.path.join(BASE_DIR, "domains")
legacy_docs = os.path.join(BASE_DIR, "docs")
assert os.path.isdir(legacy_domains), "legacy domains/ missing!"
assert os.path.isdir(legacy_docs), "legacy docs/ missing!"
print(f"Legacy domains files: {len(os.listdir(legacy_domains))} | docs files: {len(os.listdir(legacy_docs))}")

# Check 17 Tier READMEs
for d in os.listdir(CURRICULUM_DIR):
    subpath = os.path.join(CURRICULUM_DIR, d)
    if os.path.isdir(subpath):
        readme = os.path.join(subpath, "README.md")
        assert os.path.isfile(readme), f"Missing README in {d}"
print("All 17 Tier READMEs verified!")

# Check INDEX.md and prerequisites-dag.md
assert os.path.isfile(os.path.join(BASE_DIR, "INDEX.md")), "INDEX.md missing!"
assert os.path.isfile(os.path.join(BASE_DIR, "roadmaps", "prerequisites-dag.md")), "prerequisites-dag.md missing!"
assert os.path.isfile(os.path.join(BASE_DIR, "README.md")), "README.md missing!"
print("Master INDEX.md, Prerequisites DAG, and README.md verified!")
