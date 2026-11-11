# SPDX-License-Identifier: Apache-2.0
import pytest

from project_seed.memory import MemoryStore
from project_seed.registry import SeedRegistry
from project_seed.runtime import HostContext, SeedRuntime
from project_seed.validation import fixture


@pytest.fixture
def runtime():
    return SeedRuntime(SeedRegistry(fixture("registry")), MemoryStore(fixture("memory")))


@pytest.fixture
def context():
    return HostContext("test-user", frozenset({"demo"}), frozenset({"memory:read"}), "user", True)


@pytest.fixture
def proposal():
    return {"seed_id": "project.restore", "project_id": "demo"}
