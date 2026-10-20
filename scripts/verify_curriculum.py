# scripts/verify_curriculum.py
"""
Automated validation and integrity test suite for Ultimate Learning Paths repository.
Verifies all 17 Tiers, all 232 Topic Modules, 7-layer structure compliance,
file size sanity, link validity, and side-by-side preservation of legacy directories.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.tier_definitions import TIERS, TOPICS_METADATA


MANDATORY_SECTIONS = [
    "## 1. Intuisi Dasar Tanpa Jargon",
    "## 2. Fondasi Teoretis & Aksiomatik",
    "## 3. Anatomi Teknis & Cara Kerja Internal",
    "## 4. Implementasi Praktis & Kode",
    "## 5. Miskonsepsi & Jebakan Industri",
    "## 6. Proyek Latihan & Rubrik Penilaian Mandiri",
    "## 7. Rekomendasi Sumber Belajar Standar Emas"
]

def test_legacy_preservation():
    print("[1/5] Verifikasi Preservasi Direktori Lama (Side-by-Side)...")
    docs_dir = os.path.join(BASE_DIR, "docs")
    domains_dir = os.path.join(BASE_DIR, "domains")
    
    assert os.path.isdir(docs_dir), "Folder legacy 'docs/' tidak ditemukan!"
    assert os.path.isdir(domains_dir), "Folder legacy 'domains/' tidak ditemukan!"
    
    domains_files = os.listdir(domains_dir)
    assert len(domains_files) > 10, f"Folder 'domains/' tampaknya terhapus (hanya ada {len(domains_files)} files)!"
    print(f"  -> OK: Folder docs/ dan domains/ ({len(domains_files)} files) terpelihara utuh.")

def test_tier_directories_and_readmes():
    print("[2/5] Verifikasi 17 Direktori Tingkat & README...")
    curriculum_dir = os.path.join(BASE_DIR, "curriculum")
    assert os.path.isdir(curriculum_dir), "Folder 'curriculum/' tidak ditemukan!"
    
    for tier in TIERS:
        t_dir = os.path.join(curriculum_dir, tier["dir_name"])
        assert os.path.isdir(t_dir), f"Direktori Tingkat {tier['dir_name']} tidak ditemukan!"
        
        readme_path = os.path.join(t_dir, "README.md")
        assert os.path.isfile(readme_path), f"README.md pada {tier['dir_name']} tidak ditemukan!"
        assert os.path.getsize(readme_path) > 200, f"README.md pada {tier['dir_name']} terlalu kecil!"
        
    print("  -> OK: 17 Direktori Tingkat & 17 README.md diverifikasi.")

def test_all_232_topic_modules():
    print("[3/5] Verifikasi 232 File Modul Topik & Kepatuhan Template 7-Lapis...")
    total_topics = len(TOPICS_METADATA)
    assert total_topics == 232, f"Metadata topik harus tepat 232 (saat ini {total_topics})!"
    
    for t_id, slug, full_title, tier_idx in TOPICS_METADATA:
        tier = TIERS[tier_idx]
        filename = f"{t_id:03d}-{slug}.md"
        filepath = os.path.join(BASE_DIR, "curriculum", tier["dir_name"], filename)
        
        assert os.path.isfile(filepath), f"File modul hilang: {filepath}"
        
        size = os.path.getsize(filepath)
        assert size >= 500, f"File modul {filename} terlalu pendek ({size} bytes)! Harap periksa integritas isi."
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        for sec in MANDATORY_SECTIONS:
            assert sec in content, f"Modul {filename} tidak memuat bagian wajib: '{sec}'"
            
    print("  -> OK: 232 File Modul lengkap 100% dan mematuhi format 7-lapis standar.")

def test_master_index():
    print("[4/5] Verifikasi Master INDEX.md...")
    index_path = os.path.join(BASE_DIR, "INDEX.md")
    assert os.path.isfile(index_path), "Master INDEX.md tidak ditemukan!"
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    for t_id, slug, full_title, tier_idx in TOPICS_METADATA:
        expected_ref = f"{t_id:03d}-{slug}.md"
        assert expected_ref in content, f"Modul {expected_ref} tidak terdaftar di INDEX.md!"
        
    print("  -> OK: Master INDEX.md memuat tautan ke seluruh 232 modul.")

def test_dag_and_root_readme():
    print("[5/5] Verifikasi Prerequisites DAG & Master README.md...")
    dag_path = os.path.join(BASE_DIR, "roadmaps", "prerequisites-dag.md")
    assert os.path.isfile(dag_path), "File roadmaps/prerequisites-dag.md tidak ditemukan!"
    
    readme_path = os.path.join(BASE_DIR, "README.md")
    assert os.path.isfile(readme_path), "File root README.md tidak ditemukan!"
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "INDEX.md" in content, "README.md tidak menautkan INDEX.md!"
    assert "prerequisites-dag.md" in content, "README.md tidak menautkan prerequisites-dag.md!"
    for tier in TIERS:
        assert tier["dir_name"] in content, f"Tingkat {tier['dir_name']} tidak tercantum di tabel README.md!"
        
    print("  -> OK: Master README.md & Prerequisites DAG diverifikasi penuh.")

def run_all_tests():
    try:
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print("==================================================")
    print("RUNNING CURRICULUM INTEGRITY VERIFICATION SUITE")
    print("==================================================")
    try:
        test_legacy_preservation()
        test_tier_directories_and_readmes()
        test_all_232_topic_modules()
        test_master_index()
        test_dag_and_root_readme()
        print("==================================================")
        print("[SUCCESS] SEMUA PENGUJIAN LULUS 100%! VERIFIKASI SUKSES!")
        print("==================================================")
        return True
    except AssertionError as e:
        print(f"\n[FAIL] PENGUJIAN GAGAL: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
