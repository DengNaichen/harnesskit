# RULE-STACK-002

## Rule

Python 代码和测试变更必须通过 Ruff lint 和 Ruff format check。

## Details

本仓库使用 Ruff 做 lint 和 format check。Ruff 是否作为完成门槛来自 `pyproject.toml`、`.pre-commit-config.yaml` 和验证 skill；完成检查使用 check-only format 命令，不把会改文件的 `ruff format .` 写成完成门槛。

证据：

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.agents/skills/code-change-verification/SKILL.md`

验证：

- `uv run ruff check .`
- `uv run ruff format --check .`
- `make verify`
