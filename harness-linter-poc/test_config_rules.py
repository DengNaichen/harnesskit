from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import assert_issue, make_project


def test_bad_config_json_fails(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".harnesskit/config.json").write_text("{broken\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "config.invalid_json")
