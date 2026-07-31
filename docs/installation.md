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

### Use OpenCode's discovered skill directory

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

### Register a checkout elsewhere

Clone the repository into a directory whose name still matches the skill:

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/src/diataxis-docs
```

Add that directory to the `opencode.json` that applies to your project:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/src/diataxis-docs"]
  }
}
```

`skills.paths` is a supported OpenCode setting for additional directories to scan for skills. Use it when you want to keep the checkout outside a built-in skill directory; it does not remove the directory-name requirement.

Restart OpenCode after either method so the skill list reloads.

## Install into Claude Code

Claude Code loads skills from `~/.claude/skills/<name>/` and uses the same `SKILL.md` entry point.

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

Claude Code usually detects new skills automatically. Restart it if this is the first skill you have installed, or if the skill does not appear.

The `.opencode/commands/` directory in this repository holds OpenCode slash-command prompts. The skill instructions in `SKILL.md` are portable, but slash-command discovery is host-specific — see [Slash commands](commands.md).

## Verify the install

Set `SKILL_DIR` to the checkout you installed, then check that the directory name and frontmatter name agree:

```bash
SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# For the skills.paths example above, use: SKILL_DIR=~/src/diataxis-docs
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

Restart the host tool afterwards.

## Uninstall

```bash
rm -rf /path/to/diataxis-docs
```

If you installed through `skills.paths`, also remove that entry from `opencode.json`.

## Troubleshoot

| Symptom | Cause | Fix |
| --- | --- | --- |
| The skill never triggers | Directory name is not `diataxis-docs` | Rename the directory, then restart the host |
| The skill never triggers | `skills.paths` points at the wrong or missing directory | Point it at the `diataxis-docs` checkout directory that directly contains `SKILL.md`, then restart OpenCode |
| The skill never triggers | Host was not restarted | Restart OpenCode or Claude Code |
| `SKILL.md` not found | Cloned one directory too deep | The file must sit at `<skills-dir>/diataxis-docs/SKILL.md` |
| Slash commands are missing | Host does not read `.opencode/commands/` | Use natural-language prompts, or copy the command bodies into your host's own command format |

## Next steps

- [Slash commands](commands.md) — the five bundled commands and what each returns
- [AI IDE integration](ide-integration.md) — export the guidance to Cursor, Copilot, Claude Code, and others
- [FAQ](faq.md) — scope, evaluation, and how this differs from generic writing help
