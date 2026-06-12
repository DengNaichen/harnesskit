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
{{#if ARCHITECTURE_DOC}}
- `{{ARCHITECTURE_DOC}}`：架构分层、模块边界和项目地图；需要了解目录结构或模块职责时优先阅读。
{{/if}}
- `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`：提交 PR 时使用的模板。
{{#if DOCS_BUILD_OUTPUT_DIR}}
- `{{DOCS_BUILD_OUTPUT_DIR}}`：文档构建输出目录。
{{/if}}

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
