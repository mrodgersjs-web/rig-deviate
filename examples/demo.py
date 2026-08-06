"""examples/demo.py — runnable demo of rig-deviate.

Run with:

    python examples/demo.py

or, after installing the package:

    python -m rig_deviate.demo
"""
from __future__ import annotations

from rig_deviate import deviate, score


def main() -> None:
    seed = "Our product helps teams collaborate better."

    print("=== RIG Deviate Demo ===\n")
    print(f"Seed text: {seed!r}\n")

    # Apply a single cognitive engine at +10σ.
    graviton = deviate(seed, "GRAVITON", 10)
    print(f"GRAVITON (+10σ): {graviton}\n")

    # Apply a mechanism engine.
    forge = deviate(seed, "FORGE", 10)
    print(f"FORGE (+10σ): {forge}\n")

    # Apply a hard physics gate (positive pole).
    tunnel = deviate(seed, "TUNNEL", 10)
    print(f"TUNNEL (+10σ): {tunnel}\n")

    # Score the most deviant result.
    report = score(graviton)
    print("Score report:")
    print(f"  RIG-L: {report['rig_l']} ({report['rig_l_label']})")
    print(f"  Weakest gate: {report['weakest_gate']}")
    print(f"  Features: {report['features']}")


if __name__ == "__main__":
    main()
