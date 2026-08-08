# Learning From Bad Feedback

## Issue: Agent updates behavior based on incorrect/noisy feedback.

**Frequency**: Common

**Symptoms**
- Performance worsens after feedback ingestion.
- A small number of mislabeled or adversarial ratings (e.g., coordinated brigading, a mis-clicked bulk-review tool) get weighted the same as trustworthy feedback and measurably shift the agent's policy.
- Gold-standard spot-check accuracy for a specific reviewer or automated grader quietly drops while their feedback keeps flowing into training unchanged.

**Root Cause**
Without gold-standard items seeded into review queues, there is no ongoing way to measure whether a given reviewer or automated grader's ratings are actually accurate, so a degraded or careless source can operate undetected indefinitely. Every feedback source is then weighted equally regardless of its (unmeasured) track record, and because incentive structures like per-item pay or throughput quotas reward reviewers for speed rather than accuracy, rubber-stamping becomes the path of least resistance under those incentives. With no pre- or post-ingestion eval regression check standing between a feedback batch and the training pipeline, a batch corrupted by one careless or adversarial source reaches production and measurably degrades behavior before anyone notices the quality of the underlying labels had dropped.

**Example**
```
A crowd-sourced rating panel is used to grade an agent's email-drafting suggestions. One contractor,
working through a large batch under a per-item time bonus, rates nearly every suggestion "excellent"
without reading them, including several drafts with factual errors and one with an inappropriate tone.
Because contractor accuracy isn't tracked against a gold-standard set, this batch is ingested at full
weight. The training update reinforces the exact behaviors (padding, unverified claims) that a careful
reviewer would have flagged, and post-deployment quality metrics drop over the following week.
```

**Contributing Factors**
- No gold-standard/spot-check items are seeded into review queues, so reviewer or grader accuracy cannot be measured against ground truth.
- Feedback sources are weighted equally regardless of historical accuracy, so a single degraded or adversarial source has full influence.
- Incentive structures (per-item pay, throughput quotas) reward reviewers for speed over accuracy, encouraging rubber-stamping.
- No pre/post-ingestion eval regression check exists, so a bad batch reaches production before anyone notices the quality drop.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Gold-standard seed accuracy check | Known-answer item seeded into a reviewer's queue disguised as real traffic | Reviewer/grader rating matches the known-correct label | Reviewer rates the seeded item incorrectly and this goes undetected |
| Rubber-stamped batch detection | Batch where >95% of items from one source receive an identical "excellent" rating regardless of content | Anomalous-pattern detector flags the batch for quarantine before ingestion | Batch is ingested at full weight with no anomaly flag |
| Post-ingestion eval regression | Full eval suite run before and after ingesting a synthetic bad-feedback batch | Regression is detected and the batch is blocked/rolled back automatically | Batch ships to production despite a measurable eval regression |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| reviewer_source_accuracy_vs_gold_standard_percent (eval) | > 90% | Score reviewer/source ratings on seeded gold-standard items against the known-correct label |
| post_ingestion_eval_regression_rate_percent (eval) | 0% | Run the fixed eval suite before and after simulated ingestion of a candidate feedback batch |
| anomalous_batch_detection_recall | > 95% | Inject synthetic corrupted/adversarial batches into a test harness and measure detection rate |

---

## Mitigation Strategies

### Prevention
1. **Feedback Validation Pipeline**: Run every incoming feedback batch through schema, sanity, and outlier checks (e.g., label contradicts an automatically verifiable fact, rating inconsistent with transcript content) before it is eligible to influence any update, catching corrupted or nonsensical labels at the door.
2. **Reviewer/Source Quality Scoring**: Maintain a rolling accuracy score for each feedback source (human reviewer, crowd panel, automated grader) measured against a gold-standard set, and weight or exclude low-scoring sources from contributing to behavior updates.
3. **Gold-Standard Spot-Check Injection**: Continuously seed review queues with known-answer items indistinguishable from real traffic; reviewer/source performance on these seeds is the primary, always-fresh signal for whether a feedback stream can currently be trusted.

### Detection & Response
1. **Post-Ingestion Performance Regression Monitoring**: Run the full eval suite immediately before and after each feedback batch is ingested into training; any regression beyond tolerance flags that batch as suspect before it reaches production.
2. **Anomalous Feedback Pattern Detection**: Apply statistical outlier detection to incoming label distributions (e.g., sudden shift in rating distribution from one source, coordinated identical ratings) that can indicate noisy, mistaken, or adversarial feedback.
3. **Automatic Rollback on Regression**: If a deployed update derived from a feedback batch causes an eval or production metric regression, automatically revert to the last-known-good model/prompt/policy state and freeze that feedback batch from further use pending investigation.

### Architecture Patterns
1. **Feedback Quality Gateway**: A pipeline stage sitting between raw feedback capture and the training/update system that validates, scores, and filters incoming feedback, rejecting or down-weighting batches that fail quality checks.
2. **Shadow Evaluation Before Promotion**: Every candidate update derived from new feedback is evaluated offline against a fixed, held-out benchmark before it is allowed to replace the production agent, catching bad-feedback-driven regressions pre-deployment.
3. **Versioned Update Ledger with Rollback**: Every production update is tied to the specific feedback batch and eval result that produced it, stored in a versioned ledger enabling one-click revert to any prior state when a batch is later found to be corrupted.

### Metrics
1. **reviewer_source_accuracy_vs_gold_standard_percent**: Target: > 90%; Alert threshold: < 75%
2. **post_ingestion_eval_regression_rate_percent**: Target: 0%; Alert threshold: any regression on a shipped update
3. **feedback_batch_rejection_rate_percent**: Target: < 10% (healthy pipeline); Alert threshold: > 30% (source degrading) or sudden 0% (validation bypassed)
4. **rollback_events_per_month**: Target: near 0; Alert threshold: > 2 in a rolling 30 days

### Alerts
1. **Post-Update Regression Detected** (P1 - Critical): Condition - eval or production metric regresses beyond tolerance after a feedback-driven update ships. Action: Auto-rollback to last-known-good state, freeze the responsible feedback batch, open incident for root-cause review.
2. **Feedback Source Accuracy Drop** (P2 - Warning): Condition - a reviewer/source's gold-standard accuracy drops below 75%. Action: Suspend that source's contribution weight to zero pending recalibration, audit recent batches from that source.
3. **Anomalous Label Pattern Flagged** (P3 - Info): Condition - outlier detection flags unusual distribution shift in incoming feedback. Action: Hold the batch in quarantine, route for manual spot-check before ingestion continues.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| post_ingestion_eval_regression_rate_percent | any regression on a shipped update |
| reviewer_source_accuracy_vs_gold_standard_percent | < 75% |
| rollback_events_per_month | > 2 in a rolling 30 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Post-Update Regression Detected | eval or production metric regresses beyond tolerance after a feedback-driven update ships | High |
| Feedback Source Accuracy Drop | a reviewer/source's gold-standard accuracy drops below 75% | Medium |
| Anomalous Label Pattern Flagged | outlier detection flags unusual distribution shift in incoming feedback | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
