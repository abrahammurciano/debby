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
            target.symlink_to(src)

    @classmethod
    def _normalize_files(
        cls, files: Iterable[Tuple[Path, Path]]
    ) -> Mapping[Path, Path]:
        return {
            dst.relative_to(dst.anchor) if dst.is_absolute() else dst: src
            for src, dst in files
        }

    @property
    def sources(self) -> Iterable[Path]:
        return self._files.values()

    @property
    def destinations(self) -> Iterable[Path]:
        return self._files.keys()

    @cached_property
    def total_size(self) -> int:
        return sum(
            (max(f.resolve().stat().st_size, 1024) // 1024) * 1024 for f in self.sources
        )

    def __getitem__(self, key: Path) -> Path:
        return self._files[key]

    def __iter__(self) -> Iterator[Path]:
        return iter(self._files)

    def __len__(self) -> int:
        return len(self._files)
