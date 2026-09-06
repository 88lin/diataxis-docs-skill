<div align="center">

<img src="assets/cover-zh.png" alt="Diataxis Docs Skill——基于 Diataxis 的技术文档写作、分类、拆分、审查技能" width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Hosts: Claude Code and OpenCode](https://img.shields.io/badge/Hosts-Claude%20Code%20%7C%20OpenCode-111827?style=flat-square)](docs/zh-CN/installation.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb?style=flat-square)](https://diataxis.fr/)
[![Templates: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a?style=flat-square)](https://www.thegooddocsproject.dev/)
[![Evals: 35](https://img.shields.io/badge/Evals-35-blueviolet?style=flat-square)](evals/evals.json)

**[English](README.md)** &nbsp;·&nbsp; [安装](docs/zh-CN/installation.md) &nbsp;·&nbsp; [斜杠命令](docs/zh-CN/commands.md) &nbsp;·&nbsp; [IDE 集成](docs/zh-CN/ide-integration.md) &nbsp;·&nbsp; [常见问题](docs/zh-CN/faq.md)

</div>

---

## 它解决什么问题

绝大多数文档问题其实是分类问题，而不是写作问题。

一个页面同时要教会新手、指导熟练用户、罗列 API 字段、解释设计取舍，结果是**四类读者都没被服务好**。文笔可以很好，页面依然是失败的。

这个 Skill 让 AI 助手在动笔之前，先判断*需要写的是哪一类文档*。

<table>
<tr><th align="left">如果内容…</th><th align="left">…服务于用户的…</th><th align="left">…那么它属于…</th></tr>
<tr><td>指导<b>行动</b></td><td>技能<b>获取</b></td><td>🎓 &nbsp;<b>教程</b> Tutorial</td></tr>
<tr><td>指导<b>行动</b></td><td>技能<b>应用</b></td><td>🔧 &nbsp;<b>操作指南</b> How-to</td></tr>
<tr><td>传递<b>认知</b></td><td>技能<b>应用</b></td><td>📖 &nbsp;<b>参考</b> Reference</td></tr>
<tr><td>传递<b>认知</b></td><td>技能<b>获取</b></td><td>💡 &nbsp;<b>解释说明</b> Explanation</td></tr>
</table>

判断完成后，Skill 会按该文体写作，并明确说明**哪些内容不该写进这一页**。决策树、各文体的反模式清单和质量检查项都在 [`SKILL.md`](SKILL.md)。

## 安装

<table>
<tr><td width="50%" valign="top">

**Claude Code**

```bash
git clone \
  https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

</td><td width="50%" valign="top">

**OpenCode**

```bash
git clone \
  https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

</td></tr>
</table>

> [!IMPORTANT]
> 存放 `SKILL.md` 的目录**必须**命名为 `diataxis-docs`，与 frontmatter 里的 `name` 一致——这也是上面两条命令都显式指定目标路径的原因。装好后重启宿主。

项目级安装、斜杠命令的复制步骤、验证与排错见 **[安装 Skill](docs/zh-CN/installation.md)**。

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
| :--- | :--- |
| `/docs-classify` | 页面属于哪一类文体，以及混合形态信号 |
| `/docs-split` | 拆分方案，以及每个拆出页面的草稿 |
| `/docs-review` | 带严重级别标记的发布前审查意见 |
| `/docs-audit` | 对整个文档目录逐页分类 |
| `/docs-quickstart` | 一条通往首次成功的最短路径 |

完整输出结构见 **[斜杠命令](docs/zh-CN/commands.md)**。

<details>
<summary><b>两个宿主都提供全部五个命令，但需要一次复制步骤</b></summary>

<br>

命令分别放在 `.claude/commands/` 和 `.opencode/commands/`。两个宿主都不会发现已安装 Skill *内部*嵌套的命令目录，所以要把它们复制到宿主自己的命令目录一次：

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md ~/.config/opencode/commands/
```

完整步骤、PowerShell 写法和项目级路径见 [安装 Skill](docs/zh-CN/installation.md)。

</details>

## 看它实际怎么工作

[`examples/messy-to-diataxis/`](examples/messy-to-diataxis/) 里有一个真实感的「快速开始」页面，它一页干了四件事；旁边是它应该被拆成的四个单一目的页面。

```text
拆分前   before.md                  1 个页面，4 种任务
           │
           ├──▶  after/01-tutorial.md      🎓  动手学会
拆分后     ├──▶  after/02-how-to.md        🔧  完成任务
           ├──▶  after/03-reference.md     📖  查询事实
           └──▶  after/04-explanation.md   💡  理解原因
```

## 文档

| 页面 | 适用场景 |
| :--- | :--- |
| **[安装 Skill](docs/zh-CN/installation.md)** | 在 Claude Code 或 OpenCode 中加载它 |
| **[斜杠命令](docs/zh-CN/commands.md)** | 每个命令接收什么、返回什么 |
| **[AI IDE 集成](docs/zh-CN/ide-integration.md)** | 导出到 Cursor、Copilot、Aider 等其他助手 |
| **[开发与贡献](docs/zh-CN/development.md)** | 跑本地检查、新增评测项和斜杠命令 |
| **[范围与设计的常见问题](docs/zh-CN/faq.md)** | 它不做什么，以及为什么 |

Skill **按需加载**的参考资料（不会进入每次请求）：

各文档类型的[蓝图](references/doc-blueprints.md) &nbsp;·&nbsp; [读者分析清单](references/reader-analysis.md) &nbsp;·&nbsp; 到 Good Docs Project 模板的[映射表](references/template-map.md) &nbsp;·&nbsp; [中文写作反模式](references/zh-cn-anti-patterns.md)

## 在其他助手中使用

`SKILL.md` 是可移植的。导出脚本会把它写入各个助手读取的规则文件，并自动补上该工具需要的 frontmatter：

```bash
python scripts/export_rules.py --list           # 查看所有目标
python scripts/export_rules.py --target . --compact
```

默认选中的 11 个目标里有 7 个会加载进项目的**每一次**请求，所以对它们来说 `--compact` 很重要——它只导出六个决策关键章节，而不是完整指南。详见 **[AI IDE 集成](docs/zh-CN/ide-integration.md)**。

## 设计原则

- **读者优先。** 围绕读者此刻想做的事来写。
- **一页只服务一种需求。** 不要把学习、操作、查询、思考混在一起。
- **用链接，不要堆砌。** 拆出配套文档，好过把一页写长。
- **结构服从目的。** 先定文档类型，再定标题层级。
- **它是指南，不是蓝图。** 从你现在所处的位置出发，一次走一步。

## 贡献

欢迎提 Issue 和 Pull Request。比修 bug 更大的改动，请先开 Issue 讨论。

```bash
python scripts/check_local.py    # CI 跑的是同一条命令
```

见 [CONTRIBUTING.md](CONTRIBUTING.md) 与[开发与贡献](docs/zh-CN/development.md)。

## 资料来源

本项目建立在 **[Diataxis](https://diataxis.fr/)** 和 **[The Good Docs Project](https://www.thegooddocsproject.dev/)** 的思想之上。本仓库不是二者的镜像或翻译，而是把它们提炼成一个可执行的 Skill。

<div align="center">

<br>

**MIT 许可证**——见 [LICENSE](LICENSE)

</div>
