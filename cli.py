# CLI entry point. Run: python cli.py <hash>
# Uses only Python stdlib (no rich yet — that comes in Phase 4)

import sys
import argparse
from matcher import HashMatcher

# ─── BANNER ───────────────────────────────────────────────────────────────────
BANNER = r"""
  _  _         _    ___ _ _     _
 | || |__ _ __| |_ | _ (_) |___| |_
 | __ / _` (_-< ' \|  _/ | / _ \  _|
 |_||_\__,_/__/_||_|_| |_|_\___/\__|

  Hash Identifier v0.1  |  Phase 1 Build
  ----------------------------------------
"""

# ─── DISPLAY ──────────────────────────────────────────────────────────────────
def print_results(hash_input: str, results: list):
    print(f"\n  Input  : {hash_input}")
    print(f"  Length : {len(hash_input.strip())} characters\n")

    if not results:
        print("  [!] No matching hash type found.")
        print("  Tip: Make sure the hash is complete and not truncated.\n")
        return

    print(f"  Found {len(results)} possible match(es):\n")
    print(f"  {'#':<4} {'Hash Name':<30} {'Score':<8} {'Hashcat':<10} {'John':<18} Tags")
    print("  " + "-" * 85)

    for i, r in enumerate(results, 1):
        mode   = str(r.hashcat_mode) if r.hashcat_mode is not None else "—"
        john   = r.john_format if r.john_format else "—"
        tags   = ", ".join(r.tags)
        marker = " <-- most likely" if i == 1 else ""
        print(f"  {i:<4} {r.name:<30} {r.score:<8} {mode:<10} {john:<18} {tags}{marker}")

    print()
    print(f"  [i] Description of top match:")
    print(f"      {results[0].description}\n")


# ─── ARGUMENT PARSER ──────────────────────────────────────────────────────────
def build_parser():
    parser = argparse.ArgumentParser(
        prog="hashpilot",
        description="HashPilot — identify hash types with confidence scoring",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "hash",
        nargs="?",
        help="The hash string to identify"
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress the ASCII banner"
    )
    return parser


# ─── MAIN LOOP ────────────────────────────────────────────────────────────────
def main():
    parser = build_parser()
    args = parser.parse_args()

    matcher = HashMatcher()

    if not args.no_banner:
        print(BANNER)

    # If hash passed as argument, run once and exit
    if args.hash:
        results = matcher.match(args.hash)
        print_results(args.hash, results)
        return

    # Interactive mode: keep asking for hashes until user types 'exit'
    print("  Interactive mode — type a hash and press Enter.")
    print("  Type 'exit' or press Ctrl+C to quit.\n")

    while True:
        try:
            user_input = input("  hashpilot> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Bye!\n")
            break

        if user_input.lower() in ("exit", "quit", "q"):
            print("\n  Bye!\n")
            break

        if not user_input:
            continue

        results = matcher.match(user_input)
        print_results(user_input, results)


if __name__ == "__main__":
    main()