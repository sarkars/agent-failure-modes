# Feedback Sparsity

## Issue: Not enough signal to learn safely.

**Frequency**: Occasional

**Symptoms**
- Few labels; high variance in conclusions.
- Long-tail intents or rare edge-case behaviors receive an update-affecting "conclusion" from a handful of labels while high-traffic segments have hundreds, producing wildly different statistical confidence across segments that the pipeline treats as equally trustworthy.
- A single vocal reviewer or a short burst of feedback (e.g., one bad week) swings the aggregate signal for a low-volume segment because there is no other data to dilute it.

**Root Cause**
Not enough signal to learn safely.

**Example**
```
A travel-booking agent handles a rare "multi-city award-ticket rebooking" intent only 8 times in a
month. Three of those interactions happen to receive a thumbs-down (perhaps from one frustrated
customer contacting support three times). The learning pipeline computes a 37.5% negative rate for
this intent, well above the 10% threshold that normally triggers a policy rollback, and disables the
agent's handling of that intent entirely -- even though 8 samples is far too small to distinguish a
real regression from noise.
```

**Contributing Factors**
- Long-tail intents/segments naturally receive low traffic, so absolute label counts stay small no matter how long the system runs.
- No minimum sample size or confidence-interval gate exists before a segment's aggregate feedback is allowed to drive an automated update.
- Reviewer capacity is allocated uniformly or randomly rather than prioritized toward high-uncertainty or low-coverage segments (no active learning).
- Feedback collection is opt-in/passive (e.g., only unhappy users bother to rate), so the small sample that does exist is not representative of the segment as a whole.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Low-count segment update attempt | Segment with 8 labels, 3 negative, below the configured minimum of 50 | Pipeline blocks the automated update and marks the segment "insufficient data" | Update proceeds and changes production behavior for that segment |
| Confidence-interval width check | Segment metric with wide CI due to small n (e.g., 37.5% negative rate, n=8) | Conclusion is not acted on because CI width exceeds tolerance | Point estimate is treated as ground truth and drives a policy rollback |
| Active-learning prioritization | Pool of unlabeled examples with varying model uncertainty scores | Highest-uncertainty examples are surfaced to reviewers first | Reviewer queue is ordered randomly/FIFO, ignoring uncertainty signal |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| labels_per_segment_count (eval) | >= 50 per segment before use | Count labels per segment in the evaluation dataset and compare to configured minimum |
| conclusion_confidence_interval_width (eval) | within pre-defined tolerance | Compute CI on the segment's key metric using standard binomial/Wilson interval methods |
| sparse_segment_flag_accuracy | 100% of below-minimum segments correctly flagged | Verify the guardrail layer correctly marks all synthetic below-threshold segments as insufficient data |

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
| labels_per_segment_count | < 50% of defined minimum |
| label_coverage_percent_of_traffic | < 50% |
| sparse_segment_count | increasing for 2+ consecutive review cycles |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Update Triggered on Insufficient Data | an automated behavior update is about to apply to a segment below the minimum sample size | Critical |
| Coverage Drop Across Segments | label coverage percent falls below 50% for two consecutive cycles | Medium |
| Active Learning Queue Starved | uncertainty-sampled queue is not being cleared at the expected rate | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
