# Context Stuffing Failure

## Issue: Too many chunks dilute relevant evidence.

**Frequency**: Occasional

**Symptoms**
- Long context; answer ignores key chunk.
- Answer omits a fact present in a retrieved chunk buried in the middle of a long context window ("lost in the middle").
- Increasing top-k retrieved chunks measurably lowers answer accuracy even though the correct chunk is included somewhere in context.
- Synthesis draws on a low-relevance chunk positioned near the start or end of the context instead of the correct chunk placed mid-context.

**Root Cause**
Retrieval is configured with a large top-k to maximize recall, but with no re-ranking or truncation step before synthesis and no relevance-based ordering of chunks within the context window, the correct chunk can end up buried in the middle of the context rather than positioned where the model attends most (the start or end). Because no chunk-level relevance scores are passed to the synthesis model to help it weight evidence, and a fixed context budget forces the inclusion of many only-marginally-relevant chunks alongside the correct one, the model has no signal telling it which chunk in a long, undifferentiated context actually matters — so more retrieved evidence measurably lowers accuracy instead of raising it.

**Example**
```
Query: "What's the notice period for terminating the enterprise contract?"
Retrieval returns the top-20 chunks (k=20) to maximize recall. The correct chunk
(notice period = 60 days) is ranked 11th and lands in the middle of the 20-chunk
context window. The synthesis model's answer instead cites a tangential chunk about
"contract renewal timelines" from near the top of the context, because the correct
answer was diluted among 19 other chunks discussing unrelated contract clauses.
```

**Contributing Factors**
- Retrieval configured with a large top-k (e.g., 15-20) to maximize recall, with no re-ranking or truncation step before synthesis.
- No relevance-based ordering of chunks within the context window, so the most relevant chunk isn't positioned where the model attends most (start/end).
- No chunk-level relevance scores passed to the synthesis model to help it weight evidence.
- Fixed context budget forces inclusion of many marginally-relevant chunks rather than a curated few highly-relevant ones.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Buried correct chunk | Query where the correct answer's chunk is ranked 10-15th among 20 retrieved chunks | Answer uses the correct, lower-ranked chunk | Answer uses a higher-ranked but less relevant chunk instead |
| Answer quality vs context size | Same query run with top-k=5 vs top-k=20 | Accuracy stays consistent or improves with more context | Accuracy at k=20 is measurably lower than at k=5 |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| key_evidence_inclusion_rate_percent | 100% | For eval queries with a known ground-truth chunk, check whether that chunk's content is reflected in the synthesized answer |

---

## Mitigation Strategies

### Prevention
1. **Context Compression Strategy**: Instead of passing all retrieved chunks, compress context intelligently. Rank chunks by relevance_to_query. Select top-K (K=3-5) most relevant chunks. Pass ranked list with relevance_scores. Reduces dilution from low-relevance chunks.
2. **Evidence Ranking Before Synthesis**: Explicitly rank evidence chunks before passing to synthesis model. Highlight top_evidence chunks with markers ('HIGHLY RELEVANT:', 'SUPPORTING:', 'SUPPLEMENTARY:'). Model should prioritize highly-ranked evidence.
3. **Context Length Constraints**: Set maximum context_window_tokens (e.g., 3000 tokens). Truncate less-relevant chunks first. Never exceed context limit, even if more chunks available.

### Detection & Response
1. **Context Dilution Detection**: Compare relevance_ranking of chunks passed to synthesis model. Alert if irrelevant chunks (rank > 10, relevance < 0.3) included in context. Track: % of context from relevant vs low-relevance chunks.
2. **Key Evidence Omission Detection**: For queries where ground-truth relevant chunk is known, verify it's included in synthesis context. Alert if key evidence excluded due to context overflow.
3. **Answer Quality vs Context Length**: Measure synthesis quality with varying context_lengths. Alert if quality drops when context > threshold (indicates stuffing hurting performance). Find optimal context_length.

### Architecture Patterns
1. **Evidence Ranking Module**: Pre-synthesis, rank retrieved chunks by relevance. Compute ranking_scores. Pass ranked_list + scores to synthesis model. Model sees relevance_indicators.
2. **Dynamic Context Selection**: Given query + retrieved chunks, dynamically select subset of chunks to maximize relevance_density. Example: choose chunks with relevance > 0.6, stop when context_length reaches limit.
3. **Hierarchical Summarization**: Progressively summarize chunks as context fills. Compress low-relevance chunks into brief summaries. Preserve full details only for highly-relevant chunks.

### Metrics
1. **context_compression_ratio**: Target: 0.3-0.5 (keep 30-50% of retrieved chunks); Alert if ratio > 0.8 (too much context)
2. **evidence_dilution_percent**: Target: < 10% of context from low-relevance chunks (rank > 10)
3. **key_evidence_inclusion_rate_percent**: Target: 100%; Key chunks must be in context
4. **context_length_optimal_tokens**: Target: 2000-4000; Alert if exceeding window
5. **synthesis_quality_by_context_length**: Target: quality maintains with < 3000 tokens; Alert if degrades

### Alerts
1. **Context Stuffing Detected** (P2 - Warning): Condition - > 80% of context from low-relevance chunks OR context_length > max. Action: Review chunk ranking, apply compression, consider re-retrieval.
2. **Key Evidence Omitted** (P2 - Warning): Condition - highly-relevant evidence chunk excluded from context. Action: Adjust context_length or ranking algorithm, consider regenerating answer.
3. **Synthesis Quality Degradation Due to Context Size** (P1 - Critical): Condition - answer quality degrades with context_length > threshold. Action: Investigate model's context handling, apply compression, potential model tuning.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| key_evidence_inclusion_rate_percent | < 90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Key Evidence Drop Detected | key_evidence_inclusion_rate_percent on eval sample falls below 90% | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
