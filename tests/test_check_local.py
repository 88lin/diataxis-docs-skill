"""Tests for scripts/check_local.py.

Each test feeds a deliberately wrong input to one check and asserts the check
reports it. Without these, a validator can silently stop validating.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_local  # noqa: E402


VALID_FIELDS = {
    "name": "diataxis-docs",
    "description": "Apply the Diataxis compass to write and restructure technical documentation.",
    "license": "MIT",
    "metadata": {"version": "0.2.0"},
}
VALID_BODY = "\n".join(["# Title", "", "Body line."])


def fields(**overrides: object) -> dict[str, object]:
    merged = dict(VALID_FIELDS)
    merged.update(overrides)
    return merged


class FrontmatterParsingTests(unittest.TestCase):
    def test_split_frontmatter_ignores_body_delimiter(self) -> None:
        text = "---\nname: x\n---\n\nBody\n\n---\n\nMore body\n"
        frontmatter, body = check_local.split_frontmatter(text)
        self.assertEqual(frontmatter, "name: x")
        self.assertIn("More body", body)

    def test_split_frontmatter_requires_terminator(self) -> None:
        frontmatter, _ = check_local.split_frontmatter("---\nname: x\n")
        self.assertIsNone(frontmatter)

    def test_parse_simple_yaml_reads_nested_map(self) -> None:
        parsed = check_local.parse_simple_yaml('name: demo\nmetadata:\n  version: "0.2.0"\n')
        self.assertEqual(parsed["name"], "demo")
        self.assertEqual(parsed["metadata"], {"version": "0.2.0"})

    def test_parse_simple_yaml_strips_quotes_and_comments(self) -> None:
        parsed = check_local.parse_simple_yaml('name: "demo"  # trailing comment\n')
        self.assertEqual(parsed["name"], "demo")


class SkillFrontmatterTests(unittest.TestCase):
    def setUp(self) -> None:
        check_local.warnings.clear()

    def test_valid_frontmatter_passes(self) -> None:
        self.assertEqual(check_local.check_skill_frontmatter(fields(), VALID_BODY), [])

    def test_uppercase_name_fails(self) -> None:
        problems = check_local.check_skill_frontmatter(fields(name="Diataxis-Docs"), VALID_BODY)
        self.assertTrue(any("must match" in p for p in problems), problems)

    def test_underscore_name_fails(self) -> None:
        problems = check_local.check_skill_frontmatter(fields(name="diataxis_docs"), VALID_BODY)
        self.assertTrue(any("must match" in p for p in problems), problems)

    def test_missing_name_fails(self) -> None:
        problems = check_local.check_skill_frontmatter(fields(name=""), VALID_BODY)
        self.assertTrue(any("missing or empty field: name" in p for p in problems), problems)

    def test_overlong_description_fails(self) -> None:
        long_description = "x" * (check_local.DESCRIPTION_MAX_CHARS + 1)
        problems = check_local.check_skill_frontmatter(fields(description=long_description), VALID_BODY)
        self.assertTrue(any("description is" in p and "max" in p for p in problems), problems)

    def test_long_description_warns_below_hard_limit(self) -> None:
        description = "x" * (check_local.DESCRIPTION_WARN_CHARS + 1)
        problems = check_local.check_skill_frontmatter(fields(description=description), VALID_BODY)
        self.assertEqual(problems, [])
        self.assertTrue(any("dilute trigger matching" in w for w in check_local.warnings))

    def test_oversized_body_fails(self) -> None:
        body = "\n".join(f"line {i}" for i in range(check_local.SKILL_BODY_MAX_LINES + 1))
        problems = check_local.check_skill_frontmatter(fields(), body)
        self.assertTrue(any("body is" in p and "max" in p for p in problems), problems)

    def test_body_near_limit_warns(self) -> None:
        body = "\n".join(f"line {i}" for i in range(check_local.SKILL_BODY_WARN_LINES + 1))
        problems = check_local.check_skill_frontmatter(fields(), body)
        self.assertEqual(problems, [])
        self.assertTrue(any("close to the" in w for w in check_local.warnings))

    def test_unknown_field_warns_but_does_not_fail(self) -> None:
        # OpenCode and Claude Code both ignore unrecognised frontmatter keys,
        # so an unknown key is a warning, not an error.
        problems = check_local.check_skill_frontmatter(fields(version="0.2.0"), VALID_BODY)
        self.assertEqual(problems, [])
        self.assertTrue(any("not recognised by OpenCode" in w for w in check_local.warnings))
        self.assertTrue(any("'version'" in w for w in check_local.warnings))

    def test_non_string_metadata_value_fails(self) -> None:
        problems = check_local.check_skill_frontmatter(fields(metadata={"version": ""}), VALID_BODY)
        self.assertTrue(any("metadata.version" in p for p in problems), problems)


class InstallPathTests(unittest.TestCase):
    def write(self, root: Path, rel: str, text: str) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_mismatched_install_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(
                root,
                "README.md",
                "Clone it:\n\n```bash\ngit clone https://example.com/r.git ~/.config/opencode/skills/diataxis-docs-skill\n```\n",
            )
            problems = check_local.check_install_paths("diataxis-docs", root=root)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("diataxis-docs-skill", problems[0])
            self.assertIn("README.md:4", problems[0])

    def test_matching_install_directory_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(
                root,
                "README.md",
                "```bash\ngit clone https://example.com/r.git ~/.config/opencode/skills/diataxis-docs\n```\n",
            )
            self.assertEqual(check_local.check_install_paths("diataxis-docs", root=root), [])

    def test_placeholder_directory_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "README.md", "Copy into `skills/<name>/`.\n")
            self.assertEqual(check_local.check_install_paths("diataxis-docs", root=root), [])

    def test_repo_name_ending_in_skill_is_not_a_false_positive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "README.md", "Run `python /path/to/diataxis-docs-skill/scripts/export_rules.py`.\n")
            self.assertEqual(check_local.check_install_paths("diataxis-docs", root=root), [])

    def test_bilingual_docs_are_both_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "README.md", "skills/diataxis-docs\n")
            self.write(root, "docs/zh-CN/installation.md", "skills/wrong-name\n")
            problems = check_local.check_install_paths("diataxis-docs", root=root)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("docs/zh-CN/installation.md", problems[0])


class CommandFrontmatterTests(unittest.TestCase):
    def setUp(self) -> None:
        check_local.warnings.clear()

    def write_command(self, root: Path, frontmatter: str) -> None:
        path = root / ".opencode" / "commands" / "docs-test.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}---\n\nRun the command.\n", encoding="utf-8")

    def test_variant_is_recognised(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_command(root, "description: Test command.\nvariant: high\n")
            self.assertEqual(check_local.check_commands(root), [])
            self.assertEqual(check_local.warnings, [])

    def test_name_is_unrecognised_but_only_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_command(root, "name: docs-test\ndescription: Test command.\n")
            self.assertEqual(check_local.check_commands(root), [])
            self.assertTrue(any("'name'" in warning for warning in check_local.warnings))

    def test_description_is_required_by_repository_convention(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_command(root, "agent: build\n")
            problems = check_local.check_commands(root)
            self.assertTrue(any("required by this repository" in problem for problem in problems), problems)


class AnchorTests(unittest.TestCase):
    def test_markdown_anchor_slugifies_headings(self) -> None:
        self.assertEqual(check_local.markdown_anchor("Quick decision tree"), "quick-decision-tree")
        self.assertEqual(check_local.markdown_anchor("Anti-patterns: what NOT to do"), "anti-patterns-what-not-to-do")


class RepositoryTests(unittest.TestCase):
    """The repository itself must satisfy the checks that need no fixtures."""

    def test_repo_skill_frontmatter_is_valid(self) -> None:
        check_local.warnings.clear()
        fields_, body, problems = check_local.load_skill_frontmatter()
        self.assertEqual(problems, [])
        self.assertEqual(check_local.check_skill_frontmatter(fields_, body), [])

    def test_repo_commands_are_valid(self) -> None:
        self.assertEqual(check_local.check_commands(), [])

    def test_repo_evals_are_valid(self) -> None:
        self.assertEqual(check_local.check_evals(), [])


if __name__ == "__main__":
    unittest.main()
