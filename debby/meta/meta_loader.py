from debby.args import Args
from debby.exceptions import MissingMetadataError

from .meta import Meta, MetaVars


class MetaLoader:
    """Load metadata from a source.

    Classes that inherit from this class should implement the `load_from_source` method. The value they return will be overridden by the values specified by the user in the command-line arguments, and the resulting metadata will be returned.

    Args:
        args: The command-line arguments.
    """

    def __init__(self, args: Args) -> None:
        self._args = args

    def load(self) -> Meta:
        """Load the metadata."""
        kwargs: MetaVars = {**self.load_from_source(), **self.overrides()}
        try:
            return Meta(**kwargs)
        except TypeError as e:
            raise MissingMetadataError(str(e)) from None

    def load_from_source(self) -> MetaVars:
        """Load the metadata from the source."""
        return {}

    def overrides(self) -> MetaVars:
        """Return metadata overrides as specified by the user."""
        result: MetaVars = {}
        if self._args.name:
            result["name"] = self._args.name
        if self._args.source:
            result["source"] = self._args.source
        if self._args.version:
            result["version"] = self._args.version
        if self._args.section:
            result["section"] = self._args.section
        if self._args.priority:
            result["priority"] = self._args.priority
        if self._args.architecture:
            result["architecture"] = self._args.architecture
        if self._args.essential:
            result["essential"] = self._args.essential
        if self._args.maintainer:
            result["maintainer"] = self._args.maintainer
        if self._args.description:
            result["description"] = self._args.description
        if self._args.homepage:
            result["homepage"] = self._args.homepage
        if self._args.depends:
            result["depends"] = self._args.depends
        if self._args.pre_depends:
            result["pre_depends"] = self._args.pre_depends
        if self._args.recommends:
            result["recommends"] = self._args.recommends
        if self._args.suggests:
            result["suggests"] = self._args.suggests
        if self._args.enhances:
            result["enhances"] = self._args.enhances
        if self._args.breaks:
            result["breaks"] = self._args.breaks
        if self._args.conflicts:
            result["conflicts"] = self._args.conflicts
        return result
