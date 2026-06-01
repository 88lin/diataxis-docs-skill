---
name: docs-audit
description: Audit a whole documentation site or docs directory. Use when the user wants a page-by-page Diataxis classification and a list of mixed-form pages.
---

You are running the diataxis-docs skill in audit mode.

The user's input is below. It is either a path to a docs directory, a list of page paths, or a list of pasted pages.

## Input

$ARGUMENTS

## Task

1. If the user gave a path, list the markdown files in the directory and treat each as a page.
2. If the user gave a list of pages, treat each as a page.
3. For each page, classify the dominant form and run the mixed-doc smell test.
4. Produce a per-page row in a table.
5. Group findings by severity: pages that need a split, pages that need a small fix, and pages that are clean.

## Output shape

```markdown
## Audit summary

- Pages reviewed: <count>
- Pages that need a split: <count>
- Pages that need a small fix: <count>
- Pages that are clean: <count>

## Per-page findings

| Page | Dominant form | Mixed-form? | Severity | Recommended action |
| --- | --- | --- | --- | --- |
| <path or name> | <form> | yes / no | split / fix / clean | <one-line action> |
| ... |

## Pages that need a split

### <page name>

- Dominant form: <form>
- Mixed-form signals: <list>
- Recommended split: <bullet list of new pages and their forms>

### ...

## Pages that need a small fix

- <page name>: <short description of the fix>
- ...

## Clean pages

- <list>
```

If the input is too large, audit a representative sample (around 5 to 10 pages) and tell the user the rest can be processed on request.
