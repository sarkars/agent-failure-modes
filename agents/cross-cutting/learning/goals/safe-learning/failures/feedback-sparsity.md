# Feedback Sparsity

## Issue: Not enough signal to learn safely.

**Frequency**: Occasional

**Symptoms**
- Few labels; high variance in conclusions.
- [Add more specific symptoms]

**Root Cause**
Not enough signal to learn safely.

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
1. **Active Learning / Uncertainty Sampling**: Prioritize scarce human review budget on the examples where the agent's confidence is lowest or where model disagreement (e.g., ensemble variance) is highest, so limited labels concentrate signal where it reduces the most uncertainty rather than being spent randomly.
2. **Minimum Sample Size Gate per Cohort**: Require a defined minimum label count for a segment, intent, or behavior before any conclusion or update derived from it is allowed to affect production behavior; segments below threshold are explicitly marked "insufficient data" rather than silently acted upon.
3. **Synthetic/Proxy Signal Augmentation**: Supplement sparse human labels with bounded, validated proxy signals (self-consistency checks, model-graded evals cross-checked against a human-labeled subset) to widen coverage, while capping how much influence proxy-derived signal can have relative to genuine human feedback.

### Detection & Response
1. **Label Volume & Coverage Monitoring**: Continuously track label counts per segment/intent/behavior against defined minimums, surfacing which slices of traffic are running on stale or absent feedback.
2. **Statistical Significance Gating**: Before any behavior change is attributed to feedback, compute a confidence interval on the underlying metric; wide intervals block the conclusion from being acted on rather than being treated as ground truth.
3. **Sparse-Segment Flagging and Deferral**: Automatically exclude segments below the sample-size threshold from automated update decisions, routing them instead to a queue for targeted additional labeling.

### Architecture Patterns
1. **Active Learning Sampling Service**: A queue that ranks unlabeled examples by uncertainty/diversity score and feeds the highest-value items to human reviewers first, maximizing information gain per labeling hour.
2. **Stratified Label Store**: A label store that tracks counts and confidence intervals per segment (not just an aggregate), exposing a coverage API that other systems query before trusting a conclusion for that segment.
3. **Statistical Guardrail Layer**: A wrapper around the learning/update pipeline that checks sample size and confidence interval width before allowing an update to proceed, blocking with a clear "insufficient data" reason code otherwise.

### Metrics
1. **labels_per_segment_count**: Target: >= defined minimum (e.g., 200) per segment; Alert threshold: < 50% of minimum
2. **label_coverage_percent_of_traffic**: Target: > 80% of active segments meeting minimum; Alert threshold: < 50%
3. **conclusion_confidence_interval_width**: Target: within pre-defined tolerance for the metric; Alert threshold: exceeds tolerance and still used for a decision
4. **sparse_segment_count**: Target: trending down over time; Alert threshold: increasing for 2+ consecutive review cycles

### Alerts
1. **Update Triggered on Insufficient Data** (P1 - Critical): Condition - an automated behavior update is about to apply to a segment below the minimum sample size. Action: Block the update, route segment to active-learning queue, require manual override with justification to proceed.
2. **Coverage Drop Across Segments** (P2 - Warning): Condition - label coverage percent falls below 50% for two consecutive cycles. Action: Reallocate reviewer capacity via active learning sampler, investigate why label volume dropped.
3. **Active Learning Queue Starved** (P3 - Info): Condition - uncertainty-sampled queue is not being cleared at the expected rate. Action: Escalate to review capacity planning, consider temporary proxy signal augmentation.

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

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
