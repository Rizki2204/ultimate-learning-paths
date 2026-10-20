"""Tier 12 and 13 aggregator: Topics 183 - 206
"""
from scripts.encyclopedia.tier_12_part1 import DATA_TIER_12_PART1
from scripts.encyclopedia.tier_12_part2 import DATA_TIER_12_PART2
from scripts.encyclopedia.tier_13_part1 import DATA_TIER_13_PART1
from scripts.encyclopedia.tier_13_part2 import DATA_TIER_13_PART2

DATA_TIER_12_13 = {}
DATA_TIER_12_13.update(DATA_TIER_12_PART1)
DATA_TIER_12_13.update(DATA_TIER_12_PART2)
DATA_TIER_12_13.update(DATA_TIER_13_PART1)
DATA_TIER_12_13.update(DATA_TIER_13_PART2)
