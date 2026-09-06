import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "audit_docs.py"

sys.path.insert(0, str(ROOT / "scripts"))

import audit_docs  # noqa: E402


class AuditHelpers(unittest.TestCase):
    """Unit tests for the counting helpers that decide a page's signals."""

    def test_shell_pipes_in_code_blocks_are_not_tables(self) -> None:
        text = """# Ops runbook

```bash
ls -la | grep skill | wc -l
cat access.log | awk '{print $1}' | sort | uniq -c
ps aux | grep python | head -n 5
```
"""
        signals, _, _, _ = audit_docs.analyze_text(text)
        self.assertEqual(signals["table_rows"], 0)
        self.assertEqual(signals["code_blocks"], 1)

    def test_real_table_rows_are_counted_without_separator(self) -> None:
        text = """# Reference

| Field | Type |
| --- | --- |
| id | string |
| name | string |
| size | integer |
"""
        signals, _, _, _ = audit_docs.analyze_text(text)
        # 1 header row + 3 body rows; the `| --- |` separator is excluded.
        self.assertEqual(signals["table_rows"], 4)

    def test_pipe_lines_without_separator_are_not_a_table(self) -> None:
        text = "# Notes\n\nUse `a | b` or run foo | bar in your shell.\n\nAnother | line | here.\n"
        signals, _, _, _ = audit_docs.analyze_text(text)
        self.assertEqual(signals["table_rows"], 0)

    def test_frontmatter_is_excluded_from_text_signals(self) -> None:
        text = """---
description: Why the architecture has this design tradeoff and background
---

# Title

Plain body text.
"""
        signals, _, _, _ = audit_docs.analyze_text(text)
        self.assertEqual(signals["explanation_terms"], 0)

    def test_code_block_contents_are_excluded_from_text_signals(self) -> None:
        text = """# Title

```python
# why this design has a tradeoff: background and architecture rationale
value = 1
```
"""
        signals, _, _, _ = audit_docs.analyze_text(text)
        self.assertEqual(signals["explanation_terms"], 0)
        self.assertEqual(signals["code_blocks"], 1)

    def test_tilde_and_nested_fences_are_handled(self) -> None:
        text = """# Title

~~~markdown
```bash
echo hi | wc -l
```
~~~
"""
        signals, _, _, _ = audit_docs.analyze_text(text)
        self.assertEqual(signals["code_blocks"], 1)
        self.assertEqual(signals["table_rows"], 0)


