# -*- coding: utf-8 -*-
"""
Authentic Domain Exercises for Tiers 00-05 (Topics 001-087).
"""

from scripts.encyclopedia.remediation.data_tier_00 import DATA_TIER_00
from scripts.encyclopedia.remediation.data_tier_01 import DATA_TIER_01
from scripts.encyclopedia.remediation.data_tier_02 import DATA_TIER_02
from scripts.encyclopedia.remediation.data_tier_03 import DATA_TIER_03
from scripts.encyclopedia.remediation.data_tier_04 import DATA_TIER_04
from scripts.encyclopedia.remediation.data_tier_05 import DATA_TIER_05

EXERCISES_TIER_00_05 = {}

for tier_data in [DATA_TIER_00, DATA_TIER_01, DATA_TIER_02, DATA_TIER_03, DATA_TIER_04, DATA_TIER_05]:
    for tid, content in tier_data.items():
        if "exercise" in content:
            EXERCISES_TIER_00_05[tid] = content["exercise"]

DOMAIN_EXERCISES_TIER_00_05 = EXERCISES_TIER_00_05
