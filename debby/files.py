import shutil
from functools import cached_property
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Tuple


class Files(Mapping[Path, Path]):
    """A mapping of target paths in the package to source paths on the filesystem.

    Args:
        files: An iterable of pairs of source paths and destination paths.
    """

    def __init__(self, files: Iterable[Tuple[Path, Path]]) -> None:
        self._files = self._normalize_files(files)

    def __post_init__(self) -> None:
        if any(
            not src.exists() or dst.is_absolute() for dst, src in self._files.items()
        ):
            raise ValueError(
                "source files must all exist and destination paths must all be relative"
            )

    def package(self, path: Path) -> None:
        for dst, src in self.items():
            target = path / dst
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, target)
            else:
                shutil.copy2(src, target)

    @property
    def sources(self) -> Iterable[Path]:
        return self._files.values()

    @property
    def destinations(self) -> Iterable[Path]:
        return self._files.keys()

    @cached_property
    def total_size(self) -> int:
        return sum(
            self._size_of(path) for source in self.sources for path in source.rglob("*")
        )

    def __getitem__(self, key: Path) -> Path:
        return self._files[key]

    def __iter__(self) -> Iterator[Path]:
        return iter(self._files)

    def __len__(self) -> int:
        return len(self._files)

    @classmethod
    def _normalize_files(
        cls, files: Iterable[Tuple[Path, Path]]
    ) -> Mapping[Path, Path]:
        return {
            dst.relative_to(dst.anchor) if dst.is_absolute() else dst: src
            for src, dst in files
        }

    @classmethod
    def _size_of(cls, path: Path) -> int:
        """Get the size of a filesystem object for the Installed-Size field in the control file.

        The disk space is given as the accumulated size of each regular file and symlink rounded to 1 KiB used units, and a baseline of 1 KiB for any other filesystem object type.

        https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-installed-size
        """
        if path.is_file():
            return max(1024, (path.stat().st_size // 1024) * 1024)
        return 1024
