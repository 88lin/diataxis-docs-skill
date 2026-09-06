# Develop and contribute

How to validate a change, add content, and understand what CI enforces.

## Before you start

You need Python 3.11 or newer. There are no third-party dependencies; every script uses the standard library so CI needs no install step.

## Run the checks

```bash
python scripts/check_local.py
```

This is the single source of truth for repository validation. CI runs this exact command, so a green local run means a green CI run. It exits non-zero on the first category of failure and prints every problem it found.

It validates:

- `SKILL.md` frontmatter against the skill spec: `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, `description` is within 1024 characters, and unrecognised fields are reported
- `SKILL.md` body stays under 500 lines, warning from 400
- installation docs clone into a directory named after the skill
- both hosts ship the same five slash commands, each with a `description`, a `$ARGUMENTS` placeholder, and frontmatter fields that host recognises
- `evals/evals.json` structure, unique ids, known categories, and referenced files
- internal markdown links, heading anchors, and image paths
- English and Chinese docs stay paired
- required files exist
- `SKILL.md`, `evals/evals.json`, and `CHANGELOG.md` agree on the version
- every section `export_rules.py --compact` selects still exists in `SKILL.md`
- the unit tests pass

## Run the tests directly

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

- `tests/test_check_local.py` feeds deliberately wrong input to each check and asserts it is caught. A validator that stops validating is worse than no validator.
- `tests/test_audit_docs.py` covers the signal counters, the CLI exit codes, and `--exclude`.
- `tests/test_export_rules.py` writes compact and full exports to temporary projects, then checks link integrity and the Windsurf size limit.

## Scan docs for mixed-form smells

```bash
python scripts/audit_docs.py docs/
python scripts/audit_docs.py . --exclude 'CHANGELOG.md' --fail-on high
```

The scanner reports pages worth a human look. It is not an authoritative classifier.

Signals are counted on prose only: YAML frontmatter and fenced code blocks are removed first, and inline code spans are removed before tables are counted. A shell pipeline such as `ls | wc -l` inside a code block is therefore not counted as a table row.

| Signal | Meaning |
| --- | --- |
| `code_blocks` | Fenced blocks, counted as blocks rather than fence lines |
| `table_rows` | Header and body rows of real tables; separator rows excluded |
| `step_lines` | Instruction lines. English: an imperative verb at the start. Chinese: a verb anywhere in a short list item or colon-terminated lead-in, since Chinese instructions usually open with an adverbial phrase |
| `explanation_terms` | Words such as why, background, architecture, tradeoff |
| `reference_terms` | Interface vocabulary such as parameter, field, schema, endpoint, limit |

Scores accumulate across three rules; 4 or more is high risk, 2 or 3 is medium. `--fail-on {none,medium,high}` sets the exit code, which is how CI keeps this repository's own pages honest.

Three deliberate limits keep the false-positive rate down:

- **Code blocks are not reference evidence.** Every how-to is full of commands, so counting them made each installation guide look like a reference page carrying instructions.
- **A table needs reference vocabulary to count against a how-to.** A how-to may legitimately end in a symptom/cause/fix table; only words like parameter or field mark a table as describing an interface.
- **The weak `tutorial/how-to` rule cannot flag a page alone.** It adds 1 point to a page another rule already flagged, rather than promoting a clean page on its own.

Chinese matching is keyword-based with no word segmentation, so a bullet opening with a verb used as a noun ("安装文档…", "installation docs…") can still be counted as a step. A one-signal miscount does not change the risk level on its own; treat the score as triage, not a verdict. `tests/test_audit_docs.py` asserts that each translated page scores the same risk as its English original, which is how per-language pattern drift gets caught.

## Add an eval

Append an object to the `evals` array in [`evals/evals.json`](../evals/evals.json):

```json
{
  "id": 33,
  "category": "classification",
  "prompt": "The prompt a user would actually type.",
  "expected_output": "The shape of a correct answer, not its exact wording.",
  "files": ["SKILL.md"]
}
```

`id` must be unique, `category` must appear in the top-level `categories` array, and every path in `files` must exist. Add a new category to that array before using it. Then run `python scripts/check_local.py`.

Evals are prompt-and-expectation pairs for human or model review. There is no automatic scoring.

## Add a slash command

Create the same file in **both** [`.claude/commands/`](../.claude/commands/) and [`.opencode/commands/`](../.opencode/commands/), then add its name to `COMMAND_NAMES` in `scripts/check_local.py`. The file name becomes the command name. `check_local.py` fails if a command exists for one host and not the other.

```markdown
---
description: One sentence on when to use this command.
---

