"""Static integrity tests for skill markdown and the knowledge base."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from content_creator_legal_risk_analyzer.constants import (
    DIMENSIONS,
    FRAMEWORKS,
    ROOT,
    SUB_SKILLS,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_main_skill_exists_with_frontmatter():
    main = ROOT / "skills" / "main.md"
    assert main.exists()
    text = _read(main)
    assert text.startswith("---")
    assert "name:" in text
    assert "description:" in text


def test_all_sub_skills_exist():
    for slug in SUB_SKILLS:
        path = ROOT / "skills" / f"{slug}.md"
        assert path.exists(), f"missing {path}"
        text = _read(path)
        assert "## Inputs" in text
        assert "## Outputs" in text
        assert "## Quality Gate" in text
        assert "## Tools" in text


def test_main_skill_lists_all_dimensions():
    text = _read(ROOT / "skills" / "main.md")
    for dim in DIMENSIONS:
        assert dim in text, f"dimension '{dim}' not referenced in main.md"


def test_main_skill_invokes_all_sub_skills():
    text = _read(ROOT / "skills" / "main.md")
    for slug in SUB_SKILLS:
        assert slug in text, f"sub-skill '{slug}' not invoked in main.md"


def test_main_skill_cites_all_frameworks():
    text = _read(ROOT / "skills" / "main.md")
    for fw in FRAMEWORKS:
        assert fw in text, f"framework '{fw}' not cited in main.md"


def test_main_skill_has_all_output_sections():
    text = _read(ROOT / "skills" / "main.md")
    for section in [
        "Executive Summary",
        "Scorecard",
        "Detailed Findings",
        "Prioritized Improvement Roadmap",
        "Sources & Frameworks Cited",
        "Disclaimers",
    ]:
        assert section in text, f"output section '{section}' missing"


def test_brain_has_dated_entries_and_hashes():
    brain = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
    assert brain.exists()
    text = _read(brain)
    dates = re.findall(r"### \[(\d{4}-\d{2}-\d{2})\]", text)
    assert dates, "no dated knowledge entries found"
    hashes = re.findall(r"<!--hash:([0-9a-f]{16})-->", text)
    assert hashes, "no dedup hashes found"
    assert len(hashes) == len(set(hashes)), "duplicate hashes in knowledge base"


def test_schemas_are_valid_json():
    import json

    for name in ["scorecard.schema.json", "roadmap.schema.json"]:
        path = ROOT / "schemas" / name
        assert path.exists()
        json.load(path.open("r", encoding="utf-8"))


def test_reuse_map_exists():
    path = ROOT / "cluster" / "legal-compliance" / "REUSE-MAP.md"
    assert path.exists()
    text = _read(path)
    assert "sub-requirements-gatherer" in text
    assert "sub-compliance-check" in text
