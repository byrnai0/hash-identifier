# matcher.py — HashPilot Phase 3
# Added: hint parameter threading

from hash_db import HASH_PROTOTYPES, HashPrototype
from scorer import compute_score
from typing import List, Optional


class MatchResult:
    def __init__(self, prototype: HashPrototype, score: int):
        self.name         = prototype.name
        self.hashcat_mode = prototype.hashcat_mode
        self.john_format  = prototype.john_format
        self.description  = prototype.description
        self.tags         = prototype.tags
        self.score        = score

    def __repr__(self):
        mode = str(self.hashcat_mode) if self.hashcat_mode is not None else "N/A"
        return f"MatchResult(name={self.name!r}, score={self.score}, hashcat={mode})"


class HashMatcher:

    def match(self, hash_input: str,
              context: Optional[str] = None,
              hint: Optional[str] = None) -> List[MatchResult]:

        hash_input = hash_input.strip()
        if not hash_input:
            return []

        candidates = []
        for prototype in HASH_PROTOTYPES:
            if prototype.regex.fullmatch(hash_input):
                score = compute_score(
                    prototype.weight,
                    prototype.name,       # Phase 3: pass name for hint lookup
                    prototype.tags,
                    context=context,
                    hint=hint
                )
                candidates.append(MatchResult(prototype, score))

        candidates.sort(key=lambda r: (-r.score, r.name))
        return candidates

    def match_summary(self, hash_input: str,
                      context: Optional[str] = None,
                      hint: Optional[str] = None) -> dict:
        results = self.match(hash_input, context, hint)
        return {
            "input":      hash_input,
            "length":     len(hash_input.strip()),
            "context":    context or "none",
            "hint":       hint or "none",
            "candidates": [
                {
                    "name":         r.name,
                    "score":        r.score,
                    "hashcat_mode": r.hashcat_mode,
                    "john_format":  r.john_format,
                    "description":  r.description,
                    "tags":         r.tags,
                }
                for r in results
            ]
        }