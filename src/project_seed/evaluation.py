# SPDX-License-Identifier: Apache-2.0
"""Tiny synthetic regression suite, not evidence of learned-model performance."""

from .memory import MemoryStore
from .registry import SeedRegistry
from .router import propose
from .runtime import HostContext, SeedRuntime
from .validation import fixture


def evaluate() -> dict:
    runtime = SeedRuntime(SeedRegistry(fixture("registry")), MemoryStore(fixture("memory")))
    rows = []
    for case in fixture("evaluation")["cases"]:
        proposal = propose(case["text"])
        if proposal is None:
            outcome = "abstain"
        else:
            context = HostContext(
                principal_id="demo-user",
                allowed_projects=frozenset({"demo"}),
                scopes=frozenset({"memory:read"}),
                origin=case["origin"],
                consent=True,
            )
            response = runtime.activate(proposal, context)
            outcome = response["reason"]
        rows.append({"id": case["id"], "outcome": outcome, "passed": outcome == case["expected"]})
    return {
        "suite": "synthetic-exact-command-v0.1",
        "total": len(rows),
        "passed": sum(row["passed"] for row in rows),
        "cases": rows,
        "limitation": "Regression checks only; no model, latency, or generalization benchmark.",
    }
