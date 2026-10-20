"""Tier 14, 15, and 16 aggregator: Topics 207 - 232
"""
from scripts.encyclopedia.tier_14_part1 import DATA_TIER_14_PART1
from scripts.encyclopedia.tier_14_part2 import DATA_TIER_14_PART2
from scripts.encyclopedia.tier_15_part1 import DATA_TIER_15_PART1
from scripts.encyclopedia.tier_15_part2 import DATA_TIER_15_PART2
from scripts.encyclopedia.tier_16_part1 import DATA_TIER_16_PART1

DATA_TIER_14_16 = {}
DATA_TIER_14_16.update(DATA_TIER_14_PART1)
DATA_TIER_14_16.update(DATA_TIER_14_PART2)
DATA_TIER_14_16.update(DATA_TIER_15_PART1)
DATA_TIER_14_16.update(DATA_TIER_15_PART2)
DATA_TIER_14_16.update(DATA_TIER_16_PART1)
