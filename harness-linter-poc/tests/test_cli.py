from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from harness_lint import main
from testing_helpers import make_project


def test_main_exit_code(tmp_path: Path) -> None:
    project = make_project(tmp_path)

    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 0

    (project / ".harnesskit/config.json").unlink()
    with redirect_stdout(StringIO()):
        assert main([str(project)]) == 1
