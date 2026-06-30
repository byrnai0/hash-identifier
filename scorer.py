# scorer.py — HashPilot Phase 3
# Context-aware scoring + application hint boosting

from typing import List, Optional
from hints import get_hint_multiplier

CONTEXT_MULTIPLIERS = {
    "windows": {
        "windows": 2.0,
        "linux":   0.4,
        "web":     0.8,
        "wifi":    0.5,
    },
    "linux": {
        "linux":   2.0,
        "windows": 0.4,
        "web":     0.9,
        "wifi":    0.5,
    },
    "web": {
        "web":      2.0,
        "linux":    0.8,
        "windows":  0.5,
        "wifi":     0.3,
        "database": 1.5,
    },
    "database": {
        "database": 2.0,
        "web":      1.5,
        "linux":    0.9,
        "windows":  0.6,
        "wifi":     0.2,
    },
    "ctf": {
        "ctf":     2.0,
        "web":     1.2,
        "linux":   1.1,
        "windows": 1.1,
        "wifi":    1.3,
    },
    "wifi": {
        "wifi":    3.0,
        "linux":   0.5,
        "windows": 0.5,
        "web":     0.3,
        "database":0.3,
    },
}

VALID_CONTEXTS = list(CONTEXT_MULTIPLIERS.keys())


def get_multiplier(tags: List[str], context: Optional[str]) -> float:
    if not context:
        return 1.0
    context = context.lower().strip()
    if context not in CONTEXT_MULTIPLIERS:
        return 1.0
    table = CONTEXT_MULTIPLIERS[context]
    boosts   = [table[tag] for tag in tags if tag in table and table[tag] >= 1.0]
    penalties= [table[tag] for tag in tags if tag in table and table[tag] < 1.0]
    if boosts:
        return max(boosts)
    elif penalties:
        return min(penalties)
    return 1.0


def compute_score(base_weight: int, hash_name: str,
                  tags: List[str], context: Optional[str] = None,
                  hint: Optional[str] = None) -> int:
    """
    Final score = base_weight × context_multiplier × hint_multiplier
    Capped at 100.
    Phase 3 change: added hash_name and hint parameters.
    """
    context_mult = get_multiplier(tags, context)
    hint_mult    = get_hint_multiplier(hash_name, hint)
    raw_score    = base_weight * context_mult * hint_mult
    return min(100, round(raw_score))