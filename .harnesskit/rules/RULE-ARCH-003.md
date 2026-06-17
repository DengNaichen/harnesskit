# RULE-ARCH-003

## Rule

`harnesskit lint` 的产品入口必须来自 [src/harnesskit/linter/](../../src/harnesskit/linter/)，不要继续把 [harness-linter-poc/](../../harness-linter-poc/) 当成主入口。

## Details

[src/harnesskit/linter/](../../src/harnesskit/linter/) 是当前打包进 CLI 的 Context Harness linter runtime，`harnesskit lint`、pre-commit 和未来对外 lint 行为都应以这里为事实来源。[harness-linter-poc/](../../harness-linter-poc/) 只保留为旧 POC/参考实现，不再作为新增功能或用户入口的首要修改位置。

证据：

- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [src/harnesskit/linter/](../../src/harnesskit/linter/)
- [harness-linter-poc/](../../harness-linter-poc/)
- [.pre-commit-config.yaml](../../.pre-commit-config.yaml)

验证：

- review 负责确认新增 lint 行为落在 [src/harnesskit/linter/](../../src/harnesskit/linter/) 和 `harnesskit lint`。
- `uv run harnesskit lint .` 和 CLI 测试负责证明产品入口可用。
