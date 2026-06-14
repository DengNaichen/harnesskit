#!/usr/bin/env python3
"""Tests for the standalone Harness Linter POC."""

from __future__ import annotations

import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from harness_lint import lint_project, main


def test_valid_harness_passes(tmp_path: Path) -> None:
    project = make_project(tmp_path)

    report = lint_project(project)

    assert report.passed, report.issues
    assert report.issues == []


def test_missing_codex_skill_fails(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".agents/skills/mykit-audit/SKILL.md").unlink()

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "codex.skill.missing")


def test_bad_config_json_fails(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".mykit/config.json").write_text("{broken\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "config.invalid_json")


def test_skill_frontmatter_is_required(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".agents/skills/mykit-audit/SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "skill.frontmatter.missing")


def test_local_markdown_link_must_exist(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text("[missing](docs/missing.md)\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.link.missing")


def test_skill_references_must_exist(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text("Use $missing-skill before changes.\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "skill.reference.missing")


def test_todo_checklist_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "<!-- mykit:todo-checklist:start -->\nopen checklist\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.todo_checklist.unpaired")


def test_tech_stack_block_matches_repo_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    append_tech_stack_block(
        project / "AGENTS.md",
        {
            "Language": "Python 3.11+",
            "Package manager": "uv",
            "CLI": "Typer",
            "Terminal output": "Rich",
            "Templates": "Jinja2",
            "Build backend": "Hatchling",
            "Tests": "pytest",
        },
    )

    report = lint_project(project)

    assert report.passed, report.issues


def test_tech_stack_block_must_match_repo_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    append_tech_stack_block(
        project / "AGENTS.md",
        {
            "Package manager": "npm",
            "Tests": "unittest",
        },
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "tech_stack.mismatch")


def test_tech_stack_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "<!-- mykit:tech-stack:start -->\n- Package manager: uv\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.tech_stack.unpaired")


def test_verification_docs_must_match_pytest_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\nRun `uv run python -m unittest discover -s tests`.\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "verification.stale_test_framework")
    issue = next(item for item in report.issues if item.code == "verification.stale_test_framework")
    assert issue.line == 3
    assert issue.found == "Run `uv run python -m unittest discover -s tests`."
    assert issue.expected == "uv run pytest"
    assert issue.evidence
    assert issue.suggested_fix
    assert issue.verify_command == "uv run pytest"


def test_unittest_docs_are_allowed_for_unittest_projects(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, test_framework="unittest")
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\nRun `uv run python -m unittest discover -s tests`.\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert report.passed, report.issues


def test_main_exit_code(tmp_path: Path) -> None:
    project = make_project(tmp_path)

    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 0

    (project / ".mykit/config.json").unlink()
    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 1


def assert_issue(report, code: str) -> None:
    assert any(issue.code == code for issue in report.issues), report.issues


def make_project(root: Path) -> Path:
    project = root / "demo"
    project.mkdir()

    (project / ".mykit").mkdir()
    (project / ".mykit/config.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "project_name": "demo",
                "mykit_version": "0.1.0",
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
        "# AGENTS\n\nUse $mykit-audit, $mykit-refresh, and $mykit-explain as needed.\n",
        encoding="utf-8",
    )
    (project / "CLAUDE.md").symlink_to("AGENTS.md")

    for skill_name in ("mykit-audit", "mykit-refresh", "mykit-explain"):
        skill_dir = project / ".agents" / "skills" / skill_name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: Test skill.\n---\n\n# {skill_name}\n",
            encoding="utf-8",
        )

    return project


def add_python_stack(project: Path, *, test_framework: str = "pytest") -> None:
    (project / "pyproject.toml").write_text(
        """[project]
name = "demo"
requires-python = ">=3.11"
dependencies = [
    "jinja2>=3.1.6",
    "rich>=15.0.0",
    "typer>=0.26.7",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
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
        "<!-- mykit:tech-stack:start -->",
        *[f"- {key}: {value}" for key, value in entries.items()],
        "<!-- mykit:tech-stack:end -->",
        "",
    ]
    with path.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines))
