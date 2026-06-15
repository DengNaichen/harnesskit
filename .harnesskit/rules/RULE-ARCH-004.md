# RULE-ARCH-004

## Rule

重要路径、职责或生成资产变化时，必须同步 `ARCHITECTURE.md`。

## Details

`ARCHITECTURE.md` 是粗粒度仓库地图。新增重要模块、linter rule、测试分组、生成资产或职责边界变化时，应更新地图，避免 agent 入口和真实仓库结构漂移。

证据：

- `ARCHITECTURE.md`
- `harness-linter-poc/app/rules/architecture.py`
- `.pre-commit-config.yaml`
- `AGENTS.md`

验证：

- harness lint architecture coverage 和 Markdown link check 可检查路径、coverage hint 与链接。
- review 负责判断职责或生成资产变化是否需要同步架构说明。
