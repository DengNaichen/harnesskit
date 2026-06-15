from __future__ import annotations

import json
from pathlib import Path


def assert_issue(report, code: str) -> None:
    assert any(issue.code == code for issue in report.issues), report.issues


def make_project(root: Path) -> Path:
    project = root / "demo"
    project.mkdir()

    (project / ".harnesskit").mkdir()
    (project / ".harnesskit/config.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "project_name": "demo",
                "harnesskit_version": "0.1.0",
                "default_integration": "codex",
                "installed_integrations": ["codex"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (project / "AGENTS.md").write_text(
        "# AGENTS\n\nUse $scan-facts and $code-change-verification as needed.\n",
        encoding="utf-8",
    )
    (project / "CLAUDE.md").symlink_to("AGENTS.md")

    write_skill(
        project,
        "code-change-verification",
        "# code-change-verification\n\n"
        + verification_block(
            {
                "Python lint": "Ruff inactive",
                "Python format": "Ruff format inactive",
                "Package build": "inactive",
                "Pre-commit hooks": "inactive",
            }
        ),
    )
    for skill_name in (
        "fill-agents",
        "fill-architecture",
        "fill-rules",
        "fill-skills",
        "harness-init",
        "implementation-strategy",
        "pr-draft-summary",
        "scan-facts",
        "scan-stack",
    ):
        write_skill(project, skill_name, f"# {skill_name}\n")

    return project


def write_skill(project: Path, skill_name: str, body: str) -> None:
    skill_dir = project / ".agents" / "skills" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: Test skill.\n---\n\n{body}",
        encoding="utf-8",
    )


def add_python_stack(
    project: Path,
    *,
    test_framework: str = "pytest",
    dev_dependencies: list[str] | None = None,
    ruff_formatter: bool = False,
    build_system: bool = True,
) -> None:
    dev_dependency_lines = ""
    if dev_dependencies:
        entries = "\n".join(f'    "{dependency}",' for dependency in dev_dependencies)
        dev_dependency_lines = f"""
[dependency-groups]
dev = [
{entries}
]
"""
    ruff_formatter_lines = ""
    if ruff_formatter:
        ruff_formatter_lines = """
[tool.ruff.format]
quote-style = "double"
"""
    build_system_lines = ""
    if build_system:
        build_system_lines = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

    (project / "pyproject.toml").write_text(
        f"""[project]
name = "demo"
requires-python = ">=3.11"
dependencies = [
    "jinja2>=3.1.6",
    "rich>=15.0.0",
    "typer>=0.26.7",
]
{build_system_lines}
{dev_dependency_lines}
{ruff_formatter_lines}
""",
        encoding="utf-8",
    )
    (project / "uv.lock").write_text("", encoding="utf-8")
    tests_dir = project / "tests"
    tests_dir.mkdir()
    if test_framework == "pytest":
        (tests_dir / "test_demo.py").write_text("import pytest\n", encoding="utf-8")
    else:
        (tests_dir / "test_demo.py").write_text("import unittest\n", encoding="utf-8")


def append_tech_stack_block(path: Path, entries: dict[str, str]) -> None:
    lines = [
        "",
        "<!-- harnesskit:tech-stack:start -->",
        *[f"- {key}: {value}" for key, value in entries.items()],
        "<!-- harnesskit:tech-stack:end -->",
        "",
    ]
    with path.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines))


def append_verification_block(path: Path, entries: dict[str, str]) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write("\n" + verification_block(entries))


def write_architecture_doc(project: Path, block: str) -> None:
    (project / "ARCHITECTURE.md").write_text(
        "# Architecture\n\n"
        + "\n".join(line.strip() for line in block.strip().splitlines())
        + "\n",
        encoding="utf-8",
    )


def verification_block(entries: dict[str, str]) -> str:
    lines = [
        "<!-- harnesskit:verification:start -->",
        *[f"- {key}: {value}" for key, value in entries.items()],
        "<!-- harnesskit:verification:end -->",
        "",
    ]
    return "\n".join(lines)
