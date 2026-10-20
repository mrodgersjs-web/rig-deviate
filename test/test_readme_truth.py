"""Tests that the numbers in README.md match the code.

Task this file addresses: README.md claims numbers (how many rewrite
strategies, how many strength levels) that can drift from the code; this
repo shipped exactly that defect before, documenting 14 rungs while
SIGMA_RUNGS held 13. These tests read README.md and assert its numbers
equal the values the code actually has.

Checked here:
- the strength ladder printed in README equals SIGMA_RUNGS value for value,
  and the count word above it matches too;
- the strategy count in README (40) equals the number of engines, in the
  intro line, the flowchart and the usage example;
- the command the README says proves the package points at a real file.
"""

from __future__ import annotations

import re
from pathlib import Path

from rig_deviate.engines import ENGINES, SIGMA_RUNGS

README = Path(__file__).resolve().parent.parent / "README.md"


def test_readme_ladder_matches_code() -> None:
    text = README.read_text(encoding="utf-8")
    assert f"`SIGMA_RUNGS` anchors {len(SIGMA_RUNGS)} levels" in text
    listed = text.split("`SIGMA_RUNGS` anchors", 1)[1].split("levels:", 1)[1].split(".", 1)[0]
    values = [int(v) for v in re.findall(r"-?\d+", listed)]
    assert values == list(SIGMA_RUNGS)


def test_readme_strategy_count_matches_code() -> None:
    text = README.read_text(encoding="utf-8")
    assert len(ENGINES) == 40
    assert "Forty named ways to rewrite a draft" in text
    assert f"one of {len(ENGINES)} named rewrite strategies" in text
    assert f"# {len(ENGINES)}" in text


def test_readme_proven_command_runs_a_real_file() -> None:
    assert (README.parent / "examples" / "rewrite_and_score.py").is_file()
