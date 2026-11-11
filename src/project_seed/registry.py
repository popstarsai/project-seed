# SPDX-License-Identifier: Apache-2.0
"""A local allowlist, never an executable plugin manifest."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .validation import InvalidData, validate


@dataclass(frozen=True, slots=True)
class Seed:
    id: str
    version: str
    description: str
    capability: str
    required_scope: str
    enabled: bool


class SeedRegistry:
    def __init__(self, document: dict[str, Any]):
        validate(document, "registry")
        seeds = {}
        for entry in document["seeds"]:
            seed = Seed(**entry)
            if seed.id in seeds:
                raise InvalidData("duplicate seed ID")
            seeds[seed.id] = seed
        self._seeds = MappingProxyType(seeds)

    def get(self, seed_id: str) -> Seed | None:
        return self._seeds.get(seed_id)

    def __len__(self) -> int:
        return len(self._seeds)
