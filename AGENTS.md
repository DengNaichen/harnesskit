# 贡献者指南

本指南是 HarnessKit 仓库的 agent 操作入口。它应保持简洁、面向规则和导航；项目定位、产品背景和长期设计讨论放在 `README.md`、`docs/DESIGN.md` 或 `docs/` 中。

## 策略与强制规则

### 必须按需使用仓库本地技能

仓库本地技能位于 `.agents/skills/`。触发条件满足时，先阅读对应 `SKILL.md`，再执行任务；不要把技能正文复制进本文件。

- `$implementation-strategy`：在修改运行时代码、导出 API、CLI 命令/参数、外部配置、`.harnesskit/config.json`、模板输出、测试或其他面向用户的行为之前使用。兼容性判断以最新发布标签为基准，而不是未发布的本地分支改动。
- `$code-change-verification`：当变更影响 `src/harnesskit/`、`templates/`、`tests/`、`pyproject.toml`、`uv.lock`、Markdown 链接或构建/测试行为时，在标记完成前运行。当前完整验证栈是 `lychee './**/*.md'` 和 `uv run pytest`。
- `$pr-draft-summary`：完成中等及以上规模的运行时代码、测试、模板、构建配置或有行为影响的文档变更后，在最终交付中生成 PR 草稿块。纯仓库元数据或无行为影响的文档任务可跳过。

### 可跳过完整验证的情况

以下变更默认不需要运行 `$code-change-verification`，除非用户明确要求：

- 仅修改 `AGENTS.md`、`.agents/` 或其他 agent 元数据。
- 仅修改 `README.md`、`design.md`、`docs/` 等无行为影响的说明文档。
- 仅进行对话、审查或规划，没有改动文件。

### 兼容性边界

HarnessKit 是 Context Harness CLI 和 Codex-facing toolkit。以下面向外部使用者或目标仓库，修改前必须明确兼容性决策：

- Typer CLI：`harnesskit init`、`harnesskit integration list`、`harnesskit integration install`、参数、退出行为和用户可见消息。
- 持久配置：目标仓库中的 `.harnesskit/config.json`，当前 `schema_version` 为 `1`。
- 模板输出：`templates/` 以及 integration 模板会复制或渲染到目标仓库，属于用户可见行为。
- 支持的 integration：当前仅支持 `codex`，并且它是默认值。
- Jinja 模板使用 `StrictUndefined`；新增模板变量必须同步提供渲染上下文，或明确保留为目标仓库中的 TODO。

## 项目结构

### 概述

HarnessKit 是 Python 3.11+ 项目，使用 Typer 构建 CLI，Rich 输出终端信息，Jinja2 渲染模板，Hatchling 构建包。使用 `uv` 管理和运行本仓库命令。

### 重要目录与文件

- [`src/harnesskit/`](src/harnesskit/)：核心库和 CLI 实现。
- [`src/harnesskit/cli.py`](src/harnesskit/cli.py)：Typer 入口，定义 `harnesskit init` 和 `harnesskit integration ...` 命令。
- [`src/harnesskit/init.py`](src/harnesskit/init.py)：项目初始化、模板复制、integration 安装和 `.harnesskit/config.json` 写入逻辑。
- [`templates/`](templates/)：`harnesskit init` 安装到目标仓库的 Context Harness 模板；其中 [`templates/integrations/codex/`](templates/integrations/codex/) 存放 Codex integration 资产。
- [`tests/`](tests/)：`pytest` 测试套件，当前重点覆盖初始化、integration 安装、跳过/覆盖文件和配置写入。
- [`.agents/skills/`](.agents/skills/)：本仓库的 Codex 本地技能，定义验证、实现策略、PR 草稿和 agent 指南刷新流程。
- [`README.md`](README.md)：产品定位、MVP 边界、CLI 使用方式和 Context Harness 说明。
- [`docs/DESIGN.md`](docs/DESIGN.md)：Harness Builder MVP 设计讨论，包含 Scan -> Rule -> Guard 模型。
- [`docs/references/harness-builder/`](docs/references/harness-builder/)：harness 研究笔记和参考资料。
- [`candidate.md`](candidate.md)：日常发现的命令、约定、坑和待确认事项暂存区；不是权威规则，定期回看后再沉淀到指南、技能或文档。
- [`pyproject.toml`](pyproject.toml)：项目元数据、依赖、脚本入口和 Hatchling 构建配置。
- [`lychee.toml`](lychee.toml)：Markdown 链接检查配置，默认只检查本地链接。
- [`uv.lock`](uv.lock)：锁定依赖版本。
- [`CLAUDE.md`](CLAUDE.md)：应保持为指向 [`AGENTS.md`](AGENTS.md) 的符号链接。

当前仓库没有 Makefile、formatter/type checker 配置、docs build 命令或 GitHub PR 模板；不要在指南、总结或验证计划里虚构这些检查。Markdown 链接 lint 使用 `lychee`，并由 [`lychee.toml`](lychee.toml) 限定为 offline 本地链接检查。

## 操作指南

### 环境与命令

- 首次配置或依赖变更后运行 `uv sync`。
- 运行 Python 命令时优先使用 `uv run python ...`，确保使用仓库环境。
- 本地 CLI 入口是 `uv run harnesskit ...`；也可以用 `uv run python -m harnesskit.cli` 只在确有需要时调试入口模块。
- Markdown 链接检查需要本机安装 `lychee`；本地可用 Homebrew 安装：`brew install lychee`。

### 开发工作流

1. 先读相关模块、测试和本地技能说明，确认变更触及的边界。
2. 如果会改变运行时、CLI、配置、模板输出或测试行为，先使用 `$implementation-strategy`。
3. 实现变更时同步更新测试；模板行为改变时，把它当作用户可见行为处理。
4. 日常发现可复用命令、仓库约定、坑或待确认事项时，先追加到 `candidate.md`；只有稳定且反复有用的内容才沉淀到 `AGENTS.md`、`.agents/skills/` 或文档。
5. 需要验证时从仓库根目录运行完整验证栈：`lychee './**/*.md'`，然后 `uv run pytest`。
6. 修复失败后重新运行同一验证命令，最终交付只报告最终状态。
7. 中等及以上规模的实质性代码工作完成后，按 `$pr-draft-summary` 输出 PR 草稿块。

### 测试与自动化检查

当前完整验证栈：

```bash
lychee './**/*.md'
uv run pytest
```

仓库目前没有可证实的 `make format`、`make typecheck` 或文档构建命令。除非相关配置被加入仓库，否则不要要求这些命令作为完成条件。

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
