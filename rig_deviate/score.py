"""rig_deviate.score — Robust-MAD-Z deviation scoring for artifacts.

The DES uses Robust-MAD-Z (median absolute deviation from the median) rather than
traditional z-scores because it is resistant to outliers in the baseline corpus and
does not assume a Gaussian distribution of generic artifacts.

    MAD = median(|x_i - median(x)|)
    Robust-MAD-Z = 0.6745 * (score - median(baseline)) / max(MAD, floor)

The 0.6745 constant restores a standard-normal scale at the median absolute deviation.
"""
from __future__ import annotations

import statistics
from typing import Any, Sequence

from .engines import ENGINE_BY_CODE, ENGINES, LAYER_COGNITIVE, LAYER_NATURE, Engine

# Φ⁻¹(0.75): restores standard-normal scale under MAD.
NORMALITY_CONSTANT = 0.6745

# Minimum MAD in the 0–100 score domain so generic baselines do not explode.
MAD_FLOOR = 5.0

# Default generic-median anchor used when no per-engine corpus is supplied.
GENERIC_BASELINE = (38.0, 44.0, 47.0, 50.0, 50.0, 52.0, 55.0, 58.0, 61.0, 64.0)


class InsufficientBaselineError(ValueError):
    """Raised when a baseline has fewer than two samples."""


def robust_mad_z(score: float, baseline: Sequence[float]) -> float:
    """Compute the Robust-MAD-Z of ``score`` against ``baseline``.

    Parameters
    ----------
    score : float
        The raw artifact score for a single engine.
    baseline : Sequence[float]
        Generic-median exemplar scores for that engine (at least two values).

    Returns
    -------
    float
        The σ rating of ``score`` relative to ``baseline``.

    Raises
    ------
    InsufficientBaselineError
        If ``baseline`` has fewer than two samples.
    """
    if len(baseline) < 2:
        raise InsufficientBaselineError("baseline must contain at least two values")
    baseline_median = statistics.median(baseline)
    raw_mad = statistics.median([abs(x - baseline_median) for x in baseline])
    mad = max(raw_mad, MAD_FLOOR)
    return round(NORMALITY_CONSTANT * (score - baseline_median) / mad, 3)


def _baseline_for(engine: Engine, baselines: dict[str, Sequence[float]] | None) -> Sequence[float]:
    """Resolve a baseline for an engine, falling back to the generic anchor."""
    if baselines and engine.codename in baselines:
        return baselines[engine.codename]
    return GENERIC_BASELINE


def extract_features(text: str) -> dict[str, float]:
    """Deterministic 0–100 feature extraction from raw text.

    This is a lightweight, rule-based proxy. It measures lexical properties that
correlate with generic-LLM output (cliché density, hedging, mechanistic language,
absolutes, evidence markers, sentence length, etc.). It is honest, reproducible,
and requires no external model.
    """
    text_l = text.lower()
    words = text.split()
    n_words = max(len(words), 1)
    n_sentences = max(len([s for s in text.split(".") if s.strip()]), 1)

    clichés = (
        "leverage", "synergy", "holistic", "actionable", "bandwidth", "deep dive",
        "move the needle", "best practice", "paradigm shift", "double-click",
        "circle back", "low-hanging fruit", "game changer", "thinking outside the box",
        "unpack", "lean in", "value-add", "boil the ocean",
    )
    hedges = (
        "might", "perhaps", "generally", "typically", "often", "could", "may", "tends to",
        "in many cases", "arguably", "somewhat", "fairly", "probably", "likely",
    )
    evidence = ("[source", "http", "data", "study", "measured", "observed", "n=", "because")
    absolutes = ("always", "never", "perfect", "zero", "impossible", "guaranteed")
    mechanisms = ("because", "therefore", "causes", "pathway", "mechanism", "via")

    def _density(terms: tuple[str, ...]) -> float:
        hits = sum(text_l.count(t) for t in terms)
        return max(0.0, min(100.0, (hits / n_words) * 100.0))

    return {
        "cliche_density": _density(clichés),
        "hedge_density": _density(hedges),
        "evidence_density": _density(evidence),
        "absolute_density": _density(absolutes),
        "mechanism_density": _density(mechanisms),
        "avg_sentence_length": min(100.0, n_words / n_sentences * 2),
        "specificity": min(100.0, len(set(words)) / max(n_words, 1) * 200),
    }


