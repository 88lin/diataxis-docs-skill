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

    def test_default_selection_excludes_legacy_and_always_on_variants(self) -> None:
        selected, unknown = export_rules.select_targets([])
        self.assertEqual(unknown, [])
        keys = {target.key for target in selected}
        self.assertIn("cursor", keys)
        self.assertNotIn("cursor-legacy", keys)
        # The native skill is the default for both skill-capable hosts; the
        # always-on rule files are opt-in.
        self.assertIn("claude", keys)
        self.assertNotIn("claude-md", keys)
        self.assertIn("codex", keys)
        self.assertNotIn("codex-md", keys)
        self.assertEqual(len(selected), 11)

    def test_exclusive_groups_are_rejected(self) -> None:
        for group in export_rules.EXCLUSIVE_GROUPS:
            with self.subTest(group=group):
                args = ["--target", tempfile.gettempdir()]
                for key in group:
                    args += ["--only", key]
                output = io.StringIO()
                with redirect_stdout(output), redirect_stderr(output):
                    result = export_rules.main(args)
                self.assertEqual(result, 1)
                self.assertIn("mutually exclusive", output.getvalue())

    def test_claude_target_writes_a_native_skill(self) -> None:
        """Claude Code loads a skill on demand, so it must not be always-on."""
        target = next(item for item in export_rules.TARGETS if item.key == "claude")
        self.assertFalse(target.always_on)
        self.assertEqual(
            target.path.as_posix(), ".claude/skills/diataxis-docs/SKILL.md"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = self.export(root, "claude")
        # The frontmatter name must match the directory or the host ignores it.
        self.assertIn("name: diataxis-docs", content)
        self.assertIn("description:", content.split("---")[1])

    def test_claude_md_target_is_opt_in_and_always_on(self) -> None:
        target = next(item for item in export_rules.TARGETS if item.key == "claude-md")
        self.assertFalse(target.default)
        self.assertTrue(target.always_on)
        self.assertEqual(target.path.as_posix(), "CLAUDE.md")

    def test_assistant_count_ignores_same_tool_variants(self) -> None:
        aliased = {key for group in export_rules.EXCLUSIVE_GROUPS for key in group[1:]}
        self.assertEqual(
            export_rules.assistant_count(), len(export_rules.TARGETS) - len(aliased)
        )

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
            content = self.export(Path(tmp), "copilot", compact=True)
        self.assertNotIn("(#classification-guide)", content)
        self.assert_local_anchor_links_resolve(content)

    def test_codex_target_writes_a_native_skill(self) -> None:
        """Codex discovers .agents/skills/, so the default must not be always-on."""
        target = next(item for item in export_rules.TARGETS if item.key == "codex")
        self.assertFalse(target.always_on)
        self.assertEqual(
            target.path.as_posix(), ".agents/skills/diataxis-docs/SKILL.md"
        )
        with tempfile.TemporaryDirectory() as tmp:
            content = self.export(Path(tmp), "codex")
        self.assertIn("name: diataxis-docs", content)

    def test_codex_md_target_is_opt_in_and_always_on(self) -> None:
        target = next(item for item in export_rules.TARGETS if item.key == "codex-md")
        self.assertFalse(target.default)
        self.assertTrue(target.always_on)
        self.assertEqual(target.path.as_posix(), "AGENTS.md")

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
        self.assertEqual(len(export_rules.TARGETS), 14)

    def test_compact_sections_all_exist_in_skill(self) -> None:
        """--compact selects by exact heading text, so a rename must be caught."""
        body = export_rules.strip_frontmatter(
            export_rules.SKILL_PATH.read_text(encoding="utf-8")
        )
        _, missing = export_rules.extract_sections(body, export_rules.COMPACT_SECTIONS)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
