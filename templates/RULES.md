# [PROJECT_NAME] Harness Rules

本文件是 agent 约束索引。Rule 不是 workflow，也不是通用工程建议；Rule 只记录这个仓库里永远或局部必须成立的约束。

Skills 教 agent 怎么做一类任务；Rules 告诉 agent 在这个仓库里必须遵守什么；validation 负责把可检查的约束变成可执行反馈。[AGENTS.md](AGENTS.md) 负责路由，`.agents/skills/` 负责流程，[RULES.md](RULES.md) 只保留短约束句，不负责决定该调用哪个 skill。

每条规则必须有对应 details 文件，放在 [.harnesskit/rules/](.harnesskit/rules/)。[RULES.md](RULES.md) 负责告诉 agent “什么不能破坏”，details 文件负责说明“为什么、证据是什么、如何验证”。

除非已经从构建清单、锁文件、脚本、CI 配置、代码托管平台、[.harnesskit/facts.md](.harnesskit/facts.md) 或现有文档中验证，不要把本模板里的示例当作仓库已支持的命令或流程。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 保留已有客户规则；不要未经用户确认重排、合并、删除已有非模板规则。
- 只有满足“仓库局部、跨任务稳定、违反形态清楚、有事实依据”的内容才写成 Rule。
- 通用建议、任务步骤、工具教程、临时计划和未确认猜测不要写成 Rule。
- 新增规则时使用 `RULE-<CATEGORY>-<NUMBER>` 编号，并同步在 [.harnesskit/rules/](.harnesskit/rules/) 创建 details 文件。
- 规则正文保持一句话；事实来源、验证方式、runner 绑定和解释写进 details 文件，不需要单独拆成新的规则索引。
- 无法确认的规则保留 `[NEEDS CLARIFICATION: ...]`，不要强行启用。
<!-- harnesskit:todo-checklist:end -->

下面的分类只是整理规则的抽屉，不是启用依据。每个槽位都必须用目标仓库事实填充；没有事实就保留 `[NEEDS CLARIFICATION: ...]`。

## 通用工程实践

- RULE-ENG-001: [NEEDS CLARIFICATION: 记录本仓库的用户可见行为测试约束。] ([details](.harnesskit/rules/RULE-ENG-001.md))
- RULE-ENG-002: [NEEDS CLARIFICATION: 记录本仓库已经采用的依赖声明、锁文件或供应链同步约束。] ([details](.harnesskit/rules/RULE-ENG-002.md))
- RULE-ENG-003: [NEEDS CLARIFICATION: 记录本仓库声明的完整验证入口，不在 RULES.md 中重写 skill 路由。] ([details](.harnesskit/rules/RULE-ENG-003.md))
- RULE-ENG-004: 不要把没有仓库配置或 runner 证据的检查写成完成条件。([details](.harnesskit/rules/RULE-ENG-004.md))

## AI Coding 规则

- RULE-AI-001: [NEEDS CLARIFICATION: 记录本仓库要求判断必须基于哪些事实来源，而不是修改前流程。] ([details](.harnesskit/rules/RULE-AI-001.md))
- RULE-AI-002: 不要把模板示例、设计愿景、旧文档或未验证 facts 当成当前实现事实。([details](.harnesskit/rules/RULE-AI-002.md))
- RULE-AI-003: 发现代码、文档、rules、skills 或验证入口冲突时，先核对仓库事实再同步 context。([details](.harnesskit/rules/RULE-AI-003.md))
- RULE-AI-004: 未经用户明确要求，不要重排、合并、删除已有客户手写规则。([details](.harnesskit/rules/RULE-AI-004.md))

## 技术栈规则

- RULE-STACK-001: [NEEDS CLARIFICATION: 记录本仓库唯一或优先使用的包管理器、运行环境和命令前缀。] ([details](.harnesskit/rules/RULE-STACK-001.md))
- RULE-STACK-002: [NEEDS CLARIFICATION: 记录本仓库要求通过的工具检查入口。] ([details](.harnesskit/rules/RULE-STACK-002.md))
- RULE-STACK-003: [NEEDS CLARIFICATION: 记录工具链变更时必须同步更新的文件。] ([details](.harnesskit/rules/RULE-STACK-003.md))

## 架构规则

- RULE-ARCH-001: [NEEDS CLARIFICATION: 记录需要兼容性判断或额外审查的边界。] ([details](.harnesskit/rules/RULE-ARCH-001.md))
- RULE-ARCH-002: [NEEDS CLARIFICATION: 记录属于用户可见行为的生成输出。] ([details](.harnesskit/rules/RULE-ARCH-002.md))
- RULE-ARCH-003: [NEEDS CLARIFICATION: 记录本仓库最容易被混淆的架构边界。] ([details](.harnesskit/rules/RULE-ARCH-003.md))

## 产品 / 领域规则

- RULE-DOMAIN-001: [NEEDS CLARIFICATION: 记录本仓库最重要的业务、产品、数据或安全不变量。] ([details](.harnesskit/rules/RULE-DOMAIN-001.md))
