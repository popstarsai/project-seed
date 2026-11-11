# Roadmap

This is a contribution plan, not a schedule or evidence that proposed features exist.

## M0: Reference baseline

- [x] Specification and contributor documentation.
- [x] Strict registry, proposal, and memory schemas.
- [x] Exact command recognizer and read-only local memory runtime.
- [x] Explicit provenance, consent, scope, and project checks.
- [x] Local stdio MCP adapter using the official SDK.
- [x] Synthetic fixtures, CLI, unit/integration tests, and CI workflow.

## M1: Evaluation foundation

- [ ] Held-out multilingual corpus with provenance and train/test separation.
- [ ] Shared recognizer interface with abstention and schema-constrained output.
- [ ] Prompted recognizer adapter; no hosted API required for baseline tests.
- [ ] End-to-end latency, tokenizer usage, and policy-versus-recognition metrics.
- [ ] Host integration example demonstrating trusted source metadata.

Exit criterion: reproducible explicit-versus-prompted comparison with failures,
sample sizes, uncertainty, and unrelated-task checks. No trained model required.

## M2: Learned seed recognition

- [ ] Select a model and training dataset with separately reviewed licenses.
- [ ] Train a small, disclosed adapter for proposal/abstention behavior.
- [ ] Measure trigger collisions, quoted cues, paraphrases, and out-of-distribution cases.
- [ ] Compare against M1 using identical runtime permissions and held-out splits.
- [ ] Publish model/data cards, revisions, training settings, and limitations.

Exit criterion: independently reproducible results. Do not claim benefit if the
learned recognizer fails to improve over the simpler baselines.

## M3: Carefully scoped integrations

- [ ] Durable user-editable memory with deletion and retention controls.
- [ ] Signed registries, version pinning, and live revocation semantics.
- [ ] Remote authentication and per-tenant authorization before any HTTP service.
- [ ] Recovery checkpoint interface owned by a supervisor, not by a trigger phrase.
- [ ] Review possible integrations with memory tools and agent hosts.

Potential integrations are proposals only; none is certified or bundled.

## Starter task board

| Task | Suggested scope | Acceptance evidence |
| --- | --- | --- |
| Add Romanian/English quoted-cue fixtures | Good first task | Exact parser abstains; no accidental execution |
| Improve Windows setup | Documentation | Fresh venv, demo, and MCP instructions verified |
| Add schema edge cases | Good first task | Negative tests, sanitized errors |
| Design recognizer adapter contract | Research / API | Proposal issue, abstention contract, fake adapter tests |
| Build benchmark dataset manifest | Research | License, provenance, split hashes, no personal data |
| Review stdio host permission model | Security | Synthetic reproductions and clearly stated limitations |

Open an issue to coordinate work. This table does not imply GitHub labels or
issues have already been created.
