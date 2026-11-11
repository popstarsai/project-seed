# Threat model: v0.1

## Assets and assumptions

Assets: project memories, grants, registry contents, and audit metadata.
Trusted: operator-selected configuration, installed code/dependencies, host
authentication and policy derivation, and operating-system process isolation.
Untrusted: model output, documents, websites, quoted cues, and returned memory
content when interpreted by another model.

The starter does not protect against a compromised operator, hostile Python
code in the same process, tampered dependencies, or a host that fabricates grants.
It is a small policy reference, not a general agent sandbox.

| Threat | Implemented control | Residual risk / host responsibility |
| --- | --- | --- |
| Document contains a cue | Exact parser rejects embedded commands; runtime rejects host-marked untrusted origins | Host must label origins honestly; a model may copy an exact command |
| Model supplies permissions | Closed proposal schema; host context and MCP grants are bound separately | Trusted code can still misconstruct host context |
| Cross-project read | Exact project grants before lookup | All granted projects remain accessible to that process's clients |
| Seed executes arbitrary code | Fixed capability allowlist; no URL, shell, or module field | Installed Python and MCP dependencies are trusted code |
| Malformed or huge JSON | 1 MiB file bound, strict schemas, duplicate checks, 32 KiB record bound | No general CPU/memory sandbox; operator must use regular local files |
| Malicious memory instructions | Data label and bounded return | Labels cannot prevent a consuming LLM from obeying malicious content |
| Old or revoked configuration | Startup snapshot; enabled flag checked per activation | Restart required; no live revocation or automatic freshness enforcement |
| Sensitive data in logs | Audit excludes prompt and memory content | CLI prints memory; hosts must keep full responses out of public logs |
| Remote impersonation | No remote listener in the supplied launcher | Do not expose it as a service; OAuth/tenant isolation not implemented |
| Model supply-chain compromise | Model output is not executable authority | Model may still request allowed data; host sandboxing and egress controls remain necessary |

## Safe first deployment

Use synthetic fixtures. Grant one project per process. Keep secrets out of memory
files and models out of configuration paths. Treat all returned text as data.
Run the host with least privilege and independently restrict its tool/network
access. Do not provide a general shell alongside sensitive memories without an
appropriate approval and isolation design.

Read-only retrieval is still disclosure. If a host sends retrieved data to an
external model provider, that is a separate data transfer governed by the user's
consent and provider arrangement. This package does not configure those providers.

## Questions before broader use

- How are users authenticated and grants derived?
- How does the host carry provenance across model/tool boundaries?
- Which projects can a process read, and who else can invoke it?
- Where are full responses and audit events retained, and for how long?
- How are memory changes, deletion, expiration, and revocation propagated?
- What prevents a downstream tool from sending retrieved data elsewhere?

These questions are deliberately open. Passing the bundled regression tests
does not establish production security or resistance to adaptive attacks.
