# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 04 (Topics 53-69):
Digital Logic, RTL Synthesis, Computer Architecture & Microarchitecture.
"""

from scripts.encyclopedia.remediation.data_tier_04_part1 import DATA_TIER_04_PART1
from scripts.encyclopedia.remediation.data_tier_04_part2 import DATA_TIER_04_PART2

DATA_TIER_04 = {}
DATA_TIER_04.update(DATA_TIER_04_PART1)
DATA_TIER_04.update(DATA_TIER_04_PART2)
