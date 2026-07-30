# Diataxis and TGDP Template Map

Use this as a compact mapping when choosing document types.

## Diataxis core forms

| Need | Form | Typical question | Writing mode |
| --- | --- | --- | --- |
| Learn by doing | Tutorial | Can you show me how to learn this? | Guided lesson |
| Do a task | How-to | How do I do X? | Practical directions |
| Look up facts | Reference | What is this field/flag/API? | Neutral description |
| Understand a topic | Explanation | Why is this designed this way? | Discursive context |

## Common TGDP template mappings

| Template | Closest Diataxis form | Notes |
| --- | --- | --- |
| Tutorial | Tutorial | Learning-oriented, hands-on |
| How-to | How-to | Goal-oriented, task-based |
| Reference | Reference | Concise, structured facts |
| Concept | Explanation | Context, background, definitions |
| Quickstart | Tutorial | Short first-success path |
| README | Mixed entry point | Often combines overview, orientation, and links to the four forms |
| Troubleshooting | How-to + reference | Symptom, cause, solution; keep it focused on problem resolution |
| Glossary | Reference | Terms and definitions |
| Release notes | Reference with user-facing framing | Changes, benefits, issues, links |
| Style guide | Meta-document | Rules for consistent writing across the system |

## Artifact to compass cell

Use this when planning a larger documentation set. Do not treat it as a backlog; only produce what the compass calls for.

| Artifact | Compass cell | Purpose |
| --- | --- | --- |
| Getting started path or quickstart | action + acquisition (tutorial) | First success for a new user |
| How-to guide collection | action + application (how-to) | One task per page, assumes competence |
| API, CLI, config, or schema reference | cognition + application (reference) | Neutral, structured facts |
| Concept, architecture, and design articles | cognition + acquisition (explanation) | Why and how it works, tradeoffs |
| Troubleshooting | action + application (how-to) | Symptom, cause, solution |
| Glossary | cognition + application (reference) | Project-specific terms |
| Release notes and changelog | cognition + application (reference) | What changed and why it matters |
| Style guide | meta | Team rules for consistent writing |
| Sample apps and runnable examples | action + acquisition (tutorial) or cognition + application (reference) | Validate the system end to end |

## Editing rule

If a section is drifting into a different need, move it to the matching document type instead of expanding the current document.
