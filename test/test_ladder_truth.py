"""Regression tests keeping the documented ladder honest."""

from __future__ import annotations


def test_ladder_has_thirteen_rungs() -> None:
    from rig_deviate.engines import SIGMA_RUNGS

    assert len(SIGMA_RUNGS) == 13


def test_module_header_matches_code() -> None:
    import rig_deviate.engines as engines

    source = open(engines.__file__, encoding="utf-8").read()
    assert "14-rung" not in source
    assert "13" in source.split("SIGMA_RUNGS")[0]
