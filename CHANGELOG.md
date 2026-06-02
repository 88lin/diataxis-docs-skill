# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Review follow-up fixes

#### Changed

- `scripts/export_rules.py`, `README.md`, and `README.zh-CN.md`: expanded the export helper from 9 rule-file targets across 8 assistants to 12 targets across 11 assistants by adding Gemini CLI (`GEMINI.md`), Continue (`.continue/rules/diataxis.md`), and Amazon Q Developer (`.amazonq/rules/diataxis.md`).
- `assets/preview.svg`: refreshed the preview headline from a quote-heavy compass label to a clearer "Two questions, four forms" framing, removed decorative background circles, and replaced the long quote footer with the skill's practical classify-draft-link workflow.

#### Fixed

- `README.md` and `README.zh-CN.md`: clarified the difference between rule-file targets and distinct AI assistants, and added the cross-IDE integration section to the table of contents.
- `README.md` and `README.zh-CN.md`: corrected the blueprint layering note so Diataxis has four core forms, with Quickstart described as a Tutorial sub-type rather than a fifth core form.
- `evals/evals.json`: softened the large-system eval so it asks for an iterative first-pages plan and treats navigation as an emerging sketch, matching the "guide, not a plan" philosophy.
- `references/doc-blueprints.md`: removed hidden zero-width characters from the tutorial code fence.
- `CHANGELOG.md`: fixed the historical self-link to the SKILL.md anti-patterns section.
- `scripts/check_local.py` and `.github/workflows/ci.yml`: extended Markdown validation to catch broken heading anchors and hidden zero-width characters, not just missing linked files.
- `README.md` and `README.zh-CN.md`: updated the local development checklist so it matches the stronger Markdown anchor and zero-width-character validation.

### Compass guidance, FAQ sync, and Before/After visual

#### Changed

- `SKILL.md`: `Use the compass flexibly` now opens with the official "when to use the compass" guidance. The compass is most useful when the work feels routine and the answer is not yet clear, because intuition can give an immediate answer that is also wrong. This pulls in a piece of the official compass page that was previously implicit in the body.
- `SKILL.md`: the compass section now distinguishes the **compass** (a decision tool: two questions + truth-table) from the **Diataxis map** (the static 2x2 quadrant view on diataxis.fr). The map is for orientation; the compass is for decisions; the two are not interchangeable.
- `README.md` and `README.zh-CN.md`: the FAQ "How is the skill evaluated?" answer now reports 29 evals across 11 categories and names the nine coverage areas (classification, mixed-form detection, per-form writing, review, migration, large-system planning, adjacent types, anti-pattern avoidance, non-trigger). The old text claimed 14 evals across 6 categories and had drifted out of sync with the `Evals: 29` badge.
- `README.md` and `README.zh-CN.md`: the `Why this exists` / `为什么要这个 Skill` section now closes with a compact before-and-after file tree showing the `examples/messy-to-diataxis/` split (one mixed-form page → four single-form pages), so a new reader can see concretely what the skill produces.
- `scripts/check_local.py`: `check_skill_frontmatter()` now prints a soft warning when the SKILL.md `description` exceeds 60 words, and adds the word count to the existing OK line. The warning is intentionally not a hard error: the current description is 52 words, well under the budget, and contributors who push past 60 words should see the warning and trim it without the build failing.
- `CHANGELOG.md`: the "Preview image refresh and tag normalization" block has been moved from `[Unreleased]` into `[0.1.0]` so the changelog matches the actual content of the v0.1.0 tag (it was previously listed under Unreleased even though that commit was the one the tag points to).

### Compass, workflow, and tutorial fidelity fixes

#### Changed

