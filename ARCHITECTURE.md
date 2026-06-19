# 架构地图

本文件是 HarnessKit 的粗粒度仓库地图。它帮助 agent 和贡献者在修改前找到正确的代码区域。本文件不是工作流规范、API 参考、详细设计文档或完整文件清单。

下面的 Markdown 链接就是地图。带有 `<!-- harnesskit:coverage=direct-children -->` 的路径会要求 linter 检查它的直接子项是否也在本文中以链接形式表示。只有当 direct-child coverage 本身能帮助防漂移时，才加 coverage marker。

## 顶层地图

- [`src/harnesskit/`](src/harnesskit/)：打包后的 HarnessKit 运行时代码。修改 CLI、初始化行为、integration 安装、模板渲染、`.harnesskit/config.json` 写入或 `harnesskit lint` 时看这里。
  - [`cli.py`](src/harnesskit/cli.py)：Typer 命令面，定义 `harnesskit init`、`harnesskit lint`、`harnesskit integration ...` 和 `--version`。
  - [`init.py`](src/harnesskit/init.py)：初始化引擎，负责项目路径解析、内置模板复制、Jinja `StrictUndefined` 渲染、companion 文件、Codex skills、integration 校验和 `.harnesskit/config.json` 写入。
  - [`linter/`](src/harnesskit/linter/)：打包进 CLI 的 Context Harness linter runtime。规则分组在 `rules/` 下，shared models/helpers 在 `core/` 下；新增产品 lint 行为优先落在这里。
- [`templates/`](templates/)：`harnesskit init` 复制到目标仓库的内置资产。这里的改动会影响生成的 harness 输出，应视为用户可见模板行为，并通常同步 init 测试。
- [`tests/`](tests/)：打包 CLI/init 行为的 pytest 测试，覆盖生成文件、配置写入、integration 安装、跳过/强制覆盖行为、未补全模板标记和 shared skill 输出。
- [`harness-linter-poc/`](harness-linter-poc/)：旧 Context Harness linter POC/参考实现，不是当前产品入口。新增产品行为应优先落在 [`src/harnesskit/linter/`](src/harnesskit/linter/)。
- [`.agents/skills/`](.agents/skills/)：本仓库工作时使用的 Codex 本地技能。这里应与根目录 [AGENTS.md](AGENTS.md)、[RULES.md](RULES.md)、模板和验证 runner 保持一致。
- [`.harnesskit/`](.harnesskit/)：HarnessKit 状态、facts、可选 rule details 和验证 receipts；`.harnesskit/facts.md` 是 scan/fill 中间事实快照，不替代真实源码、配置、脚本或 runner。
- [`scripts/`](scripts/)：仓库维护脚本；当前包含 [`publish_pypi.sh`](scripts/publish_pypi.sh)，作为 `make publish` 的手动 PyPI 发布入口。
- [`docs/`](docs/)：产品、设计、实践指导、路线图、进展文档和 GitHub Pages 静态站点资产。设计类文档位于 [`docs/design/`](docs/design/)，代码风格、产品体验、安全和可靠性判断指导位于 [`docs/practices/`](docs/practices/)。

## 关键文件

- [`pyproject.toml`](pyproject.toml)：Python 包元数据、运行时依赖、console script 入口、Hatchling 构建配置和 dev dependency group；PyPI 分发名是 `infharness`，console script 是 `harnesskit`。
- [`uv.lock`](uv.lock)：`uv` 锁文件；新增或变更第三方依赖时必须同步。
- [`Makefile`](Makefile)：验证和发布入口 wrapper；`make verify` 调用 code-change-verification runner，`make publish` 调用 PyPI 发布脚本。
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml)：pre-commit hook 配置，绑定 Ruff、harness lint、pytest、Markdown link check 和 package build。
- [`AGENTS.md`](AGENTS.md)：本仓库的顶层 agent 路由指南，指向规则、skills、架构地图和验证入口。
- [`RULES.md`](RULES.md)：本仓库基于证据沉淀的短规则索引；规则不要求一条对应一个 details 文件。
- [`README.md`](README.md)：产品定位、MVP 范围、CLI 使用方式和 Context Harness 总览。

## 生成资产和外部状态

HarnessKit 会在目标仓库中安装或维护这些文件：

- `AGENTS.md`：目标仓库的 agent 路由指南，由 [`templates/AGENTS.md`](templates/AGENTS.md) 生成。
- `ARCHITECTURE.md`：目标仓库的仓库地图模板，由 [`templates/ARCHITECTURE.md`](templates/ARCHITECTURE.md) 生成。
- `RULES.md`：目标仓库的规则模板，由 [`templates/RULES.md`](templates/RULES.md) 生成。
- `CLAUDE.md`：指向 `AGENTS.md` 的 companion 文件；`codex` 和 `claude` integration 当前都把它生成为符号链接。
- `.harnesskit/config.json`：HarnessKit 状态文件，包含 `schema_version`、`project_name`、`default_integration` 和 `installed_integrations`。
- `.harnesskit/facts.md`：scan/fill 管道的中间事实快照。
- `.agents/skills/*/SKILL.md`：从 [`templates/skills/`](templates/skills/) 安装的 Codex skill 说明。

## 边界说明

- 当前运行时包刻意保持很小：CLI、init、linter 和模板资产是主要用户可见面；不要把旧 POC 或 docs 设计愿景当成当前产品入口。
- [`templates/`](templates/) 是用户可见生成输出，不是本仓库当前事实本身；不要把模板占位符复制成本仓库事实。
- [`.harnesskit/facts.md`](.harnesskit/facts.md) 是 scan/fill 输入，不是日常高影响判断的最终事实源；高影响判断仍应回到源码、配置、脚本、测试和 runner。
- [`.harnesskit/rules/`](.harnesskit/rules/) 中的 `RULE-*.md` 是可选背景/details 层；当前 [RULES.md](RULES.md) 不要求每条规则都有 details 文件。
- [`docs/`](docs/) 当前作为 GitHub Pages 静态站点资产；这不等于 package release、CI 或生产部署 gate 已配置。

## 相关文档

- [`README.md`](README.md)：产品概览、MVP 边界和 CLI 使用方式。
- [`docs/design/`](docs/design/)：AGENTS、RULES、Validation 和 Harness Builder 模型的设计笔记。
- [`docs/practices/`](docs/practices/)：代码风格、产品体验、安全和可靠性判断指导；不替代 [`RULES.md`](RULES.md) 的硬约束。
- [`docs/ROADMAP.md`](docs/ROADMAP.md)：面向未来的产品和实现路线图。

## 更新规则

当主要目录、关键文件、生成输出、验证入口或模块职责发生变化时，同步更新本文件。只有当新模块改变 agent 首先应该查看的位置时，才把它加入这里；不要因为每个 helper 函数移动就更新本地图。
