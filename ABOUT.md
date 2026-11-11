# About Project Seed

Project Seed is an independent open-source research and development project
initiated by Alin Eugen Costin / Pop Stars AI LLC. It investigates how explicit,
user-governed cues can reconnect AI agents with relevant memory and capabilities.

The first implementation is a small Python reference runtime with read-only
project retrieval, policy checks, strict schemas, an optional local MCP adapter,
and tests. The longer-term research track compares command-based, prompted,
and learned recognition. No trained model is included or claimed.

Contributors can help with evaluation, adapters, security review, and documentation.
See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

## GitHub sidebar copy

Description (ready for the repository's About field):

> User-governed context activation for AI agents: explicit seeds, read-only memory, permission-scoped MCP tools, and research into learned intent recognition.

Suggested topics:

`ai-agents`, `mcp`, `agent-memory`, `context-engineering`, `tool-calling`,
`machine-learning`, `python`, `open-source`, `research`

No separate project website has been published. Leave the website field empty.
This file documents the proposed metadata; committing it does not update GitHub's
sidebar. An owner can use the About gear or run, after authenticating GitHub CLI:

```bash
gh repo edit popstarsai/project-seed \
  --description "User-governed context activation for AI agents: explicit seeds, read-only memory, permission-scoped MCP tools, and research into learned intent recognition." \
  --add-topic ai-agents,mcp,agent-memory,context-engineering,tool-calling,machine-learning,python,open-source,research
```
