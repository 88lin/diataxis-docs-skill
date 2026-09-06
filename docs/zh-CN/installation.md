# 安装 Skill

本指南把 Diataxis Docs Skill 安装到能读取 `SKILL.md` 的 AI 助手里，并验证宿主确实加载了它。

三种方式，按上手门槛从低到高排列：

| 方式 | 适合谁 | 前置条件 |
| --- | --- | --- |
| [交给 Agent 一句话](#方式-1交给-agent-一句话) | 所有人，包括第一次装 Skill | 只需要你已经在用的 Agent |
| [`skills` CLI](#方式-2skills-cli) | 想一次装进多个 Agent | Node.js |
| [`git clone`](#方式-3git-clone) | 想自己固定并管理一份 checkout | `git` |

## 支持哪些宿主

`SKILL.md` 本身是可移植的。任何支持 Skill 发现机制的 Agent 都能加载它。

| 宿主 | 全局 Skill 目录 | 项目级 Skill 目录 | 斜杠命令 |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | 已内置，需[一次复制](#安装斜杠命令) |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` 或 `.agents/skills/` | 已内置，需[一次复制](#安装斜杠命令) |
| Codex | `~/.codex/skills/` | `.agents/skills/` | 未内置——直接用自然语言 |

其他工具——Cursor、Copilot、Cline、Windsurf、Aider、Gemini CLI、Amazon Q、Continue、Roo Code——读的是规则文件，不是 Skill。请改用导出方式，见 [AI IDE 集成](ide-integration.md)。

## 目录名必须正确

> **存放 `SKILL.md` 的目录必须命名为 `diataxis-docs`。**
>
> 宿主要求 frontmatter 里的 `name` 与所在目录名一致。本仓库叫 `diataxis-docs-skill`，而 Skill 名是 `diataxis-docs`。直接 `git clone` 会保留仓库名，Skill 因此不会被加载。
>
> 方式 1 和方式 2 会自动处理好这一点。方式 3 的每条命令都显式指定目标目录，原因就在这里。

## 方式 1：交给 Agent 一句话

把下面这段话粘贴给 Claude Code、OpenCode 或 Codex。除了 Agent 本身，不需要任何前置条件。

```text
把 https://github.com/88lin/diataxis-docs-skill 这个 Skill 安装到我的全局
skills 目录。存放 SKILL.md 的目录必须命名为 diataxis-docs，不要用仓库名。
装完告诉我你用的是哪个路径。
```

Agent 会根据自己所处的宿主选择正确的目录。它报出路径后，去[验证安装](#验证安装)。

如果你的 Agent 不能执行 shell 命令，请改用其他两种方式。

## 方式 2：`skills` CLI

[`skills`](https://github.com/vercel-labs/skills) 是 Agent Skill 的包管理器。它会检测你装了哪些 Agent，并写入各自正确的目录。

```bash
npx skills add 88lin/diataxis-docs-skill
```

它会依次询问要装哪个 Skill、装到哪些 Agent。想跳过交互：

```bash
# 全局安装，指定单个 Agent
npx skills add 88lin/diataxis-docs-skill --skill diataxis-docs --agent claude-code -g -y

# 项目级安装，一次装进多个 Agent
npx skills add 88lin/diataxis-docs-skill --skill diataxis-docs \
  --agent claude-code --agent codex --agent opencode -y
```

常用参数：

| 参数 | 作用 |
| --- | --- |
| `-g`、`--global` | 装到全局目录，而不是当前项目 |
| `-a`、`--agent` | 指定一个 Agent，可重复。取值如 `claude-code`、`codex`、`opencode` |
| `-s`、`--skill` | 按名字安装单个 Skill。本仓库提供的是 `diataxis-docs` |
| `-l`、`--list` | 只列出仓库里有什么，不安装 |
| `--copy` | 用复制代替符号链接 |
| `-y`、`--yes` | 全部接受默认值 |

默认安装方式是指向同一份副本的符号链接，所以 `npx skills update diataxis-docs` 能一次更新所有 Agent。符号链接不方便的环境（例如未开启开发者模式的 Windows）请加 `--copy`。

卸载：`npx skills remove diataxis-docs`。

## 方式 3：`git clone`

直接 clone 到宿主的 Skill 目录，并把目标目录名指定为 `diataxis-docs`。

**Claude Code**

```bash
# 全局
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs

# 只为一个项目，在项目根目录运行
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .claude/skills/diataxis-docs
```

**OpenCode**

```bash
# 全局
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs

# 只为一个项目，在项目根目录运行
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .opencode/skills/diataxis-docs
```

OpenCode 只会从文档列出的项目级和全局 Skill 目录发现 Skill，其中也包括兼容 Claude 和 Agent Skills 的目录。它不支持用 `skills.paths` 扫描任意 checkout。如果要把仓库保存在其他位置，请把它复制或链接到这些可发现目录之一。

**Codex**

```bash
# 全局
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.codex/skills/diataxis-docs

# 只为一个项目，在项目根目录运行
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .agents/skills/diataxis-docs
```

Codex 的全局目录取自 `$CODEX_HOME/skills`；未设置 `CODEX_HOME` 时回退到 `~/.codex/skills`。

以上任何一种方式装完都要重启宿主，让 Skill 列表重新加载。Claude Code 通常会自动发现新 Skill，但如果这是你装的第一个 Skill、或者 Skill 没出现，请重启它。

## 安装斜杠命令

这五个命令是可选的。不装它们，Skill 照样能通过自然语言工作；它们的作用是直接进入某种特定模式。

Claude Code 和 OpenCode 都只从自己的命令目录发现命令，都不会扫描已安装 Skill *内部*嵌套的命令目录。所以要把文件复制出来一次：

```bash
# Claude Code
mkdir -p ~/.claude/commands
cp ~/.claude/skills/diataxis-docs/.claude/commands/*.md ~/.claude/commands/

# OpenCode
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

采用项目级安装时，去掉 `~/` 前缀：

```bash
mkdir -p .claude/commands
cp .claude/skills/diataxis-docs/.claude/commands/*.md .claude/commands/
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/commands" | Out-Null
Copy-Item "$HOME/.claude/skills/diataxis-docs/.claude/commands/*.md" "$HOME/.claude/commands/"
```

如果你是用 `skills` CLI 装的，请相应调整源路径——`npx skills list` 会打印每个 Skill 的实际位置。

装好的命令是副本，所以更新 Skill 后要再执行一次复制。如果你已经有同名的 `docs-*.md` 命令，请先检查再决定是否替换。

Codex 没有内置命令。改用自然语言描述模式即可，例如「判断这个页面的类型，并指出混合形态」。

## 验证安装

先把 `SKILL_DIR` 设为实际安装位置，再确认目录名与 frontmatter 里的 name 一致：

```bash
SKILL_DIR=~/.claude/skills/diataxis-docs
# OpenCode 全局：SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# Codex 全局：   SKILL_DIR=~/.codex/skills/diataxis-docs
# 项目级安装：   SKILL_DIR=.claude/skills/diataxis-docs
basename "$SKILL_DIR"
head -2 "$SKILL_DIR/SKILL.md"
```

第一条命令必须输出 `diataxis-docs`；第二条必须输出 `---`，然后是 `name: diataxis-docs`。如果两个名称不同，重命名目录。

然后向助手提一个应当触发 Skill 的问题：

```text
帮我判断这个文档页面属于哪一类，应该写成什么类型的文档。
```

Skill 已加载时，回答会给出一个 Diataxis 文档类型——教程、操作指南、参考或解释说明——并说明这个页面应该排除哪些内容。如果得到的是泛泛的写作建议，说明 Skill 没有加载。

## 更新

```bash
npx skills update diataxis-docs      # skills CLI
git -C /path/to/diataxis-docs pull   # git clone
```

之后重启宿主。如果复制过斜杠命令，还要再执行一次复制，让提示词与 Skill 保持同步。

## 卸载

```bash
npx skills remove diataxis-docs      # skills CLI
rm -rf /path/to/diataxis-docs        # git clone
```

如果复制过斜杠命令，还要从命令目录删除这五个 `docs-*.md` 文件；删除前先确认它们确实是由本 Skill 复制过去的版本。

## 排查问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| Skill 从不触发 | 目录名不是 `diataxis-docs` | 重命名目录，然后重启宿主 |
| Skill 从不触发 | 没有重启宿主 | 重启宿主 |
| 找不到 `SKILL.md` | clone 时多套了一层目录 | 该文件必须位于 `<skills 目录>/diataxis-docs/SKILL.md` |
| `npx skills` 装错了 Agent | 自动检测发现了多个 | 显式指定：`--agent claude-code` |
| 符号链接失效或被忽略 | 文件系统或宿主不跟随符号链接 | 加 `--copy` 重新安装 |
| 没有斜杠命令 | Skill checkout 内部嵌套的命令目录不是宿主的命令发现目录 | 把文件复制到宿主的项目级或全局命令目录，然后重启 |
| 更新后斜杠命令仍是旧版本 | 装好的命令文件是副本 | 更新后再执行一次命令复制 |
| Codex 或其他宿主里没有斜杠命令 | 命令发现机制由宿主决定 | 改用自然语言提问，或把命令正文改写成该宿主的命令格式 |

## 下一步

- [斜杠命令](commands.md)——内置的五个命令各自返回什么
- [AI IDE 集成](ide-integration.md)——把指导导出到 Cursor、Copilot 等工具
- [常见问题](faq.md)——适用范围、评测方式，以及它和通用写作助手的区别
