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
    python scripts/export_rules.py
"""
import os

SKILL_PATH = "SKILL.md"

# Mapping of AI Tool -> Target Rule File Path
TARGETS = [
    ("Cursor (Legacy)", ".cursorrules"),
    ("Cursor (New Rules)", ".cursor/rules/diataxis.md"),
    ("Cline", ".clinerules"),
    ("Roo Code", ".roo/rules/diataxis.md"),
    ("Windsurf", ".windsurfrules"),
    ("GitHub Copilot", ".github/copilot-instructions.md"),
    ("Claude Code", "CLAUDE.md"),
    ("OpenAI Codex", "AGENTS.md"),
    ("Aider", "CONVENTIONS.md"),
    ("Gemini CLI", "GEMINI.md"),
    ("Continue", ".continue/rules/diataxis.md"),
    ("Amazon Q Developer", ".amazonq/rules/diataxis.md"),
]


def strip_frontmatter(content):
    """Remove the leading Opencode YAML frontmatter from SKILL.md."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def export():
    if not os.path.exists(SKILL_PATH):
        print(f"Error: {SKILL_PATH} not found.")
        print("Run this script from the repository root.")
        return

    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        raw_content = f.read()

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

    print("Exporting Diataxis rules for various AI coding assistants...\n")

    exported_count = 0
    for name, path in TARGETS:
        if os.path.exists(path):
            print(f"Skipping {name:<18} ({path}) - File already exists.")
            continue

        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Exported {name:<18} -> {path}")
        exported_count += 1

    print(f"\nDone! Exported {exported_count} new rule files.")
    print("Diataxis is a guide, not a plan. Feel free to edit these files to fit your workflow.")


if __name__ == "__main__":
    export()
