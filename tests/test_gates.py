"""Unit tests for the blocking quality gates."""
from __future__ import annotations

import pytest

from content_creator_legal_risk_analyzer.constants import DIMENSIONS
from content_creator_legal_risk_analyzer.gates import (
    GateError,
    check_compliance_verdict,
    check_final_assessment,
    check_requirements_pack,
    check_risk_register,
    check_roadmap,
    check_scorecard,
)
from content_creator_legal_risk_analyzer.models import (
    Assessment,
    ComplianceVerdict,
    RequirementPack,
    Risk,
    RoadmapItem,
    ScorecardDimension,
)


def test_requirements_gate_passes_when_complete():
    req = RequirementPack(
        scope="Risk scan",
        stakeholders=["Creator"],
        success_criteria=["Score all dimensions"],
    )
    assert check_requirements_pack(req) is True


def test_requirements_gate_fails_when_incomplete():
    with pytest.raises(GateError):
        check_requirements_pack(
            RequirementPack(scope="", stakeholders=[], success_criteria=["x"])
        )


def test_risk_gate_fails_when_evidence_missing():
    risks = [Risk(dimension="Music", likelihood="High", impact="High", evidence="", framework="DMCA")]
    with pytest.raises(GateError):
        check_risk_register(risks)


def test_compliance_gate_blocks_unauthorized_practice():
    verdict = ComplianceVerdict(
        jurisdiction="US",
        disclaimers=["This is informational."],
        unauthorized_practice_detected=True,
    )
    with pytest.raises(GateError):
        check_compliance_verdict(verdict)


def test_roadmap_gate_checks_success_metric():
    items = [RoadmapItem("Fix music", "Small", "High", "", "Quick wins", "Music/audio rights")]
    with pytest.raises(GateError):
        check_roadmap(items)


def test_scorecard_gate_requires_all_dimensions():
    scorecard = [
        ScorecardDimension(dim, "B", "evidence", "framework")
        for dim in DIMENSIONS[:-1]
    ]
    with pytest.raises(GateError) as exc:
        check_scorecard(scorecard)
    assert DIMENSIONS[-1] in str(exc.value)


def test_final_assessment_gate_requires_disclaimer_and_devils_advocate():
    scorecard = [
        ScorecardDimension(dim, "B", "evidence", "framework")
        for dim in DIMENSIONS
    ]
    roadmap = [RoadmapItem("x", "Small", "High", "metric", "Quick wins", "General")]
    bad = Assessment(
        executive_summary="s",
        scorecard=scorecard,
        findings=[],
        roadmap=roadmap,
        sources=[],
        disclaimers=[],
        devil_advocate_note="",
    )
    with pytest.raises(GateError):
        check_final_assessment(bad)
