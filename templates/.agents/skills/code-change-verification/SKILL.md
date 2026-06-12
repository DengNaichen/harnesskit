---
name: code-change-verification
description: Run the mandatory verification stack when changes affect runtime code, tests, or build/test behavior.
---

# Code Change Verification

## Overview

Ensure work is only marked complete after formatting, linting, type checking, and tests pass. Use this skill when changes affect runtime code, tests, or build/test configuration. You can skip it for docs-only or repository metadata unless a user asks for the full stack.

## Quick start

1. Keep this skill at `./.agents/skills/code-change-verification` so it loads automatically for the repository.
2. Run from the repository root with `make format` first.
3. Then run `make lint`, `make typecheck`, and `make tests`.
4. If any command fails, fix the issue, rerun the full sequence, and report the failing output.
5. Confirm completion only when all commands succeed with no remaining issues.

## Manual workflow

- If dependencies are not installed or have changed, run `make sync` first to install dev requirements via `uv`.
- Run from the repository root with `make format` first, then `make lint`, `make typecheck`, and `make tests`.
- Do not skip steps; stop and fix issues immediately when a command fails.
- If you run the steps manually, you may parallelize `make lint`, `make typecheck`, and `make tests` after `make format` completes, but you must stop the remaining steps as soon as one fails.
- Re-run the full stack after applying fixes so the commands execute in the required order.
