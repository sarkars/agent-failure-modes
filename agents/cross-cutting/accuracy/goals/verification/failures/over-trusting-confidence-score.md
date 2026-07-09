# Over-Trusting Confidence Score

## Issue: Agent treats model/OCR confidence as correctness.

**Frequency**: Common

**Symptoms**
- High confidence but source mismatch.
- [Add more specific symptoms]

**Root Cause**
Agent treats model/OCR confidence as correctness.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
