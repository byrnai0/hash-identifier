# cli.py — HashPilot Phase 4
# Rich CLI: coloured tables, panels, styled output

import argparse
from matcher import HashMatcher
from scorer import VALID_CONTEXTS
from hints import VALID_HINTS

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

BANNER = r"""[bold cyan]
  ╔═══════════════════════╗
  ║   H A S H P I L O T   ║
  ╚═══════════════════════╝
[/bold cyan]
[dim]  Identify hashes with confidence scoring![/dim]
[dim]  ----------------------------------------[/dim]
"""

def score_colour(score: int) -> str:
    """Return a rich colour string based on the score value."""
    if score >= 80:
        return "bold green"
    elif score >= 50:
        return "yellow"
    elif score >= 25:
        return "orange3"
    else:
        return "red"


def print_results(hash_input: str, results: list,
                  context: str = None, hint: str = None):

    # ── Input summary panel ───────────────────────────────────────────────────
    info_lines = [f"[bold]Input  :[/bold] [cyan]{hash_input}[/cyan]"]
    info_lines.append(f"[bold]Length :[/bold] {len(hash_input.strip())} characters")
    if context:
        info_lines.append(f"[bold]Context:[/bold] [magenta]{context}[/magenta]")
    if hint:
        info_lines.append(f"[bold]Hint   :[/bold] [blue]{hint}[/blue]")

    console.print(Panel(
        "\n".join(info_lines),
        title="[bold white]HashPilot[/bold white]",
        border_style="cyan",
        padding=(0, 2)
    ))

    if not results:
        console.print(
            Panel(
                "[bold red][!] No matching hash type found.[/bold red]\n"
                "[dim]Tip: Make sure the hash is complete and not truncated.[/dim]",
                border_style="red"
            )
        )
        return

    # ── Results table ─────────────────────────────────────────────────────────
    table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold white on dark_cyan",
        show_lines=False,
        padding=(0, 1)
    )

    table.add_column("#",         style="dim",        width=4,  justify="right")
    table.add_column("Hash Name", style="bold white",  width=30)
    table.add_column("Score",                          width=8,  justify="center")
    table.add_column("Hashcat",   style="dim cyan",   width=10, justify="center")
    table.add_column("John",      style="dim cyan",   width=16)
    table.add_column("Tags",      style="dim white")

    for i, r in enumerate(results, 1):
        mode  = str(r.hashcat_mode) if r.hashcat_mode is not None else "—"
        john  = r.john_format if r.john_format else "—"
        tags  = ", ".join(r.tags)
        col   = score_colour(r.score)

        # Highlight the top result row
        if i == 1:
            name_text = Text(f"★ {r.name}", style="bold green")
        else:
            name_text = Text(f"  {r.name}", style="white")

        table.add_row(
            str(i),
            name_text,
            Text(str(r.score), style=col),
            mode,
            john,
            tags
        )

    console.print(table)

    # ── Description of top match ──────────────────────────────────────────────
    console.print(
        f"  [bold green]★ Most likely:[/bold green] "
        f"[white]{results[0].name}[/white] — "
        f"[dim]{results[0].description}[/dim]\n"
    )


def process_file(filepath: str, matcher: HashMatcher,
                 context: str, hint: str):
    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f
                     if line.strip() and not line.strip().startswith("#")]
    except FileNotFoundError:
        console.print(f"\n[bold red][!] File not found:[/bold red] {filepath}\n")
        return

    if not lines:
        console.print("\n[yellow][!] File is empty or has no valid hash lines.[/yellow]\n")
        return

    console.print(f"\n[bold cyan]Processing {len(lines)} hash(es) from '[white]{filepath}[/white]'...[/bold cyan]\n")

    for i, hash_input in enumerate(lines, 1):
        console.rule(f"[dim]Hash {i} of {len(lines)}[/dim]")
        results = matcher.match(hash_input, context=context, hint=hint)
        print_results(hash_input, results, context=context, hint=hint)

    console.rule("[dim]Done[/dim]")


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
        console.print(BANNER)

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
    console.print("[bold]Interactive mode[/bold] — type a hash and press Enter.")
    console.print(f"[dim]Tip: use --context [{'/'.join(VALID_CONTEXTS)}][/dim]")
    console.print(f"[dim]Tip: use --hint [{'/'.join(VALID_HINTS)}][/dim]")
    console.print("[dim]Type 'exit' to quit.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]hashpilot>[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye![/dim]\n")
            break

        if user_input.lower() in ("exit", "quit", "q"):
            console.print("\n[dim]Bye![/dim]\n")
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