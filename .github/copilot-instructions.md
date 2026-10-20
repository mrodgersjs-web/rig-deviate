# Copilot instructions for rig-deviate

## What this repo is

A text rewriting and scoring toolkit. It ships forty named rewrite strategies
(the "engines"), each applied at one of thirteen strength settings, and a scorer
that reports how far a draft sits from generic phrasing. The goal is a draft that
says something specific, with a number to back it up.

- `rig_deviate/engines.py` the strategy catalog and the deterministic rewrite
  rules for each strategy.
- `rig_deviate/score.py` the scorer: per-strategy deviation scores and the
  combined verdict.
- `rig_deviate/cli.py` the `rig-deviate` command line: `engines` lists the
  strategies, `rewrite` applies one, `score` scores text.
- `mcp/server.py` exposes the same operations to MCP clients.
- `examples/` runnable walkthroughs (`demo.py`, `rewrite_and_score.py`).

## Layout

`rig_deviate/` is the typed package (`py.typed` ships). `test/` is the pytest
suite, including `test_readme_truth.py` and `test_ladder_truth.py`, which pin the
numbers in the README and the strength ladder to what the code actually has.
`docs/architecture.md` holds design notes. `.github/workflows/ci.yml` runs lint
and the tests.

## Setup and test commands

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
pytest -q --cov
```

Lint before every commit: `ruff check .`. Smoke path: `pytest -q test/`.
Try the CLI with `rig-deviate engines`, then `rig-deviate score "some text"`.

## Conventions

- Conventional commit prefixes: feat, fix, test, docs, ci, build, chore.
- Every behavior change lands with a test in the same commit.
- Rewrites are deterministic regex and rule transforms, not model calls: the same
  input and strength must always produce the same output.
- Strength settings and engine names are data, not code: changing the ladder or
  the catalog means updating `test_ladder_truth.py` and `test_readme_truth.py`
  in the same commit.
- No secrets, no API keys, no machine paths such as `/Users/...` in tracked
  files.

## Truth rule

Any number in a README, docstring, or comment must come from a command you ran
in this repo (for example `pytest -q`, `rig-deviate engines | wc -l`, or
`wc -l`). If the engine count or the ladder length changes, update the sentence
in the same commit. Never round up and never keep a count from an older run.
