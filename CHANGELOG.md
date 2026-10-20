# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- This commit switches the README CI badge to the shields.io workflow status URL and adds a 15 minute timeout to all three workflow jobs.
- This commit adds .github/copilot-instructions.md describing the rewrite engines, the scorer, the pytest and ruff commands, and the truth rule for numbers in docs.
- This commit adds .github/CODEOWNERS, which assigns @mrodgersjs-web as the code owner for every file in the repo.

- This commit adds the `tomli` backport to the dev extra for Python 3.10 and has `test/test_packaging_config.py` fall back to it, because `tomllib` only exists from 3.11 and the 3.10 CI leg failed at import.

## [0.2.0] - 2026-10-19

### Changed

- Documentation rewritten in plain English with runnable worked examples and real output.
- Removed superlative claims from code, docs, and CLI descriptions.
- Packaging completed: dev extras (pytest, pytest-cov, ruff), ruff configuration, coverage configuration.

### Added

- `pyproject.toml` packaging config: `rig-deviate` console script, dev
  extras (pytest, pytest-cov, ruff), ruff rules on the py310 floor and
  coverage config; `test/test_packaging_config.py` asserts that config is
  present and points at importable code.
- `test/test_readme_truth.py`: reads README.md and asserts its numbers (40
  strategies, 13 strength levels, the ladder values) match the code.
- CI workflow that runs lint and the test suite with coverage on push and pull request.
- Community files: security policy, code of conduct, contributing guide, issue and pull request templates.
- `docs/architecture.md` design notes and a runnable example under `examples/`.
