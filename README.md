<div align="center">

# Diataxis Docs Skill 📚

**A reusable Opencode skill for writing structured, user-first technical documentation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill: Opencode](https://img.shields.io/badge/Skill-Opencode-111827)](SKILL.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb)](https://diataxis.fr/)
[![Docs: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a)](https://www.thegooddocsproject.dev/)
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
- [How it works](#how-it-works)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Example prompts](#example-prompts)
- [Included blueprints](#included-blueprints)
- [Design principles](#design-principles)
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

---

## How it works

The skill starts with two questions:

1. Is the content about action or cognition?
2. Is the reader acquiring skill or applying skill?

That produces four documentation forms:

| Reader need | Diataxis form | Typical question | Best format |
| --- | --- | --- | --- |
| Learn through action | Tutorial | "Can you teach me?" | A guided lesson |
| Complete a task | How-to guide | "How do I do this?" | A practical sequence |
| Look up exact facts | Reference | "What does this mean?" | Tables, lists, schemas |
| Build understanding | Explanation | "Why does this work this way?" | Contextual discussion |

The skill then applies reusable writing rules and document blueprints so the output stays focused.

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
└── evals/
    └── evals.json
```

### Key files

| File | Purpose |
| --- | --- |
| `SKILL.md` | Main skill instructions, trigger guidance, classification logic, and quality checks |
| `references/reader-analysis.md` | Reader-first checklist before drafting documentation |
| `references/doc-blueprints.md` | Reusable structures for common documentation types |
| `references/template-map.md` | Mapping between Diataxis forms and Good Docs Project templates |
| `evals/evals.json` | Sample prompts for checking whether the skill behaves as expected |
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
Design a Diataxis documentation system for my SDK or API.
```

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
