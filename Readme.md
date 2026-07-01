<div align="center">

# HashPilot

**A CLI hash identifier with context-aware confidence scoring**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Phase](https://img.shields.io/badge/Build-v0.4-cyan)

*Identify MD5, SHA-256, bcrypt, NTLM and 35+ other hash types — with ranked confidence scores, context awareness, and application hints*

</div>

---

## What Is HashPilot?

HashPilot is a command-line tool that takes an unknown hash string and identifies what hashing algorithm produced it. Unlike existing tools that return a flat unranked list, HashPilot ranks every result with a **confidence score** based on three factors:

1. **Base weight** — how commonly that hash type appears in the real world
2. **Context** — where the hash was found (Windows environment, Linux system, web app, CTF, etc.)
3. **Application hint** — which specific application generated it (Ethereum, Git, WordPress, Django, etc.)

This makes HashPilot meaningfully smarter than tools like `hashid` or `name-that-hash` for ambiguous cases — for example, MD5 and NTLM are structurally identical (both 32 hex characters), but passing `--context windows` correctly boosts NTLM above MD5.

---

## Features

- **35+ hash types** — MD5, SHA family, bcrypt, NTLM, Unix crypt formats, Argon2, PBKDF2, WPA PMKID, and more
- **Confidence scoring** — every result ranked 0–100, colour-coded green/yellow/orange/red
- **Context-aware ranking** — `--context windows/linux/web/database/ctf/wifi`
- **Application hint system** — `--hint ethereum/git/wordpress/django/mysql/jwt` and more
- **File input mode** — pass a `.txt` file with multiple hashes, identified in one run
- **Rich terminal UI** — coloured tables, panels, score indicators
- **Standalone EXE** — runs on any Windows machine with no Python required

---

## Project Structure

```
hashpilot/
├── hash_db.py    — Hash prototype database (35+ types, regex, weights, tags)
├── scorer.py     — Context-aware scoring engine (multiplier tables)
├── hints.py      — Application hint database (per-app hash boosts)
├── matcher.py    — Core matching engine (regex loop + score calculation)
└── cli.py        — CLI entry point (Rich UI, argument parsing)
```

---

## Installation

**Option 1 — Run from source (requires Python 3.10+)**

```bash
git clone https://github.com/yourusername/hashpilot.git
cd hashpilot
pip install rich
python cli.py
```

**Option 2 — Standalone EXE (Windows, no Python needed)**

Download `hashpilot.exe` from the [Releases](../../releases) page and run directly from CMD.

---

## Usage

```bash
# Identify a single hash
python cli.py 5d41402abc4b2a76b9719d911017c592

# With context — boosts hashes native to that environment
python cli.py --context windows 5d41402abc4b2a76b9719d911017c592

# With application hint — boosts hashes that app is known to use
python cli.py --hint ethereum e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51

# Combine context and hint
python cli.py --context linux --hint git aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d

# File input — one hash per line, # lines are comments
python cli.py --file hashes.txt

# File input with flags
python cli.py --file hashes.txt --context ctf --hint ethereum

# Interactive mode
python cli.py

# Suppress banner
python cli.py --no-banner 5d41402abc4b2a76b9719d911017c592
```

---

## Available Flags

| Flag | Short | Options | What It Does |
|------|-------|---------|--------------|
| `--context` | `-c` | `windows` `linux` `web` `database` `ctf` `wifi` | Boosts hashes native to where the hash was found |
| `--hint` | — | `ethereum` `bitcoin` `git` `linux` `wordpress` `django` `windows` `mysql` `jwt` `wifi` | Boosts hashes that specific application uses |
| `--file` | `-f` | path to `.txt` file | Identify multiple hashes from a file |
| `--no-banner` | — | — | Suppress the ASCII banner |

---

## How the Scoring Works

Every candidate hash gets a score calculated as:

```
score = min(100, round(base_weight × context_multiplier × hint_multiplier))
```

- **`base_weight`** (1–100): defined per hash type in `hash_db.py`. MD5 = 95, Keccak-256 = 35.
- **`context_multiplier`**: from `scorer.py`. e.g. in `--context windows`, NTLM gets `×2.0`, Linux hashes get `×0.4`.
- **`hint_multiplier`**: from `hints.py`. e.g. `--hint ethereum` gives Keccak-256 `×4.0`, SHA-256 `×0.5`.

Scores are colour-coded in the terminal:

| Score | Colour | Meaning |
|-------|--------|---------|
| 80–100 | 🟢 Green | High confidence |
| 50–79 | 🟡 Yellow | Medium confidence |
| 25–49 | 🟠 Orange | Low confidence |
| 0–24 | 🔴 Red | Very unlikely |

---

## Sample Output

```
╭─ HashPilot ──────────────────────────────────────╮
│  Input   : 5d41402abc4b2a76b9719d911017c592       │
│  Length  : 32 characters                          │
│  Context : windows                                │
╰───────────────────────────────────────────────────╯

  #    Hash Name                 Score    Hashcat    John          Tags
  ╭────────────────────────────────────────────────────────────────────╮
  │  1  ★ NTLM                    100      1000       nt             windows, ctf       │
  │  2    MD5                      76      0          raw-md5        web, linux, ctf    │
  │  3    MD4                      30      900        raw-md4        windows, ctf       │
  │  4    LM (LAN Manager)         20      3000       lm             windows            │
  ╰────────────────────────────────────────────────────────────────────╯

  ★ Most likely: NTLM — Windows authentication hash. Visually identical to MD5.
```

---

## Sample Hashes for Testing

| Hash Type | Sample Value |
|-----------|-------------|
| MD5 | `5d41402abc4b2a76b9719d911017c592` |
| SHA-1 | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| SHA-256 | `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` |
| SHA-512 | `9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043` |
| bcrypt | `$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW` |
| Keccak-256 (Ethereum) | `e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51` |

---

## Known Limitations

Hashes that share identical structure (same length, same character set) **cannot be distinguished by regex alone**. This is a limitation of all pattern-based hash identifiers, not just HashPilot:

| Ambiguous Pair | Length | Why |
|----------------|--------|-----|
| MD5 / NTLM | 32 hex | Identical structure |
| SHA-256 / SHA3-256 / Keccak-256 | 64 hex | Identical structure |
| SHA-512 / BLAKE2b-512 | 128 hex | Identical structure |
| SHA-1 / RIPEMD-160 | 40 hex | Identical structure |

For these pairs, use `--context` and `--hint` to get the most accurate ranking. The tool will always give you its best-weighted guess but cannot be 100% certain.

---

## Building the EXE

```bash
pip install pyinstaller
pyinstaller --onefile --name hashpilot cli.py
# Output: dist/hashpilot.exe
```

---

## What Makes HashPilot Different

| Feature | hashid | name-that-hash | HashPilot |
|---------|--------|----------------|-----------|
| Hash pattern matching | ✅ | ✅ | ✅ |
| Ranked results | ❌ | Partial | ✅ |
| Confidence scores | ❌ | ❌ | ✅ |
| Context-aware ranking | ❌ | ❌ | ✅ |
| Application hints | ❌ | ❌ | ✅ |
| File input mode | ✅ | ✅ | ✅ |
| Standalone EXE | ❌ | ❌ | ✅ |

---

## License

MIT License — free to use, modify and distribute.
