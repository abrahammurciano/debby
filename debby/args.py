import os
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Optional, Sequence, Tuple, Union

from typing_extensions import Self


@dataclass
class Args:
    files: Sequence[Tuple[Path, Path]]
    template: Optional[Path]
    out_dir: Path
    pyproject: Optional[Path]
    poetry: Optional[Path]
    name: Optional[str]
    source: Optional[str]
    version: Optional[str]
    section: Optional[str]
    priority: Optional[str]
    architecture: Optional[str]
    essential: Optional[Literal["yes", "no"]]
    maintainer: Optional[str]
    description: Optional[str]
    homepage: Optional[str]
    depends: Optional[str]
    pre_depends: Optional[str]
    recommends: Optional[str]
    suggests: Optional[str]
    enhances: Optional[str]
    breaks: Optional[str]
    conflicts: Optional[str]
    no_size: bool = False

    @classmethod
    def parse(cls, argv: Optional[Sequence[str]] = None) -> Self:
        parser = ArgumentParser()
        parser.add_argument(
            "-f",
            "--file",
            dest="files",
            help="Path to the files to package. Can be passed multiple times. E.g. --file SOURCE1 DESTINATION1 --file SOURCE2 DESTINATION2. Sources must point to existing files or directories and destinations will be treated as relative to the package root.",
            type=Path,
            nargs=2,
            action="append",
            default=[],
        )
        parser.add_argument(
            "-t",
            "--template",
            help="Path to the control file template",
            type=Path,
        )
        parser.add_argument(
            "-o",
            "--out-dir",
            help="Path to the output directory",
            type=Path,
            default=Path("debian/build"),
        )
        parser.add_argument(
            "--no-size",
            help="Do not include the total size of the package in the control file",
            action="store_true",
        )
        cls._add_meta_source_group(parser)
        cls._add_meta_override_args(parser)
        return cls(**vars(parser.parse_args(argv)))

    @classmethod
    def _add_meta_source_group(cls, parser: ArgumentParser) -> None:
        meta_source_group = parser.add_mutually_exclusive_group(required=True)
        meta_source_group.add_argument(
            "--pyproject",
            help="Read metadata according to PEP 621 from the given pyproject.toml file",
            type=Path,
            metavar="pyproject.toml",
        )
        meta_source_group.add_argument(
            "--poetry",
            help="Read poetry metadata from the given pyproject.toml file",
            type=Path,
            metavar="pyproject.toml",
        )

    @classmethod
    def _add_meta_override_args(cls, parser: ArgumentParser) -> None:
        meta_overrides_group = parser.add_argument_group(
            "Metadata Overrides",
            "Override metadata fields. Environment variables such as DEBBY_META_VERSION can be used to set these fields.",
        )
        meta_overrides_group.add_argument(
            "-n",
            "--name",
            help="Specify the package name",
            default=os.environ.get("DEBBY_META_NAME"),
        )
        meta_overrides_group.add_argument(
            "-s",
            "--source",
            help="Specify the package source",
            default=os.environ.get("DEBBY_META_SOURCE"),
        )
        meta_overrides_group.add_argument(
            "-v",
            "--version",
            help="Specify the package version",
            default=os.environ.get("DEBBY_META_VERSION"),
        )
        meta_overrides_group.add_argument(
            "--section",
            help="Specify the package section",
            default=os.environ.get("DEBBY_META_SECTION"),
        )
        meta_overrides_group.add_argument(
            "-p",
            "--priority",
            help="Specify the package priority",
            default=os.environ.get("DEBBY_META_PRIORITY"),
        )
        meta_overrides_group.add_argument(
            "-a",
            "--architecture",
            help="Specify the package architecture",
            default=os.environ.get("DEBBY_META_ARCHITECTURE"),
        )
        meta_overrides_group.add_argument(
            "-e",
            "--essential",
            choices=["yes", "no"],
            help="Specify whether the package is essential",
            default=os.environ.get("DEBBY_META_ESSENTIAL"),
        )
        meta_overrides_group.add_argument(
            "-m",
            "--maintainer",
            help="Specify the package maintainer",
            default=os.environ.get("DEBBY_META_MAINTAINER"),
        )
        meta_overrides_group.add_argument(
            "-d",
            "--description",
            help="Specify the package description",
            default=os.environ.get("DEBBY_META_DESCRIPTION"),
        )
        meta_overrides_group.add_argument(
            "--homepage",
            help="Specify the package homepage",
            default=os.environ.get("DEBBY_META_HOMEPAGE"),
        )
        cls._add_dependencies_args(meta_overrides_group)

    @classmethod
    def _add_dependencies_args(cls, parser: Union[ArgumentParser, Any]) -> None:
        parser.add_argument_group("Dependencies", "Specify package dependencies")
        parser.add_argument(
            "--depends",
            help="Specify package dependencies",
            default=os.environ.get("DEBBY_META_DEPENDS"),
        )
        parser.add_argument(
            "--pre-depends",
            help="Specify package pre-dependencies",
            default=os.environ.get("DEBBY_META_PRE_DEPENDS"),
        )
        parser.add_argument(
            "--recommends",
            help="Specify package recommendations",
            default=os.environ.get("DEBBY_META_RECOMMENDS"),
        )
        parser.add_argument(
            "--suggests",
            help="Specify package suggestions",
            default=os.environ.get("DEBBY_META_SUGGESTS"),
        )
        parser.add_argument(
            "--enhances",
            help="Specify package enhancements",
            default=os.environ.get("DEBBY_META_ENHANCES"),
        )
        parser.add_argument(
            "--breaks",
            help="Specify package breaks",
            default=os.environ.get("DEBBY_META_BREAKS"),
        )
        parser.add_argument(
            "--conflicts",
            help="Specify package conflicts",
            default=os.environ.get("DEBBY_META_CONFLICTS"),
        )
