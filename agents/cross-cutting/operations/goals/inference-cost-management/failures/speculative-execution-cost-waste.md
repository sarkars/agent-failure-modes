# Speculative Execution Cost Waste

## Issue
Speculative decoding (using a small, cheap draft model to propose several tokens ahead, then verifying them in one pass with the large target model) and similar speculative-execution techniques are adopted to cut inference latency and cost by accepting multiple tokens per verification pass instead of one. When the draft model's acceptance rate is low — because it's poorly matched to the target model's distribution, the task domain shifted away from what the draft model was tuned on, or decoding parameters weren't retuned after a target-model update — the technique burns extra compute generating and verifying draft tokens that get rejected, and the workload ends up paying for both the draft model's compute and largely wasted target-model verification passes, sometimes at a higher total cost per accepted token than standard autoregressive decoding would have cost outright.

**Frequency**: Rare

**Symptoms**
- Draft-token acceptance rate is well below the level that was measured or expected when speculative decoding was adopted (e.g. dropping from a validated 65% to an actual 20-30% in production)
- Cost-per-accepted-token with speculative decoding enabled is at or above the cost-per-token of standard autoregressive decoding for the same workload, negating the intended savings
- Acceptance rate varies sharply by request type or domain, with certain traffic segments performing far worse than the aggregate number suggests
- A recent target-model version upgrade or a shift in the traffic mix (new use case, new customer segment) precedes a decline in acceptance rate that wasn't caught because acceptance rate isn't monitored as an ongoing production metric
- GPU utilization is elevated relative to tokens actually delivered to users, because rejected draft tokens still consumed compute for both proposal and verification

## Root Cause
Speculative decoding's cost savings depend entirely on the draft model's proposals being accepted often enough that the extra draft-generation compute is more than offset by the reduced number of full target-model forward passes needed. The draft model is typically a much smaller model distilled or selected to approximate the target model's output distribution on a validation set representative of the traffic at adoption time; if the draft model was never really well-matched (chosen mainly for being cheap and fast rather than for measured distributional similarity), or if the target model is later upgraded to a new version with a meaningfully different output distribution, or if the traffic mix shifts toward domains, styles, or languages the draft model wasn't tuned on, the acceptance rate silently degrades. Because speculative decoding is usually adopted once as an infrastructure optimization and then left running rather than continuously monitored against its assumed acceptance rate, a degradation isn't caught until someone compares actual cost outcomes to the projected savings — and by then the technique may have been quietly costing more than plain decoding for an extended period, with the loss disguised inside an aggregate "GPU cost" line that doesn't distinguish accepted-token efficiency from wasted speculative compute.

## Example
```
A code-completion agent adopts speculative decoding, pairing a 1B-parameter
draft model with a 34B-parameter target model, after validation showing a
68% token-acceptance rate on a benchmark of common code-completion
patterns (Python, JavaScript, mainstream library usage). The team
projects a 40% reduction in cost-per-generated-token and ships it as the
default decoding path.

Six months later, the product expands to support a new user segment:
data-science notebook completions involving heavy use of specialized
scientific-computing libraries and LaTeX-formatted markdown cells, a
domain the original draft model was never trained or validated against.
This segment grows to 35% of total traffic.

Nobody re-validates the draft model against the new segment's
distribution, and acceptance rate isn't tracked as an ongoing dashboard
metric, only measured once during initial adoption. On the data-science
segment specifically, acceptance rate is actually 22%, well below the
threshold at which speculative decoding remains cost-effective given the
1B draft model's own non-trivial compute cost.

A quarterly cost review, prompted by GPU spend not falling as fast as
traffic-adjusted projections expected, finds that the data-science
segment's effective cost-per-token with speculative decoding enabled is
actually 12% higher than a same-segment estimate of plain autoregressive
decoding would have been — the draft model's wasted proposal compute on
this segment exceeded the savings from its successful proposals on the
rest of the traffic mix.
```

## Statistics
| Finding | Context |
|---------|---------|
| Speculative decoding acceptance rates commonly range from 50-75% on well-matched draft/target/domain combinations but can fall below 30% on domain-mismatched traffic | Typical range across published speculative-decoding evaluations |
| Below an acceptance-rate threshold specific to the draft/target model size ratio (commonly somewhere in the 30-40% range), speculative decoding's compute overhead can exceed its savings, making it more expensive than standard decoding | Typical range depending on draft-to-target model size ratio |
| A target-model version upgrade or a 20%+ shift in traffic-domain mix is a common trigger for a material, uncaught acceptance-rate decline | Estimated pattern based on typical causes of speculative-decoding regression |

## Mitigations
1. **Monitor acceptance rate as an ongoing production metric, not a one-time validation number**: Track draft-token acceptance rate continuously in production, segmented by traffic domain/type, so a decline is caught as it happens rather than discovered in a periodic cost review.
2. **Re-validate the draft model whenever the target model changes**: Treat any target-model version upgrade as a trigger to re-measure acceptance rate and re-tune or re-select the draft model, rather than assuming the pairing remains well-matched across target-model versions.
3. **Segment-aware speculative decoding**: Disable or use a differently-tuned draft model for traffic segments with measured low acceptance rates, rather than applying one draft model uniformly across a traffic mix with heterogeneous domains.
4. **Automatic fallback to standard decoding below an acceptance-rate floor**: Configure the serving layer to detect when rolling acceptance rate for a segment drops below the cost-effectiveness threshold and automatically fall back to standard autoregressive decoding for that segment until the draft model is retuned.
5. **Report cost-per-accepted-token as a named metric, not folded into aggregate GPU cost**: Track and report the actual realized savings (or loss) from speculative decoding as an explicit line item, so a degradation shows up as a clear signal rather than being invisible inside a general infrastructure cost trend.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| draft_token_acceptance_rate | Fraction of draft-proposed tokens accepted by the target model verification pass, segmented by traffic domain | Alert if any segment drops below the cost-effectiveness threshold (e.g. < 35%) |
| speculative_decoding_cost_delta | Measured cost-per-token with speculative decoding versus an estimated cost-per-token under standard decoding for the same traffic | Alert if delta turns positive (speculative decoding costing more) |
| acceptance_rate_segment_variance | Spread of acceptance rate across traffic segments | Alert if variance widens significantly versus the baseline established at adoption |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Acceptance rate below cost-effectiveness floor | draft_token_acceptance_rate falls below the segment-specific breakeven threshold | High | Trigger automatic fallback to standard decoding for the affected segment; schedule draft-model re-tuning |
| Speculative decoding costing more than standard decoding | speculative_decoding_cost_delta turns positive for 24+ hours | High | Audit recent target-model or traffic-mix changes; consider disabling speculative decoding pending investigation |

## Related Patterns
- [Model Compression Failure](./model-compression-failure.md) - both are cost-motivated inference optimizations that can silently underperform their design intent on a subset of traffic
- [Batch Cost Inefficiency](./batch-cost-inefficiency.md) - both describe throughput-oriented optimizations whose benefit depends on a matching assumption (batch fill rate, acceptance rate) that can quietly break
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - wasted speculative compute is a direct mechanism by which raw throughput metrics can look fine while cost-per-successful-output worsens
