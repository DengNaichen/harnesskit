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

<!--
第一版内置三个 Codex skills：

- `$mykit-audit`：只读审计当前仓库的 Context Harness 状态。
- `$mykit-refresh`：补装或刷新 harness 资产，默认不覆盖已有文件。
- `$mykit-explain`：解释当前仓库里的 mykit 资产和使用方式。
-->
<!-- 我认为这部分应该属于 roadmap，因为它描述的是第一版 skill 组合，而不是 README 必须保留的当前使用入口。 -->

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

<!--
为了实施 Harness Preservation，`mykit` 后续应提供或整合确定性的 Harness Check / Harness Lint 能力。它不是目标项目的通用代码 linter 或 formatter，而是优先检查和维护 mykit 生成的 harness 资产，例如 `AGENTS.md`、`.agents/skills/`、`.mykit/config.json`、文档链接、验证入口和模板资产。必要时可以提供安全的 `--fix` 能力，但不应默认接管目标项目自身的代码风格。
-->
<!-- 我认为这部分应该属于 roadmap，因为它描述的是后续 Harness Check / Harness Lint 的能力形态。 -->

<!--
未来可以继续加入 Claude Code 或内部产品 integration、仓库扫描、更丰富的模板、机器生成事实、sensors、evals 或 evidence 收集。但这些能力应该建立在 Context Harness 的边界之上，而不是把 `mykit` 做成 agent runtime。
-->
<!-- 我认为这部分应该属于 roadmap，因为它列的是未来可能加入的 integration、scan、sensors、evals 和 evidence 能力。 -->
