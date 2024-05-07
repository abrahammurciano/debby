# Debby

Create .deb files easily using python package metadata

## Installation

You can install this package with pip.
```sh
$ pip install debby
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/debby)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/debby.git)

[![PyPI - debby](https://img.shields.io/badge/PyPI-debby-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/debby/)

## Usage

This tool creates the directory structure (including the control file) to then create a .deb package with `dpkg-deb`.

You may provide a template for the control file (see [Control File Template](#control-file-template)) or provide the metadata directly via the command line or environment variables.

You may also provide files to include in the package with `-f/--file` option, which may be passed multiple times.

You may also provide a source for the metadata (see [Metadata Sources](#metadata-sources)). You can also specify specific metadata values via the command line. If no metadata source is provided, and all the required metadata is not provided via the command line, an error will be raised.

```sh
OUT_DIR=$(debby -f path/to/binary /usr/bin/binary -f path/to/config /etc/config --pyproject pyproject.toml)
dpkg-deb --build $OUT_DIR
```

### Metadata Sources

Currently, the following metadata sources are supported:

- `--pyproject`: Reads the metadata from the given pyproject.toml file, according to the [PEP 621](https://peps.python.org/pep-0621/) specification.
- `--poetry`: Reads the metadata from the given pyproject.toml file, according to [Poetry](https://python-poetry.org/docs/pyproject/)'s specification.

### Control File Template

It is possible to provide a template for the control file with `-t/--template path/to/control.template`. If provided, this template will be used to generate the control file instead of creating one from scratch. The template should be a text file with the following allowed placeholders.

| Placeholder | Description | Examples |
| --- | --- | --- |
| `{meta.name}` | The [name](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-package) of the package | `debby` |
| `{meta.source}` | The [source](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-source) of the package | `debby` |
| `{meta.version}` | The [version](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-version) of the package | `0.1.0` |
| `{meta.section}` | The [section](https://www.debian.org/doc/debian-policy/ch-archive.html#s-subsections) of the package | `misc`, `python` |
| `{meta.priority}` | The [priority](https://www.debian.org/doc/debian-policy/ch-archive.html#s-priorities) of the package | `optional` |
| `{meta.architecture}` | The [architecture](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-architecture) of the package | `all` |
| `{meta.eessential}` | The [essential](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-essential) status of the package | `yes`, `no` |
| `{meta.maintainer}` | The [maintainer](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-maintainer) of the package | `Abraham Murciano <abrahammurciano@gmail.com>` |
| `{meta.description}` | The [description](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-description) of the package | `Create .deb files easily using python package metadata` |
| `{meta.homepage}` | The [homepage](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-homepage) of the package | `https://abrahammurciano.github.io/debby/debby` |
| `{meta.depends}` | The [dependencies](https://www.debian.org/doc/debian-policy/ch-relationships.html) of the package | `python3`, `jq, pv (>= 1.0.0)` |
| `{meta.recommends}` | The [recommended packages](https://www.debian.org/doc/debian-policy/ch-relationships.html) of the package | `jq, pv (>= 1.0.0)` |
| `{meta.suggests}` | The [suggested packages](https://www.debian.org/doc/debian-policy/ch-relationships.html) of the package | `jq, pv (>= 1.0.0)` |
| `{meta.enhances}` | The [enhanced packages](https://www.debian.org/doc/debian-policy/ch-relationships.html) of the package | `jq, pv (>= 1.0.0)` |
| `{meta.breaks}` | The [packages that this package breaks](https://www.debian.org/doc/debian-policy/ch-relationships.html) | `jq, pv (>= 1.0.0)` |
| `{meta.conflicts}` | The [packages that this package conflicts with](https://www.debian.org/doc/debian-policy/ch-relationships.html) | `jq, pv (>= 1.0.0)` |
| `{files.total_size}` | The total size of all the files given with the `-f/--file` option | `123456` |