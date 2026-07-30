#!/usr/bin/env python3
"""Export SKILL.md as rule files for AI coding assistants.

Writes the Diataxis guide to the rule-file path each assistant reads, adding
the frontmatter that tool requires so the exported file is actually loaded.

Two things are worth knowing before you run this:

1.  Several targets are *always-on* context. Cline, Roo Code, Copilot, Claude
    Code, Codex, Aider, Gemini CLI, and Amazon Q load their rule file into
    every request in the project. Exporting the full SKILL.md there costs
    roughly 5k tokens per request. Use --compact for those.
2.  Tool-specific formats are not interchangeable. Cursor ignores plain .md
    files in .cursor/rules (they must be .mdc), and Windsurf workspace rules
    are capped at 12,000 characters. This script writes the correct extension
    and warns when a file exceeds a documented limit.

Usage:
    python scripts/export_rules.py --list
    python scripts/export_rules.py --dry-run
    python scripts/export_rules.py --only claude --only cursor --compact
    python scripts/export_rules.py --target ../my-project --force
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

SOURCE_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = SOURCE_ROOT / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)

RULE_DESCRIPTION = (
    "Diataxis documentation guide: classify a docs request as tutorial, how-to, "
    "reference, or explanation, and write it in the right form."
)

# Sections kept by --compact, matched on the H2 heading text.
COMPACT_SECTIONS = [
    "The Diataxis compass",
    "Quick decision tree",
    "When NOT to use this skill",
    "Anti-patterns: what NOT to do",
    "Quality checks",
]

PREAMBLE = (
    "# Diataxis Documentation Guide\n"
    "\n"
    "A systematic approach to technical documentation based on the Diataxis "
    "framework. Use it to classify what the reader needs and structure "
    "documentation accordingly, as a guide rather than a rigid template.\n"
    "\n"
    "---\n"
    "\n"
)


@dataclass(frozen=True)
class Target:
    """One assistant's rule file."""

    key: str
    name: str
    path: Path
    frontmatter: dict[str, str] = field(default_factory=dict)
    char_limit: int | None = None
    always_on: bool = True
    note: str = ""


# Ordered by tool. `always_on` marks targets whose content enters every request
# in the project, which is where --compact matters most.
TARGETS: list[Target] = [
    Target(
        key="cursor",
        name="Cursor",
        path=Path(".cursor/rules/diataxis.mdc"),
        frontmatter={"description": RULE_DESCRIPTION, "alwaysApply": "false"},
        always_on=False,
        note="Must be .mdc; Cursor ignores plain .md files in .cursor/rules.",
    ),
    Target(
        key="cursor-legacy",
        name="Cursor (legacy)",
        path=Path(".cursorrules"),
        note="Deprecated by Cursor. Do not use alongside .cursor/rules.",
    ),
    Target(key="cline", name="Cline", path=Path(".clinerules")),
    Target(
        key="roo",
        name="Roo Code",
        path=Path(".roo/rules/diataxis.md"),
        note="Roo loads every file in .roo/rules, so this is always-on context.",
    ),
    Target(
        key="windsurf",
        name="Windsurf",
        path=Path(".windsurf/rules/diataxis.md"),
        frontmatter={"trigger": "model_decision", "description": RULE_DESCRIPTION},
        char_limit=12000,
        always_on=False,
        note="Workspace rules are capped at 12,000 characters.",
    ),
    Target(
        key="windsurf-legacy",
        name="Windsurf (legacy)",
        path=Path(".windsurfrules"),
        char_limit=6000,
        note="Legacy single-file format; prefer .windsurf/rules.",
    ),
    Target(key="copilot", name="GitHub Copilot", path=Path(".github/copilot-instructions.md")),
    Target(key="claude", name="Claude Code", path=Path("CLAUDE.md")),
    Target(key="codex", name="OpenAI Codex", path=Path("AGENTS.md")),
    Target(key="aider", name="Aider", path=Path("CONVENTIONS.md")),
    Target(key="gemini", name="Gemini CLI", path=Path("GEMINI.md")),
    Target(
        key="continue",
        name="Continue",
        path=Path(".continue/rules/diataxis.md"),
        frontmatter={
            "name": "Diataxis Documentation Guide",
            "description": RULE_DESCRIPTION,
            "alwaysApply": "false",
        },
        always_on=False,
    ),
    Target(key="amazonq", name="Amazon Q Developer", path=Path(".amazonq/rules/diataxis.md")),
]


def strip_frontmatter(content: str) -> str:
    """Remove a leading YAML frontmatter block.

    Uses an anchored regex rather than a naive split on '---', which would be
    broken by a thematic break or a table separator in the body.
    """
    return FRONTMATTER_RE.sub("", content, count=1).strip()


