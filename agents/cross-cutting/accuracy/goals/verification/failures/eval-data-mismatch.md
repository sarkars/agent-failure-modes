# Eval-Data Mismatch

## Issue: Tests do not represent production inputs.

**Frequency**: Common

**Symptoms**
- Good eval score but production failures.
- [Add more specific symptoms]

**Root Cause**
Tests do not represent production inputs.

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
1. **Production Trace Sampling Pipeline**: Continuously sample real production requests/traces (stratified by intent, locale, channel), scrub PII, and add to the eval corpus on a rolling basis (e.g., weekly refresh with 5-10% of new traffic). Ensures the eval set tracks distributional drift instead of freezing at a launch snapshot.
2. **Distributional Drift Detection Before Eval Sign-Off**: Compute feature-level distance (embedding centroid shift, token-length histogram, intent-frequency KL divergence) between the eval set and the last N days of production traffic; block eval sign-off if divergence exceeds threshold.
3. **Stratified Eval Construction by Production Segments**: Partition the eval set using real segment weights (customer tier, locale, channel, query complexity) pulled from production analytics rather than hand-picked examples, so rare-but-frequent-in-prod segments aren't underrepresented.

### Detection & Response
1. **Eval-vs-Production Score Correlation Tracking**: Log per-release eval score alongside a matched production quality score (from sampled human review or downstream outcome); alert when correlation breaks down, i.e. eval flat/up while production quality drops.
2. **Shadow Evaluation on Live Traffic**: Run the eval suite's rubric against a sampled slice of real production outputs weekly; compare pass rate to the static eval suite's pass rate and flag divergence beyond a set delta.
3. **Post-Release Production Failure Triage Loop**: Tag every production incident/complaint as "eval would have caught" or "eval gap"; convert gaps into new eval cases within a fixed SLA.

### Architecture Patterns
1. **Continuous Eval Refresh Service**: Scheduled job that pulls stratified production samples, runs PII scrubbing, dedupes against existing eval cases, and stages new candidates for human labeling before merge into the eval set.
2. **Eval Set Versioning with Freshness Metadata**: Each eval case stores collection_date and source_distribution tags; CI blocks merges when the eval set's median age exceeds a staleness threshold (e.g., 90 days).
3. **Dual-Track Scoring Dashboard**: A single dashboard plots static eval score and shadow-production score on the same timeline per model/prompt version, making mismatch visible to reviewers before ship decisions.

### Metrics
1. **eval_prod_distribution_divergence**: Target: < 0.1 (normalized embedding/KL distance); Alert threshold: > 0.25
2. **eval_set_median_age_days**: Target: < 30 days; Alert threshold: > 90 days
3. **eval_vs_shadow_score_delta_pct**: Target: < 5%; Alert threshold: > 15%
4. **eval_gap_conversion_rate_pct**: Target: > 90% of flagged gaps become eval cases within 2 weeks; Alert threshold: < 60%

### Alerts
1. **Eval-Production Divergence Spike** (P1 - Critical): Condition - distributional divergence exceeds 0.25 or shadow score drops >15% below static eval score for two consecutive releases. Action: Freeze release sign-off gated on this eval suite, trigger emergency eval refresh.
2. **Eval Set Staleness** (P2 - Warning): Condition - eval set median age exceeds 90 days without refresh. Action: Schedule mandatory refresh sprint before the next major release.
3. **Unconverted Production Gaps** (P3 - Info): Condition - more than 10 flagged production gaps sit unconverted to eval cases past SLA. Action: Notify eval owner, add to backlog grooming.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