def _engine_raw_score(features: dict[str, float], engine: Engine) -> float:
    """Map extracted features to a 0–100 raw score for a given engine.

    The mapping is heuristic but deterministic. Positive features for an engine
raise the raw score; negative features lower it.
    """
    f = features

    # Cognitive engines: reward evidence/mechanism/specificity, penalize clichés/hedges.
    if engine.layer == LAYER_COGNITIVE:
        base = 50.0
        base += f["evidence_density"] * 0.4
        base += f["mechanism_density"] * 0.4
        base += f["specificity"] * 0.2
        base -= f["cliche_density"] * 0.5
        base -= f["hedge_density"] * 0.3
        if engine.codename in ("ANCHOR", "WITNESS", "BAYES"):
            base += f["evidence_density"] * 0.3
        if engine.codename == "FORGE":
            base += f["mechanism_density"] * 0.4
        if engine.codename in ("GLYPH", "ECHO"):
            base += f["specificity"] * 0.3
        return max(0.0, min(100.0, base))

    # Nature engines: reward specificity and low cliché/hedge density.
    if engine.layer == LAYER_NATURE:
        base = 50.0
        base += f["specificity"] * 0.3
        base -= f["cliche_density"] * 0.4
        base -= f["hedge_density"] * 0.3
        return max(0.0, min(100.0, base))

    # Physics engines are hard gates; raw score is a structural signal, not a soft rating.
    base = 50.0
    base += f["evidence_density"] * 0.3
    base -= f["absolute_density"] * 0.5
    return max(0.0, min(100.0, base))


def score_artifact(
    text: str,
    *,
    baselines: dict[str, Sequence[float]] | None = None,
    engines: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Score an artifact against the deviation engines.

    Parameters
    ----------
    text : str
        The artifact to score.
    baselines : dict[str, Sequence[float]], optional
        Per-engine baseline corpora. Engines not present use the generic anchor.
    engines : Sequence[str], optional
        Subset of engine codenames to score. Defaults to all 40.

    Returns
    -------
    dict[str, Any]
        A result packet with ``scores`` (per-engine MAD-Z), ``rig_l`` (composite),
        ``label``, and ``features``.
    """
    features = extract_features(text)
    target_engines = [ENGINE_BY_CODE[c.upper()] for c in engines] if engines else list(ENGINES)

    scores: dict[str, dict[str, Any]] = {}
    layer_sigmas: dict[str, list[float]] = {LAYER_COGNITIVE: [], LAYER_NATURE: []}
    weakest: tuple[float, str] | None = None

    for eng in target_engines:
        raw = _engine_raw_score(features, eng)
        baseline = _baseline_for(eng, baselines)
        sigma = robust_mad_z(raw, baseline)
        scores[eng.codename] = {
            "raw": raw,
            "madz": sigma,
            "layer": eng.layer,
        }
        if eng.layer in layer_sigmas:
            layer_sigmas[eng.layer].append(abs(sigma))
            if weakest is None or abs(sigma) < weakest[0]:
                weakest = (abs(sigma), eng.codename)

    # Composite RIG-L: mean of top-6 |σ| pulls across soft layers, risk-penalized.
    all_soft = sorted(layer_sigmas[LAYER_COGNITIVE] + layer_sigmas[LAYER_NATURE], reverse=True)
    top6 = all_soft[:6]
    rig_l = round(sum(top6) / len(top6), 2) if top6 else 0.0
    # Risk penalty: many weak engines drag the composite down.
    if all_soft:
        weak_ratio = sum(1 for s in all_soft if s < 3.0) / len(all_soft)
        rig_l = round(rig_l * (1 - 0.5 * weak_ratio), 2)

    label = "block"
    if rig_l >= 20.0:
        label = "doctrine_artifact"
    elif rig_l >= 10.0:
        label = "promote"
    elif rig_l >= 5.0:
        label = "review"
    elif rig_l >= 3.0:
        label = "marginal"

    return {
        "text": text,
        "features": features,
        "scores": scores,
        "rig_l": rig_l,
        "rig_l_label": label,
        "weakest_gate": weakest[1] if weakest else None,
    }


def score(text: str, **kwargs: Any) -> dict[str, Any]:
    """Alias for :func:`score_artifact`."""
    return score_artifact(text, **kwargs)


__all__ = [
    "NORMALITY_CONSTANT",
    "MAD_FLOOR",
    "GENERIC_BASELINE",
    "InsufficientBaselineError",
    "robust_mad_z",
    "extract_features",
    "score_artifact",
    "score",
]
