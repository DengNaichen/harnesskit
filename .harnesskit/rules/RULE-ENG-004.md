# RULE-ENG-004

## Rule

不要把本仓库未配置的 typecheck、coverage、docs build 或 CI 写成完成条件。

## Details

本仓库当前没有 type checker、coverage gate、docs build 命令或 `.github` CI 配置。未配置的检查可以记录为待确认或未配置，但不能写成完成门槛；验证计划必须以仓库事实为准。

证据：

- [AGENTS.md](../../AGENTS.md)
- [pyproject.toml](../../pyproject.toml)
- [Makefile](../../Makefile)
- [.agents/skills/code-change-verification/SKILL.md](../../.agents/skills/code-change-verification/SKILL.md)
- [RULES.md](../../RULES.md)

验证：

- harness verification drift checks 可发现验证说明与已配置工具的部分漂移。
- review 负责确认未配置的 typecheck、coverage、docs build 或 CI 没有被写成完成条件。
