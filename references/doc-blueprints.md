# Documentation Blueprints

Use these as starting structures. Adapt them to the reader and the product, but do not mix document types unnecessarily.

## Tutorial blueprint

**Goal:** Make the user feel successful.

A Tutorial is a single linear path from "I have never done this" to "I just did this". Adapt the reader and the product, but do not introduce branches, alternatives, or deep explanation along the way.

````markdown
# [Action-oriented Title, e.g., Build your first X]

## Introduction
Briefly state what we will build or do. (Max 2 sentences).

## Prerequisites
- What they need installed.
- What prior knowledge is assumed.

## Step 1: [Action]
Clear instruction.
```bash
# exact command
```
*Expected output:* [Show exactly what they should see].

## Step 2: [Action]
...

## Summary
What we achieved. Link to the **How-to** for real-world variations.
````

Rules:

- Teach one path.
- Keep explanation minimal.
- Make success visible early.

## How-to blueprint

**Goal:** Help a competent reader complete one real task.

```markdown
# [Task-oriented title, e.g., Configure SAML single sign-on]

## Goal
State the task and the desired result in 1-2 sentences.

## Before you begin
- Required access, tools, accounts, or configuration.
- Assumed knowledge. Do not teach it here.

## Steps

### 1. [Action]
Do the next concrete action.

### 2. [Action]
Continue until the task is complete.

## Verify the result
Show how the reader knows the task worked.

## Troubleshooting
Only include issues that block this task. Link deeper explanations elsewhere.

## See also
- [Reference page]
- [Explanation page]
```

Rules:

- One task per page.
- Assume competence.
- Keep the path short and practical.
- Link concepts and reference data instead of teaching them inline.

## Reference blueprint

**Goal:** Let the reader look up exact facts quickly.

```markdown
# [Thing being described]

Brief neutral description of the thing and its scope.

## Syntax or shape
Show the command, object, endpoint, schema, or file format.

## Fields / parameters / options

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `<name>` | `<type>` | yes/no | Exact meaning. |

## Values and limits
List allowed values, defaults, limits, status codes, or constraints.

## Examples
Show minimal valid examples of input and output.

## Related reference
- [Related entry]
```

Rules:

- Be neutral.
- Describe only; do not instruct.
- Follow the structure of the thing described.
- Keep entries parallel and complete.

## Explanation blueprint

**Goal:** Help the reader understand one concept, design decision, or tradeoff.

```markdown
# About [concept]

## Overview
Frame the concept and why it matters.

## Background
Give only the context needed to understand this concept.

## How it works
Explain relationships, mechanisms, or mental models.

## Tradeoffs and alternatives
Compare approaches and explain the consequences.

## Implications
Say what this means for users, maintainers, or system design.

## Related topics
- [Tutorial, how-to, or reference link]
```

Rules:

- Explain the why.
- Connect ideas.
- Keep it bounded.
- Do not include step-by-step procedures.

## Quickstart blueprint

- Title
- What you will accomplish
- Audience
- Prerequisites
- Install or configure, if needed
- First success path
- Next steps

Rules:

- Optimize for first success.
- Avoid edge cases.
- Keep it short.

## README blueprint

- Project name
- Short project description
- Who it is for
- What problem it solves
- Key features or screenshots
- How to install or use
- Additional documentation
- Getting help
- Contributing
- License or terms

Rules:

- Make the first impression clear.
- Lead with why the project matters.

## Troubleshooting blueprint

- Title
- Problem overview
- Symptoms
- Likely causes
- Solutions
- Verification
- Related help

Rules:

- Organize by symptom and remedy.
- Keep it direct and short.

## Glossary blueprint

- Term
- Abbreviation
- Definition
- Source or note, if needed

Rules:

- Keep definitions concise.
- Prefer project-specific terms only.

## Release notes blueprint

- Title with version or date
- Short summary
- New features
- Improvements
- Bug fixes
- Known issues
- Deprecated features, if needed

Rules:

- Write for stakeholders.
- Say what changed and why it matters.
- Keep language plain.
