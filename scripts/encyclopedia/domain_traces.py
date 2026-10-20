# -*- coding: utf-8 -*-
"""
Authentic domain execution traces across all 232 topics.
Merges curated traces from:
- Tiers 00-05 (traces_tier_00_05.py, 87 topics)
- Tiers 06-11 (traces_tier_06_11.py, 95 topics)
- Tiers 12-16 (traces_tier_12_16.py, 50 topics)
"""

from scripts.encyclopedia.remediation.traces_tier_00_05 import TRACES_TIER_00_05
from scripts.encyclopedia.remediation.traces_tier_06_11 import TRACES_TIER_06_11
from scripts.encyclopedia.remediation.traces_tier_12_16 import TRACES_TIER_12_16

DOMAIN_TRACES = {}
DOMAIN_TRACES.update(TRACES_TIER_00_05)
DOMAIN_TRACES.update(TRACES_TIER_06_11)
DOMAIN_TRACES.update(TRACES_TIER_12_16)

if __name__ == "__main__":
    print(f"Loaded DOMAIN_TRACES with {len(DOMAIN_TRACES)} topics.")
    assert len(DOMAIN_TRACES) == 232, f"Expected 232, got {len(DOMAIN_TRACES)}"
    for tid in range(1, 233):
        assert tid in DOMAIN_TRACES, f"Missing trace for topic {tid}"
    print("DOMAIN_TRACES successfully validated across all 232 topics!")