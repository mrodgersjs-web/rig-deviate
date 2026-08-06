"""test/test_engines.py — public API sanity tests."""
from __future__ import annotations

import numbers

import pytest

from rig_deviate import (
    ENGINE_CODENAMES,
    ENGINES,
    UnknownEngineError,
    deviate,
    score,
)
from rig_deviate.engines import LAYER_COGNITIVE, LAYER_NATURE, LAYER_PHYSICS


EXPECTED_ENGINES = 40


def test_all_engines_exist() -> None:
    assert len(ENGINES) == EXPECTED_ENGINES
    assert len(ENGINE_CODENAMES) == EXPECTED_ENGINES
    assert len(set(ENGINE_CODENAMES)) == EXPECTED_ENGINES


def test_layer_counts() -> None:
    layers = [e.layer for e in ENGINES]
    assert layers.count(LAYER_COGNITIVE) == 20
    assert layers.count(LAYER_NATURE) == 10
    assert layers.count(LAYER_PHYSICS) == 10


def test_deviate_returns_text() -> None:
    seed = "Our product helps teams collaborate."
    for code in ENGINE_CODENAMES:
        result = deviate(seed, code, 5)
        assert isinstance(result, str)
        assert len(result) >= len(seed) or result != seed or code.startswith("T")


def test_deviate_clamps_sigma() -> None:
    seed = "hello world"
    # Very large sigma is clamped; should still return text.
    result = deviate(seed, "GRAVITON", 1000)
    assert isinstance(result, str)


def test_deviate_unknown_engine_raises() -> None:
    with pytest.raises(UnknownEngineError):
        deviate("hello", "NOTANENGINE", 5)


def test_deviate_negative_sigma() -> None:
    seed = "We leverage best-in-class synergy to move the needle."
    result = deviate(seed, "GRAVITON", -10)
    assert isinstance(result, str)


def test_score_returns_number() -> None:
    report = score("We leverage best-in-class synergy to move the needle.")
    assert isinstance(report["rig_l"], numbers.Real)
    assert isinstance(report["rig_l_label"], str)
    assert isinstance(report["scores"], dict)
    assert len(report["scores"]) == EXPECTED_ENGINES
    for entry in report["scores"].values():
        assert isinstance(entry["madz"], numbers.Real)
        assert isinstance(entry["raw"], numbers.Real)


def test_score_subset() -> None:
    report = score("hello", engines=["GRAVITON", "FORGE"])
    assert set(report["scores"].keys()) == {"GRAVITON", "FORGE"}


def test_score_features_extracted() -> None:
    report = score("because mechanism A causes outcome B")
    assert "features" in report
    assert "mechanism_density" in report["features"]
    assert report["features"]["mechanism_density"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
