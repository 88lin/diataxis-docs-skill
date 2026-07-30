# 斜杠命令

[`.opencode/commands/`](../../.opencode/commands/) 里五个 OpenCode 斜杠命令的参考。当你想直接指定某种 Diataxis 工作模式、而不依赖自然语言触发时使用它们。

命令名来自文件名，而不是 frontmatter。`docs-classify.md` 定义的是 `/docs-classify`。

## 速查

| 命令 | 输入 | 返回 |
| --- | --- | --- |
| `/docs-classify` | 单个页面或粘贴的内容 | 它属于哪种 Diataxis 类型，以及混合形态的信号 |
| `/docs-split` | 一个混合形态的页面 | 拆分方案，以及拆分后每个页面的草稿 |
| `/docs-review` | 一份草稿 | 带严重级别标记的发布前审查意见 |
| `/docs-audit` | 一个文档目录或页面清单 | 逐页分类结果和处理优先级清单 |
| `/docs-quickstart` | 对产品或工具的描述 | 一条通向首次成功的最短路径 |

## `/docs-classify`

判定单个文档页面的类型。

输出章节：Classification、Section-by-section tags、Mixed-form signals、Recommended split (if any)、Reasoning。

```text
/docs-classify docs/getting-started.md
```

## `/docs-split`

把混合了多种形态的页面拆成它本应拥有的那几份文档。

输出章节：Diagnosis、Split plan、Drafts、Original page replacement。

Drafts 章节会给出拆分方案中每个页面的完整草稿，所以这是五个命令里输出最长的一个。

```text
/docs-split docs/getting-started.md
```

## `/docs-review`

发布前审查一份草稿。

输出章节：Review summary、Findings、Mixed-form signals、Suggested edits。每条 Finding 都带严重级别，便于你判断哪些问题会阻塞发布。

```text
/docs-review docs/api/webhooks.md
```

## `/docs-audit`

审计整个文档目录或一份页面清单。

输出章节：Audit summary、Per-page findings、Pages that need a split、Pages that need a small fix、Clean pages。

```text
/docs-audit docs/
```

对大型站点，先用 [`scripts/audit_docs.py`](../../scripts/audit_docs.py) 做一遍机械预筛，再把被标记的页面交给这个命令。见 [开发与贡献](development.md#扫描文档的混合形态气味)。

## `/docs-quickstart`

起草一份 quickstart。quickstart 是教程的一种特化形式：它优化的是**首次成功**，而不是完整性。

输出章节：What you will build、Prerequisites、Steps、Next steps。

```text
/docs-quickstart 我们那个用来开通预发布数据库的 CLI
```

## 参数

每个命令正文里的 `$ARGUMENTS` 会被替换成你在命令名之后输入的全部内容。可以传路径、路径列表，或直接粘贴页面内容。

## 在 OpenCode 之外的宿主里

斜杠命令的发现机制由宿主决定。Claude Code 会加载 `SKILL.md`，但不读 `.opencode/commands/`。在其他宿主里，要么用自然语言描述模式（"判断这个页面的类型，并指出混合形态"），要么把命令正文改写成该宿主自己的命令格式。

## 新增命令

见 [开发与贡献](development.md#新增斜杠命令)。
