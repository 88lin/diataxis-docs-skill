# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-31

Documentation-structure release. The repository now follows its own advice: a
short entry README with a bilingual `docs/` tree, a slimmer `SKILL.md`, and
validation scripts that are unit-tested instead of duplicated inside CI.

### Removed

- **Breaking.** `README.md` and `README.zh-CN.md`: dropped the "Option 2" install method that used a `{"skills": {"paths": [...]}}` block in `opencode.json`. OpenCode has no such config key, so that method never worked. Cloning into a `diataxis-docs` directory is now the only documented layout.
- **Breaking.** `SKILL.md`: removed the top-level `version` frontmatter field. It is not part of the skill spec and is silently ignored by the runtime; the value now lives under `metadata.version`.
- `.github/workflows/ci.yml`: removed roughly 11 KB of inline Python that re-implemented `scripts/check_local.py`. The two copies had already drifted apart.
- `SKILL.md`: removed the `Core idea`, `Template selection heuristic`, `Writing patterns`, and `Practical output pattern` sections. Each restated guidance that already appeared elsewhere in the file; the unique content was merged into the sections that kept it.

### Added

- `docs/` and `docs/zh-CN/`: five task-scoped pages per language covering installation, slash commands, IDE integration, development, and FAQ. Both trees are kept in sync by a new parity check.
- `scripts/audit_docs.py`: `--fail-on {none,medium,high}` for CI gating and a repeatable `--exclude GLOB` for files that are legitimately mixed-form, such as the changelog.
- `scripts/export_rules.py`: `--list`, `--dry-run`, `--force`, `--only KEY`, `--target DIR`, and `--compact`. `--compact` exports five decision-critical sections instead of the whole body.
- `scripts/export_rules.py`: a Windsurf modern-format target (`.windsurf/rules/diataxis.md`), bringing the exporter to 13 rule files across 11 assistants.
- `tests/test_check_local.py`: unit tests for frontmatter parsing, name and description validation, install-path scanning, anchor resolution, and the repository's own metadata.
- `.gitignore`: ignores Python build artefacts and every rule file `export_rules.py` can write, so exporting into this repository no longer dirties the tree.
- `references/template-map.md`: an `Artifact to compass cell` table, moved out of `SKILL.md`.
- `evals/evals.json`: a top-level `categories` array listing the 11 categories the 32 evals cover.
- `scripts/check_local.py` and `.github/workflows/ci.yml`: version-consistency check keeping `SKILL.md`, `evals/evals.json`, and `CHANGELOG.md` in agreement.
- `scripts/audit_docs.py`: heuristic scanner flagging pages with mixed-form signals (step-like lines, reference tables, code blocks, explanation terms).
- `references/zh-cn-anti-patterns.md`: Chinese-language documentation smell signals for Chinese-first docs and localization review.
- `evals/evals.json`: a large-system migration eval for a 50-page SDK site, plus two anti-pattern-avoidance evals (a Quickstart on OAuth2, and a Reference page smuggling a 5-step guide).
- `references/doc-blueprints.md`: how-to, reference, and explanation blueprints expanded into concrete Markdown skeletons, matching the tutorial skeleton.

### Changed

