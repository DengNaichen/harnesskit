# RULE-AI-002

## Rule

不要把模板示例、设计愿景或旧文档当成当前实现事实。

## Details

[docs/design/](../../docs/design/) 记录设计理念和未来方向，不等于当前实现。当前状态必须从源码、测试、配置、脚本、锁文件、Makefile/pre-commit 和根目录架构地图交叉验证。

证据：

- [docs/design/](../../docs/design/)
- [README.md](../../README.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [src/harnesskit/](../../src/harnesskit/)
- [harness-linter-poc/](../../harness-linter-poc/)
- [Makefile](../../Makefile)
- [.pre-commit-config.yaml](../../.pre-commit-config.yaml)

验证：

- harness lint 可发现部分 context drift。
- review 负责判断设计愿景、模板示例或旧文档是否被误当成当前事实。
