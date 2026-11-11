# SPDX-License-Identifier: Apache-2.0
"""Exact-command baseline. This is not a semantic or fine-tuned recognizer."""

import re

_COMMAND = re.compile(r"/seed ([a-z][a-z0-9._-]{0,63}) ([a-z0-9][a-z0-9._-]{0,63})", re.ASCII)


def propose(text: str) -> dict[str, str] | None:
    if not isinstance(text, str) or len(text) > 135:
        return None
    match = _COMMAND.fullmatch(text)
    if match is None:
        return None
    return {"seed_id": match[1], "project_id": match[2]}
