from pathlib import Path
from typing import Iterable

from debby.files import Files
from debby.meta import Meta


class ControlFile:
    def __init__(
        self,
        meta: Meta,
        files: Files,
        template: Path | None = None,
        include_size: bool = True,
    ) -> None:
        self._meta = meta
        self._files = files
        self._template = template
        self._include_size = include_size

    def create(self, path: Path) -> None:
        path.write_text("\n".join(self._lines()) + "\n")

    def _lines(self) -> Iterable[str]:
        if not self._template:
            return self._default_lines()
        return (
            line.format(metadata=self._meta, files=self._files)
            for line in self._template.read_text().splitlines()
        )

    def _default_lines(self) -> Iterable[str]:
        yield f"Package: {self._meta.name}"
        if self._meta.source:
            yield f"Source: {self._meta.source}"
        yield f"Version: {self._meta.version}"
        if self._meta.section:
            yield f"Section: {self._meta.section}"
        if self._meta.priority:
            yield f"Priority: {self._meta.priority}"
        yield f"Architecture: {self._meta.architecture}"
        if self._meta.essential:
            yield f"Essential: {self._meta.essential}"
        if self._include_size and self._files.total_size:
            yield f"Installed-Size: {self._files.total_size}"
        yield f"Maintainer: {self._meta.maintainer}"
        yield f"Description: {self._meta.description}"
        if homepage := self._meta.homepage:
            yield f"Homepage: {homepage}"
        if depends := self._meta.depends:
            yield f"Depends: {depends}"
        if pre_depends := self._meta.pre_depends:
            yield f"Pre-Depends: {pre_depends}"
        if recommends := self._meta.recommends:
            yield f"Recommends: {recommends}"
        if suggests := self._meta.suggests:
            yield f"Suggests: {suggests}"
        if enhances := self._meta.enhances:
            yield f"Enhances: {enhances}"
        if breaks := self._meta.breaks:
            yield f"Breaks: {breaks}"
        if conflicts := self._meta.conflicts:
            yield f"Conflicts: {conflicts}"
