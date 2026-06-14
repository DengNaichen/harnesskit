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
    (project / ".agents/skills/harnesskit-audit/SKILL.md").unlink()

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "codex.skill.missing")


def test_bad_config_json_fails(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".harnesskit/config.json").write_text("{broken\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "config.invalid_json")


def test_skill_frontmatter_is_required(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".agents/skills/harnesskit-audit/SKILL.md").write_text(
        "# no frontmatter\n", encoding="utf-8"
    )

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
    (project / "AGENTS.md").write_text(
        "Use $missing-skill before changes.\n", encoding="utf-8"
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "skill.reference.missing")


def test_todo_checklist_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "<!-- harnesskit:todo-checklist:start -->\nopen checklist\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.todo_checklist.unpaired")


def test_tech_stack_block_matches_repo_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    append_verification_block(
        project / "AGENTS.md",
        {"Package build": "uv build"},
    )
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
        "<!-- harnesskit:tech-stack:start -->\n- Package manager: uv\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.tech_stack.unpaired")


def test_verification_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"])
    (project / "AGENTS.md").write_text(
        "<!-- harnesskit:verification:start -->\n- Tests: uv run pytest\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.verification.unpaired")


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
    issue = next(
        item
        for item in report.issues
        if item.code == "verification.stale_test_framework"
    )
    assert issue.line == 3
    assert issue.found == "Run `uv run python -m unittest discover -s tests`."
    assert issue.expected == "uv run pytest"
    assert issue.evidence
    assert issue.suggested_fix
    assert issue.verify_command == "uv run pytest"


def test_unittest_docs_are_allowed_for_unittest_projects(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, test_framework="unittest", build_system=False)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\nRun `uv run python -m unittest discover -s tests`.\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert report.passed, report.issues


def test_declared_ruff_requires_verification_block(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"])
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\nRuff is installed but not currently a completion gate.\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "verification.block_missing")
    issue = next(
        item for item in report.issues if item.code == "verification.block_missing"
    )
    assert issue.severity == "error"
    assert issue.path == "AGENTS.md"
    assert issue.found == "AGENTS.md has no verification block"
    assert issue.expected
    assert issue.evidence == [
        "pyproject.toml declares ruff",
        "AGENTS.md is a verification doc",
    ]
    assert issue.suggested_fix
    assert issue.verify_command == "uv run ruff check ."


def test_declared_ruff_reports_each_verification_doc_that_omits_it(
    tmp_path: Path,
) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"])
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n" + verification_block({"Tests": "uv run pytest"}),
        encoding="utf-8",
    )
    write_skill(
        project,
        "code-change-verification",
        "# Verification\n\n" + verification_block({"Tests": "uv run pytest"}),
    )

    report = lint_project(project)

    issues = [
        item
        for item in report.issues
        if item.code == "verification.tool_not_documented"
    ]
    assert {item.path for item in issues} == {
        "AGENTS.md",
        ".agents/skills/code-change-verification/SKILL.md",
    }
    verification_skill_issue = next(
        item
        for item in issues
        if item.path == ".agents/skills/code-change-verification/SKILL.md"
    )
    assert (
        verification_skill_issue.found
        == "harnesskit:verification block does not mention Ruff"
    )
    assert (
        verification_skill_issue.expected
        == "add Ruff to the verification block as an active gate or explicitly inactive"
    )


def test_documented_ruff_dependency_is_allowed(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"])
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {"Tests": "uv run pytest", "Python lint": "uv run ruff check ."}
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code == "verification.tool_not_documented" for item in report.issues
    ), report.issues


def test_configured_ruff_formatter_requires_format_check_gate(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"], ruff_formatter=True)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {"Tests": "uv run pytest", "Python lint": "uv run ruff check ."}
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "verification.format_not_documented")
    issue = next(
        item
        for item in report.issues
        if item.code == "verification.format_not_documented"
    )
    assert issue.path == "AGENTS.md"
    assert issue.found == "harnesskit:verification block does not mention Ruff format"
    assert (
        issue.expected
        == "add `uv run ruff format --check .` as a format gate or explicitly mark Ruff format inactive"
    )
    assert issue.verify_command == "uv run ruff format --check ."


def test_configured_ruff_formatter_rejects_mutating_format_command(
    tmp_path: Path,
) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"], ruff_formatter=True)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Python lint": "uv run ruff check .",
                "Python format": "uv run ruff format .",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "verification.format_command_mutates")
    issue = next(
        item
        for item in report.issues
        if item.code == "verification.format_command_mutates"
    )
    assert issue.found == "- Python format: uv run ruff format ."
    assert issue.expected == "uv run ruff format --check ."
    assert issue.verify_command == "uv run ruff format --check ."


def test_configured_ruff_formatter_check_gate_is_allowed(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"], ruff_formatter=True)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Python lint": "uv run ruff check .",
                "Python format": "uv run ruff format --check .",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code.startswith("verification.format") for item in report.issues
    ), report.issues


def test_configured_ruff_formatter_can_be_marked_inactive(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project, dev_dependencies=["ruff>=0.15.17"], ruff_formatter=True)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Python lint": "uv run ruff check .",
                "Python format": "Ruff format inactive",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code.startswith("verification.format") for item in report.issues
    ), report.issues


def test_configured_package_build_requires_verification_gate(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n" + verification_block({"Tests": "uv run pytest"}),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "verification.build_not_documented")
    issue = next(
        item
        for item in report.issues
        if item.code == "verification.build_not_documented"
    )
    assert issue.path == "AGENTS.md"
    assert issue.found == "harnesskit:verification block does not mention package build"
    assert (
        issue.expected
        == "add `uv build` as a package build gate or explicitly mark package build inactive"
    )
    assert issue.verify_command == "uv build"


def test_configured_package_build_gate_is_allowed(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Package build": "uv build",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code == "verification.build_not_documented" for item in report.issues
    ), report.issues


def test_configured_package_build_can_be_marked_inactive(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Package build": "inactive",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code == "verification.build_not_documented" for item in report.issues
    ), report.issues


def test_main_exit_code(tmp_path: Path) -> None:
    project = make_project(tmp_path)

    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 0

    (project / ".harnesskit/config.json").unlink()
    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 1


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
        "# AGENTS\n\nUse $harnesskit-audit, $harnesskit-refresh, and $harnesskit-explain as needed.\n",
        encoding="utf-8",
    )
    (project / "CLAUDE.md").symlink_to("AGENTS.md")

    for skill_name in ("harnesskit-audit", "harnesskit-refresh", "harnesskit-explain"):
        write_skill(project, skill_name, f"# {skill_name}\n")

    return project


def write_skill(project: Path, skill_name: str, body: str) -> None:
    skill_dir = project / ".agents" / "skills" / skill_name
    skill_dir.mkdir(parents=True)
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


def verification_block(entries: dict[str, str]) -> str:
    lines = [
        "<!-- harnesskit:verification:start -->",
        *[f"- {key}: {value}" for key, value in entries.items()],
        "<!-- harnesskit:verification:end -->",
        "",
    ]
    return "\n".join(lines)
