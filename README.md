# Content Creator Legal Risk Analyzer

Flag copyright, licensing, and rights risks in creator content before publishing.

## What it does

This Codex skill turns Claude into an IP and media-law specialist that:

1. Gathers requirements and surfaces unknowns (`sub-requirements-gatherer`).
2. Ranks risks by likelihood ? impact with cited evidence (`sub-risk-screener`).
3. Scores content on 8 dimensions against 5 named, citable frameworks.
4. Generates a prioritized, effort/impact-ranked improvement roadmap (`sub-improvement-roadmap`).
5. Runs a mandatory compliance check with disclaimers and jurisdiction notes (`sub-compliance-check`).

## Repository layout

```
content-creator-legal-risk-analyzer/
??? skills/                      # Markdown skill definitions
?   ??? main.md                  # Harness entry point
?   ??? sub-*.md                 # Sub-skills
??? src/                         # Reference Python implementation
?   ??? content_creator_legal_risk_analyzer/
?       ??? harness.py           # Workflow orchestration
?       ??? gates.py             # Blocking quality gates
?       ??? models.py            # Dataclasses
?       ??? schemas.py           # Schema loader
?       ??? constants.py         # Dimensions, frameworks, sub-skills
??? schemas/                     # Standardized JSON schemas
?   ??? scorecard.schema.json
?   ??? roadmap.schema.json
??? tools/
?   ??? knowledge_updater.py     # Weekly knowledge-base crawler
?   ??? crontab.txt              # Linux/macOS cron schedule
?   ??? schedule-windows.ps1     # Windows Task Scheduler registration
??? tests/                       # Pytest suite + scenario pass/fail log
?   ??? test-scenarios.md
?   ??? TEST-RESULTS.md
?   ??? test_*.py
??? cluster/legal-compliance/REUSE-MAP.md  # Cross-skill reuse map
??? SECOND-KNOWLEDGE-BRAIN.md    # Living knowledge base
??? PROJECT-detail.md            # Technical spec
??? PROJECT-DEVELOPMENT-PHASE-TRACKING.md
??? CLAUDE.md                    # Skill overview
```

## Running the test suite

```powershell
$env:PYTHONPATH = "src"
python -m pytest -v
```

Last run: **27 passed, 0 failed** (2026-06-23).

## Updating the knowledge base

```bash
# Bootstrap with curated seed entries (no network required)
python tools/knowledge_updater.py --seed

# Live weekly crawl (network + optional crawl4ai)
python tools/knowledge_updater.py

# Dry run
python tools/knowledge_updater.py --dry-run
```

Schedule weekly via `tools/crontab.txt` (Linux/macOS) or `tools/schedule-windows.ps1` (Windows, admin).

## Legal disclaimer

This project provides **informational risk analysis only** and is **not a substitute for advice from a licensed attorney** in your jurisdiction.
