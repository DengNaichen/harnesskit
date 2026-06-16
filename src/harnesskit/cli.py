"""Command-line entry point for harnesskit."""

from __future__ import annotations

import sys
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


app = typer.Typer(
    name="harnesskit",
    help="HarnessKit Context Harness CLI and Codex-facing toolkit.",
    add_completion=False,
)
integration_app = typer.Typer(help="Manage agent integrations.", add_completion=False)
app.add_typer(integration_app, name="integration")
console = Console()
INTEGRATION_MENU_OPTIONS = (
    ("codex", "Codex", ""),
    ("claude", "Claude Code", "coming soon"),
    ("cursor", "Cursor", "coming soon"),
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
    """HarnessKit Context Harness CLI and Codex-facing toolkit."""


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
    selected_integration = _select_integration(integration)
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
        str, typer.Argument(help="Integration key to install. Currently only 'codex'.")
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


def _print_result_files(result) -> None:
    if result.created:
        console.print("Written:")
        for path in result.created:
            console.print(f"  {path.relative_to(result.project_path)}")
    if result.skipped:
        console.print("Skipped existing files:")
        for path in result.skipped:
            console.print(f"  {path.relative_to(result.project_path)}")


def _select_integration(integration: str | None) -> str:
    if integration is not None:
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

    return str(selected)


def _integration_menu_choices() -> list[questionary.Choice]:
    available = set(available_integrations())
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
