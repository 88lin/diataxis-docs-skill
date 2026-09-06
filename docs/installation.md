# Install the skill

This guide installs the Diataxis Docs Skill into Claude Code or OpenCode and verifies that the host actually loaded it.

## Before you start

You need `git` and one of the following hosts:

- Claude Code
- OpenCode

Both load the same `SKILL.md`, and both ship the same five slash commands in host-specific directories.

## The directory name matters

> **The directory that contains `SKILL.md` must be named `diataxis-docs`.**
>
> Both hosts expect the frontmatter `name` to match the containing directory. This repository is called `diataxis-docs-skill`, but the skill is named `diataxis-docs`. A plain `git clone` keeps the repository name, so the skill will not load. Every command below passes the target directory explicitly for this reason.

## Install into Claude Code

### Install globally

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

### Install for one project

Run this from the project root:

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .claude/skills/diataxis-docs
```

### Install the slash commands

Claude Code discovers commands from `~/.claude/commands/` globally or `.claude/commands/` in a project. It does not scan the `.claude/commands/` directory nested inside an installed skill, so copy the files out:

```bash
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/commands" | Out-Null
Copy-Item "$HOME/.claude/skills/diataxis-docs/.claude/commands/*.md" "$HOME/.claude/commands/"
```

Claude Code usually detects new skills automatically. Restart it if this is your first skill, or if the skill does not appear.

## Install into OpenCode

### Install globally

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

### Install for one project

Run this from the project root:

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .opencode/skills/diataxis-docs
```

OpenCode discovers skills only in its documented project and global skill directories, including the Claude- and agent-compatible ones. It does not support a `skills.paths` setting for arbitrary checkouts. If you keep the repository elsewhere, copy or link it into one of those directories.

Restart OpenCode after either method so the skill list reloads.

### Install the slash commands

OpenCode discovers commands from `.opencode/commands/` in the current project or `~/.config/opencode/commands/` globally, and likewise does not scan the copy nested inside an installed skill.

```bash
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

For a project-local installation:

```bash
mkdir -p .opencode/commands
cp .opencode/skills/diataxis-docs/.opencode/commands/*.md .opencode/commands/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.config/opencode/commands" | Out-Null
Copy-Item "$HOME/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md" "$HOME/.config/opencode/commands/"
```

The installed commands are copies, so repeat the copy after updating the skill. Review an existing `docs-*.md` command before replacing it if you already use the same name.

## Verify the install

Set `SKILL_DIR` to the checkout you installed, then check that the directory name and the frontmatter name agree:

```bash
SKILL_DIR=~/.claude/skills/diataxis-docs
# OpenCode global: SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# Project-local:   SKILL_DIR=.claude/skills/diataxis-docs
basename "$SKILL_DIR"
head -2 "$SKILL_DIR/SKILL.md"
```

The first command must print `diataxis-docs`; the second must print `---` followed by `name: diataxis-docs`. If the two names differ, rename the directory.

Then ask your assistant a question that should trigger the skill:

```text
Classify this docs page and tell me what kind of document it should be.
```

A loaded skill answers with a Diataxis form — tutorial, how-to, reference, or explanation — and says what to exclude from the page. A generic writing answer means the skill did not load.

## Update

```bash
git -C /path/to/diataxis-docs pull
```

Restart the host afterwards. If you copied the slash commands, repeat the copy so their prompts stay in sync.

## Uninstall

```bash
rm -rf /path/to/diataxis-docs
```

If you copied the slash commands, remove the five `docs-*.md` files from the command directory as well, after checking that they are the copies from this skill.

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| The skill never triggers | Directory name is not `diataxis-docs` | Rename the directory, then restart the host |
| The skill never triggers | Host was not restarted | Restart Claude Code or OpenCode |
| `SKILL.md` not found | Cloned one directory too deep | The file must sit at `<skills-dir>/diataxis-docs/SKILL.md` |
| Slash commands are missing | The command directory nested inside a skill checkout is not a discovered command directory | Copy the files into the host's project or global command directory, then restart |
| Slash commands are stale after an update | The installed command files are copies | Repeat the command-copy step after pulling |
| Slash commands are missing in a third host | Command discovery is host-specific | Use natural-language prompts, or adapt the command bodies to that host's format |

## Next steps

- [Slash commands](commands.md) — the five bundled commands and what each returns
- [AI IDE integration](ide-integration.md) — export the guidance to Cursor, Copilot, and others
- [FAQ](faq.md) — scope, evaluation, and how this differs from generic writing help
