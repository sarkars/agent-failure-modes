# Conflicting Source Failure

## Issue: Agent fails to reconcile contradictions between sources.

**Frequency**: Common

**Symptoms**
- Two cited docs disagree; no resolution.
- [Add more specific symptoms]

**Root Cause**
Agent fails to reconcile contradictions between sources.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Source Authority Hierarchy**: Define authoritative sources per domain (official_policy > blog_posts > forums > user_submissions). Prioritize high-authority sources; surface lower-authority sources with disclaimers. Example: 'Source A (official): X. Source B (blog): Y'.
2. **Conflict Detection & Flagging**: When retrieving contradictory information, explicitly mark conflict in response. Example: 'Source A says X, but Source B says Y. Source A is more authoritative.' Let user see all positions with authority scores.
3. **Source Provenance Tracking**: For each fact, track source document with URL/ID, publication_date, author, authority_level. Enable users to jump to source. Provide metadata about source credibility.

### Detection & Response
1. **Contradiction Detection**: Use NLI (natural language inference) model to detect contradictions in retrieved documents. Flag queries where top-k contain contradictions. Alert on conflict detection.
2. **Source Trustworthiness Scoring**: Track user feedback on sources (marked trustworthy/untrustworthy). Compute source_credibility_score over time. Downrank low-credibility sources in ranking.
3. **Temporal Source Conflict**: Detect version conflicts (old doc says X, new doc says Y). Alert to potential deprecated information. Recommend newest authoritative source.

### Architecture Patterns
1. **Multi-Source Conflict Resolution Layer**: After retrieval, extract claims from each document. Use NLI to identify contradictions. Rank sources by authority. Generate resolution strategy (use highest authority OR surface all sources + confidence).
2. **Source Attribution Metadata**: For each retrieved passage, attach: source_id, source_type, publication_date, authority_score, author. Enable filtering by source type/credibility.
3. **Conflict Report Generation**: When contradictions detected, generate conflict report: each source's position + authority_score + explanation. Enable user to make informed decision.

### Metrics
1. **conflicting_source_detection_rate_percent**: Target: > 90% (when conflicts exist); Alert threshold: < 70%
2. **source_authority_ranking_accuracy_percent**: Target: 95%; Domain experts agree on authority ordering
3. **user_feedback_conflict_resolution_satisfaction_percent**: Target: > 85%; Alert threshold: < 75%
4. **contradictory_claims_in_top_10_results_percent**: Target: < 5%; Alert threshold: > 15%
5. **conflict_disclosure_rate_percent**: Target: 100%; All conflicts must be flagged

### Alerts
1. **Contradictory Sources Detected** (P2 - Warning): Condition - NLI detects contradictions in top-5 results. Action: Surface conflict report to user, suggest authoritative source, escalate if high-priority query.
2. **Authority Rank Violation** (P2 - Warning): Condition - low-authority source ranked higher than high-authority on same topic. Action: Audit ranking model, update authority scores, rerun retrieval.
3. **Temporal Conflict Detected** (P2 - Warning): Condition - outdated source contradicts current source. Action: Surface version conflict, mark outdated source as deprecated, recommend current source.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
