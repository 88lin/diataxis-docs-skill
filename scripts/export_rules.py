#!/usr/bin/env python3
"""Export Diataxis SKILL.md to .cursorrules or .clinerules.

Usage:
    python scripts/export_rules.py

Reads SKILL.md from the script's own directory, strips the
OpenCode-specific frontmatter, and writes a gentle preamble
plus the body to .cursorrules and .clinerules in the current
working directory. Existing files are not overwritten.

This is a helper for users of other AI coding assistants
(Cursor, Cline / Roo Code) who want to apply the same
Diataxis guidance in their own project. The diataxis-docs-skill
repo itself remains an OpenCode skill.
"""
import os

SKILL_PATH = "SKILL.md"
CURSOR_PATH = ".cursorrules"
CLINE_PATH = ".clinerules"


def strip_frontmatter(content):
    """Remove the leading OpenCode YAML frontmatter from SKILL.md."""
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

    for path in [CURSOR_PATH, CLINE_PATH]:
        if os.path.exists(path):
            print(
                f"Skipping {path} (already exists). "
                f"Delete it first if you want to overwrite."
            )
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Wrote {path}")


if __name__ == "__main__":
    export()
