# Risk Severity Misclassification

## Issue: Agent treats critical issue as minor or vice versa.

**Frequency**: Common

**Symptoms**
- Escalation severity mismatch.
- [Add more specific symptoms]

**Root Cause**
Agent treats critical issue as minor or vice versa.

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
1. **Severity Rubric with Clear Criteria**: Define explicit rubric mapping issue characteristics to severity levels (P1/Critical, P2/High, P3/Medium, P4/Low). Example: 'IF security_breach THEN P1', 'IF customer_angry AND order_value > $1000 THEN P2'. Rubric version-controlled, reviewed by domain experts.
2. **Risk Scoring Framework**: Implement scoring model that computes risk_score based on: issue_type, customer_impact, financial_impact, time_sensitivity, systemic_risk. Score maps to severity level. Example: score_100+ = P1, score_50-99 = P2.
3. **Reviewer Calibration**: Periodically (monthly) run reviewer calibration session where domain experts review sample of classifications (50 issues). Measure agreement rate. If agreement < 90%, retrain rubric and team. Track calibration sessions in audit log.

### Detection & Response
1. **Severity Mismatch Detection**: For each issue, check classification against rubric. Alert if classification doesn't match rubric criteria (e.g., security_breach classified as P3 instead of P1). Log mismatch type, agent_id, expert_review_status.
2. **Escalation Speed vs Severity**: Monitor time-to-escalation by severity level. Alert if P1 issue not escalated within 30min, P2 within 4hrs, etc. Flag delayed escalations for investigation.
3. **Resolution Outcome Correlation**: Track issue outcomes by severity classification. Alert if high percentage of P4 classifications result in escalations (indicates misclassification). Conversely, alert if high P1 classifications resolve without action (false positives).

### Architecture Patterns
1. **Severity Classification Gate**: Pre-escalation, route all issues through severity classifier. Classifier outputs: severity_level, confidence_score, reasoning (which rubric criteria matched). Log all classifications with confidence.
2. **Multi-Reviewer Consensus for High-Risk**: For high-impact issue categories (security, financial, customer-facing), require 2-3 reviewers to agree on severity before escalation. Reduce false positives for high-consequence misclas sifications.
3. **Dynamic Severity Adjustment**: Allow expert reviewers to adjust agent's severity classification. Log all adjustments with reason. Use adjustment patterns to retrain rubric.

### Metrics
1. **severity_misclassification_rate_percent**: Target: < 2%; Alert threshold: > 5%; Track: under-classified (critical→minor), over-classified (minor→critical)
2. **p1_misclassification_rate_percent**: Target: < 1%; Critical issues under-classified are highest risk
3. **reviewer_agreement_rate_percent**: Target: > 90%; Measure rubric clarity via multi-reviewer agreement
4. **escalation_speed_by_severity_sla_met_percent**: Target: 100%; P1: 30min, P2: 4hrs, P3: 24hrs, P4: 48hrs
5. **severity_classification_confidence_avg**: Target: > 0.85; Alert if confidence < 0.70

### Alerts
1. **Critical Issue Misclassified as Minor** (P1 - Critical): Condition - P1-level issue classified as P3/P4. Action: Immediate reclassification, escalation, notify severity classification team, post-incident review.
2. **Escalation SLA Miss** (P2 - Warning): Condition - issue not escalated within SLA for its severity level. Action: Alert operator, manual escalation, investigate delay reason.
3. **Low Confidence Severity Classification** (P2 - Warning): Condition - classification confidence < 0.60. Action: Flag for secondary review, require 2-reviewer agreement, escalate to expert if disagreement.

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
