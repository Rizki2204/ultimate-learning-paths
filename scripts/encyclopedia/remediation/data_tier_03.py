# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 03 (Topics 38-52):
Circuits, Analog Electronics & Microelectronics.
"""

from scripts.encyclopedia.remediation.data_tier_03_part1 import DATA_TIER_03_PART1
from scripts.encyclopedia.remediation.data_tier_03_part2 import DATA_TIER_03_PART2

DATA_TIER_03 = {}
DATA_TIER_03.update(DATA_TIER_03_PART1)
DATA_TIER_03.update(DATA_TIER_03_PART2)
