# RULE-ARCH-001

## Rule

CLI/runtime 行为以 `src/harnesskit/` 和对应测试为事实来源。

## Details

`src/harnesskit/` 是打包发布的 CLI/runtime。CLI 命令、初始化行为、integration 安装、模板渲染或 `.harnesskit/config.json` 写入属于产品行为。兼容性判断和修改流程由 `AGENTS.md` 与 `$implementation-strategy` 承担；本规则只声明 runtime 行为的事实来源。

证据：

- `ARCHITECTURE.md`
- `src/harnesskit/`
- `tests/test_init.py`

验证：

- `uv run pytest tests/test_init.py`
- `make verify`
