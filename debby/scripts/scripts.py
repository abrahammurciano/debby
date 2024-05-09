from pathlib import Path

from debby.args import Args

from .script import Script
from .script_stage import ScriptStage


class Scripts:
    """Scripts to run at different stages of the package's lifecycle."""

    def __init__(self, args: Args) -> None:
        self._scripts = tuple(
            Script(stage, path, commands)
            for stage, path, commands in (
                (ScriptStage.PREINST, args.preinst, args.preinst_cmd),
                (ScriptStage.POSTINST, args.postinst, args.postinst_cmd),
                (ScriptStage.PRERM, args.prerm, args.prerm_cmd),
                (ScriptStage.POSTRM, args.postrm, args.postrm_cmd),
            )
            if path or commands
        )

    def create(self, path: Path) -> None:
        for script in self._scripts:
            script.create(path)
