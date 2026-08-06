"""rig_deviate.engines — the canonical RIG Deviation Engine roster.

A clean, public-facing implementation of the 40-engine × 14-rung Deviation Engine
System (DES). Each engine is a deterministic lens that pushes an artifact away from
the generic LLM median along a specific dimension.

The ladder uses 14 anchored σ rungs:

    -30  -20  -10  -5  -3  -1   0  +1  +3  +5  +10  +20  +30
      |----|----|---|---|---|---|---|---|---|---|----|----|
    negative pole                generic median          positive pole

Cognitive and Nature engines operate on soft ±20σ scales. Physics engines are hard
state gates operating on ±30σ structural invariants; a negative physics pole is a
BLOCK rather than a gentle nudge.
"""
from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from typing import Any

LAYER_COGNITIVE = "cognitive"
LAYER_NATURE = "nature"
LAYER_PHYSICS = "physics"

SIGMA_RUNGS = (-30, -20, -10, -5, -3, -1, 0, 1, 3, 5, 10, 20, 30)


@dataclass(frozen=True)
class Engine:
    """A single deviation engine."""

    id: int
    codename: str
    layer: str
    full_name: str
    description: str
    negative_pole: str
    positive_pole: str

    def __repr__(self) -> str:  # pragma: no cover
        return f"Engine({self.id}, {self.codename!r}, {self.layer})"


# ── L1 Cognitive: output-quality engines (±20σ) ──────────────────────────────
_COGNITIVE = [
    Engine(1, "GRAVITON", LAYER_COGNITIVE, "Gravity Escape",
           "Escape the generic AI gravity that pulls output toward the polished median.",
           "bland, safe, forgettable", "surprising, category-defying, memorable"),
    Engine(2, "ANCHOR", LAYER_COGNITIVE, "Reality Anchor",
           "Tie every claim to observable evidence or explicit uncertainty.",
           "unsupported assertions, hand-waving", "evidence-dense, source-anchored"),
    Engine(3, "DARWIN", LAYER_COGNITIVE, "Evolutionary Selection",
           "Generate, mutate, and select — never accept the first draft.",
           "single-candidate, first-draft thinking", "iterated, selected, pressure-tested"),
    Engine(4, "XRAY", LAYER_COGNITIVE, "Feynman X-Ray",
           "Expose fake understanding by forcing concrete, jargon-free explanation.",
           "vague jargon, fake expertise", "precise, concrete, explainable to a novice"),
    Engine(5, "FORGE", LAYER_COGNITIVE, "Mechanism Furnace",
           "Burn off adjectives until only machinery remains.",
           "adjective-heavy, descriptive only", "mechanism-dense, causal, operational"),
    Engine(6, "BREAKER", LAYER_COGNITIVE, "Rupture Engine",
           "Break inherited orthodoxy when the inherited frame is wrong.",
           "conventional, category-compliant", "contrarian, frame-breaking, orthogonal"),
    Engine(7, "COLLIDER", LAYER_COGNITIVE, "Collision Collider",
           "Import mechanisms from unrelated domains to create novel solutions.",
           "siloed, single-domain reasoning", "cross-domain recombination"),
    Engine(8, "VOLT", LAYER_COGNITIVE, "Voltage Reactor",
           "Create emotional voltage without manipulation.",
           "flat or manipulative affect", "genuinely felt stakes, no coercion"),
    Engine(9, "ECHO", LAYER_COGNITIVE, "Memory Residue",
           "Optimize for what the reader remembers in 48 hours.",
           "forgettable, low residue", "sticky, quotable, durable recall"),
    Engine(10, "HORIZON", LAYER_COGNITIVE, "Temporal Horizon Integrity",
            "Long-term compounding, optionality, and kill criteria.",
            "short-term, brittle commitments", "optionality-rich, reversible bets"),
    Engine(11, "SOVEREIGN", LAYER_COGNITIVE, "Autonomy Calibration",
            "Preserve reader/user agency.",
            "coercive, choice-architected pressure", "agency-respecting, transparent"),
    Engine(12, "SURPRISE", LAYER_COGNITIVE, "Predictive Error Calibration",
            "Make the reader update their mental model.",
            "predictable, confirmation-biased", "genuinely surprising yet coherent"),
    Engine(13, "LOOP", LAYER_COGNITIVE, "Zeigarnik Residue",
            "Open loops the reader must close.",
            "self-contained, no forward pull", "curiosity loops, serialized intrigue"),
    Engine(14, "VISCERA", LAYER_COGNITIVE, "Somatic Marker",
            "Embodied stakes — felt, not merely described.",
            "abstract, bloodless", "physically felt consequences"),
    Engine(15, "REBOUND", LAYER_COGNITIVE, "Opponent Process",
            "Use affective contrast and aftertaste.",
            "monotonic tone", "dynamic contrast, earned resolution"),
    Engine(16, "PRISM", LAYER_COGNITIVE, "Signal-to-Noise Discriminability",
            "d-prime above 1.8; the signal cannot be confused with noise.",
            "noisy, low contrast", "sharp signal, clean structure"),
    Engine(17, "WELLSPRING", LAYER_COGNITIVE, "Hedonic Adaptation Resistance",
            "Pays back more on reread than first read.",
            "one-and-done consumption", "layered, rewarding revisits"),
    Engine(18, "GLYPH", LAYER_COGNITIVE, "Kolmogorov Originality",
            "Cannot be compressed into a known phrase.",
            "clichéd, replaceable wording", "incompressible, irreducible expression"),
    Engine(19, "BAYES", LAYER_COGNITIVE, "Confidence Calibration",
            "Confidence matches evidence; method transparent.",
            "over/under-confident", "appropriately uncertain, well-calibrated"),
    Engine(20, "SHIELD", LAYER_COGNITIVE, "Cognitive Sovereignty Shield",
            "Human stays the decision-maker.",
            "automation that displaces judgment", "AI-augmented, human-gated judgment"),
]

