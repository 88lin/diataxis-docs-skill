<div align="center">

# Diataxis Docs Skill 📚

**A reusable Opencode skill for writing structured, user-first technical documentation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill: Opencode](https://img.shields.io/badge/Skill-Opencode-111827)](SKILL.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb)](https://diataxis.fr/)
[![Docs: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a)](https://www.thegooddocsproject.dev/)
[![Evals: 29](https://img.shields.io/badge/Evals-29-blueviolet)](evals/evals.json)
[![GitHub stars](https://img.shields.io/github/stars/88lin/diataxis-docs-skill?style=social)](https://github.com/88lin/diataxis-docs-skill)

[Chinese](README.zh-CN.md) · [Skill file](SKILL.md) · [Blueprints](references/doc-blueprints.md) · [Template map](references/template-map.md)

</div>

---

## Preview

<p align="center">
  <img src="assets/preview.svg" alt="Diataxis Docs Skill preview" width="100%">
</p>

```text
User need                 Diataxis form        Output style
────────────────────────────────────────────────────────────────
Learn by doing            Tutorial             Guided lesson
Complete a real task      How-to guide          Practical steps
Look up exact facts       Reference             Structured facts
Understand why            Explanation           Context and tradeoffs
```

---

## Table of Contents

- [Why this exists](#why-this-exists)
- [What this skill helps with](#what-this-skill-helps-with)
- [When NOT to use this skill](#when-not-to-use-this-skill)
- [How it works](#how-it-works)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Example prompts](#example-prompts)
- [Slash commands](#slash-commands)
- [Worked example](#worked-example)
- [Included blueprints](#included-blueprints)
- [Design principles](#design-principles)
- [How this skill differs from generic writing help](#how-this-skill-differs-from-generic-writing-help)
- [Local development](#local-development)
- [FAQ](#faq)
- [Sources](#sources)
- [Contributing](#contributing)
- [License](#license)

---

## Why this exists

Most documentation problems are classification problems.

When a single page tries to teach a beginner, guide a working user, list API facts, explain design tradeoffs, and troubleshoot errors all at once, the page becomes noisy. Beginners feel lost, experienced users cannot find the facts, and maintainers do not know where new content belongs.

This skill uses the [Diataxis](https://diataxis.fr/) framework to help an AI assistant decide what kind of document is needed before writing it.

The goal is simple:

- choose the right document type
- write for the reader's actual state
- keep each page focused on one user need
- link related material instead of mixing everything together
- make documentation easier to maintain over time

What a "noisy" page looks like in practice — one of the smallest worked examples in this repo:

```text
BEFORE  examples/messy-to-diataxis/before.md     # 1 page, 4 jobs at once

AFTER   examples/messy-to-diataxis/after/
        ├── 01-tutorial.md                       # tutorial
        ├── 02-how-to.md                         # how-to
        ├── 03-reference.md                      # reference
        └── 04-explanation.md                    # explanation
```

The full before-and-after is in [`examples/messy-to-diataxis/`](examples/messy-to-diataxis/); the [Worked example](#worked-example) section below walks through the split.

---

## What this skill helps with

Use this skill when you want to write, rewrite, organize, or review technical documentation such as:

- tutorials
- how-to guides
- reference documentation
- explanation or concept articles
- quickstarts
- READMEs
- troubleshooting guides
- glossaries
- release notes
- documentation style guides

It is especially useful for prompts like:

- "Help me organize this documentation site."
- "Turn this messy guide into Diataxis-style docs."
- "Write a README and quickstart for this project."
- "Split this page into tutorial, how-to, reference, and explanation."
- "Review this documentation structure and tell me what is mixed together."
- "Design a Diataxis documentation system for my SDK or API."
- "Classify this single page and tell me what kind of document it should be."
- "Audit our docs site and flag pages that mix Diataxis forms."
- "Migrate our existing docs to a Diataxis-based system."

## When NOT to use this skill

This skill is intentionally scoped. Do not use it for:

- marketing copy, blog posts, or non-technical writing
- purely visual content such as UI mockups, slides, or design specs
- code review, refactoring, or implementation work
- short responses that do not need a documentation structure
- translating already-structured documentation between languages

If the request is about _what_ to say more than _which kind of document_ to write, you are outside this skill's scope.

---

## How it works

The skill is built around the [Diataxis compass](https://diataxis.fr/compass/) — a two-question truth-table that maps any piece of content to exactly one of four forms.

| If the content… | …and serves the user's… | …then it must belong to… |
| --- | --- | --- |
| informs action | acquisition of skill | a tutorial |
| informs action | application of skill | a how-to guide |
| informs cognition | application of skill | reference |
| informs cognition | acquisition of skill | explanation |

The compass can be applied to a single sentence, a page, or a whole documentation set. It can be applied to new content, and equally well to existing content that may need to be moved.

> "The compass can be applied equally to user situations that need documentation, or to documentation itself that perhaps needs to be moved or improved. Like many good tools, it's surprisingly banal." — diataxis.fr/compass

### Quick decision tree

If you are not sure which form a request belongs to, walk through this:

```text
What is the reader trying to do right now?
│
├── Acquiring a new skill from scratch?
│   ├── With a complete, guided lesson → Tutorial
│   └── With the shortest path to first success → Quickstart
│
├── Applying a known skill to a real task?
│   ├── General task with a clear goal → How-to
│   └── Stuck on an error → Troubleshooting
│
├── Looking up an exact fact, field, command, or limit? → Reference
│
└── Trying to understand why or how it works?            → Explanation
```

The skill also ships an **anti-patterns checklist** that flags the most common failure mode: a single page that mixes two or more of these forms. The full checklist is in [`SKILL.md`](SKILL.md#anti-patterns-what-not-to-do).

### Workflow philosophy

Diataxis is meant to be used as a guide, not as a plan. The skill follows the official workflow:

- **Use Diataxis as a guide, not a plan.** Apply the compass where you are, not where you wish you were.
- **Do not worry about structure.** Focus on content quality. The structure emerges from the work.
- **Work one step at a time.** Make small, responsive improvements; finish and ship each one before starting the next. Do not plan a complete rewrite before starting.
- **Diataxis changes the structure of your documentation from the inside.** It is not a template to impose on top of existing content; allow the work to develop organically and the structure will emerge.

In other words, a messy page that is honest about its content is better than a clean four-section site with nothing in three of the four sections.

---

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── assets/
│   └── preview.svg
├── references/
│   ├── doc-blueprints.md
│   ├── reader-analysis.md
│   └── template-map.md
├── evals/
│   └── evals.json
├── examples/
│   └── messy-to-diataxis/
│       ├── README.md
│       ├── before.md
│       └── after/
│           ├── 01-tutorial.md
│           ├── 02-how-to.md
│           ├── 03-reference.md
│           └── 04-explanation.md
├── .opencode/
│   └── commands/
│       ├── docs-classify.md
│       ├── docs-split.md
│       ├── docs-review.md
│       ├── docs-audit.md
│       └── docs-quickstart.md
├── .github/
│   └── workflows/
│       └── ci.yml
└── scripts/
    └── check_local.py
```

### Key files

| File | Purpose |
| --- | --- |
| `SKILL.md` | Main skill instructions, trigger guidance, classification logic, and quality checks |
| `references/reader-analysis.md` | Reader-first checklist before drafting documentation |
| `references/doc-blueprints.md` | Reusable structures for common documentation types |
| `references/template-map.md` | Mapping between Diataxis forms and Good Docs Project templates |
| `evals/evals.json` | Sample prompts for checking whether the skill behaves as expected |
| `examples/messy-to-diataxis/` | Worked example: a mixed-form page and the four Diataxis pages it should split into |
| `.opencode/commands/` | Slash commands (`/docs-classify`, `/docs-split`, `/docs-review`, `/docs-audit`, `/docs-quickstart`) |
| `.github/workflows/ci.yml` | CI that validates evals.json, internal links, and repository structure |
| `scripts/check_local.py` | The same checks, runnable locally before pushing |
| `assets/preview.svg` | Preview art for the GitHub README header |

---

## Installation

### Option 1: clone into an Opencode skill directory

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git ~/.config/opencode/skills/diataxis-docs
```

Restart Opencode after cloning so the skill list is reloaded.

### Option 2: add the repository path to `skills.paths`

Add the folder path to your `opencode.json`:

```jsonc
{
  "skills": {
    "paths": ["/path/to/diataxis-docs-skill"]
  }
}
```

Then restart Opencode.

---

## Example prompts

A small set of representative prompts the skill is designed to handle well:

```text
Design a Diataxis documentation system for my SDK or API.
```

```text
Write a README and quickstart for this developer tool.
```

```text
Turn this API page into a proper reference document.
```

```text
Review this documentation and tell me where it mixes concepts, procedures, and reference data.
```

```text
Classify this single docs page and tell me what kind of document it should be.
```

```text
Migrate our existing docs to a Diataxis-based system.
```

```text
Write a troubleshooting guide for the top five errors our users hit.
```

```text
Refactor this mega-page that tries to teach, instruct, list, and explain at once.
```

---

## Slash commands

The skill ships with explicit slash commands in [`.opencode/commands/`](.opencode/commands/). Use them when you want the AI to behave in a specific Diataxis mode without relying on natural-language triggering.

| Command | What it does |
| --- | --- |
| `/docs-classify` | Classify a single page or paste using the decision tree; flag mixed forms |
| `/docs-split` | Split a mixed-form page into the right Diataxis documents and draft each one |
| `/docs-review` | Pre-publication review of a draft, with severity-tagged findings |
| `/docs-audit` | Page-by-page audit of a docs directory or list of pages |
| `/docs-quickstart` | Draft a short, opinionated quickstart that gets a user to first success |

Each command file documents its own output shape. The commands are best used as a starting point: read the prompt, then paste the page or path you want to process.

---

## Worked example

See [`examples/messy-to-diataxis/`](examples/messy-to-diataxis/) for a complete before-and-after. The `before.md` file is a realistic "Getting Started" page that mixes a tutorial, a how-to, a reference table, and a design explanation. The `after/` directory shows how the same content should be split into four single-purpose pages.

The example is intentionally short but representative. The recommended procedure is:

1. Open `before.md` and tag each section as tutorial, how-to, reference, or explanation.
2. Group sections by tag.
3. For each group, write a new page using the matching blueprint from `references/doc-blueprints.md`.
4. Replace the original with a short overview page that links to the four.

---

## Included blueprints

The skill includes practical blueprints for:

| Blueprint | Use it for |
| --- | --- |
| Tutorial | A guided learning path with visible progress |
| How-to | A focused task or real-world problem |
| Reference | Parameters, fields, commands, flags, values, limits, and schemas |
| Explanation | Concepts, background, design reasons, tradeoffs, and alternatives |
| Quickstart | A short path to first success |
| README | A project entry point and first impression |
| Troubleshooting | Symptoms, causes, solutions, and verification |
| Glossary | Project-specific terms and definitions |
| Release notes | User-facing change summaries |

For larger systems, the skill can also help plan:

- SDK onboarding paths
- API or CLI reference structures
- developer portal navigation
- runnable code example requirements
- documentation versioning and release-note structures
- platform-oriented docs for Markdown, Docusaurus, ReadTheDocs, Mintlify, GitBook, or repository docs

---

## Design principles

- Reader first: write for what the reader is trying to do right now.
- One need per page: avoid mixing learning, working, lookup, and reflection.
- Link, do not overload: move extra explanation or reference into companion docs.
- Structure follows purpose: choose the document type before choosing headings.
- Practical over theoretical: use Diataxis as a working tool, not as decoration.

---

## How this skill differs from generic writing help

A generic writing assistant optimizes for fluent prose. This skill optimizes for **the right kind of document**.

| Generic writing help | Diataxis Docs Skill |
| --- | --- |
| "Here is a well-written docs page." | "Here is the right kind of docs page for this audience." |
| Treats the request as a writing task. | Treats the request as a classification task. |
| Mixes tutorial, how-to, reference, and explanation by default. | Splits, prunes, and rewrites to keep one form per document. |
| Encourages comprehensive coverage. | Encourages focused pages with links to companions. |
| Does not tell the AI what to avoid. | Ships an explicit anti-patterns checklist. |
| Evaluated on prose quality. | Evaluated on classification accuracy and form separation. |

If you only want fluent prose, you do not need this skill. If you want the AI to make the **shape** of the document correct, this skill is for you.

---

## Local development

Contributors can run the same checks the CI workflow runs before pushing:

```bash
python scripts/check_local.py
```

The script validates:

- `evals/evals.json` is valid JSON, has the required top-level fields, and each eval has `id`, `category`, `prompt`, `expected_output`, and `files`.
- All eval IDs are unique and categories are from the known list.
- All internal markdown links point to existing files.
- All required files (skill, references, examples, commands, CI) are present.

CI is defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and runs on every push and pull request to `master`.

---

## Helper for Cursor and Cline users

While this repository is structured specifically as an Opencode skill (using `.opencode/commands/` and Opencode-specific frontmatter), the core guidance in `SKILL.md` can also serve users of other AI coding assistants.

We provide a helper script that extracts the body of `SKILL.md` (stripping the Opencode frontmatter) and writes it to `.cursorrules` and `.clinerules` in the current directory:

```bash
python scripts/export_rules.py
```

This will generate:

- `.cursorrules` (for Cursor)
- `.clinerules` (for Cline / Roo Code)

Note: the script does not overwrite existing files. Diataxis is meant to be used as a guide, not a rigid plan, so feel free to adapt the generated rules file to your team's specific workflow.

---

## FAQ

**Q: Is this skill just a summary of the Diataxis website?**

No. The skill distills Diataxis into a working workflow the AI can apply directly, and adds a Good Docs Project mapping, a per-form blueprint, a per-form anti-pattern checklist, and a structured plan for large systems. It is meant to be loaded by an agent, not read by a human.

**Q: Does the skill replace the human author?**

No. The skill makes the AI make better first-draft decisions about _what kind_ of document to write. A human still owns tone, accuracy, and final structure.

**Q: Can I use this skill without knowing Diataxis?**

Yes. The decision tree, the anti-patterns checklist, and the per-form blueprints are designed to be usable by a reader who has never read the Diataxis source material.

**Q: What languages does the skill support?**

The skill is language-agnostic. The bundled READMEs are bilingual (English and Simplified Chinese); the framework itself is applied to the language the user writes in.

**Q: How is the skill evaluated?**

The repository ships [`evals/evals.json`](evals/evals.json) with 29 sample prompts across 11 categories, including classification, mixed-form detection, per-form writing, review, migration, large-system planning, adjacent types, anti-pattern avoidance, and explicit non-trigger cases. Each eval declares a category and an expected output shape so regressions are easy to spot.

**Q: Will the skill write code examples for me?**

Only as part of a tutorial or reference page. The skill's main job is to choose the right form; the code itself is your responsibility, since only you know the product.

**Q: How do I add a new slash command?**

Add a Markdown file under `.opencode/commands/` with frontmatter that includes `name` and `description`. The body should describe the task, the input, and the expected output shape. Look at `docs-classify.md` or `docs-audit.md` for the smallest good examples.

**Q: How do I add a new eval?**

Add a new object to the `evals` array in `evals/evals.json` with `id`, `category`, `prompt`, `expected_output`, and `files`. The `id` must be unique, and the `category` must be one of the known categories listed in the validation script. Then run `python scripts/check_local.py` to confirm.

---

## Sources

This skill is inspired by and based on ideas from:

- [Diataxis](https://diataxis.fr/)
- [The Good Docs Project](https://www.thegooddocsproject.dev/)

The repository does not mirror those sources. It distills their ideas into a reusable Opencode skill.

---

## Contributing

Issues and pull requests are welcome.

If you want to propose a bigger change, open an issue first so we can keep the skill focused and avoid overfitting it to a single documentation style.

Good contributions usually improve one of these areas:

- clearer trigger wording in `SKILL.md`
- better documentation blueprints
- more realistic eval prompts
- examples of successful documentation transformations
- SDK, API, and developer portal examples
- translations or localization improvements

Please keep the style practical, reader-first, and aligned with Diataxis.

---

## License

MIT. See [LICENSE](LICENSE).
