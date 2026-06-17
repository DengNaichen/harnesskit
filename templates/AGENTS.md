# [PROJECT_NAME] 贡献者指南

本文件是当前仓库的 agent 启动入口：保留少量会影响操作判断的事实，并把 agent 路由到规则、架构地图、skills 和验证入口。它不是项目知识库；完整目录职责应放在 [ARCHITECTURE.md](ARCHITECTURE.md) 或同类架构地图中，工程约束应放在 [RULES.md](RULES.md) 中，具体任务流程应放在 `.agents/skills/` 中，产品背景应放在 `README.md`、设计文档或 `docs/` 中。

除非已经从构建清单、锁文件、脚本、CI 配置、代码托管平台、[.harnesskit/facts.md](.harnesskit/facts.md) 或现有文档中验证，不要把本模板里的示例当作仓库已支持的命令、路径或流程。

## 操作关键事实

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只保留会改变 agent 当下操作判断的少量事实。
- 完整目录地图、模块职责和长期设计背景不要写在这里。
- 无法确认的事实保留 `[NEEDS CLARIFICATION: ...]`，不要从示例项目套用。
<!-- harnesskit:todo-checklist:end -->

- [NEEDS CLARIFICATION: 用一句话说明仓库类型、主要语言/运行时、包管理器或构建入口。]
- [NEEDS CLARIFICATION: 记录最重要的用户可见边界，例如 CLI/API、持久配置、模板输出、生成资产、数据库 schema、外部集成或发布产物。]
- [NEEDS CLARIFICATION: 记录少量会影响修改策略的当前状态，例如默认 integration、schema version、支持平台、主要验证入口或 companion 指南。]

## 上下文路由

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 路由到真实存在的文件；未配置的入口写成未配置或待确认。
- 不要在本文件复制完整规则目录、架构地图或 skill 正文。
- 不要规定必须列出每条 rule；只说明 agent 如何找到并使用适用规则。
<!-- harnesskit:todo-checklist:end -->

- 开始任务前先读 [RULES.md](RULES.md) 或 [NEEDS CLARIFICATION: 本仓库规则入口；未配置时写未配置]，并按需查看规则 details、验证说明或团队确认来源。
- 涉及路径职责、实现边界、生成资产或旧/新实现取舍时，读 [ARCHITECTURE.md](ARCHITECTURE.md) 或 [NEEDS CLARIFICATION: 同类架构地图；未配置时写未配置]。
- 需要产品定位、设计背景、路线图或用户文档时，读 `README.md`、`docs/` 或 [NEEDS CLARIFICATION: 设计文档或未配置]。
- 涉及代码风格、产品体验、安全或可靠性判断时，按需阅读 [docs/practices/](docs/practices/)；这些文件是判断指导，不替代 [RULES.md](RULES.md) 的硬约束。
- 触发本地 skill 时，先读对应 skill 文件；当前技能目录是 `.agents/skills/` 或 [NEEDS CLARIFICATION: 未配置]。
- [.harnesskit/facts.md](.harnesskit/facts.md) 可作为扫描事实快照；高影响判断仍要回到真实仓库文件核对。

## 工作策略

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只写本仓库真实采用或明确希望 agent 遵守的策略。
- 把详细步骤放进 skills；本节只保留触发点和边界。
- 没有对应 skill 或 workflow 时写未配置，不要保留示例命令作为事实。
<!-- harnesskit:todo-checklist:end -->

