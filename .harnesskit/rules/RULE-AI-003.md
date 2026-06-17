# RULE-AI-003

## Rule

发现代码、文档、rules、skills 或验证入口冲突时，先核对仓库事实再同步 context。

## Details

不要静默选择其中一边。先确认可验证来源，再同步 [AGENTS.md](../../AGENTS.md)、[RULES.md](../../RULES.md)、[ARCHITECTURE.md](../../ARCHITECTURE.md)、skills、facts 或验证入口。

证据：

- [AGENTS.md](../../AGENTS.md)
- [RULES.md](../../RULES.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [.agents/skills/](../../.agents/skills/)
- [harness-linter-poc/](../../harness-linter-poc/)

验证：

- `lychee './**/*.md'`
- harness lint
- review 负责处理机器检查无法判断的语义冲突。
