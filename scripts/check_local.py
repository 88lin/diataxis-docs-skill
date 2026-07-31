#!/usr/bin/env python3
"""Repository validation for the diataxis-docs skill.

This is the single source of truth for repository checks. CI runs this exact
script, so `python scripts/check_local.py` locally reproduces the CI result.

Checks:
    - SKILL.md frontmatter is valid for OpenCode and Claude Code
    - SKILL.md stays within the recommended size budget
    - installation docs clone into a directory named after the skill
    - slash command frontmatter follows the OpenCode command spec
    - evals.json structure, unique ids, and known categories
    - internal markdown links, heading anchors, and image paths resolve
    - bilingual docs stay paired
    - required files exist
    - SKILL.md, evals.json, and CHANGELOG.md agree on the version
    - unit tests pass

Usage:
    python scripts/check_local.py
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# OpenCode recognises only these SKILL.md frontmatter fields; everything else is
# ignored silently. Claude Code ignores unknown fields too, so an unknown key is
# a warning rather than an error.
# https://opencode.ai/docs/skills/
RECOGNISED_SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata"}

# https://opencode.ai/docs/commands/ - the command name comes from the file name.
# `description` is optional in OpenCode, but required by this repository so the
# command picker remains useful.
RECOGNISED_COMMAND_FIELDS = {"description", "agent", "model", "variant", "subtask"}

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESCRIPTION_MAX_CHARS = 1024
DESCRIPTION_WARN_CHARS = 500
SKILL_BODY_MAX_LINES = 500  # Claude Code guidance: keep SKILL.md under 500 lines.
SKILL_BODY_WARN_LINES = 400

INSTALL_DOCS = [
    "README.md",
    "README.zh-CN.md",
    "docs/installation.md",
    "docs/zh-CN/installation.md",
]
INSTALL_PATH_PLACEHOLDERS = {"<name>", "<skill-name>", "*", "skill-name", "name"}

ZERO_WIDTH_CHARS = {
    "\u200b": "U+200B ZERO WIDTH SPACE",
    "\ufeff": "U+FEFF ZERO WIDTH NO-BREAK SPACE",
}

# Markdown shipped by installed dependencies or build tools is not part of the
# repository contract. Excluding these directories keeps local validation
# equivalent to the clean checkout used by CI.
MARKDOWN_SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    "site",
}

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "evals/evals.json",
    "references/doc-blueprints.md",
    "references/reader-analysis.md",
    "references/template-map.md",
    "references/zh-cn-anti-patterns.md",
    "assets/preview.svg",
    "docs/installation.md",
    "docs/commands.md",
    "docs/ide-integration.md",
    "docs/development.md",
    "docs/faq.md",
    "docs/zh-CN/installation.md",
    "docs/zh-CN/commands.md",
    "docs/zh-CN/ide-integration.md",
    "docs/zh-CN/development.md",
    "docs/zh-CN/faq.md",
    "examples/messy-to-diataxis/README.md",
    "examples/messy-to-diataxis/before.md",
    "examples/messy-to-diataxis/after/01-tutorial.md",
    "examples/messy-to-diataxis/after/02-how-to.md",
    "examples/messy-to-diataxis/after/03-reference.md",
    "examples/messy-to-diataxis/after/04-explanation.md",
    ".opencode/commands/docs-classify.md",
    ".opencode/commands/docs-split.md",
    ".opencode/commands/docs-review.md",
    ".opencode/commands/docs-audit.md",
    ".opencode/commands/docs-quickstart.md",
    "scripts/export_rules.py",
    "scripts/audit_docs.py",
    "scripts/check_local.py",
    "tests/test_audit_docs.py",
    "tests/test_check_local.py",
    "tests/test_export_rules.py",
]

warnings: list[str] = []


def warn(message: str) -> None:
    warnings.append(message)
    print(f"  WARN: {message}")


# --------------------------------------------------------------------------
# Frontmatter parsing
# --------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Split leading YAML frontmatter from a markdown document.

    Returns (frontmatter_text, body). frontmatter_text is None when the
    document has no properly delimited frontmatter block. The delimiters are
    matched on line boundaries so that a `---` inside the body cannot end the
    block early.
    """
    match = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return None, text
    return match.group(1), text[match.end():]


