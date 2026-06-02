import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "audit_docs.py"


class AuditDocsTests(unittest.TestCase):
    def write_file(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_mixed_page_is_high_risk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(
                root / "auth.md",
                """# Authentication

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
""",
            )

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--format", "json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            report = json.loads(proc.stdout)
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

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--format", "json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            report = json.loads(proc.stdout)
            item = report["pages"][0]

            self.assertEqual(item["risk"], "low")
            self.assertEqual(item["suspected_mix"], [])

    def test_markdown_output_includes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_file(root / "guide.md", "# Guide\n\n1. Install.\n2. Configure.\n")

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )

            self.assertIn("# Diataxis Smell Scan", proc.stdout)
            self.assertIn("Pages scanned:", proc.stdout)


if __name__ == "__main__":
    unittest.main()
