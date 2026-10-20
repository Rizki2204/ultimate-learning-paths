# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 05 (Topics 70-87):
Embedded Systems, Firmware Bare-Metal & RTOS/IoT.
"""

from scripts.encyclopedia.remediation.data_tier_05_part1 import DATA_TIER_05_PART1
from scripts.encyclopedia.remediation.data_tier_05_part2 import DATA_TIER_05_PART2

DATA_TIER_05 = {}
DATA_TIER_05.update(DATA_TIER_05_PART1)
DATA_TIER_05.update(DATA_TIER_05_PART2)
