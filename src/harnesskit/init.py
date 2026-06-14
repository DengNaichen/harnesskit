"""Project initialization logic."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from jinja2 import Environment, StrictUndefined, TemplateError

from . import __version__


JINJA_TEMPLATE_SUFFIX = ".j2"
DEFAULT_INTEGRATION = "codex"
SUPPORTED_INTEGRATIONS = ("codex",)
CONFIG_SCHEMA_VERSION = 1
HARNESSKIT_DIR = ".harnesskit"
CONFIG_FILE = "config.json"
INTEGRATIONS_TEMPLATE_DIR = "integrations"
SKILLS_TEMPLATE_DIR = "skills"
CODEX_SKILL_OUTPUT_DIR = Path(".agents") / "skills"
TEMPLATE_SYMLINKS = {
    Path("CLAUDE.md"): Path("AGENTS.md"),
}

JINJA_ENV = Environment(
    autoescape=False,
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


class InitError(Exception):
    """Raised when project initialization cannot continue."""


@dataclass(frozen=True)
class InitResult:
    project_path: Path
    created: list[Path]
    skipped: list[Path]


def available_integrations() -> tuple[str, ...]:
    return SUPPORTED_INTEGRATIONS


def init_project(
    project: str | None,
    *,
    here: bool = False,
    force: bool = False,
    integration: str = DEFAULT_INTEGRATION,
) -> InitResult:
    integration = _validate_integration(integration)
    project_path = _resolve_project_path(project, here=here)
    template_root = _locate_templates()

    if project_path.exists() and not project_path.is_dir():
        raise InitError(f"{project_path} exists but is not a directory")

    project_path.mkdir(parents=True, exist_ok=True)

    context = {"PROJECT_NAME": project_path.name}
    result = _copy_template_tree(
        template_root,
        project_path,
        context,
        force=force,
        excluded_top_dirs={INTEGRATIONS_TEMPLATE_DIR, SKILLS_TEMPLATE_DIR},
    )

    integration_result = _install_integration_assets(
        project_path,
        integration,
        context,
        force=force,
    )
    config_path = _write_config(project_path, integration)

    return InitResult(
        project_path=project_path,
        created=[*result.created, *integration_result.created, config_path],
        skipped=[*result.skipped, *integration_result.skipped],
    )


def install_integration(
    project_path: str | Path,
    integration: str,
    *,
    force: bool = False,
) -> InitResult:
    integration = _validate_integration(integration)
    resolved_project_path = Path(project_path).expanduser().resolve()

    if not resolved_project_path.is_dir():
        raise InitError(f"{resolved_project_path} is not a directory")

    if not _config_path(resolved_project_path).is_file():
        raise InitError("not a harnesskit project; run `harnesskit init --here` first")

    context = {"PROJECT_NAME": resolved_project_path.name}
    result = _install_integration_assets(
        resolved_project_path,
        integration,
        context,
        force=force,
    )
    config_path = _write_config(resolved_project_path, integration)

    return InitResult(
        project_path=resolved_project_path,
        created=[*result.created, config_path],
        skipped=result.skipped,
    )


def _copy_template_tree(
    source_root: Path,
    destination_root: Path,
    context: dict[str, str],
    *,
    force: bool,
    excluded_top_dirs: Iterable[str] = (),
) -> InitResult:
    created: list[Path] = []
    skipped: list[Path] = []
    excluded = set(excluded_top_dirs)

    for source in sorted(source_root.rglob("*")):
        if source.is_dir():
            continue

        source_relative_path = source.relative_to(source_root)
        if source_relative_path.parts and source_relative_path.parts[0] in excluded:
            continue

        relative_path = _template_output_path(source_relative_path)
        destination = destination_root / relative_path
        symlink_target = _template_symlink_target(source_relative_path, source)

        if (destination.exists() or destination.is_symlink()) and not force:
            skipped.append(destination)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if symlink_target is not None:
            _write_symlink(destination, symlink_target)
        else:
            _copy_template(source, destination, context)
        created.append(destination)

    return InitResult(project_path=destination_root, created=created, skipped=skipped)


def _install_integration_assets(
    project_path: Path,
    integration: str,
    context: dict[str, str],
    *,
    force: bool,
) -> InitResult:
    integration = _validate_integration(integration)
    template_root = _locate_templates()
    source_root = template_root / INTEGRATIONS_TEMPLATE_DIR / integration

    if source_root.exists() and not source_root.is_dir():
        raise InitError(f"templates for integration '{integration}' were not found")

    if source_root.is_dir():
        integration_result = _copy_template_tree(source_root, project_path, context, force=force)
    else:
        integration_result = InitResult(project_path=project_path, created=[], skipped=[])

    if integration == DEFAULT_INTEGRATION:
        skill_result = _install_shared_skill_assets(project_path, context, force=force)
        return InitResult(
            project_path=project_path,
            created=[*integration_result.created, *skill_result.created],
            skipped=[*integration_result.skipped, *skill_result.skipped],
        )

    return integration_result


def _install_shared_skill_assets(
    project_path: Path,
    context: dict[str, str],
    *,
    force: bool,
) -> InitResult:
    template_root = _locate_templates()
    source_root = template_root / SKILLS_TEMPLATE_DIR

    if not source_root.is_dir():
        raise InitError("shared skill templates were not found")

    return _copy_template_tree(
        source_root,
        project_path / CODEX_SKILL_OUTPUT_DIR,
        context,
        force=force,
    )


def _resolve_project_path(project: str | None, *, here: bool) -> Path:
    if project == ".":
        here = True
        project = None

    if here and project:
        raise InitError("pass either a project name or --here, not both")

    if here:
        return Path.cwd()

    if not project:
        raise InitError("missing project name; pass a name, '.', or --here")

    return Path(project).expanduser().resolve()


def _locate_templates() -> Path:
    package_templates = Path(__file__).parent / "templates"
    if package_templates.is_dir():
        return package_templates

    source_templates = Path(__file__).resolve().parents[2] / "templates"
    if source_templates.is_dir():
        return source_templates

    raise InitError("bundled templates were not found")


def _template_output_path(path: Path) -> Path:
    if path.name.endswith(JINJA_TEMPLATE_SUFFIX):
        return path.with_name(path.name[: -len(JINJA_TEMPLATE_SUFFIX)])
    return path


def _template_symlink_target(path: Path, source: Path) -> Path | None:
    output_path = _template_output_path(path)
    if output_path in TEMPLATE_SYMLINKS:
        return TEMPLATE_SYMLINKS[output_path]
    if source.is_symlink():
        return source.readlink()
    return None


def _write_symlink(destination: Path, target: Path) -> None:
    if destination.exists() or destination.is_symlink():
        destination.unlink()
    destination.symlink_to(target)


def _copy_template(source: Path, destination: Path, context: dict[str, str]) -> None:
    if source.is_symlink():
        _write_symlink(destination, source.readlink())
        return

    if source.name.endswith(JINJA_TEMPLATE_SUFFIX):
        text = source.read_text(encoding="utf-8")
        try:
            rendered = JINJA_ENV.from_string(text).render(context)
        except TemplateError as exc:
            raise InitError(f"failed to render template {source}: {exc}") from exc
        destination.write_text(rendered, encoding="utf-8")
        return

    shutil.copy2(source, destination)


def _validate_integration(integration: str) -> str:
    normalized = integration.strip().lower()
    if normalized not in SUPPORTED_INTEGRATIONS:
        available = ", ".join(SUPPORTED_INTEGRATIONS)
        raise InitError(f"unsupported integration '{integration}'. Available integrations: {available}")
    return normalized


def _config_path(project_path: Path) -> Path:
    return project_path / HARNESSKIT_DIR / CONFIG_FILE


def _write_config(project_path: Path, integration: str) -> Path:
    integration = _validate_integration(integration)
    config_path = _config_path(project_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _read_config(project_path)
    installed = existing.get("installed_integrations", [])
    if not isinstance(installed, list):
        installed = []

    installed_integrations = [item for item in installed if isinstance(item, str)]
    if integration not in installed_integrations:
        installed_integrations.append(integration)

    config = {
        "schema_version": CONFIG_SCHEMA_VERSION,
        "project_name": project_path.name,
        "harnesskit_version": __version__,
        "default_integration": integration,
        "installed_integrations": installed_integrations,
    }
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path


def _read_config(project_path: Path) -> dict[str, object]:
    config_path = _config_path(project_path)
    if not config_path.exists():
        return {}

    try:
        raw_config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InitError(f"failed to read {config_path}: {exc}") from exc

    if not isinstance(raw_config, dict):
        raise InitError(f"{config_path} must contain a JSON object")

    return raw_config
