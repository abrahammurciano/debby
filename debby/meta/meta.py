from dataclasses import dataclass
from typing import Literal, TypedDict


class MetaVars(TypedDict, total=False):
    """A dictionary of metadata variables."""

    name: str
    source: str
    version: str
    section: str
    priority: str
    architecture: str
    essential: Literal["yes", "no"]
    maintainer: str
    description: str
    homepage: str
    depends: str
    pre_depends: str
    recommends: str
    suggests: str
    enhances: str
    breaks: str
    conflicts: str


@dataclass(kw_only=True, frozen=True, slots=True)
class Meta:
    """Metadata for a Debian package."""

    name: str
    source: str | None = None
    version: str
    section: str | None = None
    priority: str | None = None
    architecture: str = "all"
    essential: Literal["yes", "no"] | None = None
    maintainer: str
    description: str
    homepage: str | None = None
    depends: str | None = None
    pre_depends: str | None = None
    recommends: str | None = None
    suggests: str | None = None
    enhances: str | None = None
    breaks: str | None = None
    conflicts: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.name}_{self.version}_{self.architecture}"
