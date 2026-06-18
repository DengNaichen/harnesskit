# HarnessKit Harness Rules

本文件是 HarnessKit 仓库的 agent 约束索引。Rule 不是 workflow，也不是通用工程建议；Rule 只记录本仓库里永远或局部必须成立的约束。

Skills 教 agent 怎么做一类任务；Rules 告诉 agent 在本仓库里必须遵守什么；verification runners 负责把可检查的约束变成可执行反馈。[AGENTS.md](AGENTS.md) 负责路由，`.agents/skills/` 负责流程，[RULES.md](RULES.md) 只保留短约束句，不负责承载 rationale、路径地图或 runner 细节。

Rules 不要求一条规则对应一个 details 文件。复杂背景进入 [ARCHITECTURE.md](ARCHITECTURE.md) 或 [docs/practices/](docs/practices/)；可执行或可跟踪检查进入验证入口、pre-commit hook、linter runtime 或其他 runner。

下面的分类只是整理规则的抽屉，不是启用依据。每条已启用规则都必须有本仓库事实或团队确认支撑。

## 通用工程实践

- RULE-ENG-001: 修改用户可见行为时，必须同步添加或更新自动化测试。
- RULE-ENG-002: 新增第三方依赖时，必须同步更新 [pyproject.toml](pyproject.toml) 和 [uv.lock](uv.lock)。
- RULE-ENG-003: 需要完整验证的变更必须使用 `make verify` 作为验证入口。
- RULE-ENG-004: 不要把本仓库未配置的 typecheck、coverage、docs build 或 CI 写成完成条件。
- RULE-ENG-005: 发布、部署或托管相关判断必须以仓库配置或团队确认为准，不要把局部 docs 托管配置推断成 package release、CI 或生产部署门槛。

## 代码风格与维护性

- RULE-STYLE-001: 代码变更必须遵循现有模块边界；跨边界重构需要明确理由和验证。

## 技术栈规则

- RULE-STACK-001: Python 命令优先通过 `uv run ...` 使用仓库环境执行。
- RULE-STACK-002: Python 代码和测试变更必须通过 Ruff lint 和 Ruff format check。
- RULE-STACK-003: 测试入口是 `uv run pytest`，不要把其他测试框架写进验证计划。
- RULE-STACK-004: 影响 package、模板打包或构建配置时，必须确认 `uv build` 通过。

## 架构规则

- RULE-ARCH-001: CLI/runtime 行为以 [src/harnesskit/](src/harnesskit/) 和对应测试为事实来源。
- RULE-ARCH-002: [templates/](templates/) 是用户可见生成输出，模板行为变化必须同步 init 测试。
- RULE-ARCH-003: `harnesskit lint` 的产品入口必须来自 [src/harnesskit/linter/](src/harnesskit/linter/)。
- RULE-ARCH-004: 重要路径、职责或生成资产变化时，必须同步 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 产品与体验规则

- RULE-PRODUCT-001: 用户可见文案和生成资产必须明确区分已支持能力、待确认占位和未来愿景。

## 安全规则

- RULE-SEC-001: 不要把 secret、token、私有凭据或机器特定敏感信息写入模板、facts、rules、报告或生成产物。
- RULE-SEC-002: 文件写入必须保持在目标项目内，且默认不得覆盖已有文件，除非用户显式选择覆盖。

## 产品 / 领域规则

- RULE-DOMAIN-001: HarnessKit 当前 MVP 只负责 Context Harness，不实现 agent runtime、沙箱或多 agent 编排。