{% if HAS_CODEX_INTEGRATION %}
- 修改用户可见行为、公开 API、CLI 命令或参数、外部配置、持久化数据、模板输出或生成资产前，先使用 $implementation-strategy 明确兼容性边界。
- 影响运行时代码、模板、测试、构建配置、锁文件、Markdown 链接或验证行为的变更，在完成前使用 $code-change-verification。
- 初次补全或刷新 harness context 时，按需使用 $harness-init 或 $scan-facts。
- 刷新 [docs/practices/](docs/practices/) 判断指导时，使用 $fill-practices；如果发现新的硬约束候选，再交给 $fill-rules。
- 中等及以上规模的行为变更完成后，按 $pr-draft-summary 准备交付说明。
{% else %}
- 修改用户可见行为、公开 API、CLI 命令或参数、外部配置、持久化数据、模板输出或生成资产前，先明确兼容性边界：[NEEDS CLARIFICATION: implementation-strategy skill、团队流程、人工判断或未配置]。
- 影响运行时代码、模板、测试、构建配置、锁文件、Markdown 链接或验证行为的变更，在完成前按 [NEEDS CLARIFICATION: code-change-verification skill、真实验证流程或未配置] 验证。
- 初次补全或刷新 harness context 时，按需使用 [NEEDS CLARIFICATION: harness-init 或 scan-facts skill、对应人工流程或未配置]。
- 刷新 [docs/practices/](docs/practices/) 判断指导时，按 [NEEDS CLARIFICATION: fill-practices skill、人工流程或未配置] 处理；不要把所有指导直接写成硬规则。
- 中等及以上规模的行为变更完成后，按 [NEEDS CLARIFICATION: pr-draft-summary skill、仓库 PR 模板、变更摘要要求或未配置] 准备交付说明。
{% endif %}
- 发现可复用约定、规则候选、命令漂移或待确认事项时，记录到 [RULES.md](RULES.md) details、[.harnesskit/facts.md](.harnesskit/facts.md)、相关文档、todo 文件或 [NEEDS CLARIFICATION: 未配置]。

## 验证入口

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 只写已经从仓库配置、脚本、锁文件、CI、hook 或团队确认中验证过的命令。
- 没有对应工具时说明未配置，不要填入通用示例命令。
- 区分 Rule、Validation 和 Runner；不要把未绑定检查写成强制拦截。
<!-- harnesskit:todo-checklist:end -->

完整验证入口：[NEEDS CLARIFICATION: 真实命令；没有统一入口时写未配置，并列出可执行的局部验证方式]。

当前已确认的验证 runner：[NEEDS CLARIFICATION: Makefile、package scripts、pre-commit、CI、平台 gate、agent skill、人工 review 或未配置]。

当前未配置或未证实的检查：[NEEDS CLARIFICATION: typecheck、coverage、docs build、CI、release gate、PR 模板或 N/A]。不要在指南、总结或验证计划里虚构这些完成条件。

维护验证说明时区分 Rule、Validation 和 Runner：Rule 是约束，Validation 是检查方式，Runner 是实际执行位置。没有 runner 证据的检查只能标记为人工执行、agent 执行或未绑定。

<!-- harnesskit:verification:start -->
- Full verification: [NEEDS CLARIFICATION: 真实完整验证命令或未配置]
- Format: [NEEDS CLARIFICATION: 真实 format check 命令或未配置]
- Lint: [NEEDS CLARIFICATION: 真实 lint 命令或未配置]
- Typecheck: [NEEDS CLARIFICATION: 真实 typecheck 命令或未配置]
- Tests: [NEEDS CLARIFICATION: 真实 test 命令或未配置]
- Build: [NEEDS CLARIFICATION: 真实 build 命令或未配置]
- Hooks / CI: [NEEDS CLARIFICATION: 真实 hook/CI 命令或未配置]
<!-- harnesskit:verification:end -->

验证失败后修复问题并重新运行同一验证命令；最终交付只报告最终状态。

## 漂移处理

如果 [AGENTS.md](AGENTS.md)、[RULES.md](RULES.md)、[ARCHITECTURE.md](ARCHITECTURE.md)、skills、验证入口、项目命令或仓库事实互相冲突，不要静默选择一边；先核对真实文件，再同步修复漂移的 context 文件。

文档职责保持分离：[AGENTS.md](AGENTS.md) 讲 agent 如何开始和路由，[RULES.md](RULES.md) 讲不能破坏的约束，[ARCHITECTURE.md](ARCHITECTURE.md) 或同类文件讲仓库地图，skills 讲任务流程，[docs/practices/](docs/practices/) 讲判断指导，`README.md` 和 `docs/` 讲产品与设计背景。
