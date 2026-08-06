"""RIG Deviate — push AI output past the generic median.

Public API
----------
* :func:`rig_deviate.deviate` — apply a single deviation engine to text.
* :func:`rig_deviate.score` — score an artifact's deviation from the LLM median.
* :data:`rig_deviate.ENGINES` — tuple of all 40 engines.
* :data:`rig_deviate.ENGINE_CODENAMES` — tuple of all 40 codenames.

Example
-------
>>> from rig_deviate import deviate, score
>>> result = deviate("Our product helps teams collaborate.", "GRAVITON", 10)
>>> report = score(result)
"""
from __future__ import annotations

from .engines import (
    ENGINE_BY_CODE,
    ENGINE_BY_ID,
    ENGINE_CODENAMES,
    ENGINES,
    LAYER_COGNITIVE,
    LAYER_NATURE,
    LAYER_PHYSICS,
    SIGMA_RUNGS,
    UnknownEngineError,
    deviate,
    deviate_all,
    engine_info,
)
from .score import (
    GENERIC_BASELINE,
    MAD_FLOOR,
    NORMALITY_CONSTANT,
    InsufficientBaselineError,
    extract_features,
    robust_mad_z,
    score,
    score_artifact,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "deviate",
    "deviate_all",
    "engine_info",
    "score",
    "score_artifact",
    "robust_mad_z",
    "extract_features",
    "ENGINES",
    "ENGINE_CODENAMES",
    "ENGINE_BY_CODE",
    "ENGINE_BY_ID",
    "LAYER_COGNITIVE",
    "LAYER_NATURE",
    "LAYER_PHYSICS",
    "SIGMA_RUNGS",
    "GENERIC_BASELINE",
    "MAD_FLOOR",
    "NORMALITY_CONSTANT",
    "UnknownEngineError",
    "InsufficientBaselineError",
]
