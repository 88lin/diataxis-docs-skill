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
- add or refine a slash command under `.opencode/commands/`

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

The script runs three checks locally and mirrors the CI workflow exactly:

- **Validate evals.json** — JSON is well-formed, every eval has the required fields (`id`, `category`, `prompt`, `expected_output`, `files`), every `id` is unique, every `category` is in the whitelist, and prompts/expected outputs are non-trivial.
- **Check internal links** — every relative Markdown link points to a file that exists.
- **Verify structure** — all required files and example files are present.

CI runs the same checks on every push to `master` and on every pull request, so a passing local run is the fastest way to keep CI green.

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

Slash commands live in `.opencode/commands/`. Each file is a small prompt template with a YAML frontmatter block.

Conventions:

- Filename: `docs-<verb>.md`, lowercase, hyphen-separated. Use one of `classify`, `split`, `review`, `audit`, `quickstart`, or add a new verb that matches what the command actually does.
- Frontmatter must include `name` and `description` on the first five lines. The CI workflow greps for this; if either is missing the build fails.
- The body should be a short system prompt that references the relevant section of `SKILL.md` rather than duplicating its content. The point of a slash command is to point the model at the right part of the skill, not to copy it.
- If you add a new command, also add a row to the `Slash commands` / `斜杠命令` table in `README.md` and `README.zh-CN.md`.

## Style

- Prefer simple, practical language.
- Keep the skill reader-first.
- Make the change easy to verify.

## Versioning and releasing

The skill uses a single source of truth for its version:

- `SKILL.md` frontmatter `version: X.Y.Z`
- `evals/evals.json` top-level `version: X.Y.Z`
- `CHANGELOG.md` `[X.Y.Z]` entry under a dated heading

The three must match. If you change behaviour in a way that affects the contract with users, bump the version and add a CHANGELOG entry. Until a tagged release is cut, both files are at `0.1.0`.

## Questions

Open an issue if you are not sure whether a change fits the project. Use the templates in `.github/ISSUE_TEMPLATE/` (bug, feature, docs, or general question) and the PR template in `.github/PULL_REQUEST_TEMPLATE.md` so reviewers have what they need on the first read.
