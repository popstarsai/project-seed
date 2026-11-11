# SPDX-License-Identifier: Apache-2.0
"""Separate untrusted activation proposals from host-supplied authority."""

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .memory import MemoryStore
from .registry import SeedRegistry
from .validation import InvalidData, validate

_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}", flags=re.ASCII)


@dataclass(frozen=True, slots=True)
class HostContext:
    """Trusted host state, NOT a deserializer for model/tool-supplied arguments.

    The embedding application must authenticate users and derive permissions.
    This dataclass is a policy input, not an authentication mechanism.
    """

    principal_id: str
    allowed_projects: frozenset[str] = frozenset()
    scopes: frozenset[str] = frozenset()
    origin: str = "untrusted"
    consent: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.principal_id, str) or not _ID.fullmatch(self.principal_id):
            raise InvalidData("invalid host principal ID")
        if self.origin not in {"user", "model", "untrusted"} or type(self.consent) is not bool:
            raise InvalidData("invalid host provenance or consent")
        for name in ("allowed_projects", "scopes"):
            value = getattr(self, name)
            if not isinstance(value, (set, frozenset)):
                raise InvalidData("host grants must be sets")
            if not all(isinstance(item, str) for item in value):
                raise InvalidData("host grant must be a string")
            object.__setattr__(self, name, frozenset(value))
        if not all(_ID.fullmatch(item) for item in self.allowed_projects):
            raise InvalidData("invalid host project grant")


class SeedRuntime:
    def __init__(self, registry: SeedRegistry, memory: MemoryStore):
        self.registry = registry
        self.memory = memory

    def activate(self, proposal: Any, context: HostContext) -> dict[str, Any]:
        seed_id = project_id = seed_version = None

        def result(status: str, reason: str, data: dict | None = None) -> dict[str, Any]:
            return {
                "schema_version": "0.1",
                "status": status,
                "reason": reason,
                "seed_id": seed_id,
                "seed_version": seed_version,
                "project_id": project_id,
                "data": data,
                "audit": {
                    "event_id": str(uuid4()),
                    "timestamp": datetime.now(UTC).isoformat(),
                    "principal_id": context.principal_id,
                    "origin": context.origin,
                    "status": status,
                    "reason": reason,
                },
            }

        try:
            validate(proposal, "proposal")
        except InvalidData:
            return result("denied", "invalid_proposal")
        seed_id, project_id = proposal["seed_id"], proposal["project_id"]
        # Check host authority before looking up seeds or touching project data.
        if context.origin not in {"user", "model"}:
            return result("denied", "untrusted_origin")
        if not context.consent:
            return result("denied", "consent_required")
        if project_id not in context.allowed_projects:
            return result("denied", "project_not_allowed")
        if "memory:read" not in context.scopes:
            return result("denied", "scope_required")
        seed = self.registry.get(seed_id)
        if seed is None:
            return result("denied", "unknown_seed")
        seed_version = seed.version
        if not seed.enabled:
            return result("denied", "seed_disabled")
        # Defense in depth: never dispatch arbitrary names, URLs, or code.
        if seed.capability != "memory.read_project" or seed.required_scope != "memory:read":
            return result("denied", "unsupported_capability")
        memory = self.memory.read_project(project_id)
        if memory is None:
            return result("not_found", "memory_not_found")
        return result(
            "ok",
            "retrieved",
            {
                "memory": memory,
                "record_sha256": self.memory.record_digest(project_id),
                "trust": "data_not_instructions",
            },
        )