- **Breaking.** `scripts/export_rules.py`: the Cursor target is now `.cursor/rules/diataxis.mdc` with `description` and `alwaysApply: false` frontmatter. Cursor ignores plain `.md` files in `.cursor/rules`, so the previous `.md` output was never loaded. Delete any stale `.cursor/rules/diataxis.md` after upgrading.
- **Breaking.** `scripts/audit_docs.py`: the JSON signal key `tables` is now `table_rows`, matching what it counts.
- `README.md` and `README.zh-CN.md`: rewritten as entry pages of about 130 lines. The previous 550-line versions were the only pages in the repository that the bundled audit script rated high risk.
- `SKILL.md`: cut from 463 to 413 lines by removing verbatim repetition. Every remaining topic now has exactly one home.
- `scripts/check_local.py`: rewritten. It validates skill and command frontmatter against the fields OpenCode actually recognises, checks eval structure, resolves Markdown links and heading anchors including HTML `<img src>`, and enforces translation parity.
- `scripts/check_local.py`: unknown frontmatter keys are a warning, not an error. Both OpenCode and Claude Code ignore unrecognised keys, so failing on them would break custom metadata.
- `scripts/check_local.py`: command frontmatter no longer needs a `name`. OpenCode derives the command name from the filename; when `name` is present it must still match.
- `.github/workflows/ci.yml`: rewritten as a single matrix job over Python 3.11 and 3.12, with a read-only token, ref-scoped concurrency, and manual dispatch.
- `scripts/export_rules.py`: emits the frontmatter each target needs and warns when output exceeds a target's character limit (12,000 for modern Windsurf rules, 6,000 for legacy `.windsurfrules`).
- `docs/ide-integration.md`: documents the resident-context cost. Ten of the 13 targets load on every request, roughly 5,200 tokens for a full export against roughly 2,300 for `--compact`.
- `scripts/export_rules.py`: expanded from 2 targets to 9 (Cursor legacy and modern, Cline, Roo Code, Windsurf, Copilot, Claude Code, Codex, Aider), then to 12 with Gemini CLI, Continue, and Amazon Q Developer.
- `scripts/export_rules.py`: reads `SKILL.md` from the skill repository but writes rule files into the target directory, so it is safe to run inside another project.
- `SKILL.md` and `references/reader-analysis.md`: added a tutorial-versus-how-to fallback that asks one clarifying question and defaults to a focused how-to only when the user cannot answer.
- `SKILL.md`: the compass section now separates the *compass* (two questions plus a truth table, a decision tool) from the *map* (the static 2x2 diagram on diataxis.fr, an orientation tool), and opens with the official guidance that the compass earns its keep when the work feels routine but the answer is not yet obvious.
- `SKILL.md`: `Workflow philosophy` now carries the official organic metaphor and reads "one step at a time" as finish-and-ship, since a step that is never shipped is not an improvement.
- `SKILL.md`: Tutorial guidance no longer asks for a stated learning outcome. The official tutorial page treats "In this tutorial you will learn…" as presumptuous, so the bullet is now "start with what the reader will do or build", and `learn` was dropped from the trigger keywords.
- `SKILL.md`, `evals/evals.json`: the Explanation requirement to "commit to a perspective" is now "offers a point of view or insight". Context-laying explanations that frame a topic without taking a position are valid.
- `assets/preview.svg`: redrawn as an actual compass with axis labels, the four forms in their correct cells, and the classify-draft-link workflow in the footer.

### Fixed

- `scripts/audit_docs.py`: a line containing two or more pipe characters was counted as a table row, so shell pipelines inside code blocks inflated the reference signal. Tables now require a header row followed by a separator row, and fenced code blocks and frontmatter are excluded from prose signals.
- `scripts/export_rules.py`: `strip_frontmatter()` used `content.split("---", 2)`, which truncated the body at the first thematic break in the document. It now matches the frontmatter delimiters as anchored line boundaries.
- `scripts/export_rules.py`: write failures and unknown `--only` keys exited 0. They now exit 1.
- `scripts/check_local.py`: the install-path scanner read `diataxis-docs-skill/scripts` as a `skills/scripts` install path and reported a false positive. The pattern now requires a word boundary before `skills/`.
- `scripts/check_local.py`: frontmatter parsing no longer strips a `#` that appears inside a quoted value.
- `SKILL.md`: the intent check referred to a "Diataxis decision tree" section that does not exist. It now points at the compass.
- `references/doc-blueprints.md`: removed hidden zero-width characters from the tutorial code fence; `check_local.py` now catches them.
- `scripts/check_local.py`: Markdown validation now catches broken heading anchors.
- `README.md` and `README.zh-CN.md`: corrected the blueprint layering note so Diataxis has four core forms, with Quickstart as a tutorial sub-type rather than a fifth form.
- `evals/evals.json`: the large-system eval now asks for an iterative first-pages plan and treats navigation as an emerging sketch, matching the guide-not-a-plan philosophy.
- `README.md` and `README.zh-CN.md`: the two install options previously used different target paths, and the evals count drifted out of sync with its badge. Both are resolved by the rewrite.

## [0.1.0] - 2026-06-02

First tagged release. Includes the four rounds of changes accumulated since the previous unreleased state.

### Frontmatter hygiene, decision-tree fix, and eval expansion

#### Added

