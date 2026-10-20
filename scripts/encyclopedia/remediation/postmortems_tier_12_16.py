# -*- coding: utf-8 -*-
"""
Authentic Domain Post-Mortems for Tiers 12-16 (Topics 183-232).
"""

from scripts.encyclopedia.remediation.data_tier_12 import DATA_TIER_12
from scripts.encyclopedia.remediation.data_tier_13 import DATA_TIER_13
from scripts.encyclopedia.remediation.data_tier_14 import DATA_TIER_14
from scripts.encyclopedia.remediation.data_tier_15 import DATA_TIER_15
from scripts.encyclopedia.remediation.data_tier_16 import DATA_TIER_16

POSTMORTEMS_TIER_12_16 = {}

for tier_data in [DATA_TIER_12, DATA_TIER_13, DATA_TIER_14, DATA_TIER_15, DATA_TIER_16]:
    for tid, content in tier_data.items():
        if "postmortem" in content:
            POSTMORTEMS_TIER_12_16[tid] = content["postmortem"]

if __name__ == "__main__":
    print(f"POSTMORTEMS_TIER_12_16 loaded with {len(POSTMORTEMS_TIER_12_16)} post-mortems (183-232).")
    assert len(POSTMORTEMS_TIER_12_16) == 50, f"Expected 50, got {len(POSTMORTEMS_TIER_12_16)}"
    for tid in range(183, 233):
        assert tid in POSTMORTEMS_TIER_12_16, f"Missing postmortem for topic {tid}"
    print("Post-mortems Tier 12-16 successfully validated!")
