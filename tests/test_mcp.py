# SPDX-License-Identifier: Apache-2.0
import asyncio
import json
import sys
from dataclasses import replace

import pytest

pytest.importorskip("mcp")

from mcp import Client, StdioServerParameters  # noqa: E402

from project_seed.mcp_server import create_server  # noqa: E402
from project_seed.validation import fixture  # noqa: E402


def test_mcp_schema_and_bound_permissions(runtime, context):
    async def exercise():
        server = create_server(runtime, replace(context, origin="model"))
        async with Client(server) as client:
            tools = await client.list_tools()
            tool = next(tool for tool in tools.tools if tool.name == "seed_activate")
            assert set(tool.input_schema["properties"]) == {"seed_id", "project_id"}
            assert tool.annotations.read_only_hint is True
            result = await client.call_tool(
                "seed_activate", {"seed_id": "project.restore", "project_id": "demo"}
            )
            assert result.structured_content["status"] == "ok"
            denied = await client.call_tool(
                "seed_activate", {"seed_id": "project.restore", "project_id": "private"}
            )
            assert denied.structured_content["reason"] == "project_not_allowed"
            assert denied.structured_content["data"] is None

    asyncio.run(exercise())


def test_mcp_cannot_override_host_consent(runtime, context):
    async def exercise():
        server = create_server(runtime, replace(context, consent=False, origin="model"))
        async with Client(server) as client:
            result = await client.call_tool(
                "seed_activate",
                {"seed_id": "project.restore", "project_id": "demo", "consent": True},
            )
            # SDK may reject the extra key; it must never gain access either way.
            assert result.is_error or result.structured_content["reason"] == "consent_required"

    asyncio.run(exercise())


def test_real_stdio_roundtrip(tmp_path):
    registry, memory = tmp_path / "registry.json", tmp_path / "memory.json"
    registry.write_text(json.dumps(fixture("registry")))
    memory.write_text(json.dumps(fixture("memory")))

    async def exercise():
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "project_seed.mcp_server",
                "--registry",
                str(registry),
                "--memory",
                str(memory),
                "--principal",
                "stdio-test",
                "--allow-project",
                "demo",
                "--allow-memory-read",
                "--consent",
            ],
        )
        async with Client(parameters, read_timeout_seconds=15) as client:
            result = await client.call_tool(
                "seed_activate", {"seed_id": "project.restore", "project_id": "demo"}
            )
            assert result.structured_content["reason"] == "retrieved"

    asyncio.run(exercise())
