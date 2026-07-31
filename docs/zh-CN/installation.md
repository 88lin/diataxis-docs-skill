# 安装 Skill

本指南把 Diataxis Docs Skill 安装到 OpenCode 或 Claude Code，并验证宿主工具确实加载了它。

## 开始之前

你需要 `git`，以及下列宿主之一：

- OpenCode
- Claude Code

## 目录名必须正确

> **存放 `SKILL.md` 的目录必须命名为 `diataxis-docs`。**
>
> OpenCode 要求 frontmatter 里的 `name` 与所在目录名一致。本仓库叫 `diataxis-docs-skill`，而 Skill 名是 `diataxis-docs`。直接 `git clone` 会保留仓库名，OpenCode 因此不会加载这个 Skill。下面每条命令都显式指定了目标目录，原因就在这里。

## 安装到 OpenCode

### 全局安装

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

### 只为一个项目安装

在项目根目录运行：

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  .opencode/skills/diataxis-docs
```

OpenCode 只会从文档列出的项目级和全局 Skill 目录发现 Skill，其中也包括兼容 Claude 和 Agent Skills 的目录。它不支持用 `skills.paths` 扫描任意 checkout。如果要把仓库保存在其他位置，请把它复制或链接到这些可发现目录之一。

无论采用哪种方式，完成后都要重启 OpenCode，让 Skill 列表重新加载。

### 安装斜杠命令

安装 Skill **不会**自动安装其中的五个斜杠命令。OpenCode 只从当前项目的 `.opencode/commands/` 或全局的 `~/.config/opencode/commands/` 发现命令，不会扫描已安装 Skill 内部嵌套的 `.opencode/commands/`。

采用上面的全局安装时：

```bash
mkdir -p ~/.config/opencode/commands
cp ~/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md \
  ~/.config/opencode/commands/
```

采用项目级安装时：

```bash
mkdir -p .opencode/commands
cp .opencode/skills/diataxis-docs/.opencode/commands/*.md \
  .opencode/commands/
```

PowerShell 用户可以这样全局安装命令：

```powershell
New-Item -ItemType Directory -Force "$HOME/.config/opencode/commands" | Out-Null
Copy-Item "$HOME/.config/opencode/skills/diataxis-docs/.opencode/commands/*.md" "$HOME/.config/opencode/commands/"
```

这里生成的是副本，所以更新 Skill 后要再次执行复制命令。如果你已经有同名的 `docs-*.md` 命令，请先检查再决定是否替换。

## 安装到 Claude Code

Claude Code 从 `~/.claude/skills/<name>/` 加载 Skill，入口文件同样是 `SKILL.md`。

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

Claude Code 通常会自动发现新 Skill。如果这是你安装的第一个 Skill，或者 Skill 没有出现，重启它。

`SKILL.md` 里的 Skill 指令是可移植的，但斜杠命令的发现机制由宿主决定。Claude Code 不会加载这些 OpenCode 命令——见 [斜杠命令](commands.md)。

## 验证安装

先把 `SKILL_DIR` 设为实际安装位置，再确认目录名与 frontmatter 里的 name 一致：

```bash
SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# 如果采用项目级安装，则改为：SKILL_DIR=.opencode/skills/diataxis-docs
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
git -C /path/to/diataxis-docs pull
```

之后重启宿主工具。如果复制过 OpenCode 斜杠命令，还要再次执行复制命令，让提示词与 Skill 保持同步。

## 卸载

```bash
rm -rf /path/to/diataxis-docs
```

如果复制过 OpenCode 斜杠命令，还要从命令目录删除这五个 `docs-*.md` 文件；删除前先确认它们确实是由本 Skill 复制过去的版本。

## 排查问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| Skill 从不触发 | 目录名不是 `diataxis-docs` | 重命名目录，然后重启宿主 |
| Skill 从不触发 | 没有重启宿主 | 重启 OpenCode 或 Claude Code |
| 找不到 `SKILL.md` | clone 时多套了一层目录 | 该文件必须位于 `<skills 目录>/diataxis-docs/SKILL.md` |
| OpenCode 中没有斜杠命令 | Skill checkout 内部嵌套的 `.opencode/commands/` 不是命令发现目录 | 把文件复制到项目的 `.opencode/commands/` 或全局 `~/.config/opencode/commands/`，然后重启 OpenCode |
| 更新后斜杠命令仍是旧版本 | 安装的命令文件是副本 | 拉取 Skill 更新后，再执行一次命令复制步骤 |
| 其他宿主中没有斜杠命令 | 命令发现机制由宿主决定 | 改用自然语言提问，或把命令正文改写成该宿主自己的命令格式 |

## 下一步

- [斜杠命令](commands.md)——内置的五个命令各自返回什么
- [AI IDE 集成](ide-integration.md)——把指导导出到 Cursor、Copilot、Claude Code 等工具
- [常见问题](faq.md)——适用范围、评测方式，以及它和通用写作助手的区别
