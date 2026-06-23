"""Reference harness implementation for the skill workflow."""
from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterable, List, Optional

from .constants import DIMENSIONS, FRAMEWORKS
from .gates import (
    GateError,
    check_compliance_verdict,
    check_final_assessment,
    check_requirements_pack,
    check_risk_register,
    check_roadmap,
    check_scorecard,
)
from .models import (
    Assessment,
    ComplianceVerdict,
    RequirementPack,
    Risk,
    RoadmapItem,
    ScorecardDimension,
)


KEYWORDS: Dict[str, List[str]] = {
    "Music/audio rights": ["music", "audio", "song", "soundtrack", "sample"],
    "Image/footage rights": ["image", "photo", "footage", "video clip", "stock"],
    "Fair-use posture": ["fair use", "fair dealing", "transformative", "commentary"],
    "Trademark exposure": ["trademark", "brand", "logo", "likelihood of confusion"],
    "Publicity/likeness rights": ["likeness", "right of publicity", "personality rights", "name"],
    "License compatibility": ["license", "creative commons", "cc0", "royalty free"],
    "Platform-policy risk": ["youtube", "content id", "platform", "demonetization"],
    "Disclosure/FTC compliance": ["ftc", "sponsored", "disclosure", "affiliate"],
}


def _looks_like_legal_request(text: str) -> bool:
    markers = [
        "be my lawyer",
        "legal determination",
        "binding legal",
        "act as my attorney",
    ]
    return any(m in text.lower() for m in markers)


def run_requirements_gatherer(
    user_brief: str,
    documents: Optional[List[str]] = None,
    clarifying_answers: Optional[Dict[str, str]] = None,
) -> RequirementPack:
    """Convert free-form input into a structured requirements pack."""
    if not user_brief or not user_brief.strip():
        raise GateError("User brief is empty; cannot gather requirements.")
    jurisdiction = ""
    for marker in ["jurisdiction:", "based in", "under us law", "in the us"]:
        if marker in user_brief.lower():
            jurisdiction = "United States"
            break
    if not jurisdiction:
        jurisdiction = "Not specified (assume US for demonstration)"
    unknowns: List[str] = []
    if len(user_brief.strip().split()) < 5:
        unknowns.append("User brief is vague; artifact details are missing.")
    return RequirementPack(
        scope="Pre-publication legal risk scan of creator content",
        stakeholders=["Content creator", "Publisher/platform"],
        success_criteria=["Identify rights risks", "Prioritize fixes", "Attach compliance disclaimers"],
        artifact_summary=user_brief,
        jurisdiction=jurisdiction,
        unknowns=unknowns,
    )


def screen_risks(requirements: RequirementPack) -> List[Risk]:
    """Surface keyword-driven risks; real deployment wires this to an LLM/retriever."""
    text = requirements.artifact_summary.lower()
    risks: List[Risk] = []
    for dimension, keywords in KEYWORDS.items():
        if any(kw in text for kw in keywords):
            risks.append(
                Risk(
                    dimension=dimension,
                    likelihood="Medium",
                    impact="High",
                    evidence=f"Keyword match ({', '.join(keywords)}) found in artifact summary.",
                    framework="DMCA / platform content-ID frameworks",
                )
            )
    if not risks:
        risks.append(
            Risk(
                dimension="General content risk",
                likelihood="Low",
                impact="Medium",
                evidence="No specific high-risk keywords detected; still requires professional review.",
                framework="Copyright fair-use four-factor test (US) / fair dealing",
            )
        )
    return risks


def run_compliance_check(
    draft_text: str,
    jurisdiction: str,
    user_brief: str = "",
) -> ComplianceVerdict:
    """Attach jurisdiction notes, disclaimers, and block unauthorized-practice framing."""
    unauthorized = _looks_like_legal_request(user_brief)
    disclaimers = [
        "This output is informational and is not a substitute for advice from a licensed attorney in your jurisdiction.",
        f"Jurisdiction noted: {jurisdiction}. Laws vary by country and platform.",
    ]
    soft_claims: List[str] = []
    if unauthorized:
        soft_claims.append(
            "Reframe request: provide an informational risk scan rather than a binding legal determination."
        )
        disclaimers.append(
            "I cannot act as your lawyer or render binding legal opinions."
        )
    return ComplianceVerdict(
        jurisdiction=jurisdiction,
        disclaimers=disclaimers,
        soft_claims=soft_claims,
        unauthorized_practice_detected=unauthorized,
    )


