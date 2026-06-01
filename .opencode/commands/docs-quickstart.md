---
name: docs-quickstart
description: Draft a quickstart for a developer tool, SDK, or service. Use when the user wants the shortest path to first success for a new user.
---

You are running the diataxis-docs skill in quickstart mode.

A quickstart is a special form of tutorial: it optimizes for **first success**, not for completeness.

The user's input is below. It describes the product or tool that needs a quickstart.

## Input

$ARGUMENTS

## Task

1. Ask at most two short clarifying questions if the input is missing critical info: the install command, the smallest possible first success, and the runtime prerequisites. If the user already gave those, proceed.
2. Choose a single, opinionated path. No branches. No optional steps.
3. Keep the whole page short. Target under 80 lines of Markdown.
4. Show the expected output at every checkpoint.
5. End with a single sentence that links to the deeper tutorial.

## Output shape

```markdown
# Quickstart: <product or feature>

<one-sentence value statement>

## What you will build

<one-sentence description of the first success>

## Prerequisites

- <prereq>
- ...

## Steps

### 1. <step>

<command or code>

You should see:

<expected output>

### 2. <step>

...

## Next steps

<one-sentence link to the longer tutorial or how-to guide>
```

If the user asked for a longer tutorial, say so and offer to expand the quickstart into a full tutorial.
