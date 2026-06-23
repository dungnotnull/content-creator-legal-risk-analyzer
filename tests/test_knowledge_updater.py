"""Tests for the knowledge updater crawler."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tools import knowledge_updater as ku


def test_relevance_score_favors_recency_and_keywords():
    high = {"title": "copyright fair use creator", "year": date.today().year, "abstract": "", "url": "http://example.com/a"}
    low = {"title": "unrelated topic", "year": 2010, "abstract": "", "url": "http://example.com/b"}
    assert ku.relevance_score(high) > ku.relevance_score(low)


def test_dedup_appends_only_new_entries(tmp_path: Path):
    brain = tmp_path / "BRAIN.md"
    existing_url = "http://example.com/existing"
    brain.write_text(
        f"### [2024-01-01] Old entry\n- Link: {existing_url}\n<!--hash:{ku._hash(existing_url)}-->\n",
        encoding="utf-8",
    )
    new_url = "http://example.com/new"
    entries = [
        {"title": "Existing", "url": existing_url, "authors": "A", "year": 2024, "abstract": "copyright"},
        {"title": "New entry", "url": new_url, "authors": "B", "year": 2024, "abstract": "music licensing"},
    ]
    count = ku.append_entries(entries, brain)
    assert count == 1
    text = brain.read_text(encoding="utf-8")
    assert today_iso() in text
    assert "New entry" in text
    assert "http://example.com/new" in text
    assert "Relevance score:" in text
    assert re_hash_count(text) == 2


def test_dry_run_does_not_write(tmp_path: Path):
    brain = tmp_path / "BRAIN.md"
    entries = [{"title": "T", "url": "http://example.com/t", "authors": "A", "year": 2024, "abstract": "x"}]
    count = ku.append_entries(entries, brain, dry_run=True)
    assert count == 1
    assert not brain.exists()


def test_graceful_degradation_on_network_failure():
    class Boom(Exception):
        pass
    def bad_fetch(url: str) -> str:
        raise Boom("network down")
    original = ku.fetch_url
    ku.fetch_url = bad_fetch
    try:
        entries = ku.fetch_entries(ku.Config())
        assert entries == []
    finally:
        ku.fetch_url = original


def test_seed_entries_have_required_fields():
    for entry in ku.SEED_ENTRIES:
        assert entry["title"]
        assert entry["url"]
        assert entry["authors"]
        assert entry["year"]


def today_iso() -> str:
    return date.today().isoformat()


def re_hash_count(text: str) -> int:
    import re

    return len(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))
