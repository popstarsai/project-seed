# SPDX-License-Identifier: Apache-2.0
"""Read-only, in-memory snapshot of an explicitly selected JSON document."""

import hashlib
import json
from copy import deepcopy
from typing import Any

from .validation import InvalidData, validate

MAX_RECORD_BYTES = 32_768


class MemoryStore:
    def __init__(self, document: dict[str, Any]):
        validate(document, "memory")
        self._records: dict[str, dict[str, Any]] = {}
        self._digests: dict[str, str] = {}
        for record in document["projects"]:
            project_id = record["project_id"]
            if project_id in self._records:
                raise InvalidData("duplicate project ID")
            encoded = json.dumps(record, sort_keys=True, ensure_ascii=True).encode("utf-8")
            if len(encoded) > MAX_RECORD_BYTES:
                raise InvalidData("memory record exceeds 32 KiB")
            self._records[project_id] = deepcopy(record)
            self._digests[project_id] = hashlib.sha256(encoded).hexdigest()

    def read_project(self, project_id: str) -> dict[str, Any] | None:
        record = self._records.get(project_id)
        return deepcopy(record) if record is not None else None

    def record_digest(self, project_id: str) -> str:
        return self._digests[project_id]

    def __len__(self) -> int:
        return len(self._records)
