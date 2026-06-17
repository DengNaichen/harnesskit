---
name: implementation-strategy
description: Decide how to implement changes before editing code. Use when a task changes exported APIs, runtime behavior, serialized state, tests, or docs and you need to choose the compatibility boundary, whether shims or migrations are warranted, and when unreleased interfaces can be rewritten directly.
---

# Implementation Strategy

## Overview

Use this skill before editing code when the task changes runtime behavior or anything that might look like a compatibility concern. The goal is to keep implementations simple while protecting real released contracts.

## Quick start

1. Identify the surface you are changing: released public API, unreleased branch-local API, internal helper, persisted schema, wire protocol, CLI/config/env surface, or docs/examples only.
2. Determine the latest release boundary:
   ```bash
   BASE_TAG="$(git tag -l 'v*' --sort=-v:refname | head -n1)"
   echo "$BASE_TAG"
   ```
3. Judge breaking-change risk against that latest release tag, not against unreleased branch churn or post-tag changes already on `main`.
4. Prefer the simplest implementation that satisfies the current task. Update callers, tests, docs, and examples directly instead of preserving superseded unreleased interfaces.
5. Add a compatibility layer only when there is a concrete released consumer, an otherwise supported durable external state boundary that requires it, or when the user explicitly asks for a migration path.

## Compatibility boundary rules

- Released public API or documented external behavior: preserve compatibility or provide an explicit migration path.
- Persisted schema, serialized state, wire protocol, CLI flags, environment variables, and externally consumed config: treat as compatibility-sensitive when they are part of the latest release or when the repo explicitly intends to preserve them across commits, processes, or machines.
- Interface changes introduced only on the current branch: not a compatibility target. Rewrite them directly.
- Interface changes present on `main` but added after the latest release tag: not a semver breaking change by themselves. Rewrite them directly unless they already define a released or explicitly supported durable external state boundary.
- Internal helpers, private types, same-branch tests, fixtures, and examples: update them directly instead of adding adapters.
- Unreleased persisted schema versions on `main` may be renumbered or squashed before release when intermediate snapshots are intentionally unsupported.

## Default implementation stance

- Prefer deletion or replacement over aliases, overloads, shims, feature flags, and dual-write logic when the old shape is unreleased.
- Do not preserve a confusing abstraction just because it exists in the current branch diff.
- If review feedback claims a change is breaking, verify it against the latest release tag and actual external impact before accepting the feedback.
- If a change truly crosses the latest released contract boundary, call that out explicitly in implementation notes, release notes context, and the user-facing summary.

## Project-specific compatibility rules

- Treat the Typer CLI surface (`harnesskit init`, `harnesskit integration ...`, flags, arguments, exit behavior, and user-facing messages) as compatibility-sensitive once released.
- Treat [.harnesskit/config.json](../../../.harnesskit/config.json) as durable external state. Its current `schema_version` is `1`; structure changes need tests and an explicit compatibility decision.
- Treat generated template output under [templates/](../../../templates/) as user-facing behavior because `harnesskit init` copies or renders it into target repositories.
- Current supported integration is `codex`; adding or renaming integrations affects CLI behavior, template layout, README guidance, and tests.
- Jinja templates use `StrictUndefined`; adding template variables requires corresponding render context or an intentional target-repo TODO.

## When to stop and confirm

- The change would alter behavior shipped in the latest release tag.
- The change would modify durable external data, protocol formats, or serialized state.
- The change would remove or rename existing CLI commands, flags, config keys, template output paths, or supported integrations.
- The user explicitly asked for backward compatibility, deprecation, or migration support.

## Output expectations

When this skill materially affects the implementation approach, state the decision briefly in your reasoning or handoff, for example:

- `Compatibility boundary: latest release tag v0.x.y; branch-local interface rewrite, no shim needed.`
- `Compatibility boundary: released schema; preserve compatibility and add migration coverage.`
