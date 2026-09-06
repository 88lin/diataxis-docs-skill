# Install the skill

This guide installs the Diataxis Docs Skill into an agent that reads `SKILL.md`, and verifies that the host actually loaded it.

Three methods, in order of how little you need to know:

| Method | Best for | Needs |
| --- | --- | --- |
| [Ask your agent](#method-1-ask-your-agent) | Anyone, including a first skill | Nothing but the agent you already use |
| [`skills` CLI](#method-2-the-skills-cli) | Installing into several agents at once | Node.js |
| [`git clone`](#method-3-git-clone) | Pinning a checkout you update yourself | `git` |

## Supported hosts

`SKILL.md` is the portable part. Any agent that discovers skills can load it.

| Host | Global skill directory | Project skill directory | Slash commands |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Bundled, [one copy step](#install-the-slash-commands) |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` or `.agents/skills/` | Bundled, [one copy step](#install-the-slash-commands) |
| Codex | `~/.codex/skills/` | `.agents/skills/` | Not bundled — use natural language |

Anything else — Cursor, Copilot, Cline, Windsurf, Aider, Gemini CLI, Amazon Q, Continue, Roo Code — reads a rule file rather than a skill. Export to it instead: see [AI IDE integration](ide-integration.md).

## The directory name matters

> **The directory that contains `SKILL.md` must be named `diataxis-docs`.**
>
> Hosts expect the frontmatter `name` to match the containing directory. This repository is called `diataxis-docs-skill`, but the skill is named `diataxis-docs`. A plain `git clone` keeps the repository name, so the skill will not load.
>
> Methods 1 and 2 handle this for you. Method 3 passes the target directory explicitly for this reason.

## Method 1: ask your agent

Paste this into Claude Code, OpenCode, or Codex. No prerequisites beyond the agent itself.

```text
Install the skill at https://github.com/88lin/diataxis-docs-skill into my
global skills directory. The directory holding SKILL.md must be named
diataxis-docs, not the repository name. Then tell me the path you used.
```

The agent picks the right directory for the host it is running in. When it reports a path, [verify the install](#verify-the-install).

If your agent cannot run shell commands, use one of the other methods.

## Method 2: the `skills` CLI

[`skills`](https://github.com/vercel-labs/skills) is a package manager for agent skills. It detects which agents you have installed and writes to the correct directory for each.

```bash
npx skills add 88lin/diataxis-docs-skill
```

It prompts for the skill and the agents, then installs. To skip the prompts:

```bash
# Global, one named agent
npx skills add 88lin/diataxis-docs-skill --skill diataxis-docs --agent claude-code -g -y

# Project-local, several agents at once
npx skills add 88lin/diataxis-docs-skill --skill diataxis-docs \
  --agent claude-code --agent codex --agent opencode -y
```

Useful flags:

| Flag | Effect |
| --- | --- |
| `-g`, `--global` | Install to the global directory instead of the project |
| `-a`, `--agent` | Target one agent. Repeatable. `claude-code`, `codex`, `opencode`, and others |
| `-s`, `--skill` | Install one skill by name. This repository ships `diataxis-docs` |
| `-l`, `--list` | Show what the repository contains, install nothing |
| `--copy` | Copy the files instead of symlinking them |
| `-y`, `--yes` | Accept the defaults |

Installs are symlinks to one canonical copy by default, so `npx skills update diataxis-docs` updates every agent at once. Pass `--copy` where symlinks are awkward, such as Windows without Developer Mode.

To remove it: `npx skills remove diataxis-docs`.

## Method 3: `git clone`

Clone straight into the host's skill directory, passing `diataxis-docs` as the target name.

**Claude Code**

```bash
# Global
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs

# One project, run from the project root
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .claude/skills/diataxis-docs
```

**OpenCode**

```bash
# Global
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs

# One project, run from the project root
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .opencode/skills/diataxis-docs
```

OpenCode discovers skills only in its documented project and global skill directories, including the Claude- and agent-compatible ones. It does not support a `skills.paths` setting for arbitrary checkouts. If you keep the repository elsewhere, copy or link it into one of those directories.

**Codex**

```bash
# Global
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.codex/skills/diataxis-docs

# One project, run from the project root
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .agents/skills/diataxis-docs
```

Codex resolves the global directory from `$CODEX_HOME/skills`, falling back to `~/.codex/skills` when `CODEX_HOME` is unset.

Restart the host after any of these so the skill list reloads. Claude Code usually detects new skills automatically, but restart it if this is your first skill or the skill does not appear.

## Install the slash commands

The five commands are optional. The skill works through natural language without them; they exist to enter a specific mode directly.

Claude Code and OpenCode both discover commands from their own command directories, and neither scans a command directory nested *inside* an installed skill. So copy the files out once:

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

For a project-local installation, drop the `~/` prefixes:

```bash
mkdir -p .claude/commands
cp .claude/skills/diataxis-docs/.claude/commands/*.md .claude/commands/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/commands" | Out-Null
Copy-Item "$HOME/.claude/skills/diataxis-docs/.claude/commands/*.md" "$HOME/.claude/commands/"
```

Adjust the source path if you installed with the `skills` CLI — `npx skills list` prints where each skill landed.

The installed commands are copies, so repeat the copy after updating the skill. Review an existing `docs-*.md` command before replacing it if you already use the same name.

Codex has no bundled commands. Describe the mode in natural language instead: "classify this page and flag mixed forms".

## Verify the install

Set `SKILL_DIR` to the directory you installed into, then check that the directory name and the frontmatter name agree:

```bash
SKILL_DIR=~/.claude/skills/diataxis-docs
# OpenCode global: SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# Codex global:    SKILL_DIR=~/.codex/skills/diataxis-docs
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
npx skills update diataxis-docs      # skills CLI
git -C /path/to/diataxis-docs pull   # git clone
```

Restart the host afterwards. If you copied the slash commands, repeat the copy so their prompts stay in sync.

## Uninstall

```bash
npx skills remove diataxis-docs      # skills CLI
rm -rf /path/to/diataxis-docs        # git clone
```

If you copied the slash commands, remove the five `docs-*.md` files from the command directory as well, after checking that they are the copies from this skill.

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| The skill never triggers | Directory name is not `diataxis-docs` | Rename the directory, then restart the host |
| The skill never triggers | Host was not restarted | Restart the host |
| `SKILL.md` not found | Cloned one directory too deep | The file must sit at `<skills-dir>/diataxis-docs/SKILL.md` |
| `npx skills` picked the wrong agent | Auto-detection found several | Name it: `--agent claude-code` |
| The symlink is broken or ignored | The filesystem or host does not follow symlinks | Reinstall with `--copy` |
| Slash commands are missing | The command directory nested inside a skill checkout is not a discovered command directory | Copy the files into the host's project or global command directory, then restart |
| Slash commands are stale after an update | The installed command files are copies | Repeat the command-copy step after updating |
| Slash commands are missing in Codex or another host | Command discovery is host-specific | Use natural-language prompts, or adapt the command bodies to that host's format |

## Next steps

- [Slash commands](commands.md) — the five bundled commands and what each returns
- [AI IDE integration](ide-integration.md) — export the guidance to Cursor, Copilot, and others
- [FAQ](faq.md) — scope, evaluation, and how this differs from generic writing help
