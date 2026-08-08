# Over-Trusting Confidence Score

## Issue: Agent treats model/OCR confidence as correctness.

**Frequency**: Common

**Symptoms**
- High confidence but source mismatch.
- Auto-accept logic lets outputs above a raw confidence threshold skip human review entirely, and a nonzero share of those high-confidence outputs later turn out to be wrong when spot-checked against ground truth.
- Confidence scores stay uniformly high even as input quality degrades (blurry scans, out-of-distribution document types), because the score was never calibrated against a labeled dataset for this task.

**Root Cause**
This happens because confidence scores are typically used operationally straight out of the model or vendor default, never calibrated against a labeled ground-truth dataset that would reveal what a given score actually means for this task, and no independent source cross-check is required for high-stakes fields even when the reported confidence is high. Thresholds are usually set once at launch and left unrevisited as the input distribution shifts -- new vendors, layouts, or locales -- even though models and OCR systems are known to be systematically overconfident on exactly this kind of out-of-distribution input, a failure mode that goes unmonitored because no one is specifically watching for it.

**Example**
```
An invoice-processing pipeline uses OCR confidence >= 0.95 as the bar for auto-posting
extracted line-item totals without human review. A new vendor starts sending invoices in
a slightly different layout. The OCR model reports 0.97 confidence on the extracted total
-- it's reading the number cleanly -- but it's reading the wrong field (a subtotal instead
of the grand total) because the new layout shifted column positions. The pipeline
auto-posts the wrong amount because confidence was treated as a proxy for correctness
rather than being calibrated or cross-checked against a source total.
```

**Contributing Factors**
- Confidence scores are used operationally straight out of the vendor/model default without ever being calibrated against a labeled ground-truth dataset for this specific task.
- No independent source/ground-truth cross-check is required for high-stakes fields even when confidence is high, so a confidently-wrong extraction sails through.
- Confidence thresholds are set once at launch and never revisited as input distribution shifts (new document layouts, new vendors, new locales).
- Models and OCR systems are systematically overconfident on out-of-distribution inputs, and this failure mode isn't monitored for specifically.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| High-confidence wrong-field extraction | New vendor invoice layout with shifted column positions, OCR confidence >= 0.95 | Extracted total is cross-checked against source and routed to review on mismatch | Wrong field auto-posted despite high confidence, no source cross-check performed |
| Calibration curve validation | Labeled ground-truth dataset scored for reliability diagram/Brier score | Calibration curve matches expected confidence-to-accuracy relationship | High-confidence bucket shows a nontrivial real error rate |
| Out-of-distribution confidence check | Document type/locale never seen in training data | Confidence score reflects genuine uncertainty (lower) or triggers review | Model reports high confidence on an out-of-distribution input it gets wrong |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| high_confidence_error_rate_pct | < 1% (errors within the "high confidence" bucket) | Sample high-confidence outputs and check against ground truth |
| calibration_curve_deviation_ece | Expected Calibration Error < 0.05 | Compute reliability diagram/ECE against a labeled ground-truth dataset |
| source_verification_override_rate_pct | Tracked, no fixed target | Track how often independent source-verification overrides a high-confidence extraction |

---

## Mitigation Strategies

### Prevention
1. **Confidence Calibration Against Ground Truth**: Before using any confidence score operationally, calibrate it against a labeled ground-truth dataset (reliability diagrams / Brier score) to establish what a given confidence value actually means for that model on that task; never assume raw confidence equals probability of correctness.
2. **Independent Verification Regardless of Confidence Tier**: Require a source/ground-truth cross-check for high-stakes fields even when confidence is high, since calibration studies consistently show models and OCR systems can be confidently wrong, especially out-of-distribution.
3. **Confidence-Threshold Policy Tied to Task Risk, Not Model Output Alone**: Set operational thresholds using calibrated confidence combined with task risk tier, and validate the threshold-setting process against real error rates periodically rather than setting it once from vendor defaults.

### Detection & Response
1. **High-Confidence Error Rate Monitoring**: Sample high-confidence outputs and check them against ground truth specifically (not just low-confidence ones); track the error rate within the "high confidence" bucket, since a nonzero rate there means the confidence signal is being over-trusted.
2. **Confidence Drift Detection**: Monitor the confidence-score distribution over time and by input segment (document type, locale, image quality); a shift without a corresponding recalibration signals that current thresholds no longer reflect true accuracy.
3. **Confidence-vs-Outcome Correlation Audits**: Periodically recompute the calibration curve using fresh production-labeled data and compare to the original calibration; recalibrate or lower trust in the signal if drift is found.

### Architecture Patterns
1. **Calibration Layer Between Raw Score and Decision Logic**: A dedicated calibration service converts raw model/OCR confidence into a calibrated probability-of-correctness using a held-out labeled dataset, and all downstream routing/decision logic consumes the calibrated value, not the raw score.
2. **Confidence + Source-Verification Dual Gate**: Routing logic requires both a calibrated confidence above threshold AND an independent source/ground-truth match before treating an extracted value as final; either check failing routes to human review.
3. **Continuous Recalibration Pipeline**: A scheduled job recomputes calibration curves from newly labeled production samples and automatically updates operational thresholds, flagging significant calibration drift for human review rather than silently auto-adjusting on high-stakes tasks.

### Metrics
1. **high_confidence_error_rate_pct**: Target: < 1% (errors within the "high confidence" bucket); Alert threshold: > 3%
2. **calibration_curve_deviation_ece**: Target: Expected Calibration Error < 0.05; Alert threshold: > 0.15
3. **confidence_distribution_drift_score**: Target: stable month-over-month; Alert threshold: significant shift (e.g., > 2 std dev) without recalibration
4. **source_verification_override_rate_pct**: Target: tracked, no fixed target; Alert threshold: sudden spike indicates confidence signal degrading

### Alerts
1. **High-Confidence Error Rate Exceeds Threshold** (P1 - Critical): Condition - sampled audit finds high-confidence bucket error rate above 3%. Action: Suspend auto-accept on high-confidence outputs for the affected task/segment, force human review pending recalibration.
2. **Calibration Drift Detected** (P2 - Warning): Condition - Expected Calibration Error exceeds 0.15 versus last validated calibration. Action: Trigger recalibration pipeline, review recent input distribution changes (new document types, locales, image quality).
3. **Confidence Distribution Shift** (P3 - Info): Condition - confidence score distribution shifts significantly without matching recalibration. Action: Investigate input pipeline changes, schedule recalibration review.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| high_confidence_error_rate_pct | > 3% |
| calibration_curve_deviation_ece | > 0.15 |
| confidence_distribution_drift_score | > 2 std dev shift without recalibration |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High-Confidence Error Rate Exceeds Threshold | Sampled audit finds high-confidence bucket error rate above 3% | High |
| Calibration Drift Detected | Expected Calibration Error exceeds 0.15 versus last validated calibration | Medium |
| Confidence Distribution Shift | Confidence score distribution shifts significantly without matching recalibration | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
