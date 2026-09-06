<div align="center">

<img src="assets/cover-zh.png" alt="Diataxis Docs Skill——基于 Diataxis 的技术文档写作、分类、拆分、审查技能" width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Hosts: any agent that reads SKILL.md](https://img.shields.io/badge/%E5%AE%BF%E4%B8%BB-%E4%BB%BB%E4%BD%95%E8%AF%BB%E5%8F%96%20SKILL.md%20%E7%9A%84%20Agent-111827?style=flat-square)](docs/zh-CN/installation.md)
[![Assistants: 12](https://img.shields.io/badge/%E6%94%AF%E6%8C%81%E5%8A%A9%E6%89%8B-12%20%E4%B8%AA-0ea5e9?style=flat-square)](docs/zh-CN/ide-integration.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb?style=flat-square)](https://diataxis.fr/)
[![Evals: 35](https://img.shields.io/badge/Evals-35-blueviolet?style=flat-square)](evals/evals.json)

**[English](README.md)** &nbsp;·&nbsp; [安装](#安装) &nbsp;·&nbsp; [它能做什么](#它到底做什么) &nbsp;·&nbsp; [命令](#斜杠命令) &nbsp;·&nbsp; [文档](docs/zh-CN/installation.md)

</div>

---

## 大多数文档问题，其实是分类问题

一个页面同时要教会新手、指导熟练用户、罗列 API 字段、解释设计取舍，结果是**四类读者都没被服务好**。新手找不到那节课；熟练用户找不到操作步骤；专家找不到他要查的那个字段；维护者不知道新内容该放哪里。

文笔可以很好，页面依然是失败的。

这个 Skill 让 AI 助手在动笔之前，先判断*需要写的是哪一类文档*。

## 它到底做什么

给它一个身兼四职的页面。它会告诉你这一页本该是哪四份文档，并把每一份都写出来。

```text
输入    《QuokkaDB 快速开始》 ── 一个页面，四种任务

        ├─ 简介 ...................... 💡 解释说明
        ├─ 我们为什么做 QuokkaDB ..... 💡 解释说明
        ├─ 快速安装与首次连接 ........ 🎓 教程
        │    └─ 刚才发生了什么 ....... 💡 解释说明  ← 放错了页面
        ├─ 常见任务 .................. 🔧 操作指南
        ├─ 参考 ...................... 📖 参考
        ├─ 排查问题 .................. 🔧 操作指南
        └─ 下一步 .................... ·  链接堆，不属于任何文体

输出    4 个单一目的的页面
        🎓  教程：你的第一个 QuokkaDB 程序
              你将做出什么 · 前置条件 · 步骤
              刚才发生了什么 · 下一步去哪
        🔧  操作指南：配置 QuokkaDB 连接
              目标 · 步骤 · 执行事务 · 结果 · 延伸阅读
        📖  参考：QuokkaDB Python 客户端
              连接参数 · 函数 · 错误码 · 限制
        💡  解释说明：QuokkaDB 为什么选 LSM-tree 引擎
              起因 · 为什么要 ACID · 为什么选 LSM-tree · 对用户的影响
```

这是一个真实跑出来的示例，不是示意图——拆分前后的页面都在 [`examples/messy-to-diataxis/`](examples/messy-to-diataxis/)。

更关键的是，它还会说明**每一页不该写什么**。一份教程一旦长出「背景介绍」章节，它就不再是教程了。

## 它怎么判断

两个问题，四种答案。这就是 Diataxis 罗盘：

<table>
<tr><th align="left">如果内容…</th><th align="left">…服务于用户的…</th><th align="left">…那么它属于…</th></tr>
<tr><td>指导<b>行动</b></td><td>技能<b>获取</b></td><td>🎓 &nbsp;<b>教程</b> Tutorial</td></tr>
<tr><td>指导<b>行动</b></td><td>技能<b>应用</b></td><td>🔧 &nbsp;<b>操作指南</b> How-to</td></tr>
<tr><td>传递<b>认知</b></td><td>技能<b>应用</b></td><td>📖 &nbsp;<b>参考</b> Reference</td></tr>
<tr><td>传递<b>认知</b></td><td>技能<b>获取</b></td><td>💡 &nbsp;<b>解释说明</b> Explanation</td></tr>
</table>

写的时候，每种文体还各有一套规则：

| 文体 | 读者在 | 必须有 | **不能**有 |
| :--- | :--- | :--- | :--- |
| 🎓 教程 | 学习 | 一条线性路径、看得见的结果、明确的前置条件 | 分支、可选项、大段背景 |
| 🔧 操作指南 | 干活 | 单一目标、简短序列、一个验证步骤 | 教学、概念铺垫 |
| 📖 参考 | 查阅 | 结构与被描述对象一致、精确取值 | 操作指令、推荐做法、模糊表述 |
| 💡 解释说明 | 思考 | 一个有边界的话题、明确观点、取舍分析 | 操作流程、「怎么做」的写法 |

完整决策树、各文体的反模式清单和质量检查项都在 [`SKILL.md`](SKILL.md)。

## 安装

挑符合你情况的那一列。三种方式最终效果相同。

<table>
<tr>
<td width="33%" valign="top">

### 🗣️ &nbsp;交给 Agent 一句话

*最适合新手，零前置条件。*

把下面这段粘贴给 Claude Code、OpenCode 或 Codex：

```text
把这个 Skill 安装到我的全局
skills 目录：
github.com/88lin/diataxis-docs-skill
存放 SKILL.md 的目录必须命名为
diataxis-docs，不要用仓库名。
装完告诉我你用的是哪个路径。
```

</td>
<td width="33%" valign="top">

### 📦 &nbsp;`skills` CLI

*适合一次装进多个 Agent，需要 Node.js。*

```bash
npx skills add \
  88lin/diataxis-docs-skill
```

它会检测你装了哪些 Agent，并写入各自正确的目录。跳过交互：

```bash
npx skills add \
  88lin/diataxis-docs-skill \
  --skill diataxis-docs \
  --agent claude-code -g -y
```

</td>
<td width="33%" valign="top">

### 🧬 &nbsp;`git clone`

*适合自己固定一份 checkout，需要 git。*

```bash
U=88lin/diataxis-docs-skill

# Claude Code
git clone https://github.com/$U \
  ~/.claude/skills/diataxis-docs

# OpenCode
git clone https://github.com/$U \
  ~/.config/opencode/skills/diataxis-docs

# Codex
git clone https://github.com/$U \
  ~/.codex/skills/diataxis-docs
```

</td>
</tr>
</table>

> [!IMPORTANT]
> 存放 `SKILL.md` 的目录**必须**命名为 `diataxis-docs`，与 frontmatter 里的 `name` 一致。前两种方式会自动处理好；clone 命令显式指定目标路径，原因就在这里。装好后重启宿主。

项目级安装、可选的斜杠命令复制步骤、验证与排错见 **[安装 Skill](docs/zh-CN/installation.md)**。

## 哪些助手能用

<table>
<tr><th align="left" width="34%">原生加载 <code>SKILL.md</code></th><th align="left" width="66%">读取导出的规则文件</th></tr>
<tr valign="top"><td>

**Claude Code**<br>
**OpenCode**<br>
**Codex**

按需加载：与文档无关的请求上成本为零。

</td><td>

Cursor &nbsp;·&nbsp; GitHub Copilot &nbsp;·&nbsp; Cline &nbsp;·&nbsp; Roo Code &nbsp;·&nbsp; Windsurf &nbsp;·&nbsp; Aider &nbsp;·&nbsp; Gemini CLI &nbsp;·&nbsp; Continue &nbsp;·&nbsp; Amazon Q

```bash
python scripts/export_rules.py --list
python scripts/export_rules.py --target . --compact
```

导出脚本把 `SKILL.md` 写到各工具实际读取的路径，并补上它需要的 frontmatter。默认目标里有 6 个属于常驻上下文，这正是 `--compact` 的用途。

</td></tr>
</table>

完整目标表和各工具注意事项见 **[AI IDE 集成](docs/zh-CN/ide-integration.md)**。

## 怎么用

直接用自然语言提问，不需要命令：

```text
把这份混乱的指南改写成 Diataxis 风格的文档。
把这个页面拆成教程、操作指南、参考和解释说明。
为我的 SDK 设计一套 Diataxis 文档体系。
审计我们的文档站，标出混合形态的页面。
```

### 斜杠命令

可选的快捷入口，用于直接进入某种模式，目前提供给 Claude Code 和 OpenCode：

| 命令 | 产出 |
| :--- | :--- |
| `/docs-classify` | 页面属于哪一类文体，以及混合形态信号 |
| `/docs-split` | 拆分方案，以及每个拆出页面的草稿 |
| `/docs-review` | 带严重级别标记的发布前审查意见 |
| `/docs-audit` | 对整个文档目录逐页分类 |
| `/docs-quickstart` | 一条通往首次成功的最短路径 |

完整输出结构见 **[斜杠命令](docs/zh-CN/commands.md)**。

<details>
<summary><b>这些命令是可选的，且需要一次复制步骤</b></summary>

<br>

不装它们，Skill 照样能通过自然语言工作。如果你想用，注意 Claude Code 和 OpenCode 都不会发现已安装 Skill *内部*嵌套的命令目录，所以要把它们复制到宿主自己的命令目录一次：

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

Codex 没有内置命令——改用自然语言描述模式即可。

完整步骤、PowerShell 写法和项目级路径见 [安装 Skill](docs/zh-CN/installation.md)。

## 哪些助手能用

**原生加载 `SKILL.md`**——按需触发，与文档无关的请求上成本为零：**Claude Code**、**OpenCode**、**Codex**。

**读取导出的规则文件**——Cursor、GitHub Copilot、Cline、Roo Code、Windsurf、Aider、Gemini CLI、Continue、Amazon Q：

```bash
python scripts/export_rules.py --list             # 查看全部 14 个目标
python scripts/export_rules.py --target . --compact
```

导出脚本把 `SKILL.md` 写到各工具实际读取的路径，并补上它需要的 frontmatter。默认目标里有 6 个属于常驻上下文——会被拼接到项目的**每一次**请求前面，每个约 3,500 tokens——这正是 `--compact` 的用途：它只导出六个决策关键章节，约 2,100 tokens。

各工具注意事项和完整目标表见 **[AI IDE 集成](docs/zh-CN/ide-integration.md)**。

## 还附带了什么

- **一个混合形态扫描器。** `python scripts/audit_docs.py docs/` 会按代码块、表格行、步骤行和解释性词汇给每个页面打分，标出值得人工过一眼的那些。大型站点在花模型 token 之前，可以先用它做筛查。
- **按需加载的参考资料**，不会进入每次请求：各文档类型的[蓝图](references/doc-blueprints.md)、[读者分析清单](references/reader-analysis.md)、到 Good Docs Project 模板的[映射表](references/template-map.md)，以及[中文写作反模式](references/zh-cn-anti-patterns.md)。
- **35 条评测**，覆盖 13 个类别，见 [`evals/evals.json`](evals/evals.json)，其中包含故意设置的「不应触发」用例——遇到与文档结构无关的请求，这个 Skill 应该保持安静。

## 文档

| 页面 | 适用场景 |
| :--- | :--- |
| **[安装 Skill](docs/zh-CN/installation.md)** | 三种安装方式、各宿主路径、安装验证 |
| **[斜杠命令](docs/zh-CN/commands.md)** | 每个命令接收什么、返回什么 |
| **[AI IDE 集成](docs/zh-CN/ide-integration.md)** | 导出到 Cursor、Copilot、Aider 等其他助手 |
| **[开发与贡献](docs/zh-CN/development.md)** | 跑本地检查、新增评测项和斜杠命令 |
| **[范围与设计的常见问题](docs/zh-CN/faq.md)** | 它不做什么，以及为什么 |

Skill **按需加载**的参考资料（不会进入每次请求）：

各文档类型的[蓝图](references/doc-blueprints.md) &nbsp;·&nbsp; [读者分析清单](references/reader-analysis.md) &nbsp;·&nbsp; 到 Good Docs Project 模板的[映射表](references/template-map.md) &nbsp;·&nbsp; [中文写作反模式](references/zh-cn-anti-patterns.md)

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
