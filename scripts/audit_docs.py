#!/usr/bin/env python3
"""Heuristic Diataxis mixed-form smell scanner.

This script does not classify documentation with authority. It scans Markdown
files for signals that a page may be mixing Diataxis forms, then reports the
pages worth reviewing by a human or an AI assistant.

Signals are counted on prose only. YAML frontmatter and fenced code blocks are
removed before the text patterns run, and inline code spans are removed before
tables are counted, so a shell pipeline such as `ls | wc -l` inside a code block
is never mistaken for a Markdown table row.

Usage:
    python scripts/audit_docs.py docs/
    python scripts/audit_docs.py docs/ --format json
    python scripts/audit_docs.py . --exclude 'CHANGELOG.md' --fail-on high
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Sequence


STEP_RE = re.compile(
    r"^\s*(?:\d+\.\s*|[-*]\s+)?(?:run|install|configure|create|set|copy|open|click|deploy|start|stop|verify|add|update|enable|disable)\b",
    re.IGNORECASE,
)
CN_STEP_RE = re.compile(r"^\s*(?:\d+\.\s*|[-*]\s+)?(?:运行|安装|配置|创建|设置|复制|打开|点击|部署|启动|停止|验证|添加|更新|启用|禁用)")
EXPLANATION_RE = re.compile(
    r"\b(?:why|background|concept|architecture|design|tradeoff|trade-off|rationale|overview|history)\b",
    re.IGNORECASE,
)
CN_EXPLANATION_RE = re.compile(r"(?:为什么|背景|概念|架构|设计|取舍|权衡|原理|历史)")
REFERENCE_RE = re.compile(r"\b(?:parameter|field|schema|endpoint|status code|return value|limit|type)\b", re.IGNORECASE)
CN_REFERENCE_RE = re.compile(r"(?:参数|字段|模式|接口|端点|状态码|返回值|限制|类型)")

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
FENCE_RE = re.compile(r"^(?P<indent>\s{0,3})(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$")

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__", "site", ".next"}
RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


@dataclass
class PageReport:
    path: str
    risk: str
    score: int
    suspected_mix: list[str]
    signals: dict[str, int]
    evidence: list[str]


def strip_frontmatter(text: str) -> str:
    """Remove a leading YAML frontmatter block, keeping line count stable."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    blank = "\n" * match.group(0).count("\n")
    return blank + text[match.end():]


def split_code_blocks(lines: Sequence[str]) -> tuple[list[str], int]:
    """Split Markdown lines into prose lines and count fenced code blocks.

    Fence lines and their contents are replaced by empty strings so that line
    numbering stays aligned with the original file.
    """
    prose: list[str] = []
    code_blocks = 0
    fence_char = ""
    fence_len = 0

    for line in lines:
        match = FENCE_RE.match(line)
        if not fence_char:
            if match:
                fence_char = match.group("fence")[0]
                fence_len = len(match.group("fence"))
                prose.append("")
                continue
            prose.append(line)
            continue

        # Inside a fenced block: only a bare fence of the same character and at
        # least the same length closes it.
        if (
            match
            and match.group("fence")[0] == fence_char
            and len(match.group("fence")) >= fence_len
            and not match.group("info").strip()
        ):
            fence_char = ""
            fence_len = 0
            code_blocks += 1
        prose.append("")

    if fence_char:
        # Unterminated fence still counts as one code block.
        code_blocks += 1
    return prose, code_blocks


def count_table_rows(lines: Sequence[str]) -> int:
    """Count Markdown table rows in prose lines.

    A table is only recognised when a pipe-bearing header line is immediately
    followed by a separator row. Separator rows are not counted, so the result
    is the number of real header and body rows.
    """
    cleaned = [INLINE_CODE_RE.sub("", line) for line in lines]
    rows = 0
    index = 0
    total = len(cleaned)

    while index < total - 1:
        header = cleaned[index]
        separator = cleaned[index + 1]
        if "|" in header and header.strip() and TABLE_SEPARATOR_RE.match(separator):
            rows += 1  # header row
            body = index + 2
            while body < total and "|" in cleaned[body] and cleaned[body].strip():
                if not TABLE_SEPARATOR_RE.match(cleaned[body]):
                    rows += 1
                body += 1
            index = body
            continue
        index += 1

    return rows


def count_steps(lines: Sequence[str]) -> int:
    return sum(1 for line in lines if STEP_RE.search(line) or CN_STEP_RE.search(line))


def count_matches(pattern: re.Pattern[str], text: str) -> int:
    return len(pattern.findall(text))


def is_excluded(display_path: str, patterns: Sequence[str]) -> bool:
    return any(
        fnmatch.fnmatch(display_path, pattern) or fnmatch.fnmatch(Path(display_path).name, pattern)
        for pattern in patterns
    )


def iter_markdown_files(root: Path, exclude: Sequence[str]) -> Iterable[Path]:
    base = root if root.is_dir() else root.parent
    if root.is_file():
        if root.suffix.lower() in {".md", ".mdx"} and not is_excluded(root.name, exclude):
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in {".md", ".mdx"}:
            continue
        # Compare only components below the requested scan root. Checking
        # `path.parts` would incorrectly skip an explicit target whose own
        # name (or an ancestor outside the target) is `site` or `build`.
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts[:-1]):
            continue
        display_path = path.relative_to(base).as_posix()
        if is_excluded(display_path, exclude):
            continue
        yield path


