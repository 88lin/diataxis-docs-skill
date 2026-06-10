#!/usr/bin/env python3
"""Universal AI IDE Rules Exporter for Diataxis.

Exports SKILL.md to 12 rule-file targets across 11 major AI coding
assistants (Cursor, Cline, Roo Code, Windsurf, GitHub Copilot,
Claude Code, OpenAI Codex, Aider, Gemini CLI, Continue, Amazon Q
Developer). Reads SKILL.md, strips the Opencode-specific frontmatter,
prepends a gentle preamble aligned with the
"guide, not a plan" philosophy, and writes the body to the
standard rule-file path for each tool.

Existing files are never overwritten. Parent directories that
do not yet exist (such as .github/ or .cursor/rules/) are
created on demand.

Usage:
    # From this repository, export into this repository:
    python scripts/export_rules.py

    # From another project, export this skill's rules into that project:
    python /path/to/diataxis-docs-skill/scripts/export_rules.py
"""
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent
TARGET_ROOT = Path.cwd()
SKILL_PATH = SOURCE_ROOT / "SKILL.md"

# Mapping of AI Tool -> Target Rule File Path, relative to the project that
# should receive the exported rule files. Run from that target project root.
TARGETS: list[tuple[str, Path]] = [
    ("Cursor (Legacy)", Path(".cursorrules")),
    ("Cursor (New Rules)", Path(".cursor/rules/diataxis.md")),
    ("Cline", Path(".clinerules")),
    ("Roo Code", Path(".roo/rules/diataxis.md")),
    ("Windsurf", Path(".windsurfrules")),
    ("GitHub Copilot", Path(".github/copilot-instructions.md")),
    ("Claude Code", Path("CLAUDE.md")),
    ("OpenAI Codex", Path("AGENTS.md")),
    ("Aider", Path("CONVENTIONS.md")),
    ("Gemini CLI", Path("GEMINI.md")),
    ("Continue", Path(".continue/rules/diataxis.md")),
    ("Amazon Q Developer", Path(".amazonq/rules/diataxis.md")),
]


def strip_frontmatter(content: str) -> str:
    """Remove the leading Opencode YAML frontmatter from SKILL.md."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def export() -> None:
    if not SKILL_PATH.exists():
        print(f"Error: {SKILL_PATH} not found.")
        return

    raw_content = SKILL_PATH.read_text(encoding="utf-8")

    body_content = strip_frontmatter(raw_content)

    preamble = (
        "# Diataxis Documentation Guide\n"
        "This document outlines a systematic approach to technical documentation "
        "based on the Diataxis framework. Use it as a guide to help classify user "
        "needs and structure documentation organically, rather than as a rigid "
        "template.\n"
        "\n"
        "---\n"
        "\n"
    )

    final_content = preamble + body_content

    print("Exporting Diataxis rules for various AI coding assistants...")
    print(f"Target project: {TARGET_ROOT}\n")

    exported_count = 0
    for name, relative_path in TARGETS:
        path = TARGET_ROOT / relative_path
        display_path = relative_path.as_posix()
        if path.exists():
            print(f"Skipping {name:<18} ({display_path}) - File already exists.")
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(final_content, encoding="utf-8")
        print(f"Exported {name:<18} -> {display_path}")
        exported_count += 1

    print(f"\nDone! Exported {exported_count} new rule files.")
    print("Diataxis is a guide, not a plan. Feel free to edit these files to fit your workflow.")


if __name__ == "__main__":
    export()
