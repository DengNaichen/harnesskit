"""Skill metadata and reference checks."""

from __future__ import annotations

from pathlib import Path

from .constants import SKILL_REFERENCE_PATTERN
from .issues import issue
from .models import Issue


def check_skill_frontmatter(project_path: Path, issues: list[Issue]) -> None:
    for skill_path in sorted((project_path / ".agents" / "skills").glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            issues.append(
                issue(
                    "error",
                    "skill.frontmatter.missing",
                    project_path,
                    "SKILL.md must start with frontmatter",
                    skill_path,
                )
            )
            continue

        for required_key in ("name", "description"):
            if not frontmatter.get(required_key):
                issues.append(
                    issue(
                        "error",
                        f"skill.frontmatter.{required_key}",
                        project_path,
                        f"frontmatter must include {required_key}",
                        skill_path,
                    )
                )


def check_skill_references(project_path: Path, issues: list[Issue]) -> None:
    agents_path = project_path / "AGENTS.md"
    if not agents_path.is_file():
        return

    text = agents_path.read_text(encoding="utf-8")
    for skill_name in sorted(set(SKILL_REFERENCE_PATTERN.findall(text))):
        skill_path = project_path / ".agents" / "skills" / skill_name / "SKILL.md"
        if not skill_path.is_file():
            issues.append(
                issue(
                    "error",
                    "skill.reference.missing",
                    project_path,
                    f"AGENTS.md references ${skill_name}, but .agents/skills/{skill_name}/SKILL.md does not exist",
                    agents_path,
                )
            )


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")

    return None
