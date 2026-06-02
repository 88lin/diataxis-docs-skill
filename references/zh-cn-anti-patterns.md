# Chinese Technical Documentation Anti-patterns

Use this reference only when reviewing Chinese technical documentation, Chinese localization drafts, or Chinese-first docs sites. Keep the main Diataxis decision in `SKILL.md` language-neutral; this file adds local smell signals.

## Common mixed-form signals

- A tutorial opens with several paragraphs of product vision, team history, or emotional preface before the first action.
- A tutorial embeds a large API parameter table instead of linking to reference documentation.
- A how-to starts with a long concept history before stating the task goal.
- A how-to mixes troubleshooting, background theory, and reference tables into the same flow.
- A reference page includes broad best-practice essays, personal recommendations, or implementation stories.
- An explanation article contains a full procedure that could be followed step by step.

## Practical review rule

Treat these as smell signals, not hard bans. When one appears, ask whether the content serves the same reader state as the page. If not, move it to a companion tutorial, how-to, reference, or explanation page and link to it.
