# Reliability Practices

本文件记录当前仓库改动风险较高的区域。它回答“在这个项目里，改哪些东西需要格外小心”，不重复通用可靠性建议。硬约束见 [RULES.md](../../RULES.md)。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实测试、hook、CI、release、兼容性、生成输出、持久数据和运维边界中提炼风险区域。
- 按影响范围和失败代价排序；不要把所有目录都列成高风险。
- 区分 command、validation 和 runner；不要把未配置检查写成 gate。
- 可执行硬约束进入 [RULES.md](../../RULES.md)，路径职责进入 [ARCHITECTURE.md](../../ARCHITECTURE.md)。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 高风险改动区域

按风险从高到低排列：

| 区域 | 影响范围 | 为什么风险高 |
|------|----------|-------------|
| [NEEDS CLARIFICATION: path or surface] | [NEEDS CLARIFICATION: 影响的用户、数据、部署、生成输出或外部集成] | [NEEDS CLARIFICATION: 失败代价、回滚难度、兼容性或安全风险] |
| [NEEDS CLARIFICATION: path or surface] | [NEEDS CLARIFICATION: 影响范围] | [NEEDS CLARIFICATION: 风险原因] |
| [NEEDS CLARIFICATION: path or surface] | [NEEDS CLARIFICATION: 影响范围] | [NEEDS CLARIFICATION: 风险原因] |

相比之下，[NEEDS CLARIFICATION: 已核实风险较低的区域] 的改动风险较低，前提是 [NEEDS CLARIFICATION: 不触碰的接口、数据、配置或外部行为边界]。

## 当前验证能力

- [NEEDS CLARIFICATION: 完整验证入口，例如 `make verify`、CI job 或“当前没有自动化验证”。]
- [NEEDS CLARIFICATION: 局部测试、lint、format、build、link check、migration check 或部署验证入口。]
- [NEEDS CLARIFICATION: 哪些风险只能通过 review、人工验证或 agent 执行验证。]
- 验证失败后修复问题并重新运行同一验证命令；最终交付只报告最终状态。

## 和 Rules 的关系

完成条件、runner 约束和必须始终成立的硬规则见 [RULES.md](../../RULES.md)。本文件只记录可靠性判断边界：哪里风险高、为什么高、以及当前有什么验证能力覆盖它。
