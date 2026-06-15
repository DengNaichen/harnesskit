# RULE-ARCH-003

## Rule

不要把 `harness-linter-poc/` 当成打包 runtime 或外部 CLI API。

## Details

`harness-linter-poc/` 是独立 Context Harness linter POC，用于自举验证和 pre-commit。它当前不属于 `src/harnesskit` 包运行时，也不是对外 CLI API。

证据：

- `ARCHITECTURE.md`
- `harness-linter-poc/`
- `.pre-commit-config.yaml`

验证：

- review 负责确认变更没有把 POC 当成 runtime/API。
- harness lint tests 只证明 linter POC 自身行为，不证明 runtime 边界。
