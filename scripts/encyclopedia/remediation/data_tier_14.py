# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 14 (Topics 207-216):
Fintech, Financial Engineering, HFT & Blockchain.
Consolidates Part 1 and Part 2.
"""

from scripts.encyclopedia.remediation.data_tier_14_part1 import DATA_TIER_14_PART1
from scripts.encyclopedia.remediation.data_tier_14_part2 import DATA_TIER_14_PART2

DATA_TIER_14 = {}
DATA_TIER_14.update(DATA_TIER_14_PART1)
DATA_TIER_14.update(DATA_TIER_14_PART2)

if __name__ == "__main__":
    print(f"DATA_TIER_14 loaded with {len(DATA_TIER_14)} topics (207-216).")
    assert len(DATA_TIER_14) == 10, f"Expected 10 topics, got {len(DATA_TIER_14)}"
    for tid in range(207, 217):
        assert tid in DATA_TIER_14, f"Missing topic {tid}"
    print("Tier 14 validation successful!")
