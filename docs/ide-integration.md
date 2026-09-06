# Export the guidance to other AI assistants

Claude Code, OpenCode, and Codex load this repository as a skill directly — see [Install the skill](installation.md). For every other assistant, [`scripts/export_rules.py`](../scripts/export_rules.py) writes `SKILL.md` to the rule-file path that tool reads, with the frontmatter it needs.

## Before you start

Read [Context cost](#context-cost) first. Six of the eleven default targets load into every request in the project.

## List the targets

```bash
python scripts/export_rules.py --list
```

14 rule-file targets across 11 assistants (11 selected by default):

| Key | Tool | Path | Default | Always-on |
| --- | --- | --- | --- | --- |
| `cursor` | Cursor | `.cursor/rules/diataxis.mdc` | yes | no |
| `cursor-legacy` | Cursor (legacy) | `.cursorrules` | no | yes |
| `cline` | Cline | `.clinerules/diataxis.md` | yes | yes |
| `roo` | Roo Code | `.roo/rules/diataxis.md` | yes | yes |
| `windsurf` | Windsurf | `.windsurf/rules/diataxis.md` | yes | no |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | yes | yes |
| `claude` | Claude Code (skill) | `.claude/skills/diataxis-docs/SKILL.md` | yes | no |
| `claude-md` | Claude Code (CLAUDE.md) | `CLAUDE.md` | no | yes |
| `codex` | OpenAI Codex (skill) | `.agents/skills/diataxis-docs/SKILL.md` | yes | no |
| `codex-md` | OpenAI Codex (AGENTS.md) | `AGENTS.md` | no | yes |
| `aider` | Aider | `CONVENTIONS.md` | yes | yes |
| `gemini` | Gemini CLI | `GEMINI.md` | yes | yes |
| `continue` | Continue | `.continue/rules/diataxis.md` | yes | no |
| `amazonq` | Amazon Q Developer | `.amazonq/rules/diataxis.md` | yes | yes |

Three pairs target the same tool and cannot be selected together: `cursor` with `cursor-legacy`, `claude` with `claude-md`, and `codex` with `codex-md`.

## Preview before writing

`--dry-run` reports what would happen and writes nothing:

```bash
python /path/to/diataxis-docs-skill/scripts/export_rules.py --target . --dry-run
```

## Export

Run from the project that should receive the rule files, or point `--target` at it:

```bash
# Everything, into the current project. Windsurf automatically uses compact
# output when the full guide would exceed its platform limit.
python /path/to/diataxis-docs-skill/scripts/export_rules.py

# Only the tools your team uses, compact form
python /path/to/diataxis-docs-skill/scripts/export_rules.py --only cursor --only copilot --compact
```

Existing files are never overwritten unless you pass `--force`.

## Options

| Option | Effect |
| --- | --- |
| `--target DIR` | Project to export into. Defaults to the current directory. |
| `--only KEY` | Export one target. Repeat for several. |
| `--list` | Print the target table and exit. |
| `--dry-run` | Report planned writes without touching the filesystem. |
| `--force` | Overwrite existing rule files. |
| `--compact` | Export six decision-critical sections instead of the whole guide. |

## Context cost

An always-on rule file is prepended to every request in that project. The full guidance is about 13,900 characters, roughly 3,500 tokens per request. Across the six always-on default targets that is around 21,000 tokens per request if you export the full guide to all of them.

`--compact` exports the compass, the quick decision tree, the four-forms table, the non-trigger list, the anti-patterns, and the quality checks — about 8,400 characters, roughly 2,100 tokens. That is enough for the assistant to classify a request correctly and avoid the common failure modes.

Use the full export for the targets that load conditionally (`cursor`, `windsurf`, `continue`, `claude`, `codex`), and `--compact` for the always-on ones. The exporter prints both numbers after each run.

## Tool-specific notes

**Claude Code.** The default `claude` target writes a native skill to `.claude/skills/diataxis-docs/SKILL.md`, which the host loads only when a request matches the skill description. It costs nothing on unrelated requests, so it is the target to prefer. `claude-md` writes `CLAUDE.md` instead, which is always-on; use it only for a host that reads `CLAUDE.md` but does not support skills, and pair it with `--compact`. If you installed this repository as a skill, you do not need either target.

**Codex.** Same shape as Claude Code. The default `codex` target writes a native skill to `.agents/skills/diataxis-docs/SKILL.md`, the project skill directory Codex discovers, so it loads on demand. `codex-md` writes `AGENTS.md`, which is always-on; it is worth choosing when several agents in the project read `AGENTS.md` and you want one shared file rather than a per-tool rule. Pair it with `--compact`, and delete a stale `AGENTS.md` written by version 0.3.0 or earlier, which exported there by default.

**Cursor.** Project rules must use the `.mdc` extension; a plain `.md` file in `.cursor/rules` is ignored by the rules system. The script writes `.cursor/rules/diataxis.mdc` with `description` and `alwaysApply: false`, which makes it an agent-requested rule: Cursor reads the description and pulls the rule in when the task looks documentation-related. Use `--only cursor-legacy` only for an older Cursor setup, and never select both targets together.

**Cline.** Workspace rules live in the `.clinerules/` directory. The exporter writes `.clinerules/diataxis.md`; a single `.clinerules` file is not the current directory-based format.

**Windsurf.** Workspace rules are capped at 12,000 characters per file. The full guidance exceeds that, so the exporter automatically falls back to the compact guide for this target; pass `--compact` when you want every target to use the same compact source. The legacy `.windsurfrules` target is not offered: its 6,000-character limit is smaller than even the compact guide, so it has no valid export mode. Delete a stale `.windsurfrules` generated by an earlier version.

**Roo Code.** Every file in `.roo/rules/` is loaded on every request, so this target is effectively always-on even though it lives in a rules directory.

**Continue.** The script writes `name`, `description`, and `alwaysApply: false`, which lets the agent decide when to pull the rule in.

**Aider.** Writing `CONVENTIONS.md` is only half the job. Aider does not read it until you add it to `.aider.conf.yml`:

```yaml
read:
  - CONVENTIONS.md
```

## Keep exports out of version control

The exported files are derived from `SKILL.md`. This repository's `.gitignore` excludes every path the exporter can write, so a local export never lands in a commit. In your own project, decide whether to commit them: committing shares the rules with your team, and ignoring them keeps a single source of truth.

## Re-export after an update

```bash
git -C /path/to/diataxis-docs-skill pull
python /path/to/diataxis-docs-skill/scripts/export_rules.py --target . --force
```
