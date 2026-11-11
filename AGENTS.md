# Project Seed agent instructions

Respond and work as a researcher and developer. Distinguish implemented behavior,
measured results, and hypotheses. Read `specifications.md` and `docs/threat-model.md`
before changing runtime behavior.

- Keep changes focused; preserve existing contributor work and Apache-2.0 notices.
- Model proposals must never set permissions, consent, provenance, or identity.
- Keep the initial capability read-only, local, bounded, and explicitly granted.
- Do not introduce arbitrary URL fetching, code execution, or model-selected paths.
- Keep fixtures synthetic; never commit credentials, real memories, or user logs.
- Use the official MCP SDK; do not invent an MCP wire protocol.
- Add negative tests for changes to validation, routing, authorization, or transport.
- Update schemas/spec/docs when contracts change; mark future work honestly.
- Do not present deterministic parser tests as learned model performance.

Checks: `ruff check .`, `ruff format --check .`, `python -m pytest -q`,
`project-seed demo`, `project-seed evaluate`, and `python -m build`.
