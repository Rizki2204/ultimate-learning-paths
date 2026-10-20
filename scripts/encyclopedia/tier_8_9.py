# -*- coding: utf-8 -*-
"""
Tier 8 & Tier 9 Aggregated Knowledge Base
Covers Topics 125 - 156 (DSP, Wireless, Networks, Distributed Systems, Software Eng, DevOps & SRE)
Canonical realignment applied via CANONICAL_TIERS_6_11.
"""

from scripts.encyclopedia.canonical_tiers_6_11 import CANONICAL_TIERS_6_11

DATA_TIER_8_9 = {
    tid: CANONICAL_TIERS_6_11[tid]
    for tid in range(125, 157)
    if tid in CANONICAL_TIERS_6_11
}
