# 贡献者指南

本指南是 HarnessKit 仓库的 agent 操作入口。它应保持简洁、面向规则和导航；项目定位、产品背景和长期设计讨论放在 `README.md`、`docs/design/DESIGN.md` 或 `docs/` 中。

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

仓库本地技能位于 `.agents/skills/`。触发条件满足时，先阅读对应 `SKILL.md`，再执行任务；不要把技能正文复制进本文件。

### `RULES.md` 作为规则源

`RULES.md` 是本仓库已确认或待确认的工程规则清单和约束索引。`AGENTS.md` 只负责把 agent 路由到 `RULES.md`；不要在本文件里为每条 Rule 重复建立触发条件或决策树。

开始任务前先查看 `RULES.md`；执行时遵守其中适用的约束；交付前按 `RULES.md` details 和相关 skill 运行已绑定 Guard。

如果 `AGENTS.md`、skills、验证入口或项目命令与 `RULES.md` 不一致，不要静默选择一边；先用仓库事实核对，再同步修复漂移的 context 文件。

### 兼容性边界

HarnessKit 是 Context Harness CLI 和 Codex-facing toolkit。以下面向外部使用者或目标仓库，修改前必须明确兼容性决策：

- Typer CLI：`harnesskit init`、`harnesskit integration list`、`harnesskit integration install`、参数、退出行为和用户可见消息。
- 持久配置：目标仓库中的 `.harnesskit/config.json`，当前 `schema_version` 为 `1`。
- 模板输出：`templates/` 以及 integration 模板会复制或渲染到目标仓库，属于用户可见行为。
- 支持的 integration：当前仅支持 `codex`，并且它是默认值。
- Jinja 模板使用 `StrictUndefined`；新增模板变量必须同步提供渲染上下文，或明确保留为目标仓库中的 TODO。

### 当前实现边界

HarnessKit 现在同时在构建可安装到目标仓库的 CLI/toolkit，以及保护 harness 资产不腐坏的 linter/Guard 原型。修改前先分清边界：

- `src/harnesskit/` 是打包发布的 CLI/runtime；这里的改动按产品行为处理，会影响 `harnesskit init`、integration 命令和 `.harnesskit/config.json` 写入。
- `templates/` 是写入目标仓库的 harness 输出；这里的改动按用户可见模板行为处理，并同步 `tests/test_init.py`。
- `harness-linter-poc/` 是独立的 Context Harness linter POC，用于本仓库自举验证；它当前不属于 `src/harnesskit` 包运行时，也不是对外 CLI API，但会影响 `make verify`、pre-commit 和 harness 质量检查。
- `docs/design/` 记录设计理念；不要把设计文档里的“应该如何设计”误写成当前项目已经实现的状态。

## 上下文入口

HarnessKit 是 Python 3.11+ 项目，使用 Typer 构建 CLI，Rich 输出终端信息，Jinja2 渲染模板，Hatchling 构建包。使用 `uv` 管理和运行本仓库命令。

- [`ARCHITECTURE.md`](ARCHITECTURE.md)：完整仓库地图，查目录职责、关键文件和边界时先读它。
- [`RULES.md`](RULES.md)：工程规则、Guard 绑定和项目命令事实来源。
- [`.agents/skills/`](.agents/skills/)：本仓库的 Codex 本地技能；触发后再读对应 `SKILL.md`。
- [`README.md`](README.md) 和 [`docs/`](docs/)：产品定位、设计背景、路线图和研究材料。
- [`CLAUDE.md`](CLAUDE.md)：应保持为指向 [`AGENTS.md`](AGENTS.md) 的符号链接。

当前仓库有 `Makefile`，完整验证入口是 `make verify`；没有 type checker 配置、docs build 命令或 GitHub PR 模板，不要在指南、总结或验证计划里虚构这些检查。Markdown 链接 lint 使用 `lychee`，并由 [`lychee.toml`](lychee.toml) 限定为 offline 本地链接检查。

