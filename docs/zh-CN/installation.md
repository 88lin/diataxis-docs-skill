# 安装 Skill

本指南把 Diataxis Docs Skill 安装到 OpenCode 或 Claude Code，并验证宿主工具确实加载了它。

## 开始之前

你需要 `git`，以及下列宿主之一：

- OpenCode
- Claude Code

## 目录名必须正确

> **存放 `SKILL.md` 的目录必须命名为 `diataxis-docs`。**
>
> OpenCode 要求 frontmatter 里的 `name` 与所在目录名一致。本仓库叫 `diataxis-docs-skill`，而 Skill 名是 `diataxis-docs`。直接 `git clone` 会保留仓库名，Skill 因此无法加载——而且 OpenCode 和 Claude Code 都不会给出任何报错。下面每条命令都显式指定了目标目录，原因就在这里。

## 安装到 OpenCode

### 使用 OpenCode 默认扫描的 Skill 目录

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.config/opencode/skills/diataxis-docs
```

### 注册其他位置的 checkout

把仓库克隆到其他位置，同时确保目录名仍与 Skill 名一致：

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/src/diataxis-docs
```

把该目录加入对当前项目生效的 `opencode.json`：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/src/diataxis-docs"]
  }
}
```

`skills.paths` 是 OpenCode 支持的配置项，用于增加扫描 Skill 的目录。它适合把 checkout 放在默认 Skill 目录之外，但不会取消目录名要求。

无论采用哪种方式，完成后都要重启 OpenCode，让 Skill 列表重新加载。

## 安装到 Claude Code

Claude Code 从 `~/.claude/skills/<name>/` 加载 Skill，入口文件同样是 `SKILL.md`。

```bash
git clone https://github.com/88lin/diataxis-docs-skill.git \
  ~/.claude/skills/diataxis-docs
```

Claude Code 通常会自动发现新 Skill。如果这是你安装的第一个 Skill，或者 Skill 没有出现，重启它。

本仓库的 `.opencode/commands/` 目录存放的是 OpenCode 斜杠命令提示词。`SKILL.md` 里的 Skill 指令是可移植的，但斜杠命令的发现机制由宿主决定——见 [斜杠命令](commands.md)。

## 验证安装

先把 `SKILL_DIR` 设为实际安装位置，再确认目录名与 frontmatter 里的 name 一致：

```bash
SKILL_DIR=~/.config/opencode/skills/diataxis-docs
# 如果使用上面的 skills.paths 示例，则改为：SKILL_DIR=~/src/diataxis-docs
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

之后重启宿主工具。

## 卸载

```bash
rm -rf /path/to/diataxis-docs
```

如果通过 `skills.paths` 安装，还要从 `opencode.json` 中删除对应条目。

## 排查问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| Skill 从不触发 | 目录名不是 `diataxis-docs` | 重命名目录，然后重启宿主 |
| Skill 从不触发 | `skills.paths` 指向错误或不存在的目录 | 让它指向直接包含 `SKILL.md` 的 `diataxis-docs` checkout 目录，然后重启 OpenCode |
| Skill 从不触发 | 没有重启宿主 | 重启 OpenCode 或 Claude Code |
| 找不到 `SKILL.md` | clone 时多套了一层目录 | 该文件必须位于 `<skills 目录>/diataxis-docs/SKILL.md` |
| 斜杠命令不存在 | 宿主不读 `.opencode/commands/` | 改用自然语言提问，或把命令正文改写成宿主自己的命令格式 |

## 下一步

- [斜杠命令](commands.md)——内置的五个命令各自返回什么
- [AI IDE 集成](ide-integration.md)——把指导导出到 Cursor、Copilot、Claude Code 等工具
- [常见问题](faq.md)——适用范围、评测方式，以及它和通用写作助手的区别
