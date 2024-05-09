import os
from argparse import ArgumentParser
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Literal, Optional, Sequence, Tuple, Union

from typing_extensions import Self


@dataclass
class Args:
    files: Sequence[Tuple[Path, Path]]
    template: Optional[Path]
    out_dir: Path
    preinst: Optional[Path]
    preinst_cmd: Sequence[str]
    postinst: Optional[Path]
    postinst_cmd: Sequence[str]
    prerm: Optional[Path]
    prerm_cmd: Sequence[str]
    postrm: Optional[Path]
    postrm_cmd: Sequence[str]
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
            help="Path to the files/directories to package. Can be passed multiple times. E.g. --file SOURCE1 DESTINATION1 --file SOURCE2 DESTINATION2. Sources must point to existing files or directories and destinations will be treated as relative to the package root. You may also choose to not use this flag and copy the files manually to the output directory.",
            type=Path,
            nargs=2,
            action="append",
            default=[],
            metavar=("SOURCE", "DESTINATION"),
        )
        parser.add_argument(
            "-t",
            "--template",
            help="Path to a control file template to use instead of generating one from scratch. This file may contain placeholders such as {meta.name} and {meta.version}. See the documentation for more information. https://abrahammurciano.github.io/debby",
            type=Path,
        )
        parser.add_argument(
            "-o",
            "--out-dir",
            help="Path to the output directory. Defaults to the current working directory.",
            type=Path,
            default=".",
        )
        parser.add_argument(
            "--no-size",
            help="Do not include the total size of the package in the control file.",
            action="store_true",
        )
        cls._add_script_args(parser)
        cls._add_meta_source_args(parser)
        cls._add_meta_override_args(parser)
        parser.add_argument(
            "-V",
            action="version",
            help="Print the version and exit.",
            version=metadata.version((__package__ or "debby").split(".", 1)[0]),
        )
        return cls(**vars(parser.parse_args(argv)))

    @classmethod
    def _add_script_args(cls, parser: ArgumentParser) -> None:
        from debby.scripts.script_stage import ScriptStage

        script_group = parser.add_argument_group(
            "Scripts",
            "Specify scripts to run at different stages of the package's lifecycle.",
        )
        for script_stage in ScriptStage:
            group = script_group.add_mutually_exclusive_group()
            group.add_argument(
                f"--{script_stage.name}",
                help=f"Include ./{script_stage.name} as the {script_stage.descriptive_name} script, or the given file if one is specified.",
                type=Path,
                nargs="?",
                const=script_stage.name,
            )
            group.add_argument(
                f"--{script_stage.name}-cmd",
                help=f"Run the given command during the {script_stage.descriptive_name} stage. May be passed multiple times and they will all be run in order.",
                action="append",
                default=[],
                metavar="COMMAND",
            )

    @classmethod
    def _add_meta_source_args(cls, parser: ArgumentParser) -> None:
        meta_source_group = parser.add_mutually_exclusive_group()
        meta_source_group.add_argument(
            "--pyproject",
            help="Read metadata according to PEP 621 from ./pyproject.toml, or the given file if specified.",
            type=Path,
            metavar="PYPROJECT_FILE",
            nargs="?",
            const="pyproject.toml",
        )
        meta_source_group.add_argument(
            "--poetry",
            help="Read poetry metadata from the ./pyproject.toml file, or the given file if specified.",
            type=Path,
            metavar="PYPROJECT_FILE",
            nargs="?",
            const="pyproject.toml",
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
            help="Specify the package name.",
            default=os.environ.get("DEBBY_META_NAME"),
        )
        meta_overrides_group.add_argument(
            "-s",
            "--source",
            help="Specify the package source.",
            default=os.environ.get("DEBBY_META_SOURCE"),
        )
        meta_overrides_group.add_argument(
            "-v",
            "--version",
            help="Specify the package version.",
            default=os.environ.get("DEBBY_META_VERSION"),
        )
        meta_overrides_group.add_argument(
            "--section",
            help="Specify the package section. For example, 'misc' or 'python'.",
            default=os.environ.get("DEBBY_META_SECTION"),
        )
        meta_overrides_group.add_argument(
            "-p",
            "--priority",
            help="Specify the package priority. Usually 'optional'.",
            default=os.environ.get("DEBBY_META_PRIORITY"),
        )
        meta_overrides_group.add_argument(
            "-a",
            "--architecture",
            help="Specify the package architecture. Defaults to 'all'.",
            default=os.environ.get("DEBBY_META_ARCHITECTURE", "all"),
        )
        meta_overrides_group.add_argument(
            "-e",
            "--essential",
            choices=["yes", "no"],
            help="Specify whether the package is essential.",
            default=os.environ.get("DEBBY_META_ESSENTIAL"),
        )
        meta_overrides_group.add_argument(
            "-m",
            "--maintainer",
            help="Specify the package maintainer. For example, 'John Doe <john.doe@example.com>'.",
            default=os.environ.get("DEBBY_META_MAINTAINER"),
        )
        meta_overrides_group.add_argument(
            "-d",
            "--description",
            help="Specify the package description.",
            default=os.environ.get("DEBBY_META_DESCRIPTION"),
        )
        meta_overrides_group.add_argument(
            "--homepage",
            help="Specify the package homepage.",
            default=os.environ.get("DEBBY_META_HOMEPAGE"),
        )
        cls._add_dependencies_args(meta_overrides_group)

    @classmethod
    def _add_dependencies_args(cls, parser: Union[ArgumentParser, Any]) -> None:
        parser.add_argument_group("Dependencies", "Specify package dependencies")
        parser.add_argument(
            "--depends",
            help="Specify packages that your package depends on. For example, 'python3, python3-requests (>= 2.24)'.",
            default=os.environ.get("DEBBY_META_DEPENDS"),
        )
        parser.add_argument(
            "--pre-depends",
            help="Specify packages that must be installed before your package is installed.",
            default=os.environ.get("DEBBY_META_PRE_DEPENDS"),
        )
        parser.add_argument(
            "--recommends",
            help="Specify packages that are recommended but not strictly required for your package.",
            default=os.environ.get("DEBBY_META_RECOMMENDS"),
        )
        parser.add_argument(
            "--suggests",
            help="Specify packages that are suggested but not required for your package.",
            default=os.environ.get("DEBBY_META_SUGGESTS"),
        )
        parser.add_argument(
            "--enhances",
            help="Specify packages that your package enhances.",
            default=os.environ.get("DEBBY_META_ENHANCES"),
        )
        parser.add_argument(
            "--breaks",
            help="Specify packages that your package breaks.",
            default=os.environ.get("DEBBY_META_BREAKS"),
        )
        parser.add_argument(
            "--conflicts",
            help="Specify packages that your package conflicts with.",
            default=os.environ.get("DEBBY_META_CONFLICTS"),
        )