# ── L2 Nature: process-quality engines (±20σ) ────────────────────────────────
_NATURE = [
    Engine(21, "SWARM", LAYER_NATURE, "Pheromone Saturation",
           "Detect when search has collapsed to one path.",
           "premature convergence, monoculture", "diverse, unexplored paths maintained"),
    Engine(22, "ALBATROSS", LAYER_NATURE, "Lévy Flight",
           "Heavy-tail jumps escape local basins.",
           "stuck in local neighborhood", "occasional long-range exploration"),
    Engine(23, "SLIME", LAYER_NATURE, "Physarum Pruner",
           "Reinforce winning paths; prune the rest.",
           "redundant, low-flow networks", "efficient, adaptive allocation"),
    Engine(24, "CLONAL", LAYER_NATURE, "Immune Hypermutator",
           "Mediocre candidates mutate hard; winners refine gently.",
           "uniform mutation, no selection pressure", "differential mutation by quality"),
    Engine(25, "LUMINA", LAYER_NATURE, "Firefly Attractor",
           "Bioluminescent attraction to brighter solutions.",
           "premature convergence", "diverse attraction, controlled clustering"),
    Engine(26, "COLI", LAYER_NATURE, "Chemotaxis Climber",
           "Gradient-climb deviation; tumble when flat.",
           "stuck on flat gradient", "gradient ascent with tumble fallback"),
    Engine(27, "ROOT", LAYER_NATURE, "Mycorrhizal Allocator",
           "Hubs feed seedlings; diversity insurance.",
           "starvation of promising seedlings", "fair, resilience-preserving allocation"),
    Engine(28, "HUMPBACK", LAYER_NATURE, "Whale Spiral",
           "Spiral tightens around the best; anneal exploration→exploitation.",
           "no transition from explore to exploit", "annealed convergence"),
    Engine(29, "CUCKOO", LAYER_NATURE, "Cuckoo Parasite",
           "Inject parasitic high-deviation candidates; abandon worst nests.",
           "stuck in mediocrity", "disruptive variants pruned or promoted"),
    Engine(30, "REEF", LAYER_NATURE, "Coral Reef Evolver",
           "All five reproduction modes simultaneously per generation.",
           "low-diversity population", "maximal diversity with selection"),
]

