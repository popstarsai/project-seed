# Project Seed

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![CI](https://github.com/popstarsai/project-seed/actions/workflows/ci.yml/badge.svg)](https://github.com/popstarsai/project-seed/actions/workflows/ci.yml)

**Help an AI agent reconnect with the right context, under the user's control.**

Project Seed explores explicit, inspectable associations between meaningful cues,
persistent project memory, and permission-scoped tools. A model may propose a
seed activation; the application decides whether it is authorized. Memory stays
outside model weights so it can be inspected, corrected, and replaced.

Initiated by **Alin Eugen Costin / Pop Stars AI LLC**. Researchers, developers,
documentation writers, and security reviewers are welcome.

## About

Open-source research and a reference runtime for user-governed context activation
in AI agents. Version 0.1 starts with read-only project memory, strict JSON
contracts, explicit host permissions, a local MCP adapter, and reproducible tests.
Learned seed recognition is a research track, not a feature already delivered.

**Status: experimental alpha.** No production security certification, trained
model, hosted service, model weights, or published performance claims.

## Try it locally

Python 3.11 or later. No GPU, account, API key, or model download is needed.
Installation downloads Python dependencies; the demo itself makes no network calls.

```bash
git clone https://github.com/popstarsai/project-seed.git
cd project-seed
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,mcp]"
project-seed demo
project-seed evaluate
python -m pytest -q
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`, or use
`.venv\Scripts\python.exe` directly. For the core only, install with
`python -m pip install -e .`; `dev` and `mcp` are optional extras.

The demo retrieves a **synthetic** project with a summary, decisions, next steps,
source timestamp, and a record digest. It explicitly grants access to `demo`
for this process. It does not read your files or actual conversation history.

## How it works

1. A command or recognizer proposes a seed ID and a project ID.
2. The runtime validates the proposal against a closed schema.
3. Host-supplied provenance, consent, project access, and scope are checked.
4. An enabled seed resolves to the built-in read-only memory capability.
5. The caller receives bounded data and an audit event, or a structured denial.

The baseline command is `/seed project.restore demo`. The parser accepts only a
whole, exact command; it does not search documents for trigger strings. The
runtime independently rejects requests that the host marks as untrusted.

**Host trust matters:** this library does not authenticate users or infer where a
model's idea came from. Tool arguments must never determine permissions. A
connected MCP client can request all data granted to its process. Use synthetic
data first, and read the [threat model](docs/threat-model.md).

## What is implemented?

| Available now | Planned research / engineering |
| --- | --- |
| Exact-command baseline | Prompted and fine-tuned semantic recognizers |
| JSON registry and memory snapshot validation | Signed registry distribution and hot revocation |
| Deny-by-default host policy | Remote authentication and tenant isolation |
| One read-only memory capability | Additional reviewed, narrowly scoped capabilities |
| Stdio MCP adapter, official Python SDK | Model/provider adapters and host integrations |
| Synthetic evaluation and unit/integration tests | Held-out multilingual and adversarial benchmarks |

## Use your own synthetic snapshot

Start with the JSON files in [`src/project_seed/fixtures/`](src/project_seed/fixtures/).
Keep private copies in ignored `local-data/`; do not commit personal memories.

```bash
project-seed validate \
  --registry src/project_seed/fixtures/registry.json \
  --memory src/project_seed/fixtures/memory.json

project-seed run \
  --registry src/project_seed/fixtures/registry.json \
  --memory src/project_seed/fixtures/memory.json \
  --principal local-user --allow-project demo --allow-memory-read --consent \
  --seed project.restore --project demo
```

These are local administrative flags, not authentication credentials. Omitting
the grants or consent denies a read. The snapshot and registry are loaded at
startup; restart after edits or permission changes.

## Connect over MCP

See [MCP setup](docs/mcp.md) and the [example host configuration](examples/mcp-config.json).
The adapter exposes only `seed_activate(seed_id, project_id)`. It has no shell,
file-writing, arbitrary URL, memory-editing, or HTTP-listener tool.

## Join the project

Read the [specification](specifications.md), [directory guide](docs/directory.md),
[contributing guide](CONTRIBUTING.md), and [roadmap](ROADMAP.md).

Good first contributions include multilingual negative examples, clearer Windows
setup instructions, schema edge-case tests, and evaluation fixtures with documented
provenance. Larger contributions include recognizer adapters and reproducible
comparisons of explicit, prompted, and learned activation. Open an issue before
changing the authority boundary or adding a new capability.

Please distinguish **implemented**, **measured**, and **hypothesized** in every
claim. Passing the bundled checks is not proof of generalization or safety.

## Background and license

Inspired by a constructive question following [ProjectDiscovery's model
supply-chain research](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned):
can learned cue-to-action associations become transparent, consent-based utilities?
Existing tool-use learning work, including [Toolformer](https://arxiv.org/abs/2302.04761),
is relevant prior art. See [research notes](docs/research.md).

Project Seed does **not** require abliteration, hidden triggers, or bypassing
model safeguards. This repository contains no poisoning or exploit implementation.

Licensed under [Apache License 2.0](LICENSE), with attribution in [NOTICE](NOTICE).
Third-party models, datasets, and dependencies retain their own licenses.