- `SKILL.md`: the `Use the compass flexibly` paragraph is now closer to the official diataxis.fr wording. The double "you think that you think" was dropped (the rhetorical self-doubt is captured by the surrounding "— or the documentation in front of you seems to be —" interpolation), but the parenthetical that the compass also applies to existing documentation is now present, and the surrounding sentence reads as a more faithful gloss of the official page.
- `SKILL.md`: the compass-vs-map paragraph no longer speculates about what the official source means by "use the map". It now just defines the term — the *map* is the static 2x2 quadrant diagram on diataxis.fr; the *compass* is the question-based decision tool in this skill — and leaves the "use the map" / "use the compass" rhetorical distinction to the official page itself.
- `SKILL.md`: `Workflow philosophy` now includes the official "organic" metaphor ("the way cells form a tissue") and the "finish and ship" reading of "one step at a time". The first makes the inside-out growth pattern explicit; the second closes the loop on the "small, responsive improvements" point — a step that is never shipped is not an improvement.
- `SKILL.md`: `Tutorial` no longer asks for "a clear learning outcome" (the official tutorial page is explicit that "In this tutorial you will learn …" is presumptuous and recommends "we will create and deploy …" framing). The bullet is now "start with what the reader will do or build".
- `SKILL.md`: `Tutorial` "Good signs" no longer includes `learn` as a trigger keyword. The other signals (`try`, `first time`, `hands-on`, `intro`, `walkthrough`) are all about the reader's stance and stay.
- `SKILL.md`: the `Explanation` anti-pattern "No opinion. An explanation that does not commit to a perspective is just a summary" is now "No point of view or insight. An explanation that neither offers a perspective nor helps the reader form a new understanding is just a summary." The original wording made committing to a perspective a hard requirement, which the official page does not. Context-laying explanations that offer a frame without taking a position are still valid.

### Per-form final check alignment

#### Fixed

- `SKILL.md`: the `Per-form final check` Explanation line still said "the author commits to a perspective" — a direct contradiction of the softened anti-pattern above. It now says "the author offers a point of view or insight", matching the new anti-pattern exactly. Caught during a follow-up review of the same Explanation guidance.

### Bilingual and reference sync

#### Changed

- `README.md` and `README.zh-CN.md`: the `Workflow philosophy` / `工作流哲学` section is now in sync with `SKILL.md`. The English `Work one step at a time` bullet now says "finish and ship each one before starting the next"; the Chinese `一次只做一步` bullet now says "每步做完就发布，再开始下一步". The English `Diataxis changes the structure of your documentation from the inside` bullet now says "allow the work to develop organically and the structure will emerge"; the Chinese `Diataxis 从内部改变文档结构` bullet now says "让工作有机生长，结构会自然浮现". The README is the entry page for most readers, and the missing "ship" wording was a real gap — a step that is never shipped is not an improvement, and the constraint should appear on the entry page.
- `references/doc-blueprints.md`: dropped the redundant `Learning goal` field from the Tutorial blueprint. The blueprint still has `What you will build or do` (a second-person planning field that the writer fills in with the same wording they will use in the output), and `Learning goal` was a near-duplicate that used the "learning" word SKILL.md has been moving away from. One field, no "learning", no redundancy.
- `SKILL.md`: the `Mixed-doc smell test` line "A 'How-to' that begins with a learning outcome statement" is now "A 'How-to' that begins with 'In this tutorial you will learn…' or similar tutorial-style framing". The signal is the same; the wording now uses a concrete verbatim phrase instead of an abstract term that no longer appears in the positive guidance of this skill.

### Eval wording alignment

#### Fixed

- `evals/evals.json`: eval #8's `expected_output` still said "An explanation that commits to a perspective …" — the old hard-requirement wording that the SKILL.md anti-pattern and final check were softened away from. It now says "offers a point of view or insight", matching the new anti-pattern and final check exactly. Caught by a content sweep after the Round 6 softening. The eval was the only place outside the changelog that still used the old wording.

### Cross-IDE helper, trap evals, and Tutorial blueprint refresh

#### Added