## 操作指南

### 开发工作流

1. 先读 `RULES.md`、相关模块、测试和本地技能说明，确认变更触及的边界。
2. 修改运行时代码、导出 API、CLI 命令/参数、外部配置、`.harnesskit/config.json`、模板输出、测试或其他面向用户的行为前，先使用 `$implementation-strategy`；兼容性判断以最新发布标签为基准，而不是未发布的本地分支改动。
3. 实现变更时同步更新测试；模板行为改变时，把它当作用户可见行为处理。
4. 日常发现可复用命令、仓库约定、坑或待确认事项时，优先记录到 `RULES.md` 的待确认条目、相关文档或本地技能说明中；只有稳定且反复有用的内容才沉淀为强规则。
5. 当变更影响 `src/harnesskit/`、`templates/`、`tests/`、`pyproject.toml`、`uv.lock`、Markdown 链接或构建/测试行为时，在标记完成前使用 `$code-change-verification`；当前完整验证入口是 `make verify`。
6. 修复失败后重新运行同一验证命令，最终交付只报告最终状态。
7. 中等及以上规模的运行时代码、测试、模板、构建配置或有行为影响的文档变更完成后，按 `$pr-draft-summary` 输出 PR 草稿块；纯仓库元数据或无行为影响的文档任务可跳过。

### 测试与自动化检查

#### Guard 与 Runner 绑定

维护 `RULES.md` 或验证说明时，区分 **Rule**、**Guard** 和 **Runner**：Rule 是要遵守的规则，Guard 是可执行检查，Runner 是实际运行这个检查的位置。不要只因为写了一个 Guard 命令就声称它能拦住问题；必须写清楚它绑定到了哪个 runner，以及证据来自哪里。

当前本仓库的主要 runner 是 `Makefile`、`$code-change-verification` 和 `.pre-commit-config.yaml`。如果未来接入 CI、SVN server hook、内部平台 gate 或其他 runner，同步更新 `RULES.md`、本节和验证 skill。没有 runner 证据的检查只能标记为人工执行、agent 执行或未绑定，不能写成强制拦截。

当前完整验证栈：

<!-- harnesskit:verification:start -->
- Full verification: make verify
- Markdown links: lychee './**/*.md'
- Python lint: uv run ruff check .
- Python format: uv run ruff format --check .
- Tests: uv run pytest
- Package build: uv build
- Pre-commit hooks: uv run pre-commit run --all-files
<!-- harnesskit:verification:end -->

仓库目前没有可证实的 `make typecheck` 或文档构建命令。除非相关配置被加入仓库，否则不要要求这些命令作为完成条件。

### 修改模板时的注意事项

- `templates/AGENTS.md` 和 integration 模板会影响新初始化项目的输出；改动后通常需要更新或新增 `tests/test_init.py` 覆盖。
- `init_project()` 默认跳过已有文件，`--force` 才覆盖；不要破坏这一行为。
- `install_integration()` 要求目标仓库已有 `.harnesskit/config.json`。
- `.harnesskit/config.json` 写入 JSON 时保留 `ensure_ascii=False` 和缩进风格，避免无意义 churn。

### Pull Request 与提交规范

- 提交信息使用简洁祈使句，保持提交小而聚焦。
- 有新行为时尽可能补测试；面向用户的 CLI、配置或模板变化需要同步文档。
- PR 描述应包含摘要和测试计划；如果使用 `$pr-draft-summary`，按其输出块作为草稿基础。

### 审查关注点

- CLI 行为、错误消息和退出码是否符合现有 Typer 风格。
- `.harnesskit/config.json` 的 schema 和 integration 列表是否保持兼容。
- 模板渲染是否有完整上下文，避免 `StrictUndefined` 在运行时失败。
- 新行为是否被 `pytest` 覆盖。
- 文档是否把项目说明和 agent 操作规则分开：`README.md` 讲产品，`AGENTS.md` 讲 agent 如何工作。
