from enum import Enum


class ScriptStage(Enum):
    """The stages of the package's lifecycle that a script can run at."""

    PREINST = ("preinst", "pre-installation")
    POSTINST = ("postinst", "post-installation")
    PRERM = ("prerm", "pre-removal")
    POSTRM = ("postrm", "post-removal")

    @property
    def name(self) -> str:
        """The name of the script. E.g. 'preinst', 'postinst', 'prerm', 'postrm'."""
        return self.value[0]

    @property
    def descriptive_name(self) -> str:
        """A descriptive name for the script. E.g. 'pre-installation', 'post-installation', 'pre-removal', 'post-removal'."""
        return self.value[1]
