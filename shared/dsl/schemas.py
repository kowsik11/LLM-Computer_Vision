from __future__ import annotations

from pydantic.json_schema import models_json_schema

from .models import ActionProgram


def dsl_json_schema() -> dict:
    """Return the JSON Schema for the DSL program."""

    schema, defs = models_json_schema([ActionProgram], ref_template="#/$defs/{model}")
    # Pydantic nests the schema for our root model under definitions; fall back to schema itself.
    root_schema = schema.get("definitions", {}).get("ActionProgram", schema)
    if defs:
        root_schema["$defs"] = defs
    return root_schema
