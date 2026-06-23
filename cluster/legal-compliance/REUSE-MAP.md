# Legal-Compliance Cluster Reuse Map

This skill (`content-creator-legal-risk-analyzer`) belongs to the `legal-compliance` cluster. The sub-skills and schemas below are shared with sibling skills in the cluster.

## Shared sub-skills

| Sub-skill | Reused by sibling skills | Why it is reusable |
|-----------|--------------------------|--------------------|
| `sub-requirements-gatherer` | `ad-copy-legal-checker`, `platform-terms-analyzer`, `influencer-disclosure-checker` | Every compliance skill needs structured intake: scope, stakeholders, success criteria, and explicit unknowns. |
| `sub-risk-screener` | `trademark-risk-screener`, `privacy-policy-checker`, `gdpr-privacy-checker` | Ranking risks by likelihood ? impact with cited evidence is cluster-agnostic. |
| `sub-compliance-check` | All `legal-compliance` sibling skills | Mandatory jurisdiction notes and "not a substitute for licensed professional advice" disclaimers are universal. |
| `sub-improvement-roadmap` | `accessibility-audit`, `gdpr-privacy-checker`, `terms-of-service-summarizer` | Effort/impact-ranked, measurable remediation plans are useful across domains. |

## Standardized output schemas

All cluster skills emit deliverables that validate against:

- `schemas/scorecard.schema.json` ? eight-dimension scorecard with evidence and named framework.
- `schemas/roadmap.schema.json` ? prioritized roadmap items with effort, impact, and success metric.

## Integration pattern

1. Sibling skills invoke the shared sub-skills by name.
2. The main harness enforces the shared gates from `src/content_creator_legal_risk_analyzer/gates.py`.
3. Final output is serialized to match the cluster JSON schemas for downstream tooling.
