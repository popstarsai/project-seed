# Local MCP setup

The starter uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk),
pinned to `mcp==2.3.0` for this adapter. It provides a stdio server, not an HTTP
service. Install the project in a virtual environment before registering it:

```bash
python -m pip install -e ".[mcp]"
```

See [`examples/mcp-config.json`](../examples/mcp-config.json). Replace the three
absolute-path placeholders with your clone and its virtual environment. On
Windows use `.venv/Scripts/python.exe`; JSON also accepts forward slashes in
Windows paths. Host configuration formats vary; the example uses the common
`mcpServers` shape and does not install itself into any host.

The server process can also be started explicitly:

```bash
python -m project_seed.mcp_server \
  --registry src/project_seed/fixtures/registry.json \
  --memory src/project_seed/fixtures/memory.json \
  --principal local-demo --allow-project demo --allow-memory-read --consent
```

It waits for MCP messages on stdin, so it is not an interactive chat. Start it
through an MCP host for ordinary use. Diagnostics belong on stderr; stdout is
reserved for the protocol.

## Tool contract

`seed_activate` accepts exactly the two semantic arguments:

```json
{"seed_id": "project.restore", "project_id": "demo"}
```

The SDK exposes this via standard MCP tool discovery/invocation. There is no
special `mcp://memory/fetch_graph(...)` invocation syntax. The tool returns a
structured runtime result. Domain denials and missing memory are structured
outcomes, not transport failures; inspect `status`, `reason`, and `data`.

Example success fields (the actual memory and audit fields are omitted here):

```json
{
  "schema_version": "0.1",
  "status": "ok",
  "reason": "retrieved",
  "seed_id": "project.restore",
  "seed_version": "0.1.0",
  "project_id": "demo"
}
```

## Permission boundary

Startup flags are chosen by the trusted operator or host. They are not accepted
from tool arguments. `--consent` approves reads for this process's lifetime;
it is not a per-call user confirmation UI. Do not set it for data the user has
not agreed to expose to that host.

All callers of one process share its grants. A model induced by a webpage could
still request an already-granted project: the adapter cannot observe the true
cause of the request. Hosts must preserve source provenance and apply approval
rules. Do not claim that annotations or an opaque seed ID prevent injection.

Restart the server after changing memory, registry entries, or grants. Use one
narrow snapshot/process per trust context; do not put this implementation behind
a public reverse proxy. Remote authorization is future work.

## Verification

```bash
python -m pip install -e ".[dev,mcp]"
python -m pytest tests/test_mcp.py -q
```

The suite checks tool discovery, bound permissions, a forged-consent attempt,
and a real subprocess stdio roundtrip. It does not claim compatibility with every
MCP host UI or verify host-side prompt-injection defenses.
