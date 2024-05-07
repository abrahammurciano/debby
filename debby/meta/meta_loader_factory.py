from debby.args import Args

from .meta_loader import MetaLoader
from .poetry_meta_loader import PoetryMetaLoader
from .pyproject_meta_loader import PyprojectMetaLoader


class MetaLoaderFactory:
    """Factory for creating an appropriate MetaLoader according to the given arguments.

    Args:
        args: The command-line arguments.
    """

    def __init__(self, args: Args) -> None:
        self._args = args

    def loader(self) -> MetaLoader:
        """Create the appropriate MetaLoader."""
        if self._args.pyproject:
            return PyprojectMetaLoader(self._args)
        if self._args.poetry:
            return PoetryMetaLoader(self._args)
        return MetaLoader(self._args)