def parse_scalar(value: str) -> str:
    """Unwrap a quoted YAML scalar, or strip a trailing comment from a bare one.

    A `#` inside quotes is part of the value, so quoted scalars are read up to
    their closing quote and the remainder of the line is discarded.
    """
    value = value.strip()
    if value[:1] in {'"', "'"}:
        quote = value[0]
        end = value.find(quote, 1)
        return value[1:end] if end != -1 else value[1:]
    comment = re.search(r"(?:^|\s)#", value)
    if comment:
        value = value[: comment.start()]
    return value.strip()


def parse_simple_yaml(text: str) -> dict[str, object]:
    """Parse the small YAML subset used by skill and command frontmatter.

    Supports `key: value` scalars, quoted scalars, trailing comments, and one
    level of nested mapping (used by `metadata:`). This avoids a PyYAML
    dependency in CI.
    """
    result: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indented = raw_line[:1] in {" ", "\t"}
        line = raw_line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = parse_scalar(value)
        if indented and current_key is not None:
            nested = result.setdefault(current_key, {})
            if isinstance(nested, dict):
                nested[key] = value
            continue
        if value == "":
            result[key] = {}
            current_key = key
        else:
            result[key] = value
            current_key = None
    return result


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------


def markdown_anchor(text: str) -> str:
    """Return the GitHub-style heading anchor for common markdown headings."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("`", "").replace("*", "").replace("_", "").replace("~", "")
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def anchors_for_markdown(path: Path) -> set[str]:
    """Collect heading anchors from a markdown file."""
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
    counts: dict[str, int] = {}
    anchors: set[str] = set()
    text = path.read_text(encoding="utf-8")
    for match in heading_re.finditer(text):
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if any(part in MARKDOWN_SKIP_DIRS for part in relative.parts[:-1]):
            continue
        files.append(path)
    return files


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def load_skill_frontmatter() -> tuple[dict[str, object], str, list[str]]:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        return {}, "", ["SKILL.md: file not found"]
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    if frontmatter is None:
        return {}, text, ["SKILL.md: missing or unterminated YAML frontmatter block"]
    return parse_simple_yaml(frontmatter), body, []


def check_skill_frontmatter(fields: dict[str, object], body: str) -> list[str]:
    """Validate SKILL.md frontmatter against the OpenCode skill spec."""
    problems: list[str] = []

    name = str(fields.get("name", "")).strip()
    description = str(fields.get("description", "")).strip()

    if not name:
        problems.append("SKILL.md: frontmatter missing or empty field: name")
    else:
        if len(name) > 64:
            problems.append(f"SKILL.md: name is {len(name)} characters (max 64)")
        if not SKILL_NAME_RE.match(name):
            problems.append(
                f"SKILL.md: name {name!r} must match ^[a-z0-9]+(-[a-z0-9]+)*$ "
                "(lowercase alphanumeric with single hyphen separators)"
            )

    if not description:
        problems.append("SKILL.md: frontmatter missing or empty field: description")
    elif len(description) > DESCRIPTION_MAX_CHARS:
        problems.append(
            f"SKILL.md: description is {len(description)} characters "
            f"(max {DESCRIPTION_MAX_CHARS})"
        )
    elif len(description) > DESCRIPTION_WARN_CHARS:
        warn(
            f"SKILL.md: description is {len(description)} characters. Long "
            "descriptions dilute trigger matching and eat the skill listing budget."
        )

    unknown = sorted(set(fields) - RECOGNISED_SKILL_FIELDS)
    if unknown:
        warn(
            f"SKILL.md: frontmatter fields {unknown} are not recognised by OpenCode "
            f"and are ignored. Recognised: {sorted(RECOGNISED_SKILL_FIELDS)}."
        )

    metadata = fields.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            problems.append("SKILL.md: metadata must be a string-to-string map")
        else:
            for key, value in metadata.items():
                if not isinstance(value, str) or not value:
                    problems.append(f"SKILL.md: metadata.{key} must be a non-empty string")

    body_lines = len(body.strip().splitlines())
    if body_lines > SKILL_BODY_MAX_LINES:
        problems.append(
            f"SKILL.md: body is {body_lines} lines (max {SKILL_BODY_MAX_LINES}). "
            "Move detail into references/ and link to it."
        )
    elif body_lines > SKILL_BODY_WARN_LINES:
        warn(
            f"SKILL.md: body is {body_lines} lines, close to the "
            f"{SKILL_BODY_MAX_LINES}-line budget."
        )

    if not problems:
        print(
            f"  SKILL.md frontmatter OK: name={name!r} "
            f"description={len(description)} chars, body={body_lines} lines"
        )
    return problems


def check_install_paths(skill_name: str, root: Path | None = None) -> list[str]:
    """Installation docs must clone into a directory named after the skill.

    OpenCode requires the frontmatter `name` to match the directory that
    contains SKILL.md. A clone command that keeps the repository name would
    make the skill fail to load with no error message.

    `root` is overridable so tests can point the check at a fixture tree.
    """
    root = root or ROOT
    problems: list[str] = []
    if not skill_name:
        return problems
    # The lookbehind keeps a repository path such as `diataxis-docs-skill/scripts`
    # from matching the `skill/` at the end of the directory name.
    pattern = re.compile(r"(?<![\w-])skills?/([A-Za-z0-9._<>-]+)")
    checked = 0
    for rel in INSTALL_DOCS:
        path = root / rel
        if not path.is_file():
            continue
        checked += 1
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in pattern.finditer(line):
                target = match.group(1)
                if target in INSTALL_PATH_PLACEHOLDERS or target == skill_name:
                    continue
                if target.endswith(".md") or target.endswith(".json"):
                    continue
                problems.append(
                    f"{rel}:{line_no}: installs into 'skills/{target}' but the skill "
                    f"name is {skill_name!r}; OpenCode requires the directory name to "
                    "match the frontmatter name"
                )
    if not problems:
        print(f"  install path consistency OK: {checked} docs target 'skills/{skill_name}'")
    return problems


def check_commands(root: Path | None = None) -> list[str]:
    """Validate OpenCode slash command frontmatter and repository conventions."""
    root = root or ROOT
    problems: list[str] = []
    command_dir = root / ".opencode" / "commands"
    files = sorted(command_dir.glob("*.md"))
    if not files:
        return [".opencode/commands/: no command files found"]
    for path in files:
        rel = path.relative_to(root).as_posix()
        frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if frontmatter is None:
            problems.append(f"{rel}: missing or unterminated YAML frontmatter block")
            continue
        fields = parse_simple_yaml(frontmatter)
        if not str(fields.get("description", "")).strip():
            problems.append(
                f"{rel}: frontmatter missing or empty field: description "
                "(required by this repository)"
            )
        unknown = sorted(set(fields) - RECOGNISED_COMMAND_FIELDS)
        if unknown:
            warn(f"{rel}: unrecognised command frontmatter fields {unknown}")
    if not problems:
        print(f"  slash commands OK: {len(files)} commands")
    return problems


def check_evals() -> list[str]:
    """Validate evals.json structure and content."""
    path = ROOT / "evals" / "evals.json"
    problems: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"evals.json could not be read: {exc}"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"evals.json is not valid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["evals.json: top-level value must be a JSON object"]

    required_top = {"skill_name", "version", "categories", "evals"}
    missing = required_top - set(data.keys())
    if missing:
        problems.append(f"evals.json: missing top-level fields: {sorted(missing)}")

    known_categories_value = data.get("categories", [])
    if not isinstance(known_categories_value, list) or not known_categories_value:
        problems.append("evals.json: 'categories' must be a non-empty list")
        known_categories: list[str] = []
    else:
        known_categories = []
        for i, category in enumerate(known_categories_value):
            if not isinstance(category, str) or not category.strip():
                problems.append(f"evals.json: categories[{i}] must be a non-empty string")
            else:
                known_categories.append(category)

    evals = data.get("evals", [])
    if not isinstance(evals, list):
        return problems + ["evals.json: 'evals' must be a list"]
    if not evals:
        return problems + ["evals.json: 'evals' must not be empty"]

    required_per_eval = {"id", "category", "prompt", "expected_output", "files"}
    seen_ids: set[str | int] = set()
    for i, ev in enumerate(evals):
        if not isinstance(ev, dict):
            problems.append(f"evals.json: eval[{i}] must be a JSON object")
            continue

        label = ev.get("id", i)
        for field in sorted(required_per_eval):
            if field not in ev:
                problems.append(f"evals.json: eval[{i}] missing field: {field}")

        if "id" in ev:
            eval_id = ev["id"]
            if isinstance(eval_id, bool) or not isinstance(eval_id, (str, int)):
                problems.append(
                    f"evals.json: eval[{i}] id must be a string or integer"
                )
            elif isinstance(eval_id, str) and not eval_id.strip():
                problems.append(f"evals.json: eval[{i}] id must not be empty")
            elif eval_id in seen_ids:
                problems.append(f"evals.json: duplicate id: {eval_id}")
            else:
                seen_ids.add(eval_id)

        category = ev.get("category")
        if "category" in ev:
            if not isinstance(category, str) or not category.strip():
                problems.append(f"evals.json: eval[{i}] category must be a non-empty string")
            elif known_categories and category not in known_categories:
                problems.append(
                    f"evals.json: eval[{label}] unknown category: {category!r}"
                )

        prompt = ev.get("prompt")
        if "prompt" in ev:
            if not isinstance(prompt, str):
                problems.append(f"evals.json: eval[{label}] prompt must be a string")
            elif len(prompt.strip()) < 10:
                problems.append(f"evals.json: eval[{label}] prompt is too short")

        expected_output = ev.get("expected_output")
        if "expected_output" in ev:
            if not isinstance(expected_output, str):
                problems.append(
                    f"evals.json: eval[{label}] expected_output must be a string"
                )
            elif len(expected_output.strip()) < 10:
                problems.append(f"evals.json: eval[{label}] expected_output is too short")

        files = ev.get("files")
        if "files" in ev:
            if not isinstance(files, list):
                problems.append(f"evals.json: eval[{label}] files must be a list")
            else:
                for file_index, referenced in enumerate(files):
                    if not isinstance(referenced, str) or not referenced.strip():
                        problems.append(
                            f"evals.json: eval[{label}] files[{file_index}] must be a non-empty string"
                        )
                    elif not (ROOT / referenced).exists():
                        problems.append(
                            f"evals.json: eval[{label}] references missing file: {referenced}"
                        )

    used_categories = {
        ev.get("category")
        for ev in evals
        if isinstance(ev, dict) and isinstance(ev.get("category"), str)
    }
    unused = sorted(set(known_categories) - used_categories)
    if unused:
        warn(f"evals.json: categories declared but unused: {unused}")

    if not problems:
        used = used_categories
        print(f"  evals.json OK: {len(evals)} evals across {len(used)} categories")
    return problems


def check_links() -> list[str]:
    """Check that internal markdown links and images resolve."""
    md_files = markdown_files()
    link_re = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:)([^)]+?)\)")
    img_re = re.compile(r"<img[^>]+src=\"(?!https?://)([^\"]+)\"")
    problems: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for md in md_files:
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        for char, label in ZERO_WIDTH_CHARS.items():
            for line_no, line in enumerate(text.splitlines(), 1):
                if char in line:
                    problems.append(f"{rel}:{line_no}: contains {label}")

        for match in img_re.finditer(text):
            target = match.group(1).strip()
            if not (md.parent / target).resolve().exists():
                problems.append(f"{rel}: broken image path {target}")

        for match in link_re.finditer(text):
            raw_target = match.group(1).strip()
            if not raw_target:
                continue
            target_path, _, anchor = raw_target.partition("#")
            if not target_path and anchor:
                candidate = md.resolve()
            else:
                candidate = (md.parent / target_path).resolve()
            if not candidate.exists():
                problems.append(f"{rel}: broken link to {raw_target}")
                continue
            if anchor and candidate.suffix.lower() == ".md":
                anchor_cache.setdefault(candidate, anchors_for_markdown(candidate))
                if anchor not in anchor_cache[candidate]:
                    problems.append(f"{rel}: broken anchor in link to {raw_target}")

    if not problems:
        print(f"  links and markdown hygiene OK: scanned {len(md_files)} markdown files")
    return problems


def check_translation_parity() -> list[str]:
    """docs/ and docs/zh-CN/ must stay paired."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return ["docs/: directory not found"]
    english = {p.name for p in docs.glob("*.md")}
    chinese = {p.name for p in (docs / "zh-CN").glob("*.md")}
    problems = []
    for name in sorted(english - chinese):
        problems.append(f"docs/zh-CN/{name}: missing Chinese counterpart for docs/{name}")
    for name in sorted(chinese - english):
        problems.append(f"docs/{name}: missing English counterpart for docs/zh-CN/{name}")
    if not problems:
        print(f"  bilingual docs OK: {len(english)} pages in both languages")
    return problems


