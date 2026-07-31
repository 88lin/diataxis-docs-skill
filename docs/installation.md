# Install the skill

This guide installs the Diataxis Docs Skill into OpenCode or Claude Code and verifies that the host tool actually loaded it.

## Before you start

You need `git` and one of the following hosts:

- OpenCode
- Claude Code

## The directory name matters

> **The directory that contains `SKILL.md` must be named `diataxis-docs`.**
>
> OpenCode requires the frontmatter `name` to match the containing directory. This repository is called `diataxis-docs-skill`, but the skill is named `diataxis-docs`. A plain `git clone` keeps the repository name, so OpenCode will not load the skill. Every command below passes the target directory explicitly for this reason.

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

OpenCode discovers skills only in its documented project and global skill directories (including the Claude- and agent-compatible directories). It does not support a `skills.paths` setting for arbitrary checkouts. If you keep the repository elsewhere, copy or link it into one of those discovered directories.

Restart OpenCode after either method so the skill list reloads.

### Install the slash commands

Installing the skill does **not** install its five slash commands. OpenCode discovers commands only from `.opencode/commands/` in the current project or `~/.config/opencode/commands/` globally; it does not scan the `.opencode/commands/` directory nested inside an installed skill.

For the global installation above:

```bash
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

For a project-local installation:

```bash
mkdir -p .opencode/commands
cp .opencode/skills/diataxis-docs/.opencode/commands/*.md \
  .opencode/commands/
```

PowerShell users can install the commands globally with:

```powershell
New-Item -ItemType Directory -Force "$HOME/.config/opencode/commands" | Out-Null
Copy-Item "$HOME/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md" "$HOME/.config/opencode/commands/"
```

These are copies, so repeat the command after updating the skill. Review an existing `docs-*.md` command before replacing it if you already use the same command name.

## Install into Claude Code

Claude Code loads skills from `~/.claude/skills/<name>/` and uses the same `SKILL.md` entry point.

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

Claude Code usually detects new skills automatically. Restart it if this is the first skill you have installed, or if the skill does not appear.

The skill instructions in `SKILL.md` are portable, but slash-command discovery is host-specific. Claude Code does not load the OpenCode commands; see [Slash commands](commands.md).

## Verify the install

Set `SKILL_DIR` to the checkout you installed, then check that the directory name and frontmatter name agree:

```bash
SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# For a project-local install, use: SKILL_DIR=.opencode/skills/diataxis-docs
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

Restart the host tool afterwards. If you copied the OpenCode slash commands, repeat the copy command so their prompts stay in sync.

## Uninstall

```bash
rm -rf /path/to/diataxis-docs
```

If you copied the OpenCode slash commands, remove the five `docs-*.md` files from the command directory as well, after checking that they are the copies from this skill.

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| The skill never triggers | Directory name is not `diataxis-docs` | Rename the directory, then restart the host |
| The skill never triggers | Host was not restarted | Restart OpenCode or Claude Code |
| `SKILL.md` not found | Cloned one directory too deep | The file must sit at `<skills-dir>/diataxis-docs/SKILL.md` |
| Slash commands are missing in OpenCode | The skill checkout's nested `.opencode/commands/` is not a discovered command directory | Copy the files into the project's `.opencode/commands/` or global `~/.config/opencode/commands/`, then restart OpenCode |
| Slash commands are stale after an update | Installed command files are copies | Repeat the command-copy step after pulling the skill update |
| Slash commands are missing in another host | Command discovery is host-specific | Use natural-language prompts, or adapt the command bodies to that host's command format |

## Next steps

- [Slash commands](commands.md) — the five bundled commands and what each returns
- [AI IDE integration](ide-integration.md) — export the guidance to Cursor, Copilot, Claude Code, and others
- [FAQ](faq.md) — scope, evaluation, and how this differs from generic writing help
