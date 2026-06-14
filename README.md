# mykit

`mykit` 是一个用于在现有仓库中初始化轻量级 Context Harness 的 CLI 与 Codex-facing toolkit。

它的目标是让 AI agent 能够稳定理解一个代码仓库：这个项目是什么、目录如何组织、开发和验证命令是什么、哪些工程规则不能被破坏，并在项目演进中保持这些上下文资产不腐坏、不漂移。这样用户不需要在每次对话里反复解释项目背景。

## 项目定位

`mykit` 会把一组 agent 友好的项目资产安装到目标仓库中。这些资产可以理解为面向 agent 的技术治理层，主要包括：

- 清晰的仓库入口说明
- 项目结构和架构边界
- 开发、测试和验证命令
- 质量、可靠性和安全规则
- agent 可以按需渐进式读取的参考资料

当前 MVP 只聚焦 **Context Harness**，并且只支持 Codex integration。`mykit` 不实现 agent runtime、工具沙箱、编排控制器，也不做长期运行 agent 的调度系统。

## 产品体验

`mykit` 本体仍然是 CLI，但真正的使用体验不是让用户反复手敲脚本，而是把 CLI 和 agent skills 配合起来：

1. 用户安装 `mykit`。
2. 在某个仓库里运行 `mykit init --here`，或运行 `mykit init <project>`。
3. `mykit` 初始化 Context Harness 核心资产。
4. `mykit` 同时安装 Codex skills 到 `.agents/skills/`。
5. 用户回到 Codex 对话框里，通过 `$mykit-*` skills 继续审计、刷新和解释 harness。

第一版内置三个 Codex skills：

- `$mykit-audit`：只读审计当前仓库的 Context Harness 状态。
- `$mykit-refresh`：补装或刷新 harness 资产，默认不覆盖已有文件。
- `$mykit-explain`：解释当前仓库里的 mykit 资产和使用方式。

## 为什么需要 Context Harness

AI agent 需要稳定、可复用、随代码一起演进的本地上下文，而不是依赖某一次对话里的临时说明。Context Harness 的作用，就是把项目知识沉淀成仓库中的文件：

- `AGENTS.md`：agent 的操作规则和仓库导航入口
- 架构或质量文档：更深入的工程约束
- 生成或人工整理的参考资料：避免 agent 凭空猜测关键事实
- 验证入口：把自然语言规则连接到可执行检查

`AGENTS.md` 应该保持克制，专注于“agent 在这个仓库里应该怎么工作”。至于 `mykit` 是什么、为什么存在、MVP 边界在哪里，这些项目定位说明应该放在 `README.md`。

## 当前结构

这个仓库目前包含：

- `src/mykit/`：Python CLI 实现
- `templates/`：`mykit init` 会安装到目标仓库的模板文件
- `docs/references/harness-builder/`：后续 harness 设计的研究笔记和参考资料

当前 CLI 暴露：

```bash
mykit init <project>
mykit init --here
mykit init --here --integration codex
mykit integration list
mykit integration install codex
```

`init` 会把内置模板复制到目标仓库，并写入 `.mykit/config.json`。如果目标文件已经存在，默认跳过；传入 `--force` 时才会覆盖。当前唯一支持的 integration 是 `codex`，它也是默认值。

## MVP 边界

近期产品边界应该保持小而清晰：

- 初始化一套最小 Context Harness
- 让 `AGENTS.md` 成为简洁的 agent 地图
- 安装 Codex 本地 skills 到 `.agents/skills/`
- 把项目说明和 agent 操作规则分开
- 让生成资产在进一步自动化之前保持容易审查
- 维护已安装 harness 的完整性，避免它在使用中腐坏或与仓库事实脱节

MVP 暂不追求让 harness 在使用中自动进化成更完整的架构体系；这属于后续的 Harness Evolution。当前更重要的是 Harness Preservation：确认已有的 `AGENTS.md`、skills、配置、验证入口和文档引用仍然存在、可读、可解释，并且没有明显漂移。

为了实施 Harness Preservation，`mykit` 后续应提供或整合确定性的 Harness Check / Harness Lint 能力。它不是目标项目的通用代码 linter 或 formatter，而是优先检查和维护 mykit 生成的 harness 资产，例如 `AGENTS.md`、`.agents/skills/`、`.mykit/config.json`、文档链接、验证入口和模板资产。必要时可以提供安全的 `--fix` 能力，但不应默认接管目标项目自身的代码风格。

未来可以继续加入 Claude Code 或内部产品 integration、仓库扫描、更丰富的模板、机器生成事实、sensors、evals 或 evidence 收集。但这些能力应该建立在 Context Harness 的边界之上，而不是把 `mykit` 做成 agent runtime。
