## What

A one-sentence summary of the change.

## Why

Link the issue or eval that motivated the change. If there is no issue, explain the user-visible benefit in two or three sentences.

## How

A short walkthrough of what you changed and why. Mention any new eval added, any section of `SKILL.md` rewritten, or any template created.

## Validation

- [ ] `python scripts/check_local.py` passes locally
- [ ] CI passes (push the branch and check the Actions tab)
- [ ] Bilingual parity: if you changed `README.md`, the matching change is in `README.zh-CN.md`
- [ ] If you added an eval, the category is on the whitelist in `CONTRIBUTING.md` and the `files` field is populated (or `[]` for `non-trigger`)
- [ ] If you bumped the skill version, all three of `SKILL.md`, `evals/evals.json`, and `CHANGELOG.md` were updated

## Notes for the reviewer

Anything that needs a second pair of eyes: trade-offs, open questions, screenshots.
