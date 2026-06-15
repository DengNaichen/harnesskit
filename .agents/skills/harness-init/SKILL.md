---
name: harness-init
description: Orchestrate Context Harness initialization after harnesskit init. Use when bootstrapping or refreshing the generated harness by running scan-facts, fill-agents, fill-architecture, fill-rules, fill-skills, and a final consistency review.
---

# Harness Init

Use this skill as the first user-facing workflow after `harnesskit init`. It coordinates the fact-first fill flow without copying every specialized instruction into one large skill.

## Workflow

1. Use `$scan-facts` to refresh `.harnesskit/facts.md` from repository evidence.
2. Resolve any high-impact questions that facts cannot settle before writing durable guidance.
3. Use `$fill-architecture` to update `ARCHITECTURE.md`.
4. Use `$fill-rules` to update `RULES.md`.
5. Use `$fill-agents` to update `AGENTS.md`.
6. Use `$fill-skills` to update project-specific sections inside generated skills.
7. Review consistency across `.harnesskit/facts.md`, `AGENTS.md`, `ARCHITECTURE.md`, `RULES.md`, `.agents/skills/`, `CLAUDE.md`, and the verification entrypoint.

## Consistency Review

Check that:

- skills referenced in `AGENTS.md` exist under `.agents/skills/`;
- `AGENTS.md` routes maps to `ARCHITECTURE.md`, rules to `RULES.md`, and procedures to skills;
- `RULES.md` command bindings agree with the verification skill and any runner config;
- `ARCHITECTURE.md` links point to real paths;
- unresolved uncertainty remains as `[NEEDS CLARIFICATION: ...]`.

## Boundaries

- Do not let this skill replace the specialized fill skills; invoke them in order.
- Do not invent repository facts, commands, CI, branch protection, or release policy.
- Do not run full runtime verification for guidance-only edits unless the edits also affect runtime code, templates, build/test config, or generated behavior.
