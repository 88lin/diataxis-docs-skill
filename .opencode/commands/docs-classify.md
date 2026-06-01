---
name: docs-classify
description: Classify a single documentation page using Diataxis. Use when the user pastes or references a page and asks what kind of document it should be.
---

You are running the diataxis-docs skill in classification mode.

The user's input is below. Treat it as a single documentation page that may mix several Diataxis forms.

## Input

$ARGUMENTS

## Task

1. Read the page and identify each section.
2. For each section, assign one of: tutorial, how-to, reference, explanation, quickstart, troubleshooting, glossary, release notes, style guide, or other.
3. Decide the **dominant** form of the page.
4. Run the **mixed-doc smell test** from `SKILL.md`. List any signals that the page mixes forms.
5. If the page mixes forms, propose a split. For each new page, name it, summarize its outline, and link the related sections.

## Output shape

```markdown
## Classification

- Dominant form: <form>
- Reader state: <learning | working | looking up | reflecting>

## Section-by-section tags

- <section heading>: <form>
- ...

## Mixed-form signals

- <signal 1>
- <signal 2>

## Recommended split (if any)

1. <new page name> — <form> — <one-sentence summary>
2. ...

## Reasoning

<short paragraph explaining the call>
```

If the page is already single-form, say so explicitly and skip the split section.
