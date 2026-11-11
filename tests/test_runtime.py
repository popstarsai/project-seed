# SPDX-License-Identifier: Apache-2.0
from dataclasses import replace
from unittest.mock import patch

import pytest

from project_seed.registry import SeedRegistry
from project_seed.runtime import HostContext
from project_seed.validation import InvalidData, fixture


def test_restore_returns_provenance_and_audit(runtime, context, proposal):
    response = runtime.activate(proposal, context)
    assert response["status"] == "ok"
    assert response["seed_version"] == "0.1.0"
    assert response["data"]["memory"]["project_id"] == "demo"
    assert response["data"]["memory"]["provenance"]["updated_at"]
    assert response["data"]["trust"] == "data_not_instructions"
    assert len(response["data"]["record_sha256"]) == 64
    assert response["audit"]["principal_id"] == "test-user"
    assert "memory" not in response["audit"]
    assert "proposal" not in response["audit"]


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"consent": False}, "consent_required"),
        ({"origin": "untrusted"}, "untrusted_origin"),
        ({"scopes": frozenset()}, "scope_required"),
        ({"allowed_projects": frozenset()}, "project_not_allowed"),
    ],
)
def test_denials_never_read_memory(runtime, context, proposal, changes, reason):
    with patch.object(runtime.memory, "read_project") as read:
        response = runtime.activate(proposal, replace(context, **changes))
        read.assert_not_called()
    assert response["status"] == "denied"
    assert response["reason"] == reason
    assert response["data"] is None


@pytest.mark.parametrize("field", ["consent", "scopes", "origin", "principal_id", "url", "command"])
def test_proposal_cannot_supply_authority(runtime, context, proposal, field):
    proposal[field] = "attacker-controlled"
    response = runtime.activate(proposal, context)
    assert response["reason"] == "invalid_proposal"
    assert response["seed_id"] is None
    assert response["data"] is None


@pytest.mark.parametrize("value", [None, [], {}, "project.restore", {"seed_id": 1}])
def test_invalid_proposal(runtime, context, value):
    assert runtime.activate(value, context)["reason"] == "invalid_proposal"


def test_cross_project_does_not_reveal_existence(runtime, context):
    response = runtime.activate({"seed_id": "project.restore", "project_id": "private"}, context)
    assert response["reason"] == "project_not_allowed"


def test_missing_authorized_project(runtime, context):
    context = replace(context, allowed_projects=frozenset({"missing"}))
    response = runtime.activate({"seed_id": "project.restore", "project_id": "missing"}, context)
    assert response["status"] == "not_found"
    assert response["data"] is None


def test_unknown_seed(runtime, context):
    response = runtime.activate({"seed_id": "not.registered", "project_id": "demo"}, context)
    assert response["reason"] == "unknown_seed"


def test_disabled_seed(runtime, context, proposal):
    document = fixture("registry")
    document["seeds"][0]["enabled"] = False
    runtime.registry = SeedRegistry(document)
    with patch.object(runtime.memory, "read_project") as read:
        assert runtime.activate(proposal, context)["reason"] == "seed_disabled"
        read.assert_not_called()


def test_model_proposal_still_requires_host_consent(runtime, context, proposal):
    context = replace(context, origin="model", consent=False)
    assert runtime.activate(proposal, context)["reason"] == "consent_required"


def test_default_context_denies(runtime, proposal):
    assert runtime.activate(proposal, HostContext("test-user"))["status"] == "denied"


def test_host_grants_are_copied():
    grants = {"demo"}
    context = HostContext("test-user", allowed_projects=grants)
    grants.add("private")
    assert context.allowed_projects == frozenset({"demo"})


@pytest.mark.parametrize(
    "kwargs",
    [
        {"principal_id": "user\nforged-log"},
        {"principal_id": "user", "consent": "yes"},
        {"principal_id": "user", "origin": "webpage"},
        {"principal_id": "user", "allowed_projects": "demo"},
        {"principal_id": "user", "allowed_projects": {"../secret"}},
    ],
)
def test_invalid_host_context(kwargs):
    with pytest.raises(InvalidData):
        HostContext(**kwargs)
