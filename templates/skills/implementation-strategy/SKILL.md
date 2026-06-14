---
name: implementation-strategy
description: Decide how to implement changes before editing code. Use when a task changes exported APIs, runtime behavior, serialized state, tests, or docs and you need to choose the compatibility boundary, whether shims or migrations are warranted, and when unreleased interfaces can be rewritten directly.
---

# Implementation Strategy

## Overview

Use this skill before editing code when the task changes runtime behavior or anything that might look like a compatibility concern. The goal is to keep implementations simple while protecting real released contracts.

## Quick start

1. Identify the surface you are changing: released public API, unreleased branch-local API, internal helper, persisted schema, wire protocol, CLI/config/env surface, or docs/examples only.
2. Determine the latest release boundary. If repository guidance names a release tag pattern, use that; otherwise use the latest reachable tag:
   ```bash
   BASE_TAG="$(git describe --tags --abbrev=0 2>/dev/null || true)"
   echo "$BASE_TAG"
   ```
3. If no release tag exists, say so and judge compatibility against documented public contracts and durable external state only.
4. Judge breaking-change risk against the latest release tag or documented compatibility policy, not against unreleased branch churn or post-tag changes already on the default branch.
5. Prefer the simplest implementation that satisfies the current task. Update callers, tests, docs, and examples directly instead of preserving superseded unreleased interfaces.
6. Add a compatibility layer only when there is a concrete released consumer, an otherwise supported durable external state boundary that requires it, or when the user explicitly asks for a migration path.

## Compatibility boundary rules

- Released public API or documented external behavior: preserve compatibility or provide an explicit migration path.
- Persisted schema, serialized state, wire protocol, CLI flags, environment variables, and externally consumed config: treat as compatibility-sensitive when they are part of the latest release or when the repo explicitly intends to preserve them across commits, processes, or machines.
- Interface changes introduced only on the current branch: not a compatibility target. Rewrite them directly.
- Interface changes present on the default branch but added after the latest release tag: not a breaking change by themselves. Rewrite them directly unless they already define a released or explicitly supported durable external state boundary.
- Internal helpers, private types, same-branch tests, fixtures, and examples: update them directly instead of adding adapters.
- Unreleased persisted schema versions on the default branch may be renumbered or squashed before release when intermediate snapshots are intentionally unsupported.

## Default implementation stance

- Prefer deletion or replacement over aliases, overloads, shims, feature flags, and dual-write logic when the old shape is unreleased.
- Do not preserve a confusing abstraction just because it exists in the current branch diff.
- If review feedback claims a change is breaking, verify it against the latest release tag and actual external impact before accepting the feedback.
- If a change truly crosses the latest released contract boundary, call that out explicitly in implementation notes, release notes context, and the user-facing summary.

## Project-specific compatibility rules

<!-- mykit:todo-checklist:start -->
Before filling this section:
- Identify released public surfaces, generated outputs, persisted data, and CLI/config contracts from repository evidence.
- Record the release tag or branch policy only if the repository already defines one.
- After the real compatibility boundary is documented, remove this checklist block.
<!-- mykit:todo-checklist:end -->

Fill this section in the target repository after inspecting real project contracts. Until it is filled, do not infer project policy from examples.

- TODO: Document released public APIs, CLI/config/env surfaces, persisted schemas, wire protocols, generated outputs, or package boundaries that must remain compatible.
- TODO: Document the release tag pattern or release branch policy if it differs from `git describe --tags --abbrev=0`.
- TODO: Document migration, deprecation, or schema-version rules required by this repository.

## When to stop and confirm

- The change would alter behavior shipped in the latest release tag.
- The change would modify durable external data, protocol formats, or serialized state.
- The user explicitly asked for backward compatibility, deprecation, or migration support.

## Output expectations

When this skill materially affects the implementation approach, state the decision briefly in your reasoning or handoff, for example:

- `Compatibility boundary: latest release tag v0.x.y; branch-local interface rewrite, no shim needed.`
- `Compatibility boundary: released schema; preserve compatibility and add migration coverage.`
