"""Local validation scripts for the diataxis-docs skill.

These run the same checks the CI workflow runs, so contributors can validate
their changes before pushing.

Usage:
    python scripts/check_local.py
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZERO_WIDTH_CHARS = {
    "\u200b": "U+200B ZERO WIDTH SPACE",
    "\ufeff": "U+FEFF ZERO WIDTH NO-BREAK SPACE",
}


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


def check_evals() -> list[str]:
    """Validate evals.json structure and content."""
    path = ROOT / "evals" / "evals.json"
    problems: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"evals.json is not valid JSON: {exc}"]

    required_top = {"skill_name", "evals"}
    missing = required_top - set(data.keys())
    if missing:
        problems.append(f"evals.json: missing top-level fields: {sorted(missing)}")

    evals = data.get("evals", [])
    if not isinstance(evals, list):
        problems.append("evals.json: 'evals' must be a list")
        return problems
    if not evals:
        problems.append("evals.json: 'evals' must not be empty")
        return problems

    required_per_eval = {"id", "category", "prompt", "expected_output", "files"}
    known_categories = {
        "classification",
        "per-form-writing",
        "decision-framework",
        "single-page-classification",
        "mixed-form-detection",
        "review",
        "large-system",
        "migration",
        "adjacent-types",
        "anti-pattern-avoidance",
        "non-trigger",
    }

    seen_ids: set[int] = set()
    for i, ev in enumerate(evals):
        for field in required_per_eval:
            if field not in ev:
                problems.append(f"evals.json: eval[{i}] missing field: {field}")
        if "id" in ev:
            if ev["id"] in seen_ids:
                problems.append(f"evals.json: duplicate id: {ev['id']}")
            seen_ids.add(ev["id"])
        if "category" in ev and ev["category"] not in known_categories:
            problems.append(
                f"evals.json: eval[{ev.get('id', i)}] unknown category: {ev['category']!r}"
            )
        if "prompt" in ev and len(ev["prompt"].strip()) < 10:
            problems.append(f"evals.json: eval[{ev.get('id', i)}] prompt is too short")
        if "expected_output" in ev and len(ev["expected_output"].strip()) < 10:
            problems.append(
                f"evals.json: eval[{ev.get('id', i)}] expected_output is too short"
            )

    if not problems:
        cats = {e["category"] for e in evals if "category" in e}
        print(
            f"  evals.json OK: {len(evals)} evals across {len(cats)} categories"
        )
    return problems


def check_links() -> list[str]:
    """Check that internal markdown links point to existing files and anchors."""
    md_files = sorted(ROOT.rglob("*.md"))
    md_files = [p for p in md_files if ".git" not in p.parts]

    link_re = re.compile(
        r"\[[^\]]*\]\((?!https?://|mailto:)([^)]+?)\)"
    )
    problems: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        for char, label in ZERO_WIDTH_CHARS.items():
            for line_no, line in enumerate(text.splitlines(), 1):
                if char in line:
                    problems.append(f"{md.relative_to(ROOT)}:{line_no}: contains {label}")

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
                problems.append(f"{md.relative_to(ROOT)}: broken link to {raw_target}")
                continue
            if anchor:
                anchor_cache.setdefault(candidate, anchors_for_markdown(candidate))
                if anchor not in anchor_cache[candidate]:
                    problems.append(
                        f"{md.relative_to(ROOT)}: broken anchor in link to {raw_target}"
                    )

    if not problems:
        print(
            f"  internal links and markdown hygiene OK: scanned {len(md_files)} markdown files"
        )
    return problems


def check_structure() -> list[str]:
    """Check that required files and example files exist."""
    required = [
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
        "tests/test_audit_docs.py",
    ]
    problems = [f"missing: {p}" for p in required if not (ROOT / p).is_file()]
    if not problems:
        print(f"  structure OK: {len(required)} required files present")
    return problems


def check_skill_frontmatter() -> list[str]:
    """Check that SKILL.md has a valid YAML frontmatter with name, version, description.

    The frontmatter is the OpenCode entry point for the skill. A missing or
    broken frontmatter silently disables the skill, so we fail the build if
    the delimiters, fields, or values are wrong.
    """
    path = ROOT / "SKILL.md"
    problems: list[str] = []
    if not path.is_file():
        return ["SKILL.md: file not found"]
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        problems.append("SKILL.md: missing opening --- frontmatter delimiter")
        return problems
    parts = text.split("---", 2)
    if len(parts) < 3:
        problems.append("SKILL.md: frontmatter not properly closed")
        return problems

    fm = parts[1].strip()
    fields = {"name": "", "version": "", "description": ""}
    for line in fm.splitlines():
        for key in fields:
            if line.startswith(f"{key}:"):
                fields[key] = line[len(key) + 1 :].strip().strip('"').strip("'")
                break

    for key, value in fields.items():
        if not value:
            problems.append(f"SKILL.md: frontmatter missing or empty field: {key}")

    description_words = len(fields["description"].split())
    if description_words > 60:
        print(
            f"  WARN: SKILL.md: description is {description_words} words "
            f"(recommended: <= 60). A long description can dilute trigger matching; "
            f"move workflow guidance and enumeration into the body instead."
        )

    if not problems:
        print(
            f"  SKILL.md frontmatter OK: name={fields['name']!r} "
            f"version={fields['version']!r} description={len(fields['description'])} chars "
            f"({description_words} words)"
        )
    return problems


def check_audit_docs_tests() -> list[str]:
    """Run the audit_docs.py unit tests."""
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        return [f"audit_docs.py tests failed:\n{output}"]
    print("  audit_docs.py tests OK")
    return []


def main() -> int:
    print("Running local checks...")
    all_problems: list[str] = []
    for name, fn in [
        ("evals", check_evals),
        ("links", check_links),
        ("structure", check_structure),
        ("frontmatter", check_skill_frontmatter),
        ("audit-docs-tests", check_audit_docs_tests),
    ]:
        all_problems.extend(fn())

    if all_problems:
        print("\nFAILED:")
        for p in all_problems:
            print(f"  - {p}")
        return 1
    print("\nAll local checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
