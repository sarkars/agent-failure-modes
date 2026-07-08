# Context Stuffing Failure

## Issue: Too many chunks dilute relevant evidence.

**Frequency**: Occasional

**Symptoms**
- Long context; answer ignores key chunk.
- [Add more specific symptoms]

**Root Cause**
Too many chunks dilute relevant evidence.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
