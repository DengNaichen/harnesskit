# RULE-ENG-003

## Rule

需要完整验证的变更必须使用 `make verify` 作为验证入口。

## Details

`make verify` 是本仓库单一完整验证入口。它运行 Markdown links、Ruff lint、Ruff format check、pytest、package build 和 pre-commit hooks。哪些任务触发完整验证由开发工作流和 $code-change-verification 说明；本规则只绑定入口命令，避免 [RULES.md](../../RULES.md) 变成任务路由器。

证据：

- [Makefile](../../Makefile)
- [AGENTS.md](../../AGENTS.md)
- [.agents/skills/code-change-verification/SKILL.md](../../.agents/skills/code-change-verification/SKILL.md)
- [.pre-commit-config.yaml](../../.pre-commit-config.yaml)

验证：

- `make verify`
