#!/usr/bin/env python3
"""Heuristic Diataxis mixed-form smell scanner.

This script does not classify documentation with authority. It scans Markdown
files for signals that a page may be mixing Diataxis forms, then reports the
pages worth reviewing by a human or an AI assistant.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


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


@dataclass
class PageReport:
    path: str
    risk: str
    score: int
    suspected_mix: list[str]
    signals: dict[str, int]
    evidence: list[str]


def iter_markdown_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in {".md", ".mdx"}:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in {".md", ".mdx"}:
            continue
        if any(part in {".git", "node_modules", "dist", "build"} for part in path.parts):
            continue
        yield path


def count_code_blocks(text: str) -> int:
    return len(re.findall(r"^```", text, flags=re.MULTILINE)) // 2


def count_tables(lines: list[str]) -> int:
    return sum(1 for line in lines if line.count("|") >= 2)


def count_steps(lines: list[str]) -> int:
    return sum(1 for line in lines if STEP_RE.search(line) or CN_STEP_RE.search(line))


def count_matches(pattern: re.Pattern[str], text: str) -> int:
    return len(pattern.findall(text))


def analyze_file(path: Path, base: Path) -> PageReport:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    signals = {
        "code_blocks": count_code_blocks(text),
        "tables": count_tables(lines),
        "step_lines": count_steps(lines),
        "explanation_terms": count_matches(EXPLANATION_RE, text) + count_matches(CN_EXPLANATION_RE, text),
        "reference_terms": count_matches(REFERENCE_RE, text) + count_matches(CN_REFERENCE_RE, text),
    }

    suspected_mix: list[str] = []
    evidence: list[str] = []
    score = 0

    reference_weight = signals["tables"] + signals["reference_terms"] + signals["code_blocks"]
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

    if score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    display_path = path.relative_to(base).as_posix() if path.is_relative_to(base) else path.as_posix()
    return PageReport(display_path, risk, score, sorted(set(suspected_mix)), signals, evidence)


def build_report(target: Path) -> dict[str, object]:
    base = target if target.is_dir() else target.parent
    pages = [analyze_file(path, base) for path in iter_markdown_files(target)]
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
            f"code={signals['code_blocks']}; tables={signals['tables']}; "
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Markdown docs for mixed-form Diataxis smell signals.")
    parser.add_argument("target", type=Path, help="Markdown file or documentation directory to scan")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.target.exists():
        print(f"Error: target not found: {args.target}", file=sys.stderr)
        return 2
    report = build_report(args.target)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