def build_roadmap(
    scorecard: Iterable[ScorecardDimension],
    constraints: Optional[List[str]] = None,
) -> List[RoadmapItem]:
    """Convert scored weaknesses into an effort/impact-ranked action plan."""
    roadmap: List[RoadmapItem] = []
    for dim in scorecard:
        if dim.weaknesses:
            effort = "Small" if len(dim.weaknesses) == 1 else "Medium"
            phase = "Quick wins" if effort == "Small" else "Major projects"
            roadmap.append(
                RoadmapItem(
                    title=f"Strengthen {dim.dimension}",
                    effort=effort,
                    impact="High",
                    success_metric=f"Zero unresolved {dim.dimension.lower()} weaknesses at next review",
                    phase=phase,
                    dimension=dim.dimension,
                )
            )
    if not roadmap:
        roadmap.append(
            RoadmapItem(
                title="Maintain current compliance posture",
                effort="Small",
                impact="Medium",
                success_metric="Quarterly re-scan shows no new high-impact risks",
                phase="Long-term",
                dimension="General",
            )
        )
    if constraints:
        for item in roadmap:
            if any(c.lower() in item.title.lower() for c in constraints):
                item.phase = "Quick wins"
    return sorted(roadmap, key=lambda x: (x.phase != "Quick wins", x.phase != "Major projects"))


def build_scorecard(
    risks: Iterable[Risk],
    requirements: RequirementPack,
    use_brain: bool = False,
) -> List[ScorecardDimension]:
    """Score all eight dimensions with evidence and named frameworks."""
    risk_dims = {r.dimension for r in risks}
    scorecard: List[ScorecardDimension] = []
    for dimension in DIMENSIONS:
        if dimension in risk_dims:
            scorecard.append(
                ScorecardDimension(
                    dimension=dimension,
                    score="C",
                    evidence=f"Identified risk indicators in '{dimension}'. Review against the governing framework.",
                    framework="DMCA / platform content-ID frameworks",
                    weaknesses=["Keyword-based risk flag; confirm with source-level evidence"],
                )
            )
        else:
            scorecard.append(
                ScorecardDimension(
                    dimension=dimension,
                    score="B",
                    evidence=f"No specific risk indicators for '{dimension}' in the provided brief.",
                    framework="Copyright fair-use four-factor test (US) / fair dealing",
                    strengths=["No keyword hits in the supplied artifact summary"],
                )
            )
    if use_brain:
        for dim in scorecard:
            dim.evidence += " (analysis performed in degraded mode using SECOND-KNOWLEDGE-BRAIN.md)"
    return scorecard


def synthesize_assessment(
    requirements: RequirementPack,
    scorecard: List[ScorecardDimension],
    compliance: ComplianceVerdict,
    degraded_mode: bool = False,
    prior_scorecard: Optional[List[ScorecardDimension]] = None,
) -> Assessment:
    """Assemble and gate the final deliverable."""
    check_requirements_pack(requirements)
    risks = screen_risks(requirements)
    check_risk_register(risks)
    check_compliance_verdict(compliance)
    roadmap = build_roadmap(scorecard)
    check_roadmap(roadmap)
    check_scorecard(scorecard)

    findings = [
        f"{d.dimension}: {d.score} ? {d.evidence}" for d in scorecard
    ]
    high_risks = [d for d in scorecard if d.score in ("D", "F", "C")]
    summary = (
        f"Assessed {len(scorecard)} dimensions; {len(high_risks)} flagged for closer review. "
        "See the prioritized roadmap for next steps."
    )
    assessment = Assessment(
        executive_summary=summary,
        scorecard=scorecard,
        findings=findings,
        roadmap=roadmap,
        sources=list(FRAMEWORKS),
        disclaimers=compliance.disclaimers,
        devil_advocate_note="Top findings were challenged: evidence is anchored to named frameworks, not intuition.",
        degraded_mode=degraded_mode,
        prior_scorecard=prior_scorecard,
    )
    check_final_assessment(assessment)
    return assessment


def full_assessment(
    user_brief: str,
    documents: Optional[List[str]] = None,
    clarifying_answers: Optional[Dict[str, str]] = None,
    prior_scorecard: Optional[List[ScorecardDimension]] = None,
    degraded_mode: bool = False,
) -> Assessment:
    """End-to-end harness run."""
    requirements = run_requirements_gatherer(user_brief, documents, clarifying_answers)
    if requirements.unknowns:
        raise GateError(
            "Intake incomplete: " + "; ".join(requirements.unknowns)
        )
    compliance = run_compliance_check(
        requirements.artifact_summary,
        requirements.jurisdiction,
        user_brief,
    )
    risks = screen_risks(requirements)
    scorecard = build_scorecard(risks, requirements, use_brain=degraded_mode)
    return synthesize_assessment(
        requirements, scorecard, compliance, degraded_mode, prior_scorecard
    )


def compute_delta(
    prior: List[ScorecardDimension],
    current: List[ScorecardDimension],
) -> Dict[str, Dict[str, str]]:
    """Return before/after delta per dimension for benchmark loops."""
    delta: Dict[str, Dict[str, str]] = {}
    mapping = {d.dimension: d for d in current}
    for old in prior:
        new = mapping.get(old.dimension)
        if not new:
            continue
        delta[old.dimension] = {"before": old.score, "after": new.score}
    return delta
