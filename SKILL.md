---
name: diataxis-docs
description: "Use when writing, restructuring, splitting, classifying, reviewing, or auditing technical documentation with Diataxis forms: tutorials, how-to guides, reference, explanation, quickstarts, READMEs, troubleshooting, glossaries, release notes, and style guides. Trigger on prompts like write docs, organize docs, fix docs, split this page, classify this docs page, audit our docs site, migrate to Diataxis, review this draft, or design a documentation system for an SDK or API."
---

# Diataxis Documentation Skill

Use this skill to turn a documentation request into the right document type, with the right level of detail, for the right reader.

## Core idea

Diataxis separates documentation by two questions:

- Is the content about action or cognition?
- Is the reader acquiring skill or applying skill?

That yields four primary forms:

- Tutorial: action + acquisition
- How-to: action + application
- Reference: cognition + application
- Explanation: cognition + acquisition

Use the distinction first. Do not start by outlining sections.

## Quick decision tree

When in doubt, walk through this before drafting:

```text
What is the reader trying to do right now?
│
├── Acquiring a new skill from scratch?
│   ├── With a complete, guided lesson → Tutorial
│   └── With the shortest path to first success → Quickstart
│
├── Applying a known skill to a real task?
│   ├── General task with a clear goal → How-to
│   └── Diagnosing a failure or error → Troubleshooting
│
├── Looking up an exact fact, field, command, or limit? → Reference
│
└── Trying to understand why or how it works?        → Explanation
```

If the request hits more than one branch, split it into multiple documents rather than blending them.

## When to use this skill

Use this skill when the task is to:

- write, rewrite, restructure, or review a documentation page
- choose the right document type for a new request
- split a single messy page into the right Diataxis forms
- design a full documentation system for an SDK, API, CLI, or product
- map user questions to the correct documentation form

## When NOT to use this skill

Do not use this skill for:

- marketing copy, blog posts, or non-technical writing
- purely visual content such as UI mockups, slides, or design specs
- code review, refactoring, or implementation work
- writing a single paragraph or a short response that does not need a document structure
- translations of finished documentation that already follows a clear structure

## Guiding principles

- Clarity: write in simple, direct language.
- Accuracy: keep facts, code snippets, and document details up to date.
- User centricity: optimize for the reader's goal, not the author's internal structure.
- Consistency: keep tone, terminology, and formatting aligned across the document set.

## Workflow

1. Identify the reader.
2. Identify the reader's current state: learning, working, looking up facts, or reflecting.
3. Identify the user need: a task, a fact, a concept, or a learning path.
4. Classify the content using the Diataxis compass.
5. Write only for that form.
6. Link out to the other forms instead of mixing them in.
7. Check whether the document still feels complete, focused, and easy to use.

If the request spans multiple needs, split it into multiple documents rather than blending them together.

## Typical delivery pattern

For most requests, follow this order:

1. Clarify the document type, audience, goal, and scope if they are not obvious.
2. Propose or infer the outline for that document type.
3. Write the document in Markdown using the right blueprint.
4. If the request is actually a mixed documentation system, split it into companion docs instead of one large page.

Do not force a long approval loop for every task. Use a short clarification loop only when the user has not given enough information.

## Anti-patterns: what NOT to do

The most common failure in technical documentation is **mixing forms**. The rules below are the inverse of the guidance above. If a draft shows any of these signals, stop and split, prune, or rewrite.

### The four cardinal sins

| Sin | What it looks like | Fix |
| --- | --- | --- |
| Page does everything | One page teaches, instructs, lists facts, and explains tradeoffs | Split into tutorial, how-to, reference, and explanation |
| Tutorial gives options | Step 2 offers three alternative paths | Pick one path; move alternatives to a how-to |
| How-to teaches | Page starts with "Concepts" or "Background" | Strip the teaching; link to a tutorial or explanation |
| Reference narrates | Reference page uses "we recommend", "you should", or stories | Strip the narration; keep neutral descriptions only |

### Per-form anti-patterns

**Tutorial anti-patterns**

- Branching paths or "choose your adventure" steps. Tutorials must be linear.
- Long background sections before the first action. Move background to explanation.
- Hidden prerequisites. State them at the top.
- Skipping the expected result. Show what success looks like at every checkpoint.
- Over-explaining. If a sentence is not helping the learner do the next step, cut it.

**How-to anti-patterns**

- Opening with theory. Start with the goal.
- "First, let's understand…" sections. The reader is working, not learning.
- Re-teaching concepts the user already knows. Link out instead.
- More than one goal per page. Split the page.
- "When you are done, you will understand…" framing. That belongs in a tutorial.

**Reference anti-patterns**

- Imperative voice ("Run this command", "Set this value"). Reference describes, it does not instruct.
- Comparisons, recommendations, or "best practice" opinions. Move them to explanation.
- Sections ordered by importance to the author. Order by the structure of the thing described.
- Missing examples of input and output. Every entry should show concrete usage.
- Soft language such as "usually", "generally", "often". Be exact or omit.

