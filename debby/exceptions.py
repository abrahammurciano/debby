class DebbyError(Exception):
    """Base class for all Debby exceptions."""


class MissingMetadataError(DebbyError):
    """Raised when required metadata is missing."""

    def __str__(self) -> str:
        return f"Missing some required metadata. Make sure it's present in any of the sources, or provide it as a command-line argument or environment variable. {super().__str__()}"
