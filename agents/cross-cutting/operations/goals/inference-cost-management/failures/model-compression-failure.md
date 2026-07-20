# Model Compression Failure

## Issue
A team quantizes or distills a model specifically to cut inference cost (smaller weights, faster kernels, cheaper hardware) and validates the change against an aggregate quality benchmark that looks acceptable, but the compression technique degrades a specific capability disproportionately — long-context recall, numerical precision, rare-token/tail-vocabulary generation, or multi-step tool-calling reliability — that the aggregate benchmark doesn't isolate. The compressed model ships, the cost savings materialize as planned, but a narrow slice of production traffic silently gets worse outputs, and the hidden quality cost (rework, escalations, lost trust) offsets or exceeds the infrastructure savings.

**Frequency**: Occasional

**Symptoms**
- Aggregate eval scores (accuracy, BLEU, general benchmark suites) look flat or only slightly down after compression, but a specific downstream task's success rate drops sharply
- User complaints or escalations cluster around a particular capability (e.g. numeric calculations, long-document summarization, structured tool-call output) not represented proportionally in the validation benchmark
- The compressed model's error mode is qualitatively different from the original's — confident wrong answers rather than uncertain ones — making automated quality gates less effective at catching it
- A/B tests comparing compressed vs. original show no statistically significant difference in a broad metric but a significant regression when segmented by request type
- Cost savings from compression are real and on-target, but support ticket volume or manual-review rate rises enough to erode or exceed the savings

## Root Cause
Quantization (reducing weight/activation precision, e.g. FP16 to INT8 or INT4) and distillation (training a smaller model to mimic a larger one's outputs) both compress information non-uniformly across a model's capabilities — some circuits and representations tolerate precision loss or capacity reduction gracefully, while others (often those handling long-range dependencies, precise numeric reasoning, or low-frequency patterns that the training distribution underrepresents) degrade sharply past a compression threshold. Standard validation practice evaluates compressed models against the same aggregate benchmarks used for the original model, because that's the fastest way to get a go/no-go signal, but aggregate benchmarks average across many capabilities and can hide a severe regression in one narrow area behind stable-or-improved performance in the many other areas that make up most of the benchmark's weight. The problem compounds because the team doing the compression optimization is typically infrastructure-focused and measuring against infrastructure-relevant metrics (latency, memory, cost) plus a generic quality gate, not against the task-specific evaluation suites that would catch capability-specific degradation — that evaluation typically lives with a different team, if it exists at all for the affected capability.

## Example
```
A finance-research agent's underlying 70B model is quantized from FP16 to
INT4 to cut GPU memory footprint by roughly 4x and reduce serving cost per
token by an estimated 55%. The validation process runs the standard
internal quality suite (MMLU-style multiple choice, general instruction
following, safety refusal rate) before and after quantization; all three
categories show less than 1.5% degradation, comfortably inside the
team's 3% acceptance threshold, and the quantized model ships fleet-wide.

Three weeks later, the finance-research agent's core task — extracting
specific dollar figures and percentages from SEC filings and performing
basic arithmetic on them (e.g. computing a year-over-year change) — shows
a spike in analyst-reported errors. Investigation finds the INT4
quantization disproportionately degraded the model's numeric-token
precision: figures like "$847.3M" get subtly misread or the arithmetic
on them comes out wrong at a rate the standard quality suite, which
contains almost no numeric-extraction-and-computation tasks, never
exercised.

A targeted eval built after the incident shows the quantized model's
accuracy on a numeric-extraction-and-arithmetic benchmark dropped from
91% (original) to 68% (INT4), a regression invisible in the original
validation. The team estimates the resulting analyst rework and two
externally-reported financial-figure errors cost more in remediation
than the quantization saved in infrastructure over the following
quarter, and rolls back to FP16 for the finance-research workload
specifically while keeping INT4 for less numerically-sensitive agents.
```

## Statistics
| Finding | Context |
|---------|---------|
| Aggressive quantization (below INT8, e.g. INT4 or lower) commonly causes disproportionate degradation on numeric reasoning and long-context recall tasks relative to general benchmark performance | Typical range observed in quantization-impact studies |
| Aggregate benchmark score changes of under 2% after compression can co-occur with 15-30% relative degradation on narrow, underrepresented task categories | Estimated range based on capability-segmented evaluation comparisons |
| Distillation to a smaller model commonly preserves 90%+ of aggregate benchmark performance while showing larger relative drops specifically on tail-vocabulary or rare-pattern generation tasks | Typical range from teacher-student distillation case studies |

## Mitigations
1. **Task-specific evaluation suites before shipping compression**: Build or source narrow, task-specific benchmarks (numeric reasoning, long-context recall, structured output/tool-calling reliability) that mirror actual production capability requirements, and require them to pass alongside aggregate benchmarks before a compressed model ships.
2. **Segment quality gates by request type in production A/B tests**: When comparing compressed and original models, evaluate outcome metrics segmented by request category, not only in aggregate, so a regression concentrated in one segment isn't averaged away by stable performance elsewhere.
3. **Capability-aware compression targeting**: Apply different compression levels to different deployment contexts — e.g. reserve full precision for numerically- or precision-sensitive workloads while using aggressive quantization for conversational/low-stakes workloads — rather than a single fleet-wide compression decision.
4. **Shadow-mode canary before full cutover**: Run the compressed model in shadow mode against a sample of live traffic, comparing its outputs to the original model's on the same inputs, and flag divergences for manual review before full rollout, rather than relying solely on pre-deployment benchmarks.
5. **Cross-functional sign-off from capability owners**: Require teams that own specific downstream capabilities (numeric extraction, tool-calling, long-document tasks) to review and sign off on compression changes affecting their models, closing the gap between infrastructure-driven optimization and task-specific quality ownership.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| task_specific_eval_delta | Change in task-specific benchmark score after a compression change, per capability category | Alert if any category regresses > 5% |
| segment_error_rate_delta | Change in error/escalation rate segmented by request type, pre- vs. post-compression | Alert if any segment regresses > 10% relative |
| shadow_mode_divergence_rate | Rate at which compressed-model outputs diverge materially from original-model outputs on the same live inputs | Alert if divergence rate exceeds the pre-agreed threshold for a given task category |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Task-specific regression detected | task_specific_eval_delta shows > 5% degradation on any tracked capability after compression | High | Halt or roll back rollout for affected workload; escalate to capability owner |
| Segment-specific production error spike | segment_error_rate_delta exceeds 10% relative increase for any request-type segment post-compression | High | Investigate correlation with compression rollout; consider workload-specific precision exemption |

## Related Patterns
- [Quantization Accuracy Degradation Undetected](./quantization-accuracy-degradation-undetected.md) - the specific case of this pattern where the undetected regression is a general accuracy drop rather than a capability-specific one; the two often co-occur
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - a compression change that increases rework/escalation cost is a direct instance of raw throughput improving while cost-per-successful-output worsens
- [Speculative Execution Cost Waste](./speculative-execution-cost-waste.md) - another cost-motivated inference optimization technique that can carry hidden quality or efficiency costs not visible in aggregate metrics
