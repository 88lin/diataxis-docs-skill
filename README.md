<div align="center">

<img src="assets/cover-en.png" alt="Diataxis Docs Skill — write documentation for readers. Structured. Practical. Reusable." width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Hosts: any agent that reads SKILL.md](https://img.shields.io/badge/Hosts-any%20agent%20that%20reads%20SKILL.md-111827?style=flat-square)](docs/installation.md)
[![Assistants: 12](https://img.shields.io/badge/Assistants-12-0ea5e9?style=flat-square)](docs/ide-integration.md)
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

Pick whichever row describes you. All three end at the same place.

<table>
<tr>
<td width="33%" valign="top">

### 🗣️ &nbsp;Ask your agent

*Best for newcomers. No prerequisites.*

Paste this into Claude Code, OpenCode, or Codex:

```text
Install the skill at
https://github.com/88lin/diataxis-docs-skill
into my global skills directory.
The directory holding SKILL.md must
be named diataxis-docs, not the
repository name. Then tell me the
path you used.
```

</td>
<td width="33%" valign="top">

### 📦 &nbsp;`skills` CLI

*Best for several agents at once. Needs Node.js.*

```bash
npx skills add \
  88lin/diataxis-docs-skill
```

It detects your installed agents and writes to the right directory for each. Non-interactive:

```bash
npx skills add \
  88lin/diataxis-docs-skill \
  --skill diataxis-docs \
  --agent claude-code -g -y
```

</td>
<td width="33%" valign="top">

### 🧬 &nbsp;`git clone`

*Best for pinning a checkout. Needs git.*

```bash
U=88lin/diataxis-docs-skill

# Claude Code
git clone https://github.com/$U \
  ~/.claude/skills/diataxis-docs

# OpenCode
git clone https://github.com/$U \
  ~/.config/opencode/skills/diataxis-docs

# Codex
git clone https://github.com/$U \
  ~/.codex/skills/diataxis-docs
```

</td>
</tr>
</table>

> [!IMPORTANT]
> The directory containing `SKILL.md` **must** be named `diataxis-docs` to match the frontmatter `name`. The first two methods handle this; the clone commands pass the target path explicitly for this reason. Restart the host afterwards.

Project-local installs, the optional slash-command copy step, verification, and troubleshooting: **[Install the skill](docs/installation.md)**.

## Which assistants can use it

<table>
<tr><th align="left" width="34%">Loads <code>SKILL.md</code> natively</th><th align="left" width="66%">Reads an exported rule file</th></tr>
<tr valign="top"><td>

**Claude Code**<br>
**OpenCode**<br>
**Codex**

On-demand: costs nothing on unrelated requests.

</td><td>

Cursor &nbsp;·&nbsp; GitHub Copilot &nbsp;·&nbsp; Cline &nbsp;·&nbsp; Roo Code &nbsp;·&nbsp; Windsurf &nbsp;·&nbsp; Aider &nbsp;·&nbsp; Gemini CLI &nbsp;·&nbsp; Continue &nbsp;·&nbsp; Amazon Q

```bash
python scripts/export_rules.py --list
python scripts/export_rules.py --target . --compact
```

The exporter writes `SKILL.md` to the path each tool reads, with the frontmatter it needs. Six default targets are always-on context, which is what `--compact` is for.

</td></tr>
</table>

Full target table and per-tool notes: **[AI IDE integration](docs/ide-integration.md)**.

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
<summary><b>The commands are optional, and need one copy step</b></summary>

<br>

The skill works through natural language without them. If you want them, note that neither Claude Code nor OpenCode discovers a command directory nested *inside* an installed skill, so copy them into the host's own command directory once:

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md ~/.config/opencode/commands/
```

Codex has no bundled commands — describe the mode in natural language instead.

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
| **[Install the skill](docs/installation.md)** | Three install methods, per-host paths, verification |
| **[Slash commands](docs/commands.md)** | What each command takes and returns |
| **[AI IDE integration](docs/ide-integration.md)** | Exporting to Cursor, Copilot, Aider, and other assistants |
| **[Develop and contribute](docs/development.md)** | Running the checks, adding evals and commands |
| **[Scope and design FAQ](docs/faq.md)** | What it does not do, and why |

Reference material the skill loads **on demand**, not on every request:

[Blueprints](references/doc-blueprints.md) per document type &nbsp;·&nbsp; a [reader checklist](references/reader-analysis.md) &nbsp;·&nbsp; a [template map](references/template-map.md) to Good Docs Project templates &nbsp;·&nbsp; [Chinese-language anti-patterns](references/zh-cn-anti-patterns.md)

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
