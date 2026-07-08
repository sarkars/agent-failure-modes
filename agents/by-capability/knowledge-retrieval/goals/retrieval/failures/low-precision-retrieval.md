# Low-Precision Retrieval

## Issue: Agent retrieves irrelevant chunks and synthesizes wrong answer.

**Frequency**: Occasional

**Symptoms**
- Citations do not support claim.
- [Add more specific symptoms]

**Root Cause**
Agent retrieves irrelevant chunks and synthesizes wrong answer.

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
1. **Learning-to-Rank Re-Ranker**: After initial retrieval (recall-focused), apply ML re-ranking model to sort results by relevance. Train on query-document-relevance tuples from user feedback/annotations. Re-ranker produces relevance_score for each result; filter out low-scoring irrelevant chunks.
2. **Citation Support Verification**: Before synthesizing answer, verify each claim has supporting citation. Validate that cited chunk actually contains the claim. Block claims lacking citation support. Example: if claim='CEO announced X', verify cited document contains 'CEO announced X'.
3. **Semantic Coherence Check**: Compute semantic similarity between query and each retrieved chunk. Filter chunks below similarity threshold (e.g., < 0.6). Only use high-similarity chunks for synthesis.

### Detection & Response
1. **Precision@k Monitoring**: Track precision@5, precision@10, precision@20 metrics in production. Estimate via user feedback (marked relevant/irrelevant). Alert if precision drops > 10% month-over-month.
2. **Citation Verification Audit**: Periodically audit synthesized answers. Verify each claim has supporting citation in retrieved chunks. Track: citation_accuracy_rate. Alert if < 95%.
3. **Irrelevant Result Clustering**: When user marks result irrelevant, analyze characteristics. Cluster irrelevant results to identify systematic false positive patterns (e.g., 'all metaphor-based documents marked irrelevant').

### Architecture Patterns
1. **Multi-Stage Ranking Funnel**: Stage 1 (recall): broad vector search. Stage 2 (precision): re-rank with LTR model. Stage 3 (quality): LLM verification that top-k chunks support synthesis. Only use Stage 3 approved chunks.
2. **Feature Engineering for Ranking**: For each query-document pair, compute features: semantic_similarity, keyword_overlap, freshness, click_count, user_feedback_score. Feed to LTR model for ranking.
3. **Citation Grounding Layer**: Before synthesis, extract claims from synthesis. For each claim, find supporting citations in retrieved chunks. Only include claims with matched citations. Block ungrounded claims.

### Metrics
1. **precision_at_5_percent**: Target: > 80%; Alert threshold: < 70%
2. **precision_at_10_percent**: Target: > 75%; Alert threshold: < 65%
3. **citation_accuracy_rate_percent**: Target: > 95%; Claims have supporting citations
4. **irrelevant_in_top_10_rate_percent**: Target: < 15%; Alert threshold: > 25%
5. **ltr_model_ndcg_score**: Target: > 0.85; Measure ranking quality

### Alerts
1. **Precision Degradation** (P1 - Critical): Condition - precision@10 drops > 15% month-over-month. Action: Audit LTR model, check feature quality, potential retraining, ranking parameter tuning.
2. **High Irrelevant Result Rate** (P2 - Warning): Condition - > 25% of top-10 results marked irrelevant. Action: LTR model debugging, feature analysis, training data quality review.
3. **Citation Grounding Failure** (P1 - Critical): Condition - claim synthesized without supporting citation in retrieved chunks. Action: Block answer, escalate, audit synthesis logic, rerun retrieval.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
