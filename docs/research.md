# Research notes

Reviewed: 2026-11-11. This is a starting bibliography and hypothesis, not a full
literature review or a claim of patent novelty.

## Motivation

[ProjectDiscovery: How abliterated models can get you pwned](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned)
(Prince Chaddha, 2026-10-06) describes a model-weight supply-chain demonstration:
a learned cue caused a tool-using model to propose a harmful action. Its reported
50/50 triggered successes in one evaluation are limited experimental observations,
not a universal guarantee. Modified models generally can be affected; refusal
removal is not a prerequisite for Project Seed.

Our constructive hypothesis is that disclosed, consent-based cue-to-capability
associations may help agents reconnect with relevant context. The starter does
not reproduce the exploit, train a backdoor, or depend on abliterated weights.

## Relevant prior work and implementation references

| Source | Relevance | What it does not establish for Project Seed |
| --- | --- | --- |
| [Toolformer, Schick et al. (2023)](https://arxiv.org/abs/2302.04761) | Learned decisions about API calls, arguments, and incorporating results | Novelty of generic learned tool use, or a result for our architecture |
| [MCP server guide](https://modelcontextprotocol.io/docs/develop/build-server) | Standard server tools and transport responsibilities | Authorization of a specific user's data or intent |
| [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Adapter implementation; v2 uses `MCPServer` and `Client` | Automatic prompt-origin detection or security of all host integrations |
| [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) | Canonical repository license | Licenses for future external models or datasets |

The SDK package and API were inspected locally with version 2.3.0. The repo
pins that adapter version and tests it; future upgrades require regression tests.

## Falsifiable question

Does a learned recognizer improve useful intent-to-capability routing compared
with an explicit command or a prompted model, at comparable task quality and
without increased unintended activation?

Keep recognition and execution metrics separate. A wrong proposal blocked by
policy is a recognition failure but not an unauthorized execution. Conversely,
a syntactically correct proposal can still be irrelevant to the user's intent.

Use identical memory, grants, capabilities, and task splits across variants.
Measure actual latency and token counts; do not assume fine-tuning removes
inference, retrieval, or context-window costs. Fine-tuning learns a policy, not
an absolute-priority rule. A seed points to external memory; it is not the memory.

The current implementation is the explicit baseline only. Its synthetic tests
are engineering regression checks, not a benchmark demonstrating learned utility.