- `scripts/export_rules.py`: a helper that reads `SKILL.md`, strips the Opencode-specific frontmatter, and writes the body to `.cursorrules` and `.clinerules` in the current working directory. Existing files are not overwritten. A short preamble (aligned with the "use as a guide, not a plan" philosophy, not the previous "strictly adhering" framing) is prepended so the rules file reads as a guide rather than a directive. This makes the core Diataxis guidance usable in Cursor and Cline / Roo Code workflows without turning the diataxis-docs-skill repo into a multi-IDE project.
- `evals/evals.json`: two new `anti-pattern-avoidance` evals (#30 Quickstart on OAuth2, #31 Reference page that smuggles a 5-step bcrypt guide plus a "best practices" section). Both expected outputs use the soft "the AI should suggest splitting" wording, consistent with the project's "use the compass flexibly" stance. IDs are integers (30, 31) to match the existing 1-29 sequence.
- `README.md` and `README.zh-CN.md`: new `Helper for Cursor and Cline users` / `给 Cursor 和 Cline 用户的辅助脚本` section explaining the export script. The README explicitly notes that the diataxis-docs-skill repo itself is an Opencode skill; the script is a *helper* for users of other AI coding assistants, not a claim that the skill is universally applicable as-is.

#### Changed

- `references/doc-blueprints.md`: the `Tutorial blueprint` is now a concrete markdown skeleton (Action-oriented title, Introduction that states what the reader will build or do, Prerequisites, numbered Steps with an inline bash block and an `*Expected output*` callout, Summary that links to the How-to for real-world variations) wrapped in a `**Goal:** Make the user feel successful` framing. The previous bullet-list form is replaced, not appended, so the file reads as a usable skeleton instead of a checklist. The other blueprints (How-to, Reference, Explanation) keep their existing bullet-list form for now; the Tutorial change is the only one that needed the "what the user will build or do" fix to align with the rest of the skill.
- `scripts/check_local.py`: the `check_structure()` required-files list now includes `scripts/export_rules.py` so the helper cannot be deleted without the build failing.

### Universal AI IDE Integration (9 targets)

#### Changed

- `scripts/export_rules.py`: expanded from 2 targets to 9. The new list covers Cursor (legacy + new rules), Cline, Roo Code, Windsurf, GitHub Copilot, Claude Code, OpenAI Codex, and Aider. The script creates parent directories on demand (e.g., `.github/`, `.cursor/rules/`) with `exist_ok=True` to avoid a benign race when the directory was just created by another process. Existing rule files are still never overwritten; the script prints a skip message and moves on.
- `README.md` and `README.zh-CN.md`: the `Helper for Cursor and Cline users` section is replaced with `Universal AI IDE Integration` / `跨 AI IDE 集成`. The "universally applicable" framing is softened to "portable to other AI coding assistants, though each tool has its own conventions and you may want to adapt the file format to fit your stack". The "automatically formats and places" wording is corrected to "automatically writes the Diataxis rules to the standard rule-file path" — the script does not actually format differently per tool, it writes the same body to each target. The new section closes with a `Tool-specific notes` / `工具适配说明` subsection that honestly documents the two cases where users have to do something after running the script: Cursor new rules and Roo Code work better with a `description:` YAML frontmatter that the script does not add, and Aider requires `CONVENTIONS.md` to be added to the `read:` list in `.aider.conf.yml` to be loaded.

### README and Installation sync

#### Fixed

- `README.md` and `README.zh-CN.md`: the `Repository structure` tree was missing `scripts/export_rules.py` even though the script and its README section were added in the previous round. Added the missing line to both files' directory trees.
- `README.md` and `README.zh-CN.md`: the `Installation` / `安装方式` `Option 2` JSON example used `/path/to/diataxis-docs-skill` while `Option 1` used `~/.config/opencode/skills/diataxis-docs`. The two paths disagreed; a contributor copy-pasting both would have ended up with a config that does not match the clone. Aligned the JSON example to use the same `~/.config/opencode/skills/diataxis-docs` path so the two options now agree end to end.
- `README.md` and `README.zh-CN.md`: the FAQ "How is the skill evaluated?" answer still said "29 sample prompts" even though the suite has been 31 since the trap evals (#30, #31) were added. Changed to "over 30" / "30 多条" so the wording stays correct as the suite grows without becoming a maintenance trap on every new eval.

#### Changed

- `README.md` and `README.zh-CN.md`: the `Included blueprints` / 内置的文档骨架 section now has a one-line layering note after the table. The first 5 rows are the core Diataxis forms (Tutorial, How-to, Reference, Explanation, plus Quickstart as a Tutorial sub-type); the last 4 rows (README, Troubleshooting, Glossary, Release notes) are adjacent types mapped to the closest Diataxis form via the Good Docs Project templates in `references/template-map.md`. All 9 rows are kept (the file actually contains all 9 blueprint sections, so the original 9-row list was accurate — only the layering was missing). The README now mirrors the same core-vs-adjacent split that `references/template-map.md` already uses internally.

### Evals badge count

#### Fixed

- `README.md` and `README.zh-CN.md`: the top-of-page `Evals` shields.io badge hard-coded the value `29` from the original suite size, but the suite has been `31` since the trap evals (#30 Quickstart on OAuth2, #31 Reference page that smuggles a 5-step bcrypt guide) were added. Updated both badges to `Evals-31-blueviolet`. The `over 30` / `30 多条` wording in the FAQ is already in place; this round only fixes the badge.

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
