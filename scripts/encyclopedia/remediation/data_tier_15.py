# -*- coding: utf-8 -*-
r"""
Consolidated Remediation Data for Tier 15 (Topics 217-226):
Mechatronics, Robotics, Control Theory & Automation.
"""

from scripts.encyclopedia.remediation.data_tier_15_part1 import DATA_TIER_15_PART1
from scripts.encyclopedia.remediation.data_tier_15_part2 import DATA_TIER_15_PART2

DATA_TIER_15 = {}
DATA_TIER_15.update(DATA_TIER_15_PART1)
DATA_TIER_15.update(DATA_TIER_15_PART2)

if __name__ == "__main__":
    print(f"Loaded {len(DATA_TIER_15)} topics for Tier 15: {sorted(DATA_TIER_15.keys())}")
    assert len(DATA_TIER_15) == 10, f"Expected 10 topics in Tier 15, got {len(DATA_TIER_15)}"
    print("Tier 15 integrity verification passed!")
