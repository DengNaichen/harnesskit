"""Command-line entry point for harnesskit."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import questionary
import typer
from rich.console import Console

from . import __version__
from .init import (
    DEFAULT_INTEGRATION,
    InitError,
    available_integrations,
    init_project,
    install_integration,
)
from .linter.runner import lint_project, print_json_report, print_text_report


app = typer.Typer(
    name="harnesskit",
    help="HarnessKit Context Harness CLI and agent-facing toolkit.",
    add_completion=False,
)
integration_app = typer.Typer(help="Manage agent integrations.", add_completion=False)
app.add_typer(integration_app, name="integration")
console = Console()
NO_INTEGRATION_MENU_VALUE = "__none__"
INTEGRATION_MENU_OPTIONS = (
    ("codex", "Codex", ""),
    ("claude", "Claude Code", ""),
    ("infcode", "infCode", "coming soon"),
    ("cursor", "Cursor", "coming soon"),
    (NO_INTEGRATION_MENU_VALUE, "None / Skip for now", ""),
)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"harnesskit {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
) -> None:
    """HarnessKit Context Harness CLI and agent-facing toolkit."""


@app.command("init")
def init_command(
    project: Annotated[
        str | None,
        typer.Argument(help="Project directory, or '.' for the current directory."),
    ] = None,
    here: Annotated[
        bool, typer.Option("--here", help="Initialize the current directory.")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Overwrite existing generated files.")
    ] = False,
    no_integration: Annotated[
        bool,
        typer.Option(
            "--no-integration",
            help="Initialize core Context Harness assets without agent integration.",
        ),
    ] = False,
    integration: Annotated[
        str | None,
        typer.Option(
            "--integration",
            help=(
                "Agent integration to install. If omitted, HarnessKit opens an "
                "interactive selector."
            ),
        ),
    ] = None,
) -> None:
    """Initialize a Context Harness from bundled templates."""
    selected_integration = _select_integration(
        integration, no_integration=no_integration
    )
    try:
        result = init_project(
            project,
            here=here,
            force=force,
            integration=selected_integration,
        )
    except InitError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Initialized [green]{result.project_path}[/green]")
    _print_result_files(result)


@integration_app.command("list")
def integration_list_command() -> None:
    """List supported agent integrations."""
    console.print("Available integrations:")
    for integration in available_integrations():
        default_label = (
            " [dim](default)[/dim]" if integration == DEFAULT_INTEGRATION else ""
        )
        console.print(f"  [cyan]{integration}[/cyan]{default_label}")


@integration_app.command("install")
def integration_install_command(
    integration: Annotated[
        str,
        typer.Argument(help="Integration key to install, such as 'codex' or 'claude'."),
    ],
    force: Annotated[
        bool, typer.Option("--force", help="Overwrite existing integration files.")
    ] = False,
) -> None:
    """Install an agent integration into the current harnesskit project."""
    try:
        result = install_integration(".", integration, force=force)
    except InitError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Installed [cyan]{integration}[/cyan] integration in [green]{result.project_path}[/green]"
    )
    _print_result_files(result)


@app.command("lint")
def lint_command(
    project: Annotated[str, typer.Argument(help="Project directory to lint.")] = ".",
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Print a machine-readable JSON report."),
    ] = False,
    external_markdownlint: Annotated[
        bool,
        typer.Option(
            "--external-markdownlint",
            help="Run markdownlint-cli2 or markdownlint when installed.",
        ),
    ] = False,
) -> None:
    """Check Context Harness assets for drift and broken links."""
    report = lint_project(
        Path(project),
        external_markdownlint=external_markdownlint,
    )
    if json_output:
        print_json_report(report)
    else:
        print_text_report(report)

    if not report.passed:
        raise typer.Exit(1)


def _print_result_files(result) -> None:
    if result.created:
        console.print("Written:")
        for path in result.created:
            console.print(f"  {path.relative_to(result.project_path)}")
    if result.skipped:
        console.print("Skipped existing files:")
        for path in result.skipped:
            console.print(f"  {path.relative_to(result.project_path)}")


def _select_integration(
    integration: str | None,
    *,
    no_integration: bool = False,
) -> str | None:
    if integration is not None and no_integration:
        console.print("[red]error:[/red] pass either --integration or --no-integration")
        raise typer.Exit(1)

    if no_integration:
        return None

    if integration is not None:
        if integration.strip().lower() == "none":
            return None
        return integration

    if not _has_interactive_terminal():
        console.print(
            f"[dim]No interactive terminal detected; using {DEFAULT_INTEGRATION}.[/dim]"
        )
        return DEFAULT_INTEGRATION

    selected = questionary.select(
        "Select agent integration",
        choices=_integration_menu_choices(),
        default=DEFAULT_INTEGRATION,
        pointer=">",
        qmark="",
    ).ask()

    if selected is None:
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit(1)

    if selected == NO_INTEGRATION_MENU_VALUE:
        return None

    return str(selected)


def _integration_menu_choices() -> list[questionary.Choice]:
    available = {NO_INTEGRATION_MENU_VALUE, *available_integrations()}
    choices: list[questionary.Choice] = []
    known_menu_integrations: set[str] = set()

    for key, label, disabled_reason in INTEGRATION_MENU_OPTIONS:
        known_menu_integrations.add(key)
        title = f"{label} (default)" if key == DEFAULT_INTEGRATION else label
        choices.append(
            questionary.Choice(
                title=title,
                value=key,
                disabled=None if key in available else disabled_reason,
            )
        )

    for key in available_integrations():
        if key in known_menu_integrations:
            continue
        choices.append(questionary.Choice(title=key, value=key))

    return choices


def _has_interactive_terminal() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
