"""Issue construction helpers."""

from __future__ import annotations

from pathlib import Path

from .models import Issue, Severity


def issue(
    severity: Severity,
    code: str,
    project_path: Path,
    message: str,
    path: Path,
    *,
    line: int | None = None,
    found: str | None = None,
    expected: str | None = None,
    evidence: list[str] | None = None,
    suggested_fix: str | None = None,
    verify_command: str | None = None,
) -> Issue:
    display_path = relative_path(project_path, path)
    return Issue(
        severity=severity,
        code=code,
        path=display_path,
        message=message,
        line=line,
        found=found,
        expected=expected,
        evidence=evidence,
        suggested_fix=suggested_fix,
        verify_command=verify_command,
    )


def relative_path(project_path: Path, path: Path) -> str:
    try:
        relative = path.resolve().relative_to(project_path.resolve())
        return str(relative)
    except ValueError:
        return str(path)
