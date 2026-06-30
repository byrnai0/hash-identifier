# cli.py — HashPilot Phase 3
# Added: --file and --hint flags

import argparse
from matcher import HashMatcher
from scorer import VALID_CONTEXTS
from hints import VALID_HINTS

BANNER = r"""
  _  _         _    ___ _ _     _
 | || |__ _ __| |_ | _ (_) |___| |_
 | __ / _` (_-< ' \|  _/ | / _ \  _|
 |_||_\__,_/__/_||_|_| |_|_\___/\__|

  HashPilot v0.3  |  Phase 3 — File Input + App Hints
  ------------------------------------------------------
"""


def print_results(hash_input: str, results: list,
                  context: str = None, hint: str = None):
    print(f"\n  Input   : {hash_input}")
    print(f"  Length  : {len(hash_input.strip())} characters")
    if context:
        print(f"  Context : {context}")
    if hint:
        print(f"  Hint    : {hint}")
    print()

    if not results:
        print("  [!] No matching hash type found.")
        print("  Tip: Make sure the hash is complete and not truncated.\n")
        return

    print(f"  Found {len(results)} possible match(es):\n")
    print(f"  {'#':<4} {'Hash Name':<30} {'Score':<8} {'Hashcat':<10} {'John':<18} Tags")
    print("  " + "-" * 88)

    for i, r in enumerate(results, 1):
        mode   = str(r.hashcat_mode) if r.hashcat_mode is not None else "—"
        john   = r.john_format if r.john_format else "—"
        tags   = ", ".join(r.tags)
        marker = "  <-- most likely" if i == 1 else ""
        print(f"  {i:<4} {r.name:<30} {r.score:<8} {mode:<10} {john:<18} {tags}{marker}")

    print(f"\n  [i] {results[0].description}\n")


def process_file(filepath: str, matcher: HashMatcher,
                 context: str, hint: str):
    """Read a file of hashes (one per line) and identify each one."""
    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()
                     and not line.startswith("#")]
    except FileNotFoundError:
        print(f"\n  [!] File not found: {filepath}\n")
        return

    if not lines:
        print("\n  [!] File is empty or has no valid hash lines.\n")
        return

    print(f"\n  Processing {len(lines)} hash(es) from '{filepath}'...\n")
    print("  " + "=" * 88)

    for hash_input in lines:
        results = matcher.match(hash_input, context=context, hint=hint)
        print_results(hash_input, results, context=context, hint=hint)
        print("  " + "-" * 88)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="hashpilot",
        description="HashPilot — identify hash types with confidence scoring"
    )
    parser.add_argument(
        "hash",
        nargs="?",
        help="Single hash string to identify"
    )
    parser.add_argument(
        "--file", "-f",
        metavar="FILE",
        help="Path to a .txt file with one hash per line"
    )
    parser.add_argument(
        "--context", "-c",
        choices=VALID_CONTEXTS,
        default=None,
        help=f"Where the hash was found: {', '.join(VALID_CONTEXTS)}"
    )
    parser.add_argument(
        "--hint",
        choices=VALID_HINTS,
        default=None,
        help=f"Application that generated the hash: {', '.join(VALID_HINTS)}"
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress banner"
    )
    return parser


def main():
    parser  = build_parser()
    args    = parser.parse_args()
    matcher = HashMatcher()

    if not args.no_banner:
        print(BANNER)

    # File mode
    if args.file:
        process_file(args.file, matcher,
                     context=args.context, hint=args.hint)
        return

    # Single hash argument mode
    if args.hash:
        results = matcher.match(args.hash,
                                context=args.context,
                                hint=args.hint)
        print_results(args.hash, results,
                      context=args.context, hint=args.hint)
        return

    # Interactive mode
    print("  Interactive mode — type a hash and press Enter.")
    print(f"  Tip: run with --context [{'/'.join(VALID_CONTEXTS)}] for smarter results.")
    print(f"  Tip: run with --hint [{'/'.join(VALID_HINTS)}] to boost app-specific hashes.")
    print("  Type 'exit' to quit.\n")

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

        results = matcher.match(user_input,
                                context=args.context,
                                hint=args.hint)
        print_results(user_input, results,
                      context=args.context, hint=args.hint)


if __name__ == "__main__":
    main()