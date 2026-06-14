---
name: code-change-verification
description: Run the mandatory verification stack when changes affect runtime code, tests, or build/test behavior.
---

# Code Change Verification

## Overview

Ensure work is only marked complete after the repository's own verification checks have run. Use this skill when changes affect runtime code, tests, user-facing generated outputs, templates, or build/test configuration. You can skip it for docs-only or repository metadata unless a user asks for the full stack.

## Repository verification stack

<!-- harnesskit:todo-checklist:start -->
Before filling this section:
- Verify each command from repository files such as manifests, scripts, locks, or CI config.
- Leave unavailable checks as `TODO` instead of inventing generic commands.
- After the real stack is configured, remove this checklist block.
<!-- harnesskit:todo-checklist:end -->

- Setup command: TODO
- Format command: TODO
- Lint command: TODO
- Typecheck command: TODO
- Test command: TODO
- Full verification command: TODO
- Notes: TODO

## Quick start

1. Keep this skill at `./.agents/skills/code-change-verification` so it loads automatically for the repository.
2. Use the commands listed in "Repository verification stack".
3. Run only commands that are filled with concrete repository commands. Treat `TODO` entries as missing, not optional examples.
4. Run commands from the repository root, preserving the order documented in this skill.
5. If a command fails, fix the issue, rerun the relevant verification stack, and report the final status.
6. If this skill still contains only `TODO` verification entries, report that verification is not configured.

## Manual workflow

- If dependency installation is required and the setup command has been filled above, run that setup command before verification.
- Prefer the full verification command when it has been filled above.
- If there is no full verification command, run the filled format, lint, typecheck, and test commands in that order, skipping only entries that remain `TODO`.
- Do not add new tools or create new verification commands as part of this skill unless the user explicitly asks for that change.
- Do not treat `TODO` entries or generic examples in templates as proof that the target repository supports those commands.
- Re-run failed checks after applying fixes so the reported verification matches the final working tree.
