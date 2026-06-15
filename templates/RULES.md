# [PROJECT_NAME] Harness Rules

本文件是当前仓库的 Harness Rules 模板。它提供一组工程好实践候选项，不预设客户仓库已经具备这些规则。agent 进入仓库后，应根据客户已有代码库和团队事实补全本文件：能确认的就沉淀为规则，暂时确认不了的就保留占位符和待确认说明。

除非已经从构建清单、锁文件、脚本、CI 配置、代码托管平台或现有文档中验证，不要把本模板里的示例当作仓库已支持的命令或流程。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 能从客户仓库事实确认的内容，替换对应 `[NEEDS CLARIFICATION: ...]` 占位符。
- 暂时确认不了的内容，保留占位符，并在最终说明或本节附近记录待确认原因。
- 确认不适用的 `[REMOVE IF UNUSED]` 小节，可以删除；不能确认是否适用时先保留。
- 只有启用为真实规则的条目，才写成明确的 agent 契约和 Guard。
- 保持本文件、`AGENTS.md`、验证入口和 CI 配置一致；不能确认一致性时保留待确认标记。
<!-- harnesskit:todo-checklist:end -->

## 使用方式

- **基础候选规则**：比较通用的好实践，优先尝试用客户仓库事实补全；确认不了就保留待确认，不要强行启用。
- **可选规则**：只有仓库事实证明已配置相关工具、流程或平台能力时才启用；确认不了就保留占位符或标记未配置。
- **事实来源**：写具体文件、脚本、CI 配置、平台设置或人工确认来源。
- **agent 契约**：用祈使句写 agent 必须遵守的动作规则。
- **Guard 类型**：写 `确定性`、`部分确定性`、`人工/agent review` 或 `未配置`，说明这条规则能被工具验证到什么程度。
- **Guard**：写能验证或执行该规则的检查、命令、CI gate、review gate 或平台配置。

## 基础候选规则

### [RULE-001: 单一验证入口]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 例如 Makefile、justfile、package scripts、CI 配置、AGENTS.md]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 agent 完成任务前必须运行的唯一验证命令]
- **Guard**：[NEEDS CLARIFICATION: 说明 CI 或本地检查如何运行同一个验证入口]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`Makefile`、`.github/workflows/ci.yml`、`AGENTS.md`。
- **agent 契约**：使用 `make verify` 作为本地开发、agent 交付和 CI 的唯一完整验证入口。
- **Guard**：CI 必须调用 `make verify`，文档中的验证命令也必须指向 `make verify`。
-->

### [RULE-002: 新增行为必须有测试]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 测试目录、测试框架配置、CI 配置、PR 规则]
- **agent 契约**：[NEEDS CLARIFICATION: 说明哪些变更必须添加自动化测试]
- **Guard**：[NEEDS CLARIFICATION: 测试命令、CI 测试任务、PR review 清单]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：`tests/`、`pyproject.toml`、`.github/workflows/ci.yml`、PR 模板。
- **agent 契约**：为新增功能、bug fix、CLI 行为、配置行为、模板输出或用户可见行为变化添加对应自动化测试。
- **Guard**：完整验证入口和 CI 必须运行测试；PR 描述说明测试覆盖；review 检查代码变更和测试变更是否匹配。
-->

### [RULE-003: Test 入口以仓库事实为准]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 测试配置、依赖清单、现有测试、CI 配置]
- **agent 契约**：[NEEDS CLARIFICATION: 说明真实测试框架和真实测试命令]
- **Guard**：[NEEDS CLARIFICATION: 验证入口、CI 任务、漂移检查]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`tests/`、`pyproject.toml`、`.github/workflows/ci.yml`。
- **agent 契约**：以仓库事实决定测试入口；检测到测试框架变化时，同步更新文档、验证入口和 CI。
- **Guard**：统一验证入口和 CI 必须运行真实测试命令，并检查过期测试命令。
-->

### [RULE-004: 命名遵守本仓库现有风格]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 现有源码、linter 配置、语言命名约定]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 agent 必须遵守的命名风格]
- **Guard**：[NEEDS CLARIFICATION: linter、review、命名 Guard 或人工 review]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：现有源码、linter 配置、团队 review 规则。
- **agent 契约**：遵守仓库已有命名风格编写新增代码，尊重本地代码中的既有例外。
- **Guard**：linter 检查可自动覆盖的命名和风格问题；仓库惯例和例外由 review 确认。
-->

