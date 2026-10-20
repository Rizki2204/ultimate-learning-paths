# -*- coding: utf-8 -*-
"""
Authentic multi-tier exercises across all 232 topics.
Merges curated exercises from:
- Tiers 00-05 (exercises_tier_00_05.py, 87 topics)
- Tiers 06-11 (exercises_tier_06_11.py, 95 topics)
- Tiers 12-16 (exercises_tier_12_16.py, 50 topics)
"""

from scripts.encyclopedia.remediation.exercises_tier_00_05 import EXERCISES_TIER_00_05
from scripts.encyclopedia.remediation.exercises_tier_06_11 import DOMAIN_EXERCISES_TIER_06_11
from scripts.encyclopedia.remediation.exercises_tier_12_16 import DOMAIN_EXERCISES_TIER_12_16

DOMAIN_EXERCISES = {}
DOMAIN_EXERCISES.update(EXERCISES_TIER_00_05)
DOMAIN_EXERCISES.update(DOMAIN_EXERCISES_TIER_06_11)
DOMAIN_EXERCISES.update(DOMAIN_EXERCISES_TIER_12_16)

# Format any dict exercises into 3-tier markdown strings
for tid, ex in DOMAIN_EXERCISES.items():
    if isinstance(ex, dict):
        formatted = f"### Tingkat 1: Dasar\n- **Tugas**: {ex['level1']}\n\n### Tingkat 2: Menengah\n- **Tugas**: {ex['level2']}\n\n### Tingkat 3: Mahir\n- **Tugas**: {ex['level3']}"
        DOMAIN_EXERCISES[tid] = formatted

if __name__ == "__main__":
    print(f"Loaded DOMAIN_EXERCISES with {len(DOMAIN_EXERCISES)} topics.")
    assert len(DOMAIN_EXERCISES) == 232, f"Expected 232, got {len(DOMAIN_EXERCISES)}"
    for tid in range(1, 233):
        assert tid in DOMAIN_EXERCISES, f"Missing exercise for topic {tid}"
    print("DOMAIN_EXERCISES successfully validated across all 232 topics!")