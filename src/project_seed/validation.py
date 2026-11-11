# SPDX-License-Identifier: Apache-2.0
"""Bounded JSON loading and shared, packaged JSON Schema contracts."""

import json
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

MAX_FILE_BYTES = 1_048_576


class InvalidData(ValueError):
    """Invalid input; messages deliberately omit document contents."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidData("duplicate JSON object key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise InvalidData("non-finite JSON number")


def load_json(path: str | Path) -> Any:
    try:
        with Path(path).open("rb") as stream:
            content = stream.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            raise InvalidData("JSON document exceeds 1 MiB")
        return json.loads(
            content.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InvalidData("cannot read a valid JSON document") from exc


@lru_cache
def validator(name: str) -> Draft202012Validator:
    if name not in {"registry", "proposal", "memory"}:
        raise ValueError("unknown schema")
    schema = json.loads(files("project_seed").joinpath(f"schemas/{name}.json").read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate(data: Any, schema: str) -> None:
    try:
        validator(schema).validate(data)
    except (ValidationError, RecursionError) as exc:
        raise InvalidData(f"document does not match {schema} schema") from exc


def fixture(name: str) -> dict[str, Any]:
    if name not in {"registry", "memory", "evaluation"}:
        raise ValueError("unknown fixture")
    return json.loads(files("project_seed").joinpath(f"fixtures/{name}.json").read_text())
