import tomllib
from pathlib import Path

from .meta import MetaVars
from .meta_loader import MetaLoader


class PoetryMetaLoader(MetaLoader):
    """Load poetry metadata from a pyproject.toml file."""

    @property
    def _pyproject(self) -> Path:
        assert self._args.poetry is not None
        return self._args.poetry

    def load_from_source(self) -> MetaVars:
        poetry_data = tomllib.loads(self._pyproject.read_text())["tool"]["poetry"]
        result: MetaVars = {
            "name": poetry_data["name"],
            "version": poetry_data["version"],
            "description": poetry_data["description"],
            "maintainer": next(
                iter((*poetry_data.get("maintainers", ()), *poetry_data["authors"]))
            ),
        }
        if homepage := poetry_data.get("homepage"):
            result["homepage"] = homepage
        return result
