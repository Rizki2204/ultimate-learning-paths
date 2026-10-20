# -*- coding: utf-8 -*-
"""
Authentic historical disaster post-mortems across all 232 topics.
Merges curated postmortems from:
- Tiers 00-05 (postmortems_tier_00_05.py, 87 topics)
- Tiers 06-11 (postmortems_tier_06_11.py, 95 topics)
- Tiers 12-16 (postmortems_tier_12_16.py, 50 topics)
"""

from scripts.encyclopedia.remediation.postmortems_tier_00_05 import POSTMORTEMS_TIER_00_05
from scripts.encyclopedia.remediation.postmortems_tier_06_11 import POSTMORTEMS_TIER_06_11
from scripts.encyclopedia.remediation.postmortems_tier_12_16 import POSTMORTEMS_TIER_12_16

DOMAIN_POSTMORTEMS = {}
DOMAIN_POSTMORTEMS.update(POSTMORTEMS_TIER_00_05)
DOMAIN_POSTMORTEMS.update(POSTMORTEMS_TIER_06_11)
DOMAIN_POSTMORTEMS.update(POSTMORTEMS_TIER_12_16)

# Normalize analysis / forensic keys so both are accessible
for tid, pm in DOMAIN_POSTMORTEMS.items():
    analysis_text = pm.get("analysis") or pm.get("forensic") or ""
    pm["analysis"] = analysis_text
    pm["forensic"] = analysis_text

if __name__ == "__main__":
    print(f"Loaded DOMAIN_POSTMORTEMS with {len(DOMAIN_POSTMORTEMS)} topics.")
    assert len(DOMAIN_POSTMORTEMS) == 232, f"Expected 232, got {len(DOMAIN_POSTMORTEMS)}"
    for tid in range(1, 233):
        assert tid in DOMAIN_POSTMORTEMS, f"Missing postmortem for topic {tid}"
    print("DOMAIN_POSTMORTEMS successfully validated across all 232 topics!")