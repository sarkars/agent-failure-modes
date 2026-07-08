# Citation Mismatch

## Issue: Agent cites a source that does not support the claim.

**Frequency**: Common

**Symptoms**
- Claim-source entailment check fails.
- [Add more specific symptoms]

**Root Cause**
Agent cites a source that does not support the claim.

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
1. **Citation Grounding Verifier**: Before finalizing answer, verify each claim has supporting citation in retrieved chunks. Use NLI (natural language inference) model to check entailment: does citation actually support claim? Block unsupported claims or flag with low-confidence warning.
2. **Quote-Grounding Eval**: Build eval dataset with claim-citation pairs. Score: does citation contain exact match or paraphrase of claim? Measure citation_accuracy. Target: > 98% of claims properly grounded.
3. **Citation Requirement Enforcement**: Set policy: all factual claims must have citations. Synthesis system enforces: claim generated → search retrieved_chunks for matching quote → include cite or mark low-confidence → display to user.

### Detection & Response
1. **Claim-Citation Entailment Check**: After synthesis, extract claims. For each claim, verify matching citation in retrieved_chunks. Use NLI model to check entailment. Alert on mismatches.
2. **User Feedback on Citations**: Track user feedback on citations ('citation supports claim', 'citation doesn't match'). Compute citation_accuracy from feedback. Alert if accuracy < 95%.
3. **Citation Audit Sampling**: Periodically audit synthesized answers (weekly sample 100). Verify citations genuinely support claims. Domain experts rate. Track accuracy by agent/model.

### Architecture Patterns
1. **Citation Extraction and Verification Layer**: After synthesis, automatically extract claims and verify citations. For each claim: search_retrieved_chunks for supporting quote → validate entailment → include citation with confidence_score or mark ungrounded.
2. **NLI-Based Entailment Checking**: Use entailment model to score: does_citation_entail_claim? Scores < 0.7 require human review before answering. Scores 0.7-0.9 include confidence warning. Scores > 0.9 confident.
3. **Citation Confidence Scoring**: For each citation, compute confidence based on: exact_match_score, semantic_similarity, entailment_score. Display confidence alongside citation.

### Metrics
1. **citation_accuracy_percent**: Target: > 98%; Alert threshold: < 95%; % claims properly cited
2. **unsupported_claim_rate_percent**: Target: 0%; Alert threshold: > 0.5%; Claims with no supporting citation
3. **citation_entailment_score_avg**: Target: > 0.85; Alert threshold: < 0.75
4. **user_feedback_citation_accuracy_percent**: Target: > 95%; Users confirm citations support claims
5. **citation_audit_agreement_percent**: Target: > 95%; Expert auditors agree claims are supported

### Alerts
1. **Unsupported Claim Detected** (P1 - Critical): Condition - claim synthesized without supporting citation in chunks. Action: Block answer, escalate, flag for human synthesis, investigate retrieval quality.
2. **Low Citation Entailment** (P2 - Warning): Condition - claim-citation entailment score < 0.65. Action: Add low-confidence warning, mark for human review, potential answer regeneration.
3. **Citation Accuracy Degradation** (P1 - Critical): Condition - citation_accuracy drops > 10% month-over-month. Action: Investigate synthesis model, review retrieved chunks quality, potential model retraining.

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
