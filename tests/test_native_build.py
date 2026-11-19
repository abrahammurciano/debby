"""Tests for building .deb files natively with the --build option."""

import shutil
import subprocess
import tarfile
from io import BytesIO
from pathlib import Path

import pytest

from debby.__main__ import main


def read_ar(path: Path) -> dict:
    """Read a Unix ar archive into a {name: bytes} mapping."""
    data = path.read_bytes()
    assert data.startswith(b"!<arch>\n"), "not an ar archive"
    members = {}
    offset = 8
    while offset < len(data):
        header = data[offset : offset + 60]
        name = header[0:16].decode().strip().rstrip("/")
        size = int(header[48:58].decode().strip())
        members[name] = data[offset + 60 : offset + 60 + size]
        offset += 60 + size + (size % 2)
    return members


@pytest.fixture
def deb(tmp_path: Path) -> Path:
    config = tmp_path / "config"
    config.write_text("hello\n")
    script = tmp_path / "postinst.sh"
    script.write_text("#!/bin/sh\ntrue\n")
    script.chmod(0o755)
    deb = tmp_path / "test.deb"
    main(
        [
            "-f",
            str(config),
            "etc/debby-test/config",
            "--name",
            "debby-test",
            "--version",
            "1.0",
            "--maintainer",
            "Test <test@example.com>",
            "--description",
            "Test package",
            "--postinst",
            str(script),
            "-b",
            str(deb),
        ]
    )
    return deb


def test_ar_structure(deb: Path) -> None:
    members = read_ar(deb)
    assert set(members) == {"debian-binary", "control.tar.gz", "data.tar.gz"}
    assert members["debian-binary"] == b"2.0\n"


def test_control_tar(deb: Path) -> None:
    control_tar = BytesIO(read_ar(deb)["control.tar.gz"])
    with tarfile.open(fileobj=control_tar, mode="r:gz") as tar:
        assert {"control", "postinst"} <= set(tar.getnames())
        assert tar.getmember("postinst").mode & 0o111, "scripts must be executable"


def test_data_tar_contains_directory_entries(deb: Path) -> None:
    """Regression test: dpkg cannot unpack files into directories that have
    no entry in data.tar and do not already exist on the target system."""
    data_tar = BytesIO(read_ar(deb)["data.tar.gz"])
    with tarfile.open(fileobj=data_tar, mode="r:gz") as tar:
        names = tar.getnames()
        assert tar.getmember("etc").isdir()
        assert tar.getmember("etc/debby-test").isdir()
    assert "etc/debby-test/config" in names


@pytest.mark.skipif(shutil.which("dpkg") is None, reason="dpkg not available")
def test_dpkg_installs_into_empty_root(deb: Path, tmp_path: Path) -> None:
    """End to end: the package must install onto a system where none of its
    directories exist yet."""
    root = tmp_path / "root"
    root.mkdir()
    result = subprocess.run(
        [
            "dpkg",
            f"--root={root}",
            "--force-not-root",
            "--force-script-chrootless",
            "-i",
            str(deb),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (root / "etc/debby-test/config").read_text() == "hello\n"
