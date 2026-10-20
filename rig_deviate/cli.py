"""Command line for rig-deviate.

Commands:
    engines            list all 40 rewrite strategies with their strength range
    rewrite TEXT       rewrite TEXT with one strategy at a chosen strength
    score TEXT         score TEXT and print the rig_l grade

Exit codes: 0 success, 2 usage error.
"""

from __future__ import annotations

import argparse
import json

from .engines import ENGINES, SIGMA_RUNGS, UnknownEngineError, deviate
from .score import score


def cmd_engines(args: argparse.Namespace) -> int:
    rows = [
        {
            "codename": e.codename,
            "layer": e.layer,
            "id": e.id,
            "focus": e.full_name,
        }
        for e in ENGINES
    ]
    if args.json:
        print(json.dumps({"count": len(rows), "sigma_rungs": list(SIGMA_RUNGS), "engines": rows},
                         indent=2, sort_keys=True))
        return 0
    print(f"{len(rows)} rewrite strategies, {len(SIGMA_RUNGS)} strength levels: {list(SIGMA_RUNGS)}")
    for e in ENGINES:
        print(f"  {e.id:>3}  {e.codename:<12} {e.layer:<10} {e.full_name}")
    return 0


def cmd_rewrite(args: argparse.Namespace) -> int:
    try:
        result = deviate(args.text, args.engine, args.sigma)
    except UnknownEngineError as exc:
        print(f"error: {exc}")
        return 2
    print(result)
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    report = score(args.text, engines=[args.engine] if args.engine else None)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, default=str))
        return 0
    print(f"rig_l: {report['rig_l']} {report['rig_l_label']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rig-deviate", description="Rewrite text away from generic phrasing and score the result.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("engines", help="list the 40 rewrite strategies")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_engines)

    p = sub.add_parser("rewrite", help="rewrite text with one strategy")
    p.add_argument("text")
    p.add_argument("--engine", default="GRAVITON")
    p.add_argument("--sigma", type=float, default=5.0)
    p.set_defaults(func=cmd_rewrite)

    p = sub.add_parser("score", help="score text")
    p.add_argument("text")
    p.add_argument("--engine", default=None, help="restrict scoring to one strategy")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_score)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
