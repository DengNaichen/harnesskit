# Validation Design Guide

Validation 是把 Rule 变成可验证约束的机制。[RULES.md](../../RULES.md) 说明团队和 agent 应该遵守什么；Validation 说明其中哪些部分可以被检查、如何检查、在哪里运行，以及 runner 具备什么执行或阻断强度。

本文件只说明 Validation 应该如何设计，不记录当前仓库已经绑定了哪些 Validation。具体项目的 Validation 状态、命令和 runner 证据应写在 agent 指南、验证入口、runner、hook、CI 或平台配置中；[RULES.md](../../RULES.md) 只保留必须遵守的短约束。

## 核心概念

- **Rule**：开发时必须遵守的行为规则，例如新增行为需要测试、依赖声明必须同步、文档不能误导 agent。
- **Validation**：用于验证 Rule 的检查，可以是命令、脚本、lint rule、测试、构建、平台 check 或 review。
- **Runner**：实际运行 Validation 的位置，例如本地验证入口、hook suite、CI、代码托管平台、IDE task、内部平台 gate 或人工 review。
- **Runner 证据**：证明 Validation 已经绑定到 Runner 的文件、配置、平台设置或人工确认记录。
- **执行/阻断强度**：Validation 绑定到 runner 后，对违规变更的反馈或阻断能力。
- **Receipt**：Validation 运行后留下的轻量记录，说明什么时候运行、由哪个入口运行、结果是什么。

Validation 不等同于某一种工具。pre-commit、CI、Makefile、justfile、package scripts、server hook 或内部平台都只是 Runner；Validation 是被这些 Runner 执行或承载的检查。

## 设计原则

Validation 的设计应先从 Rule 出发，再选择检查方式和 Runner：

1. 明确 Rule 要防止什么问题。
2. 判断这个问题能否确定性检测。
3. 为可检测部分设计 Validation。
4. 把 Validation 绑定到合适 Runner。
5. 记录 Runner 证据和执行/阻断强度。
6. 设计 Validation receipt，让运行结果能被 agent、人和 CI 消费。
7. 对无法完全自动化的部分，明确需要 review 或人工判断。

不要把没有 Runner 证据的检查写成强制阻断。没有绑定到 runner 的命令只是建议或人工操作；只有能证明会被运行的位置，才构成真正的 validation 链路。

## 统一入口

Validation suite 应优先收敛到一个稳定入口，例如 `make verify`、`just verify`、`npm run verify` 或 `harnesskit validation run`。agent、人工本地验证和 CI 应尽量调用同一个入口，避免不同 runner 维护不同命令列表。

入口可以拆成不会递归的子任务：

- 核心检查：lint、format check、test、build、link check 等确定性 Validation。
- Hook suite：运行 pre-commit 或类似本地 hook。
- 平台 gate：在 CI 或代码托管平台中调用同一入口，并由平台决定是否阻断。

不要让 hook suite 调用完整入口，同时完整入口又调用 hook suite。需要复用时，把核心检查拆成独立子入口，再由完整入口和 hook 分别调用。

## Validation Receipt

Validation 只运行而不留记录时，只能证明“当下命令结束了”，很难向 agent 或 reviewer 展示。轻量 receipt 可以把一次运行变成可追溯结果，但不必一开始做成完整审计系统。

推荐默认位置：

```text
.harnesskit/
  receipts/
    latest.json
    runs/
      <run_id>.json
```

`latest.json` 方便 agent 找到最近一次运行；`runs/<run_id>.json` 保存历史记录。receipt 是运行产物，默认不提交进版本库；CI 可以把它上传为 artifact。

最小 receipt 字段：

```json
{
  "schema_version": 1,
  "type": "validation",
  "run_id": "2026-06-15T10-32-11+08-00",
  "started_at": "2026-06-15T10:32:11+08:00",
  "finished_at": "2026-06-15T10:33:42+08:00",
  "entrypoint": "make verify",
  "status": "passed",
  "git": {
    "commit": "6cba0f6",
    "dirty": false
  },
  "checks": [
    {
      "name": "test",
      "command": "uv run pytest",
      "status": "passed",
      "exit_code": 0,
      "duration_seconds": 4.8
    }
  ]
}
```

失败也要写 receipt。失败记录至少应包含失败 check、exit code、时间戳和入口；完整日志可以作为后续增强，而不是 MVP 的必要条件。

## 执行/阻断强度

- **强制**：runner 或平台会阻止违规变更继续流转，例如 required checks、server hook 或不可跳过的内部 gate。
- **半强制**：默认会运行但可以被绕过，例如本地 hook suite。
- **agent 执行**：由 agent 指南、skill 或任务流程要求 agent 在交付前运行。
- **人工执行**：由人或 reviewer 按需运行，通常需要最终说明或 review 记录作为证据。
- **未绑定**：存在检查想法或命令，但没有证据表明它已经接入任何 Runner。

执行/阻断强度不是 Validation 本身的属性，而是 Validation 和 Runner 绑定后的结果。同一个检查绑定到本地脚本、pre-commit 和 CI 时，强度不同。

## Validation 类型

- **确定性 Validation**：能给出明确 pass/fail，例如 lint、format check、测试、构建、链接检查、schema 校验。
- **部分确定性 Validation**：工具只能覆盖一部分问题，例如测试是否存在、架构路径是否有效、模板变量是否完整。
- **review Validation**：主要依赖人工或 agent 判断，例如测试是否充分、命名是否符合本地语义、架构描述是否准确。
- **平台 Validation**：由代码托管、CI、权限系统或内部平台执行，例如 branch protection、required checks、审批规则。

部分确定性 Validation 不应该被描述成完全自动化。它可以降低风险，但仍需要说明剩余判断由谁负责。

## 推荐结构

一个项目可以把 Validation 信息分散到不同层级，但每一层应职责清晰：

- [RULES.md](../../RULES.md)：描述必须遵守的短 Rule；不承载完整 Validation 状态、Runner 证据或命令清单。
- Agent 指南：告诉 agent 在什么情况下必须运行哪些验证入口。
- Skill runner：封装确定性 Validation 的执行逻辑，并写入 receipt。
- 统一验证入口：把确定性 Validation 收敛为一个稳定命令，通常调用 skill runner 或项目脚本。
- Receipt 目录：保存最近一次和历史 Validation 运行摘要。
- Hook suite：在本地提交或变更流转前运行一组检查。
- CI 或平台 gate：在具备 runner 证据时作为最终阻断层。
- Review 流程：覆盖无法完全自动化的判断。

理想状态下，文档不重复维护大量命令细节，而是引用稳定验证入口；命令细节由脚本、任务配置或平台配置承载。

## 自举项目的边界

当项目本身正在设计 Validation 系统时，设计文档和实现状态要分开：

- 设计文档说明概念、原则和推荐结构。
- 当前项目状态记录在项目自己的规则、验证入口、hook 或平台配置中。
- 不要在设计文档里同时声明“应该怎么设计”和“本项目当前已经做到了什么”。

这样可以避免自举时的循环：设计文档保持抽象稳定，实现状态由可验证的项目事实负责更新。