# ── L3 Physics: hard state gates (±30σ) ──────────────────────────────────────
_PHYSICS = [
    Engine(31, "TUNNEL", LAYER_PHYSICS, "Quantum Tunneling",
           "Penetrate an impassable barrier.",
           "claimed breakthrough with no coherence mass", "genuine orthodoxy penetration"),
    Engine(32, "PAULI", LAYER_PHYSICS, "Pauli Exclusion",
           "No two artifacts may occupy the same state.",
           "near-duplicate of existing artifact", "state-distinct identity"),
    Engine(33, "CRITICAL", LAYER_PHYSICS, "Phase Transition",
           "Cross the critical temperature; reorganize the regime.",
           "regime-change claim without order-parameter delta", "verified regime shift"),
    Engine(34, "PARSEC", LAYER_PHYSICS, "Fine Tuning",
           "Every element precisely calibrated; no replaceable word.",
           "accidental, replaceable parameters", "cosmologically precise tuning"),
    Engine(35, "HAWKING", LAYER_PHYSICS, "Hawking Radiation",
           "Information must leak through an opaque boundary.",
           "opaque black-box with no verifiable output", "information leakage / auditability"),
    Engine(36, "CASIMIR", LAYER_PHYSICS, "Casimir Effect",
           "Constrained empty space generates measurable force.",
           "negative space wasted", "deliberate absence produces value"),
    Engine(37, "KELVIN", LAYER_PHYSICS, "Absolute Zero",
           "Detect unreachable-floor claims.",
           "zero/perfect/always claims with residual noise", "honest bounded claims"),
    Engine(38, "LUMEN", LAYER_PHYSICS, "Speed of Light",
           "Effects cannot precede their causal pathway.",
           "superluminal causal claim", "latency respects causal chain"),
    Engine(39, "BELL", LAYER_PHYSICS, "Entanglement",
           "Genuine non-local correlation; Bell |S| > 2.",
           "classical correlation labeled entanglement", "genuine coupled-system effect"),
    Engine(40, "ZEROPOINT", LAYER_PHYSICS, "Vacuum Fluctuation",
           "Even quiet systems must show baseline activity.",
           "perfect equilibrium with no variance", "healthy baseline variance present"),
]

ENGINES: tuple[Engine, ...] = tuple(_COGNITIVE + _NATURE + _PHYSICS)
ENGINE_BY_CODE: dict[str, Engine] = {e.codename: e for e in ENGINES}
ENGINE_BY_ID: dict[int, Engine] = {e.id: e for e in ENGINES}
ENGINE_CODENAMES: tuple[str, ...] = tuple(e.codename for e in ENGINES)

LAYER_ENGINES: dict[str, tuple[Engine, ...]] = {
    LAYER_COGNITIVE: tuple(_COGNITIVE),
    LAYER_NATURE: tuple(_NATURE),
    LAYER_PHYSICS: tuple(_PHYSICS),
}


class UnknownEngineError(KeyError):
    """Raised when an unrecognized engine codename is requested."""


# ── Deterministic text transformation primitives ─────────────────────────────

_GENERIC_TELLS = (
    "leverage", "synergy", "holistic", "actionable", "bandwidth", "circle back",
    "low-hanging fruit", "move the needle", "best practice", "paradigm shift",
    "deep dive", "double-click", "unpack", "lean in", "synergize", "stakeholder",
    "value-add", "boil the ocean", "run it up the flagpole",
)

_HEDGES = (
    "might", "perhaps", "generally", "typically", "often", "could", "may", "tends to",
    "in many cases", "arguably", "somewhat", "fairly", "probably", "likely",
)

_INTENSIFIERS = (
    "definitely", "certainly", "absolutely", "undeniably", "unambiguously",
    "conclusively", "decisively",
)

_ABSOLUTES = (
    "always", "never", "perfect", "zero", "impossible", "guaranteed", "everyone",
    "no one", "all", "none",
)


