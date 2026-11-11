# Security Policy

Project Seed is an experimental reference implementation, not a hardened security
product. Use synthetic data until your host, OS permissions, and deployment have
been independently reviewed. Read [docs/threat-model.md](docs/threat-model.md).

## Reporting

Use GitHub's **Report a vulnerability** option on this repository's Security tab
if private vulnerability reporting is enabled. If it is unavailable, open a
minimal issue asking the maintainer to establish a private reporting channel.
Do not put exploit details, credentials, personal data, or real memory snapshots
in that public issue. There is currently no verified dedicated security email or
guaranteed response SLA.

Include the affected commit, a synthetic reproduction, impact, and proposed fix
through the private channel once established. No permission is granted to test
third-party systems or other people's data.

## Supported versions

Only the current default branch is under active development. No stable releases
or long-term support branches have been published by this starter.

## Known boundaries

- `HostContext` is trusted application state, not proof of identity.
- The stdio adapter's grants are shared by all callers of that process.
- Memory is read-only but can still contain sensitive data or malicious instructions.
- Runtime data labels and MCP annotations do not neutralize prompt injection.
- Restart processes after registry, grant, or memory changes; no hot revocation exists.
- No remote authentication, tenant isolation, encryption, OS sandbox, or egress
  policy is implemented by this package.
- No tool accepts shell commands, arbitrary URLs, or per-request filesystem paths.
- Snapshots are selected at startup, bounded, and copied; the process can still
  access whatever the operating system permits.

The Apache license remains unchanged. These are deployment warnings and project
scope decisions, not additional license restrictions.
