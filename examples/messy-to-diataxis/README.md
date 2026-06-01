# Example: messy docs to Diataxis split

This example shows a single realistic documentation page that mixes several Diataxis forms, and the four documents it should be split into.

The example is fictional. It is intentionally short but representative of the kind of page that ships in many real SDK and API docs.

## Files

| File | Role |
| --- | --- |
| `before.md` | The original mixed-form page. Everything in one file: tutorial, how-to, reference, explanation. |
| `after/01-tutorial.md` | The beginner lesson. A guided path to a first success. |
| `after/02-how-to.md` | The focused task page. One goal, no teaching. |
| `after/03-reference.md` | The neutral, structured facts. |
| `after/04-explanation.md` | The context and tradeoffs. |

## Why this example is useful

A common failure mode is "we have one big Getting Started page that does everything." This example shows:

1. How to recognize the mixing with the `mixed-doc smell test` from `SKILL.md`.
2. How to decide which content belongs in which form.
3. What a clean split actually looks like in Markdown.

## How to read this example

- Open `before.md` **in source view** — each top-level section (and most sub-sections) carries an HTML comment at the start of the section that tags it with its current form. The comment is invisible in the rendered Markdown, so the page still reads as a normal doc, but every section is already labelled.
- The tag is one of the four Diataxis forms (`tutorial`, `how-to`, `reference`, `explanation`) or a `meta:` prefix when a section is not really a form at all (the page's own framing callout, a scope note, a cross-page link farm). The `meta:` prefix exists because the four forms above are the only Diataxis forms — it keeps the tag set honest.
- Use those tags to see exactly which sections need to move. The "What just happened" block inside the tutorial, the "Why we built QuokkaDB" section, the parameter table, the error-code table, the troubleshooting list, and the how-to recipe cluster all have different forms and end up in different files.
- Then read `after/01-tutorial.md` to `after/04-explanation.md` in order and confirm each one is single-purpose.
- Compare the totals. The split version is similar in length overall, but each page is focused and easy to scan.

## Applying this to your own docs

Use the same procedure on any page that fails the smell test:

1. Open the page in source view and tag each section. Use one of the four Diataxis forms (`tutorial`, `how-to`, `reference`, `explanation`) when the section is a real form. Use `meta: <role>` when it is a page-level framing callout, a scope note, or a cross-page link farm that is not a form at all.
2. Group sections by tag.
3. For each group, write a new page using the matching blueprint from `references/doc-blueprints.md`.
4. Replace the original with a short overview page that links to the four.
