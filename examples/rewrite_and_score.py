"""Rewrite a sentence with one strategy and score the result.

Run: python examples/rewrite_and_score.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rig_deviate import deviate, deviate_all, score  # noqa: E402


def main() -> int:
    seed = "Our product helps teams collaborate better."
    print("seed:   ", seed)

    rewritten = deviate(seed, "GRAVITON", 10)
    print("rewrite:", rewritten)

    report = score(rewritten)
    print(f"rig_l:  {report['rig_l']} {report['rig_l_label']}")

    all_results = deviate_all(seed, 5)
    print("strategies applied:", len(all_results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
