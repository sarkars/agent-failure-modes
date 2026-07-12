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

## Mitigation Strategies

### Prevention
1. **Outcome-validated metric selection**: Before adopting any eval metric, validate it against actual user outcomes (satisfaction, task completion, compliance) on a sample, rather than inheriting metrics from another domain, since 45% of teams use metrics inherited without validation per Key Statistics. Trade-off: requires an upfront correlation study and ongoing re-validation as the product evolves.
2. **Task-specific composite metrics over generic NLP metrics**: Design metrics specific to the actual use case (e.g., legal citation accuracy, compliance adherence) rather than relying on generic proxies like BLEU or exact match, since the example showed BLEU (0.78) scored wrong citations the same as correct ones. Trade-off: task-specific metrics are more expensive to build, require domain expertise, and don't transfer to other products.
3. **Multi-metric guardrails instead of single-metric optimization**: Require a response to pass a balanced set of metrics (factual accuracy, completeness, compliance, task completion) rather than any single measurable metric, preventing the single-axis optimization pressure Goodhart's Law describes in Contributing Factors. Trade-off: multi-metric thresholds are harder to tune and can conflict, requiring an explicit prioritization policy.

### Detection & Response
1. **Eval-score-to-outcome correlation tracking**: Continuously calculate the correlation between eval metric scores and downstream outcomes (satisfaction, business KPIs, incident rate); a metric with declining or low correlation is flagged for review, directly targeting the "60% of eval metrics don't correlate with user satisfaction" finding.
2. **Passed-eval-failed-production case audits**: Systematically audit cases that passed evaluation but generated complaints or incidents in production, like the example's 3 compliance violations despite an all-metrics PASS, tracing which metric(s) gave false confidence.
3. **Human evaluation spot-checking against automated scores**: Run periodic human judgment sampling calibrated against automated metric scores, since BLEU/ROUGE correlate below 0.3 with human quality judgments per Key Statistics, giving an independent check the automated metric alone cannot provide.

### Architecture Patterns
1. **LLM-as-judge or human-in-the-loop layer alongside automated metrics**: Architect the eval pipeline so a semantic/quality-judging layer runs in parallel with cheap automated metrics like exact match or BLEU, rather than relying on the cheap metric alone as the pass/fail gate.
2. **A/B-validated metric pipeline**: Structurally require that any new or changed eval metric be validated against live A/B test outcome data before it can gate releases, closing the "metric-business outcome correlation rarely measured" gap.
3. **Domain-specific assertion framework**: Build an assertion-based evaluation harness (e.g., citation-checker, compliance-rule-checker) as a first-class architecture component alongside generic text-similarity scoring, so domain-critical failure modes have a dedicated detection path instead of being absorbed into a generic score.

### Metrics
1. **metric_outcome_correlation_coefficient**: Target: >0.6 correlation between eval score and user satisfaction/business outcome; Alert when correlation drops below 0.4
2. **passed_eval_failed_production_rate**: Target: <2% of production incidents trace back to cases that passed eval; Alert above 5%
3. **human_automated_score_agreement_rate**: Target: >85% agreement between human judgment sample and automated metric verdict; Alert below 70%
4. **single_metric_gaming_indicator**: Target: 0 detected metric-optimized-but-quality-flat changes; Alert when a change improves the primary metric by more than 5% with no corresponding user-outcome improvement

### Alerts
1. **Metric-Outcome Correlation Collapse** (P2): Condition - tracked correlation between an eval metric and real outcomes drops below the defined floor. Action: suspend using that metric as a release gate, initiate a metric redesign/validation cycle.
2. **Compliance/Safety Incident Despite Passing Eval** (P1): Condition - a production incident occurs from a response category the eval marked as passing. Action: halt further releases gated solely on that metric, add a dedicated assertion/check for the failure category, re-audit recent passed cases.
3. **Human-Automated Score Divergence** (P2): Condition - human evaluation sample disagrees with automated metric verdict above threshold rate. Action: pause reliance on the automated metric for release decisions until recalibrated against fresh human judgments.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation inadequacy
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark limitations
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation design
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Metric selection
- [CMARix: RAG & AI Trust Statistics](https://www.cmarix.com/blog/rag-ai-statistics/) - Trust metrics
