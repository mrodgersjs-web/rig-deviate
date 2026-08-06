# Contributing to RIG Deviate

Thanks for helping push AI output past the generic median.

## Development setup

```bash
git clone https://github.com/mrodgersjs-web/rig-deviate.git
cd rig-deviate
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

## Project structure

- `rig_deviate/engines.py` — the 40-engine roster and `deviate()` transform.
- `rig_deviate/score.py` — Robust-MAD-Z scoring and feature extraction.
- `examples/demo.py` — runnable demo.
- `test/` — pytest suite.

## Adding an engine

Engines are dataclasses in `rig_deviate/engines.py`. To add one:

1. Append a new `Engine(...)` to the correct layer list.
2. Add a transformation branch in `_transform_cognitive`, `_transform_nature`, or `_transform_physics`.
3. Add a scoring branch in `rig_deviate/score.py` if the new engine needs custom features.
4. Add a test in `test/test_engines.py`.

## Code style

We use `ruff` for linting and formatting:

```bash
ruff check .
ruff format .
```

## Pull request process

1. Open an issue describing the bug or feature.
2. Fork the repo and create a feature branch.
3. Keep changes focused and well-tested.
4. Ensure `pytest` passes before requesting review.
5. Update `README.md` if public behavior changes.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
