"""Domain constants for the legal-risk analyzer harness."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRAIN_PATH = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
SKILLS_DIR = ROOT / "skills"
SCHEMAS_DIR = ROOT / "schemas"

FRAMEWORKS = [
    "Copyright fair-use four-factor test (US) / fair dealing",
    "DMCA / platform content-ID frameworks",
    "Creative Commons license matrix",
    "Trademark likelihood-of-confusion factors",
    "Right of publicity / personality rights",
]

DIMENSIONS = [
    "Music/audio rights",
    "Image/footage rights",
    "Fair-use posture",
    "Trademark exposure",
    "Publicity/likeness rights",
    "License compatibility",
    "Platform-policy risk",
    "Disclosure/FTC compliance",
]

SUB_SKILLS = [
    "sub-requirements-gatherer",
    "sub-risk-screener",
    "sub-compliance-check",
    "sub-improvement-roadmap",
]
