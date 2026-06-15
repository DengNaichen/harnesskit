from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import (
    add_python_stack,
    assert_issue,
    make_project,
    verification_block,
    write_skill,
)


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


def test_configured_pre_commit_requires_verification_gate(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / ".pre-commit-config.yaml").write_text("repos: []\n", encoding="utf-8")
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

    assert not report.passed
    assert_issue(report, "verification.pre_commit_not_documented")
    issue = next(
        item
        for item in report.issues
        if item.code == "verification.pre_commit_not_documented"
    )
    assert issue.path == "AGENTS.md"
    assert issue.found == "harnesskit:verification block does not mention pre-commit"
    assert (
        issue.expected
        == "add `uv run pre-commit run --all-files` as a pre-commit gate or explicitly mark pre-commit inactive"
    )
    assert issue.verify_command == "uv run pre-commit run --all-files"


def test_configured_pre_commit_gate_is_allowed(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    (project / ".pre-commit-config.yaml").write_text("repos: []\n", encoding="utf-8")
    (project / "AGENTS.md").write_text(
        "# AGENTS\n\n"
        + verification_block(
            {
                "Tests": "uv run pytest",
                "Package build": "uv build",
                "Pre-commit hooks": "uv run pre-commit run --all-files",
            }
        ),
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not any(
        item.code == "verification.pre_commit_not_documented" for item in report.issues
    ), report.issues
