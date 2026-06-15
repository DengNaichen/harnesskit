# RULE-ENG-003

## Rule

[NEEDS CLARIFICATION: 记录本仓库声明的完整验证入口，不在 RULES.md 中重写 skill 路由。]

## Details

完整验证入口必须来自仓库事实，例如 Makefile、justfile、package scripts、CI workflow、pre-commit 配置或 agent skill。没有统一入口时，不要虚构；可以在 details 中记录当前已确认的分散检查和待统一事项。哪些任务触发完整验证应由 `AGENTS.md` 和 verification skill 说明，避免 `RULES.md` 变成任务路由器。

证据：

- [NEEDS CLARIFICATION: Makefile、justfile、package script、CI workflow、pre-commit 配置或 skill]

验证：

- [NEEDS CLARIFICATION: 完整验证命令、runner 绑定、CI required check 或未配置]
