---
name: docs-split
description: Split a mixed-form documentation page into the right Diataxis documents. Use when the user pastes a messy page and asks for a refactor.
---

You are running the diataxis-docs skill in split mode.

The user's input is below. Treat it as a single documentation page that mixes several Diataxis forms.

## Input

$ARGUMENTS

## Task

1. Run `docs-classify` mentally first. Identify the dominant form and the mixed-form signals.
2. Decide how many new pages are needed (usually 2 to 4).
3. For each new page:
   - assign a single Diataxis form
   - list the sections from the original that should move into it
   - write a short outline using the matching blueprint from `references/doc-blueprints.md`
4. Draft the new pages. Keep prose close to the original where possible; rewrite only to remove cross-form contamination.
5. If the original page is the project entry point, also draft a short overview page that links to the new pages.

## Output shape

```markdown
## Diagnosis

- Dominant form: <form>
- Mixed-form signals: <list>

## Split plan

1. <new page name> — <form>
   - Sections from original: <list>
   - Outline: <bullet outline>
2. <new page name> — <form>
   - ...

## Drafts

### <new page name>

<full markdown draft>

### <new page name>

<full markdown draft>

...

## Original page replacement

<short overview page that links to the new pages>
```

Do not invent product details. Where the original is ambiguous, write a clear placeholder and note it.
