# HarnessKit

HarnessKit 是一个用于在现有仓库中初始化轻量级 Context Harness 的 CLI 与 agent-facing toolkit。

它的目标是让 AI agent 能够稳定理解一个代码仓库：这个项目是什么、目录如何组织、开发和验证命令是什么、哪些工程规则不能被破坏，并在项目演进中保持这些上下文资产不腐坏、不漂移。这样用户不需要在每次对话里反复解释项目背景。

## 项目定位

HarnessKit 会把一组 agent 友好的 Harness 资产安装到目标仓库中，让 agent 有稳定的仓库入口、操作规则和验证入口。

当前 MVP 只聚焦 **Context Harness**，并且只支持 Codex integration。HarnessKit 不实现 agent runtime、工具沙箱、编排控制器，也不做长期运行 agent 的调度系统。

## 产品体验

HarnessKit 本体仍然是 CLI，但真正的使用体验不是让用户反复手敲脚本，而是把 CLI 和 agent skills 配合起来：

1. 用户安装 `harnesskit`。
2. 在某个仓库里运行 `harnesskit init --here`，或运行 `harnesskit init <project>`。
3. HarnessKit 初始化 Context Harness 核心资产。
4. HarnessKit 同时安装 Codex skills 到 `.agents/skills/`。
5. 用户回到 Codex 对话框里，通过本地 skills 继续扫描仓库事实、验证变更和沉淀规则。

## 核心模型

HarnessKit 把 agent-facing context 拆成三类职责：

- **Skills** 教 agent 怎么做一类任务，例如扫描事实、判断兼容性、验证改动或刷新模板。
- **Rules** 告诉 agent 在这个仓库里永远或局部必须遵守什么约束。
- **Validations** 负责把可检查的约束转成验证反馈，并记录它们在哪些 runner 中执行。

`AGENTS.md` 是入口路由器：它不复制所有规则和流程，而是告诉 agent 什么时候读哪些文件、触发哪些 skills、运行哪些 validations。`RULES.md` 是短规则索引；规则的长解释、证据和 validation 绑定可以下沉到 `.harnesskit/rules/` 或对应设计文档中。

## 当前结构

这个仓库目前包含：

- `src/harnesskit/`：Python CLI、初始化引擎和 Context Harness linter runtime
- `templates/`：`harnesskit init` 会安装到目标仓库的模板文件
- `harness-linter-poc/`：旧 linter POC/参考实现
- `.agents/skills/`：本仓库本地 Codex skills
- `docs/design/`：AGENTS、ARCHITECTURE、RULES、Validation 和 Harness Builder 的设计说明

当前 CLI 暴露：

```bash
harnesskit init <project>
harnesskit init --here
harnesskit init --here --integration codex
harnesskit init --here --integration claude
harnesskit init --here --no-integration
harnesskit integration list
harnesskit integration install codex
harnesskit integration install claude
harnesskit lint .
```

`init` 会把内置模板复制到目标仓库，并写入 `.harnesskit/config.json`。如果目标文件已经存在，默认跳过；传入 `--force` 时才会覆盖。当前支持的 integration 是 `codex` 和 `claude`，其中 `codex` 是默认值。

## 本地开发

首次配置或依赖变更后运行：

```bash
uv sync
```

本地 CLI 入口：

```bash
uv run harnesskit ...
```

调试入口模块时可以运行：

```bash
uv run python -m harnesskit.cli
```

完整验证入口：

```bash
make verify
```

Markdown 链接检查需要本机安装 `lychee`；本地可用 Homebrew 安装：

```bash
brew install lychee
```

## MVP 边界

近期产品边界应该保持小而清晰：

- 初始化一套最小 Context Harness
- 让 `AGENTS.md` 成为简洁的 agent 顶层路由器
- 提供 `ARCHITECTURE.md` 作为目标仓库的粗粒度架构地图模板
- 提供 `RULES.md` 作为短规则索引，而不是流程手册
- 安装 Codex 本地 skills 到 `.agents/skills/`
- 用 linter/Validation 原型保护 harness 文件不腐坏、不漂移
- 通过 skills、rules、validations 和文档分别承载流程、约束、执行检查和设计说明
- 把项目说明和 agent 操作规则分开
- 让生成资产在进一步自动化之前保持容易审查
- 维护已安装 harness 的完整性，避免它在使用中腐坏或与仓库事实脱节

后续路线放在 [`docs/ROADMAP.md`](docs/ROADMAP.md)。
