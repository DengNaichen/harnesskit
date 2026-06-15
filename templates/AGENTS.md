# [PROJECT_NAME] 贡献者指南

本指南是当前仓库的 agent 操作入口。它应作为顶层路由器：告诉 agent 先读什么、规则索引在哪里、哪些技能要触发、如何验证完成，以及发现上下文漂移时应该修哪里。

本文件不应承载完整项目知识、完整目录地图、规则全集、逐条 Rule 路由或工具链实现。项目定位、产品背景和长期设计讨论应放在 `README.md`、设计文档或 `docs/` 中；目录职责和模块边界应放在 `ARCHITECTURE.md` 或同类架构地图中；工程规则应放在 `RULES.md` 中；具体流程应放在 `.agents/skills/*/SKILL.md` 中。

除非已经从构建清单、锁文件、脚本、CI 配置、代码托管平台或现有文档中验证，不要把本模板里的示例当作仓库已支持的命令、路径或流程。

## 目录

- [策略与强制Skill](#策略与强制skill)
- [上下文入口](#上下文入口)
- [操作指南](#操作指南)
- [测试与自动化检查](#测试与自动化检查)
- [修改模板时的注意事项](#修改模板时的注意事项)
- [Pull Request 与提交规范](#pull-request-与提交规范)
- [审查关注点](#审查关注点)

## 策略与强制Skill

### 必须按需使用仓库本地Skills

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- `.agents/skills/` 中列出的技能真实存在，且名称和触发条件一致。
- 删除本仓库不需要的技能规则，避免 agent 追随不存在的流程。
- 本节只记录技能目录和使用原则；具体触发条件写进“开发工作流”。
- 新增技能时只写目录、使用原则或工作流触发点，执行细节放在对应 `SKILL.md`。
<!-- harnesskit:todo-checklist:end -->

- **技能目录**：[NEEDS CLARIFICATION: 例如 `.agents/skills/`，或说明本仓库未配置本地技能]
- **使用原则**：[NEEDS CLARIFICATION: 例如触发条件满足时先阅读对应 `SKILL.md`；未配置或仍含 `[NEEDS CLARIFICATION: ...]` 的技能只能作为待配置项]

### `RULES.md` 作为规则源

- **状态**：[NEEDS CLARIFICATION: 已确认 / 待补全 / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: `RULES.md`、规则维护说明、团队确认来源]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 agent 开始任务前如何路由到 `RULES.md`，交付前如何根据 details 或相关 skill 运行已绑定 validation；不要在 `AGENTS.md` 中为每条 Rule 建立路由]
- **漂移处理**：[NEEDS CLARIFICATION: 说明 `AGENTS.md`、skills、验证入口或项目命令与 `RULES.md` 不一致时如何核对和同步]

### 兼容性边界

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 找出本仓库已经对外承诺的 CLI、API、配置、schema、协议和生成输出。
- 明确最新发布标签、发布分支或“尚未发布”的判断依据。
- 没有证据的兼容性规则保留为待确认，不要从示例项目套用。
<!-- harnesskit:todo-checklist:end -->

修改下列内容前，必须明确兼容性决策：

- [NEEDS CLARIFICATION: CLI、公开 API、配置文件、环境变量或用户可见消息]
- [NEEDS CLARIFICATION: 持久化数据、schema、协议或序列化格式]
- [NEEDS CLARIFICATION: 模板、生成物或会写入其他仓库/环境的输出]
- [NEEDS CLARIFICATION: 文档中明确承诺支持的工作流、命令或行为]

判断破坏性变更时，以 [NEEDS CLARIFICATION: 最新发布标签、发布分支或团队确认规则] 为基准。

### 当前实现边界

[NEEDS CLARIFICATION: 说明本仓库需要区分的 runtime、模板、POC、设计文档、生成资产或其他实现边界。]

- [NEEDS CLARIFICATION: runtime / CLI / package 边界]
- [NEEDS CLARIFICATION: 模板、生成输出或写入外部仓库的资产边界]
- [NEEDS CLARIFICATION: POC、实验目录、设计文档或非 runtime 边界]

## 上下文入口

开始修改前，先从仓库事实建立上下文：

- [NEEDS CLARIFICATION: 构建/包管理清单路径，例如 `pyproject.toml`、`package.json`、`go.mod` 或同类文件]
- [NEEDS CLARIFICATION: scan/fill 事实快照路径，例如 `.harnesskit/facts.md`；未配置时说明待补全]
- [NEEDS CLARIFICATION: 架构地图路径，例如 `ARCHITECTURE.md`；未配置时说明待补全]
- [NEEDS CLARIFICATION: 产品说明、设计文档或 `docs/` 路径]
- [NEEDS CLARIFICATION: agent 指南、规则文件、技能目录和 companion 指南路径]

不要在指南、总结或验证计划里虚构仓库未配置的 formatter、linter、type checker、docs build、CI、发布流程或 PR 模板。只有从仓库事实确认后，才能把它们写成完成条件。

关键路由入口：

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只记录少量能帮助 agent 路由到正确事实来源和执行入口的路径。
- 完整目录地图放在 `ARCHITECTURE.md` 或同类架构地图；本节只指向它，不复制它。
- 从构建清单、目录结构、脚本、技能和文档中验证每条入口说明。
- 补完并确认后，可以删除这个 checklist 块。
<!-- harnesskit:todo-checklist:end -->

| 入口 | 路径 | 用途 / 事实来源 |
| --- | --- | --- |
| 架构地图 | [NEEDS CLARIFICATION: 路径或未配置] | [NEEDS CLARIFICATION: 说明目录职责和模块边界在哪里维护] |
| 工程规则 | [NEEDS CLARIFICATION: 路径或未配置] | [NEEDS CLARIFICATION: 说明 Rule、validation 和命令绑定在哪里维护] |
| scan/fill facts | [NEEDS CLARIFICATION: `.harnesskit/facts.md` 或未配置] | [NEEDS CLARIFICATION: 说明 facts 如何由 `$scan-facts` 刷新，并由 fill skills 消费] |
| 本地技能 | [NEEDS CLARIFICATION: 路径或未配置] | [NEEDS CLARIFICATION: 说明技能触发条件在哪里维护] |
| 构建/包管理清单 | [NEEDS CLARIFICATION: 路径或未配置] | [NEEDS CLARIFICATION: 说明包管理、构建和工具链事实来源] |
| companion agent 指南 | [NEEDS CLARIFICATION: 例如 `CLAUDE.md` 指向 `AGENTS.md`，或未配置] | [NEEDS CLARIFICATION: 说明如何保持一致] |

## 操作指南

### 开发工作流

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 工作流步骤符合本仓库真实的开发、测试和交付习惯。
- 模板、生成物、配置和运行时代码的处理顺序清楚。
- 删除不适用于本仓库的通用步骤。
<!-- harnesskit:todo-checklist:end -->

1. [NEEDS CLARIFICATION: 初次补全 harness 时是否先运行 `$harness-init` 或 `$scan-facts`；日常任务前应阅读的模块、测试、文档、规则或技能]
2. [NEEDS CLARIFICATION: 哪些改动必须先使用 `$implementation-strategy` 做兼容性判断]
3. [NEEDS CLARIFICATION: 哪些改动必须同步测试、文档、示例或模板输出]
4. [NEEDS CLARIFICATION: 发现仓库约定、命令或待确认事项时应记录到哪里]
5. [NEEDS CLARIFICATION: 哪些改动完成前必须使用 `$code-change-verification`，以及完整验证入口是什么]
6. [NEEDS CLARIFICATION: 验证失败后如何修复、重跑和报告]
7. [NEEDS CLARIFICATION: 何时使用 `$pr-draft-summary` 生成 PR 草稿、变更摘要或 review checklist]

### 测试与自动化检查

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只写已经从仓库配置、脚本、锁文件或 CI 中验证过的命令。
- 没有对应工具时说明未配置，不要填入通用示例命令。
- 同步更新 `.agents/skills/code-change-verification/SKILL.md` 中的验证栈。
- 为每个 validation 记录实际 runner，例如 pre-commit、CI、SVN server hook、agent verify、IDE task 或内部平台 gate。
<!-- harnesskit:todo-checklist:end -->

- **完整验证入口**：[NEEDS CLARIFICATION: 真实命令；未配置时写未配置]
- **验证 runner**：[NEEDS CLARIFICATION: Makefile、skill runner、pre-commit、CI、平台 gate、人工 review 或未配置]
- **验证 receipt / 结果记录**：[NEEDS CLARIFICATION: receipt 路径、CI job、平台记录或未配置]
- **与 `RULES.md` 的关系**：[NEEDS CLARIFICATION: 说明 Rule、validation、Runner 和项目命令绑定如何保持一致]

#### Validation 与 Runner 绑定

维护 `RULES.md` 或验证说明时，区分 **Rule**、**Validation** 和 **Runner**：Rule 是规则，Validation 是可执行检查或验证方式，Runner 是实际运行检查的位置。只有能从仓库、CI、hook、平台配置或团队确认中找到 runner 证据时，才能说这个 validation 会被执行或具备阻断效果。

没有 runner 证据的 validation 应标记为人工执行、agent 执行或未绑定，不能写成强制拦截。

### 修改模板时的注意事项

- [NEEDS CLARIFICATION: 哪些模板或 integration 模板会影响新初始化项目的输出]
- [NEEDS CLARIFICATION: 模板覆盖、跳过已有文件、force 行为或配置写入规则]
- [NEEDS CLARIFICATION: 模板变量、渲染上下文、占位符或生成资产验证要求]

### Pull Request 与提交规范

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只记录仓库实际采用的提交、分支、PR 描述和 review 要求。
- 没有 PR 模板、CI 或发布流程时不要虚构。
- 与 `$pr-draft-summary` 的输出要求保持一致。
<!-- harnesskit:todo-checklist:end -->

- **提交信息**：[NEEDS CLARIFICATION: 提交格式、语言、粒度或未配置]
- **分支 / PR 流程**：[NEEDS CLARIFICATION: 分支策略、PR 要求、review 要求或未配置]
- **PR 描述**：[NEEDS CLARIFICATION: 摘要、测试计划、风险说明、模板路径或未配置]
- **发布说明**：[NEEDS CLARIFICATION: 何时需要 changelog、release note 或迁移说明]

### 审查关注点

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 审查项覆盖本仓库最容易出错的行为边界和数据边界。
- 保留能指导 agent 做代码审查的风险项，删除空泛条目。
- 新增关键模块或生成流程后同步更新本节。
<!-- harnesskit:todo-checklist:end -->

- [NEEDS CLARIFICATION: 用户可见行为、错误消息、退出码或 API 风险]
- [NEEDS CLARIFICATION: 持久配置、schema、协议、生成输出或迁移风险]
- [NEEDS CLARIFICATION: 模板渲染、变量上下文、占位符泄漏或生成物风险]
- [NEEDS CLARIFICATION: 测试、示例、文档或 coverage 风险]
- [NEEDS CLARIFICATION: context drift 风险，例如 `AGENTS.md`、`RULES.md`、skills、架构地图和验证入口不一致]