def extract_sections(body: str, headings: Sequence[str]) -> tuple[str, list[str]]:
    """Return the requested H2 sections in document order, plus any missing ones."""
    lines = body.splitlines()
    wanted = {heading.strip().casefold(): heading for heading in headings}
    found: set[str] = set()
    collected: list[str] = []
    keeping = False

    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip().casefold()
            keeping = title in wanted
            if keeping:
                found.add(title)
        elif line.startswith("# "):
            keeping = False
        if keeping:
            collected.append(line)

    missing = [wanted[key] for key in wanted if key not in found]
    return "\n".join(collected).strip(), sorted(missing)


def render_frontmatter(fields: dict[str, str]) -> str:
    if not fields:
        return ""
    lines = ["---"]
    for key, value in fields.items():
        needs_quotes = any(char in value for char in ":#") and not value.startswith('"')
        lines.append(f'{key}: "{value}"' if needs_quotes else f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def build_content(target: Target, body: str) -> str:
    return render_frontmatter(target.frontmatter) + PREAMBLE + body + "\n"


def approx_tokens(text: str) -> int:
    """Very rough token estimate for context-cost reporting."""
    return len(text) // 4


def select_targets(keys: Sequence[str]) -> tuple[list[Target], list[str]]:
    if not keys:
        return list(TARGETS), []
    by_key = {target.key: target for target in TARGETS}
    selected = [by_key[key] for key in keys if key in by_key]
    unknown = [key for key in keys if key not in by_key]
    return selected, unknown


def print_target_table() -> None:
    width = max(len(target.key) for target in TARGETS)
    print(f"{len(TARGETS)} rule-file targets across 11 assistants:\n")
    print(f"{'KEY'.ljust(width)}  {'TOOL'.ljust(20)}  {'ALWAYS-ON'.ljust(9)}  PATH")
    for target in TARGETS:
        always = "yes" if target.always_on else "no"
        print(f"{target.key.ljust(width)}  {target.name.ljust(20)}  {always.ljust(9)}  {target.path.as_posix()}")
    print("\nAlways-on targets enter every request in the project. Use --compact for those.")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export SKILL.md as rule files for AI coding assistants.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Project to export into (default: cwd)")
    parser.add_argument("--only", action="append", default=[], metavar="KEY", help="Export one target key. Repeatable.")
    parser.add_argument("--list", action="store_true", help="List target keys and paths, then exit")
    parser.add_argument("--dry-run", action="store_true", help="Report what would be written without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing rule files")
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Export only the compass, decision tree, non-triggers, anti-patterns, and quality checks",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(list(argv) if argv is not None else sys.argv[1:])

    if args.list:
        print_target_table()
        return 0

    targets, unknown = select_targets(args.only)
    if unknown:
        print(f"Error: unknown target key(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Known keys: {', '.join(t.key for t in TARGETS)}", file=sys.stderr)
        return 1

    if not SKILL_PATH.is_file():
        print(f"Error: {SKILL_PATH} not found.", file=sys.stderr)
        return 1

    body = strip_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
    if args.compact:
        body, missing = extract_sections(body, COMPACT_SECTIONS)
        if missing:
            print(f"Error: --compact could not find section(s): {', '.join(missing)}", file=sys.stderr)
            return 1
        if not body:
            print("Error: --compact produced an empty document.", file=sys.stderr)
            return 1

    target_root = args.target.resolve()
    if not target_root.is_dir():
        print(f"Error: target directory not found: {target_root}", file=sys.stderr)
        return 1

    mode = "Planning" if args.dry_run else "Exporting"
    print(f"{mode} Diataxis rules ({'compact' if args.compact else 'full'}) into {target_root}\n")

    written = 0
    skipped = 0
    failed = 0

    for target in targets:
        content = build_content(target, body)
        path = target_root / target.path
        display = target.path.as_posix()
        label = f"{target.name:<19} {display}"

        if target.char_limit and len(content) > target.char_limit:
            print(f"  WARN  {label} - {len(content)} chars exceeds the {target.char_limit} limit; use --compact")

        if path.exists() and not args.force:
            print(f"  SKIP  {label} - exists (use --force to overwrite)")
            skipped += 1
            continue

        if args.dry_run:
            action = "would overwrite" if path.exists() else "would write"
            print(f"  PLAN  {label} - {action}, {len(content)} chars")
            written += 1
            continue

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except OSError as error:
            print(f"  FAIL  {label} - {error}", file=sys.stderr)
            failed += 1
            continue

        action = "overwrote" if args.force else "wrote"
        print(f"  OK    {label} - {action}, {len(content)} chars")
        written += 1

    verb = "would write" if args.dry_run else "wrote"
    print(f"\n{verb} {written}, skipped {skipped}, failed {failed}.")

    always_on = [t for t in targets if t.always_on]
    if always_on and not args.compact:
        cost = approx_tokens(build_content(always_on[0], body))
        print(
            f"Note: {len(always_on)} of these targets load into every request. "
            f"That is roughly {cost} tokens per request each. Re-run with --compact to shrink them."
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