class AuditDocsCliTests(unittest.TestCase):
    def write_file(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_script(self, *args: str, expect_code: int = 0) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, expect_code, msg=proc.stderr)
        return proc

    MIXED_PAGE = """# Authentication

## Why OAuth works this way

This design has tradeoffs and background worth understanding.

## Configure authentication

1. Create an app.
2. Set the callback URL.
3. Copy the client secret.
4. Run the login command.

| Field | Description |
| --- | --- |
| client_id | OAuth client identifier |
| client_secret | OAuth client secret |
| callback_url | Redirect URL |

```bash
tool auth login
```

```json
{"token": "example"}
```
"""

    def test_mixed_page_is_high_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "auth.md", self.MIXED_PAGE)
            report = json.loads(self.run_script(str(root), "--format", "json").stdout)
            item = report["pages"][0]
            self.assertEqual(item["risk"], "high")
            self.assertIn("how-to/reference", item["suspected_mix"])
            self.assertIn("explanation", item["suspected_mix"])

    def test_reference_page_is_low_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(
                root / "api.md",
                """# API parameters

| Field | Type | Description |
| --- | --- | --- |
| id | string | Resource ID |
| status | string | Current state |

```json
{"id": "ord_123", "status": "paid"}
```
""",
            )
            report = json.loads(self.run_script(str(root), "--format", "json").stdout)
            item = report["pages"][0]
            self.assertEqual(item["risk"], "low")
            self.assertEqual(item["suspected_mix"], [])

    def test_markdown_output_includes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "guide.md", "# Guide\n\n1. Install.\n2. Configure.\n")
            proc = self.run_script(str(root))
            self.assertIn("# Diataxis Smell Scan", proc.stdout)
            self.assertIn("Pages scanned:", proc.stdout)

    def test_fail_on_high_returns_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "auth.md", self.MIXED_PAGE)
            proc = self.run_script(str(root), "--fail-on", "high", expect_code=1)
            self.assertIn("FAIL", proc.stderr)
            self.assertIn("auth.md", proc.stderr)

    def test_fail_on_high_passes_for_clean_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "guide.md", "# Guide\n\nA short explanation page.\n")
            self.run_script(str(root), "--fail-on", "high", expect_code=0)

    def test_install_how_to_is_not_flagged(self) -> None:
        """Commands and a troubleshooting table do not make a page mixed-form.

        A how-to is expected to be full of code blocks and may legitimately end
        in a symptom/cause/fix table. Counting either as reference evidence made
        every installation guide look like a reference page with instructions.
        """
        page = """# Install the thing

## Install

Run this from the project root:

```bash
git clone https://example.com/thing.git
```

```bash
cd thing && make install
```

```bash
thing --version
```

```bash
thing init
```

## Verify

Set `THING_HOME`, then confirm the version:

```bash
echo "$THING_HOME"
```

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| Command not found | Not on PATH | Add the bin directory to PATH |
| Version mismatch | Stale build | Re-run make install |
| Nothing happens | Config missing | Copy the sample config |
"""
        signals, mix, _, score = audit_docs.analyze_text(page)
        self.assertEqual(mix, [], signals)
        self.assertEqual(score, 0, signals)

    def test_how_to_with_reference_table_is_still_flagged(self) -> None:
        """Reference vocabulary beside steps is the signal that must survive."""
        page = """# Configure webhooks

1. Run the create command.
2. Set the endpoint URL.
3. Verify the signature.

| Parameter | Type | Limit |
| --- | --- | --- |
| url | string | 2048 |
| secret | string | 64 |
| retries | integer | 5 |
"""
        signals, mix, _, score = audit_docs.analyze_text(page)
        self.assertIn("how-to/reference", mix)
        self.assertGreaterEqual(score, 3, signals)

    def test_weak_signal_alone_does_not_reach_medium_risk(self) -> None:
        """The +1 code-blocks rule must not promote an otherwise clean page."""
        signals, mix, _, score = audit_docs.analyze_text(
            "# Guide\n\n"
            + "Run the command:\n\n```bash\nrun\n```\n\n" * 4
            + "Install the package:\n\nSet the value:\n"
        )
        self.assertNotIn("tutorial/how-to", mix)
        self.assertLess(score, 2, signals)

    def test_chinese_instructions_are_counted(self) -> None:
        for line in (
            "在项目根目录运行：",
            "1. 安装依赖",
            "- 复制配置文件",
            "采用项目级安装时：",
        ):
            with self.subTest(line=line):
                self.assertEqual(audit_docs.count_steps([line]), 1)

    def test_chinese_headings_and_tables_are_not_steps(self) -> None:
        """These lines contain instruction verbs used as nouns, not as steps."""
        for line in (
            "## 安装到 Claude Code",
            "### 全局安装",
            "| Skill 从不触发 | 目录名不对 | 重命名目录 |",
            "> 存放 SKILL.md 的目录必须命名为 diataxis-docs",
            "- `tests/test_check_local.py` 给每个检查喂进故意写错的输入，断言它确实被抓住了",
        ):
            with self.subTest(line=line):
                self.assertEqual(audit_docs.count_steps([line]), 0)

    def test_diataxis_vocabulary_is_not_reference_vocabulary(self) -> None:
        """`反模式` and `文档类型` are Diataxis terms, not interface terms.

        Matching them made any page that discusses Diataxis itself look like a
        reference page.
        """
        text = "反模式清单说明了文档类型的选择，以及模式匹配的边界。"
        self.assertEqual(audit_docs.count_matches(audit_docs.CN_REFERENCE_RE, text), 0)
        self.assertEqual(
            audit_docs.count_matches(audit_docs.CN_REFERENCE_RE, "参数与字段的取值范围"), 3
        )

    def test_translated_pages_score_the_same(self) -> None:
        """A translation must not score differently from its English original.

        The signal patterns are per-language, so drift between them shows up as
        one language flagging a page the other considers clean.
        """
        pairs = [
            ("docs/installation.md", "docs/zh-CN/installation.md"),
            ("docs/development.md", "docs/zh-CN/development.md"),
            ("docs/commands.md", "docs/zh-CN/commands.md"),
            ("docs/faq.md", "docs/zh-CN/faq.md"),
            ("docs/ide-integration.md", "docs/zh-CN/ide-integration.md"),
        ]
        for english, chinese in pairs:
            with self.subTest(page=english):
                left = audit_docs.analyze_file(ROOT / english, ROOT)
                right = audit_docs.analyze_file(ROOT / chinese, ROOT)
                self.assertEqual(
                    left.risk,
                    right.risk,
                    f"{english} is {left.risk} but {chinese} is {right.risk}",
                )

    def test_exclude_skips_matching_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "auth.md", self.MIXED_PAGE)
            self.write_file(root / "guide.md", "# Guide\n\nShort page.\n")
            self.run_script(str(root), "--exclude", "auth.md", "--fail-on", "high", expect_code=0)
            report = json.loads(
                self.run_script(str(root), "--exclude", "auth.md", "--format", "json").stdout
            )
            self.assertEqual(report["pages_scanned"], 1)
            self.assertEqual(report["pages"][0]["path"], "guide.md")

    def test_explicit_excluded_directory_name_is_still_scanned(self) -> None:
        for directory_name in ("site", "build"):
            with self.subTest(directory_name=directory_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / directory_name
                self.write_file(root / "guide.md", "# Guide\n\nInstall the tool.\n")
                report = json.loads(self.run_script(str(root), "--format", "json").stdout)
                self.assertEqual(report["pages_scanned"], 1)
                self.assertEqual(report["pages"][0]["path"], "guide.md")

    def test_nested_excluded_directory_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "guide.md", "# Guide\n\nInstall the tool.\n")
            self.write_file(root / "site" / "generated.md", "# Generated\n")
            report = json.loads(self.run_script(str(root), "--format", "json").stdout)
            self.assertEqual(report["pages_scanned"], 1)
            self.assertEqual(report["pages"][0]["path"], "guide.md")

    def test_missing_target_returns_two(self) -> None:
        self.run_script("does/not/exist", expect_code=2)


if __name__ == "__main__":
    unittest.main()
