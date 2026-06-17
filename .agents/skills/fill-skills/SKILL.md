---
name: fill-skills
description: Fill project-specific sections inside generated skills from .harnesskit/facts.md. Use after scan-facts when configuring verification commands, compatibility boundaries, PR summary category signals, or other local skill placeholders.
---

# Fill Skills

Use this skill to update project-specific sections inside generated skills. It consumes [.harnesskit/facts.md](../../../.harnesskit/facts.md) and verifies high-impact claims against repository evidence.

## Workflow

1. Read [.harnesskit/facts.md](../../../.harnesskit/facts.md) and the generated skills in [.agents/skills/](../../skills/).
2. Update only project-specific sections that are meant to be filled, such as verification stack, compatibility boundaries, PR summary category signals, and local trigger notes.
3. Keep generic procedural guidance stable unless it conflicts with repository facts.
4. Preserve unresolved items as `[NEEDS CLARIFICATION: ...]`.
5. If a change affects [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), or [RULES.md](../../../RULES.md), invoke the matching fill skill instead of editing those artifacts from here.

## Output

Update `.agents/skills/*/SKILL.md` files only when their project-specific placeholders can be resolved from facts and repository evidence.

## Boundaries

- Do not add new tools or verification commands unless the repository already defines them or the user explicitly requests that change.
- Do not rewrite skill bodies into project documentation.
- Do not remove placeholders that still represent real uncertainty.
