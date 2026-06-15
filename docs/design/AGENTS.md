# AGENTS.md 设计说明

`AGENTS.md` 是 agent 进入仓库后的操作入口。它不应该承载所有项目知识，而应该告诉 agent：先读什么、哪些规则必须遵守、哪些技能要触发、如何验证完成，以及发现上下文漂移时应该修哪里。

本文件只说明 `AGENTS.md` 应该如何设计，不记录当前仓库自己的完整操作指南。具体项目的 agent 指南应写在该项目根目录的 `AGENTS.md` 中。

## 顶层路由器

`AGENTS.md` 的核心定位是 agent-facing context 的顶层路由器。它不直接成为项目知识库、规则全集、目录地图或工具链实现，而是把 agent 路由到正确的事实来源和执行入口。

一个好的 `AGENTS.md` 应能快速回答：

- 进入仓库后先读哪些文件。
- 哪些变更触发哪些本地 skill。
- 工程规则以哪个文件为准。
- 完整目录地图在哪里。
- 完成前运行哪个验证入口。
- 哪些低风险情况可以跳过完整验证。
- 当规则、文档、skill、runner 和仓库事实不一致时，应回到哪里核对。

因此，`AGENTS.md` 应更像控制面，而不是数据面：它写路由、触发条件和完成门槛；具体内容由 `RULES.md`、`ARCHITECTURE.md`、`.agents/skills/`、`Makefile`、脚本、CI 和项目文档承载。

## 核心职责

`AGENTS.md` 应承担五类职责：

- **上下文路由**：指出 `ARCHITECTURE.md`、`RULES.md`、本地 skills 和验证入口在哪里，以及什么时候读取它们。
- **行为路由**：说明哪些变更触发哪些 skill、兼容性判断或验证流程。
- **规则消费**：告诉 agent 如何使用 `RULES.md`，而不是在 `AGENTS.md` 里复制整份规则清单。
- **完成门槛**：说明交付前应运行哪个验证入口，以及失败后如何收敛。
- **漂移处理**：当文档、规则、skills、验证入口和仓库事实不一致时，要求 agent 回到事实来源核对并同步更新。

`AGENTS.md` 的目标是降低 agent 进场成本，而不是成为项目说明书或第二份仓库地图。产品定位、长期设计、路线图和背景材料应放在 `README.md`、`docs/` 或设计文档里；目录职责和模块边界应放在 `ARCHITECTURE.md`。

## 和其他文件的分工

- `AGENTS.md`：agent 操作入口，写执行路径、触发条件和完成要求。
- `RULES.md`：工程规则清单，写 Rule 状态、事实来源、agent 契约、Validation 类型和 Validation。
- `ARCHITECTURE.md`：仓库地图，写主要目录、关键文件和职责边界。
- `.agents/skills/*/SKILL.md`：具体流程说明，写技能触发后的步骤和命令。
- `Makefile`、脚本或 CI 配置：承载可执行入口，不把命令细节长期复制在多个文档里。
- `README.md` 和 `docs/`：产品说明、设计背景、路线图和长期讨论。

好的 `AGENTS.md` 应该引用这些文件，而不是吞掉它们的内容。引用关系越清楚，越容易发现漂移。

## 设计原则

### 简洁但可执行

`AGENTS.md` 应短到 agent 能快速读完，但必须包含足够明确的动作规则。空泛原则不如具体入口有用，例如“保持质量”不如“运行 `make verify`，失败后修复并重跑”。

### 以仓库事实为准

不要从模板、习惯或其他仓库复制命令。验证入口、测试框架、包管理器、构建方式和 CI 状态必须来自仓库清单、锁文件、脚本、配置或人工确认。

### 把规则放在 `RULES.md`

`AGENTS.md` 应说明如何消费 `RULES.md`：

- 开始任务前，根据变更范围查看相关 Rule。
- 执行时遵守对应 agent 契约。
- 交付前运行已绑定 Validation。
- `RULES.md` 中待确认或未配置的规则不能当作完成门槛。

这样可以避免 `AGENTS.md` 和 `RULES.md` 各写一套规则后互相漂移。

### 把流程放在 skill

当某个流程有足够多步骤或容易变化时，应放进 `.agents/skills/*/SKILL.md`，`AGENTS.md` 只保留触发条件和路径。这样 agent 会先读入口，再按需加载具体技能。

典型例子：

