---
name: code-change-verification
description: Run the mandatory verification stack when changes affect runtime code, tests, or build/test behavior.
---

# Code Change Verification

## Overview

Ensure work is only marked complete after the repository's available verification command passes. Use this skill when changes affect runtime code, templates that change generated behavior, tests, or build/test configuration. You can skip it for docs-only or repository metadata unless a user asks for the full stack.

## Quick start

1. Keep this skill at `./.agents/skills/code-change-verification` so it loads automatically for the repository.
2. If dependencies are not installed or have changed, run `uv sync`.
3. Run from the repository root:
   ```bash
   uv run python -m unittest discover -s tests
   ```
4. If the command fails, fix the issue, rerun it, and report the failing output.
5. Confirm completion only when the command succeeds with no remaining issues.

## Manual workflow

- If dependencies are not installed or have changed, run `uv sync` first.
- Run `uv run python -m unittest discover -s tests` from the repository root.
- This repository currently has no Makefile, formatter, linter, type checker, pytest config, or docs build command. Do not invent those checks.
- Re-run the test command after applying fixes so the reported verification matches the final working tree.
