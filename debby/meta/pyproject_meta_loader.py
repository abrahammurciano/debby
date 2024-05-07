import tomllib
from pathlib import Path
from typing import Any, Iterable, Mapping, TypedDict

from .meta import MetaVars
from .meta_loader import MetaLoader


class PyprojectMetaLoader(MetaLoader):
    """Load python project metadata according to PEP621 from a pyproject.toml file."""

    @property
    def _pyproject(self) -> Path:
        assert self._args.pyproject is not None
        return self._args.pyproject

    def load_from_source(self) -> MetaVars:
        project_data = tomllib.loads(self._pyproject.read_text())["project"]
        result: MetaVars = {
            "name": project_data["name"],
        }
        if "version" not in project_data["dynamic"]:
            result["version"] = project_data["version"]
        if maintainer := self._get_maintainer(project_data):
            result["maintainer"] = maintainer
        if description := project_data.get("description"):
            result["description"] = description
        if homepage := self._get_homepage(project_data.get("urls", {})):
            result["homepage"] = homepage

        return result

    def _get_maintainer(self, project_data: Mapping[str, Any]) -> str | None:
        people: Iterable[_Person] = (
            project_data.get("maintainers") or project_data.get("authors") or ()
        )
        person = next(iter(people), None)
        if person is None:
            return None
        if person.get("name") and person.get("email"):
            return f"{person.get('name')} <{person.get('email')}>"
        if person.get("name"):
            return person.get("name")
        if person.get("email"):
            return person.get("email")
        return None

    def _get_homepage(self, urls: Mapping[str, str]) -> str | None:
        for key in ("Homepage", "Repository", "Documentation"):
            if url := urls.get(key):
                return url
        return next(iter(urls.values()), None)


class _Person(TypedDict, total=False):
    name: str
    email: str
