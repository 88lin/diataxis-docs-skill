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

    def test_missing_target_returns_two(self) -> None:
        self.run_script("does/not/exist", expect_code=2)


if __name__ == "__main__":
    unittest.main()
