# CLAUDE.md — Content Creator Legal Risk Analyzer (copyright, music, images)

**Skill name:** `content-creator-legal-risk-analyzer`
**Tagline:** Flag copyright, licensing, and rights risks in creator content before publishing.
**Source idea:** #98 (cluster: `legal-compliance`)
**Current phase:** Phase 5 — Integration & Cross-Skill Wiring (complete)

## Problem This Skill Solves
Creators unknowingly use copyrighted music, images, footage, or trademarks and face takedowns, demonetization, or lawsuits. They need a pre-publication risk scan with safer alternatives.

## Harness Flow Summary
1. **sub-requirements-gatherer** → Capture objectives, stakeholders, constraints, and the document/artifact under review so analysis is complete.
2. **sub-risk-screener** → Surface the highest-impact risks early so the analysis and roadmap focus where it matters.
3. **sub-compliance-check** → Ensure no output crosses into unauthorized practice or non-compliant claims; attach required disclaimers and jurisdiction notes.
4. **sub-improvement-roadmap** → Convert weaknesses into a sequenced, effort/impact-ranked action plan the user can execute.
5. **main (synthesis)** → assemble the scored deliverable + prioritized roadmap and run final quality gates.

## Gates
**Compliance gate:** `sub-compliance-check` MUST run before the final deliverable is emitted. Attach jurisdiction notes and required disclaimers; never present output as a substitute for licensed professional advice.

## Sub-skills
- `skills/sub-requirements-gatherer.md` — Elicit and structure the full set of content asset inventory requirements and context.
- `skills/sub-risk-screener.md` — Identify and rank IP-infringement risks and red-flag clauses/conditions.
- `skills/sub-compliance-check.md` — Verify the deliverable against applicable laws, standards, and disclosure rules.
- `skills/sub-improvement-roadmap.md` — Prioritized improvement roadmap for the risk-mitigation with effort/impact.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources
- [US Copyright Office](https://www.copyright.gov)
- [Creative Commons](https://creativecommons.org)
- [WIPO](https://www.wipo.int)
- [Electronic Frontier Foundation](https://www.eff.org)

ArXiv / research categories crawled: cs.CY

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly from the sources above.
- `src/content_creator_legal_risk_analyzer/harness.py` — reference Python implementation of the scoring/roadmap/gate workflow.
- `schemas/scorecard.schema.json` & `schemas/roadmap.schema.json` — standardized cluster output schemas.

## Active Development Tasks
- [x] Scaffold deliverables and sub-skills
- [x] Define scoring dimensions against named frameworks
- [x] Expand `SECOND-KNOWLEDGE-BRAIN.md` with first crawl batch
- [x] Add 3 more adversarial test scenarios
- [x] Wire shared cluster sub-skills for reuse

## Reference Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — living domain knowledge base
- `cluster/legal-compliance/REUSE-MAP.md` — cross-skill reuse map
