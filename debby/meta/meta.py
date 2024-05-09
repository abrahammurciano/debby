from dataclasses import dataclass
from typing import Literal, Optional, TypedDict


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


@dataclass
class Meta:
    """Metadata for a Debian package."""

    name: str
    version: str
    maintainer: str
    description: str
    architecture: str
    source: Optional[str] = None
    section: Optional[str] = None
    priority: Optional[str] = None
    essential: Optional[Literal["yes", "no"]] = None
    homepage: Optional[str] = None
    depends: Optional[str] = None
    pre_depends: Optional[str] = None
    recommends: Optional[str] = None
    suggests: Optional[str] = None
    enhances: Optional[str] = None
    breaks: Optional[str] = None
    conflicts: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.name}_{self.version}_{self.architecture}"