- `evals/evals.json`: 2 new evals in the two highest-frequency categories — `classification` (#28, glossary placement) and `mixed-form-detection` (#29, 1 200-line Authentication guide). Suite is now 29 evals across 11 categories, with `classification` and `mixed-form-detection` at 3 each.
- `evals/evals.json`: top-level `description` now explicitly states that for `non-trigger` evals `files` is empty because the skill must not read any reference files.
- `scripts/check_local.py`: new `check_skill_frontmatter()` that verifies `SKILL.md` has an opening `---` delimiter, a closing `---` delimiter, and non-empty `name`, `version`, and `description` fields. Wired into `main()` alongside the other checks.
- `.github/workflows/ci.yml`: new "Check SKILL.md frontmatter" step inside the `verify-structure` job, using the same logic as `check_skill_frontmatter()` so a broken frontmatter breaks CI before it can be merged.
- `.github/ISSUE_TEMPLATE/`: four issue templates — `bug_report.md`, `feature_request.md`, `docs.md`, `question.md` — each with a YAML frontmatter that drives the GitHub picker.
- `.github/PULL_REQUEST_TEMPLATE.md`: a short checklist-style PR template that requires `python scripts/check_local.py` to pass, requires bilingual parity, and reminds contributors to bump all three version sources together.

#### Changed

- `SKILL.md`: frontmatter `description` is now trigger-only. Removed the 10-item doc-type enumeration and the trailing "apply the compass flexibly / work one page at a time" workflow guidance, both of which duplicated body content and hurt trigger matching.
- `SKILL.md`: `Core idea` collapsed from a 4-type list into a single sentence that points at the compass and the classification guide.
- `SKILL.md`: `Large documentation systems` softened. "Inputs to gather" is now a single prose paragraph (the table was reading as a checklist). "Reference map" was renamed to "Common artifact patterns (for reference only)" and prefixed with a "Do not treat this as a backlog. Only produce artifacts the compass calls for." warning.
- `SKILL.md`: `Quality checks` no longer duplicates the Mixed-doc smell test. The Quality Checks section now opens by pointing at the canonical smell test in [Anti-patterns: what NOT to do](SKILL.md#anti-patterns-what-not-to-do) instead of repeating the same checklist inline. Net: 478 -> 444 lines.
- `README.md` and `README.zh-CN.md`: the `Quick decision tree` ASCII art now correctly shows Explanation as a sibling of Reference (same indentation as the other root branches), not as a sub-branch.
- `README.zh-CN.md`: the compass table header changed from "那么它一定属于" to "那么它归入" to soften the mandatory tone and stay consistent with the workflow philosophy.

#### Fixed

- `SKILL.md`, `README.md`, `README.zh-CN.md`: the Quick decision tree ASCII art had a stray `│` on the line between Reference and Explanation that visually placed Explanation as a child of Reference. Both the stray rail and the alignment of the `→` arrow are now correct.

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

### Preview image refresh and tag normalization

#### Changed

- `assets/preview.svg`: regenerated. The preview is now an actual Diataxis compass — a 2x2 grid with the two axis labels (ACQUISITION / APPLICATION at the top, ACTION / COGNITION rotated on the left), the four forms placed in their correct compass cells (Tutorial = action + acquisition, How-to = action + application, Explanation = cognition + acquisition, Reference = cognition + application), the official compass quote, and a subtle cross-hair down the middle to make the structure explicit. Each card has a tinted background gradient and a colored left bar keyed to the form (green / amber / purple / cyan).
- `examples/messy-to-diataxis/before.md`: replaced the non-standard `explanation-light` tags (and the related `troubleshooting` and `mixed entry point` labels) with the strict 4-form vocabulary. The convention is now: use one of `tutorial`, `how-to`, `reference`, `explanation` for a real Diataxis form; use `meta: <role>` for things that are not a form at all (page-level framing, scope notes, link farms). Final tag count: 4 forms + 4 `meta:` = 23 tags, zero non-standard labels.
- `examples/messy-to-diataxis/README.md`: updated "How to read this example" and "Applying this to your own docs" to describe the form-or-`meta:` convention.

## Earlier versions

Earlier changes were not tracked with a structured changelog. See the git history for the initial scaffold, bilingual README, visual preview, and large-system planning notes that shipped in earlier iterations.
