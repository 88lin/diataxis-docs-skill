# 开发与贡献

如何验证改动、新增内容，以及了解 CI 到底在检查什么。

## 开始之前

需要 Python 3.11 或更高版本。没有任何第三方依赖，所有脚本只用标准库，所以 CI 不需要安装步骤。

## 运行检查

```bash
python scripts/check_local.py
```

这是仓库校验的唯一事实来源。CI 运行的就是这条命令，所以本地跑通就等于 CI 跑通。它在第一类失败处返回非零退出码，并打印所有发现的问题。

它会校验：

- `SKILL.md` frontmatter 是否符合 Skill 规范：`name` 匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`、`description` 不超过 1024 字符，并报告未被识别的字段
- `SKILL.md` 正文不超过 500 行，超过 400 行时告警
- 安装文档 clone 的目标目录名与 Skill 名一致
- 两个支持命令发现的宿主提供同样的五个斜杠命令，每个都有 `description`、`$ARGUMENTS` 占位符，且 frontmatter 字段为该宿主所识别
- `evals/evals.json` 的结构、id 唯一性、分类合法性，以及引用的文件确实存在
- Markdown 内部链接、标题锚点和图片路径
- 中英文档保持配对
- 必需文件齐全
- `SKILL.md`、`evals/evals.json` 和 `CHANGELOG.md` 的版本号一致
- `export_rules.py --compact` 选取的每个章节在 `SKILL.md` 中确实存在
- 单元测试通过

## 直接运行测试

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

- `tests/test_check_local.py` 给每项检查喂入故意写错的输入，断言它确实被抓出来。一个停止校验的校验器比没有校验器更糟。
- `tests/test_audit_docs.py` 覆盖信号计数器、CLI 退出码和 `--exclude`。
- `tests/test_export_rules.py` 会把精简版和完整版真实写入临时项目，再检查链接完整性与 Windsurf 字符上限。

## 扫描文档的混合形态气味

```bash
python scripts/audit_docs.py docs/
python scripts/audit_docs.py . --exclude 'CHANGELOG.md' --fail-on high
```

扫描器报告的是值得人工看一眼的页面，它不是权威的分类器。

信号只在正文上统计：先剥离 YAML frontmatter 和围栏代码块，统计表格前再剥离行内代码。因此代码块里的 `ls | wc -l` 这类 shell 管道不会被算成表格行。

| 信号 | 含义 |
| --- | --- |
| `code_blocks` | 围栏代码块，按块计数而不是按围栏行 |
| `table_rows` | 真实表格的表头行与数据行，不含分隔行 |
| `step_lines` | 操作指令行。英文识别行首的祈使动词；中文因为通常以状语开头，所以在较短的列表项或以冒号结尾的引导句中，动词出现在任意位置都算 |
| `explanation_terms` | why、背景、架构、取舍一类词 |
| `reference_terms` | 参数、字段、schema、端点、取值范围一类描述接口的词 |

三条规则累加得分，4 分及以上为 high，2 到 3 分为 medium。`--fail-on {none,medium,high}` 决定退出码——CI 正是靠它让本仓库自己的页面保持诚实。

有三条刻意的限制，用来压低误报率：

- **代码块不算参考证据。** 任何合格的操作指南都充满命令，把它们计入参考信号会让每一份安装指南看起来都像夹带指令的参考页。
- **表格必须配合接口词汇才会计入混合。** 操作指南完全可以用一张「现象 / 原因 / 处理」表收尾；只有参数、字段这类词才说明这张表在描述接口。
- **弱信号 `tutorial/how-to` 不能单独标记页面。** 它只给已被其他规则标记的页面加 1 分，不会独自把干净的页面升级。

中文匹配基于关键词，没有分词，所以以动词作名词开头的条目（例如「安装文档……」）仍可能被算成一条步骤。单个信号的误计不会独自改变风险等级——把分数当作分诊结果，而不是判决。`tests/test_audit_docs.py` 会断言每个中文页面与其英文原页评出相同的风险等级，这正是发现两套语言规则漂移的方式。

## 新增评测项

在 [`evals/evals.json`](../../evals/evals.json) 的 `evals` 数组里追加一个对象：

```json
{
  "id": 33,
  "category": "classification",
  "prompt": "用户真的会输入的那句提示词。",
  "expected_output": "正确答案应有的形状，而不是它的确切措辞。",
  "files": ["SKILL.md"]
}
```

`id` 必须唯一，`category` 必须出现在顶层 `categories` 数组里，`files` 里的每个路径都必须存在。要用新分类，先把它加进那个数组。然后运行 `python scripts/check_local.py`。

评测是供人或模型审阅的"提示词—预期"配对，没有自动打分。

## 新增斜杠命令

在 [`.claude/commands/`](../../.claude/commands/) 和 [`.opencode/commands/`](../../.opencode/commands/) **两个**目录下新建同名 Markdown 文件，再把命令名加进 `scripts/check_local.py` 的 `COMMAND_NAMES`。文件名即命令名。如果某个命令只存在于一个宿主，`check_local.py` 会失败。

```markdown
---
description: 一句话说明什么时候用这个命令。
---

