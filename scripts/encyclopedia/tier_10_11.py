# -*- coding: utf-8 -*-
"""
Tier 10 & Tier 11 Aggregated Knowledge Base
Covers Topics 157 - 182 (Databases, Enterprise Systems, Cybersecurity & Reverse Engineering)
Canonical realignment applied via CANONICAL_TIERS_6_11.
"""

from scripts.encyclopedia.canonical_tiers_6_11 import CANONICAL_TIERS_6_11

DATA_TIER_10_11 = {
    tid: CANONICAL_TIERS_6_11[tid]
    for tid in range(157, 183)
    if tid in CANONICAL_TIERS_6_11
}
