# Questions about scope and design

Why this skill exists, what it deliberately does not do, and how it differs from asking an assistant to "write good docs".

## Why does this skill exist?

Most documentation problems are classification problems, not writing problems.

When one page tries to teach a beginner, guide a working user, list API facts, and explain design tradeoffs at once, every reader loses. The beginner cannot find the lesson, the working user cannot find the steps, the expert cannot find the field they came for, and the maintainer does not know where new content belongs. The prose can be excellent and the page still fails.

Diataxis addresses this by asking two questions before writing: does the content inform action or cognition, and does it serve acquiring or applying skill? The answers pick one of four forms. This skill turns those questions into something an assistant applies before it starts drafting.

## Is this just a summary of the Diataxis website?

No. Diataxis is a framework for people. This skill is an operating procedure for a model.

It adds a trigger definition so the assistant knows when the framework applies, a per-form anti-pattern checklist so it knows what to avoid, blueprints so each form has a starting structure, a mapping to Good Docs Project templates so adjacent document types have a home, and a plan for large systems so it does not try to rewrite a docs site in one pass.

## How is this different from generic writing help?

A generic assistant optimizes for fluent prose. This skill optimizes for the right kind of document.

| Generic writing help | This skill |
| --- | --- |
| "Here is a well-written docs page." | "Here is the right kind of page for this reader." |
| Treats the request as a writing task. | Treats the request as a classification task. |
| Mixes forms by default. | Splits and prunes to keep one form per page. |
| Encourages comprehensive coverage. | Encourages focused pages that link to companions. |
| Does not say what to avoid. | Ships an explicit anti-patterns checklist. |
| Judged on prose quality. | Judged on classification accuracy and form separation. |

If you want fluent prose, you do not need this skill. If you want the shape of the document to be right, you do.

## When should I not use it?

The skill is deliberately narrow. It is the wrong tool for marketing copy and blog posts, for visual artifacts such as mockups and slides, for code review and implementation work, for short answers that need no document structure, and for translating documentation that is already well structured.

A useful test: if the request is more about *what* to say than about *which kind of document* to write, you are outside the scope. The skill ships explicit non-trigger evals so this boundary is tested rather than assumed.

## Does it replace the author?

No. It improves the assistant's first-draft decision about what kind of document to write. Accuracy, tone, product knowledge, and the final structure remain yours. The skill cannot know whether a claim about your product is true.

## Do I need to know Diataxis to use it?

No. The decision tree, the anti-pattern checklist, and the blueprints are written to be usable without having read the source material. Reading [diataxis.fr](https://diataxis.fr/) will make you better at judging the output, but it is not a prerequisite for getting useful output.

## What languages does it work in?

The framework is language-agnostic and the skill applies it in whatever language you write in. The bundled documentation is bilingual, English and Simplified Chinese. `references/zh-cn-anti-patterns.md` covers failure modes specific to Chinese technical writing, since some anti-patterns do not transfer between languages.

## Will it write my code examples?

Only as part of a tutorial or a reference page, and only where an example is what the form calls for. Choosing the form is the skill's job; the correctness of the code is yours, because only you can run it.

## How is the skill evaluated?

[`evals/evals.json`](../evals/evals.json) holds 32 prompts across 11 categories: classification, single-page classification, mixed-form detection, per-form writing, decision framework, review, migration, large-system planning, adjacent types, anti-pattern avoidance, and non-trigger cases.

Each eval pairs a realistic prompt with the shape a correct answer should have. Scoring is manual — a human or a model reads the response and judges it. There is no automated grader, so treat the evals as a regression checklist rather than a benchmark score. Adding one is described in [Development](development.md#add-an-eval).

## Why is the skill file so long?

Because it is a reference the model consults, not a page a person reads start to finish. Every line is still a cost paid on each use, so the file is capped at 500 lines by CI and detail lives in `references/`, which the skill links to and loads only when needed.

The same reasoning shapes the rule export for other assistants. See [Context cost](ide-integration.md#context-cost).

## Was there a `skills.paths` config option?

Version 0.1.0 documented an OpenCode `skills.paths` setting. That option does not exist. Install by cloning into a directory OpenCode already discovers, as described in [Install the skill](installation.md).