**Explanation anti-patterns**

- Step-by-step instructions. Explanations do not give procedures.
- "How to" titles. Use "About …" or "Why …" framing.
- Unbounded scope. Cover one concept, one design decision, or one tradeoff at a time.
- No opinion. An explanation that does not commit to a perspective is just a summary.

### Mixed-doc smell test

A page is probably mixing forms if it has two or more of:

- A "Background" or "Concepts" section **and** a "Steps" or "Procedure" section
- Both narrative paragraphs **and** parameter tables in roughly equal weight
- Both "Why we built it this way" framing **and** "Run this command" instructions
- A "Tutorial" heading that includes optional branches or troubleshooting
- A "How-to" that begins with a learning outcome statement
- A README longer than about 500 lines that tries to teach, instruct, list, and explain at once

When a page trips the smell test, the right response is to **split it**, not to add headings.

### README-specific anti-patterns

- README doing the work of an entire docs site. README is an entry point.
- "Quickstart" inside the README that is actually a full tutorial. Link to the tutorial instead.
- Listing every command, option, or flag in the README. Move them to reference.
- Mixing install, configure, deploy, troubleshoot, and contribute all in one file.

### Adjacent-type anti-patterns

- **Troubleshooting that explains**: keep it symptom → cause → solution. Move "why this happens" to explanation.
- **Glossary that teaches**: a glossary is a list of terms. Move usage examples to how-to or reference.
- **Release notes that justify**: release notes state change and impact. Move rationale to explanation.
- **Style guide that classifies**: the style guide should describe voice and rules, not re-derive Diataxis.
- **Quickstart that explores**: a quickstart optimizes for first success, not for completeness.

## Large documentation systems

When the user asks for a full documentation system, SDK docs, API docs, developer portal, or documentation site, plan it as a layered deliverable rather than a single page.

### Inputs to gather first

| Category | Items to confirm |
| --- | --- |
| Source material | API spec, source code, existing docs, product notes, screenshots, transcripts |
| Audience profiles | Beginners, experienced developers, admins, support, partners, non-technical users |
| Platform preference | Plain Markdown, Docusaurus, ReadTheDocs, Mintlify, GitBook, static site, repo docs |
| Style constraints | Brand voice, terminology, localization, accessibility, formatting rules |
| Code examples | Languages, runnable snippets, SDK samples, CLI examples, sample repositories |
| Lifecycle needs | Versioning, search, navigation, release notes, changelog, deprecation policy |
| Success metrics | What readers must be able to do after reading; what feedback the team expects |

### Output artifacts to propose

Map each artifact to a Diataxis form so the system stays honest:

| Artifact | Primary form | Purpose |
| --- | --- | --- |
| Getting started path or quickstart | Tutorial | First success for a new user |
| How-to guide collection | How-to | One task per page, assumes competence |
| API, CLI, config, or schema reference | Reference | Neutral, structured facts |
| Concept, architecture, and design articles | Explanation | Why and how it works, tradeoffs |
| Troubleshooting section | How-to (with reference links) | Symptom → cause → solution |
| Glossary | Reference | Project-specific terms |
| Release notes and changelog | Reference (with user-facing framing) | What changed and why it matters |
| Style guide | Meta | Team rules for consistent writing |
| Sample apps and runnable examples | Tutorial / Reference | Validate the system end to end |
| Navigation and information architecture | Structural layer | Keep Diataxis separation visible in IA |

### Per-platform notes

- **Plain Markdown or repo docs**: keep one form per file; use clear filenames such as `how-to-deploy.md`.
- **Docusaurus / Mintlify / GitBook**: place each form under a distinct top-level section so navigation reinforces the separation.
- **ReadTheDocs / static sites**: use section labels and admonitions sparingly; do not hide form boundaries inside prose.
- **Multi-product portals**: keep one Diataxis quadrant per page; let the cross-product index live in a separate overview page.

### Decision flow

1. Clarify the audience, platform, and source material.
2. List the artifacts above and tag each with a primary form.
3. For each artifact, choose the matching blueprint from `references/doc-blueprints.md`.
4. Build the navigation so the four forms remain visibly separated.
5. Add a release-notes and deprecation policy if the system has a versioned lifecycle.

Keep the Diataxis separation intact even when the final site has platform-specific navigation.

## Reference files

Use the bundled references when you need more structure than the main guidance provides:

- `references/reader-analysis.md`: ask these questions before drafting.
- `references/doc-blueprints.md`: use these section patterns when outlining a document.
- `references/template-map.md`: use this to map Diataxis forms to common TGDP templates.

## Classification guide

### Tutorial

Use when the reader needs a guided learning experience.

Write it as a safe, structured lesson:

- start with a clear learning outcome
- use a single path
- keep steps concrete and sequential
- show expected results early and often
- minimize explanation
- avoid options and digressions

Good signs:

