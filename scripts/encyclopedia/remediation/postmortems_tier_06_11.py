# -*- coding: utf-8 -*-
"""
Authentic Domain Post-Mortems for Tiers 06-11 (Topics 088-182).
"""

from scripts.encyclopedia.remediation.data_tier_06 import DATA_TIER_06
from scripts.encyclopedia.remediation.data_tier_07 import DATA_TIER_07
from scripts.encyclopedia.remediation.data_tier_08 import DATA_TIER_08
from scripts.encyclopedia.remediation.data_tier_09 import DATA_TIER_09
from scripts.encyclopedia.remediation.data_tier_10 import DATA_TIER_10
from scripts.encyclopedia.remediation.data_tier_11 import DATA_TIER_11

POSTMORTEMS_TIER_06_11 = {}

for tier_data in [DATA_TIER_06, DATA_TIER_07, DATA_TIER_08, DATA_TIER_09, DATA_TIER_10, DATA_TIER_11]:
    for tid, content in tier_data.items():
        if "postmortem" in content:
            POSTMORTEMS_TIER_06_11[tid] = content["postmortem"]

if __name__ == "__main__":
    print(f"POSTMORTEMS_TIER_06_11 loaded with {len(POSTMORTEMS_TIER_06_11)} post-mortems (088-182).")
    assert len(POSTMORTEMS_TIER_06_11) == 95, f"Expected 95, got {len(POSTMORTEMS_TIER_06_11)}"
    for tid in range(88, 183):
        assert tid in POSTMORTEMS_TIER_06_11, f"Missing postmortem for topic {tid}"
    print("Post-mortems Tier 06-11 successfully validated!")
