# RULE-STACK-003

## Rule

测试入口是 `uv run pytest`，不要把其他测试框架写进验证计划。

## Details

本仓库使用 pytest。不要把 unittest 或未配置测试框架作为验证入口；如果未来测试框架变化，同步更新 rules、skills 和 verification block。

证据：

- [pyproject.toml](../../pyproject.toml)
- [tests/](../../tests/)
- [harness-linter-poc/tests/](../../harness-linter-poc/tests/)
- [.pre-commit-config.yaml](../../.pre-commit-config.yaml)

验证：

- `uv run pytest`
- pre-commit pytest hook
- verification drift checks 可发现文档中的部分过期测试入口。
