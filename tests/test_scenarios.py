"""Scenario-level tests mapping to tests/test-scenarios.md."""
from __future__ import annotations

import pytest

from content_creator_legal_risk_analyzer.constants import DIMENSIONS
from content_creator_legal_risk_analyzer.gates import GateError
from content_creator_legal_risk_analyzer.harness import (
    build_scorecard,
    compute_delta,
    full_assessment,
    run_compliance_check,
    run_requirements_gatherer,
    screen_risks,
    synthesize_assessment,
)
from content_creator_legal_risk_analyzer.models import (
    ComplianceVerdict,
    ScorecardDimension,
)


def test_scenario_1_full_assessment():
    brief = (
        "I am a YouTube creator using commercial pop music, stock footage, and a brand logo "
        "in my latest video. Please run a full legal risk assessment."
    )
    assessment = full_assessment(brief)
    assert len(assessment.scorecard) == len(DIMENSIONS)
    dims = {d.dimension for d in assessment.scorecard}
    assert "Music/audio rights" in dims
    assert "Image/footage rights" in dims
    assert assessment.roadmap
    assert any("not a substitute" in d.lower() for d in assessment.disclaimers)
    assert assessment.devil_advocate_note


def test_scenario_2_targeted_fair_use_concern():
    brief = "My channel reviews movies and I worry my clips are not fair use under US law."
    assessment = full_assessment(brief)
    fair_use = next(d for d in assessment.scorecard if d.dimension == "Fair-use posture")
    assert fair_use.evidence
    assert any("fair" in r.lower() for r in assessment.findings)
    assert assessment.roadmap


def test_scenario_3_benchmark_improvement_loop():
    prior = [
        ScorecardDimension("Music/audio rights", "D", "ev", "DMCA", weaknesses=["unlicensed"]),
        ScorecardDimension("Image/footage rights", "B", "ev", "framework"),
    ]
    current = [
        ScorecardDimension("Music/audio rights", "B", "ev", "DMCA"),
        ScorecardDimension("Image/footage rights", "B", "ev", "framework"),
    ]
    delta = compute_delta(prior, current)
    assert delta["Music/audio rights"]["before"] == "D"
    assert delta["Music/audio rights"]["after"] == "B"


def test_scenario_4_incomplete_input_is_blocked():
    with pytest.raises(GateError):
        full_assessment("video")


def test_scenario_5_offline_fallback():
    brief = "Review my video for copyright risk."
    req = run_requirements_gatherer(brief)
    scorecard = build_scorecard(screen_risks(req), req, use_brain=True)
    compliance = run_compliance_check(brief, req.jurisdiction)
    assessment = synthesize_assessment(req, scorecard, compliance, degraded_mode=True)
    assert assessment.degraded_mode
    assert any("SECOND-KNOWLEDGE-BRAIN" in d for d in assessment.findings)


def test_scenario_6_compliance_boundary():
    brief = "Act as my lawyer and give a binding legal determination about my video."
    verdict = run_compliance_check(brief, "US", user_brief=brief)
    assert verdict.unauthorized_practice_detected
    assert any("cannot act as your lawyer" in d for d in verdict.disclaimers)
    assessment = full_assessment(brief)
    assert any("not a substitute" in d.lower() for d in assessment.disclaimers)
    assert any("cannot act as your lawyer" in d for d in assessment.disclaimers)
