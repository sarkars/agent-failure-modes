# Retrieval Confidence Miscalibration

## Issue
A retrieval system's relevance or similarity score (cosine similarity, a reranker's confidence output, a hybrid search's combined score) is meant to signal how useful a retrieved memory will be for the current query, but in practice that score frequently doesn't correlate well with actual usefulness — a high-scoring result can be topically similar but practically useless (a near-duplicate that adds nothing new, an outdated version of a fact), while a lower-scoring result can be exactly the piece of context the agent needs. Agents that treat the raw score as a trustworthy confidence signal — using it to decide what to include, how much to trust a fact, or whether to ask a clarifying question — inherit whatever miscalibration the scoring function has, often without any indication that the score wasn't dependable.

**Frequency**: Common

**Symptoms**
- Highest-scored retrieval result is not the one the agent actually needed to answer correctly
- Agent expresses unwarranted confidence in a fact because it came from a "high similarity" match, when the match was topically close but substantively wrong or outdated
- A correct, load-bearing memory scores below the retrieval cutoff and never reaches the agent
- Score distributions cluster tightly (e.g. 0.79-0.84) across results of very different actual usefulness, giving the ranking little real discriminative power
- Downstream decisions gated on a similarity threshold (e.g. "only use memories above 0.8") show no clear quality improvement over a lower or no threshold

## Root Cause
Embedding similarity and most off-the-shelf reranking scores measure semantic/topical closeness between the query and the candidate text — they were not trained or designed to measure "will this specific piece of information help resolve this specific task," which depends on factors the score has no access to: recency relative to other candidates, whether the fact has since been superseded, whether it's redundant with something else already known, or whether it addresses the actual decision the agent needs to make versus merely mentioning related keywords. Because similarity scores are continuous numbers that look like confidence values, it's easy for downstream logic to treat them as if they were calibrated probabilities of usefulness, when they are really just a proxy for topical closeness with no guarantee of monotonic correlation to real-world utility.

## Example
```
Memory store for a support agent contains, among others:
  A: "Standard return policy: 30 days, original packaging required."
     (stored 14 months ago) — similarity to query: 0.86
  B: "Policy update: as of last month, returns extended to 60 days
     for orders over $200." (stored 3 weeks ago) — similarity to
     query: 0.71

Query: "What's our return policy for this $340 order?"

Top-1 retrieval by raw similarity score returns A (0.86 > 0.71),
because A's wording more closely echoes generic "return policy"
phrasing, while B's more specific, more recent, more relevant
update scores lower due to its more specific phrasing pulling it
slightly further from the generic query embedding.

Agent, trusting the higher score as the more relevant/confident
match, tells the customer: "Our return policy is 30 days with
original packaging" — quoting outdated, superseded policy with
high apparent confidence, while the actually-correct 60-day
extension for this order size scored lower and was either not
surfaced at all (if top-1 only) or buried below the confident-
sounding top result.
```

## Statistics
| Finding | Context |
|---------|---------|
| Correlation between raw embedding similarity score and human-judged usefulness for a specific downstream task is typically moderate at best, and substantially weaker when recency or supersession is relevant to the query | Typical range reported in retrieval-quality evaluation studies |
| Top-1-by-similarity selection is measurably outperformed by rerank-then-filter approaches that incorporate recency and redundancy signals, in comparative retrieval evaluations | Reported range across teams comparing raw-similarity vs. reranked retrieval |
| A meaningful share of "confidently wrong" agent answers trace back to a high-similarity-scored but substantively outdated or redundant retrieved memory | Estimated from post-hoc analysis of agent factual-error incidents |

## Mitigations
1. **Multi-signal reranking**: Combine raw similarity with recency, source authority, and redundancy signals in a reranking step rather than trusting embedding similarity alone as the final ranking.
2. **Calibration evaluation**: Periodically measure how well the retrieval score actually predicts downstream task success (not just topical relevance), and recalibrate or replace the scoring function when correlation is weak.
3. **Decouple "retrieved" from "trusted"**: Treat retrieval score as a candidate-selection signal only, and require a separate validation step (recency check, contradiction check) before treating a retrieved fact as authoritative.
4. **Present score uncertainty, not false precision**: When surfacing confidence to the agent or user, avoid presenting raw similarity scores as if they were calibrated probabilities; use coarse bands or explicit caveats instead.
5. **Supersession-aware retrieval**: For domains where facts change over time (policies, prices, statuses), explicitly boost recency or check for a "supersedes" relationship rather than relying on similarity score alone to surface the current version.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| score_utility_correlation | Correlation between retrieval score and human/eval-judged usefulness on a sampled query set | Alert if < 0.4 |
| outdated_top_result_rate | Rate at which the top-scored result is a superseded version of a fact that has a more current counterpart in the store | Alert if > 5% |
| confident_wrong_answer_rate | Rate of agent answers traced to a high-scoring but substantively incorrect/outdated retrieved memory | Alert if > 2% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Confidently wrong answer traced to retrieval | An agent answer is found incorrect and traces to a high-similarity but outdated/wrong retrieved memory | High | Flag the source memory for review, check for a superseding record that should have ranked higher |
| Score calibration drift | score_utility_correlation drops below threshold on periodic evaluation | Medium | Re-evaluate reranking model/weights, review recent shifts in query or content patterns |

## Related Patterns
- [Retrieval Temporal Ordering Failure](./retrieval-temporal-ordering-failure.md) - a specific, common cause of miscalibration: the score doesn't account for recency, letting stale results outrank current ones
- [Retrieval Deduplication Failure](./retrieval-deduplication-failure.md) - near-duplicate high-scoring results compound miscalibration by crowding out genuinely distinct, useful candidates
- [Semantic Drift in Embeddings](./semantic-drift-in-embeddings.md) - an embedding model change can itself introduce or worsen miscalibration by shifting what "similar" means without recalibrating downstream thresholds
