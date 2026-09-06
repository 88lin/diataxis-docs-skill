# Slash commands

Reference for the five slash commands. Use them when you want a specific Diataxis mode without relying on natural-language triggering.

The commands are optional. The skill works through natural language in any host that loads it; these are a shortcut into one mode.

Each command ships twice, once per host that supports command discovery, with the same body and host-specific frontmatter:

- Claude Code: [`.claude/commands/`](../.claude/commands/)
- OpenCode: [`.opencode/commands/`](../.opencode/commands/)

The command name comes from the file name in both hosts, not from the frontmatter. `docs-classify.md` defines `/docs-classify`.

Codex loads the skill but has no bundled commands here — see [Other hosts](#other-hosts).

## Summary

| Command | Input | Returns |
| --- | --- | --- |
| `/docs-classify` | One page or paste | The Diataxis form it belongs to, plus mixed-form signals |
| `/docs-split` | One mixed-form page | A split plan and a draft of each resulting page |
| `/docs-review` | A draft | Severity-tagged pre-publication findings |
| `/docs-audit` | A docs directory or page list | Page-by-page classification and a triage list |
| `/docs-quickstart` | A product or tool description | A short path to first success |

## `/docs-classify`

Classify a single documentation page.

Output sections: Classification, Section-by-section tags, Mixed-form signals, Recommended split (if any), Reasoning.

```text
/docs-classify docs/getting-started.md
```

## `/docs-split`

Split a page that mixes forms into the documents it should have been.

Output sections: Diagnosis, Split plan, Drafts, Original page replacement.

The Drafts section contains a full draft of every page in the split plan, so this command produces the longest output of the five.

```text
/docs-split docs/getting-started.md
```

## `/docs-review`

Review a draft before publication.

Output sections: Review summary, Findings, Mixed-form signals, Suggested edits. Findings carry a severity so you can decide what blocks publication.

```text
/docs-review docs/api/webhooks.md
```

## `/docs-audit`

Audit a whole docs directory or a list of pages.

Output sections: Audit summary, Per-page findings, Pages that need a split, Pages that need a small fix, Clean pages.

```text
/docs-audit docs/
```

For a mechanical pre-pass over a large site, run [`scripts/audit_docs.py`](../scripts/audit_docs.py) first and feed the flagged pages to this command. See [Development](development.md#scan-docs-for-mixed-form-smells).

## `/docs-quickstart`

Draft a quickstart, which is a tutorial optimized for first success rather than completeness.

Output sections: What you will build, Prerequisites, Steps, Next steps.

```text
/docs-quickstart our CLI for provisioning staging databases
```

## Arguments

Every command body substitutes `$ARGUMENTS` with everything you typed after the command name. Pass a path, a list of paths, or pasted page content.

## Make the commands discoverable

The bundled command directories are sources. Installing the repository as a skill places them inside the skill checkout, and neither host discovers commands nested in a skill: Claude Code reads `~/.claude/commands/` or a project's `.claude/commands/`, and OpenCode reads `~/.config/opencode/commands/` or a project's `.opencode/commands/`. Follow [Install the skill](installation.md#install-the-slash-commands) to copy them into one of those locations.

## Frontmatter per host

The bodies are identical; only the frontmatter differs, because each host recognises its own fields and silently ignores the rest.

| Host | Fields used here | Also recognised |
| --- | --- | --- |
| Claude Code | `description`, `argument-hint` | `model`, `allowed-tools`, `disable-model-invocation` |
| OpenCode | `description` | `agent`, `model`, `variant`, `subtask` |

`check_local.py` enforces that both directories contain the same five commands and warns when a field belongs to the other host.

## Other hosts

Slash-command discovery is host-specific, and this repository ships commands only for the two hosts above. Codex loads `SKILL.md` the same way they do, but its prompt format is not covered here.

In Codex or any other host, either describe the mode in natural language — "classify this page and flag mixed forms", "audit docs/ and tell me which pages mix forms" — or copy a command body into that host's own command format. The bodies are plain Markdown prompts with a `$ARGUMENTS` placeholder, so adapting one is mostly a matter of matching the frontmatter and the substitution syntax.

## Add a command

See [Development](development.md#add-a-slash-command).
