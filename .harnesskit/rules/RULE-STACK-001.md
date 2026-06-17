# RULE-STACK-001

## Rule

Python 命令优先通过 `uv run ...` 使用仓库环境执行。

## Details

本仓库使用 `uv` 管理环境和命令。运行测试、lint、format、pre-commit、CLI 或 Python 调试命令时优先使用 `uv run ...`；具体本地开发命令维护在 [README.md](../../README.md)。

证据：

- [AGENTS.md](../../AGENTS.md)
- [README.md](../../README.md)
- [pyproject.toml](../../pyproject.toml)
- [uv.lock](../../uv.lock)
- [Makefile](../../Makefile)

验证：

- `make verify` 覆盖本仓库配置的主要 Python 命令入口。
- review 负责确认临时 Python 命令是否优先使用 `uv run ...`。