### [RULE-005: import 和依赖必须同步]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 依赖清单、锁文件、import 风格、包管理器]
- **agent 契约**：[NEEDS CLARIFICATION: 说明新增代码引用如何同步到依赖声明]
- **Guard**：[NEEDS CLARIFICATION: locked install、测试、import/dependency Guard、review]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：依赖清单、锁文件、包管理器配置、CI 配置。
- **agent 契约**：不要引入未声明依赖；新增 import / require / use / package reference 时同步更新依赖清单和锁文件。
- **Guard**：locked install、测试和 build 必须通过；review 检查依赖清单和锁文件是否同步。
-->

### [RULE-006: 文档和 context harness 不漂移]

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: AGENTS.md、RULES.md、skills、验证文档、技术栈文档]
- **agent 契约**：[NEEDS CLARIFICATION: 说明哪些 agent-facing context 文件必须和仓库事实保持一致]
- **Guard**：[NEEDS CLARIFICATION: Markdown 链接检查、marker 配对检查、skill 引用检查、漂移检查]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：`AGENTS.md`、`RULES.md`、skills、验证文档、技术栈文档、harness lint 配置。
- **agent 契约**：保持 agent-facing context 和仓库事实一致，避免 `AGENTS.md`、本文件、skills 和验证文档误导 agent。
- **Guard**：检查 Markdown 链接、marker 配对、skill 引用、tech stack drift 和 verification drift；语义准确性由 review 确认。
-->

## 可选规则

### [可选规则: Branch protection 和 required checks] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库使用代码托管平台、受保护主干和 PR 合并流程时启用。若不能确认，保留占位符；若确认未配置，标记为未配置，不要要求 agent 强制执行。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 仓库设置、branch protection 导出、CI required checks、团队规则]
- **agent 契约**：[NEEDS CLARIFICATION: 说明受保护分支、push 限制和 review 要求]
- **Guard**：[NEEDS CLARIFICATION: 代码托管平台的 branch protection / required checks 配置]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：代码托管平台 branch protection 设置、required checks 配置、团队规则。
- **agent 契约**：不要直接 push 到受保护主干；合并前等待 required checks 通过并满足 review 要求。
- **Guard**：代码托管平台强制 branch protection、required checks 和 review 要求。
-->

### [可选规则: 锁文件一致性] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库有依赖清单和锁文件时启用。若不能确认，保留占位符；若确认未配置锁文件，标记为未配置，不要虚构 locked install 命令。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: 依赖清单、锁文件、包管理器文档、CI 配置]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 locked install 命令和依赖更新规则]
- **Guard**：[NEEDS CLARIFICATION: 验证入口和 CI 中的 locked / frozen / reproducible install]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`pyproject.toml`、`uv.lock`、CI 配置。
- **agent 契约**：使用 `uv sync --locked` 安装依赖；依赖变更必须同步 `pyproject.toml` 和 `uv.lock`。
- **Guard**：验证入口和 CI 运行 `uv sync --locked`，依赖清单和锁文件不一致时失败。
-->

### [可选规则: Type check] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库配置了 type checker 或团队明确要求类型检查时启用。若不能确认，保留占位符；若确认未配置，标记为未配置，不要添加示例 type check 命令。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: type checker 配置、依赖清单、CI 配置、项目文档]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 type check 命令，以及 agent 什么时候必须运行它]
- **Guard**：[NEEDS CLARIFICATION: 验证入口和 CI type check 任务]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：type checker 配置、依赖清单、CI 配置。
- **agent 契约**：修改运行时代码、导出 API 或类型相关代码时运行仓库声明的 type check 命令。
- **Guard**：验证入口和 CI 运行 type check 命令。
-->

### [可选规则: 测试覆盖率 gate] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库配置了 coverage 工具或团队明确要求覆盖率阈值时启用。若不能确认，保留占位符；若确认未配置，不要虚构 coverage 命令或阈值。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: coverage 配置、测试命令、CI 配置、团队阈值规则]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 agent 何时必须保持或提高覆盖率，以及 coverage 不能替代行为测试]
- **Guard**：[NEEDS CLARIFICATION: coverage 命令、阈值 gate、CI coverage 任务]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：coverage 配置、测试命令、CI coverage 任务、团队阈值规则。
- **agent 契约**：修改运行时代码或新增行为时保持覆盖率不下降；coverage 只能作为辅助信号，不能替代针对新增行为的自动化测试。
- **Guard**：验证入口和 CI 运行 coverage 命令，并在覆盖率低于团队阈值时失败。
-->

