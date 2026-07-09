# Learning From Bad Feedback

## Issue: Agent updates behavior based on incorrect/noisy feedback.

**Frequency**: Common

**Symptoms**
- Performance worsens after feedback ingestion.
- [Add more specific symptoms]

**Root Cause**
Agent updates behavior based on incorrect/noisy feedback.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
