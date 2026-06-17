# RULE-ENG-002

## Rule

新增第三方依赖时，必须同步更新 [pyproject.toml](../../pyproject.toml) 和 [uv.lock](../../uv.lock)。

## Details

不要引入未声明依赖。新增第三方 import、构建依赖或开发工具依赖时，同步更新依赖清单和锁文件；首次配置或依赖变更后运行 `uv sync`。

证据：

- [pyproject.toml](../../pyproject.toml)
- [uv.lock](../../uv.lock)
- [AGENTS.md](../../AGENTS.md)

验证：

- `uv run pytest`
- `uv build`
- review 检查依赖声明和锁文件是否同步；测试和构建只能间接暴露缺失依赖。
