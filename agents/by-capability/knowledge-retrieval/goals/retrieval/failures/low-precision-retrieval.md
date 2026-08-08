# Low-Precision Retrieval

## Issue: Agent retrieves irrelevant chunks and synthesizes wrong answer.

**Frequency**: Occasional

**Symptoms**
- Citations do not support claim.
- Top-ranked results include documents that share keywords with the query but address a different topic entirely.
- Synthesized answer contains a claim that traces back to a semantically similar but factually unrelated chunk.
- Precision@5 drops noticeably below the precision@10 baseline for a specific query category (e.g., short, ambiguous queries).

**Root Cause**
The embedding model conflates surface-level keyword overlap with true semantic relevance, so a chunk that shares vocabulary with the query but addresses an unrelated topic can score as similar as one that actually answers it. With no re-ranking stage running after initial dense retrieval to filter topically-similar-but-irrelevant chunks, and a similarity threshold set permissively enough to let borderline matches into the top-k, irrelevant chunks reach synthesis alongside relevant ones — and because no citation-grounding check verifies a chunk actually supports the specific claim before it's used, the wrong chunk can end up cited as if it did.

**Example**
```
Query: "What's the policy on remote work for contractors?"
Vector search returns high-similarity chunks because "remote," "work," and "contractors"
appear frequently, but several top-5 results come from a "Remote Desktop Access" IT
security doc, not the HR contractor policy. The agent synthesizes an answer blending
VPN/remote-access rules with contractor status, producing a claim about "contractors
needing VPN approval for remote work" that neither source actually states.
```

**Contributing Factors**
- Embedding model conflates surface-level keyword overlap with true semantic relevance (e.g., "remote work" appearing in unrelated contexts).
- No re-ranking stage runs after initial dense retrieval to filter out topically-similar-but-irrelevant chunks.
- Retrieval similarity threshold is set too permissively, letting borderline-relevant chunks into the top-k.
- No citation-grounding check catches that a chunk doesn't actually support the specific claim before it's used in synthesis.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Keyword-overlap false positive | Query with terms that appear in both a relevant doc and an unrelated doc using the same vocabulary | Top results are dominated by the truly relevant document | Top results include the unrelated same-vocabulary document above the relevant one |
| Re-ranker impact | Same query run with and without the LTR re-ranking stage | precision@5 with re-ranker is markedly higher | precision@5 without re-ranker shows irrelevant docs in top positions |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| precision_at_5_percent | > 80% | Sample production queries, have raters mark each top-5 result relevant/irrelevant, compute % relevant |

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
| precision_at_5_percent | < 70% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Precision Degradation | precision_at_5_percent drops below 70% on rolling weekly sample | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
