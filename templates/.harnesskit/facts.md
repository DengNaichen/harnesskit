# [PROJECT_NAME] Harness Facts

本文件位于 `.harnesskit/facts.md`，是 `scan -> fill` 工作流的事实交接快照。`$scan-facts` 从仓库事实刷新本文件；`$fill-agents`、`$fill-architecture`、`$fill-rules` 和 `$fill-skills` 消费本文件来更新对应 artifact。

本文件不是仓库事实本身的替代品。填充任何 agent-facing 文档前，仍应优先核对真实源码、清单、脚本、锁文件、CI/hook 配置和现有文档。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 每条已确认事实都带有仓库证据路径或团队确认来源。
- 无法确认的内容保留 `[NEEDS CLARIFICATION: ...]`，不要把模板示例写成事实。
- facts 刷新后，按需运行 `$fill-agents`、`$fill-architecture`、`$fill-rules` 和 `$fill-skills`。
<!-- harnesskit:todo-checklist:end -->

## Project Identity

- **Project name**: [NEEDS CLARIFICATION: 项目名称]
- **Project purpose**: [NEEDS CLARIFICATION: README、产品文档或团队确认中的项目定位]
- **Primary audience**: [NEEDS CLARIFICATION: 使用者、维护者或目标集成]
- **Evidence**: [NEEDS CLARIFICATION: 事实来源路径]

## Tech Stack

| Category | Detected fact | Evidence | Confidence |
| --- | --- | --- | --- |
| Languages / runtimes | [NEEDS CLARIFICATION: 语言和运行时] | [NEEDS CLARIFICATION: 清单、源码或配置路径] | [NEEDS CLARIFICATION: high / medium / low] |
| Package managers | [NEEDS CLARIFICATION: 包管理器或 N/A] | [NEEDS CLARIFICATION: 清单或锁文件路径] | [NEEDS CLARIFICATION: high / medium / low] |
| Frameworks / libraries | [NEEDS CLARIFICATION: 框架或关键库] | [NEEDS CLARIFICATION: 清单、源码或文档路径] | [NEEDS CLARIFICATION: high / medium / low] |
| Build tools | [NEEDS CLARIFICATION: 构建工具或 N/A] | [NEEDS CLARIFICATION: 构建配置或脚本路径] | [NEEDS CLARIFICATION: high / medium / low] |

## Validation Entrypoints

| Kind | Command | Runner / binding | Evidence |
| --- | --- | --- | --- |
| Setup | [NEEDS CLARIFICATION: 真实命令或 N/A] | [NEEDS CLARIFICATION: 本地、CI、hook、agent 执行或未绑定] | [NEEDS CLARIFICATION: 事实来源] |
| Full verify | [NEEDS CLARIFICATION: 真实命令或未配置] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |
| Test | [NEEDS CLARIFICATION: 真实命令或未配置] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |
| Lint | [NEEDS CLARIFICATION: 真实命令或 N/A] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |
| Format check | [NEEDS CLARIFICATION: 真实命令或 N/A] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |
| Type check | [NEEDS CLARIFICATION: 真实命令或 N/A] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |
| Build | [NEEDS CLARIFICATION: 真实命令或 N/A] | [NEEDS CLARIFICATION: runner 证据] | [NEEDS CLARIFICATION: 事实来源] |

## Repository Map Candidates

- [NEEDS CLARIFICATION: 主要源码目录和职责]
- [NEEDS CLARIFICATION: 主要测试目录和覆盖范围]
- [NEEDS CLARIFICATION: 主要文档目录和用途]
- [NEEDS CLARIFICATION: 模板、生成资产、部署或脚本目录]
- [NEEDS CLARIFICATION: 容易混淆的边界，例如 runtime / POC / generated output / design docs]

## Agent-Facing Assets

| Asset | Status | Evidence / notes |
| --- | --- | --- |
| `AGENTS.md` | [NEEDS CLARIFICATION: exists / missing / stale] | [NEEDS CLARIFICATION: 事实来源或待处理] |
| `ARCHITECTURE.md` | [NEEDS CLARIFICATION: exists / missing / stale] | [NEEDS CLARIFICATION: 事实来源或待处理] |
| `RULES.md` | [NEEDS CLARIFICATION: exists / missing / stale] | [NEEDS CLARIFICATION: 事实来源或待处理] |
| `.agents/skills/` | [NEEDS CLARIFICATION: exists / missing / partial] | [NEEDS CLARIFICATION: 已安装 skills 和缺口] |
| Companion guides | [NEEDS CLARIFICATION: `CLAUDE.md`、其他入口或 N/A] | [NEEDS CLARIFICATION: 指向关系和一致性] |

## Rule / Guard Candidates

- [NEEDS CLARIFICATION: 单一验证入口状态和 runner 证据]
- [NEEDS CLARIFICATION: 新增行为测试规则状态和测试入口]
- [NEEDS CLARIFICATION: 依赖和锁文件同步规则状态]
- [NEEDS CLARIFICATION: 文档/context harness 不漂移规则状态]
- [NEEDS CLARIFICATION: lint、format、typecheck、coverage、build、hook、branch protection 等可选规则状态]
- [NEEDS CLARIFICATION: 需要写入 `RULES.md` 的短规则和对应 `.harnesskit/rules/RULE-*.md` details 文件]

## Open Questions

- [NEEDS CLARIFICATION: 仓库事实无法确认、需要团队选择的决策]
