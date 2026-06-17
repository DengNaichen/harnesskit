# HarnessKit Agent Guide

本文件是 HarnessKit 仓库的 agent 启动入口：保留少量会影响操作判断的事实，并把 agent 路由到规则、架构地图、skills 和验证入口。它不是项目知识库；完整目录职责看 `ARCHITECTURE.md`，工程约束看 `RULES.md`，具体流程看 `.agents/skills/*/SKILL.md`，产品背景看 `README.md` 和 `docs/`。

## 操作关键事实

- HarnessKit 是 Python 3.11+ 的 Context Harness CLI/toolkit，使用 `uv`；具体技术栈和路径职责看 `ARCHITECTURE.md`。
- 用户可见边界包括 CLI/runtime、`.harnesskit/config.json`、模板输出、integration 输出和 `harnesskit lint`。
- 当前配置 schema version 是 `1`；支持 `codex` 和 `claude` integration，`codex` 是默认值。
- 模板会写入目标仓库并使用 Jinja `StrictUndefined`；改模板时必须确认渲染上下文。
- 本仓库 agent 指南、rules、skills 和模板默认面向中文团队语境；除 `name`、命令、路径、代码标识和必要英文术语外，新增或重写语义说明时优先使用中文。
- 根目录 `AGENTS.md` 是本仓库当前生效的 agent 指南；`templates/AGENTS.md` 是生成到目标仓库的通用模板。两者应保持结构意图一致，但不要求内容一致；不要把本仓库事实无证据复制进模板，也不要把模板占位符当成本仓库事实。
- `.agents/skills/` 是本仓库当前生效的本地 skills；`templates/skills/` 是生成到目标仓库的通用 skill 模板。两边应保持结构意图一致，但不要求内容一致；不要把本仓库专属流程无证据复制进模板。
- `CLAUDE.md` 应保持为指向 `AGENTS.md` 的 companion 文件。

## 上下文路由

- 开始任务前先读 `RULES.md`，并按 `.harnesskit/rules/<RULE-ID>.md` 查看适用规则的证据、验证方式和例外。
- 涉及路径职责、实现边界、生成资产或旧/新实现取舍时，读 `ARCHITECTURE.md`，不要把本文件扩写成目录地图。
- 需要产品定位、MVP 边界、设计背景或路线图时，读 `README.md` 和 `docs/`。
- 触发本地 skill 时，先读对应 `SKILL.md`；不要把 skill 正文复制进本文件。
- `.harnesskit/facts.md` 是扫描事实快照，可用于刷新 context，但高影响判断仍要回到真实仓库文件核对。

## 工作策略

- 修改运行时代码、导出 API、CLI 命令或参数、外部配置、`.harnesskit/config.json`、模板输出、测试或其他用户可见行为前，先使用 `$implementation-strategy` 明确兼容性边界。
- 影响 `src/harnesskit/`、`templates/`、`tests/`、`pyproject.toml`、`uv.lock`、Markdown 链接或构建/测试行为的变更，在完成前使用 `$code-change-verification`。
- 中等及以上规模的运行时代码、测试、模板、构建配置或有行为影响的文档变更完成后，按 `$pr-draft-summary` 输出 PR 草稿块；纯仓库元数据或无行为影响的文档任务可跳过。
- 模板行为变化要当作用户可见行为处理，通常需要同步 `tests/test_init.py`；`init_project()` 默认跳过已有文件，只有 `--force` 才覆盖。
- 不要未经用户明确要求重排、合并、删除已有客户手写规则；新增稳定规则时，同步 `RULES.md` 和对应 details 文件。
- 修改 `ARCHITECTURE.md` 或 `templates/ARCHITECTURE.md` 时，不要机械调用 `$fill-architecture`；如果 architecture skill 本身也在调整或与当前职责分层原则冲突，先按本文件的分层原则直接处理，并同步修正 skill。

## 验证入口

完整验证入口是 `make verify`。当前没有已证实的 type checker、coverage gate、docs build 命令、CI 或 GitHub PR 模板；不要在指南、总结或验证计划里虚构这些完成条件。

维护验证说明时区分 Rule、Validation 和 Runner：Rule 是约束，Validation 是检查方式，Runner 是实际执行位置。没有 runner 证据的检查只能标记为人工执行、agent 执行或未绑定。

<!-- harnesskit:verification:start -->
- Full verification: make verify
- Markdown links: lychee './**/*.md'
- Python lint: uv run ruff check .
- Python format: uv run ruff format --check .
- Tests: uv run pytest
- Package build: uv build
- Pre-commit hooks: uv run pre-commit run --all-files
<!-- harnesskit:verification:end -->

验证失败后修复问题并重新运行同一验证命令；最终交付只报告最终状态。

## 漂移处理

如果 `AGENTS.md`、`RULES.md`、`ARCHITECTURE.md`、skills、验证入口或项目命令互相冲突，不要静默选择一边；先用仓库事实核对，再同步修复漂移的 context 文件。

文档职责保持分离：`AGENTS.md` 讲 agent 如何开始和路由，`RULES.md` 讲不能破坏的约束，`ARCHITECTURE.md` 讲仓库地图，skills 讲任务流程，`README.md` 和 `docs/` 讲产品与设计背景。
