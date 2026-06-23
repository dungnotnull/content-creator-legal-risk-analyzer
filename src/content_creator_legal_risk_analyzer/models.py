"""Dataclasses for the legal-risk analysis harness."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RequirementPack:
    """Structured intake output handed between sub-skills."""
    scope: str
    stakeholders: List[str]
    success_criteria: List[str]
    artifact_summary: str = ""
    jurisdiction: str = ""
    out_of_scope: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)


@dataclass
class Risk:
    """A single ranked risk from the risk-screener."""
    dimension: str
    likelihood: str
    impact: str
    evidence: str
    framework: str


@dataclass
class ScorecardDimension:
    """One of the eight scored dimensions."""
    dimension: str
    score: str
    evidence: str
    framework: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


@dataclass
class RoadmapItem:
    """Prioritized, measurable remediation action."""
    title: str
    effort: str
    impact: str
    success_metric: str
    phase: str
    dimension: str


@dataclass
class ComplianceVerdict:
    """Mandatory compliance gate result."""
    jurisdiction: str
    disclaimers: List[str]
    soft_claims: List[str] = field(default_factory=list)
    unauthorized_practice_detected: bool = False


@dataclass
class Assessment:
    """Final deliverable after all gates pass."""
    executive_summary: str
    scorecard: List[ScorecardDimension]
    findings: List[str]
    roadmap: List[RoadmapItem]
    sources: List[str]
    disclaimers: List[str]
    devil_advocate_note: str
    degraded_mode: bool = False
    prior_scorecard: Optional[List[ScorecardDimension]] = None
