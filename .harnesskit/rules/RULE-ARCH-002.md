# RULE-ARCH-002

## Rule

`templates/` 是用户可见生成输出，模板行为变化必须同步 init 测试。

## Details

`templates/` 会被 `harnesskit init` 复制或渲染到目标仓库。模板变量使用 Jinja `StrictUndefined`，新增模板变量必须同步 render context 或明确保留目标仓库 TODO。具体执行流程由相关 skill 和测试入口承载；本规则只声明模板输出的用户可见边界。

证据：

- `ARCHITECTURE.md`
- `templates/`
- `tests/test_init.py`
- `src/harnesskit/init.py`

验证：

- `uv run pytest tests/test_init.py`
- `make verify`
