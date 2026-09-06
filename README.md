<div align="center">

<img src="assets/cover-en.png" alt="Diataxis Docs Skill — write documentation for readers. Structured. Practical. Reusable." width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Hosts: any agent that reads SKILL.md](https://img.shields.io/badge/Hosts-any%20agent%20that%20reads%20SKILL.md-111827?style=flat-square)](docs/installation.md)
[![Assistants: 12](https://img.shields.io/badge/Assistants-12-0ea5e9?style=flat-square)](docs/ide-integration.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb?style=flat-square)](https://diataxis.fr/)
[![Evals: 35](https://img.shields.io/badge/Evals-35-blueviolet?style=flat-square)](evals/evals.json)

**[中文](README.zh-CN.md)** &nbsp;·&nbsp; [What it does](#what-it-does) &nbsp;·&nbsp; [Install](#install) &nbsp;·&nbsp; [Compatibility](#compatibility) &nbsp;·&nbsp; [Use it](#use-it) &nbsp;·&nbsp; [Docs](#documentation)

</div>

---

## Most docs problems are classification problems

A page that teaches a beginner, guides a working user, lists API fields, and explains design tradeoffs **fails all four readers at once**. The beginner cannot find the lesson. The working user cannot find the steps. The expert cannot find the field they came for. The maintainer does not know where new content belongs.

The prose can be excellent and the page still fails.

This skill makes an AI assistant decide *what kind of document is needed* before it writes anything.

## What it does

**One page in, four documents out.** Give it a page that is trying to do four jobs, and it tells you which four documents that page should have been — then drafts each one.

**Before** — one page, four jobs:

```text
"Getting Started with QuokkaDB"
├── Introduction  ...................... 💡 explanation
├── Why we built QuokkaDB  ............. 💡 explanation
├── Quick install, first connection  ... 🎓 tutorial
│    └─ What just happened  ........... 💡 explanation   ← wrong page
├── Common tasks  ...................... 🔧 how-to
├── Reference  ......................... 📖 reference
├── Troubleshooting  ................... 🔧 how-to
└── Next steps  ........................ ·  a link farm, no form
```

**After** — four single-purpose pages:

```text
🎓  Tutorial     Your first QuokkaDB program
                 What you will build · Prerequisites · Steps · Where to go next

🔧  How-to       Configure a QuokkaDB connection
                 Goal · Steps · Run a transaction · Results

📖  Reference    QuokkaDB Python client
                 Connection options · Functions · Error codes · Limits

💡  Explanation  Why QuokkaDB chose an LSM-tree engine
                 Origin · Why ACID · Why an LSM-tree · Implications
```

That is a real worked example, not an illustration — the before-and-after pages are in [`examples/messy-to-diataxis/`](examples/messy-to-diataxis/).

Critically, it also says **what to leave out of each page**. A tutorial that grows a "Background" section has stopped being a tutorial.

## How it decides

Two questions, four answers. This is the Diataxis compass:

| If the content… | …and serves the user's… | …then it belongs to… |
| :--- | :--- | :--- |
| informs **action** | **acquisition** of skill | 🎓 &nbsp;a **tutorial** |
| informs **action** | **application** of skill | 🔧 &nbsp;a **how-to guide** |
| informs **cognition** | **application** of skill | 📖 &nbsp;**reference** |
| informs **cognition** | **acquisition** of skill | 💡 &nbsp;**explanation** |

And each form has rules the assistant applies while writing:

| Form | Reader is | Must have | Must **not** have |
| :--- | :--- | :--- | :--- |
| 🎓 Tutorial | learning | one linear path, visible results, stated prerequisites | branches, options, background essays |
| 🔧 How-to | working | one goal, short sequence, a verification step | teaching, concept introductions |
| 📖 Reference | looking up | structure mirroring the thing described, exact values | instructions, recommendations, hedging |
| 💡 Explanation | reflecting | one bounded topic, a point of view, tradeoffs | procedures, "how to" framing |

The full decision tree, the per-form anti-patterns, and the quality checks live in [`SKILL.md`](SKILL.md).

## Install

Three ways in, all ending at the same place. Pick whichever fits.

### 🗣️ &nbsp;Ask your agent

*Best for newcomers. No prerequisites.*

Paste this into Claude Code, OpenCode, or Codex:

```text
Install the skill at https://github.com/88lin/diataxis-docs-skill into my global skills directory.
The directory holding SKILL.md must be named diataxis-docs, not the repository name.
Then tell me the path you used.
```

### 📦 &nbsp;`skills` CLI

*Best for several agents at once. Needs Node.js.*

```bash
npx skills add 88lin/diataxis-docs-skill
```

It detects your installed agents and writes to the right directory for each. Non-interactive:

```bash
npx skills add 88lin/diataxis-docs-skill --skill diataxis-docs --agent claude-code -g -y
```

### 🧬 &nbsp;`git clone`

*Best for pinning a checkout. Needs git.*

```bash
# Claude Code
git clone https://github.com/88lin/diataxis-docs-skill ~/.claude/skills/diataxis-docs

# OpenCode
git clone https://github.com/88lin/diataxis-docs-skill ~/.config/opencode/skills/diataxis-docs

# Codex
git clone https://github.com/88lin/diataxis-docs-skill ~/.codex/skills/diataxis-docs
```

> [!IMPORTANT]
> The directory containing `SKILL.md` **must** be named `diataxis-docs` to match the frontmatter `name`. The first two methods handle this; the clone commands pass the target path explicitly for this reason. Restart the host afterwards.

Project-local installs, the optional [slash-command copy step](#commands), verification, and troubleshooting: **[Install the skill](docs/installation.md)**.

## Compatibility

Twelve hosts, two loading mechanisms.

### ⚡ &nbsp;Loads `SKILL.md` natively

**Claude Code** &nbsp;·&nbsp; **OpenCode** &nbsp;·&nbsp; **Codex**

The host reads the frontmatter, loads the body only when a request matches, and stays out of the way otherwise — **zero token cost on unrelated requests**. Nothing to configure: install, restart, done.

### 📄 &nbsp;Reads an exported rule file

Cursor &nbsp;·&nbsp; GitHub Copilot &nbsp;·&nbsp; Cline &nbsp;·&nbsp; Roo Code &nbsp;·&nbsp; Windsurf &nbsp;·&nbsp; Aider &nbsp;·&nbsp; Gemini CLI &nbsp;·&nbsp; Continue &nbsp;·&nbsp; Amazon Q

These read a plain rule file rather than a skill, so export one:

```bash
python scripts/export_rules.py --list
python scripts/export_rules.py --target . --compact
```

`--list` prints all 14 targets. The exporter then writes `SKILL.md` to the path each tool reads, with the frontmatter it needs. Six default targets are always-on context — prepended to *every* request in the project, roughly 3,500 tokens each — which is what `--compact` is for: it exports the six decision-critical sections at about 2,100 tokens instead.

Full target list and per-tool notes: **[AI IDE integration](docs/ide-integration.md)**.

## Use it

Ask in natural language. No command needed:

```text
Turn this messy guide into Diataxis-style docs.
Split this page into tutorial, how-to, reference, and explanation.
Design a Diataxis documentation system for my SDK.
Audit our docs site and flag pages that mix forms.
```

### Commands

Five optional shortcuts, for Claude Code and OpenCode. Each drops you into one mode directly instead of relying on natural-language triggering.

| Command | Input | Returns |
| :--- | :--- | :--- |
| `/docs-classify` | a page or paste | which form it belongs to, plus mixed-form signals |
| `/docs-split` | a mixed-form page | a split plan and a draft of each resulting page |
| `/docs-review` | a draft | severity-tagged pre-publication findings |
| `/docs-audit` | a docs directory or page list | page-by-page classification and a triage list |
| `/docs-quickstart` | a product or tool description | a short path to first success |

Every command substitutes `$ARGUMENTS` with whatever you typed after the name. Full output shapes: **[Slash commands](docs/commands.md)**.

> [!NOTE]
> **Commands are optional — and if you want them, they need one copy step.**
> The skill works through natural language without them. Neither Claude Code nor OpenCode discovers a command directory nested *inside* an installed skill, so copy them into the host's own command directory once:

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md ~/.config/opencode/commands/
```

Codex has no bundled commands — describe the mode in natural language instead, e.g. *"classify this page and flag mixed forms"*.

PowerShell variants, project-local paths, and what to do after an update: **[Install the slash commands](docs/installation.md#install-the-slash-commands)**.

## Also bundled

- **A mixed-form scanner.** `python scripts/audit_docs.py docs/` scores each page on code blocks, table rows, step lines, and explanation vocabulary, then flags the ones worth a human look. Triage for a large site before you spend model tokens on it.
- **Reference material loaded on demand**, never on every request: [blueprints](references/doc-blueprints.md) per document type, a [reader checklist](references/reader-analysis.md), a [template map](references/template-map.md) to Good Docs Project templates, and [Chinese-language anti-patterns](references/zh-cn-anti-patterns.md).
- **35 evals** across 13 categories in [`evals/evals.json`](evals/evals.json), including deliberate non-trigger cases — the skill is meant to stay quiet on requests that are not about document structure.

## Documentation

| Page | For |
| :--- | :--- |
| **[Install the skill](docs/installation.md)** | Three install methods, per-host paths, verification |
| **[Slash commands](docs/commands.md)** | What each command takes and returns |
| **[AI IDE integration](docs/ide-integration.md)** | Exporting to Cursor, Copilot, Aider, and others |
| **[Develop and contribute](docs/development.md)** | Running the checks, adding evals and commands |
| **[Scope and design FAQ](docs/faq.md)** | What it does not do, and why |

## Design principles

- **Reader first.** Write for what the reader is trying to do right now.
- **One need per page.** Do not mix learning, working, lookup, and reflection.
- **Link, do not overload.** Companion documents beat a longer page.
- **Structure follows purpose.** Choose the document type before the headings.
- **A guide, not a plan.** Apply the compass where you are, one step at a time.

## Contributing

Issues and pull requests are welcome. Open an issue first for anything larger than a fix.

```bash
python scripts/check_local.py
```

CI runs this exact command. See [CONTRIBUTING.md](CONTRIBUTING.md) and [Develop and contribute](docs/development.md).

## Sources

Built on ideas from **[Diataxis](https://diataxis.fr/)** and **[The Good Docs Project](https://www.thegooddocsproject.dev/)**. This repository mirrors neither; it distills them into a skill.

<div align="center">

<br>

**MIT licensed** — see [LICENSE](LICENSE)

</div>
