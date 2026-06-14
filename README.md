# mykit

`mykit` 是一个用于在现有仓库中初始化轻量级 Context Harness 的 CLI 与 Codex-facing toolkit。

它的目标是让 AI agent 能够稳定理解一个代码仓库：这个项目是什么、目录如何组织、开发和验证命令是什么、哪些工程规则不能被破坏，并在项目演进中保持这些上下文资产不腐坏、不漂移。这样用户不需要在每次对话里反复解释项目背景。

## 项目定位

`mykit` 会把一组 agent 友好的 Context Harness 资产安装到目标仓库中，让 agent 有稳定的仓库入口、操作规则和验证入口。

当前 MVP 只聚焦 **Context Harness**，并且只支持 Codex integration。`mykit` 不实现 agent runtime、工具沙箱、编排控制器，也不做长期运行 agent 的调度系统。

## 产品体验

`mykit` 本体仍然是 CLI，但真正的使用体验不是让用户反复手敲脚本，而是把 CLI 和 agent skills 配合起来：

1. 用户安装 `mykit`。
2. 在某个仓库里运行 `mykit init --here`，或运行 `mykit init <project>`。
3. `mykit` 初始化 Context Harness 核心资产。
4. `mykit` 同时安装 Codex skills 到 `.agents/skills/`。
5. 用户回到 Codex 对话框里，通过 `$mykit-*` skills 继续审计、刷新和解释 harness。

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

后续路线放在 `ROADMAP.md`。
