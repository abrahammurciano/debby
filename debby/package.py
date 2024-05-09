from pathlib import Path

from debby.control_file import ControlFile
from debby.files import Files
from debby.meta.meta import Meta
from debby.scripts import Scripts


class Package:
    """A directory containing a Debian package.

    Args:
        metadata: The metadata for the package.
        control: The control file for the package.
        files: The files to put in the package.
    """

    def __init__(
        self, metadata: Meta, control: ControlFile, files: Files, scripts: Scripts
    ) -> None:
        self.metadata = metadata
        self.control = control
        self.files = files
        self.scripts = scripts

    def create(self, out_dir: Path) -> Path:
        """Create the directory structure of the package, which can be packaged into a .deb file with dpkg-deb."""
        directory = out_dir / self.metadata.full_name
        debian_dir = directory / "DEBIAN"
        debian_dir.mkdir(parents=True)
        debian_dir.chmod(0o755)
        self.control.create(debian_dir / "control")
        self.scripts.create(debian_dir)
        self.files.package(directory)
        return directory
