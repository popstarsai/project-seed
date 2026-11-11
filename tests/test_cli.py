# SPDX-License-Identifier: Apache-2.0
import json
import subprocess
import sys

import pytest

from project_seed.cli import main
from project_seed.evaluation import evaluate
from project_seed.router import propose
from project_seed.validation import fixture


def test_demo(capsys):
    assert main(["demo"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ok"


def test_evaluation(capsys):
    assert main(["evaluate"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["passed"] == report["total"] == 12


def test_no_claim_of_semantic_routing():
    assert propose("Where did we leave this project?") is None
    assert propose("Unde am ramas cu proiectul?") is None
    assert evaluate()["limitation"].startswith("Regression checks only")


@pytest.mark.parametrize(
    "text", ["\n/seed project.restore demo", " /seed project.restore demo", 123]
)
def test_router_rejects_non_exact_inputs(text):
    assert propose(text) is None


def test_cli_grants_and_validation(tmp_path, capsys):
    registry, memory = tmp_path / "registry.json", tmp_path / "memory.json"
    registry.write_text(json.dumps(fixture("registry")))
    memory.write_text(json.dumps(fixture("memory")))
    files = ["--registry", str(registry), "--memory", str(memory)]
    assert main(["validate", *files]) == 0
    assert json.loads(capsys.readouterr().out) == {"seeds": 1, "projects": 1}
    args = ["run", *files, "--seed", "project.restore", "--project", "demo", "--principal", "local"]
    assert main(args) == 1
    assert json.loads(capsys.readouterr().out)["reason"] == "consent_required"
    assert main([*args, "--consent", "--allow-project", "demo", "--allow-memory-read"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ok"


def test_cli_configuration_error_is_sanitized(tmp_path, capsys):
    path = tmp_path / "private-file-name.json"
    assert main(["validate", "--registry", str(path), "--memory", str(path)]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "private-file-name" not in output.err
    assert json.loads(output.err)["status"] == "error"


def test_module_entrypoint():
    process = subprocess.run(
        [sys.executable, "-m", "project_seed", "demo"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert json.loads(process.stdout)["reason"] == "retrieved"
