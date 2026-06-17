---
name: code-change-verification
description: 当变更影响运行时代码、测试、用户可见生成输出、模板或构建/验证行为时，运行仓库强制验证栈。
---

# 代码变更验证

## 概览

确保只有在仓库自己的 verification checks 运行后，才把工作标记为完成。变更影响运行时代码、测试、用户可见 generated outputs、templates 或 build/test configuration 时使用本 skill。纯文档或仓库元数据变更可跳过，除非用户要求完整验证栈。

## 仓库验证栈

<!-- harnesskit:todo-checklist:start -->
补全本节前请确认：
- 从仓库清单、脚本、锁文件或 CI 配置中验证每条命令。
- 没有可用事实的检查保留 `[NEEDS CLARIFICATION: ...]`，不要虚构通用命令。
- 真实验证栈配置完成后，可以删除这个 checklist 块。
<!-- harnesskit:todo-checklist:end -->

- Setup command: [NEEDS CLARIFICATION: 真实 setup 命令或 N/A]
- Format command: [NEEDS CLARIFICATION: 真实 format check 命令或 N/A]
- Lint command: [NEEDS CLARIFICATION: 真实 lint 命令或 N/A]
- Typecheck command: [NEEDS CLARIFICATION: 真实 typecheck 命令或 N/A]
- Test command: [NEEDS CLARIFICATION: 真实 test 命令或 N/A]
- Full verification command：在 `scripts/run_validation.py` 已配置 repository-verified checks 后使用 `make verify`。
- Notes：`make verify` 会写入 `.harnesskit/receipts/latest.json` 和 `.harnesskit/receipts/runs/<run_id>.json`；checks 配置前，它会记录 `not_configured` 并以非零状态退出。

## 快速开始

1. 保持本 skill 位于 [`.agents/skills/code-change-verification`](./)，让仓库能自动加载它。
2. 使用 "仓库验证栈" 中列出的 commands。
3. 只运行已经填入具体仓库命令的 commands。把 `[NEEDS CLARIFICATION: ...]` 视为缺失项，而不是可选示例。
4. 从仓库根目录运行命令，并保持本 skill 记录的顺序。
5. 如果 command 失败，修复问题，重新运行相关 verification stack，并报告最终状态。
6. 如果 `make verify` 报告 `not_configured`，先根据仓库事实填充 [`scripts/run_validation.py`](scripts/run_validation.py) 中的 `CHECKS`，再把它当作验证入口。

## 手动流程

- 如果需要安装依赖，且上方 setup command 已填充，在验证前先运行该 setup command。
- [`scripts/run_validation.py`](scripts/run_validation.py) 配置完成后，优先使用 `make verify`。
- 如果没有 full verification command，则按 format、lint、typecheck、test 的顺序运行已填充命令，只跳过仍为 `[NEEDS CLARIFICATION: ...]` 的条目。
- 除非用户明确要求，不要作为本 skill 的一部分新增工具或创建新的 verification commands。
- 不要把 `[NEEDS CLARIFICATION: ...]` 条目或 templates 中的通用示例当成目标仓库支持这些命令的证据。
- 确认 `.harnesskit/receipts/latest.json` 已写入；有帮助时在最终回复中引用 receipt 路径。
- 修复后重新运行失败检查，确保报告的验证状态对应最终 working tree。
