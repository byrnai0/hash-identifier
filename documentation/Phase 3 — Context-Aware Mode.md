___

Phase 3 added two major features on top of the context scoring from Phase 2:

1. **File input mode** (`--file`) — pass a `.txt` file with one hash per line
   and identify all of them in one run, instead of entering them one by one
2. **Application hint system** (`--hint`) — tell the tool which application
   generated the hash, triggering large targeted score boosts for hash types
   that application is known to use

The hint system directly solved the SHA-256 vs SHA3-256 problem I
discovered in Phase 2 — two hashes that are structurally identical but can
be disambiguated if you know the source application.

___

## The New File: `hints.py`

This file is the application hint database. It's structured as a nested dict:

```bash
HINT_BOOSTS = {
"application_name": {
"Hash Name": multiplier,
...
}
}
```

Applications covered: `ethereum`, `bitcoin`, `git`, `linux`, `wordpress`,
`django`, `windows`, `mysql`, `jwt`, `wifi`

The multipliers work the same way as context multipliers — values above 1.0
are boosts, values below 1.0 are penalties. A hash type not listed under a
hint gets a neutral `1.0`.

Key function: `get_hint_multiplier(hash_name, hint)`: looks up a hash by
its exact name string and returns the multiplier. Returns 1.0 if no match.

___

## How the Full Score Formula Now Looks

$$
score = min(100, round(baseWeight × contextMultiplier × hintMultiplier))
$$

Three factors now feed into every score:
- `base_weight` — how common the hash is globally (from hash_db.py)
- `context_multiplier` — where it was found (from scorer.py, Phase 2)
- `hint_multiplier` — which app generated it (from hints.py, Phase 3)

All three are independent and multiply together. If no context or hint is
supplied, both multipliers default to 1.0, preserving Phase 1 behavior.

___

## Testing

```bash
# Hint test — Keccak-256 should score 100
python cli.py --hint ethereum e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51

# Windows hint — NTLM should dominate
python cli.py --hint windows 5d41402abc4b2a76b9719d911017c592

# Git hint — SHA-1 should dominate
python cli.py --hint git aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d

# File mode
python cli.py --file hashes.txt

# File + context + hint combined
python cli.py --file hashes.txt --context ctf --hint ethereum

# Django hint
python cli.py --hint django "pbkdf2_sha256$260000$abc123$abcdefghijklmnopqrstuvwxyz012345678901234567=="
```

Example:
- without ethereum hint:

```
python cli.py e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51
```

![[Pasted image 20260630143357.png]]

- with ethereum hint:

```bash
python cli.py --hint ethereum e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51
```

![[Pasted image 20260630143431.png]]

With the hint, we can also add context flag as well which increases the score of the hashes.

```bash
python cli.py --context windows --hint windows 5d41402abc4b2a76b9719d911017c592
```

![[Pasted image 20260630143652.png]]

___

## File Input Format

The tool also now checks for the hash values that are in a text file and returns the output for each of the hash in the cli.

Here are the steps for this:

1. Create a `.txt` file with one hash per line
	Example file has these values:

```
MD5 hash
5d41402abc4b2a76b9719d911017c592

SHA-256 hash
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

bcrypt
$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
```

2. Run it with this:

```bash
python cli.py --file hashes.txt
python cli.py --file hashes.txt --context ctf
python cli.py --file hashes.txt --context ctf --hint ethereum
```

3. Expected output:

![[Pasted image 20260630144404.png]]
___

## Fine-Tuning I Did After Testing

After seeing the initial output, I noticed BLAKE2s-256 ranked above SHA3-256
in the Ethereum context because it had no hint entry and defaulted to
neutral `1.0`, giving it `25 × 1.0 = 25`. That was wrong as BLAKE2s has
nothing to do with Ethereum.

Fix: added explicit penalties for non-Ethereum hashes in the ethereum hint:
```python
"ethereum": {
    "Keccak-256":  4.0,
    "SHA-256":     0.5,
    "SHA3-256":    0.8,
    "BLAKE2s-256": 0.5,
    "BLAKE2b-256": 0.5,
    "HMAC-SHA256": 0.4,
},
```

**Lesson:** When writing hint entries, don't just add boosts for relevant
hashes, also add explicit penalties for irrelevant ones that might otherwise
float up due to their base weight.

And, I raised Keccak-256 base weight in `hash_db.py` from `20` to `35`.
Ethereum has made Keccak-256 mainstream enough that its global frequency
warranted a higher base weight, independent of any hint.

With `weight=35` and `hint_multiplier=4.0`:
`35 × 4.0 = 140` → capped at **100**

___

## Known Remaining Limitation

Hint + context stacking works but can produce confusing results if the two
flags contradict each other. For example, `--context linux --hint windows`
will create a tug-of-war between the Linux context (penalising windows tags)
and the Windows hint (boosting NTLM). The tool handles this mathematically
but doesn't warn the user about the contradiction. A future improvement
would be to detect and warn when context and hint conflict.