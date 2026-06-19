# Product Sense Practices

本文件记录从 HarnessKit 当前产品文档、CLI、模板和路线图中提取的产品判断约定。它回答“这个项目里什么算产品体验”，不重复通用产品设计建议。硬约束见 [RULES.md](../../RULES.md)。

## 产品定位

- HarnessKit 服务已有代码仓库的维护者和使用 AI agent 的工程团队，核心结果是让 agent 稳定获得项目背景、目录职责、规则和验证入口。
- 当前产品是 Python CLI 与 agent-facing toolkit；MVP 聚焦 Context Harness 初始化和维护，不服务 agent runtime、工具沙箱、多 agent 编排或长期调度。
- 产品体验优先级是清晰、可审查、默认保守和可验证；生成资产应帮助 agent 少猜测，而不是制造更多文档噪音。

## 产品 Surface

### 用户入口

- 主要用户入口是 `harnesskit` CLI：`init` 初始化 harness，`integration list/install` 管理 integration，`lint` 检查 context drift。
- PyPI 分发名是 `infharness`，安装后的 console script 是 `harnesskit`；产品文案要避免把包名和命令名混淆。
- 用户会直接感知 CLI 参数、默认 integration、错误消息、生成文件、`.harnesskit/config.json`、`CLAUDE.md` symlink、`.agents/skills/` 和 lint 输出。
- CLI 失败输出应短而可修复；linter issue 应尽量给出 `found`、`expected`、证据或 suggested fix。

### 配置和默认行为

- `.harnesskit/config.json` 是 HarnessKit 状态文件；当前 schema version 是 `1`，支持 `codex` 和 `claude` integration。
- `codex` 是默认 integration；非交互终端下 `init` 会回退到默认 integration，显式 `--no-integration` 才跳过 integration assets。
- `init` 默认跳过已有文件，只有 `--force` 才覆盖；这条体验边界保护目标仓库中用户手写的 context。
- Jinja 模板使用 `StrictUndefined`；新增模板变量必须同步 render context，或明确保留目标仓库里的待确认占位。

### 生成输出和集成

- HarnessKit 生成的是 agent-facing context 资产：`AGENTS.md`、`ARCHITECTURE.md`、`RULES.md`、practice docs、`.harnesskit/facts.md`、可选 rule details、integration companion 和 Codex skills。
- 生成资产应容易审查、可手工维护、能被后续 skills/linter 校验；不要写成营销页、完整知识库或不可编辑的黑盒产物。
- `codex` integration 安装 `.agents/skills/` 和验证入口；`claude` integration 生成指向 `AGENTS.md` 的 companion 文件。
- `harnesskit lint` 的产品职责是保护 harness 文件不腐坏、不漂移；不要把它包装成通用代码 linter、formatter 或目标项目质量平台。

## 文档约定

- [README.md](../../README.md) 负责产品定位、MVP 边界、CLI 使用方式和当前支持能力。
- [AGENTS.md](../../AGENTS.md) 负责 agent 路由；[RULES.md](../../RULES.md) 负责硬约束；[ARCHITECTURE.md](../../ARCHITECTURE.md) 负责仓库地图；`docs/practices/` 负责判断指导。
- [docs/design/](../design/) 记录设计理念和未来方向，不等于当前实现事实；产品声明仍要回到源码、测试、配置或团队确认。
- `docs/` 当前作为 GitHub Pages 静态站点资产；不要把它推断成 package release、CI 或生产部署 gate。

## 风险边界

- 写产品能力前先区分当前已支持、可选 integration、生成资产、实验 POC、路线图和愿景。
- `harness-linter-poc/` 是旧参考实现，不是当前产品入口；新增 lint 能力应以 [`src/harnesskit/linter/`](../../src/harnesskit/linter/) 为准。
- 不要暗示 HarnessKit 会接管目标项目自身代码风格、自动进化 harness、运行 agent、托管沙箱或编排多 agent。
- 用户可见文案和模板 TODO 必须诚实：未确认事实保留 `NEEDS CLARIFICATION`，不要用示例填成事实。

## 和 Rules 的关系

产品相关硬约束见 [RULES.md](../../RULES.md)。本文件只帮助判断“这个仓库里的产品体验通常应该怎么理解”。
