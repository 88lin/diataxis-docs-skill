"""Tests for the rule files actually written by scripts/export_rules.py."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import export_rules  # noqa: E402


class ExportRulesTests(unittest.TestCase):
    def export(self, root: Path, key: str, *, compact: bool = False) -> str:
        args = ["--target", str(root), "--only", key]
        if compact:
            args.append("--compact")
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            result = export_rules.main(args)
        self.assertEqual(result, 0, output.getvalue())
        target = next(item for item in export_rules.TARGETS if item.key == key)
        return (root / target.path).read_text(encoding="utf-8")

    def assert_local_anchor_links_resolve(self, content: str) -> None:
        anchors = export_rules.heading_anchors(content)
        missing = [
            match.group(2)
            for match in export_rules.MARKDOWN_LINK_RE.finditer(content)
            if match.group(2).startswith("#") and match.group(2)[1:] not in anchors
        ]
        self.assertEqual(missing, [])

    def test_default_selection_excludes_legacy_cursor(self) -> None:
        selected, unknown = export_rules.select_targets([])
        self.assertEqual(unknown, [])
        keys = {target.key for target in selected}
        self.assertIn("cursor", keys)
        self.assertNotIn("cursor-legacy", keys)
        self.assertEqual(len(selected), 11)

    def test_cursor_targets_are_mutually_exclusive(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            result = export_rules.main(
                ["--target", tempfile.gettempdir(), "--only", "cursor", "--only", "cursor-legacy"]
            )
        self.assertEqual(result, 1)
        self.assertIn("mutually exclusive", output.getvalue())

    def test_cline_export_uses_rule_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.export(root, "cline")
            self.assertTrue((root / ".clinerules").is_dir())
            self.assertTrue((root / ".clinerules" / "diataxis.md").is_file())

    def test_default_windsurf_export_falls_back_to_compact(self) -> None:
        target = next(item for item in export_rules.TARGETS if item.key == "windsurf")
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with redirect_stdout(output), redirect_stderr(output):
                result = export_rules.main(["--target", str(root), "--only", "windsurf"])
            self.assertEqual(result, 0, output.getvalue())
            content = (root / target.path).read_text(encoding="utf-8")
        self.assertLessEqual(len(content), target.char_limit)
        self.assertIn("using compact output", output.getvalue())

    def test_compact_export_has_no_dead_local_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            content = self.export(Path(tmp), "codex", compact=True)
        self.assertNotIn("(#classification-guide)", content)
        self.assert_local_anchor_links_resolve(content)

    def test_full_export_uses_absolute_links_for_repository_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            content = self.export(Path(tmp), "cursor")

        targets = [match.group(2) for match in export_rules.MARKDOWN_LINK_RE.finditer(content)]
        relative = [
            target
            for target in targets
            if not target.startswith(("#", "http://", "https://", "mailto:"))
        ]
        self.assertEqual(relative, [])
        self.assertIn(
            export_rules.REPOSITORY_BLOB_BASE + "references/template-map.md",
            targets,
        )
        self.assert_local_anchor_links_resolve(content)

    def test_windsurf_compact_export_fits_modern_limit(self) -> None:
        target = next(item for item in export_rules.TARGETS if item.key == "windsurf")
        self.assertIsNotNone(target.char_limit)
        with tempfile.TemporaryDirectory() as tmp:
            content = self.export(Path(tmp), "windsurf", compact=True)
        self.assertLessEqual(len(content), target.char_limit)

    def test_legacy_windsurf_target_is_not_offered(self) -> None:
        selected, unknown = export_rules.select_targets(["windsurf-legacy"])
        self.assertEqual(selected, [])
        self.assertEqual(unknown, ["windsurf-legacy"])
        self.assertEqual(len(export_rules.TARGETS), 12)


if __name__ == "__main__":
    unittest.main()
