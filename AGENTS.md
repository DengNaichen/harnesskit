# HarnessKit Agent Guide

本文件是 HarnessKit 仓库的 agent 启动入口：保留少量会影响操作判断的事实，并把 agent 路由到规则、架构地图、skills 和验证入口。它不是项目知识库；完整目录职责看 [ARCHITECTURE.md](ARCHITECTURE.md)，工程约束看 [RULES.md](RULES.md)，具体流程看 [.agents/skills/](.agents/skills/)，产品背景看 [README.md](README.md) 和 [docs/](docs/)。

## 编码原则

## 1. 编码前先思考

**不要假设，不要掩盖困惑。**

实现之前：
- 先说明关键假设和不确定性。
- 多解读或高影响任务先确认，不要默默选择。
- 有更简单的方案时主动指出；不清楚就停下来问。

## 2. 简单优先

**用最少的代码解决问题。不要做推测性的扩展。**

- 不加用户没有要求的功能、抽象、配置项或兜底逻辑。
- 能用简单实现解决，就不要引入额外结构。
- 如果实现明显过重，先收敛到更小方案。

## 3. 外科手术式改动

**只改必须改的地方。只清理你自己造成的问题。**

- 不顺手改进相邻代码、注释或格式；不重构无关代码。
- 匹配现有风格，即使你会用不同方式实现。
- 只清理自己造成的未使用代码；发现无关死代码只说明。
- 未经用户明确要求，不要重排、合并或删除已有的用户手写规则、配置或文档结构。

## 4. 核实优先

**做判断前先核对真实文件。不要把二手信息当成事实。**

- 涉及运行时行为、配置、依赖、安全边界或模块职责的判断，必须回到源码、配置文件、脚本或构建清单核对。
- 不要把 README 中的演示说明、设计愿景、旧文档或中间产物当成当前实现事实。
- 发现文档、规则、skills 或验证入口互相冲突时，先核对仓库真实文件，再决定哪边是对的，不要静默选一边继续走。

## 操作关键事实

- HarnessKit 是 Python 3.11+ 的 Context Harness CLI/toolkit，使用 `uv`；PyPI 分发名是 `infharness`，安装后 console script 仍是 `harnesskit`；具体技术栈和路径职责看 [ARCHITECTURE.md](ARCHITECTURE.md)。
- 用户可见边界包括 CLI/runtime、[.harnesskit/config.json](.harnesskit/config.json)、模板输出、integration 输出和 `harnesskit lint`。
- [docs/](docs/) 当前作为 GitHub Pages 静态站点资产；不要再把 Vercel 当作本仓库的文档托管事实。
- 当前配置 schema version 是 `1`；支持 `codex` 和 `claude` integration，`codex` 是默认值。
- 模板会写入目标仓库并使用 Jinja `StrictUndefined`；改模板时必须确认渲染上下文。
- 本仓库 agent 指南、rules、skills 和模板默认面向中文团队语境；除 `name`、命令、路径、代码标识和必要英文术语外，新增或重写语义说明时优先使用中文。
- 根目录 [AGENTS.md](AGENTS.md) 是本仓库当前生效的 agent 指南；[templates/AGENTS.md](templates/AGENTS.md) 是生成到目标仓库的通用模板。两者应保持结构意图一致，但不要求内容一致；不要把本仓库事实无证据复制进模板，也不要把模板占位符当成本仓库事实。
- [.agents/skills/](.agents/skills/) 是本仓库当前生效的本地 skills；[templates/skills/](templates/skills/) 是生成到目标仓库的通用 skill 模板。两边应保持结构意图一致，但不要求内容一致；不要把本仓库专属流程无证据复制进模板。
- [CLAUDE.md](CLAUDE.md) 应保持为指向 [AGENTS.md](AGENTS.md) 的 companion 文件。

## 上下文路由

- 开始任务前先读 [RULES.md](RULES.md)，并按 [.harnesskit/rules/](.harnesskit/rules/) 查看适用规则的证据、验证方式和例外。
- 涉及路径职责、实现边界、生成资产或旧/新实现取舍时，读 [ARCHITECTURE.md](ARCHITECTURE.md)，不要把本文件扩写成目录地图。
- 需要产品定位、MVP 边界、设计背景或路线图时，读 [README.md](README.md) 和 [docs/](docs/)。
- 涉及代码风格、产品体验、安全或可靠性判断时，按需阅读 [docs/practices/](docs/practices/)；这些文件是判断指导，不替代 [RULES.md](RULES.md) 的硬约束。
- 触发本地 skill 时，先读 [.agents/skills/](.agents/skills/) 下对应 skill 文件；不要把 skill 正文复制进本文件。
- [.harnesskit/facts.md](.harnesskit/facts.md) 是 scan/fill 管道的中间事实快照，可用于刷新 context；日常高影响判断仍要回到真实仓库文件核对，不把 facts 当成最终指南。

## 工作策略

- 修改运行时代码、导出 API、CLI 命令或参数、外部配置、[.harnesskit/config.json](.harnesskit/config.json)、模板输出、测试或其他用户可见行为前，先使用 $implementation-strategy 明确兼容性边界。
- 影响 [src/harnesskit/](src/harnesskit/)、[templates/](templates/)、[tests/](tests/)、[pyproject.toml](pyproject.toml)、[uv.lock](uv.lock)、Markdown 链接或构建/测试行为的变更，在完成前使用 $code-change-verification。
- 中等及以上规模的运行时代码、测试、模板、构建配置或有行为影响的文档变更完成后，按 $pr-draft-summary 输出 PR 草稿块；纯仓库元数据或无行为影响的文档任务可跳过。
- 发布 PyPI 包时使用 `make publish`，它会通过 [scripts/publish_pypi.sh](scripts/publish_pypi.sh) 运行 `make verify`、清理并重建 `dist/`、再调用 `uv publish`；token 只能来自环境变量或被忽略的本地 `.env`。
- 模板行为变化要当作用户可见行为处理，通常需要同步 [tests/test_init.py](tests/test_init.py)；`init_project()` 默认跳过已有文件，只有 `--force` 才覆盖。
- 刷新 [docs/practices/](docs/practices/) 判断指导时，使用 $fill-practices；如果发现新的硬约束候选，再交给 $fill-rules 写入 [RULES.md](RULES.md) 和 details。
- 不要未经用户明确要求重排、合并、删除已有客户手写规则；新增稳定规则时，同步 [RULES.md](RULES.md) 和对应 details 文件。
- 修改 [ARCHITECTURE.md](ARCHITECTURE.md) 或 [templates/ARCHITECTURE.md](templates/ARCHITECTURE.md) 时，不要机械调用 $fill-architecture；如果 architecture skill 本身也在调整或与当前职责分层原则冲突，先按本文件的分层原则直接处理，并同步修正 skill。

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

如果 [AGENTS.md](AGENTS.md)、[RULES.md](RULES.md)、[ARCHITECTURE.md](ARCHITECTURE.md)、skills、验证入口或项目命令互相冲突，不要静默选择一边；先用仓库事实核对，再同步修复漂移的 context 文件。

文档职责保持分离：[AGENTS.md](AGENTS.md) 讲 agent 如何开始和路由，[RULES.md](RULES.md) 讲不能破坏的约束，[ARCHITECTURE.md](ARCHITECTURE.md) 讲仓库地图，skills 讲任务流程，[docs/practices/](docs/practices/) 讲判断指导，[README.md](README.md) 和 [docs/](docs/) 讲产品与设计背景。
