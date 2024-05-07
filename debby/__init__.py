"""
.. include:: ../README.md
"""

import importlib.metadata as metadata

__version__ = metadata.version(__package__ or __name__)

from .control_file import ControlFile
from .files import Files
from .meta import Meta
from .package import Package

__all__ = ("Package", "ControlFile", "Files", "Meta")
