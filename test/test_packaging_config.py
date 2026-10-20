"""Tests that the packaging config in pyproject.toml stays complete.

Task this file addresses: pyproject.toml now declares the rig-deviate
console script, dev extras and the ruff and coverage tool config, and none
of that is checked by the library itself. These tests parse the file and
assert those declarations are present and point at code that exists, so the
config cannot silently drift.

Checked here:
- the rig-deviate console script points at rig_deviate.cli:main, which is
  importable and callable;
- dev extras declare pytest, pytest-cov and ruff;
- the ruff target matches the Python floor the package declares, and
  coverage is measured on the rig_deviate package.
"""

from __future__ import annotations

from pathlib import Path

import tomllib

import rig_deviate.cli as cli

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def _config() -> dict:
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def test_console_script_points_at_real_entry() -> None:
    entry = _config()["project"]["scripts"]["rig-deviate"]
    assert entry == "rig_deviate.cli:main"
    assert callable(cli.main)


def test_dev_extras_declare_the_test_toolchain() -> None:
    dev = _config()["project"]["optional-dependencies"]["dev"]
    names = {item.split(">=")[0].split("==")[0].strip() for item in dev}
    assert {"pytest", "pytest-cov", "ruff"} <= names


def test_tool_config_matches_the_python_floor() -> None:
    cfg = _config()
    assert cfg["project"]["requires-python"] == ">=3.10"
    assert cfg["tool"]["ruff"]["target-version"] == "py310"
    assert cfg["tool"]["coverage"]["run"]["source"] == ["rig_deviate"]
