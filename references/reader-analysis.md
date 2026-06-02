# Reader Analysis Checklist

Use this before drafting any documentation.

## Questions to answer

1. Who is the reader?
2. What are they trying to do?
3. Are they learning or working?
4. What do they already know?
5. What do they need right now?
6. What should be left out of this document?
7. Which other document types should be linked instead of included?

## Reader states

- Learning: the reader is acquiring a skill and needs a guided experience.
- Working: the reader is applying a skill and needs practical help.
- Looking up: the reader needs a fact, value, rule, or limit.
- Reflecting: the reader wants context, tradeoffs, or background.

## Common signals

- New user questions usually point to tutorial or quickstart.
- Task completion questions usually point to how-to.
- Field, API, flag, or schema questions usually point to reference.
- Why and design questions usually point to explanation.


## Tutorial vs how-to fallback

When learning and working signals overlap, ask one short question before drafting:

> Is the reader trying to learn a new skill through a guided exercise, or complete a real task they already understand?

Use the answer this way:

- Guided exercise, first-time user, visible checkpoints -> tutorial or quickstart.
- Real task, known basics, production pressure -> how-to.
- Still unclear -> state the assumption and write a focused how-to, with tutorial or explanation links instead of inline teaching.

## Output rule

If the reader state is unclear, ask one short clarifying question before writing.
