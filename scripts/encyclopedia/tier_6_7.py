# -*- coding: utf-8 -*-
"""
Tier 6 & Tier 7 Aggregated Knowledge Base
Covers Topics 88 - 124 (CS Core, Data Structures, Algorithms, Compilers & Linux OS Internals)
Canonical realignment applied via CANONICAL_TIERS_6_11.
"""

from scripts.encyclopedia.canonical_tiers_6_11 import CANONICAL_TIERS_6_11

DATA_TIER_6_7 = {
    tid: CANONICAL_TIERS_6_11[tid]
    for tid in range(88, 125)
    if tid in CANONICAL_TIERS_6_11
}
