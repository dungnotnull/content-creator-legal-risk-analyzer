# PROJECT-detail.md — Content Creator Legal Risk Analyzer (copyright, music, images)

## Executive Summary
`content-creator-legal-risk-analyzer` turns Claude into an IP and media-law specialist who advises digital creators on pre-publication risk. It runs a research-first harness that intakes the user's case, binds it to named world-renowned frameworks, scores it on 8 dimensions, and returns a prioritized improvement roadmap with effort/impact. The skill is self-improving: `tools/knowledge_updater.py` continuously refreshes its knowledge base from authoritative sources.

## Problem Statement
Creators unknowingly use copyrighted music, images, footage, or trademarks and face takedowns, demonetization, or lawsuits. They need a pre-publication risk scan with safer alternatives.

## Target Users & Use Cases
- Primary: practitioners and non-experts who need an expert-grade, evidence-based assessment of their content creator legal risk analyzer (copyright, music, images) artifact.
- Trigger examples:
  - User says: "Full assessment" → skill score every dimension with evidence, highlight music/audio rights and image/footage rights findings, deliver a prioritized roadmap
  - User says: "Targeted concern" → skill diagnose the fair-use posture issue against the named framework and return focused, measurable fixes
  - User says: "Benchmark / improvement loop" → skill re-score against the same rubric, show the before/after delta per dimension, and update the roadmap

## Harness Architecture
```
intake/requirements
    │  requirements-gatherer → risk-screener → compliance-check → improvement-roadmap → synthesis
    ▼
[named frameworks] → [multi-dimensional scoring] → [prioritized roadmap] → [quality/compliance gates] → DELIVERABLE
```

## Evaluation Frameworks (world-renowned, citable)
- **Copyright fair-use four-factor test (US) / fair dealing** — Use-permissibility analysis
- **DMCA / platform content-ID frameworks** — Takedown and monetization risk
- **Creative Commons license matrix** — License-compatibility checks
- **Trademark likelihood-of-confusion factors** — Brand-use risk
- **Right of publicity / personality rights** — Likeness-use risk

## Scoring Dimensions
1. Music/audio rights
2. Image/footage rights
3. Fair-use posture
4. Trademark exposure
5. Publicity/likeness rights
6. License compatibility
7. Platform-policy risk
8. Disclosure/FTC compliance

## Full Sub-Skill Catalog
### `sub-requirements-gatherer`
- **Purpose:** Capture objectives, stakeholders, constraints, and the document/artifact under review so analysis is complete.
- **Inputs:** User brief, uploaded documents, clarifying answers
- **Outputs:** Structured requirements pack with scope, stakeholders, and explicit out-of-scope items
- **Tools:** Read, WebSearch
- **Quality gate:** Scope, stakeholders, and success criteria all captured; ambiguities flagged for confirmation.
### `sub-risk-screener`
- **Purpose:** Surface the highest-impact risks early so the analysis and roadmap focus where it matters.
- **Inputs:** Structured requirements / artifact
- **Outputs:** Ranked risk register (likelihood x impact) with the specific evidence for each risk
- **Tools:** Read, WebSearch
- **Quality gate:** Each risk has likelihood, impact, and a cited or quoted evidence anchor.
### `sub-compliance-check`
- **Purpose:** Ensure no output crosses into unauthorized practice or non-compliant claims; attach required disclaimers and jurisdiction notes.
- **Inputs:** Draft deliverable, jurisdiction, domain
- **Outputs:** Compliance verdict, required disclaimers, and a list of any claims that must be softened or removed
- **Tools:** Read, WebSearch, WebFetch
- **Quality gate:** Jurisdiction identified; mandatory disclaimers attached; no statement presented as a substitute for licensed professional advice.
### `sub-improvement-roadmap`
- **Purpose:** Convert weaknesses into a sequenced, effort/impact-ranked action plan the user can execute.
- **Inputs:** Scored weaknesses, user constraints
- **Outputs:** Prioritized roadmap (Quick wins / Major projects / Long-term) with effort, impact, and success metric per item
- **Tools:** Read, Write
- **Quality gate:** Every recommendation has effort, impact, and a measurable success criterion.

## Skill File Format Specification
Each skill file uses YAML frontmatter (`name`, `description`) followed by: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates. `skills/main.md` is the harness entry point and invokes the sub-skills above in order.

## E2E Execution Flow
1. Parse the user request and uploaded artifact(s).
2. Run intake/requirements sub-skill; flag unknowns (no silent assumptions).
3. (No safety gate for this cluster.)
4. Select governing framework(s) and rubric.
5. Score every dimension with cited evidence.
6. Generate the prioritized roadmap (effort/impact + success metric).
7. Run sub-compliance-check; attach disclaimers/jurisdiction notes before output.
8. Synthesize the final professional deliverable; pass all quality gates before display.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: US Copyright Office, Creative Commons, WIPO, Electronic Frontier Foundation
- ArXiv categories: cs.CY
- Search queries: "copyright fair use creator", "content id music licensing", "right of publicity likeness"
- Append format: dated entries with Title, Authors, Year, Venue, DOI/Link, Relevance.

## Supporting Tools Spec
`tools/knowledge_updater.py`: crawl4ai → fetch → parse → score (recency × relevance) → dedupe (URL/DOI hash) → append to `SECOND-KNOWLEDGE-BRAIN.md`. Schedule: weekly cron.

## Quality Gates (must all pass before output)
- Every scored dimension has evidence.
- At least one named framework cited.
- Roadmap items each have effort, impact, and a measurable success metric.
- Compliance check passed with disclaimers attached.

## Test Scenarios
1. **Full assessment** — Input: User submits a complete content creator legal risk analyzer artifact and asks for a full evaluation → Expected: Score every dimension with evidence, highlight music/audio rights and image/footage rights findings, deliver a prioritized roadmap
2. **Targeted concern** — Input: User reports a specific weakness in fair-use posture → Expected: Diagnose the fair-use posture issue against the named framework and return focused, measurable fixes
3. **Benchmark / improvement loop** — Input: User wants to compare a revised version against a prior baseline → Expected: Re-score against the same rubric, show the before/after delta per dimension, and update the roadmap

## Key Design Decisions
1. Scoring is always bound to named, citable frameworks — never ad hoc.
2. Intake forbids silent assumptions; unknowns are surfaced.
3. Roadmap is effort/impact-ranked and measurable.
4. Knowledge base is self-updating for trend alignment.
5. Safety/compliance gating is mandatory and blocking.
