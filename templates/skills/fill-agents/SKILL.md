---
name: fill-agents
description: Fill or refresh AGENTS.md from .harnesskit/facts.md and verified repository evidence. Use after scan-facts when updating the top-level agent router, skill triggers, validation pointers, and drift policy.
---

# Fill Agents

Use this skill to update `AGENTS.md` as the top-level agent router. Consume `.harnesskit/facts.md`, then verify important claims against repository evidence before writing durable guidance.

## Workflow

1. Read `.harnesskit/facts.md`, current `AGENTS.md`, `RULES.md`, `ARCHITECTURE.md`, and `.agents/skills/*/SKILL.md`.
2. Keep `AGENTS.md` focused on policy, context routing, skill triggers, validation entrypoints, and drift handling.
3. Route detailed directory responsibilities to `ARCHITECTURE.md`, rules to `RULES.md`, and procedures to skills.
4. Reference `$harness-init`, `$scan-facts`, `$fill-agents`, `$fill-architecture`, `$fill-rules`, `$fill-skills`, `$implementation-strategy`, `$code-change-verification`, and `$pr-draft-summary` only when the corresponding skill exists.
5. Preserve unresolved items as `[NEEDS CLARIFICATION: ...]`.

## Output

Update `AGENTS.md` only. If another artifact needs changes, record the need in your final summary or invoke the matching fill skill.

## Boundaries

- Do not copy full architecture maps, rule catalogs, or skill bodies into `AGENTS.md`.
- Do not invent verification commands, CI, branch protection, PR templates, or release processes.
- Do not use `.harnesskit/facts.md` as the only source for high-impact claims; verify against repository facts.