You are running the diataxis-docs skill in <mode> mode.

## Input

$ARGUMENTS

## Task

...

## Output shape

...
```

两个宿主的正文保持一致，只让 frontmatter 有差异。Claude Code 识别 `description`、`argument-hint`、`model`、`allowed-tools`、`disable-model-invocation`；OpenCode 识别 `description`、`agent`、`model`、`variant`、`subtask`。两个宿主都把 `description` 设为可选，但本仓库要求提供它，确保命令选择器里有清晰说明；同时要求正文包含 `$ARGUMENTS`，避免命令静默忽略用户输入。校验脚本会对该宿主不识别的字段告警，包括 `name`。

## 修改 SKILL.md

`SKILL.md` 会被加载进模型上下文，所以长度是每次使用都要付的成本。两条规则：

- 正文控制在 500 行以内。细节移进 `references/` 并链接过去。
- 不要在文件的另一处重复同一节内容。Skill 文件内部的重复既浪费上下文，又制造两处需要同步维护的内容。

`SKILL.md` 和这套文档之间同理。Skill 文件是写给模型的，这些页面是写给人的。

## 仓库结构

```text
.
├── SKILL.md                    # 宿主加载的 Skill 指令
├── README.md                   # 入口页
├── docs/                       # 面向人的文档，英文
│   └── zh-CN/                  # 面向人的文档，中文
├── references/                 # Skill 按需链接的细节
├── examples/messy-to-diataxis/ # 拆分前后的完整示例
├── evals/evals.json            # 提示词与预期的配对
├── .claude/commands/           # 斜杠命令提示词，Claude Code
├── .opencode/commands/         # 斜杠命令提示词，OpenCode
│                               # （Codex 加载 SKILL.md，但没有内置命令）
├── scripts/                    # 校验、审计与导出工具
├── tests/                      # 脚本的单元测试
└── .github/workflows/ci.yml    # 运行 check_local.py 与审计
```

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` | 触发条件、分类逻辑、反模式、质量检查 |
| `references/reader-analysis.md` | 动笔前的读者优先检查清单 |
| `references/doc-blueprints.md` | 各类文档的可复用结构 |
| `references/template-map.md` | Diataxis 文体到 Good Docs Project 模板的映射 |
| `references/zh-cn-anti-patterns.md` | 中文文档特有的反模式 |
| `scripts/check_local.py` | 仓库校验，CI 运行的就是它 |
| `scripts/audit_docs.py` | 混合形态的启发式扫描器 |
| `scripts/export_rules.py` | 面向其他助手的规则文件导出器 |

## CI

[`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) 对每次推送和面向 `master` 的 PR 运行一个 job，覆盖 Python 3.11 和 3.12：

1. `python scripts/check_local.py`
2. `python scripts/audit_docs.py . --exclude 'CHANGELOG.md' --fail-on high`
3. `python scripts/export_rules.py --list`，再各跑一次完整版和精简版的 `--dry-run` 导出，这样任一模式下的目标损坏都能被发现

CI 本身不含任何校验逻辑。新增检查意味着修改 `scripts/check_local.py`，这样本地结果和 CI 结果永远一致。

## 翻译

`docs/` 和 `docs/zh-CN/` 必须包含同名文件，出现漂移时 `check_local.py` 会失败。中文页面是完整翻译，不是摘要。`README.md` 和 `README.zh-CN.md` 遵循同样的规则。

## 提交 Pull Request

比修 bug 更大的改动，请先开 issue，以免 Skill 的范围失焦。有价值的贡献通常改进的是 `SKILL.md` 的触发措辞、蓝图、评测提示词、示例，或翻译。

见 [CONTRIBUTING.md](../../CONTRIBUTING.md)。
