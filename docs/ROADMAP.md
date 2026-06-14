# Roadmap

HarnessKit 的路线聚焦 Context Harness：先初始化并维护 agent 可用的项目上下文，再逐步增加确定性的检查和更丰富的集成能力。

## 近期

- 内置 Codex skills：
  - `$harnesskit-audit`：只读审计当前仓库的 Context Harness 状态。
  - `$harnesskit-refresh`：补装或刷新 harness 资产，默认不覆盖已有文件。
  - `$harnesskit-explain`：解释当前仓库里的 HarnessKit 资产和使用方式。
- 保持 `harnesskit init` 和 `harnesskit integration install codex` 的输出资产容易审查、可重复安装、默认不覆盖已有文件。
- 继续把产品说明、agent 操作规则、设计理念和路线图分开放置。

## Harness Preservation

- 提供或整合确定性的 Harness Check / Harness Lint 能力。
- 检查和维护 HarnessKit 生成的 harness 资产，例如 `AGENTS.md`、`.agents/skills/`、`.harnesskit/config.json`、文档链接、验证入口和模板资产。
- 必要时提供安全的 `--fix` 能力。
- 不默认接管目标项目自身的代码风格，也不把它做成通用代码 linter 或 formatter。

## 后续方向

- 支持 Claude Code 或内部产品 integration。
- 增加仓库扫描能力，用项目事实预填或校验 harness。
- 扩展模板和机器生成事实。
- 引入 sensors、evals 和 evidence 收集。
- 把 Guard 的执行锚点从 git hook 扩展为更抽象的验证入口，以适配云端 agent 环境。

## 暂不做

- 不做 agent runtime、工具沙箱或长期运行 agent 的调度系统。
- 不做多 agent orchestration / controller。
- 不在 MVP 阶段追求 Harness Evolution，也就是让 harness 在使用中自动进化成更完整的架构体系。
