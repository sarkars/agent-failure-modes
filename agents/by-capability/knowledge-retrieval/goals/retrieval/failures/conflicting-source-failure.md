# Conflicting Source Failure

## Issue: Agent fails to reconcile contradictions between sources.

**Frequency**: Common

**Symptoms**
- Two cited docs disagree; no resolution.
- Answer presents one contradictory value as fact without flagging that a second, differing source was also retrieved.
- Agent selects whichever source ranked highest on similarity, ignoring publication date or authority level of the sources.
- Agent blends contradictory numbers into an averaged or invented middle value that appears in neither source.

**Root Cause**
Agent fails to reconcile contradictions between sources.

**Example**
```
Query: "What is the maximum expense reimbursement for client dinners?"
Retrieved set contains the 2022 Travel & Expense Policy (states $75/person) and a 2024
Finance FAQ page (states $100/person, which supersedes the 2022 policy but doesn't say
so explicitly). The agent's answer says "$75 per person," citing the 2022 policy, because
that chunk ranked higher on vector similarity — even though the FAQ page is the current
authoritative source and directly contradicts it.
```

**Contributing Factors**
- Retrieval ranks by semantic similarity only, with no signal for document recency or source authority.
- No NLI/contradiction-detection step runs over the retrieved set before synthesis.
- Documents lack machine-readable supersession metadata (no "replaces doc X" or effective-date field) tying newer sources to the ones they override.
- Synthesis prompt instructs the model to "answer using the retrieved context" without requiring it to check for and surface conflicts between sources.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Two contradictory values, no flag | Two retrieved docs give different numeric answers to the same question, one older, one newer | Answer surfaces both values and states which is authoritative/current | Answer presents only one value with no acknowledgment of the conflict |
| Authority ignored | Retrieved set contains an official policy doc and a lower-authority forum/blog post with a different answer | Answer defers to the official policy source | Answer uses the blog/forum value, or blends both |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| conflicting_source_detection_rate_percent | > 90% | Run eval set of queries with known contradictory retrieved docs; measure % where the answer explicitly flags the conflict |

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
| conflicting_source_detection_rate_percent | < 70% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Conflict Surfacing Rate Drop | conflicting_source_detection_rate_percent falls below 70% on weekly eval run | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
