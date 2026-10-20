# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 02 (Topics 24-37):
Classical Physics, Electromagnetism & Semiconductor Physics.
"""

from scripts.encyclopedia.remediation.data_tier_02_part1 import DATA_TIER_02_PART1
from scripts.encyclopedia.remediation.data_tier_02_part2 import DATA_TIER_02_PART2

DATA_TIER_02 = {}
DATA_TIER_02.update(DATA_TIER_02_PART1)
DATA_TIER_02.update(DATA_TIER_02_PART2)
