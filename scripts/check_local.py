"""Local validation scripts for the diataxis-docs skill.

These run the same checks the CI workflow runs, so contributors can validate
their changes before pushing.

Usage:
    python scripts/check_local.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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
    """Check that internal markdown links point to existing files."""
    md_files = sorted(ROOT.rglob("*.md"))
    md_files = [p for p in md_files if ".git" not in p.parts]

    link_re = re.compile(
        r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)#]+?)(?:#[^)]*)?\)"
    )
    problems: list[str] = []
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        for match in link_re.finditer(text):
            target = match.group(1).strip()
            if not target:
                continue
            candidate = (md.parent / target).resolve()
            if not candidate.exists():
                problems.append(f"{md.relative_to(ROOT)}: broken link to {target}")

    if not problems:
        print(f"  internal links OK: scanned {len(md_files)} markdown files")
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
    ]
    problems = [f"missing: {p}" for p in required if not (ROOT / p).is_file()]
    if not problems:
        print(f"  structure OK: {len(required)} required files present")
    return problems


def main() -> int:
    print("Running local checks...")
    all_problems: list[str] = []
    for name, fn in [
        ("evals", check_evals),
        ("links", check_links),
        ("structure", check_structure),
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
