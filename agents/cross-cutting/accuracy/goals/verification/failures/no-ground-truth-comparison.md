# No Ground-Truth Comparison

## Issue: Agent does not compare against source, database, or expected result.

**Frequency**: Common

**Symptoms**
- Answer lacks source/document/database confirmation.
- Agent states specific figures (account balance, order status, policy terms) confidently and fluently even though it never issued a retrieval or lookup call to the system of record for that value.
- Post-hoc manual verification finds a nonzero rate of factual claims that contradict the source data, but no automated check ever caught the discrepancy before delivery.

**Root Cause**
The failure is architectural: the system lets the model answer directly from conversational context or its own memory instead of mandating a retrieval-then-verify step for factual claims, and no automated post-generation check exists to extract those claims and cross-reference them against the retrieved source or database record. High-stakes fields like pricing or balances often have no maintained ground-truth reference store to check against in the first place, and even where one could exist, latency and cost pressure discourage adding an extra verification lookup for every factual statement, so the path of least resistance is to let a fluent, unverified answer through.

**Example**
```
A customer asks a billing agent, "What's my current account balance?" Rather than
querying the billing database, the agent recalls a balance mentioned earlier in the
conversation and restates it, adjusted slightly for a recent payment it assumes was
processed. The stated balance is wrong by $340 -- the payment hadn't actually cleared yet.
No lookup-and-compare step exists in the agent's flow, so nothing catches the discrepancy
before the answer reaches the customer.
```

**Contributing Factors**
- The agent architecture allows the model to answer directly from context/memory instead of mandating a retrieval-then-verify step for factual claims.
- No automated post-generation check exists to extract claims and cross-reference them against the retrieved source or database record.
- High-stakes fields (pricing, balances, legal terms) have no maintained ground-truth reference store to check against at runtime or in eval.
- Latency/cost pressure discourages adding an extra verification lookup call for every factual statement.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Account balance lookup | "What's my current balance?" with a recent pending payment in the system | Agent queries billing database and states the actual current balance | Agent recalls/infers a balance from conversation context without a fresh lookup |
| Stale-context override | User previously stated a value that has since changed in the source system | Agent's answer reflects the current source-of-record value, not the stale context | Agent repeats the outdated value from earlier in the conversation |
| Unsourced claim detection | Agent response containing a specific factual figure | Every factual claim is traceable to a retrieved source/database record | Claim exists in the response with no corresponding source citation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| claim_source_attribution_rate_pct | 100% of factual claims cite a source | Automated post-generation extraction of claims, check for matching source citation |
| ground_truth_mismatch_rate_pct | < 1% | Automated verification comparing agent output against retrieved source/database record |
| sampled_confabulation_rate_pct | < 1% | Manually sample production outputs and verify factual claims against ground truth |

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
| ground_truth_mismatch_rate_pct | > 3% |
| claim_source_attribution_rate_pct | < 95% |
| sampled_confabulation_rate_pct | > 2% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Ground-Truth Mismatch Detected | Automated verification finds an agent claim contradicting system-of-record data | High |
| Unattributed Claim Rate Spike | Claim source-attribution rate drops below 95% in a monitoring window | Medium |
| Confabulation Sample Rate Rising | Manual sampling shows confabulation rate trending above 2% over two consecutive review cycles | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
