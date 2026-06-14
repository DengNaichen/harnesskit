"""Shared report models for the standalone Harness Linter POC."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    path: str
    message: str
    line: int | None = None
    found: str | None = None
    expected: str | None = None
    evidence: list[str] | None = None
    suggested_fix: str | None = None
    verify_command: str | None = None


@dataclass(frozen=True)
class Report:
    project_path: str
    issues: list[Issue]

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def passed(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class MarkedBlock:
    start_line: int
    content: str
