# Install the skill

This guide installs the Diataxis Docs Skill into OpenCode or Claude Code and verifies that the host tool actually loaded it.

## Before you start

You need `git` and one of the following hosts:

- OpenCode
- Claude Code

## The directory name matters

> **The directory that contains `SKILL.md` must be named `diataxis-docs`.**
>
> OpenCode requires the frontmatter `name` to match the containing directory. This repository is called `diataxis-docs-skill`, but the skill is named `diataxis-docs`. A plain `git clone` keeps the repository name, so the skill will not load — and neither OpenCode nor Claude Code prints an error when this happens. Every command below passes the target directory explicitly for this reason.

## Install into OpenCode

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

Restart OpenCode so the skill list reloads.

## Install into Claude Code

Claude Code loads skills from `~/.claude/skills/<name>/` and uses the same `SKILL.md` entry point.

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

Claude Code usually detects new skills automatically. Restart it if this is the first skill you have installed, or if the skill does not appear.

The `.opencode/commands/` directory in this repository holds OpenCode slash-command prompts. The skill instructions in `SKILL.md` are portable, but slash-command discovery is host-specific — see [Slash commands](commands.md).

## Verify the install

Check that the directory name and the frontmatter name agree:

```bash
ls -d ~/.config/opencode/skills/diataxis-docs
head -2 ~/.config/opencode/skills/diataxis-docs/SKILL.md
```

The second command must print `---` followed by `name: diataxis-docs`. If the directory name differs from that value, rename the directory.

Then ask your assistant a question that should trigger the skill:

```text
Classify this docs page and tell me what kind of document it should be.
```

A loaded skill answers with a Diataxis form — tutorial, how-to, reference, or explanation — and says what to exclude from the page. A generic writing answer means the skill did not load.

## Update

```bash
git -C ~/.config/opencode/skills/diataxis-docs pull
```

Restart the host tool afterwards.

## Uninstall

```bash
rm -rf ~/.config/opencode/skills/diataxis-docs
```

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| The skill never triggers | Directory name is not `diataxis-docs` | Rename the directory, then restart the host |
| The skill never triggers | Host was not restarted | Restart OpenCode or Claude Code |
| `SKILL.md` not found | Cloned one directory too deep | The file must sit at `<skills-dir>/diataxis-docs/SKILL.md` |
| Slash commands are missing | Host does not read `.opencode/commands/` | Use natural-language prompts, or copy the command bodies into your host's own command format |

## Next steps

- [Slash commands](commands.md) — the five bundled commands and what each returns
- [AI IDE integration](ide-integration.md) — export the guidance to Cursor, Copilot, Claude Code, and others
- [FAQ](faq.md) — scope, evaluation, and how this differs from generic writing help
