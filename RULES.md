# HarnessKit Harness Rules

本文件是 HarnessKit 仓库的 agent 约束索引。Rule 不是 workflow，也不是通用工程建议；Rule 只记录本仓库里永远或局部必须成立的约束。

每条规则必须有对应 details 文件，放在 [.harnesskit/rules/](.harnesskit/rules/)。[RULES.md](RULES.md) 负责告诉 agent “什么不能破坏”，details 文件负责说明“为什么、证据是什么、如何验证”。

下面的分类只是整理规则的抽屉，不是启用依据。每条已启用规则都必须有本仓库事实或团队确认支撑。

## 通用工程实践

- RULE-ENG-001: 修改用户可见行为时，必须同步添加或更新自动化测试。([details](.harnesskit/rules/RULE-ENG-001.md))
- RULE-ENG-002: 新增第三方依赖时，必须同步更新 [pyproject.toml](pyproject.toml) 和 [uv.lock](uv.lock)。([details](.harnesskit/rules/RULE-ENG-002.md))
- RULE-ENG-003: 需要完整验证的变更必须使用 `make verify` 作为验证入口。([details](.harnesskit/rules/RULE-ENG-003.md))
- RULE-ENG-004: 不要把本仓库未配置的 typecheck、coverage、docs build 或 CI 写成完成条件。([details](.harnesskit/rules/RULE-ENG-004.md))
- RULE-ENG-005: 发布、部署或托管相关判断必须以仓库配置或团队确认为准，不要把局部 docs 托管配置推断成 package release、CI 或生产部署门槛。([details](.harnesskit/rules/RULE-ENG-005.md))

## AI Coding 规则

- RULE-AI-001: 代码和生成行为判断必须基于已核对的仓库事实。([details](.harnesskit/rules/RULE-AI-001.md))
- RULE-AI-002: 不要把模板示例、设计愿景或旧文档当成当前实现事实。([details](.harnesskit/rules/RULE-AI-002.md))
- RULE-AI-003: 发现代码、文档、rules、skills 或验证入口冲突时，先核对仓库事实再同步 context。([details](.harnesskit/rules/RULE-AI-003.md))
- RULE-AI-004: 未经用户明确要求，不要重排、合并、删除已有客户手写规则。([details](.harnesskit/rules/RULE-AI-004.md))

## 技术栈规则

- RULE-STACK-001: Python 命令优先通过 `uv run ...` 使用仓库环境执行。([details](.harnesskit/rules/RULE-STACK-001.md))
- RULE-STACK-002: Python 代码和测试变更必须通过 Ruff lint 和 Ruff format check。([details](.harnesskit/rules/RULE-STACK-002.md))
- RULE-STACK-003: 测试入口是 `uv run pytest`，不要把其他测试框架写进验证计划。([details](.harnesskit/rules/RULE-STACK-003.md))
- RULE-STACK-004: 影响 package、模板打包或构建配置时，必须确认 `uv build` 通过。([details](.harnesskit/rules/RULE-STACK-004.md))

## 架构规则

- RULE-ARCH-001: CLI/runtime 行为以 [src/harnesskit/](src/harnesskit/) 和对应测试为事实来源。([details](.harnesskit/rules/RULE-ARCH-001.md))
- RULE-ARCH-002: [templates/](templates/) 是用户可见生成输出，模板行为变化必须同步 init 测试。([details](.harnesskit/rules/RULE-ARCH-002.md))
- RULE-ARCH-003: `harnesskit lint` 的产品入口必须来自 [src/harnesskit/linter/](src/harnesskit/linter/)。([details](.harnesskit/rules/RULE-ARCH-003.md))
- RULE-ARCH-004: 重要路径、职责或生成资产变化时，必须同步 [ARCHITECTURE.md](ARCHITECTURE.md)。([details](.harnesskit/rules/RULE-ARCH-004.md))

## 产品 / 领域规则

- RULE-DOMAIN-001: HarnessKit 当前 MVP 只负责 Context Harness，不实现 agent runtime、沙箱或多 agent 编排。([details](.harnesskit/rules/RULE-DOMAIN-001.md))
