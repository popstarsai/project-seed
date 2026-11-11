# SPDX-License-Identifier: Apache-2.0
"""Offline CLI with explicit, local-process grants."""

import argparse
import json
import sys

from .evaluation import evaluate
from .memory import MemoryStore
from .registry import SeedRegistry
from .runtime import HostContext, SeedRuntime
from .validation import InvalidData, fixture, load_json


def add_files(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--registry", required=True, help="Trusted local registry JSON path")
    parser.add_argument("--memory", required=True, help="Trusted local memory JSON path")


def add_grants(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--principal", required=True, help="Host-assigned local principal label")
    parser.add_argument("--allow-project", action="append", default=[], help="Repeat per grant")
    parser.add_argument("--allow-memory-read", action="store_true", help="Grant memory:read")
    parser.add_argument("--consent", action="store_true", help="Approve this process's reads")


def context_from_args(args: argparse.Namespace, *, origin: str) -> HostContext:
    return HostContext(
        principal_id=args.principal,
        allowed_projects=frozenset(args.allow_project),
        scopes=frozenset({"memory:read"}) if args.allow_memory_read else frozenset(),
        origin=origin,
        consent=args.consent,
    )


def runtime_from_args(args: argparse.Namespace) -> SeedRuntime:
    return SeedRuntime(SeedRegistry(load_json(args.registry)), MemoryStore(load_json(args.memory)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project Seed read-only reference runtime")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo", help="Restore a bundled synthetic project; no keys or network")
    commands.add_parser("evaluate", help="Run synthetic exact-command regression cases")
    validate_parser = commands.add_parser("validate", help="Validate registry and memory snapshots")
    add_files(validate_parser)
    run_parser = commands.add_parser("run", help="Execute one explicit seed activation")
    add_files(run_parser)
    add_grants(run_parser)
    run_parser.add_argument("--seed", required=True)
    run_parser.add_argument("--project", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "evaluate":
            report = evaluate()
            print(json.dumps(report, indent=2))
            return 0 if report["passed"] == report["total"] else 1
        if args.command == "demo":
            runtime = SeedRuntime(SeedRegistry(fixture("registry")), MemoryStore(fixture("memory")))
            context = HostContext(
                "demo-user", frozenset({"demo"}), frozenset({"memory:read"}), "user", True
            )
            proposal = {"seed_id": "project.restore", "project_id": "demo"}
        else:
            runtime = runtime_from_args(args)
            if args.command == "validate":
                print(json.dumps({"seeds": len(runtime.registry), "projects": len(runtime.memory)}))
                return 0
            context = context_from_args(args, origin="user")
            proposal = {"seed_id": args.seed, "project_id": args.project}
        result = runtime.activate(proposal, context)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "ok" else 1
    except InvalidData as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}), file=sys.stderr)
        return 2
