# Contributing

Thanks for your interest in improving the Diataxis Docs Skill.

## Good contributions

Useful contributions usually do one of these:

- improve the skill trigger wording or frontmatter
- add a better documentation blueprint in `references/`
- make the README clearer or more beautiful (in both English and Chinese)
- add more realistic eval prompts, including negative (`non-trigger`) cases
- improve bilingual wording
- add a new example for API, SDK, or developer portal documentation
- add or refine a slash command (in both `.claude/commands/` and `.opencode/commands/`)

## Before you open a pull request

1. Keep the change focused. One PR, one concern.
2. Preserve the Diataxis separation between tutorial, how-to, reference, and explanation.
3. Avoid adding generic writing advice that does not help the skill make a better documentation decision.
4. Update the README (and `README.zh-CN.md`) if the user-facing behavior changes.
5. Run `python scripts/check_local.py` and make sure it passes (see below).
6. If you touched an example, check that the internal links between `before.md` and `after/*.md` still resolve.

## Local validation

Before pushing, always run:

```bash
python scripts/check_local.py
```

It is the single source of truth for repository validation; CI runs this exact command. The full list of checks is in [Develop and contribute](docs/development.md#run-the-checks). The ones most likely to catch a contribution:

- **Slash-command parity** — both host directories ship the same five commands, each with a `description`, a `$ARGUMENTS` placeholder, and frontmatter fields that host actually recognises.
- **Export contract** — every section `export_rules.py --compact` selects still exists as an H2 heading in `SKILL.md`. Renaming a heading breaks the compact export for every always-on target.
- **evals.json** — required fields, unique ids, whitelisted categories, referenced files exist, and prompts are non-trivial.
- **Internal links** — every relative link and heading anchor resolves, and no file contains hidden zero-width characters.
- **Version consistency** — `SKILL.md`, `evals/evals.json`, and `CHANGELOG.md` agree.

A passing local run is the fastest way to keep CI green.

## Adding or editing an eval

`evals/evals.json` is the test suite. Every entry is a contract about how the skill should behave on a specific prompt.

### Required fields

Each eval must include:

| Field | Purpose |
| --- | --- |
| `id` | Stable integer identifier. Must be unique. |
| `category` | One of the categories below. |
| `prompt` | The user-style request the skill should respond to. |
| `expected_output` | What a correct response looks like. Used for human review or an automated grader. |
| `files` | The references inside this repo that back the expected output. Use `[]` only for `non-trigger` evals where the skill should refuse to engage. |

### Category whitelist

`category` must be one of:

- `classification`
- `per-form-writing`
- `decision-framework`
- `single-page-classification`
- `mixed-form-detection`
- `review`
- `large-system`
- `migration`
- `adjacent-types`
- `anti-pattern-avoidance`
- `tool-use`
- `localization`
- `non-trigger`

`non-trigger` is the only **negative** category. Its `expected_output` should describe how the skill declines, refuses, or stays silent. The skill must not read any reference files for these evals, which is why `files` is `[]`.

### Filling in `files`

`files` is required, but it does not have to be non-empty. Use it to make the eval self-documenting: list the references in this repo that should be consulted to produce the expected output. For example:

- A `per-form-writing` eval that asks for a how-to should list `references/doc-blueprints.md`.
- A `classification` eval that asks which form fits should list `SKILL.md` and `references/template-map.md`.
- A `migration` eval that references the worked example should list `examples/messy-to-diataxis/before.md` and the four `after/*.md` files.
- A `non-trigger` eval should list `[]`.

The `non-trigger` empty case is the only one where `[]` is correct. For all other categories, an empty `files` is a code-review smell — the eval is probably under-specified.

### Coverage rule of thumb

Aim for at least two evals per category. Single-eval categories are easy to regress without noticing.

## Adding or editing a slash command

Every command ships once per host: `.claude/commands/` for Claude Code and `.opencode/commands/` for OpenCode. Each file is a small prompt template with a YAML frontmatter block.

Conventions:

- Filename: `docs-<verb>.md`, lowercase, hyphen-separated. Use one of `classify`, `split`, `review`, `audit`, `quickstart`, or add a new verb that matches what the command actually does.
- Add the command to **both** directories and to `COMMAND_NAMES` in `scripts/check_local.py`. A command that exists for one host only is a gap the user finds at the prompt; the checker fails on it.
- Keep the bodies identical across hosts and vary only the frontmatter. Both hosts derive the command name from the file name. Claude Code recognises `description`, `argument-hint`, `model`, `allowed-tools`, and `disable-model-invocation`; OpenCode recognises `description`, `agent`, `model`, `variant`, and `subtask`. Anything else is silently ignored by that host, so the checker warns.
- `description` is required by this repository so the command picker stays useful, and the body must contain `$ARGUMENTS` or the command discards whatever the user typed.
- The body should be a short system prompt that references the relevant section of `SKILL.md` rather than duplicating its content. The point of a slash command is to point the model at the right part of the skill, not to copy it.
- If you add a new command, also add a row to the `Slash commands` / `斜杠命令` table in `README.md` and `README.zh-CN.md`, and to `docs/commands.md` and `docs/zh-CN/commands.md`.

## Style

- Prefer simple, practical language.
- Keep the skill reader-first.
- Make the change easy to verify.

## Versioning and releasing

The skill uses a single source of truth for its version:

- `SKILL.md` frontmatter `metadata.version: X.Y.Z`
- `evals/evals.json` top-level `version: X.Y.Z`
- `CHANGELOG.md` `[X.Y.Z]` entry under a dated heading

The three must match. If you change behaviour in a way that affects the contract with users, bump the version and add a CHANGELOG entry.

## Questions

Open an issue if you are not sure whether a change fits the project. Use the templates in `.github/ISSUE_TEMPLATE/` (bug, feature, docs, or general question) and the PR template in `.github/PULL_REQUEST_TEMPLATE.md` so reviewers have what they need on the first read.
