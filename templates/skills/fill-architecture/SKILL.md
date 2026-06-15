---
name: fill-architecture
description: Fill or refresh ARCHITECTURE.md from .harnesskit/facts.md and repository evidence. Use after scan-facts when updating the coarse repository map, important paths, generated assets, and boundary notes.
---

# Fill Architecture

Use this skill to update `ARCHITECTURE.md` as the coarse repository map for agents and contributors.

## Workflow

1. Read `.harnesskit/facts.md`, current `ARCHITECTURE.md`, top-level directories, manifests, tests, scripts, and existing docs.
2. Record only paths that help an agent choose where to look before making changes.
3. Describe responsibilities and boundaries, not every helper file.
4. Add `<!-- harnesskit:coverage=direct-children -->` only to important directories whose direct children should be documented and only after verifying the paths.
5. Preserve unresolved items as `[NEEDS CLARIFICATION: ...]`.

## Output

Update `ARCHITECTURE.md` only. If rules, skill triggers, or verification commands need changes, invoke the matching fill skill.

## Boundaries

- Do not turn `ARCHITECTURE.md` into a workflow guide, API reference, file inventory, or design essay.
- Do not treat `.harnesskit/facts.md` as a replacement for checking real paths.
- Do not list generated/vendor/cache/build output unless it is part of the agent-facing harness contract.
