# [PROJECT_NAME] Harness Rules

本文件是 Agent 约束索引。Rules 必须满足：
1. **仓库特异**：非通用工程常识（通用常识写入 practices 指导）。
2. **硬性不可逾越**：非黑即白的硬限制，用于强行压制 Agent 自作聪明的先验倾向。
3. **高防踩坑**：防止因轻信旧版本教程、本地默认配置导致构建崩溃、循环依赖或安全漏洞。

[AGENTS.md](AGENTS.md) 负责路由，[RULES.md](RULES.md) 只保留短约束句，不负责承载背景、路径地图或流程（流程放入 `.agents/skills/`，设计思想放入 `docs/practices/`）。

Rules 不要求一条规则对应一个 details 文件。复杂背景进入 [ARCHITECTURE.md](ARCHITECTURE.md) 或 [docs/practices/](docs/practices/)；可执行或可跟踪检查进入验证入口、pre-commit hook、linter runtime 或其他 runner。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 只写当前仓库特有、必须始终成立、能判断遵守或违反的短规则。
- 不要把流程、背景、路径地图、runner 细节或通用工程建议写成 Rule。
- 不要默认创建 `.harnesskit/rules/RULE-*.md` details；已有 details 只是可选背景层。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 技术栈与命名空间规则

- [NEEDS CLARIFICATION: 当前仓库特有且必须遵守的技术栈、包管理、运行时或命名空间约束。]

## 架构与模块依赖规则

- [NEEDS CLARIFICATION: 当前仓库特有且必须遵守的模块边界、依赖方向、生成资产或持久状态约束。]

## 构建与运行脚本规则

- [NEEDS CLARIFICATION: 当前仓库特有且必须遵守的构建、测试、验证、发布或运行脚本约束。]

## 安全规则

- [NEEDS CLARIFICATION: 当前仓库特有且必须遵守的 secret、权限、数据、文件写入或外部系统安全约束。]
