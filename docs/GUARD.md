# Guard Design Guide

Guard 是把 Rule 变成可验证约束的机制。`RULES.md` 说明团队和 agent 应该遵守什么；Guard 说明其中哪些部分可以被检查、如何检查、在哪里运行，以及能拦到什么程度。

本文件只说明 Guard 应该如何设计，不记录当前仓库已经绑定了哪些 Guard。具体项目的 Guard 状态、命令和 runner 证据应写在该项目自己的 `RULES.md`、agent 指南、验证入口或平台配置中。

## 核心概念

- **Rule**：开发时必须遵守的行为规则，例如新增行为需要测试、依赖声明必须同步、文档不能误导 agent。
- **Guard**：用于验证 Rule 的检查，可以是命令、脚本、lint rule、测试、构建、平台 gate 或 review gate。
- **Runner**：实际运行 Guard 的位置，例如本地验证入口、hook suite、CI、代码托管平台、IDE task、内部平台 gate 或人工 review。
- **Runner 证据**：证明 Guard 已经绑定到 Runner 的文件、配置、平台设置或人工确认记录。
- **拦截强度**：Guard 对违规变更的阻断能力。

不要把 Guard 等同于某一种工具。pre-commit、CI、Makefile、justfile、package scripts、server hook 或内部平台都只是 Runner；Guard 是被这些 Runner 执行或承载的检查。

## 设计原则

Guard 的设计应先从 Rule 出发，再选择检查方式和 Runner：

1. 明确 Rule 要防止什么问题。
2. 判断这个问题能否确定性检测。
3. 为可检测部分设计 Guard。
4. 把 Guard 绑定到合适 Runner。
5. 记录 Runner 证据和拦截强度。
6. 对无法完全自动化的部分，明确需要 review 或人工判断。

不要把没有 Runner 证据的检查写成强制阻断。没有绑定到 runner 的命令只是建议或人工操作；只有能证明会被运行的位置，才构成真正的 Guard 链路。

## 拦截强度

- **强制**：平台或流程会阻止违规变更继续流转，例如 required checks、server hook 或不可跳过的内部 gate。
- **半强制**：默认会运行但可以被绕过，例如本地 hook suite。
- **agent 执行**：由 agent 指南、skill 或任务流程要求 agent 在交付前运行。
- **人工执行**：由人或 reviewer 按需运行，通常需要最终说明或 review 记录作为证据。
- **未绑定**：存在检查想法或命令，但没有证据表明它已经接入任何 Runner。

拦截强度不是 Guard 本身的属性，而是 Guard 和 Runner 绑定后的结果。同一个检查绑定到本地脚本、pre-commit 和 CI 时，强度不同。

## Guard 类型

- **确定性 Guard**：能给出明确 pass/fail，例如 lint、format check、测试、构建、链接检查、schema 校验。
- **部分确定性 Guard**：工具只能覆盖一部分问题，例如测试是否存在、架构路径是否有效、模板变量是否完整。
- **review Guard**：主要依赖人工或 agent 判断，例如测试是否充分、命名是否符合本地语义、架构描述是否准确。
- **平台 Guard**：由代码托管、CI、权限系统或内部平台执行，例如 branch protection、required checks、审批规则。

部分确定性 Guard 不应该被描述成完全自动化。它可以降低风险，但仍需要说明剩余判断由谁负责。

## 推荐结构

一个项目可以把 Guard 信息分散到不同层级，但每一层应职责清晰：

- `RULES.md`：描述 Rule、适用范围、Guard 类型、Runner 证据和当前状态。
- Agent 指南：告诉 agent 在什么情况下必须运行哪些验证入口。
- 统一验证入口：把确定性 Guard 收敛为一个稳定命令。
- Hook suite：在本地提交或变更流转前运行一组检查。
- CI 或平台 gate：作为最终阻断层。
- Review 流程：覆盖无法完全自动化的判断。

理想状态下，文档不重复维护大量命令细节，而是引用稳定验证入口；命令细节由脚本、任务配置或平台配置承载。

## 自举项目的边界

当项目本身正在设计 Guard 系统时，设计文档和实现状态要分开：

- 设计文档说明概念、原则和推荐结构。
- 当前项目状态记录在项目自己的规则、验证入口、hook 或平台配置中。
- 不要在设计文档里同时声明“应该怎么设计”和“本项目当前已经做到了什么”。

这样可以避免自举时的循环：设计文档保持抽象稳定，实现状态由可验证的项目事实负责更新。
