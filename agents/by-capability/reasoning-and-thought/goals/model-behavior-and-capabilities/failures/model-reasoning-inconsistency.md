# Model Reasoning Inconsistency

## Issue
The model produces different reasoning chains and different final conclusions when given logically identical inputs that differ only in superficial ways — order of options, phrasing, irrelevant surrounding text, or which call happens to sample a different token early in the chain of thought. An agent that relies on the model's reasoning to make a consistent decision (approve/deny, rank A over B, classify as X) gets a decision that isn't actually a function of the underlying facts, just of incidental surface variation.

**Frequency**: Common

**Symptoms**
- Re-running the exact same decision prompt (same facts, reordered options) flips the conclusion a nonzero fraction of the time
- The model gives contradictory answers when the same question is asked in two logically equivalent but differently-worded ways within the same session
- Chain-of-thought traces for the same underlying problem take visibly different reasoning paths across calls, sometimes reaching different conclusions
- Position/order bias: presenting option A before option B versus B before A changes which one the model prefers, independent of content
- Downstream aggregate metrics (e.g. approval rate) shift measurably when only cosmetic prompt formatting changes, with no change to the underlying policy or facts

## Root Cause
Autoregressive generation with sampling means the model's reasoning is not a fixed computation over the input's logical content — it is a probabilistic walk where each generated token depends on the exact preceding token sequence, so any surface-level difference (option order, phrasing, whitespace) changes the token sequence and can cascade into a different reasoning path. Even at low temperature, the model's training didn't optimize for invariance to logically-irrelevant surface variation; it optimized for plausible next-token prediction given the specific text seen, and many training examples do correlate position or phrasing with outcome (e.g. first-listed options being preferred in typical documents), so the model has learned superficial correlations that have nothing to do with the task's actual logic. Chain-of-thought reasoning amplifies this: once the model commits to an early reasoning step that happens to differ across runs, subsequent steps condition on that divergent path, compounding a small initial difference into a materially different conclusion.

## Example
```
A vendor-risk agent evaluates whether a supplier contract clause is
"acceptable" or "requires legal review," given identical clause text,
run twice with only the order of two reference example clauses in the
few-shot prompt swapped.

Run A (example order: lenient clause first, strict clause second):
"This clause is acceptable; the indemnification cap is standard for
this contract size." -> classified ACCEPTABLE

Run B (example order: strict clause first, lenient clause second):
"This clause's indemnification cap is below typical protection levels
and should be flagged." -> classified REQUIRES REVIEW

The underlying clause text was byte-for-byte identical in both runs;
only the order of unrelated few-shot examples changed, yet the agent's
downstream action (auto-approve vs. route to legal) flipped.
```

## Statistics
| Finding | Context |
|---------|---------|
| Order-swapping options or few-shot examples in decision prompts typically flips the model's conclusion in an estimated 5-20% of cases, depending on how close the underlying decision is to the model's uncertainty boundary | Typical range observed in prompt-order-sensitivity evaluations |
| Rephrasing a logically equivalent question produces a different final answer in an estimated 10-15% of borderline cases, versus under 2% for clear-cut cases | Estimated from paraphrase-consistency evaluations on classification tasks |
| Aggregating multiple independent reasoning samples and taking a majority vote (self-consistency) typically improves decision stability by a meaningful margin over single-sample reasoning, at the cost of multiple model calls | Typical range reported across self-consistency technique evaluations |

## Mitigations
1. **Self-consistency sampling**: For high-stakes decisions, run the same prompt multiple times (varying only sampling, not content) and take a majority vote or flag disagreement for human review, rather than trusting a single reasoning pass.
2. **Order-randomization testing**: Before deploying a decision prompt, test it with option/example order systematically varied to measure and bound position-sensitivity before it reaches production.
3. **Canonicalize input presentation**: Normalize option ordering (e.g. always alphabetical or by a fixed neutral rule) rather than passing through whatever incidental order the upstream system produced, removing one axis of irrelevant variation.
4. **Lower-temperature or deterministic decoding for decision-critical calls**: Reduce (not eliminate, but reduce) run-to-run variance for calls where consistency matters more than creative diversity.
5. **Consistency monitoring in production**: Periodically re-submit sampled historical decisions and compare current output to the original, tracking a consistency-rate metric over time rather than assuming it stays constant across model or prompt changes.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| decision_flip_rate_on_reorder | Rate at which identical-content, reordered prompts produce a different conclusion | Alert if > 10% for high-stakes decision types |
| self_consistency_agreement_rate | Agreement rate across multiple independent reasoning samples of the same prompt | Alert if < 80% |
| aggregate_outcome_drift_on_cosmetic_change | Shift in aggregate decision-rate metrics attributable to formatting-only prompt changes | Alert if drift exceeds 5 percentage points |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High flip rate on sampled re-test | decision_flip_rate_on_reorder exceeds threshold for a decision pipeline | High | Route affected decision type through self-consistency voting, add to human review queue |
| Consistency regression after change | self_consistency_agreement_rate drops after a prompt or model version change | Medium | Roll back or investigate change, re-run consistency evaluation suite |

## Related Patterns
- [Model Output Format Instability](./model-output-format-instability.md) - both are forms of run-to-run nondeterminism, one in structure and one in substantive conclusions
- [Model Capacity Limits](./model-capacity-limits.md) - reasoning inconsistency is more pronounced on complex, near-boundary decisions where capacity is already strained
- [Model Fairness Bias](./model-fairness-bias.md) - a systematic, demographically-correlated subtype of the same underlying sensitivity to surface-level input variation