You are running the diataxis-docs skill in <mode> mode.

## Input

$ARGUMENTS

## Task

...

## Output shape

...
```

Keep the body identical across hosts and vary only the frontmatter. Claude Code recognises `description`, `argument-hint`, `model`, `allowed-tools`, and `disable-model-invocation`; OpenCode recognises `description`, `agent`, `model`, `variant`, and `subtask`. Both hosts make `description` optional, but this repository requires it so every command has useful picker text, and requires `$ARGUMENTS` in the body so the command cannot silently ignore its input. The checker warns about a field the host does not recognise, including `name`.

## Edit SKILL.md

`SKILL.md` is loaded into the model's context, so length is a cost paid on every use. Two rules:

- Keep the body under 500 lines. Move detail into `references/` and link to it.
- Do not restate a section elsewhere in the file. Duplication inside a skill file wastes context and creates two things to keep in sync.

The same applies between `SKILL.md` and this documentation. The skill file is written for a model; these pages are written for a person.

## Repository layout

```text
.
├── SKILL.md                    # skill instructions loaded by the host
├── README.md                   # entry point
├── docs/                       # human documentation, English
│   └── zh-CN/                  # human documentation, Chinese
├── references/                 # detail the skill links to on demand
├── examples/messy-to-diataxis/ # worked before-and-after split
├── evals/evals.json            # prompt-and-expectation pairs
├── .claude/commands/           # slash-command prompts, Claude Code
├── .opencode/commands/         # slash-command prompts, OpenCode
├── scripts/                    # validation, audit, and export tooling
├── tests/                      # unit tests for the scripts
└── .github/workflows/ci.yml    # runs check_local.py and the audit
```

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Trigger guidance, classification logic, anti-patterns, quality checks |
| `references/reader-analysis.md` | Reader-first checklist before drafting |
| `references/doc-blueprints.md` | Reusable structures per document type |
| `references/template-map.md` | Diataxis forms mapped to Good Docs Project templates |
| `references/zh-cn-anti-patterns.md` | Chinese-language documentation anti-patterns |
| `scripts/check_local.py` | Repository validation; CI runs this |
| `scripts/audit_docs.py` | Heuristic mixed-form scanner |
| `scripts/export_rules.py` | Rule-file exporter for other assistants |

## CI

[`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs one job on Python 3.11 and 3.12 for every push and pull request to `master`:

1. `python scripts/check_local.py`
2. `python scripts/audit_docs.py . --exclude 'CHANGELOG.md' --fail-on high`
3. `python scripts/export_rules.py --list`, then a full and a compact `--dry-run` export, so a broken target is caught in either mode

CI holds no validation logic of its own. Adding a check means editing `scripts/check_local.py`, which keeps the local and CI results identical.

## Translations

`docs/` and `docs/zh-CN/` must contain the same file names; `check_local.py` fails if they drift. Chinese pages are full translations, not summaries. `README.md` and `README.zh-CN.md` follow the same rule.

## Open a pull request

Open an issue first for anything larger than a fix, so the skill stays focused. Useful contributions usually improve trigger wording in `SKILL.md`, the blueprints, the eval prompts, worked examples, or the translations.

See [CONTRIBUTING.md](../CONTRIBUTING.md).
