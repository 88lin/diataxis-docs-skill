---
name: diataxis-docs
description: "Apply the Diataxis compass to write, restructure, split, classify, review, audit, or migrate technical documentation. Trigger on requests like write docs, organize docs, fix docs, split this page, classify this docs page, audit our docs site, migrate to Diataxis, review this draft, or design a documentation system for an SDK or API."
license: MIT
metadata:
  version: "0.4.0"
---

# Diataxis Documentation Skill

Turn a documentation request into the right document type, at the right level of detail, for the right reader. Classify before writing.

## The Diataxis compass

Diataxis separates documentation by two questions — action or cognition, acquiring or applying skill — and yields four forms.

| If the content… | …and serves the user's… | …then it must belong to… |
| --- | --- | --- |
| informs action | acquisition of skill | a tutorial |
| informs action | application of skill | a how-to guide |
| informs cognition | application of skill | reference |
| informs cognition | acquisition of skill | explanation |

To use the compass, ask two questions:

- Is the content about **action** (practical steps, doing) or **cognition** (propositional knowledge, thinking)?
- Is the user **acquiring** skill (study) or **applying** skill (work)?

> "The compass can be applied equally to user situations that need documentation, or to documentation itself that perhaps needs to be moved or improved. Like many good tools, it's surprisingly banal." — [diataxis.fr/compass](https://diataxis.fr/compass/)

The compass finds your bearings; it is not a map of the territory. The 2x2 quadrant diagram on [diataxis.fr](https://diataxis.fr/) is good for orientation, the compass for decisions. They are not interchangeable.

Apply it at any scale — a sentence, a section, a page, a whole documentation set — and to existing pages as readily as to new ones. When an existing page's form does not match the answer, the page needs to be moved or rewritten, not relabelled.

It is most useful exactly when you feel doubt, or when the page in front of you seems to be one thing but resists the work. Intuition sometimes answers immediately and is wrong. Do not fixate on the names; if a question feels ambiguous, both readings may be valid.

## Quick decision tree

The compass is canonical. This tree is a fast path for common cases.

```text
What is the reader trying to do right now?
│
├── Acquiring a new skill from scratch?
│   ├── With a complete, guided lesson → Tutorial
│   └── With the shortest path to first success → Quickstart
│
├── Applying a known skill to a real task?
│   ├── General task with a clear goal → How-to
│   └── Stuck on an error → Troubleshooting
│
├── Looking up an exact fact, field, command, or limit? → Reference
│
└── Trying to understand why or how it works?            → Explanation
```

Request phrasing maps the same way: "a guide for my new users" → tutorial or quickstart; "how to do X" → how-to; "what does this field mean" → reference; "why is it designed this way" → explanation; "a documentation system" → use the compass to split it into the right forms.

If a request hits more than one branch, split it into multiple documents rather than blending them.

## The four forms at a glance

| Form | Reader is | Writing mode | Must have | Must not have |
| --- | --- | --- | --- | --- |
| Tutorial | learning | guided lesson | one linear path, visible expected results, stated prerequisites | branches, options, background essays |
| How-to | working | practical directions | one goal, short logical sequence, verification step | teaching, concept introductions |
| Reference | looking up | neutral description | structure mirroring the thing described, exact values, examples | instructions, recommendations, hedging |
| Explanation | reflecting | discursive context | one bounded topic, a point of view, tradeoffs and alternatives | procedures, "how to" framing |

Trigger words: tutorial — "try", "first time", "walkthrough". How-to — "configure", "deploy", "migrate". Reference — fields, flags, schemas, limits, error codes. Explanation — "why", "background", "design", "tradeoff".

For section-by-section structures per form, load [`references/doc-blueprints.md`](references/doc-blueprints.md).

## When to use this skill

- write, rewrite, restructure, or review a documentation page
- classify a page or a request with the compass
- split a messy page into the right forms
- audit or migrate an existing documentation set, one page at a time
- design a documentation system for an SDK, API, CLI, or product
- map user questions to the correct documentation form

## When NOT to use this skill

- marketing copy, blog posts, or non-technical writing
- purely visual content such as UI mockups, slides, or design specs
- code review, refactoring, debugging, or implementation work
- a single paragraph or short answer that needs no document structure
- translating documentation that already follows a clear structure

A useful test: if the request is more about *what* to say than about *which kind of document* to write, it is out of scope.

## Workflow

1. Identify the reader and their current state: learning, working, looking up, or reflecting.
2. Identify the need behind the request: a task, a fact, a concept, or a learning path.
3. Classify with the compass, and name what to exclude.
4. Clarify document type, audience, goal, and scope only if still not obvious. One short question, not an approval loop.
5. Outline using the blueprint for that form.
6. Write for that form alone. Link out to the other forms instead of mixing them in.
7. Run the [Quality checks](#quality-checks).

If the request spans several needs, deliver companion documents rather than one blended page. Write in the language the user is writing in.

When the reader state is genuinely ambiguous — usually tutorial versus how-to — ask: *is the reader learning a new skill through a guided exercise, or completing a real task they already understand?* If the user cannot clarify, state your assumption and write a focused how-to, linking teaching material out. See [`references/reader-analysis.md`](references/reader-analysis.md) for the full checklist.

## Anti-patterns: what NOT to do

The most common failure in technical documentation is **mixing forms**. If a draft shows any of these signals, stop and split, prune, or rewrite.

### The four cardinal sins

| Sin | What it looks like | Fix |
| --- | --- | --- |
| Page does everything | One page teaches, instructs, lists facts, and explains tradeoffs | Split into tutorial, how-to, reference, and explanation |
| Tutorial gives options | Step 2 offers three alternative paths | Pick one path; move alternatives to a how-to |
| How-to teaches | Page starts with "Concepts" or "Background" | Strip the teaching; link to a tutorial or explanation |
| Reference narrates | Reference page uses "we recommend", "you should", or stories | Strip the narration; keep neutral descriptions only |

### Per-form anti-patterns

**Tutorial**: branching or "choose your adventure" steps; long background before the first action; hidden prerequisites; no expected result at each checkpoint; sentences that do not help the learner take the next step.

**How-to**: opening with theory; "First, let's understand…" sections; re-teaching what the reader already knows; more than one goal per page; "when you are done, you will understand…" framing.

**Reference**: imperative voice ("Run this command") instead of description; comparisons, recommendations, or best-practice opinions; ordering by the author's sense of importance rather than the structure of the thing described; missing input and output examples; hedging such as "usually", "generally", "often".

**Explanation**: step-by-step instructions; "How to" titles instead of "About…" or "Why…"; unbounded scope; no point of view, which makes it a summary rather than an explanation.

### Mixed-doc smell test

A page is probably mixing forms if it has two or more of:

- A "Background" or "Concepts" section **and** a "Steps" or "Procedure" section
- Both narrative paragraphs **and** parameter tables in roughly equal weight
- Both "Why we built it this way" framing **and** "Run this command" instructions
- A "Tutorial" heading that includes optional branches or troubleshooting
- A "How-to" that begins with "In this tutorial you will learn…"
- A README over roughly 500 lines trying to teach, instruct, list, and explain at once

When a page trips the smell test, **split it** — do not add headings.

### README and adjacent types

- **README**: an entry point, not a docs site. Do not inline a full tutorial, list every flag, or mix install, configure, deploy, troubleshoot, and contribute.
- **Troubleshooting**: symptom → cause → solution. Move "why this happens" to explanation.
- **Glossary**: a list of terms. Move usage examples to how-to or reference.
- **Release notes**: change and impact. Move rationale to explanation.
- **Quickstart**: optimizes for first success, not completeness.
- **Style guide**: describes voice and rules; it does not re-derive Diataxis.

## Working at scale

Diataxis is a guide, not a plan. For a full documentation system, SDK docs, API docs, or a developer portal:

1. Apply the compass to existing material first. Tag every page with a compass cell and move the misplaced ones before adding anything new.
2. Write one page at a time, applying the compass to that page alone.
3. Let top-level structure emerge once enough pages exist to demand it.
4. If asked to propose a structure up front, treat it as a sketch, not a contract.

Do not create empty sections in advance, allocate content quotas per quadrant, force information architecture before the content is good, or treat "documentation system" as a deliverable — it is a practice. A messy page that is honest about its content beats a clean four-section site with nothing in three sections.

When the user asks for "a complete documentation system", ask what already exists and start there. When they ask to fix "one mega-page", walk the compass with them; the split is a consequence, not the goal.

Gather only the inputs you need now: source material, audience, platform, style constraints, code examples, and lifecycle needs such as versioning or release notes. The compass does the rest.

**Per-platform notes.** Plain Markdown or repo docs: one form per file, clear filenames such as `how-to-deploy.md`. Docusaurus, Mintlify, or GitBook: one form per top-level section so navigation reinforces the separation. ReadTheDocs and static sites: use section labels and admonitions sparingly; do not bury form boundaries in prose. Multi-product portals: one quadrant per page, with cross-product indexes on their own overview page.

## Bundled tools

`scripts/audit_docs.py` is a heuristic mixed-form scanner bundled with this skill. Use it as a mechanical pre-pass when auditing more than a handful of pages, then apply the compass to the pages it flags.

```bash
python scripts/audit_docs.py docs/                       # Markdown report
python scripts/audit_docs.py docs/ --format json         # machine-readable
python scripts/audit_docs.py . --exclude 'CHANGELOG.md'  # skip known-mixed files
```

It reports a risk level and the signals behind it. It is not an authoritative classifier — it narrows where to look. Never present its output as a final classification; read the flagged pages and decide with the compass.

## Reference files

Load these on demand; do not read them for every request.

| File | Load when |
| --- | --- |
| [`references/doc-blueprints.md`](references/doc-blueprints.md) | outlining or drafting a document and you want the section structure for its form |
| [`references/reader-analysis.md`](references/reader-analysis.md) | the reader or their state is unclear before drafting |
| [`references/template-map.md`](references/template-map.md) | mapping an artifact or a Good Docs Project template to a form or compass cell |
| [`references/zh-cn-anti-patterns.md`](references/zh-cn-anti-patterns.md) | reviewing Chinese technical documentation or a Chinese localization draft |

## Quality checks

Before finishing, run the intent check, the per-form check, and the [Mixed-doc smell test](#mixed-doc-smell-test).

**Intent check.** Did I identify the reader and their state before drafting? Classify with the compass first? Write for the reader's actual state rather than my own mental model? Keep the document on one need? Avoid inventing structure that the content does not yet demand? Leave room for linked companion documents?

**Per-form check.**

- **Tutorial**: a complete beginner can finish it without reading anything else; every step has a visible result.
- **How-to**: an experienced user finds the answer in under a minute; the page covers exactly one goal.
- **Reference**: every entry is structured identically; nothing is missing or redundant.
- **Explanation**: one concept, a clear point of view, no procedures.

Never claim a document is verified when it has not been. If a code example or command has not been run, say so.

## Sources

This skill distills [diataxis.fr](https://diataxis.fr/) — in particular [start here](https://diataxis.fr/start-here/), [the compass](https://diataxis.fr/compass/), [how to use Diataxis](https://diataxis.fr/how-to-use-diataxis/), and the pages for [tutorials](https://diataxis.fr/tutorials/), [how-to guides](https://diataxis.fr/how-to-guides/), [reference](https://diataxis.fr/reference/), and [explanation](https://diataxis.fr/explanation/) — together with [The Good Docs Project](https://www.thegooddocsproject.dev/) [templates](https://www.thegooddocsproject.dev/template/).
