"""Blocking quality gates for the harness."""
from __future__ import annotations

from typing import Iterable

from .constants import DIMENSIONS
from .models import (
    Assessment,
    ComplianceVerdict,
    RequirementPack,
    Risk,
    RoadmapItem,
    ScorecardDimension,
)


class GateError(ValueError):
    """Raised when a blocking quality gate fails."""


def _non_empty(value: str) -> bool:
    return bool(value and value.strip())


def check_requirements_pack(req: RequirementPack) -> bool:
    if not _non_empty(req.scope):
        raise GateError("Requirements pack missing scope.")
    if not req.stakeholders:
        raise GateError("Requirements pack missing stakeholders.")
    if not req.success_criteria:
        raise GateError("Requirements pack missing success criteria.")
    return True


def check_risk_register(risks: Iterable[Risk]) -> bool:
    risks = list(risks)
    if not risks:
        raise GateError("Risk register is empty.")
    for risk in risks:
        if not _non_empty(risk.likelihood):
            raise GateError(f"Risk '{risk.dimension}' missing likelihood.")
        if not _non_empty(risk.impact):
            raise GateError(f"Risk '{risk.dimension}' missing impact.")
        if not _non_empty(risk.evidence):
            raise GateError(f"Risk '{risk.dimension}' missing evidence anchor.")
    return True


def check_compliance_verdict(verdict: ComplianceVerdict) -> bool:
    if not _non_empty(verdict.jurisdiction):
        raise GateError("Compliance verdict missing jurisdiction.")
    if not verdict.disclaimers:
        raise GateError("Compliance verdict missing disclaimers.")
    professional = any(
        "not a substitute" in d.lower() or "licensed professional" in d.lower()
        for d in verdict.disclaimers
    )
    if verdict.unauthorized_practice_detected and not professional:
        raise GateError(
            "Unauthorized-practice framing detected but no professional-advice disclaimer."
        )
    return True


def check_roadmap(roadmap: Iterable[RoadmapItem]) -> bool:
    roadmap = list(roadmap)
    if not roadmap:
        raise GateError("Roadmap is empty.")
    for item in roadmap:
        if not _non_empty(item.effort):
            raise GateError(f"Roadmap item '{item.title}' missing effort.")
        if not _non_empty(item.impact):
            raise GateError(f"Roadmap item '{item.title}' missing impact.")
        if not _non_empty(item.success_metric):
            raise GateError(f"Roadmap item '{item.title}' missing measurable success metric.")
    return True


def check_scorecard(scorecard: Iterable[ScorecardDimension]) -> bool:
    scorecard = list(scorecard)
    scored_dims = {d.dimension for d in scorecard}
    missing = set(DIMENSIONS) - scored_dims
    if missing:
        raise GateError(f"Scorecard missing dimensions: {sorted(missing)}")
    for dim in scorecard:
        if not _non_empty(dim.evidence):
            raise GateError(f"Dimension '{dim.dimension}' missing evidence.")
        if not _non_empty(dim.framework):
            raise GateError(f"Dimension '{dim.dimension}' missing named framework.")
    return True


def check_final_assessment(assessment: Assessment) -> bool:
    check_scorecard(assessment.scorecard)
    check_roadmap(assessment.roadmap)
    if not assessment.disclaimers:
        raise GateError("Final assessment missing disclaimers.")
    if not any(
        "not a substitute" in d.lower() or "licensed professional" in d.lower()
        for d in assessment.disclaimers
    ):
        raise GateError("Final assessment missing professional-advice disclaimer.")
    if not _non_empty(assessment.devil_advocate_note):
        raise GateError("Final assessment missing devil's-advocate pass.")
    return True
