# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 13 (Topics 196-206):
Sains Kognitif, Neuroengineering & NLP/LLM.
Consolidates Part 1 and Part 2.
"""

from scripts.encyclopedia.remediation.data_tier_13_part1 import DATA_TIER_13_PART1
from scripts.encyclopedia.remediation.data_tier_13_part2 import DATA_TIER_13_PART2

DATA_TIER_13 = {}
DATA_TIER_13.update(DATA_TIER_13_PART1)
DATA_TIER_13.update(DATA_TIER_13_PART2)

if __name__ == "__main__":
    print(f"DATA_TIER_13 loaded with {len(DATA_TIER_13)} topics (196-206).")
    assert len(DATA_TIER_13) == 11, f"Expected 11 topics, got {len(DATA_TIER_13)}"
    for tid in range(196, 207):
        assert tid in DATA_TIER_13, f"Missing topic {tid}"
    print("Tier 13 validation successful!")
