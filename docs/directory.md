# Repository directory

This is the actual starter layout, not a list of empty planned modules.

| Path | Purpose |
| --- | --- |
| `README.md` | Project introduction, About section, status, quickstart |
| `specifications.md` | Versioned behavior, contracts, authorization, evaluation plan |
| `ABOUT.md` | Project background and GitHub sidebar description/topics |
| `LICENSE`, `NOTICE` | Apache-2.0 license and project attribution |
| `CONTRIBUTING.md` | Setup, checks, contribution workflow |
| `CODE_OF_CONDUCT.md` | Community expectations and reporting limitations |
| `SECURITY.md` | Security-reporting guidance and supported scope |
| `ROADMAP.md` | Milestones and starter tasks with acceptance evidence |
| `AGENTS.md` | Instructions for AI-assisted contributors |
| `pyproject.toml` | Packaging, dependencies, command entry points, test/lint settings |
| `MANIFEST.in` | Documentation and examples included in source distributions |
| `src/project_seed/__init__.py` | Public core API and package version |
| `src/project_seed/__main__.py` | `python -m project_seed` entry point |
| `src/project_seed/validation.py` | Bounded JSON reading and packaged schema validation |
| `src/project_seed/registry.py` | Immutable seed definitions and allowlist |
| `src/project_seed/memory.py` | Read-only memory snapshot and per-record digest |
| `src/project_seed/runtime.py` | Trusted host context, authorization, retrieval, audit |
| `src/project_seed/router.py` | Exact-command baseline with abstention |
| `src/project_seed/evaluation.py` | Synthetic regression runner |
| `src/project_seed/cli.py` | Demo, validation, activation, and evaluation CLI |
| `src/project_seed/mcp_server.py` | Optional stdio MCP adapter, no network listener |
| `src/project_seed/schemas/` | Registry, proposal, and memory JSON Schema contracts |
| `src/project_seed/fixtures/` | Synthetic registry, memory, and evaluation examples |
| `examples/mcp-config.json` | MCP host configuration with explicit demo-only grants |
| `docs/mcp.md` | MCP setup, result handling, and trust limitations |
| `docs/threat-model.md` | Assets, threats, controls, and residual risks |
| `docs/research.md` | Primary sources, hypothesis, and research honesty |
| `docs/license-check.md` | Verification of the existing Apache license |
| `tests/` | Policy, parser, validation, CLI, and MCP integration regression tests |
| `.github/workflows/ci.yml` | Python matrix, lint, tests, demos, packaging |
| `.github/ISSUE_TEMPLATE/` | Bug and proposal templates |
| `.github/PULL_REQUEST_TEMPLATE.md` | Contributor review checklist |
| `.gitignore` | Excludes environments, builds, secrets, and local private data |

`local-data/` is intentionally ignored and not committed. It is a suggested place
for local snapshots, not a security boundary or encryption mechanism. There are
no model weights or training datasets in this repository.