def check_structure() -> list[str]:
    problems = [f"missing: {p}" for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    if not problems:
        print(f"  structure OK: {len(REQUIRED_FILES)} required files present")
    return problems


def check_version_consistency(fields: dict[str, object]) -> list[str]:
    """SKILL.md metadata.version, evals.json, and CHANGELOG.md must agree."""
    problems: list[str] = []
    metadata = fields.get("metadata")
    skill_version = ""
    if isinstance(metadata, dict):
        skill_version = str(metadata.get("version", "")).strip()
    if not skill_version:
        # Backwards compatibility with the pre-0.2.0 top-level version field.
        skill_version = str(fields.get("version", "")).strip()
        if skill_version:
            warn(
                "SKILL.md: top-level 'version' is not part of the skill spec; "
                "move it under 'metadata:'"
            )

    try:
        evals_data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"evals.json could not be read for version check: {exc}"]
    if not isinstance(evals_data, dict):
        return ["evals.json: top-level value must be a JSON object for version check"]
    evals_version = str(evals_data.get("version", "")).strip()

    try:
        changelog_text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"CHANGELOG.md could not be read for version check: {exc}"]
    released = set(re.findall(r"^## \[([^\]]+)\]", changelog_text, re.MULTILINE))

    if not skill_version:
        problems.append("SKILL.md: metadata.version is missing")
    if not evals_version:
        problems.append("evals/evals.json: top-level version is missing")
    if skill_version and evals_version and skill_version != evals_version:
        problems.append(
            f"version mismatch: SKILL.md has {skill_version!r}, "
            f"evals/evals.json has {evals_version!r}"
        )
    if skill_version and skill_version not in released:
        problems.append(f"CHANGELOG.md: missing release heading for version {skill_version!r}")

    if not problems:
        print(f"  version consistency OK: {skill_version}")
    return problems


def check_unit_tests() -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if result.returncode != 0:
        return [f"unit tests failed:\n{(result.stdout + result.stderr).strip()}"]
    tests_run = re.search(r"^Ran (\d+) tests?", result.stderr, re.MULTILINE)
    print(f"  unit tests OK: {tests_run.group(1) if tests_run else '?'} tests")
    return []


def main() -> int:
    print("Running local checks...")
    fields, body, problems = load_skill_frontmatter()
    all_problems: list[str] = list(problems)

    if not problems:
        all_problems.extend(check_skill_frontmatter(fields, body))
        all_problems.extend(check_install_paths(str(fields.get("name", "")).strip()))
        all_problems.extend(check_version_consistency(fields))

    for check in (
        check_commands,
        check_evals,
        check_links,
        check_translation_parity,
        check_structure,
        check_unit_tests,
    ):
        all_problems.extend(check())

    if all_problems:
        print("\nFAILED:")
        for problem in all_problems:
            print(f"  - {problem}")
        return 1
    if warnings:
        print(f"\nAll local checks passed with {len(warnings)} warning(s).")
    else:
        print("\nAll local checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
