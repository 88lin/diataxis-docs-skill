# 把指导导出到其他 AI 助手

本仓库以 OpenCode Skill 的形式打包，但 `SKILL.md` 里的指导是可移植的。[`scripts/export_rules.py`](../../scripts/export_rules.py) 会把它写到各个助手实际读取的规则文件路径，并补上该工具需要的 frontmatter。

## 开始之前

先读 [上下文成本](#上下文成本)。默认选中的 11 个目标里有 8 个会注入到项目的每一次请求；可选的旧版 Cursor 目标会把常驻目标总数增加到 9 个。

## 列出所有目标

```bash
python scripts/export_rules.py --list
```

覆盖 11 个助手的 12 个规则文件目标（默认选择其中 11 个）：

| Key | 工具 | 路径 | 默认 | 常驻 |
| --- | --- | --- | --- | --- |
| `cursor` | Cursor | `.cursor/rules/diataxis.mdc` | 是 | 否 |
| `cursor-legacy` | Cursor（旧格式） | `.cursorrules` | 否 | 是 |
| `cline` | Cline | `.clinerules/diataxis.md` | 是 | 是 |
| `roo` | Roo Code | `.roo/rules/diataxis.md` | 是 | 是 |
| `windsurf` | Windsurf | `.windsurf/rules/diataxis.md` | 是 | 否 |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | 是 | 是 |
| `claude` | Claude Code | `CLAUDE.md` | 是 | 是 |
| `codex` | OpenAI Codex | `AGENTS.md` | 是 | 是 |
| `aider` | Aider | `CONVENTIONS.md` | 是 | 是 |
| `gemini` | Gemini CLI | `GEMINI.md` | 是 | 是 |
| `continue` | Continue | `.continue/rules/diataxis.md` | 是 | 否 |
| `amazonq` | Amazon Q Developer | `.amazonq/rules/diataxis.md` | 是 | 是 |

## 先预览再写入

`--dry-run` 只报告会发生什么，不写任何文件：

```bash
python /path/to/diataxis-docs-skill/scripts/export_rules.py --target . --dry-run
```

## 导出

在需要接收规则文件的项目里运行，或者用 `--target` 指向它：

```bash
# 全部导出到当前项目。完整指导超过 Windsurf 平台上限时，
# 该目标会自动改用精简版。
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

默认选中的 11 个目标里有 8 个是常驻上下文；选择可选的旧版 Cursor 目标后，常驻目标会增加到 9 个。三个按需加载的目标是 `cursor`、`windsurf` 和 `continue`，但 Windsurf 的完整输出超过上限时会自动收到精简版。其余目标建议使用 `--compact`。

## 各工具注意事项

**Cursor.** 项目规则必须使用 `.mdc` 扩展名；放在 `.cursor/rules` 里的普通 `.md` 文件会被规则系统忽略。脚本写入的是 `.cursor/rules/diataxis.mdc`，并带上 `description` 和 `alwaysApply: false`，让它成为一条 agent-requested 规则：Cursor 读取 description，在任务看起来与文档相关时把规则拉进来。默认只选择现代目标；只有旧版 Cursor 环境才显式使用 `--only cursor-legacy`，两个目标不能同时选择。

**Cline.** workspace 规则位于 `.clinerules/` 目录。导出器会写入 `.clinerules/diataxis.md`；单个 `.clinerules` 文件不是当前的目录格式。

**Windsurf.** workspace 规则单文件上限 12,000 字符。完整指导超过这个上限，所以导出器会为该目标自动改用精简版；需要所有目标都使用相同精简内容时再显式传 `--compact`。脚本不再提供旧版 `.windsurfrules` 目标：它的 6,000 字符上限连精简版也容纳不下，因此不存在有效导出模式。请删除旧版本曾生成的 `.windsurfrules`。

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