### [可选规则: Linter] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库声明了 linter 时启用。若不能确认，保留占位符；若确认未配置，标记为未配置，不要要求 lint 作为完成门槛。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: linter 配置、依赖清单、脚本、CI 配置]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 lint 命令和完成门槛]
- **Guard**：[NEEDS CLARIFICATION: 验证入口和 CI lint 任务]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：linter 配置、依赖清单、脚本、CI 配置。
- **agent 契约**：把仓库声明的 lint 命令作为相关代码变更的完成门槛。
- **Guard**：验证入口和 CI 运行 lint 命令。
-->

### [可选规则: Formatter check-only gate] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库配置了 formatter 时启用。若配置了 formatter，完成门槛必须使用 check-only 命令；若不能确认，保留占位符；若确认未配置，标记为未配置。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: formatter 配置、脚本、CI 配置]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 format check 命令，以及不要把会改文件的 formatter 命令写成完成门槛]
- **Guard**：[NEEDS CLARIFICATION: 验证入口和 CI format-check 任务]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：formatter 配置、脚本、CI 配置。
- **agent 契约**：完成检查使用 check-only format 命令；不要把会改文件的 formatter 命令写成完成门槛。
- **Guard**：验证入口和 CI 运行 format check 命令。
-->

### [可选规则: Build 进入验证入口] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库配置了 package build、应用构建或产物生成时启用。若不能确认，保留占位符；若确认未配置 build，标记为未配置，不要发明 build 命令。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: build 配置、项目清单、脚本、CI 配置]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 build 命令，以及 agent 什么时候必须运行它]
- **Guard**：[NEEDS CLARIFICATION: 验证入口和 CI build 任务]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：build 配置、项目清单、脚本、CI 配置。
- **agent 契约**：影响 package、应用构建、模板打包或产物生成时运行仓库声明的 build 命令。
- **Guard**：验证入口和 CI 运行 build 命令。
-->

### [可选规则: Pre-commit 或 hook suite] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库配置了 pre-commit 或同类 hook suite 时启用。若不能确认，保留占位符；若确认未配置，标记为未配置，不要把 hook suite 当成默认存在。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: hook 配置、脚本、项目文档]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 hook suite 命令，以及它和其他 Guard 的关系]
- **Guard**：[NEEDS CLARIFICATION: 验证入口、CI 任务或本地 hook 规则]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：hook 配置、脚本、项目文档。
- **agent 契约**：把 hook suite 视为验证套件；不要把 hook suite 等同于所有 Guard。
- **Guard**：运行仓库声明的 hook suite 命令。
-->

### [可选规则: Architecture Map] [REMOVE IF UNUSED]

<!-- 可选：仅当仓库维护 `ARCHITECTURE.md` 或同类架构地图时启用。若不能确认，保留占位符；若确认未配置，标记为未配置；需要时先创建架构地图，再启用本规则。 -->

- **状态**：[NEEDS CLARIFICATION: 已确认 / 部分确认 / 待确认 / 未配置 / 不适用]
- **Guard 类型**：[NEEDS CLARIFICATION: 确定性 / 部分确定性 / 人工/agent review / 未配置]
- **事实来源**：[NEEDS CLARIFICATION: ARCHITECTURE.md 或同类架构地图]
- **agent 契约**：[NEEDS CLARIFICATION: 说明 agent 修改模块前如何使用架构地图]
- **Guard**：[NEEDS CLARIFICATION: 路径存在性、coverage hint、placeholder 或 review 检查]

<!-- 完整示例，验证后替换：
- **状态**：已确认。
- **Guard 类型**：部分确定性。
- **事实来源**：`ARCHITECTURE.md`、架构 lint 配置、review 规则。
- **agent 契约**：修改重要模块、目录职责或生成资产前先阅读架构地图；新增重要模块或职责变化时同步更新架构地图。
- **Guard**：工具检查路径存在性、coverage hint 和 placeholder；职责描述准确性由 review 确认。
-->

## 项目命令绑定

能从客户仓库事实确认的命令，就替换对应 `[NEEDS CLARIFICATION]`。暂时确认不了的命令保留占位符；确认未配置的可选规则保留为 `N/A`，并在事实来源中说明没有仓库证据。

| 检查项 | 当前命令 | 事实来源 |
| --- | --- | --- |
| 完整验证入口 | [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| 依赖安装 | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Test | [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Lint | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Format check | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Type check | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Coverage | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Build | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
| Hook suite | N/A 或 [NEEDS CLARIFICATION: 填写真实命令] | [NEEDS CLARIFICATION: 填写事实来源] |
