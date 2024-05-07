from pathlib import Path

from debby.control_file import ControlFile
from debby.files import Files
from debby.meta.meta import Meta


class Package:
    """A directory containing a Debian package.

    Args:
        metadata: The metadata for the package.
        control: The control file for the package.
        files: The files to put in the package.
    """

    def __init__(self, metadata: Meta, control: ControlFile, files: Files) -> None:
        self.metadata = metadata
        self.control = control
        self.files = files

    def create(self, out_dir: Path) -> Path:
        """Create the directory structure of the package, which can be packaged into a .deb file with dpkg-deb."""
        directory = out_dir / self.metadata.full_name
        control_dir = directory / "DEBIAN"
        control_dir.mkdir(parents=True)
        control_dir.chmod(0o755)
        self.control.create(control_dir / "control")
        self.files.package(directory)
        return directory
