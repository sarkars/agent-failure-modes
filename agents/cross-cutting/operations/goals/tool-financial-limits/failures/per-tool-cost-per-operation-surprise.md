# Per-Tool Cost-Per-Operation Surprise

## Issue
A tool's real price varies by operation type or payload characteristics — a "transcription" call costs more per minute of audio than the flat per-call estimate assumes, or a "document analysis" call is priced per page or per KB rather than per request — but the agent's cost estimator uses a single average or flat per-call figure. When the actual mix of operations skews toward the expensive end (longer audio, bigger documents, more complex queries), realized spend diverges sharply from the budget the agent believed it was operating within.

**Frequency**: Very Common

**Symptoms**
- Actual per-call cost varies widely even though the agent's internal cost model treats every call to a given tool as the same price
- Budget projections built from average historical cost break down when the input mix shifts (e.g. a batch of unusually long documents)
- Cost overruns correlate with specific input characteristics (payload size, operation subtype, output length) that the estimator doesn't take as inputs
- The vendor's pricing page lists cost as "starting at $X" or "$X per unit" (page, token, minute, MB) rather than a flat per-call price, but the integration bills it as flat
- Two calls to the same endpoint with the same nominal "operation" produce meaningfully different charges

## Root Cause
Cost estimators are commonly built during initial integration using a single representative test call, and that call's price gets hardcoded or averaged into a flat per-call figure for simplicity. Real vendor pricing for content-processing tools is very often a function of the payload (duration, size, token count, page count, complexity) rather than a flat rate per request, but that variability is only visible by reading the pricing schedule in detail or by observing a wide distribution of real invoices — neither of which happens during a quick integration.

## Example
```
An agent uses "TranscribeFast" to transcribe customer call recordings,
priced at $0.006 per second of audio (not disclosed as a flat per-call
rate, but the integration's cost estimator was written against a single
2-minute test call and hardcoded to $0.72/call).

The agent processes a batch of 300 calls. Most are short (2-3 minutes)
but 40 of them are long sales calls (25-40 minutes). The estimator
predicts 300 x $0.72 = $216 total.

Actual cost: the 260 short calls cost roughly $150 total, but the 40 long
calls cost $0.006/sec x ~1,800 sec average x 40 = $432 by themselves.
Real total: approximately $582, 2.7x the estimate, discovered only when
the daily budget cap (set based on the $216 estimate plus margin) is hit
partway through the batch and the remaining calls fail.
```

## Statistics
| Finding | Context |
|---------|---------|
| Payload-based pricing (per page, per minute, per token, per MB) is used by a large share of content-processing APIs (transcription, document AI, image analysis, LLM inference) rather than flat per-call pricing | Common industry pricing pattern |
| Cost estimators built from a single representative sample typically underestimate true spend by 1.5-3x when the real input distribution has a long tail | Typical range observed when input size varies significantly |
| Budget-cap failures caused by payload-driven cost variance are commonly discovered mid-batch rather than pre-flight, since pre-flight checks rarely inspect payload size against the pricing formula | Typical pattern absent payload-aware estimation |

## Mitigations
1. **Payload-aware cost formula**: Replace flat per-call cost estimates with the vendor's actual pricing formula (per second, per page, per token, per MB) applied to the real payload being sent, computed before the call is made.
2. **Pre-flight cost projection for batches**: Before running a batch job, sum the projected cost across all items using the payload-aware formula, and compare against remaining budget before starting, not just per-call at execution time.
3. **Outlier payload flagging**: Flag and optionally require confirmation for individual operations whose payload size implies a cost significantly above the median (e.g. an audio file 5x longer than the batch average).
4. **Continuous calibration against actual billing**: Periodically compare the payload-aware cost model's predictions against real vendor invoices and adjust the per-unit rate used in the formula if it drifts.
5. **Budget caps expressed in the same unit as pricing**: Where possible, set budget caps in the vendor's native billing unit (total minutes, total pages) rather than call count, so the cap tracks the actual cost driver.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| estimated_vs_actual_cost_variance | Difference between pre-flight cost projection and realized cost for a batch or session | Alert if variance exceeds 30% |
| payload_size_p95_vs_estimator_baseline | 95th-percentile payload size in a batch compared to the size the flat-rate estimator was calibrated against | Alert if p95 exceeds baseline by 3x |
| mid_batch_budget_exhaustion_rate | Frequency of batch jobs that hit the budget cap before completing | Alert if > 1 per week |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cost model variance high | estimated_vs_actual_cost_variance exceeds 30% for a completed batch | High | Recalibrate the payload-aware cost formula, audit recent invoices |
| Outlier payload detected pre-flight | An individual item's projected cost exceeds 5x the batch median | Medium | Flag for manual review or confirmation before dispatch |

## Related Patterns
- [Per-Tool Burst Pricing Penalty](./per-tool-burst-pricing-penalty.md) - both are cases of pricing mechanics the flat-rate cost model fails to represent
- [Hidden Tool Costs Not Visible](./hidden-tool-costs-not-visible.md) - a related failure where the cost driver isn't in the visible response at all, versus here where it's visible but unmodeled
- [Per-Tool Tiered Pricing Unknown](./per-tool-tiered-pricing-unknown.md) - another dimension of pricing complexity the agent's cost model needs to account for
