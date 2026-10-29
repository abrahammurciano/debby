from pathlib import Path
import tempfile
import tarfile
import unix_ar

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

    def build(self, output_path: Path) -> Path:
        """Build a .deb file directly at the given path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            package_dir = tmpdir_path / self.metadata.full_name
            debian_dir = package_dir / "DEBIAN"
            debian_dir.mkdir(parents=True)
            debian_dir.chmod(0o755)
            self.control.create(debian_dir / "control")
            self.scripts.create(debian_dir)
            self.files.package(package_dir)

            control_tar = tmpdir_path / "control.tar.gz"
            with tarfile.open(control_tar, "w:gz", format=tarfile.USTAR_FORMAT) as tar:
                control_file = debian_dir / "control"
                tar.add(control_file, arcname="control")
                for script_name in ("preinst", "postinst", "prerm", "postrm"):
                    script_path = debian_dir / script_name
                    if script_path.exists():
                        tar.add(script_path, arcname=script_name)

            data_tar = tmpdir_path / "data.tar.gz"
            with tarfile.open(data_tar, "w:gz", format=tarfile.USTAR_FORMAT) as tar:
                for item in package_dir.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(package_dir)
                        if rel_path.parts and rel_path.parts[0] == "DEBIAN":
                            continue
                        tar.add(item, arcname=rel_path)

            debian_binary = tmpdir_path / "debian-binary"
            debian_binary.write_text("2.0\n")

            try:
                ar = unix_ar.open(output_path, "w")
                ar.add(str(debian_binary), arcname="debian-binary")
                ar.add(str(control_tar), arcname="control.tar.gz")
                ar.add(str(data_tar), arcname="data.tar.gz")
            finally:
                ar.close()

        return output_path
