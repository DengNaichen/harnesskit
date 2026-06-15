---
name: fill-rules
description: Fill or refresh RULES.md from .harnesskit/facts.md and verified repository evidence. Use after scan-facts when updating Rule status, Guard type, runner bindings, and project command tables.
---

# Fill Rules

Use this skill to update `RULES.md` as the repository's Rule / Guard / Runner source.

## Workflow

1. Read `.harnesskit/facts.md`, current `RULES.md`, validation scripts, manifests, hook/CI config, and agent guidance.
2. For each rule, fill status, evidence, agent contract, Guard type, and Guard / runner binding.
3. Mark unsupported or unverified rules as `[NEEDS CLARIFICATION: ...]`, `N/A`, `未配置`, or `不适用` instead of enabling them from examples.
4. Distinguish Rule, Guard, and Runner; do not claim a Guard blocks changes without runner evidence.
5. Keep the project command table aligned with facts and the verification skill.

## Output

Update `RULES.md` only. If `AGENTS.md`, `ARCHITECTURE.md`, or skills need matching changes, invoke the corresponding fill skill.

## Boundaries

- Do not invent commands, CI, branch protection, coverage thresholds, typecheck, docs build, or PR requirements.
- Do not mark partial review judgments as deterministic Guard coverage.
- Do not treat `.harnesskit/facts.md` as a replacement for checking the actual runner config.
