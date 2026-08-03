# Slash commands

Reference for the five OpenCode slash commands in [`.opencode/commands/`](../.opencode/commands/). Use them when you want a specific Diataxis mode without relying on natural-language triggering.

The command name comes from the file name, not from the frontmatter. `docs-classify.md` defines `/docs-classify`.

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

The files bundled under this repository's `.opencode/commands/` directory are command sources. Installing the repository as a skill places them inside the skill checkout, but OpenCode only discovers commands from the current project's `.opencode/commands/` or the global `~/.config/opencode/commands/`. Follow [Install the slash commands](installation.md#install-the-slash-commands) to copy them into one of those locations.

## Hosts other than OpenCode

Slash-command discovery is host-specific. Claude Code loads `SKILL.md` but does not read `.opencode/commands/`. In other hosts, either describe the mode in natural language ("classify this page and flag mixed forms") or copy the command body into that host's own command format.

## Add a command

See [Development](development.md#add-a-slash-command).
