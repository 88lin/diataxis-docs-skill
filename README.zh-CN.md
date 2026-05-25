<div align="center">

# Diataxis Docs Skill 📚

**一个用于写作、重构和审查技术文档的 Opencode Skill。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill: Opencode](https://img.shields.io/badge/Skill-Opencode-111827)](SKILL.md)
[![Framework: Diataxis](https://img.shields.io/badge/Framework-Diataxis-2563eb)](https://diataxis.fr/)
[![Docs: Good Docs Project](https://img.shields.io/badge/Templates-Good%20Docs%20Project-16a34a)](https://www.thegooddocsproject.dev/)
[![GitHub stars](https://img.shields.io/github/stars/88lin/diataxis-docs-skill?style=social)](https://github.com/88lin/diataxis-docs-skill)

[英文文档](README.md) · [Skill 文件](SKILL.md) · [文档蓝图](references/doc-blueprints.md) · [模板映射](references/template-map.md)

</div>

---

## 预览

<p align="center">
  <img src="assets/preview.svg" alt="Diataxis Docs Skill 预览图" width="100%">
</p>

```text
用户需求                 Diataxis 文档类型        输出形态
──────────────────────────────────────────────────────────────
通过动手来学习           Tutorial / 教程          有引导的学习体验
完成一个真实任务         How-to / 操作指南        清晰、可执行的步骤
查询准确事实             Reference / 参考文档     表格、字段、参数、规则
理解背后的原因           Explanation / 解释说明   背景、取舍、设计原因
```

---

## 目录

- [为什么要做这个 Skill](#为什么要做这个-skill)
- [它能帮你做什么](#它能帮你做什么)
- [核心工作方式](#核心工作方式)
- [仓库结构](#仓库结构)
- [安装方式](#安装方式)
- [示例提问](#示例提问)
- [内置文档蓝图](#内置文档蓝图)
- [设计原则](#设计原则)
- [资料来源](#资料来源)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 为什么要做这个 Skill

很多技术文档的问题，不是“写得不够多”，而是“分类不清”。

一篇文档如果同时想完成这些目标，就很容易变得臃肿：

- 教新手入门
- 帮熟练用户完成任务
- 列出 API、字段、参数、命令
- 解释产品设计背后的原因
- 顺便处理故障排查

结果往往是：新手不知道从哪里开始，熟练用户找不到关键信息，维护者也不知道新增内容应该放在哪里。

这个 Skill 把 [Diataxis](https://diataxis.fr/) 框架沉淀成一个可复用的 AI 写作流程，让助手先判断“应该写哪一种文档”，再开始组织内容。

它的目标是：

- 先判断文档类型，再写正文
- 按读者当前状态写，而不是按作者脑子里的产品结构写
- 每一页只服务一个核心用户需求
- 把其它内容链接出去，而不是塞进同一篇文档
- 让文档系统长期更容易维护

---

## 它能帮你做什么

适合用于这些文档任务：

- 写教程
- 写操作指南
- 写参考文档
- 写解释说明或概念文档
- 写快速开始
- 写 README
- 写故障排查文档
- 写术语表
- 写发布说明
- 写文档风格指南

尤其适合这些场景：

- 你的文档里教程、说明、参数表、背景解释混在一起
- 你想给一个项目设计完整文档体系
- 你想把旧文档按 Diataxis 重新拆分
- 你想让 AI 写出来的文档更像“真正给用户用的文档”
- 你想复用一个稳定的文档写作框架，而不是每次重新提示 AI
- 你想为 SDK、API 或开发者门户设计完整文档体系

---

## 核心工作方式

这个 Skill 会先问两个问题：

1. 内容是在指导用户行动，还是帮助用户认知？
2. 用户是在学习技能，还是正在应用技能？

由此得到四种核心文档类型：

| 用户需求 | Diataxis 类型 | 典型问题 | 推荐写法 |
| --- | --- | --- | --- |
| 通过行动学习 | Tutorial / 教程 | “能不能带我学会？” | 像老师一样手把手引导 |
| 完成一个任务 | How-to / 操作指南 | “我该怎么做？” | 直接给可执行步骤 |
| 查询准确事实 | Reference / 参考文档 | “这个字段是什么意思？” | 表格、列表、参数、规则 |
| 建立理解 | Explanation / 解释说明 | “为什么这样设计？” | 讲背景、原因、取舍 |

然后它会根据文档类型套用不同写作规则和蓝图，避免把几种用户需求混写在一起。

---

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── assets/
│   └── preview.svg
├── references/
│   ├── doc-blueprints.md
│   ├── reader-analysis.md
│   └── template-map.md
└── evals/
    └── evals.json
```

### 关键文件说明

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | Skill 主体，包含触发说明、分类逻辑、写作规则和质量检查 |
| `references/reader-analysis.md` | 写作前的读者分析清单 |
| `references/doc-blueprints.md` | 教程、操作指南、参考文档、解释说明等文档骨架 |
| `references/template-map.md` | Diataxis 类型和 The Good Docs Project 模板的映射关系 |
| `evals/evals.json` | 用于检查 Skill 效果的示例提示词 |
| `assets/preview.svg` | GitHub 首页预览图 |

---

## 安装方式

### 方式一：克隆到 Opencode 技能目录

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git ~/.config/opencode/skills/diataxis-docs
```

克隆完成后，重启 Opencode，让它重新加载 Skill 列表。

### 方式二：在 `skills.paths` 里添加路径

在 `opencode.json` 中加入：

```jsonc
{
  "skills": {
    "paths": ["/path/to/diataxis-docs-skill"]
  }
}
```

保存后重启 Opencode。

---

## 示例提问

```text
帮我把这份混乱的产品文档拆成教程、操作指南、参考文档和解释说明。
```

```text
帮我给这个开发者工具写 README 和快速开始。
```

```text
把这个 API 页面改成真正的 reference 文档。
```

```text
审查这套文档，告诉我哪里混入了教程、说明、参考信息和故障排查。
```

```text
帮我把这套混乱的文档站拆成教程、操作指南、参考文档和解释说明。
```

---

## 内置文档蓝图

这个 Skill 内置了这些文档骨架：

| 文档蓝图 | 适用场景 |
| --- | --- |
| Tutorial / 教程 | 给用户一个可完成、可验证的学习路径 |
| How-to / 操作指南 | 帮用户完成一个真实任务 |
| Reference / 参考文档 | 字段、参数、命令、配置、API、限制、返回值 |
| Explanation / 解释说明 | 概念、背景、设计原因、替代方案、取舍 |
| Quickstart / 快速开始 | 帮用户尽快拿到第一次成功体验 |
| README | 项目的第一印象和入口页 |
| Troubleshooting / 故障排查 | 症状、原因、解决方案和验证方式 |
| Glossary / 术语表 | 项目特定术语和定义 |
| Release notes / 发布说明 | 面向用户的版本变化说明 |

对于更大的文档系统，它还可以帮助规划：

- SDK 入门路径
- API 或 CLI 参考文档结构
- 开发者门户导航
- 可运行代码示例需求
- 文档版本管理和发布说明结构
- Markdown、Docusaurus、ReadTheDocs、Mintlify、GitBook 或仓库文档等平台形态

---

## 设计原则

- 读者优先：先判断用户当前到底想完成什么。
- 一页一事：不要把学习、操作、查询和解释混在同一篇文档里。
- 链接而不是堆叠：相关但不同类型的内容应拆到配套文档中。
- 结构服从目的：先决定文档类型，再决定标题和章节。
- 实用优先：Diataxis 是工作工具，不是装饰性的术语。

---

## 资料来源

这个 Skill 主要参考和吸收了：

- [Diataxis](https://diataxis.fr/)
- [The Good Docs Project](https://www.thegooddocsproject.dev/)

本仓库没有镜像这些网站内容，而是把它们的核心思想整理成可复用的 Opencode Skill。

---

## 贡献

欢迎提交 issue 和 pull request。

如果你想提一个比较大的改动，建议先开 issue。这样更容易保持这个 Skill 的聚焦，不会被某一种文档风格带偏。

比较适合贡献的方向包括：

- 优化 `SKILL.md` 的触发描述
- 增加更好的文档蓝图
- 增加更真实的 eval 示例
- 补充实际文档改造案例
- 补充 SDK、API、开发者门户案例
- 改进中文或英文表达

请尽量保持风格：实用、读者优先、符合 Diataxis 的分类逻辑。

---

## 许可证

MIT。详见 [LICENSE](LICENSE)。