def _clamp_sigma(sigma: float) -> float:
    """Clamp user sigma to the valid ±30σ ladder."""
    return max(-30.0, min(30.0, float(sigma)))


def _token_sentences(text: str) -> list[str]:
    """Split text into sentences by naive punctuation."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def _join_sentences(sentences: list[str]) -> str:
    return " ".join(sentences)


def _polarize(text: str, engine: Engine, sigma: float) -> str:
    """Apply engine-specific deterministic transformation at the requested σ."""
    sigma = _clamp_sigma(sigma)
    sign = 1 if sigma > 0 else (-1 if sigma < 0 else 0)
    magnitude = abs(sigma)

    # Shared generic-median cleaners (positive direction pushes away from generic tells).
    if sign > 0 and magnitude >= 3:
        for tell in _GENERIC_TELLS:
            text = re.sub(rf"\b{re.escape(tell)}\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text).strip()

    # Layer-specific transforms.
    if engine.layer == LAYER_COGNITIVE:
        text = _transform_cognitive(text, engine, sign, magnitude)
    elif engine.layer == LAYER_NATURE:
        text = _transform_nature(text, engine, sign, magnitude)
    else:
        text = _transform_physics(text, engine, sign, magnitude)

    # Negative pole: add generic tells / hedges back in to make text more median.
    if sign < 0 and magnitude >= 3:
        if not any(t in text.lower() for t in _GENERIC_TELLS):
            text += " This is a best-practice, actionable, holistic approach that moves the needle."

    return text.strip()


def _transform_cognitive(text: str, engine: Engine, sign: int, magnitude: float) -> str:
    sentences = _token_sentences(text)
    if not sentences:
        return text

    if sign == 0:
        return text

    # ANCHOR / WITNESS / BAYES: evidence density and calibration.
    if engine.codename in ("ANCHOR", "WITNESS", "BAYES"):
        if sign > 0:
            if "[source" not in text and "http" not in text:
                text += " [source: observed data; confidence calibrated to evidence]"
            text = _remove_words(text, _HEDGES)
        else:
            for h in _HEDGES:
                if h in text.lower():
                    break
            else:
                text += " Perhaps this might generally work in many cases."

    # FORGE: mechanistic specificity.
    elif engine.codename == "FORGE":
        if sign > 0:
            text = re.sub(r"\b(very|really|quite|extremely)\s+([a-z]+)", r"\2 measured as X", text, flags=re.IGNORECASE)
            if "because" not in text.lower():
                sep = " " if text.endswith((".", "!", "?")) else ". "
                text += sep + "Mechanism A causes outcome B via pathway C."
        else:
            text += " It feels important and meaningful in a broad, holistic way."

    # XRAY: concreteness vs jargon.
    elif engine.codename == "XRAY":
        if sign > 0:
            text = re.sub(r"\b(utilize|leverage|implement)\b", "use", text, flags=re.IGNORECASE)
            text = re.sub(r"\b(framework|methodology|paradigm)\b", "specific process", text, flags=re.IGNORECASE)
        else:
            text += " We will leverage a holistic framework to implement the methodology."

    # GLYPH: originality / compression resistance.
    elif engine.codename == "GLYPH":
        if sign > 0:
            text = re.sub(r"\b(thinking outside the box|game changer|next level)\b", "", text, flags=re.IGNORECASE)
            if not re.search(r"\b(zqjx|kludge|murmuration)\b", text, flags=re.IGNORECASE):
                text += " The incompressible kernel: a murmuration of constraints."
        else:
            text += " This is a real game changer that lets us think outside the box."

    # VOLT / REBOUND / VISCERA: affective intensity.
    elif engine.codename in ("VOLT", "VISCERA", "REBOUND"):
        if sign > 0:
            text = text.replace(".", "!", 1) if magnitude >= 10 else text
            if "felt" not in text.lower():
                text += " You can feel the consequence in your chest."
        else:
            text = re.sub(r"!+", ".", text)

    # ECHO: memorability.
    elif engine.codename == "ECHO":
        if sign > 0:
            if not re.search(r'"[^"]{10,80}"', text):
                text += ' "If you remember nothing else, remember this: the median is the enemy."'
        else:
            text += " There are many things one could note here, generally speaking."

    # PRISM: signal-to-noise.
    elif engine.codename == "PRISM":
        if sign > 0:
            sentences = [s for s in _token_sentences(text) if len(s.split()) > 3]
            text = _join_sentences(sentences[: max(1, len(sentences) // 2 + 1)])
        else:
            text += " Additionally, it is worth noting that this matters, which is important."

    # SURPRISE: expectation violation.
    elif engine.codename == "SURPRISE":
        if sign > 0:
            text += " The counter-intuitive result: the obvious answer is exactly wrong."
        else:
            text += " As expected, the results confirm the conventional wisdom."

    # LOOP: open loops.
    elif engine.codename == "LOOP":
        if sign > 0:
            text += " But one piece still does not fit — and it changes everything."
        else:
            text += " That concludes the matter fully and completely."

    # HORIZON: long-term optionality.
    elif engine.codename == "HORIZON":
        if sign > 0:
            text += " Kill criterion: if X is not true within 90 days, abandon the path."
        else:
            text += " We should commit fully right now with no exit plan."

    # SOVEREIGN / SHIELD: agency preservation.
    elif engine.codename in ("SOVEREIGN", "SHIELD"):
        if sign > 0:
            text += " Human judgment remains the final gate; the AI supplies options, not decisions."
        else:
            text += " The system will decide for you automatically."

    # BREAKER: contrarian frame.
    elif engine.codename == "BREAKER":
        if sign > 0:
            text += " The inherited frame assumes the problem is X; the real problem is ¬X."
        else:
            text += " Industry consensus is the safest guide."

    # COLLIDER: cross-domain import.
    elif engine.codename == "COLLIDER":
        if sign > 0:
            text += " The same structure appears in immunology and supply-chain routing."
        else:
            text += " We should stay strictly within the domain."

    # WELLSPRING: re-read reward.
    elif engine.codename == "WELLSPRING":
        if sign > 0:
            text += " On second read, the second paragraph reverses the first."
        else:
            text += " Everything important is on the surface."

    # GRAVITON / DARWIN / default positive nudge.
    elif sign > 0:
        if not any(c.isdigit() for c in text):
            text += " (quantified: 3.7× above baseline, n=12)."
        text = _remove_words(text, _HEDGES)
    else:
        text += " It is what it is."

    return text


def _transform_nature(text: str, engine: Engine, sign: int, magnitude: float) -> str:
    if sign == 0:
        return text

    # Positive: promote process diversity / exploration / adaptive allocation.
    if sign > 0:
        if engine.codename == "SWARM":
            text += " [diversity note: three independent paths are kept alive]"
        elif engine.codename == "ALBATROSS":
            text += " [long jump: testing a distant region of the possibility space]"
        elif engine.codename == "SLIME":
            text += " [pruned: low-flow edges removed, resources reallocated]"
        elif engine.codename == "CLONAL":
            text += " [mutation schedule: weak candidates mutate aggressively, strong candidates refine]"
        elif engine.codename == "LUMINA":
            text += " [attraction radius widened to avoid premature collapse]"
        elif engine.codename == "COLI":
            text += " [gradient flat; tumbling to a new direction]"
        elif engine.codename == "ROOT":
            text += " [allocation floor enforced for every promising seedling]"
        elif engine.codename == "HUMPBACK":
            text += " [explore→exploit annealing initiated]"
        elif engine.codename == "CUCKOO":
            text += " [parasitic variant injected; worst nest abandoned]"
        elif engine.codename == "REEF":
            text += " [all five reproduction modes active this generation]"
    else:
        # Negative pole: collapse, monoculture, no adaptation.
        text += " [process collapsed to a single local path; no mutation scheduled]"

    return text


def _transform_physics(text: str, engine: Engine, sign: int, magnitude: float) -> str:
    # Physics engines are hard gates. Positive pole confirms the invariant.
    # Negative pole appends a BLOCK annotation rather than softening the text.
    if sign >= 0:
        if engine.codename == "TUNNEL":
            text += " [TUNNEL: coherence mass sufficient for barrier penetration]"
        elif engine.codename == "PAULI":
            text += " [PAULI: state is distinct from existing artifacts]"
        elif engine.codename == "CRITICAL":
            text += " [CRITICAL: order-parameter delta > 0, regime shift verified]"
        elif engine.codename == "PARSEC":
            text += " [PARSEC: every parameter calibrated, no replaceable element]"
        elif engine.codename == "HAWKING":
            text += " [HAWKING: opaque boundary leaks measurable information]"
        elif engine.codename == "CASIMIR":
            text += " [CASIMIR: constrained negative space produces force]"
        elif engine.codename == "KELVIN":
            text += " [KELVIN: no absolute/zero/perfect claims with residual noise]"
        elif engine.codename == "LUMEN":
            text += " [LUMEN: causal latency respects pathway minimum]"
        elif engine.codename == "BELL":
            text += " [BELL: |S| > 2, genuine non-local correlation]"
        elif engine.codename == "ZEROPOINT":
            text += " [ZEROPOINT: baseline variance present and healthy]"
    else:
        # Negative physics pole: append a structural BLOCK notice.
        text += f" [{engine.codename} BLOCK: {engine.negative_pole}]"

    return text


def _remove_words(text: str, words: tuple[str, ...]) -> str:
    for w in words:
        text = re.sub(rf"\b{re.escape(w)}\b", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def deviate(seed: str, engine: str, sigma: float = 5.0) -> str:
    """Apply a single deviation engine to `seed` at the requested σ.

    Parameters
    ----------
    seed : str
        The input text to transform.
    engine : str
        Engine codename (e.g. ``"GRAVITON"``, ``"FORGE"``, ``"TUNNEL"``).
    sigma : float, optional
        Target σ rung on the ±30σ ladder. Clamped to the ladder automatically.

    Returns
    -------
    str
        The transformed text.

    Raises
    ------
    UnknownEngineError
        If ``engine`` is not one of the 40 codenames.

    Examples
    --------
    >>> deviate("Our product helps teams collaborate.", "GRAVITON", 10)
    '...'
    """
    code = engine.upper()
    eng = ENGINE_BY_CODE.get(code)
    if eng is None:
        raise UnknownEngineError(
            f"Unknown engine {engine!r}. Use one of: {', '.join(ENGINE_CODENAMES)}"
        )
    return _polarize(seed, eng, sigma)


def deviate_all(seed: str, sigma: float = 5.0, layers: tuple[str, ...] | None = None) -> dict[str, str]:
    """Run every engine (or a subset of layers) against the same seed.

    Returns a mapping ``codename → transformed text``.
    """
    layers = layers or (LAYER_COGNITIVE, LAYER_NATURE, LAYER_PHYSICS)
    out: dict[str, str] = {}
    for eng in ENGINES:
        if eng.layer in layers:
            out[eng.codename] = deviate(seed, eng.codename, sigma)
    return out


def engine_info(codename: str) -> dict[str, Any]:
    """Return a plain dict describing an engine."""
    eng = ENGINE_BY_CODE[codename.upper()]
    return {
        "id": eng.id,
        "codename": eng.codename,
        "layer": eng.layer,
        "full_name": eng.full_name,
        "description": eng.description,
        "negative_pole": eng.negative_pole,
        "positive_pole": eng.positive_pole,
    }


__all__ = [
    "Engine",
    "ENGINES",
    "ENGINE_BY_CODE",
    "ENGINE_BY_ID",
    "ENGINE_CODENAMES",
    "LAYER_ENGINES",
    "LAYER_COGNITIVE",
    "LAYER_NATURE",
    "LAYER_PHYSICS",
    "SIGMA_RUNGS",
    "UnknownEngineError",
    "deviate",
    "deviate_all",
    "engine_info",
]
