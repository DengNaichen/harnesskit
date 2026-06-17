---
name: code-change-verification
description: Run the mandatory verification stack when changes affect runtime code, tests, or build/test behavior.
---

# Code Change Verification

## Overview

Ensure work is only marked complete after the repository's own verification checks have run. Use this skill when changes affect runtime code, tests, user-facing generated outputs, templates, or build/test configuration. You can skip it for docs-only or repository metadata unless a user asks for the full stack.

## Repository verification stack

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
- Full verification command: `make verify` after `scripts/run_validation.py` has been configured with repository-verified checks.
- Notes: `make verify` writes `.harnesskit/receipts/latest.json` and `.harnesskit/receipts/runs/<run_id>.json`; until checks are configured, it records `not_configured` and exits non-zero.

## Quick start

1. Keep this skill at [`.agents/skills/code-change-verification`](./) so it loads automatically for the repository.
2. Use the commands listed in "Repository verification stack".
3. Run only commands that are filled with concrete repository commands. Treat `[NEEDS CLARIFICATION: ...]` entries as missing, not optional examples.
4. Run commands from the repository root, preserving the order documented in this skill.
5. If a command fails, fix the issue, rerun the relevant verification stack, and report the final status.
6. If `make verify` reports `not_configured`, fill `CHECKS` in [`scripts/run_validation.py`](scripts/run_validation.py) from repository facts before treating it as verification.

## Manual workflow

- If dependency installation is required and the setup command has been filled above, run that setup command before verification.
- Prefer `make verify` after `scripts/run_validation.py` has been configured.
- If there is no full verification command, run the filled format, lint, typecheck, and test commands in that order, skipping only entries that remain `[NEEDS CLARIFICATION: ...]`.
- Do not add new tools or create new verification commands as part of this skill unless the user explicitly asks for that change.
- Do not treat `[NEEDS CLARIFICATION: ...]` entries or generic examples in templates as proof that the target repository supports those commands.
- Confirm `.harnesskit/receipts/latest.json` was written and cite the receipt path in the final response when useful.
- Re-run failed checks after applying fixes so the reported verification matches the final working tree.
