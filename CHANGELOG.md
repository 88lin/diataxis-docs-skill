# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `SKILL.md`: new `Quick decision tree` section that gives a one-screen visual aid for picking a Diataxis form before drafting.
- `SKILL.md`: new `When to use this skill` and `When NOT to use this skill` sections that scope the skill explicitly.
- `SKILL.md`: new `Anti-patterns: what NOT to do` section covering the four cardinal sins, per-form anti-patterns, a mixed-doc smell test, README-specific anti-patterns, and adjacent-type anti-patterns.
- `SKILL.md`: new `Per-form final check` list in `Quality checks` for the four primary forms.
- `SKILL.md`: `Large documentation systems` section restructured into a layered deliverable: an inputs table, an output-artifacts table mapped to Diataxis forms, per-platform notes, and a 5-step decision flow.
- `README.md` and `README.zh-CN.md`: new `Evals: 14` badge so the eval count is visible at a glance.
- `README.md` and `README.zh-CN.md`: new `When NOT to use this skill` (English) / `不适合用在什么场景` (Chinese) section.
- `README.md` and `README.zh-CN.md`: new `Quick decision tree` subsection inside `How it works` / `核心工作方式`.
- `README.md` and `README.zh-CN.md`: new `How this skill differs from generic writing help` / `它和普通写作助手有什么不同` comparison table.
- `README.md` and `README.zh-CN.md`: new `FAQ` / `常见问题` section with 8 representative questions and answers.
- `README.md` and `README.zh-CN.md`: new `Slash commands` / `斜杠命令` section with a table of all five commands.
- `README.md` and `README.zh-CN.md`: new `Worked example` / `完整示例` section pointing at `examples/messy-to-diataxis/`.
- `README.md` and `README.zh-CN.md`: new `Local development` / `本地开发` section explaining `python scripts/check_local.py`.
- `evals/evals.json`: expanded from 3 to 14 evals, each tagged with a `category` (classification, per-form-writing, decision-framework, single-page-classification, mixed-form-detection, review, large-system, migration, adjacent-types, anti-pattern-avoidance).
- `examples/messy-to-diataxis/`: a complete worked example showing a realistic mixed-form page (`before.md`) and the four single-purpose Diataxis pages it should be split into (`after/01-tutorial.md`, `02-how-to.md`, `03-reference.md`, `04-explanation.md`).
- `.opencode/commands/`: five explicit slash commands - `docs-classify.md`, `docs-split.md`, `docs-review.md`, `docs-audit.md`, `docs-quickstart.md`.
- `.github/workflows/ci.yml`: a CI workflow with three jobs - `validate-evals`, `check-internal-links`, `verify-structure`.
- `scripts/check_local.py`: the same checks, runnable locally before pushing.

### Changed

- `SKILL.md`: reorganized the body so the workflow reads as: classify (decision tree) -> scope (when to use / not to use) -> write (workflow, delivery pattern) -> avoid (anti-patterns) -> scale (large documentation systems) -> reference -> check.
- `SKILL.md`: `Quality checks` now runs both an `Intent check` and a `Mixed-doc smell test` with concrete split signals.
- `SKILL.md`: frontmatter `description` rewritten to be a tighter trigger phrase that covers classification, splitting, reviewing, auditing, and migration alongside the original write / organize / fix / template intents.
- `README.md` and `README.zh-CN.md`: removed the duplicate example prompt in the `Example prompts` / `示例提问` section and expanded the list from 5 to 8 varied prompts.
- `README.md` and `README.zh-CN.md`: updated the table of contents to match the new sections.
- `README.md` and `README.zh-CN.md`: `Repository structure` and `Key files` table extended to include `examples/`, `.opencode/commands/`, `.github/workflows/`, and `scripts/`.
- `evals/evals.json`: added a top-level `version` and `description` field for easier machine consumption.

### Fixed

- `README.md` and `README.zh-CN.md`: removed duplicate example prompts that appeared twice in `Example prompts` / `示例提问`.
- `README.md` and `README.zh-CN.md`: fixed broken internal links in the worked example (`after/02-how-to.md`, `after/04-explanation.md`) where sibling pages were incorrectly written as `../<file>.md` instead of `<file>.md`.
- `evals/evals.json`: each eval now carries an `id` and a `category`, so coverage gaps are easier to spot.

## Earlier versions

Earlier changes were not tracked with a structured changelog. See the git history for the initial scaffold, bilingual README, visual preview, and large-system planning notes that shipped in earlier iterations.
