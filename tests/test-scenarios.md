# Test Scenarios — Content Creator Legal Risk Analyzer (copyright, music, images)

These scenarios validate the harness, scoring, gates, and graceful degradation. Minimum 5; adversarial and edge cases included.

## Scenario 1: Full assessment
- **Input:** User submits a complete content creator legal risk analyzer artifact and asks for a full evaluation
- **Expected behavior:** Score every dimension with evidence, highlight music/audio rights and image/footage rights findings, deliver a prioritized roadmap
- **Frameworks expected in output:** Copyright fair-use four-factor test (US) / fair dealing, DMCA / platform content-ID frameworks
- **Quality gates checked:** every dimension scored with evidence; roadmap items measurable. Compliance disclaimers attached.
- **Pass criteria:** output contains a scorecard, evidence per dimension, and a prioritized roadmap; no silent assumptions.
## Scenario 2: Targeted concern
- **Input:** User reports a specific weakness in fair-use posture
- **Expected behavior:** Diagnose the fair-use posture issue against the named framework and return focused, measurable fixes
- **Frameworks expected in output:** Copyright fair-use four-factor test (US) / fair dealing, DMCA / platform content-ID frameworks
- **Quality gates checked:** every dimension scored with evidence; roadmap items measurable. Compliance disclaimers attached.
- **Pass criteria:** output contains a scorecard, evidence per dimension, and a prioritized roadmap; no silent assumptions.
## Scenario 3: Benchmark / improvement loop
- **Input:** User wants to compare a revised version against a prior baseline
- **Expected behavior:** Re-score against the same rubric, show the before/after delta per dimension, and update the roadmap
- **Frameworks expected in output:** Copyright fair-use four-factor test (US) / fair dealing, DMCA / platform content-ID frameworks
- **Quality gates checked:** every dimension scored with evidence; roadmap items measurable. Compliance disclaimers attached.
- **Pass criteria:** output contains a scorecard, evidence per dimension, and a prioritized roadmap; no silent assumptions.

## Scenario 4: Incomplete input (edge case)
- **Input:** User provides only a vague one-line description with no artifact.
- **Expected behavior:** Intake sub-skill flags missing mandatory fields and asks targeted clarifying questions instead of fabricating a score.
- **Pass criteria:** No score is produced from assumptions; unknowns are explicitly listed.

## Scenario 5: Offline / sources unavailable (graceful degradation)
- **Input:** A normal request, but WebSearch/WebFetch are unavailable.
- **Expected behavior:** Skill falls back to SECOND-KNOWLEDGE-BRAIN.md and clearly states the limitation and reduced confidence.
- **Pass criteria:** Output explicitly signals the degraded mode and still cites internal frameworks.

## Scenario 6: Compliance boundary
- **Input:** User asks the skill to act as their lawyer / make a binding legal determination.
- **Expected behavior:** `sub-compliance-check` blocks unauthorized-practice framing, attaches disclaimers, and reframes output as informational.
- **Pass criteria:** Output carries jurisdiction notes and a non-substitute-for-professional-advice disclaimer.
