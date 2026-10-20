# scripts/domain_generators.py
"""
Domain generators with rigorous domain-specific knowledge engines for all 17 Tiers.
"""

def build_domain_content(topic_id, slug, full_title, tier_idx):
    # Specialized generator dispatch
    if tier_idx == 0:
        return _gen_tier_0(topic_id, slug, full_title)
    elif tier_idx == 1:
        return _gen_tier_1(topic_id, slug, full_title)
    elif tier_idx == 2:
        return _gen_tier_2(topic_id, slug, full_title)
    elif tier_idx == 3:
        return _gen_tier_3(topic_id, slug, full_title)
    elif tier_idx == 4:
        return _gen_tier_4(topic_id, slug, full_title)
    elif tier_idx == 5:
        return _gen_tier_5(topic_id, slug, full_title)
    elif tier_idx == 6:
        return _gen_tier_6(topic_id, slug, full_title)
    elif tier_idx == 7:
        return _gen_tier_7(topic_id, slug, full_title)
    elif tier_idx == 8:
        return _gen_tier_8(topic_id, slug, full_title)
    elif tier_idx == 9:
        return _gen_tier_9(topic_id, slug, full_title)
    elif tier_idx == 10:
        return _gen_tier_10(topic_id, slug, full_title)
    elif tier_idx == 11:
        return _gen_tier_11(topic_id, slug, full_title)
    elif tier_idx == 12:
        return _gen_tier_12(topic_id, slug, full_title)
    elif tier_idx == 13:
        return _gen_tier_13(topic_id, slug, full_title)
    elif tier_idx == 14:
        return _gen_tier_14(topic_id, slug, full_title)
    elif tier_idx == 15:
        return _gen_tier_15(topic_id, slug, full_title)
    elif tier_idx == 16:
        return _gen_tier_16(topic_id, slug, full_title)
    else:
        return _gen_generic(topic_id, slug, full_title, tier_idx)

# Generators for each tier with comprehensive domain logic
from scripts.tier_modules_0_3 import _gen_tier_0, _gen_tier_1, _gen_tier_2, _gen_tier_3
from scripts.tier_modules_4_7 import _gen_tier_4, _gen_tier_5, _gen_tier_6, _gen_tier_7
from scripts.tier_modules_8_11 import _gen_tier_8, _gen_tier_9, _gen_tier_10, _gen_tier_11
from scripts.tier_modules_12_16 import _gen_tier_12, _gen_tier_13, _gen_tier_14, _gen_tier_15, _gen_tier_16

def _gen_generic(topic_id, slug, full_title, tier_idx):
    return {
        "intuition": f"Intuisi mendasar mengenai {full_title}.",
        "theory": f"Fondasi teori formal dan model matematis untuk {full_title}.",
        "internals": f"Anatomi internal sistem dan alur eksekusi untuk {full_title}.",
        "code_block": "```python\n# Implementasi referensi\n```",
        "pitfalls": "Jebakan umum dan miskonsepsi.",
        "exercises": "Latihan berjenjang tingkat 1 s/d 3.",
        "references": "- Buku teks standar referensi."
    }
