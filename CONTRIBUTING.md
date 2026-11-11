# Contributing to Project Seed

Welcome. You do not need to train a model to make a useful contribution. Clear
examples, rigorous tests, and honest evaluation are central to this project.

## First contribution

1. Read [README.md](README.md), [specifications.md](specifications.md), and the
   [threat model](docs/threat-model.md).
2. Pick a task in [ROADMAP.md](ROADMAP.md), or open a small proposal issue.
3. Fork the repository and create a focused branch.
4. Install Python 3.11+ and run `python -m pip install -e ".[dev,mcp]"` in a venv.
5. Make the change, add tests, and run the checks below.
6. Submit a pull request explaining the behavior, verification, and limitations.

```bash
ruff check .
ruff format --check .
python -m pytest -q
project-seed demo
project-seed evaluate
python -m build
```

## Development principles

- Model output proposes; trusted host policy authorizes.
- Prefer small, auditable modules and the official MCP SDK over hand-written transport.
- Preserve deny-by-default behavior and negative tests.
- Never accept permissions, shell commands, file paths, or remote endpoints in proposals.
- Keep docs, schemas, and implementations aligned.
- Use synthetic or explicitly licensed fixtures. Never commit API keys, user memories,
  conversation exports, private logs, or confidential project data.
- Disclose AI-assisted code generation in the PR and verify it like other code.
- Report failures and denominators; do not describe a toy test as a benchmark win.

The project is Apache-2.0. Contributions intentionally submitted for inclusion
are under the same license unless explicitly stated otherwise. Retain third-party
notices and document provenance. Linked models/datasets are not automatically
covered by this repository's license.

## Changes that need a proposal first

Adding capabilities, persistent writes, network access, training pipelines,
authentication, schema-version changes, or provider dependencies should start
with an issue describing alternatives, threat boundaries, and acceptance tests.
Maintainer review is required before merging; CI alone is not security approval.

## Research contributions

Include reproducible configuration, data/model licenses, split boundaries,
evaluation scripts, hardware and token/latency measurement details, baseline
results, and limitations. Learned recognizers must share the same runtime policy
as command-based baselines. A refusal rate or confidence score is not authorization.

## Community

Be specific, patient, and respectful. Challenge claims and code, not people.
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Vulnerability reports follow
[SECURITY.md](SECURITY.md), not ordinary public bug templates.
