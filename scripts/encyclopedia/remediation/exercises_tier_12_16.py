# -*- coding: utf-8 -*-
"""
Authentic Multi-Tier Exercises for Tiers 12-16 (Topics 183-232).
"""

from scripts.encyclopedia.remediation.data_tier_12 import DATA_TIER_12
from scripts.encyclopedia.remediation.data_tier_13 import DATA_TIER_13
from scripts.encyclopedia.remediation.data_tier_14 import DATA_TIER_14
from scripts.encyclopedia.remediation.data_tier_15 import DATA_TIER_15
from scripts.encyclopedia.remediation.data_tier_16 import DATA_TIER_16

DOMAIN_EXERCISES_TIER_12_16 = {}

for tier_data in [DATA_TIER_12, DATA_TIER_13, DATA_TIER_14, DATA_TIER_15, DATA_TIER_16]:
    for tid, content in tier_data.items():
        if "exercise" in content:
            ex = content["exercise"]
            if isinstance(ex, dict):
                formatted = f"### Tingkat 1: Dasar\n- **Tugas**: {ex['level1']}\n\n### Tingkat 2: Menengah\n- **Tugas**: {ex['level2']}\n\n### Tingkat 3: Mahir\n- **Tugas**: {ex['level3']}"
                DOMAIN_EXERCISES_TIER_12_16[tid] = formatted
            else:
                DOMAIN_EXERCISES_TIER_12_16[tid] = ex

if __name__ == "__main__":
    print(f"DOMAIN_EXERCISES_TIER_12_16 loaded with {len(DOMAIN_EXERCISES_TIER_12_16)} exercises (183-232).")
    assert len(DOMAIN_EXERCISES_TIER_12_16) == 50, f"Expected 50, got {len(DOMAIN_EXERCISES_TIER_12_16)}"
    for tid in range(183, 233):
        assert tid in DOMAIN_EXERCISES_TIER_12_16, f"Missing exercise for topic {tid}"
    print("Exercises Tier 12-16 successfully validated!")
