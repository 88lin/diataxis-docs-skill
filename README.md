# Diataxis Docs Skill 📚

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs: Markdown](https://img.shields.io/badge/Docs-Markdown-000000)](#)

A reusable Opencode skill for writing clearer technical documentation with the Diataxis framework.

一个可复用的 Opencode 技能，用 Diataxis 框架把技术文档拆清楚、写明白、写好看。✨

## What this skill does / 这个技能能做什么

| Need | Diataxis form | What you get |
| --- | --- | --- |
| Learn by doing | Tutorial / 教程 | A guided learning experience |
| Finish a task | How-to / 操作指南 | Practical, task-focused directions |
| Look up facts | Reference / 参考文档 | Neutral, structured information |
| Understand why | Explanation / 解释说明 | Context, tradeoffs, and background |

It also provides reusable blueprints for common documentation types:

- Quickstart / 快速开始
- README
- Troubleshooting / 故障排查
- Glossary / 术语表
- Release notes / 发布说明
- Style guide / 风格指南

## Why it exists / 为什么要做这个仓库

English:

Most documentation problems are really classification problems. Users do not want a single mixed page that teaches, explains, lists facts, and solves errors all at once. They want the right kind of document for the job. This skill helps you classify the request first, then write with a tighter structure and less noise.

中文：

大多数文档问题，本质上都是“分类问题”。用户并不想要一页把教程、解释、参考信息和故障排查全混在一起的内容。他们想要的是“这件事最适合哪一种文档”。这个技能会先帮你判断文档类型，再按对应结构写作，让内容更清晰、更稳定，也更好维护。

## Included files / 包含内容

```text
.
├── SKILL.md
├── references/
│   ├── doc-blueprints.md
│   ├── reader-analysis.md
│   └── template-map.md
└── evals/
    └── evals.json
```

### `SKILL.md`

The main skill instructions: trigger guidance, classification logic, writing rules, and quality checks.

### `references/reader-analysis.md`

A short checklist for understanding who the reader is, what they need, and what should be left out.

### `references/doc-blueprints.md`

Reusable skeletons for tutorials, how-tos, reference docs, explanations, quickstarts, READMEs, troubleshooting pages, glossaries, and release notes.

### `references/template-map.md`

A compact map from Diataxis forms to common Good Docs Project templates.

### `evals/evals.json`

Sample prompts you can use to sanity-check whether the skill still behaves well over time.

## How to use / 如何使用

### Install / 安装

1. Clone or download this repository.
2. Place it where Opencode scans skills, or add the repo path to `skills.paths`.
3. Restart Opencode so the skill is loaded.

### Option 1: place it where Opencode already scans

If you keep the repo inside an Opencode skill directory, Opencode can discover it automatically.

### Option 2: add the repo path to `skills.paths`

```jsonc
{
  "skills": {
    "paths": ["C:/Users/Computer/.config/opencode/skills/diataxis-docs"]
  }
}
```

After saving config changes, restart Opencode so it reloads the skill list.

### Example prompts / 示例提问

- "Help me split this messy docs site into tutorial, how-to, reference, and explanation"
- "Write a README and quickstart for this tool"
- "Turn this API doc into a proper reference page"
- "Explain the difference between tutorial and how-to for my team"
- "帮我把这份文档拆成教程、操作指南、参考文档和解释文档"
- "帮我写一个好看的中英文 README"

## Source notes / 来源说明

This skill is inspired by:

- [Diataxis](https://diataxis.fr/)
- [The Good Docs Project](https://www.thegooddocsproject.dev/)

The linked study page mentioned during development could not be fetched in this session, so it is not mirrored here.

## Contributing / 贡献

Pull requests and issues are welcome.

If you improve the skill, please keep the writing style practical, reader-first, and tightly aligned with Diataxis.

## License / 许可证

MIT. See `LICENSE`.