- 兼容性判断放进 `$implementation-strategy`。
- 完整验证放进 `$code-change-verification`。
- PR 草稿输出放进 `$pr-draft-summary`。
- 栈扫描和规则刷新放进 `$scan-stack`。

### 不虚构 runner

`AGENTS.md` 可以要求 agent 运行验证入口，但必须说明 runner 证据来自哪里。没有证据的 CI、branch protection、type check、coverage 或 docs build 不能写成强制完成条件。

### 把目录地图放在 `ARCHITECTURE.md`

`AGENTS.md` 可以列少量最高频入口，例如源码根、测试根、模板根和 `ARCHITECTURE.md` 路径，但不应该展开完整目录树。需要理解目录职责、模块边界或重要文件位置时，agent 应转去阅读 `ARCHITECTURE.md`。

这样可以避免两个问题：

- `AGENTS.md` 和 `ARCHITECTURE.md` 各维护一份目录地图，移动文件时容易只更新一边。
- agent 入口文档过长，真正的行为规则和验证入口被目录清单淹没。

### 明确可跳过条件

有些改动不需要完整验证，例如纯对话或低风险文档更新。`AGENTS.md` 可以写跳过条件，但要避免把会影响生成输出、模板行为、测试入口或验证配置的文档变更归为低风险。

## 推荐结构

一个实用的 `AGENTS.md` 通常包含：

1. 文件定位：说明这是 agent 操作入口，不是产品说明。
2. 强制 skill：列出触发条件和对应 skill 路径。
3. `RULES.md` 使用方式：说明 Rule 和 Validation 是规则源。
4. 可跳过验证的低风险情况。
5. 兼容性边界：列出 CLI、配置、模板、schema 等敏感面。
6. 关键入口索引：只列少量入口路径，并指向 `ARCHITECTURE.md` 获取完整仓库地图。
7. 操作指南：写开发流程、验证入口和失败处理。
8. Validation 与 Runner 绑定：说明命令、hook、CI 或平台 gate 的证据。
9. 审查关注点：列出最容易出错的行为边界。

模板版 `AGENTS.md` 可以保留 TODO checklist 和 `[NEEDS CLARIFICATION: ...]` 占位符；项目版 `AGENTS.md` 应尽量删掉已经完成的 checklist，留下已确认事实。

## 模板和项目版的差异

模板版 `AGENTS.md` 不能假设目标仓库已经有某个工具或流程。它应该提醒 agent：

- 先从仓库事实确认工具链。
- 未确认的路径、命令、触发条件和 runner 保留 `[NEEDS CLARIFICATION: ...]` 占位符。
- 未配置的验证命令保留 TODO 或标记未配置。
- `RULES.md` 中未确认的 Rule 不能当强规则。
- `Makefile` 或 runner 存在时，也要确认里面的 checks 已经填入真实命令。
- 模板版不需要写成候选规则清单；它仍是 `AGENTS.md` 的结构模板，只是项目事实必须等待目标仓库补全。

项目版 `AGENTS.md` 则应该更具体：

- 写真实入口路径，但不复制完整目录地图。
- 写真实验证入口。
- 写已经确认的 skill 触发条件。
- 写当前没有配置的工具，避免 agent 虚构完成门槛。

## 更新时机

以下变化通常需要同步检查 `AGENTS.md`：

- 新增、删除或重命名主要目录和关键文件。
- 变更 CLI、配置、模板输出或持久 schema。
- 变更测试、lint、format、build、pre-commit、CI 或验证入口。
- 新增、删除或重命名本地 skill。
- `RULES.md` 中的规则状态、Validation 或命令绑定发生变化。
- `ARCHITECTURE.md` 的目录职责发生变化。

如果只改 `AGENTS.md` 而不改对应的 `RULES.md`、skill 或验证入口，应该确认这是有意的；否则很可能是在制造新的 context drift。

## 自举项目的边界

当项目本身正在设计 agent harness 时，设计文档和当前项目指南要分开：

- 设计文档说明 `AGENTS.md` 应该怎么设计。
- 根目录 `AGENTS.md` 说明当前仓库的 agent 应该怎么工作。
- 模板 `templates/AGENTS.md` 说明目标仓库初始化后如何补全自己的 agent 指南。

这三层不要互相复制。设计文档保持抽象稳定，项目指南跟随仓库事实更新，模板则保持保守和待确认。
