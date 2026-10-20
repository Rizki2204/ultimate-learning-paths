# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 11 (Topics 168-182):
Cyber Security, Kriptografi & Reverse Engineering.
Consolidates Part 1 and Part 2.
"""

from scripts.encyclopedia.remediation.data_tier_11_part1 import DATA_TIER_11_PART1
from scripts.encyclopedia.remediation.data_tier_11_part2 import DATA_TIER_11_PART2

DATA_TIER_11 = {}
DATA_TIER_11.update(DATA_TIER_11_PART1)
DATA_TIER_11.update(DATA_TIER_11_PART2)

if __name__ == "__main__":
    print(f"DATA_TIER_11 loaded with {len(DATA_TIER_11)} topics (168-182).")
    assert len(DATA_TIER_11) == 15, f"Expected 15 topics, got {len(DATA_TIER_11)}"
    for tid in range(168, 183):
        assert tid in DATA_TIER_11, f"Missing topic {tid}"
    print("Tier 11 validation successful!")
