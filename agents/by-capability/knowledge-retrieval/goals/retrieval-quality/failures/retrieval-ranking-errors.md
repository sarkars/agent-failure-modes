# Retrieval Ranking Errors

## Issue: Relevant Documents Not Ranked Appropriately

**Frequency**: Common

**Symptoms**
- Answer exists in retrieved set but model misses it
- Relevant document at position 8 when top-3 used
- Irrelevant documents ranked above relevant ones
- Similar relevance scores for very different quality docs
- Position-dependent answer quality (top-1 vs top-5)

**Root Cause**
Even when relevant documents are retrieved, poor ranking means they may be positioned too low for effective use. Models have attention biases (favor early context), context windows limit how much can be passed, and top-k cutoffs may exclude relevant documents. RAGAS Context Precision specifically measures whether relevant chunks appear before irrelevant ones in the ranking.

**Example**
```
Query: "What are the tax implications of 401k early withdrawal?"

Retrieved documents (top 10):
Rank 1: General retirement planning guide (0.89 sim)
Rank 2: IRA withdrawal rules (0.87 sim) - wrong account type
Rank 3: Investment advice article (0.85 sim)
Rank 4: 401k contribution limits (0.84 sim) - wrong topic
Rank 5: 401k early withdrawal penalties ← BEST ANSWER (0.82 sim)
Rank 6: Roth vs Traditional comparison (0.81 sim)
Rank 7: 401k loan provisions (0.80 sim)
Rank 8: Tax penalty exceptions ← ALSO RELEVANT (0.78 sim)
Rank 9: General tax advice (0.77 sim)
Rank 10: Retirement age calculator (0.75 sim)

System uses top-3 for context.
Result: Answer based on wrong account type (IRA vs 401k)

RAGAS Context Precision calculation:
  Relevant docs at positions: 5, 8
  Total positions: 10
  Precision@3: 0/3 = 0.0 (no relevant in top 3)
  Precision@5: 1/5 = 0.2
  Average Precision: Low

  Ideal ranking would place positions 5,8 at 1,2
```

**Key Statistics**
From Ranking Research (RAGAS studies, 2026):
- Retrieval finds answer 80%+, ranking exposes it 60%
- Position 1 vs position 5: 25% answer quality drop
- Context Precision scores: median 0.65 in production
- "Lost in the middle" effect: 30% accuracy drop for middle positions
- MRR (Mean Reciprocal Rank) variance: 0.3-0.9 across queries

**Ranking Error Types**
| Error Type | Description | Impact |
|------------|-------------|--------|
| Similarity ≠ Relevance | High embedding similarity but wrong content | Wrong answer |
| Position bias | Relevant doc outside top-k | Answer missed |
| Tie-breaking failures | Similar scores, wrong ordering | Inconsistent |
| Query-type mismatch | Ranking tuned for different query types | Poor precision |
| Recency ignored | Older version ranked higher | Stale answer |

**Contributing Factors**
- Embedding similarity ≠ task relevance
- Fixed top-k regardless of query complexity
- No relevance-aware scoring
- Single-stage retrieval without refinement
- Ignoring document metadata in ranking
- Training data distribution mismatch

## Mitigation Strategies

### Prevention
1. **Hybrid Multi-Signal Scoring**: Combine semantic similarity with lexical/keyword matching (BM25) and metadata signals (e.g., account-type match) so documents like "401k early withdrawal penalties" aren't out-ranked by generically similar but wrong-account-type documents like IRA rules, directly addressing the "similarity != relevance" root cause.
2. **Entity/Attribute-Aware Scoring Boost**: Detect key disambiguating entities in the query (401k vs. IRA, specific product/account names) and boost documents matching that entity, since embedding similarity alone conflated topic closeness with entity-level correctness in the example.
3. **Dynamic Top-K Based on Score Distribution**: Instead of a fixed top-3/top-5 cutoff, use the score distribution (gap detection) to decide how many results to pass to the LLM, reducing the chance a relevant document at rank 5 or 8 is cut off arbitrarily.

### Detection & Response
1. **Context Precision and MRR Tracking**: Continuously monitor Context Precision and Mean Reciprocal Rank in production; treat a median around 0.65 as a baseline to improve against, with alerts on regression.
2. **Best-Answer-Position Analysis**: Log the rank position of the document that actually contained the correct answer (via eval or user feedback), and track how often it falls outside the top-k actually used, quantifying the "lost in the middle" effect.
3. **Entity-Mismatch Sampling**: For domain queries with disambiguating entities (account types, product names, versions), sample cases where the top-ranked result doesn't match the query's specific entity, using this to retrain or tune the scoring function.

### Architecture Patterns
1. **Multi-Stage Retrieval With Precision-Focused Refinement**: Use a fast recall-oriented first stage, then a slower but more accurate second-stage scorer (learned-to-rank or cross-encoder with entity features) to fix ordering before truncating to top-k.
2. **Score Calibration Across Signal Types**: Normalize and calibrate semantic, lexical, and metadata scores onto a common scale before combining, since raw cosine similarity and BM25 scores aren't directly comparable and naive combination can wash out useful signals.
3. **Query-Type-Specific Ranking Profiles**: Maintain distinct ranking configurations for query types known to require entity disambiguation (financial account types, product variants) versus general informational queries, rather than one universal ranking function.

### Metrics
1. **context_precision_at_k**: Target: > 0.75; Alert threshold: < 0.6
2. **mean_reciprocal_rank**: Target: > 0.7; Alert threshold: < 0.5
3. **correct_answer_outside_topk_rate**: Target: < 15%; Alert threshold: > 25%
4. **entity_mismatch_top1_rate**: Target: < 10% for entity-disambiguation queries; Alert threshold: > 20%

### Alerts
1. **Ranking Quality Regression** (P2): Condition - context_precision_at_k drops below 0.6 for a query segment. Action: audit the scoring function/signal weights for that segment, check for recent index or model changes.
2. **Entity Disambiguation Failure Spike** (P1): Condition - entity_mismatch_top1_rate exceeds 20% for queries with detectable disambiguating entities (e.g., account type). Action: add/boost the entity-matching feature in ranking, escalate given the risk of factually wrong domain-specific answers.
3. **Correct Answer Buried** (P2): Condition - correct_answer_outside_topk_rate exceeds 25%. Action: increase effective top-k or improve multi-stage refinement before truncation.

## References

- [RAGAS Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/context_precision.html) - Precision metric
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Position bias in long context
- [NDCG for RAG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) - Ranking evaluation
- [Hybrid Search](https://www.pinecone.io/learn/hybrid-search-intro/) - Multi-signal ranking
