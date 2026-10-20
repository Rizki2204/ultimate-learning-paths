# -*- coding: utf-8 -*-
"""
Authentic Domain Traces for Tiers 06-11 (Topics 088-182).
"""

from scripts.encyclopedia.remediation.data_tier_06 import DATA_TIER_06
from scripts.encyclopedia.remediation.data_tier_07 import DATA_TIER_07
from scripts.encyclopedia.remediation.data_tier_08 import DATA_TIER_08
from scripts.encyclopedia.remediation.data_tier_09 import DATA_TIER_09
from scripts.encyclopedia.remediation.data_tier_10 import DATA_TIER_10
from scripts.encyclopedia.remediation.data_tier_11 import DATA_TIER_11

TRACES_TIER_06_11 = {}

for tier_data in [DATA_TIER_06, DATA_TIER_07, DATA_TIER_08, DATA_TIER_09, DATA_TIER_10, DATA_TIER_11]:
    for tid, content in tier_data.items():
        if "trace" in content:
            TRACES_TIER_06_11[tid] = content["trace"]

if __name__ == "__main__":
    print(f"TRACES_TIER_06_11 loaded with {len(TRACES_TIER_06_11)} traces (088-182).")
    assert len(TRACES_TIER_06_11) == 95, f"Expected 95, got {len(TRACES_TIER_06_11)}"
    for tid in range(88, 183):
        assert tid in TRACES_TIER_06_11, f"Missing trace for topic {tid}"
    print("Traces Tier 06-11 successfully validated!")
