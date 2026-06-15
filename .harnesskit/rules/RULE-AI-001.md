# RULE-AI-001

## Rule

代码和生成行为判断必须基于已核对的仓库事实。

## Details

这条规则约束事实来源，不承担任务路由。`AGENTS.md` 和 skill trigger 决定具体流程；涉及代码、模板或生成行为时，判断必须回到 `ARCHITECTURE.md`、相关模块、测试、配置、脚本和已确认 rules，而不是只凭 README、设计文档或模板示例推断当前实现。

证据：

- `AGENTS.md`
- `ARCHITECTURE.md`
- `RULES.md`
- `.agents/skills/`

验证：

- agent/review：确认判断回到仓库事实；当前没有独立机器 validation。
