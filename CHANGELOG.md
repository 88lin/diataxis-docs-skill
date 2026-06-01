# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Eval coverage, contributing guidance, and version pinning

#### Added

- `evals/evals.json`: new `non-trigger` category with 4 negative evals (marketing copy, code debugging, translation, generic explanation) so the skill is tested for what it should refuse as well as what it should do.
- `evals/evals.json`: 7 new positive evals in previously under-represented categories (decision-framework, single-page-classification, mixed-form-detection, review, large-system, adjacent-types, anti-pattern-avoidance), plus 1 extra in `classification` and 1 extra in `migration`, bringing the suite from 14 to 27 evals across 11 categories.
- `evals/evals.json`: every non-trigger eval now has `files: []` and the schema description explains that this is the only case where an empty list is correct.
- `SKILL.md`: frontmatter `version: 0.1.0` so the skill has a single, machine-readable version.
- `CONTRIBUTING.md`: full rewrite with sections on good contributions, local validation, adding/editing evals (including the `non-trigger` category and the `files` convention), adding/editing slash commands, style, and a `Versioning and releasing` section that pins `SKILL.md`, `evals/evals.json`, and the CHANGELOG to the same version.
- `examples/messy-to-diataxis/before.md`: every top-level section (and most sub-sections) is now tagged with an HTML comment of the form `<!-- diataxis: <form> -->` so new contributors can see the form of each block in source view.
- `examples/messy-to-diataxis/README.md`: updated the "How to read this example" and "Applying this to your own docs" sections to describe the HTML-comment annotation convention.

#### Changed

- `evals/evals.json`: top-level `version` changed from `1.1.0` to `0.1.0` to match `SKILL.md` frontmatter. Both will move in lockstep on future releases.
- `evals/evals.json`: every eval now has a populated `files` field listing the references inside the repo that back its expected output. `non-trigger` evals are the only ones with `files: []`.
- `scripts/check_local.py` and `.github/workflows/ci.yml`: `known_categories` whitelist extended to include `non-trigger`.
- `README.md` and `README.zh-CN.md`: the `Evals: 14` badge is now `Evals: 27`, and the `Quick decision tree` text in the English README now matches `SKILL.md` exactly (`Acquiring a new skill from scratch?`, `... field, command, or limit?`). The Chinese README's reference branch is extended to `事实、字段、命令或参数上限` for parity.
- `CHANGELOG.md`: the previously noted `Evals: 14` badge entry is now obsolete; the new entry above supersedes it.

### Align SKILL.md with the official Diataxis compass

#### Added

- `SKILL.md`: new `The Diataxis compass` section as the primary classification tool, with the official four-row truth-table from `diataxis.fr/compass/`, the two canonical questions, the "use the compass flexibly" principle, and the "compass can be applied to existing documentation" principle.
- `SKILL.md`: new `Workflow philosophy` section that explicitly encodes the official Diataxis workflow — use as a guide not a plan, do not worry about structure, work one step at a time, structure emerges from the inside.
- `SKILL.md`: new `Anti-patterns for large systems` section that warns against creating empty sections up front, allocating content quotas per quadrant, forcing IA before content is good, and treating "documentation system" as a deliverable.
- `README.md` and `README.zh-CN.md`: rewrote the `How it works` / `核心工作方式` section so the compass is the headline tool, with the truth-table, a link to the source, the official quote, and a new `Workflow philosophy` / `工作流哲学` subsection.

#### Changed

- `SKILL.md`: `Large documentation systems` rewritten to be iterative, not top-down. Inputs are now framed as "ask only what is needed", the artifact map is relabelled "reference map (not a checklist)" and each row now includes its compass cell, and the decision flow is replaced with "How to work iteratively" steps.
- `SKILL.md`: `Workflow` now points to the new `Workflow philosophy` and `Large documentation systems` sections for whole-system work.
- `SKILL.md`: `When to use this skill` now mentions the compass, single-page audit, and one-page-at-a-time work.
- `SKILL.md`: frontmatter `description` now mentions the compass, applies to both new and existing content, and references the iterative workflow.
- `SKILL.md`: `Quick decision tree` now opens with a one-liner saying the compass is the canonical tool and the tree is a quick aid.

### Worked example, slash commands, and CI

#### Added

- `SKILL.md`: new `Quick decision tree` section that gives a one-screen visual aid for picking a Diataxis form before drafting.
- `SKILL.md`: new `When to use this skill` and `When NOT to use this skill` sections that scope the skill explicitly.
- `SKILL.md`: new `Anti-patterns: what NOT to do` section covering the four cardinal sins, per-form anti-patterns, a mixed-doc smell test, README-specific anti-patterns, and adjacent-type anti-patterns.
- `SKILL.md`: new `Per-form final check` list in `Quality checks` for the four primary forms.
- `SKILL.md`: `Large documentation systems` section restructured into a layered deliverable: an inputs table, an output-artifacts table mapped to Diataxis forms, per-platform notes, and a 5-step decision flow.
- `README.md` and `README.zh-CN.md`: new eval-count badge so the eval count is visible at a glance (set to `Evals: 14` at the time; later bumped to `Evals: 27` when the negative-eval pass landed).
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

#### Changed

- `SKILL.md`: reorganized the body so the workflow reads as: classify (decision tree) -> scope (when to use / not to use) -> write (workflow, delivery pattern) -> avoid (anti-patterns) -> scale (large documentation systems) -> reference -> check.
- `SKILL.md`: `Quality checks` now runs both an `Intent check` and a `Mixed-doc smell test` with concrete split signals.
- `SKILL.md`: frontmatter `description` rewritten to be a tighter trigger phrase that covers classification, splitting, reviewing, auditing, and migration alongside the original write / organize / fix / template intents.
- `README.md` and `README.zh-CN.md`: removed the duplicate example prompt in the `Example prompts` / `示例提问` section and expanded the list from 5 to 8 varied prompts.
- `README.md` and `README.zh-CN.md`: updated the table of contents to match the new sections.
- `README.md` and `README.zh-CN.md`: `Repository structure` and `Key files` table extended to include `examples/`, `.opencode/commands/`, `.github/workflows/`, and `scripts/`.
- `evals/evals.json`: added a top-level `version` and `description` field for easier machine consumption.

#### Fixed

- `README.md` and `README.zh-CN.md`: removed duplicate example prompts that appeared twice in `Example prompts` / `示例提问`.
- `README.md` and `README.zh-CN.md`: fixed broken internal links in the worked example (`after/02-how-to.md`, `after/04-explanation.md`) where sibling pages were incorrectly written as `../<file>.md` instead of `<file>.md`.
- `evals/evals.json`: each eval now carries an `id` and a `category`, so coverage gaps are easier to spot.

## Earlier versions

Earlier changes were not tracked with a structured changelog. See the git history for the initial scaffold, bilingual README, visual preview, and large-system planning notes that shipped in earlier iterations.
