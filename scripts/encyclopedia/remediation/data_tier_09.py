# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 09 (Topics 140-156):
Software Engineering, Full-Stack, Cloud & Site Reliability Engineering (SRE).
"""

from scripts.encyclopedia.remediation.data_tier_09_part1 import DATA_TIER_09_PART1
from scripts.encyclopedia.remediation.data_tier_09_part2 import DATA_TIER_09_PART2

DATA_TIER_09 = {}
DATA_TIER_09.update(DATA_TIER_09_PART1)
DATA_TIER_09.update(DATA_TIER_09_PART2)
