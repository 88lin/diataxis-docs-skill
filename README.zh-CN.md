<div align="center">

# Diataxis Docs Skill

**一个可复用的 OpenCode Skill，用于写作以读者为先、结构清晰的技术文档。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill: OpenCode](https://img.shields.io/badge/Skill-OpenCode-111827)](SKILL.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb)](https://diataxis.fr/)
[![Templates: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a)](https://www.thegooddocsproject.dev/)
[![Evals: 32](https://img.shields.io/badge/Evals-32-blueviolet)](evals/evals.json)

[English](README.md) · [安装](docs/zh-CN/installation.md) · [斜杠命令](docs/zh-CN/commands.md) · [IDE 集成](docs/zh-CN/ide-integration.md) · [常见问题](docs/zh-CN/faq.md)

</div>

<p align="center">
  <img src="assets/preview.svg" alt="Diataxis 的四类文档形态" width="100%">
</p>

---

## 它解决什么问题

绝大多数文档问题其实是分类问题。一个页面同时要教会新手、指导熟练用户、罗列 API 字段、解释设计取舍，结果是四类读者都没被服务好。

这个 Skill 让 AI 助手在动笔之前先判断**需要写的是哪一类文档**，判断依据是 [Diataxis](https://diataxis.fr/) 罗盘：

| 如果内容… | …服务于用户的… | …那么它属于… |
| --- | --- | --- |
| 指导行动 | 技能获取 | 教程 Tutorial |
| 指导行动 | 技能应用 | 操作指南 How-to |
| 传递认知 | 技能应用 | 参考 Reference |
| 传递认知 | 技能获取 | 解释说明 Explanation |

判断完成后，Skill 会按该文体写作，并明确说明**哪些内容不该写进这一页**。决策树、各文体的反模式清单和质量检查项都在 [`SKILL.md`](SKILL.md)。

## 安装

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

也可以把 checkout 放在其他位置，再通过 `opencode.json` 注册：

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git ~/src/diataxis-docs
```

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["~/src/diataxis-docs"] }
}
```

`skills.paths` 会增加 OpenCode 扫描 Skill 的目录。无论采用哪种方式，存放 `SKILL.md` 的目录都**必须**命名为 `diataxis-docs`，与 Skill frontmatter 里的 `name` 一致。安装后重启 OpenCode。

Claude Code 的装法、验证步骤和排错见[安装 Skill](docs/zh-CN/installation.md)。

## 怎么用

直接用自然语言提问：

```text
把这份混乱的指南改写成 Diataxis 风格的文档。
把这个页面拆成教程、操作指南、参考和解释说明。
为我的 SDK 设计一套 Diataxis 文档体系。
审计我们的文档站，标出混合形态的页面。
```

也可以用斜杠命令进入特定模式：

| 命令 | 产出 |
| --- | --- |
| `/docs-classify` | 页面属于哪一类文体，以及混合形态信号 |
| `/docs-split` | 拆分方案，以及每个拆出页面的草稿 |
| `/docs-review` | 带严重级别标记的发布前审查意见 |
| `/docs-audit` | 对整个文档目录逐页分类 |
| `/docs-quickstart` | 一条通往首次成功的最短路径 |

完整输出结构见[斜杠命令](docs/zh-CN/commands.md)。

## 看它实际怎么工作

[`examples/messy-to-diataxis/`](examples/messy-to-diataxis/) 里有一个真实感的「快速开始」页面，它一页干了四件事；旁边是它应该被拆成的四个单一目的页面。

```text
拆分前  before.md                # 1 个页面，4 种任务

拆分后  after/01-tutorial.md     # 动手学会
        after/02-how-to.md       # 完成任务
        after/03-reference.md    # 查询事实
        after/04-explanation.md  # 理解原因
```

## 文档

| 页面 | 适用场景 |
| --- | --- |
| [安装 Skill](docs/zh-CN/installation.md) | 在 OpenCode 或 Claude Code 中加载它 |
| [斜杠命令](docs/zh-CN/commands.md) | 每个命令接收什么、返回什么 |
| [AI IDE 集成](docs/zh-CN/ide-integration.md) | 导出到 Cursor、Copilot、Aider 等 11 个助手 |
| [开发与贡献](docs/zh-CN/development.md) | 跑本地检查、新增评测项和斜杠命令 |
| [关于范围与设计的问题](docs/zh-CN/faq.md) | 它不做什么，以及为什么 |

Skill 按需加载的参考资料：各文档类型的[蓝图](references/doc-blueprints.md)、[读者分析清单](references/reader-analysis.md)、到 Good Docs Project 模板的[映射表](references/template-map.md)，以及[中文写作反模式](references/zh-cn-anti-patterns.md)。

## 在 OpenCode 之外使用

`SKILL.md` 是可移植的。导出脚本会把它写入另外 11 个助手各自读取的规则文件，并自动补上每个助手需要的 frontmatter：

```bash
python scripts/export_rules.py --list
python scripts/export_rules.py --target . --compact
```

12 个目标里有 9 个是常驻上下文，每次请求都会被加载，所以 `--compact` 很重要。详见 [AI IDE 集成](docs/zh-CN/ide-integration.md)。

## 设计原则

- **读者优先。** 围绕读者此刻想做的事来写。
- **一页只服务一种需求。** 不要把学习、操作、查询、思考混在一起。
- **用链接，不要堆砌。** 拆出配套文档，好过把一页写长。
- **结构服从目的。** 先定文档类型，再定标题层级。
- **它是指南，不是蓝图。** 从你现在所处的位置出发，一次走一步。

## 贡献

欢迎提 Issue 和 Pull Request。比修 bug 更大的改动，请先开 Issue 讨论。推送前先跑 `python scripts/check_local.py`，CI 跑的是同一条命令。

见 [CONTRIBUTING.md](CONTRIBUTING.md) 与[开发与贡献](docs/zh-CN/development.md)。

## 资料来源

本项目建立在 [Diataxis](https://diataxis.fr/) 和 [The Good Docs Project](https://www.thegooddocsproject.dev/) 的思想之上。本仓库不是二者的镜像或翻译，而是把它们提炼成一个可执行的 Skill。

## 许可证

MIT，见 [LICENSE](LICENSE)。
