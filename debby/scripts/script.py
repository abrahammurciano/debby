from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

from .script_stage import ScriptStage


@dataclass
class Script:
    """A script to run at a specific stage of the package's lifecycle."""

    stage: ScriptStage
    """The stage of the package's lifecycle to run the script at."""

    path: Optional[Path] = None
    """The path to the script to run at the given stage."""

    commands: Sequence[str] = ()
    """The commands to run at the given stage."""

    def __post_init__(self) -> None:
        if self.path is None and not self.commands:
            raise ValueError("Either path or commands must be provided.")
        if self.path is not None and self.commands:
            raise ValueError("Only one of path or commands may be provided.")

    def create(self, path: Path) -> None:
        """Put the script in the given directory."""
        target = path / self.stage.name
        if self.path:
            target.write_bytes(self.path.read_bytes())
        else:
            target.write_text("\n".join(("#!/bin/sh", *self.commands)))
        target.chmod(0o755)
