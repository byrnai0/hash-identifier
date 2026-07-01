	___
## How Existing Tools Work (and Their Limits)

All current tools use roughly the same engine:

1. Take the input hash string
2. Run it against a list of regex (regular expression) patterns
3. Return all pattern names that match

___

The code for **Name-The-Hash** which is the base for this project is: 

```python
def identify(self, chash: str):
    chash = chash.strip()
    output = []
    for prototype in self.prototypes:
        if prototype.regex.match(chash):
            for mode in prototype.modes:
                output.append(mode)
    return output
```

All the hash identifiers in the market like that, hash-identifier (kali one), etc are based on this code only. They use the regex parameters and give the answer. If the hash has the same attribute of 2 or more hashing method like md5, sha-256, then these tools will just give the list of all the possible hashing function to which the given hash might belong to, without any ranking logic or a precise answer

___

What I am building:

| Feature                   | Existing Tools               | Your Tool                                                            |
| ------------------------- | ---------------------------- | -------------------------------------------------------------------- |
| **Hash pattern matching** | ✅ Regex-based                | ✅ Regex-based (foundation)                                           |
| **Result count**          | Returns all matches flat     | Confidence-scored ranked list                                    |
| **Tie-breaking**          | Random or hardcoded priority | Heuristic + frequency-weighted disambiguation                    |
| **Context awareness**     | None                         | Optional context flag (e.g., `--context web`, `--context linux`) |
| **Output format**         | Text or JSON                 | Rich CLI table + optional JSON export                            |
| **Packaging**             | Script or pip install        | Standalone `.exe` via PyInstaller                                |

___

## Project Phases — The Roadmap

Here's the full arc of the project, from zero to `.exe`:

## [[Phase 1 — Foundation (Hash Pattern Engine)]]

Build the regex database and the core matching loop. At the end of this phase, you have a working Python script that takes a hash and returns possible types.

## [[Phase 2 — Confidence Scoring System]]

Add logic to rank results. Hashes that are more commonly seen in the wild (MD5, SHA-1, SHA-256, bcrypt) should score higher when there's ambiguity. You'll define a frequency weight per hash type.

## [[Phase 3 — Context-Aware Mode]]

Add an optional `--context` flag where the user can specify where the hash was found (`web`, `linux`, `windows`, `ctf`, `database`). Each context shifts the weights — e.g., NTLM scores higher in `--context windows`, Unix crypt scores higher in `--context linux`.

## [[Phase 4 — CLI Polish]]

Use `rich` to build a clean terminal table, add a `--json` export flag, handle edge cases (empty input, non-hex strings, file input with multiple hashes).

## [[Phase 5 — Packaging]]

Use `PyInstaller` to compile everything into a single `hashid.exe` that runs on any Windows machine from CMD with no Python required.