---
name: docs-review
description: Review a documentation page for Diataxis compliance. Use when the user pastes a draft and asks for feedback before publishing.
---

You are running the diataxis-docs skill in review mode.

The user's input is below. Treat it as a documentation draft that needs pre-publication review.

## Input

$ARGUMENTS

## Task

1. Identify the dominant Diataxis form. If unclear, propose the most likely form and explain the assumption.
2. Check the draft against the **per-form anti-patterns** in `SKILL.md`.
3. Run the **mixed-doc smell test**. Flag any signals you see.
4. Check the **per-form final check** for the dominant form.
5. Produce a structured report with severity-tagged findings.

## Output shape

```markdown
## Review summary

- Dominant form: <form>
- Verdict: <ship | revise | rewrite>
- Top issue: <one-sentence summary>

## Findings

### Must fix

- <issue> — <where in the draft> — <suggested fix>
- ...

### Should fix

- <issue> — <where in the draft> — <suggested fix>
- ...

### Nice to have

- <issue> — <where in the draft> — <suggested fix>
- ...

## Mixed-form signals

- <signal>
- ...

## Suggested edits

For each "Must fix" item, paste a short replacement for the offending paragraph or heading.
```

Use "ship" only when the draft is single-form, focused, and aligned with the dominant form's blueprint. Use "revise" for small fixes. Use "rewrite" for structural problems.
