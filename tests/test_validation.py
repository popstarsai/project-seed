# SPDX-License-Identifier: Apache-2.0
import json

import pytest

from project_seed.memory import MemoryStore
from project_seed.registry import SeedRegistry
from project_seed.validation import MAX_FILE_BYTES, InvalidData, fixture, load_json, validate


@pytest.mark.parametrize("schema", ["registry", "memory"])
def test_fixtures_match_schema(schema):
    validate(fixture(schema), schema)


@pytest.mark.parametrize("schema", ["registry", "memory"])
def test_unknown_version_is_rejected(schema):
    document = fixture(schema)
    document["schema_version"] = "99"
    with pytest.raises(InvalidData):
        validate(document, schema)


@pytest.mark.parametrize("project_id", ["../secret", "/etc/passwd", "demo\n", "demo\r", "x" * 65])
def test_invalid_project_identifiers(project_id):
    with pytest.raises(InvalidData):
        validate({"seed_id": "project.restore", "project_id": project_id}, "proposal")


def test_manifest_cannot_enable_code_or_remote_urls():
    document = fixture("registry")
    document["seeds"][0]["capability"] = "shell.exec"
    with pytest.raises(InvalidData):
        SeedRegistry(document)
    document = fixture("registry")
    document["seeds"][0]["url"] = "https://example.com/payload"
    with pytest.raises(InvalidData):
        SeedRegistry(document)


def test_duplicate_ids_fail():
    document = fixture("registry")
    document["seeds"].append(document["seeds"][0])
    with pytest.raises(InvalidData):
        SeedRegistry(document)
    document = fixture("memory")
    document["projects"].append(document["projects"][0])
    with pytest.raises(InvalidData):
        MemoryStore(document)


def test_bad_timestamp_fails():
    document = fixture("memory")
    document["projects"][0]["provenance"]["updated_at"] = "yesterday"
    with pytest.raises(InvalidData):
        MemoryStore(document)


def test_snapshot_and_return_values_are_isolated():
    document = fixture("memory")
    store = MemoryStore(document)
    document["projects"][0]["summary"] = "modified"
    result = store.read_project("demo")
    assert result["summary"] != "modified"
    result["summary"] = "changed again"
    assert store.read_project("demo")["summary"] != "changed again"


def test_hash_is_stable_for_equivalent_documents():
    document = fixture("memory")
    reordered = dict(reversed(list(document.items())))
    assert MemoryStore(document).record_digest("demo") == MemoryStore(reordered).record_digest(
        "demo"
    )


def test_unrelated_projects_do_not_affect_returned_digest():
    document = fixture("memory")
    before = MemoryStore(document).record_digest("demo")
    other = fixture("memory")["projects"][0]
    other["project_id"] = "private"
    other["summary"] = "A different synthetic record"
    document["projects"].append(other)
    assert MemoryStore(document).record_digest("demo") == before


@pytest.mark.parametrize(
    ("schema", "collection", "key"),
    [
        ("registry", "seeds", "id"),
        ("registry", "seeds", "version"),
        ("memory", "projects", "project_id"),
    ],
)
def test_registry_and_memory_reject_newline_identifiers(schema, collection, key):
    document = fixture(schema)
    document[collection][0][key] += "\n"
    with pytest.raises(InvalidData):
        validate(document, schema)


def test_record_size_is_bounded():
    document = fixture("memory")
    document["projects"][0]["summary"] = "\u2603" * 6000
    with pytest.raises(InvalidData, match="32 KiB"):
        MemoryStore(document)


@pytest.mark.parametrize("content", ['{"x":1,"x":2}', '{"x":NaN}', "not json", "{" * 2000])
def test_invalid_json_file(tmp_path, content):
    path = tmp_path / "input.json"
    path.write_text(content)
    with pytest.raises(InvalidData):
        load_json(path)


def test_missing_and_oversized_files(tmp_path):
    with pytest.raises(InvalidData):
        load_json(tmp_path / "missing.json")
    path = tmp_path / "large.json"
    path.write_bytes(b" " * (MAX_FILE_BYTES + 1))
    with pytest.raises(InvalidData, match="1 MiB"):
        load_json(path)


def test_load_roundtrip(tmp_path):
    path = tmp_path / "input.json"
    document = fixture("registry")
    path.write_text(json.dumps(document))
    assert load_json(path) == document
