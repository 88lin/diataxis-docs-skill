<div align="center">

<img src="assets/cover-en.png" alt="Diataxis Docs Skill — write documentation for readers. Structured. Practical. Reusable." width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Hosts: Claude Code and OpenCode](https://img.shields.io/badge/Hosts-Claude%20Code%20%7C%20OpenCode-111827?style=flat-square)](docs/installation.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb?style=flat-square)](https://diataxis.fr/)
[![Templates: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a?style=flat-square)](https://www.thegooddocsproject.dev/)
[![Evals: 35](https://img.shields.io/badge/Evals-35-blueviolet?style=flat-square)](evals/evals.json)

**[中文](README.zh-CN.md)** &nbsp;·&nbsp; [Install](docs/installation.md) &nbsp;·&nbsp; [Commands](docs/commands.md) &nbsp;·&nbsp; [IDE integration](docs/ide-integration.md) &nbsp;·&nbsp; [FAQ](docs/faq.md)

</div>

---

## Why this exists

Most documentation problems are classification problems, not writing problems.

A page that teaches a beginner, guides a working user, lists API fields, and explains design tradeoffs **fails all four readers at once**. The prose can be excellent and the page still fails.

This skill makes an AI assistant decide *what kind of document is needed* before it writes anything.

<table>
<tr><th align="left">If the content…</th><th align="left">…and serves the user's…</th><th align="left">…then it belongs to…</th></tr>
<tr><td>informs <b>action</b></td><td><b>acquisition</b> of skill</td><td>🎓 &nbsp;a <b>tutorial</b></td></tr>
<tr><td>informs <b>action</b></td><td><b>application</b> of skill</td><td>🔧 &nbsp;a <b>how-to guide</b></td></tr>
<tr><td>informs <b>cognition</b></td><td><b>application</b> of skill</td><td>📖 &nbsp;<b>reference</b></td></tr>
<tr><td>informs <b>cognition</b></td><td><b>acquisition</b> of skill</td><td>💡 &nbsp;<b>explanation</b></td></tr>
</table>

The skill then writes in that form — and says what to leave out. [`SKILL.md`](SKILL.md) holds the decision tree, the per-form anti-patterns, and the quality checks.

## Install

<table>
<tr><td width="50%" valign="top">

**Claude Code**

```bash
git clone \
  https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

</td><td width="50%" valign="top">

**OpenCode**

```bash
git clone \
  https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

</td></tr>
</table>

> [!IMPORTANT]
> The directory containing `SKILL.md` **must** be named `diataxis-docs` to match the frontmatter `name` — which is why both commands pass the target path explicitly. Restart the host afterwards.

Project-local installs, the slash-command copy step, verification, and troubleshooting: **[Install the skill](docs/installation.md)**.

## Use it

Ask in natural language:

```text
Turn this messy guide into Diataxis-style docs.
Split this page into tutorial, how-to, reference, and explanation.
Design a Diataxis documentation system for my SDK.
Audit our docs site and flag pages that mix forms.
```

Or run a slash command for a specific mode:

| Command | Returns |
| :--- | :--- |
| `/docs-classify` | Which form a page belongs to, plus mixed-form signals |
| `/docs-split` | A split plan and a draft of each resulting page |
| `/docs-review` | Severity-tagged pre-publication findings |
| `/docs-audit` | Page-by-page classification of a docs directory |
| `/docs-quickstart` | A short path to first success |

Full output shapes: **[Slash commands](docs/commands.md)**.

<details>
<summary><b>Both hosts ship all five commands — but they need one copy step</b></summary>

<br>

The commands live in `.claude/commands/` and `.opencode/commands/`. Neither host discovers a command directory nested *inside* an installed skill, so copy them into the host's own command directory once:

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md ~/.config/opencode/commands/
```

Full steps, PowerShell variants, and project-local paths: [Install the skill](docs/installation.md).

</details>

## See it work

[`examples/messy-to-diataxis/`](examples/messy-to-diataxis/) holds a realistic "Getting Started" page doing four jobs at once, beside the four single-purpose pages it should become.

```text
BEFORE   before.md                  1 page, 4 jobs
           │
           ├──▶  after/01-tutorial.md      🎓  learn by doing
AFTER      ├──▶  after/02-how-to.md        🔧  complete a task
           ├──▶  after/03-reference.md     📖  look up facts
           └──▶  after/04-explanation.md   💡  understand why
```

## Documentation

| Page | For |
| :--- | :--- |
| **[Install the skill](docs/installation.md)** | Getting it loaded in Claude Code or OpenCode |
| **[Slash commands](docs/commands.md)** | What each command takes and returns |
| **[AI IDE integration](docs/ide-integration.md)** | Exporting to Cursor, Copilot, Aider, and other assistants |
| **[Develop and contribute](docs/development.md)** | Running the checks, adding evals and commands |
| **[Scope and design FAQ](docs/faq.md)** | What it does not do, and why |

Reference material the skill loads **on demand**, not on every request:

[Blueprints](references/doc-blueprints.md) per document type &nbsp;·&nbsp; a [reader checklist](references/reader-analysis.md) &nbsp;·&nbsp; a [template map](references/template-map.md) to Good Docs Project templates &nbsp;·&nbsp; [Chinese-language anti-patterns](references/zh-cn-anti-patterns.md)

## Use it in other assistants

`SKILL.md` is portable. The exporter writes it to the rule file each assistant reads, with the frontmatter that tool needs:

```bash
python scripts/export_rules.py --list           # see all targets
python scripts/export_rules.py --target . --compact
```

Seven of the eleven default targets load into **every** request in the project, so `--compact` matters there — it exports the six decision-critical sections instead of the whole guide. See **[AI IDE integration](docs/ide-integration.md)**.

## Design principles

- **Reader first.** Write for what the reader is trying to do right now.
- **One need per page.** Do not mix learning, working, lookup, and reflection.
- **Link, do not overload.** Companion documents beat a longer page.
- **Structure follows purpose.** Choose the document type before the headings.
- **A guide, not a plan.** Apply the compass where you are, one step at a time.

## Contributing

Issues and pull requests are welcome. Open an issue first for anything larger than a fix.

```bash
python scripts/check_local.py    # CI runs this exact command
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [Develop and contribute](docs/development.md).

## Sources

Built on ideas from **[Diataxis](https://diataxis.fr/)** and **[The Good Docs Project](https://www.thegooddocsproject.dev/)**. This repository mirrors neither; it distills them into a skill.

<div align="center">

<br>

**MIT licensed** — see [LICENSE](LICENSE)

</div>
