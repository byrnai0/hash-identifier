# Core matching engine: takes a hash string, returns ranked candidates

from hash_db import HASH_PROTOTYPES, HashPrototype
from typing import List, Tuple

# ─── RESULT OBJECT ────────────────────────────────────────────────────────────
class MatchResult:
    def __init__(self, prototype: HashPrototype, score: int):
        self.name         = prototype.name
        self.hashcat_mode = prototype.hashcat_mode
        self.john_format  = prototype.john_format
        self.description  = prototype.description
        self.tags         = prototype.tags
        self.score        = score  # confidence score 0-100

    def __repr__(self):
        mode = str(self.hashcat_mode) if self.hashcat_mode is not None else "N/A"
        return (f"MatchResult(name={self.name!r}, "
                f"score={self.score}, "
                f"hashcat={mode})")


# ─── MATCHER CLASS ────────────────────────────────────────────────────────────
class HashMatcher:
    """
    Phase 1 engine: regex matching + base-weight ranking.
    Phase 2 will extend this with context multipliers.
    """

    def match(self, hash_input: str) -> List[MatchResult]:
        """
        Run the hash string against all prototypes.
        Returns a list of MatchResult objects sorted by score (highest first).
        """
        hash_input = hash_input.strip()

        if not hash_input:
            return []

        candidates = []

        for prototype in HASH_PROTOTYPES:
            if prototype.regex.fullmatch(hash_input):
                # Phase 1: score = base weight only
                # Phase 2 will multiply by a context factor
                score = prototype.weight
                candidates.append(MatchResult(prototype, score))

        # Sort by score descending, then alphabetically for tie consistency
        candidates.sort(key=lambda r: (-r.score, r.name))

        return candidates

    def match_summary(self, hash_input: str) -> dict:
        """
        Returns a dict — useful later for JSON output mode.
        """
        results = self.match(hash_input)
        return {
            "input": hash_input,
            "length": len(hash_input.strip()),
            "candidates": [
                {
                    "name": r.name,
                    "score": r.score,
                    "hashcat_mode": r.hashcat_mode,
                    "john_format": r.john_format,
                    "description": r.description,
                    "tags": r.tags,
                }
                for r in results
            ]
        }