# 把指导导出到其他 AI 助手

本仓库以 OpenCode Skill 的形式打包，但 `SKILL.md` 里的指导是可移植的。[`scripts/export_rules.py`](../../scripts/export_rules.py) 会把它写到各个助手实际读取的规则文件路径，并补上该工具需要的 frontmatter。

## 开始之前

先读 [上下文成本](#上下文成本)。13 个目标里有 10 个会注入到项目的每一次请求，完整指导每次约 5,200 tokens。

## 列出所有目标

```bash
python scripts/export_rules.py --list
```

覆盖 11 个助手的 13 个规则文件：

| Key | 工具 | 路径 | 常驻 |
| --- | --- | --- | --- |
| `cursor` | Cursor | `.cursor/rules/diataxis.mdc` | 否 |
| `cursor-legacy` | Cursor（旧格式） | `.cursorrules` | 是 |
| `cline` | Cline | `.clinerules` | 是 |
| `roo` | Roo Code | `.roo/rules/diataxis.md` | 是 |
| `windsurf` | Windsurf | `.windsurf/rules/diataxis.md` | 否 |
| `windsurf-legacy` | Windsurf（旧格式） | `.windsurfrules` | 是 |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | 是 |
| `claude` | Claude Code | `CLAUDE.md` | 是 |
| `codex` | OpenAI Codex | `AGENTS.md` | 是 |
| `aider` | Aider | `CONVENTIONS.md` | 是 |
| `gemini` | Gemini CLI | `GEMINI.md` | 是 |
| `continue` | Continue | `.continue/rules/diataxis.md` | 否 |
| `amazonq` | Amazon Q Developer | `.amazonq/rules/diataxis.md` | 是 |

## 先预览再写入

`--dry-run` 只报告会发生什么，不写任何文件：

```bash
python /path/to/diataxis-docs-skill/scripts/export_rules.py --target . --dry-run
```

## 导出

在需要接收规则文件的项目里运行，或者用 `--target` 指向它：

```bash
# 全部导出到当前项目
python /path/to/diataxis-docs-skill/scripts/export_rules.py

# 只导出团队在用的工具，并使用精简版
python /path/to/diataxis-docs-skill/scripts/export_rules.py --only claude --only cursor --compact
```

除非加 `--force`，否则已存在的文件不会被覆盖。

## 选项

| 选项 | 作用 |
| --- | --- |
| `--target DIR` | 导出到哪个项目，默认当前目录 |
| `--only KEY` | 只导出一个目标，可重复使用 |
| `--list` | 打印目标表格后退出 |
| `--dry-run` | 只报告将要写入的内容，不触碰文件系统 |
| `--force` | 覆盖已存在的规则文件 |
| `--compact` | 只导出五个章节，而不是完整指导 |

## 上下文成本

常驻规则文件会被拼接到该项目的每一次请求前面。完整指导约 20,900 字符，每次请求约 5,200 tokens。

`--compact` 只导出罗盘、快速决策树、不适用场景清单、反模式和质量检查——约 9,400 字符，约 2,300 tokens。这些内容足以让助手正确判定请求类型并避开常见的失败模式。

对三个按需加载的目标（`cursor`、`windsurf`、`continue`）用完整导出，其余用 `--compact`。

## 各工具注意事项

**Cursor.** 项目规则必须使用 `.mdc` 扩展名；放在 `.cursor/rules` 里的普通 `.md` 文件会被规则系统忽略。脚本写入的是 `.cursor/rules/diataxis.mdc`，并带上 `description` 和 `alwaysApply: false`，让它成为一条 agent-requested 规则：Cursor 读取 description，在任务看起来与文档相关时把规则拉进来。不要同时启用旧的 `.cursorrules` 目标。

**Windsurf.** workspace 规则单文件上限 12,000 字符。完整指导超过这个上限，所以 Windsurf 请用 `--compact`。目标超过其已知上限时脚本会打印 WARN。

**Roo Code.** `.roo/rules/` 下的每个文件都会在每次请求时加载，所以这个目标虽然位于规则目录里，实际上仍是常驻上下文。

**Continue.** 脚本会写入 `name`、`description` 和 `alwaysApply: false`，由 agent 决定何时把规则拉进来。

**Aider.** 只生成 `CONVENTIONS.md` 还不够。必须在 `.aider.conf.yml` 里把它加进 `read:`，Aider 才会读取：

```yaml
read:
  - CONVENTIONS.md
```

## 不要把导出结果纳入版本控制

导出的文件派生自 `SKILL.md`。本仓库的 `.gitignore` 已经排除了它们，本地导出不会误进 commit。在你自己的项目里，是否提交由你决定：提交能让团队共享规则，忽略则保持单一事实来源。

## 更新后重新导出

```bash
git -C /path/to/diataxis-docs-skill pull
python /path/to/diataxis-docs-skill/scripts/export_rules.py --target . --force
```
