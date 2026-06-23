# Knowledge Updater Tool

`tools/knowledge_updater.py` refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly from authoritative sources and arXiv cs.CY.

## Quick start

```bash
# Bootstrap the knowledge base with curated seed entries (no network crawl)
python tools/knowledge_updater.py --seed

# Live crawl (requires network; optional crawl4ai for richer markdown)
python tools/knowledge_updater.py

# Dry-run a live crawl
python tools/knowledge_updater.py --dry-run
```

## Scheduling

- Linux/macOS: add the line in `tools/crontab.txt` to your crontab.
- Windows: run `tools/schedule-windows.ps1` as Administrator to register a weekly Task Scheduler job.

## Dependencies

- Python 3.10+
- `crawl4ai` (optional; urllib fallback always works)
- See `requirements.txt` and `pyproject.toml`.
