# Throughput Per Dollar Optimization Failure

## Issue
A team optimizes an inference serving stack against raw throughput metrics — tokens generated per second, requests served per second, or GPU utilization — and improves them measurably, but the optimization increases the rate of failed, retried, or low-quality outputs that require rework, so the cost-per-successful-output actually gets worse even as the headline throughput number improves. Because throughput is easy to measure directly from the serving layer and "successful outcome" requires tracing further downstream (did the user accept the output, did the task actually complete, did a human have to redo it), teams optimize the visible metric and only discover the economic regression later, if at all.

**Frequency**: Common

**Symptoms**
- Raw throughput metrics (tokens/sec, requests/sec, GPU utilization) improve following an optimization, and the team reports it as a win
- Downstream success-rate metrics (task completion rate, user acceptance rate, error/retry rate) degrade over the same period, but aren't reviewed alongside the throughput win because they're owned by a different team or dashboard
- Retry or regeneration rate increases after the optimization, meaning some fraction of the "extra" throughput is being consumed re-doing work that should have succeeded the first time
- Cost-per-successful-task, when calculated retrospectively, is flat or worse despite the throughput improvement, because the denominator (successful outcomes) didn't grow proportionally to the numerator (raw requests served)
- The optimization was validated against a benchmark or load test that measures speed/volume but doesn't measure or gate on output quality or task success

## Root Cause
Throughput-oriented metrics (tokens/sec, requests/sec, GPU utilization, cost-per-token) are attractive optimization targets because they're generated directly by the serving infrastructure, are available in real time, and improve predictably in response to well-understood levers (larger batches, more aggressive quantization, speculative decoding, shorter timeout/retry budgets). "Cost per successful output," by contrast, requires joining serving-layer data with downstream outcome data that often lives in a different system owned by a different team (product analytics, support tooling, human-review queues), and is measured on a longer delay. This creates a structural incentive and capability gap: infrastructure teams are measured and rewarded on the metric they can see and move quickly, while the metric that actually matters economically is harder to access and slower to compute, so it's the one that gets deprioritized. Several of the specific optimizations that help throughput can directly hurt success rate through independent mechanisms — aggressive quantization can degrade output quality, larger batches can increase latency enough to trigger client-side timeouts and retries, and tighter per-request resource limits imposed to raise utilization can truncate legitimately long generations — so the throughput-success tradeoff isn't hypothetical, it's a direct consequence of the same levers being pulled for both purposes.

## Example
```
An inference platform team is measured on "tokens generated per GPU-hour"
as their primary efficiency KPI. To improve it, they roll out three
changes in the same quarter: INT8 quantization on the serving fleet,
a reduced per-request token budget (capping max_output_tokens from 4096
to 2048 to reduce tail latency and improve batch throughput), and a
tightened client-side timeout (from 30s to 15s) paired with automatic
retry on timeout.

Tokens generated per GPU-hour rises 34% quarter over quarter, and the
platform team reports the initiative as a clear win in their quarterly
review.

Meanwhile, the product team operating the document-summarization agent
built on this platform sees task-completion rate (summaries accepted by
users without a manual edit or regeneration request) drop from 81% to
69% over the same period: the 2048-token cap truncates longer documents'
summaries mid-thought on a meaningful fraction of requests, and the
tightened timeout increases retry rate as more requests now exceed 15
seconds under real load. Each retry consumes a full additional inference
pass.

When someone finally computes cost-per-accepted-summary across both
teams' data six weeks later, it has risen 18% despite the 34% throughput
improvement: the extra tokens generated per GPU-hour were disproportionately
spent on truncated summaries needing regeneration and retried timed-out
requests, not on more successful summaries delivered per dollar.
```

## Statistics
| Finding | Context |
|---------|---------|
| Throughput-focused optimizations that also tighten per-request limits (token caps, timeouts) commonly increase retry/regeneration rate by 10-25% | Estimated range based on typical timeout/truncation-driven retry patterns |
| Cost-per-successful-output can move in the opposite direction of raw throughput metrics in a meaningful minority of infrastructure optimization initiatives when success rate isn't jointly measured | Typical pattern observed where throughput and success-rate ownership are organizationally separated |
| Joining serving-layer throughput data with downstream success/outcome data typically lags the throughput metric's availability by weeks, delaying detection of a success-rate regression | Estimated range based on typical cross-team data pipeline latency |

## Mitigations
1. **Define and jointly track cost-per-successful-outcome as the primary KPI**: Establish a single metric that divides total inference cost by successfully completed tasks (not raw requests or tokens), owned jointly by infrastructure and product teams, so a throughput win that hurts success rate can't be reported as an unqualified success.
2. **Gate infrastructure optimizations on downstream success-rate metrics, not just throughput benchmarks**: Require any throughput-improving change (quantization, token caps, timeout adjustments, batch tuning) to pass a downstream task-success or retry-rate check before full rollout, not just a speed/volume load test.
3. **Close the data-latency gap between serving metrics and outcome metrics**: Invest in a pipeline that joins serving-layer data with downstream outcome data on a short cycle (days, not weeks), so a success-rate regression from a throughput change is detectable while the change is still fresh and easy to attribute.
4. **Align team incentives across the throughput/success boundary**: Avoid measuring infrastructure teams solely on metrics like tokens/sec or GPU utilization that can be improved at the expense of a metric owned elsewhere; include a shared or cross-checked success-rate metric in the same review.
5. **Treat retries and regenerations as a cost line, not free**: Explicitly cost-attribute retried and regenerated requests back to the change that caused the retry increase, so the true cost of a throughput optimization that increases retries is visible rather than absorbed into general serving spend.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cost_per_successful_outcome | Total inference cost divided by count of downstream-confirmed successful task completions | Alert if it rises > 10% following any throughput-focused infrastructure change |
| retry_regeneration_rate | Fraction of requests that result in a client-side retry or user-initiated regeneration | Alert if it rises > 15% relative following a serving-layer change |
| throughput_success_divergence | Directional comparison of raw throughput trend versus task-success-rate trend over the same period | Alert if throughput trends up while success rate trends down concurrently |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cost-per-successful-outcome regression | cost_per_successful_outcome rises > 10% within 4 weeks of a throughput-focused change | High | Review the recent change against success-rate impact; consider partial rollback |
| Throughput and success rate diverging | throughput_success_divergence shows sustained opposite trends for 2+ weeks | Medium | Cross-team review between infrastructure and product owners to identify the causal lever |

## Related Patterns
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - a specific case where a throughput-motivated latency change can trigger the retry/regeneration dynamics this pattern describes
- [Model Compression Failure](./model-compression-failure.md) - quantization done to raise throughput is a common concrete lever that can directly cause the success-rate regression this pattern measures
- [Speculative Execution Cost Waste](./speculative-execution-cost-waste.md) - another throughput-oriented optimization whose real economic value depends on a downstream success metric (acceptance rate) that's easy to stop monitoring