def analyze_text(text: str) -> tuple[dict[str, int], list[str], list[str], int]:
    """Return (signals, suspected_mix, evidence, score) for one page."""
    body = strip_frontmatter(text)
    prose_lines, code_blocks = split_code_blocks(body.splitlines())
    prose_text = "\n".join(prose_lines)

    signals = {
        "code_blocks": code_blocks,
        "table_rows": count_table_rows(prose_lines),
        "step_lines": count_steps(prose_lines),
        "explanation_terms": count_matches(EXPLANATION_RE, prose_text) + count_matches(CN_EXPLANATION_RE, prose_text),
        "reference_terms": count_matches(REFERENCE_RE, prose_text) + count_matches(CN_REFERENCE_RE, prose_text),
    }

    suspected_mix: list[str] = []
    evidence: list[str] = []
    score = 0

    reference_weight = signals["table_rows"] + signals["reference_terms"] + signals["code_blocks"]
    howto_weight = signals["step_lines"]
    explanation_weight = signals["explanation_terms"]

    if reference_weight >= 4 and howto_weight >= 3:
        suspected_mix.append("how-to/reference")
        evidence.append("step-like instructions appear beside tables, reference terms, or code blocks")
        score += 3
    if explanation_weight >= 2 and (howto_weight >= 2 or reference_weight >= 3):
        suspected_mix.append("explanation")
        evidence.append("background, architecture, or tradeoff language appears beside practical/reference material")
        score += 2
    if signals["code_blocks"] >= 4 and howto_weight >= 3:
        suspected_mix.append("tutorial/how-to")
        evidence.append("many code blocks appear beside task steps; check whether this is a lesson or a task guide")
        score += 1

    return signals, sorted(set(suspected_mix)), evidence, score


def analyze_file(path: Path, base: Path) -> PageReport:
    text = path.read_text(encoding="utf-8", errors="replace")
    signals, suspected_mix, evidence, score = analyze_text(text)

    if score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    try:
        display_path = path.relative_to(base).as_posix()
    except ValueError:
        display_path = path.as_posix()
    return PageReport(display_path, risk, score, suspected_mix, signals, evidence)


def build_report(target: Path, exclude: Sequence[str]) -> dict[str, object]:
    base = target if target.is_dir() else target.parent
    pages = [analyze_file(path, base) for path in iter_markdown_files(target, exclude)]
    risk_counts = {"high": 0, "medium": 0, "low": 0}
    for page in pages:
        risk_counts[page.risk] += 1
    return {
        "target": target.as_posix(),
        "pages_scanned": len(pages),
        "risk_counts": risk_counts,
        "pages": [asdict(page) for page in sorted(pages, key=lambda p: (-p.score, p.path))],
    }


def render_markdown(report: dict[str, object]) -> str:
    pages = report["pages"]
    risk_counts = report["risk_counts"]
    lines = [
        "# Diataxis Smell Scan",
        "",
        f"Target: `{report['target']}`",
        f"Pages scanned: {report['pages_scanned']}",
        f"High risk: {risk_counts['high']} | Medium risk: {risk_counts['medium']} | Low risk: {risk_counts['low']}",
        "",
        "> This is a heuristic smell scan, not an authoritative Diataxis classification.",
        "",
    ]
    if not pages:
        lines.append("No Markdown files found.")
        return "\n".join(lines) + "\n"

    lines.extend([
        "| Page | Risk | Score | Suspected mix | Key signals |",
        "| --- | --- | ---: | --- | --- |",
    ])
    for page in pages:
        mix = ", ".join(page["suspected_mix"]) if page["suspected_mix"] else "-"
        signals = page["signals"]
        key_signals = (
            f"code={signals['code_blocks']}; table_rows={signals['table_rows']}; "
            f"steps={signals['step_lines']}; explanation={signals['explanation_terms']}"
        )
        lines.append(f"| `{page['path']}` | {page['risk']} | {page['score']} | {mix} | {key_signals} |")

    flagged = [page for page in pages if page["risk"] != "low"]
    if flagged:
        lines.extend(["", "## Pages to review first", ""])
        for page in flagged[:10]:
            lines.append(f"### {page['path']}")
            for item in page["evidence"]:
                lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Markdown docs for mixed-form Diataxis smell signals.")
    parser.add_argument("target", type=Path, help="Markdown file or documentation directory to scan")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="Skip paths matching this glob (relative path or file name). Repeatable.",
    )
    parser.add_argument(
        "--fail-on",
        choices=("none", "medium", "high"),
        default="none",
        help="Exit with status 1 when any page reaches this risk level (default: none)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(list(argv) if argv is not None else sys.argv[1:])
    if not args.target.exists():
        print(f"Error: target not found: {args.target}", file=sys.stderr)
        return 2

    report = build_report(args.target, args.exclude)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")

    if args.fail_on != "none":
        threshold = RISK_ORDER[args.fail_on]
        offenders = [page for page in report["pages"] if RISK_ORDER[page["risk"]] >= threshold]
        if offenders:
            print(
                f"\nFAIL: {len(offenders)} page(s) at or above '{args.fail_on}' risk.",
                file=sys.stderr,
            )
            for page in offenders:
                print(f"  {page['path']} ({page['risk']})", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
