# RULE-DOMAIN-001

## Rule

HarnessKit 当前 MVP 只负责 Context Harness，不实现 agent runtime、沙箱或多 agent 编排。

## Details

HarnessKit 是用于安装和维护 agent-facing context、规则、验证入口和本地 skills 的 CLI/toolkit。它不实现 agent loop、权限沙箱、长期运行调度或多 agent controller。

证据：

- `README.md`
- `docs/ROADMAP.md`
- `docs/design/DESIGN.md`

验证：

- review 负责确认新增功能没有越过当前 MVP 边界；产品文档提供事实来源但不是自动 runner。
