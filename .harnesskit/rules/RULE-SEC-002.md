# RULE-SEC-002

## Rule

文件写入必须保持在目标项目内，且默认不得覆盖已有文件，除非用户显式选择覆盖。

## Details

本规则保护目标仓库文件系统安全和用户手写内容。HarnessKit 的 `init_project()` 和 `install_integration()` 会复制或渲染模板到目标项目；默认行为必须跳过已有文件，只有 `--force` 或等价显式确认才覆盖。路径处理必须避免把模板或用户输入写到目标项目之外。

违反形态：

- 默认覆盖目标仓库已有文件。
- `--force` 以外的路径绕过跳过逻辑。
- 允许模板路径、integration 名称或输出路径逃逸到项目目录外。

证据：

- [docs/practices/SECURITY.md](../../docs/practices/SECURITY.md)
- [src/harnesskit/init.py](../../src/harnesskit/init.py)
- [tests/test_init.py](../../tests/test_init.py)
- [templates/](../../templates/)

验证：

- runner：`uv run pytest tests/test_init.py`
- runner：`make verify`
- review：检查新增写入路径和覆盖行为是否保持显式 opt-in。
