# 贡献者指南

本指南帮助新贡献者快速上手 {{PROJECT_NAME}} 仓库，涵盖仓库结构、测试方法、常用工具以及提交与 PR 规范。

**位置：** 仓库根目录的 `AGENTS.md`。

## 目录

1. [策略与强制规则](#策略与强制规则)
2. [项目结构指南](#项目结构指南)
3. [操作指南](#操作指南)

---

## 策略与强制规则

### 强制技能调用

#### `$code-change-verification`

当变更影响运行时代码、测试或构建/测试行为时，在标记工作完成**之前**必须运行 `$code-change-verification`。

以下情况需要运行：
{{VERIFICATION_TRIGGER_CONDITIONS}}

以下情况可跳过（除非用户明确要求运行完整验证栈）：
- 仅修改文档或仓库元数据（例如 `.agents/`、`README.md`、`AGENTS.md`、`.github/`）。

{{#if DOMAIN_KNOWLEDGE_SKILL}}
#### `${{DOMAIN_KNOWLEDGE_SKILL}}`

当涉及 {{DOMAIN_KNOWLEDGE_CONTEXT}} 时，使用 `${{DOMAIN_KNOWLEDGE_SKILL}}` 通过 {{DOMAIN_KNOWLEDGE_SOURCE}} 获取权威文档（若未配置，请引导用户完成配置）。
{{/if}}

#### `$implementation-strategy`

在修改运行时代码、导出 API、外部配置、持久化 schema、线协议或其他面向用户的行为**之前**，使用 `$implementation-strategy` 来确定兼容性边界和实现形式。判断破坏性变更时，以最新发布标签（release tag）为基准，而非未发布的分支本地改动。在最新发布标签之后引入或修改的接口，可以直接重写而无需兼容性垫片，除非它们定义了已发布或明确支持的持久外部状态边界，或用户明确要求迁移路径。`main` 上未发布的持久化格式在发布前可以重新编号或合并，当中间快照被刻意不支持时。

#### `$pr-draft-summary`

当本仓库的任务完成中等及以上规模的代码变更时，在最终交付中调用 `$pr-draft-summary`，生成标准 PR 摘要块、分支建议、标题和草稿描述。将其作为运行时代码、测试、示例、构建/测试配置或有行为影响的文档变更后的**默认收尾步骤**。

仅在以下情况跳过：
- 琐碎或纯对话性任务。
- 无行为影响的仓库元数据/纯文档任务。
- 用户明确说明不需要 PR 草稿块。

### ExecPlan（执行计划）

仅当变更影响最新发布标签中的行为或已发布/明确支持的持久外部状态边界时，才在计划早期指出兼容性风险，并在实施前确认方案。

满足以下条件时使用 ExecPlan：
- 工作是多步骤的、跨多个文件的。
- 涉及新功能或重构。
- 预计耗时超过约一小时。

从 `PLANS.md` 中的模板和规则开始，在执行过程中持续更新里程碑和活动章节（进展、意外发现、决策日志、成果与复盘）。如果范围发生变化，重写计划。若刻意跳过 ExecPlan，请在回复中说明原因。

### 公开 API 位置兼容性

将导出运行时 API 的参数顺序和 dataclass 字段顺序视为兼容性契约。

- 对于公开构造函数（例如 `{{PUBLIC_CONSTRUCTOR_EXAMPLES}}`），保留现有位置参数的含义。不得在现有公开参数顺序的中间插入新的构造函数参数或 dataclass 字段。
- 新增可选字段/参数时，尽可能追加到末尾，并保持旧字段顺序不变。
- 如果重新排序不可避免，需添加兼容层并编写测试覆盖旧的位置调用模式。
- 建议在调用处使用关键字参数以减少意外破坏，但不能以此为由打破公开 API 的位置兼容性。

### 平台、文档与安全审查

- 文档发布到线上站点，因此 SDK 行为变更与文档变更必须协调。若文档描述的行为尚未发布，要么推迟文档变更至 SDK 发布后，要么拆分为后续 PR。
- 将可运行的文档代码片段视为 API 兼容性检查。在添加 {{PLATFORM_API_EXAMPLES}} 示例前，对照实际实现验证所展示的参数和调用形式。
- 不得允许不可信的沙箱 manifest 数据绕过宿主文件系统或基目录边界。本地源代码实体化的逃生舱口必须由调用处的可信应用代码控制，不能由序列化的 manifest 数据决定。
- 在记录沙箱或安全授权时，验证实际实现路径是否执行了该授权或边界。除非相关路径确实参考了该授权，否则不得声明授权适用于 `LocalDir`、`LocalFile`、归档解压或其他实体化路径。
- {{REDACTION_GUIDANCE}}
- 对于 {{PLATFORM_NAME}} 平台或 SDK 特定的文档变更，优先使用 `${{DOMAIN_KNOWLEDGE_SKILL}}` 获取权威平台行为，并检查本地代码路径以了解 SDK 行为。在记录 {{PLATFORM_API_SURFACE}} 时，不要依赖通用 API 假设。

---

## 项目结构指南

### 概述

{{PROJECT_NAME}} 仓库提供 {{PROJECT_DESCRIPTION}}。使用 `{{RUN_COMMAND}} python ...` 执行 Python 命令，以确保环境一致。

### 仓库结构与重要文件

- `{{SOURCE_DIR}}`：核心库实现。
- `{{TEST_DIR}}`：测试套件；快照测试说明见 `{{TEST_DIR}}/README.md`。
{{#if EXAMPLES_DIR}}
- `{{EXAMPLES_DIR}}`：展示 SDK 用法的示例项目。
{{/if}}
- `{{DOCS_DIR}}`：{{DOCS_TOOL}} 文档源码{{#if TRANSLATED_DOCS_DIRS}}；不要编辑 `{{TRANSLATED_DOCS_DIRS}}` 下的翻译文档（自动生成）{{/if}}。
{{#if DOCS_SCRIPTS_DIR}}
- `{{DOCS_SCRIPTS_DIR}}`：文档工具，包括翻译和参考文档生成。
{{/if}}
{{#if DOCS_CONFIG_FILE}}
- `{{DOCS_CONFIG_FILE}}`：文档站点配置。
{{/if}}
- `Makefile`：常用开发命令。
- `{{PACKAGE_CONFIG_FILES}}`：Python 依赖和工具配置。
- `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`：提交 PR 时使用的模板。
{{#if DOCS_BUILD_OUTPUT_DIR}}
- `{{DOCS_BUILD_OUTPUT_DIR}}`：文档构建输出目录。
{{/if}}

{{#if REPOSITORY_TREE}}
### 仓库结构树

下面是仓库的高层目录结构，用于帮助 agent 快速建立项目地图。它应该保持简短，只展示主要目录、关键入口和需要避开的生成物，不要替代上面的架构规则和 domain knowledge。

```text
{{REPOSITORY_TREE}}
```
{{/if}}

### 核心运行时准则

<!--
  【Domain Knowledge 区域】
  
  这里填入 AI agent 在修改代码时必须遵守的项目特有架构规则。
  这些知识无法从文件扫描中自动获得，需要由熟悉代码库的人（或深度分析后的 AI）来填写。
  
  填写建议：
  1. 入口文件和模块边界约束（哪个文件是入口，逻辑应该放哪里）
  2. 跨文件联动规则（改 A 必须同步改 B 和 C）
  3. 需要保持一致的平行路径（例如流式与非流式实现）
  4. 状态/Schema 版本管理规则（版本号在哪里，改了要做什么）
  
  ──────────────────────────────────────
  示例一：入口文件约束
  ──────────────────────────────────────
  - `{{RUNTIME_ENTRYPOINT}}` 是运行时主入口，只负责编排和对外流程控制。
    新的运行时逻辑放在 `{{RUNTIME_INTERNAL_DIR}}/` 下，再从入口文件 import。
  - 当入口文件变大时，将辅助逻辑重构到 `{{RUNTIME_INTERNAL_DIR}}/` 的子模块中，
    入口文件只保留连接和组合逻辑。

  ──────────────────────────────────────
  示例二：跨文件协调规则
  ──────────────────────────────────────
  - 新增 `{{COORDINATED_CHANGE_TRIGGER}}` 时，需要同步更新以下所有文件：
    - `{{COORDINATED_FILE_1}}`（{{COORDINATED_FILE_1_REASON}}）
    - `{{COORDINATED_FILE_2}}`（{{COORDINATED_FILE_2_REASON}}）
    - `{{COORDINATED_FILE_3}}`（{{COORDINATED_FILE_3_REASON}}）
  - 若 `{{SCHEMA_FILE}}` 中的序列化结构发生变化，需同步更新
    `{{SCHEMA_VERSION_FIELD}}` 并在 `{{SCHEMA_SUMMARY_FIELD}}` 中补充版本说明。
  ──────────────────────────────────────
-->

---

## 操作指南

### 前提条件

- {{LANGUAGE_VERSION}}。
- 已安装 `{{PACKAGE_MANAGER}}`（用于依赖管理）并使用 `{{RUN_COMMAND}}` 运行命令。
- {{OPTIONAL_BUILD_TOOL_PREREQ}}

### 开发工作流

1. 与 `main` 同步并创建功能分支：
   ```bash
   git checkout -b feat/<简短描述>
   ```
2. 如果依赖发生变化或首次配置仓库，运行 `{{SYNC_COMMAND}}`。
3. 实现变更，并同步新增或更新测试。
4. 在实施会改变最新发布行为或已发布/明确支持的持久外部状态边界的变更前，在计划中指出兼容性或 API 风险。
{{#if HAS_DOCS_BUILD}}
5. 修改文档时构建文档：
   ```bash
   {{DOCS_BUILD_COMMAND}}
   ```
{{/if}}
6. 当适用 `$code-change-verification` 时，在标记工作完成前运行它以执行完整验证栈。
7. 用简洁的祈使句提交，保持提交小而聚焦，然后开启 PR。
8. 完成实质性代码工作并报告时，调用 `$pr-draft-summary` 作为最终交付步骤（符合文档中跳过条件的除外）。

### 测试与自动化检查

提交变更前，确保相关检查通过，并在修改代码时扩展测试覆盖。

当适用 `$code-change-verification` 时，从仓库根目录运行完整验证栈。应用修复后重新运行全套。

{{TOOLCHAIN_COMMANDS}}

<!-- 
  【Toolchain Commands 说明】
  builder 根据以下来源自动生成上面的命令块：
  1. 优先读取 Makefile target（format/lint/typecheck/tests/coverage）
  2. 其次读取 pyproject.toml 中的 [tool.pytest]、[tool.ruff]、[tool.mypy] 等配置
  3. 再次检查 CI workflow 文件（.github/workflows/）中实际运行的命令
  4. 以上均找不到时，使用通用兜底命令（python -m pytest / ruff check 等）
  
  兜底示例（无 Makefile 的项目）：
  - 运行测试：`{{RUN_COMMAND}} pytest`
  - 格式化：`{{RUN_COMMAND}} {{LINT_TOOL}} format .`
  - Lint：`{{RUN_COMMAND}} {{LINT_TOOL}} check .`
-->

### 工具与技巧

- 安装或刷新开发依赖：`{{SYNC_COMMAND}}`
- 查阅 `{{TIPS_REFERENCE}}`（Makefile / pyproject.toml）了解所有可用命令。
- 使用 `{{RUN_COMMAND}}` 运行 Python 命令以确保环境一致。
{{#if EXAMPLES_DIR}}
- 浏览 `{{EXAMPLES_DIR}}/` 查看常见用法示例。
{{/if}}

### Pull Request 与提交规范

- 使用 `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` 模板；包含摘要、测试计划和 Issue 编号（如适用）。
- 有新行为时尽可能添加测试，面向用户的变更需更新文档。
- 标记为 Ready 前运行 `make format`、`make lint`、`make typecheck` 和 `make tests`。
- Commit 消息简洁，使用祈使句；小而聚焦的提交优先。

### 审查流程与审查者关注点

- ✅ 检查通过（`make format`、`make lint`、`make typecheck`、`make tests`）。
- ✅ 测试覆盖新行为和边界情况。
- ✅ 代码可读、可维护，且与现有风格一致。
- ✅ 公开 API 和面向用户的行为变更已记录在文档中。
- ✅ 行为变更时示例已同步更新。
- ✅ 提交历史清晰，PR 描述完整。
