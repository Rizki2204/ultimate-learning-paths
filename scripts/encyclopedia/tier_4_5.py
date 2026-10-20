# -*- coding: utf-8 -*-
"""
Tier 4 & Tier 5 Aggregated Knowledge Base
Covers Topics 53 - 87 (Computer Architecture, Digital Logic, Embedded Systems, RTOS & TinyML)
"""

from scripts.encyclopedia.tier_4_part1 import DATA_TIER_4_PART1
from scripts.encyclopedia.tier_4_part2 import DATA_TIER_4_PART2
from scripts.encyclopedia.tier_5_part1 import DATA_TIER_5_PART1
from scripts.encyclopedia.tier_5_part2 import DATA_TIER_5_PART2

DATA_TIER_4_5 = {}
DATA_TIER_4_5.update(DATA_TIER_4_PART1)
DATA_TIER_4_5.update(DATA_TIER_4_PART2)
DATA_TIER_4_5.update(DATA_TIER_5_PART1)
DATA_TIER_4_5.update(DATA_TIER_5_PART2)