- "learn", "try", "first time", "hands-on", "intro", "walkthrough"
- the user is not yet competent

### How-to

Use when the reader already knows the basics and wants to achieve a task.

Write it as practical directions:

- begin with the goal
- assume basic competence
- cover one task or problem
- keep the sequence logical and short
- include warnings and alternate paths only when needed
- do not teach concepts

Good signs:

- "how do I...", "configure", "deploy", "set up", "migrate", "troubleshoot"
- the reader is in work mode

### Reference

Use when the reader needs exact facts.

Write it as neutral technical description:

- organize by the structure of the thing described
- keep language factual and concise
- include parameters, values, limits, fields, commands, return values, examples
- avoid instructions, teaching, and discussion

Good signs:

- APIs, fields, commands, flags, schemas, tables, options, limits, error codes

### Explanation

Use when the reader needs understanding.

Write it as context-rich discussion:

- explain why something exists
- connect related ideas
- discuss tradeoffs, history, and alternatives
- allow perspective and judgment
- keep it separate from procedural guidance

Good signs:

- "why", "background", "concept", "design", "tradeoff", "overview", "discussion"

## Useful adjacent document types

Use these as concrete specializations of the four forms:

- Quickstart: a short tutorial that gets a user to a first success fast
- README: the project's first impression and entry point
- Troubleshooting: symptom -> cause -> solution
- Glossary: terms and definitions for project-specific language
- Release notes: what changed, why it matters, and known issues
- Style guide: team rules for writing consistently

For API and SDK documentation, treat these as common combinations:

- Getting started or quickstart -> tutorial
- Authentication setup -> how-to or reference, depending on whether it is task steps or field definitions
- Endpoint, method, class, option, or error-code pages -> reference
- Architecture, design model, rate limits, pagination model, or SDK philosophy -> explanation
- Migration and upgrade guides -> how-to with reference links

When a request sounds like one of these, map it back to the four Diataxis needs before writing.

## Writing patterns

### For tutorials

- Use second-person or inclusive language where appropriate.
- Keep the path stable and predictable.
- Avoid comprehensive background sections.
- Give the user visible progress.

### For how-tos

- Start with the objective.
- Use conditional imperatives where helpful.
- Keep to one goal per page.
- Put supporting material in links, not inline essays.

### For reference

- Mirror the product structure.
- Prefer tables, lists, and schemas.
- Be explicit and consistent.

### For explanation

- Make connections.
- Provide context.
- Discuss alternatives and implications.
- Keep the scope bounded to one concept or topic.

## Template selection heuristic

If the user asks for:

- "a guide for my new users" -> tutorial or quickstart
- "how to do X" -> how-to
- "what does this field/command mean" -> reference
- "why is it designed this way" -> explanation
- "a single document system for docs" -> use Diataxis to split the system into the right document types

## Quality checks

Before finishing, run both the **intent check** and the **smell test**.

### Intent check

- Did I identify the reader and their state before drafting?
- Did I classify the content using the Diataxis decision tree first?
- Did I write for the reader's actual state, not the author's mental model?
- Did I keep the document focused on one need?
- Did I avoid unnecessary structure at the top level?
- Did I leave room for linked companion documents?

### Mixed-doc smell test

If two or more of the following are true, split the document before publishing:

- The page has both a "Background" or "Concepts" section and a "Steps" or "Procedure" section.
- Narrative paragraphs and parameter tables carry roughly equal weight.
- The page explains why something works and also tells the reader to run specific commands.
- The page uses a tutorial framing (learning outcomes, "let's", encouraging tone) for a task-driven audience.
- The page uses a how-to framing (imperative steps) for a beginner audience that needs a guided lesson.
- The page uses a reference framing (tables, parameter lists) for an audience that needs motivation or context.
- The page is longer than the reader's patience for that form (for example, a 2 000-line README).

### Per-form final check

- **Tutorial**: a complete beginner can finish it without reading anything else; every step has a visible result.
- **How-to**: an experienced user can find the answer in under a minute; the page covers exactly one goal.
- **Reference**: every entry is structured identically; nothing is missing or redundant.
- **Explanation**: a single concept is covered; the author commits to a perspective; no procedures are included.

## References

Use these as the primary source material behind this skill:

- https://diataxis.fr/
- https://diataxis.fr/start-here/
- https://diataxis.fr/compass/
- https://diataxis.fr/how-to-use-diataxis/
- https://diataxis.fr/tutorials/
- https://diataxis.fr/how-to-guides/
- https://diataxis.fr/reference/
- https://diataxis.fr/explanation/
- https://www.thegooddocsproject.dev/
- https://www.thegooddocsproject.dev/template/

This skill distills those sources into a practical documentation workflow.

## Practical output pattern

When the user asks you to write documentation, start with a short diagnosis first:

- What is the reader trying to do?
- What state are they in?
- Which document type is this?
- What should be excluded?

Then write the document, or produce a doc plan, in the chosen form.
