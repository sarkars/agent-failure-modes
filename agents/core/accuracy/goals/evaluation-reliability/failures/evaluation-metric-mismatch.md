# Evaluation Metric Mismatch

## Issue: Metrics Don't Measure What Actually Matters for Success

**Frequency**: Common

**Symptoms**
- High eval scores but poor user satisfaction
- Agent optimized for wrong objective
- Important failures not captured by metrics
- Metrics game-able without quality improvement
- Disconnect between eval results and business outcomes

**Root Cause**
Evaluation metrics are proxies for real-world success, but the wrong proxy can mislead. Exact string match penalizes valid paraphrases. BLEU scores don't capture factual accuracy. Response time metrics ignore response quality. Teams optimize for measurable metrics while actual user needs go unmeasured.

**Example**
```
Scenario: Legal document assistant evaluation

Evaluation metrics used:
  1. Exact match accuracy: 85%
  2. Response time: 1.2 seconds avg
  3. BLEU score: 0.78

Evaluation result: PASS (all metrics above threshold)

Production reality:
  - Users report 40% of answers "miss the point"
  - 3 compliance violations from agent responses
  - User satisfaction: 2.8/5 stars

Metric analysis:

Exact match (85%):
  - Penalized: "The statute of limitations is 3 years"
  - Expected: "Three years is the statute of limitations"
  - Both correct, marked wrong due to word order

BLEU score (0.78):
  - Measures word overlap
  - Doesn't check legal accuracy
  - Wrong citations scored same as correct ones

What should be measured:
  - Factual accuracy (especially citations)
  - Legal correctness
  - Completeness of response
  - User task completion rate
  - Compliance adherence
```

**Key Statistics**
From Evaluation Research (2026):
- 60% of eval metrics don't correlate with user satisfaction
- BLEU/ROUGE correlate <0.3 with human quality judgments
- Exact match misses 40% of valid correct responses
- 45% of teams use metrics inherited without validation
- Metric-business outcome correlation rarely measured

**Metric Mismatch Types**
| Metric | Measures | Misses |
|--------|----------|--------|
| Exact match | String equality | Valid paraphrases |
| BLEU/ROUGE | Word overlap | Factual accuracy |
| Response time | Speed | Quality |
| Completion rate | Finishing | Correctness |
| Token count | Brevity | Completeness |

**Contributing Factors**
- Easy-to-compute metrics chosen over meaningful ones
- Metrics copied from other domains
- No user outcome validation
- Single metric optimization
- No metric-to-outcome correlation analysis
- Goodhart's Law ("measure becomes target")

**Mitigation Strategies**
1. **Multi-metric evaluation**: Balance multiple dimensions
2. **Human evaluation sampling**: Regular human judgment calibration
3. **Outcome correlation**: Validate metrics predict real outcomes
4. **Semantic similarity**: Use embeddings instead of exact match
5. **Task-specific metrics**: Design metrics for actual use case
6. **A/B validation**: Correlate eval scores with production A/B results

**Detection**
- Compare eval scores to user satisfaction
- Audit "passed eval, failed production" cases
- Calculate metric-outcome correlations
- Survey users about quality vs. eval results
- Track metric gaming indicators

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation inadequacy
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark limitations
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation design
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Metric selection
- [CMARix: RAG & AI Trust Statistics](https://www.cmarix.com/blog/rag-ai-statistics/) - Trust metrics
