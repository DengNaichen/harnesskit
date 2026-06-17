"""Config file checks."""

from __future__ import annotations

import json
from pathlib import Path

from ..core.constants import CONFIG_SCHEMA_VERSION, SUPPORTED_INTEGRATIONS
from ..core.issues import issue
from ..core.models import Issue


def check_config(project_path: Path, issues: list[Issue]) -> dict[str, object] | None:
    config_path = project_path / ".harnesskit" / "config.json"
    if not config_path.is_file():
        issues.append(
            issue(
                "error",
                "config.missing",
                project_path,
                "missing .harnesskit/config.json",
                config_path,
            )
        )
        return None

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(
            issue(
                "error",
                "config.invalid_json",
                project_path,
                f"invalid JSON: {exc}",
                config_path,
            )
        )
        return None

    if not isinstance(config, dict):
        issues.append(
            issue(
                "error",
                "config.not_object",
                project_path,
                "config must be a JSON object",
                config_path,
            )
        )
        return None

    if config.get("schema_version") != CONFIG_SCHEMA_VERSION:
        issues.append(
            issue(
                "error",
                "config.schema_version",
                project_path,
                f"schema_version must be {CONFIG_SCHEMA_VERSION}",
                config_path,
            )
        )

    default_integration = config.get("default_integration")
    if (
        default_integration is not None
        and default_integration not in SUPPORTED_INTEGRATIONS
    ):
        issues.append(
            issue(
                "error",
                "config.default_integration",
                project_path,
                f"unsupported default_integration: {default_integration!r}",
                config_path,
            )
        )

    installed = config.get("installed_integrations")
    if not isinstance(installed, list) or not all(
        isinstance(item, str) for item in installed
    ):
        issues.append(
            issue(
                "error",
                "config.installed_integrations",
                project_path,
                "installed_integrations must be a list of strings",
                config_path,
            )
        )
        return config

    for integration in installed:
        if integration not in SUPPORTED_INTEGRATIONS:
            issues.append(
                issue(
                    "error",
                    "config.installed_integration.unsupported",
                    project_path,
                    f"unsupported installed integration: {integration!r}",
                    config_path,
                )
            )

    return config
