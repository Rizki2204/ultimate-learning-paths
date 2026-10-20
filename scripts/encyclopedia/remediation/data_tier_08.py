# -*- coding: utf-8 -*-
"""
Aggregated Remediation Data for Tier 08 (Topics 125-139):
Digital Signal Processing, Telecommunications & Computer Networks.
"""

from scripts.encyclopedia.remediation.data_tier_08_part1 import DATA_TIER_08_PART1
from scripts.encyclopedia.remediation.data_tier_08_part2 import DATA_TIER_08_PART2

DATA_TIER_08 = {}
DATA_TIER_08.update(DATA_TIER_08_PART1)
DATA_TIER_08.update(DATA_TIER_08_PART2)
