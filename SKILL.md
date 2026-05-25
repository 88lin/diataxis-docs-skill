---
name: diataxis-docs
description: "Use when writing, restructuring, or reviewing technical documentation with Diataxis documentation forms including tutorials, how-to guides, reference docs, explanations, quickstarts, README, troubleshooting, glossary, style guide, and release notes. Use for prompts like write docs, organize docs, fix docs, or make a template."
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

## Large documentation systems

When the user asks for a full documentation system, SDK docs, API docs, developer portal, or documentation site, gather these inputs before designing the structure:

- source material: API specification, source code, existing docs, product notes, or screenshots
- target audience profiles: beginners, experienced developers, admins, support teams, partners, or non-technical users
- platform preference: Markdown, Docusaurus, ReadTheDocs, Mintlify, GitBook, static site, or repository docs
- style constraints: brand voice, terminology, localization, accessibility, and formatting rules
- code example needs: languages, runnable examples, SDK snippets, CLI examples, or sample repositories
- lifecycle needs: versioning, search, navigation, release notes, changelog, and deprecation policy

For a full documentation system, propose output artifacts such as:

- tutorial sequence or getting-started path
- how-to guide collection
- API or CLI reference pages
- explanation and concept articles
- troubleshooting section
- code examples or sample app repository
- navigation structure
- versioning and release-note structure

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

Before finishing, ask:

- Did I mix learning, doing, looking up, and explaining in one place?
- Did I write for the reader's actual state, not the author's mental model?
- Did I keep the document focused on one need?
- Did I avoid unnecessary structure at the top level?
- Did I leave room for linked companion documents?

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
