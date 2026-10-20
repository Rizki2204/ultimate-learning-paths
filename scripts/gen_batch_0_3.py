# scripts/gen_batch_0_3.py
"""
Generator for Batch 1: Tingkat 0 to Tingkat 3 (Topics 1 to 52).
Generates rigorous, educational, 7-layer curriculum files.
"""

import os
from scripts.tier_definitions import TIERS, TOPICS_METADATA

def get_tier_dir(tier_idx, base_path):
    tier = TIERS[tier_idx]
    dir_path = os.path.join(base_path, "curriculum", tier["dir_name"])
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def build_topic_batch_0_3(base_path):
    print("Generating Batch 1: Tingkat 0 s/d 3 (Topics 1 - 52)...")
    
    # Detailed topic definitions for Topics 1..52
    from scripts.topic_data_batch_0_3 import BATCH_0_3_DATA
    
    for t_id in range(1, 53):
        meta = TOPICS_METADATA[t_id - 1]
        topic_id, slug, full_title, tier_idx = meta
        tier = TIERS[tier_idx]
        tier_dir = get_tier_dir(tier_idx, base_path)
        
        data = BATCH_0_3_DATA.get(topic_id, {})
        
        # Determine prev and next topic links
        prev_link = f"[{TOPICS_METADATA[t_id-2][1]}](./{t_id-1:03d}-{TOPICS_METADATA[t_id-2][1]}.md)" if t_id > 1 else "None"
        next_link = f"[{TOPICS_METADATA[t_id][1]}](./{t_id+1:03d}-{TOPICS_METADATA[t_id][1]}.md)" if t_id < 232 else "None"
        
        filename = f"{topic_id:03d}-{slug}.md"
        filepath = os.path.join(tier_dir, filename)
        
        content = f"""# Modul {topic_id:03d}: {full_title}

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat {tier_idx}: {tier['title']}](./README.md)
*Sebelumnya*: {prev_link} | *Berikutnya*: {next_link}

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
{data.get('intuition', 'Intuisi dasar topik ini.')}

## 2. Fondasi Teoretis & Aksiomatik / Matematis
{data.get('theory', 'Fondasi teoretis dan matematis aksiomatik.')}

## 3. Anatomi Teknis & Cara Kerja Internal
{data.get('internals', 'Anatomi dan mekanisme teknis internal.')}

## 4. Implementasi Praktis & Kode / Simulasi Riil
{data.get('code_block', '```python\n# Implementasi standar\n```')}

## 5. Miskonsepsi & Jebakan Industri
{data.get('pitfalls', 'Miskonsepsi umum dan jebakan.')}

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
{data.get('exercises', 'Tantangan proyek progresif.')}

## 7. Rekomendasi Sumber Belajar Standar Emas
{data.get('references', '- Buku teks standar universitas internasional.')}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Batch 1 completed successfully!")

if __name__ == "__main__":
    import sys
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_topic_batch_0_3(base)
