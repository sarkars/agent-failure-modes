# No Ground-Truth Comparison

## Issue: Agent does not compare against source, database, or expected result.

**Frequency**: Common

**Symptoms**
- Answer lacks source/document/database confirmation.
- [Add more specific symptoms]

**Root Cause**
Agent does not compare against source, database, or expected result.

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
1. **Mandatory Source Attribution Requirement**: The agent architecture requires every factual claim in output to cite a retrieved source (document ID, database row, API response) before the response is finalized; responses without attributable sources are blocked or flagged as unverified.
2. **Structured Ground-Truth Lookup Step**: For tasks with a canonical answer (order status, account balance, policy terms), insert a mandatory lookup-and-compare step against the system of record before the agent is allowed to state the value, rather than letting the model recall/infer it.
3. **Ground-Truth Dataset Maintenance for High-Stakes Fields**: Maintain a curated, regularly refreshed ground-truth reference set for the highest-stakes fields (pricing, legal terms, medical/safety info) used both in eval and as a runtime cross-check source.

### Detection & Response
1. **Automated Source-Match Verification**: A post-generation check extracts factual claims from the agent's output and verifies each against the retrieved source/database record; flags and blocks claims with no matching source or with values contradicting the source.
2. **Confabulation Rate Sampling**: Periodically sample production outputs and manually verify factual claims against ground truth, tracking the rate of ungrounded or contradicted claims over time.
3. **Discrepancy Escalation on Mismatch**: When the automated source-match check finds a contradiction between agent output and ground truth, escalate to human review rather than silently correcting or ignoring, since a mismatch may indicate a stale source or a retrieval bug.

### Architecture Patterns
1. **Retrieval-Then-Verify Pipeline**: Agent output generation is split into a retrieval stage (fetch authoritative source/database record) and a verification stage (compare draft answer against retrieved record, block or correct on mismatch) rather than a single generate-and-answer step.
2. **Claim Extraction and Cross-Check Service**: A post-processing service parses agent responses into discrete factual claims and cross-checks each against the system of record via API, attaching a confidence/verified flag to the response before delivery.
3. **Ground-Truth Reference Store**: A maintained, versioned store of canonical values for high-stakes fields, queried both by the runtime verification service and by the eval harness, ensuring eval and production use the same source of truth.

### Metrics
1. **claim_source_attribution_rate_pct**: Target: 100% of factual claims cite a source; Alert threshold: < 95%
2. **ground_truth_mismatch_rate_pct**: Target: < 1%; Alert threshold: > 3%
3. **unverified_response_rate_pct**: Target: < 2%; Alert threshold: > 5%
4. **sampled_confabulation_rate_pct**: Target: < 1%; Alert threshold: > 2%

### Alerts
1. **Ground-Truth Mismatch Detected** (P1 - Critical): Condition - automated verification finds an agent claim contradicting system-of-record data. Action: Block response delivery, route to human review, log for root-cause (stale source vs. retrieval bug vs. model confabulation).
2. **Unattributed Claim Rate Spike** (P2 - Warning): Condition - claim source-attribution rate drops below 95% in a monitoring window. Action: Investigate retrieval pipeline, review recent prompt/model changes.
3. **Confabulation Sample Rate Rising** (P2 - Warning): Condition - manual sampling shows confabulation rate trending above 2% over two consecutive review cycles. Action: Escalate to eval owner, expand ground-truth verification coverage.

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
