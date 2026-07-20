# Quantization Accuracy Degradation Undetected

## Issue
A model is quantized to reduce inference cost, and the accuracy drop it introduces is real but small enough, or spread thinly enough across the output distribution, that pre-production evaluation — typically a quick smoke test or a comparison against a loose acceptance threshold — doesn't catch it. The quantized model ships to production because it "passed," and the accuracy gap only surfaces later through downstream signals (increased user corrections, retries, escalations, or a slow drift in a business metric) that take weeks to trace back to the quantization change, by which point the cost savings have been partly or fully offset by the quality cost, and root-causing requires reconstructing a change that's no longer top-of-mind.

**Frequency**: Common

**Symptoms**
- Pre-deployment evaluation shows the quantized model within an accepted tolerance (e.g. within 2% of the original on a standard benchmark), but the tolerance itself was set arbitrarily rather than validated against downstream business impact
- A slow, hard-to-attribute rise in user-initiated retries, corrections, or "regenerate response" actions begins shortly after a quantization rollout, but isn't immediately connected to the deployment
- Support or QA teams report a subjective sense that "the model got worse" weeks after quantization shipped, without a specific reproducible failure to point to
- A/B test between quantized and original models, if run at all, was underpowered (too short a duration or too small a sample) to detect a real but modest effect size
- The eval suite used for the go/no-go decision was the same generic suite used for every model change, not one calibrated to the sensitivity of this specific deployment's task

## Root Cause
Quantization's accuracy impact is usually small in aggregate — a few percentage points on standard benchmarks — which is exactly the range where statistical noise, benchmark selection, and threshold-setting decisions can mask a real regression. Teams under cost pressure to ship the savings quickly often run a single evaluation pass against a fixed threshold rather than a properly powered statistical comparison, and thresholds themselves are frequently set by convention ("anything under 2-3% degradation is fine") rather than by modeling what that degradation actually costs downstream in retries, escalations, or lost conversions. Because the effect is gradual and modest rather than a sharp failure, none of the fast-feedback signals a team relies on for catching regressions (crash rates, hard errors, obvious broken outputs) fire — the quantized model still produces plausible-looking answers, just wrong slightly more often, and that kind of degradation is invisible to monitoring that watches for failures rather than for a shift in output quality distribution. By the time an aggregate downstream metric (user satisfaction, task success rate, correction rate) drifts enough to be noticed, weeks of other changes have happened in parallel, making the quantization rollout one of many candidate causes rather than an obvious, isolated one.

## Example
```
A legal-document review agent's model is quantized from FP16 to INT8 to
cut GPU serving cost by roughly 40%. Pre-deployment validation runs the
team's standard 200-example QA benchmark; the quantized model scores
89.5% versus the original's 91.0%, a 1.5-point drop comfortably inside
the team's informal "under 3%" acceptance bar. The model ships.

Over the following 5 weeks, the rate at which reviewing attorneys flag an
agent-generated clause summary as "needs correction" rises gradually from
a baseline of 4.2% to 6.8%, but this coincides with the start of a new
contract-type intake (a plausible alternative explanation) and a UI
change to the flagging button (another plausible explanation), so it
isn't immediately attributed to the quantization.

A retrospective analysis six weeks post-launch, prompted by a client
complaint about a missed liability clause, re-runs both the original and
quantized models against a larger, stratified 2,000-example benchmark
specifically covering clause types by rarity. The quantized model shows
a 1.5% drop on common clause types (matching the original small-sample
result) but an 11% drop on rare clause types that make up only 8% of the
original 200-example benchmark but a disproportionate share of actual
client risk. The original benchmark's small sample and unstratified
composition had diluted a real, risk-concentrated regression into a
seemingly negligible aggregate number.
```

## Statistics
| Finding | Context |
|---------|---------|
| Small benchmark sets (under a few hundred examples) commonly lack statistical power to detect quantization-driven accuracy drops of 2-5%, the typical range quantization introduces | Typical range based on standard statistical power calculations for classification-style evals |
| Accuracy degradation from INT8 quantization is commonly under 2% in aggregate but can concentrate 3-8x more heavily in underrepresented input categories | Typical range observed across quantization-impact studies |
| Time-to-detection for a real but modest quantization regression, when relying on downstream business-metric drift rather than targeted evaluation, commonly runs 3-8 weeks | Estimated range based on typical incident-attribution timelines |

## Mitigations
1. **Properly powered, stratified evaluation before shipping**: Use evaluation sets large enough and stratified by input category (including rare/high-risk categories) to have statistical power to detect the modest degradation quantization typically causes, not a generic small smoke-test benchmark.
2. **Set acceptance thresholds from downstream cost, not convention**: Derive the acceptable accuracy-drop threshold from an actual model of downstream cost (rework, escalation, customer impact) for this specific task, rather than reusing a generic "under 3%" rule across all deployments regardless of stakes.
3. **Run a properly powered live A/B test, not just an offline eval**: Before full rollout, run the quantized model against a meaningful fraction of live traffic for long enough and at large enough sample size to detect a real effect on downstream metrics (correction rate, task success), rather than relying solely on a pre-deployment offline benchmark.
4. **Instrument output-quality-adjacent signals, not just error rates**: Track leading indicators of subtle quality regression — user correction rate, regenerate-response rate, downstream task success rate — as first-class monitored metrics that would catch a "still plausible, slightly worse" degradation that hard-failure monitoring misses.
5. **Tag and timestamp model-serving changes for fast attribution**: Maintain a clear, queryable changelog of quantization and other model-serving changes correlated with deployment timestamps, so a later metric-drift investigation can quickly check candidate causes instead of reconstructing history from memory.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| stratified_eval_accuracy_delta | Accuracy change between quantized and original model, computed per input-category stratum | Alert if any stratum regresses > 5% even if aggregate is within tolerance |
| user_correction_rate | Rate at which users flag, correct, or regenerate agent outputs | Alert if trending upward > 15% relative over a 4-week rolling window |
| downstream_task_success_rate | End-to-end task success metric tracked post-deployment | Alert if declining trend correlates temporally with a model-serving change |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Stratum-level accuracy regression | Any input-category stratum shows > 5% accuracy drop in pre-deployment stratified eval | High | Block rollout or restrict quantization to unaffected categories; investigate quantization-sensitive representations |
| Gradual downstream metric drift post-quantization | user_correction_rate or downstream_task_success_rate drifts unfavorably within 8 weeks of a quantization rollout | Medium | Cross-reference deployment changelog; run a targeted stratified re-evaluation |

## Related Patterns
- [Model Compression Failure](./model-compression-failure.md) - the broader pattern of compression breaking a specific capability; this pattern is the detection-gap variant where the regression is real but statistically invisible pre-deployment
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - undetected accuracy loss silently worsens cost-per-successful-output even while raw serving cost metrics look like a clean win
- [Batch Cost Inefficiency](./batch-cost-inefficiency.md) - both are cost-optimization efforts whose success is measured on an incomplete metric, hiding a real efficiency loss elsewhere
