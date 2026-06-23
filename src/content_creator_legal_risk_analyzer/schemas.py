"""Load and expose the standardized assessment schemas."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .constants import SCHEMAS_DIR


def load_json_schema(name: str) -> Dict[str, Any]:
    path = SCHEMAS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


SCORECARD_SCHEMA = load_json_schema("scorecard.schema.json")
ROADMAP_SCHEMA = load_json_schema("roadmap.schema.json")

__all__ = ["SCORECARD_SCHEMA", "ROADMAP_SCHEMA", "load_json_schema"]
