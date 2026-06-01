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
​```bash
# exact command
​```
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

- Title that states the task
- Problem or goal
- Before you begin
- Steps
- Results or verification
- Troubleshooting or notes, if needed
- See also

Rules:

- One task per page.
- Assume competence.
- Keep the path short and practical.

## Reference blueprint

- Title
- Brief description
- Terminology or scope, if needed
- Structured entries or sections
- Tables, lists, or schemas
- Commands, flags, parameters, values, or limits
- Examples
- Related reference links

Rules:

- Be neutral.
- Describe only.
- Follow the structure of the thing described.

## Explanation blueprint

- Title that can be read as "About ..."
- Short overview
- Background
- Why it matters
- Conceptual discussion
- Alternatives or tradeoffs
- Implications
- Related topics

Rules:

- Explain the why.
- Connect ideas.
- Keep it bounded.

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
