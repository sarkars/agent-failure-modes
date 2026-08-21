# AI Agent Misclassifies Risk Severity: Causes and Fixes

## Issue: The agent treats a critical issue as minor, or a minor issue as critical, because its severity rubric relies on loose judgment instead of hard triggers.

**Frequency**: Common

**Symptoms**
- Escalation severity mismatch between what the agent assigned and what a reviewer would assign.
- A security or safety-relevant report is triaged as low priority and sits in a queue for days before anyone notices.
- Reviewers repeatedly override the agent's severity classification, but the pattern isn't fed back into the rubric.

**Root Cause**
The severity rubric's criteria are vague and not hardcoded to specific, unambiguous signals — "unauthorized access" isn't wired to force a P1 outcome the way a concrete rule would — so classification depends on a loose judgment call rather than a deterministic trigger. High routine-issue volume pushes that judgment toward the lower-effort default severity absent an unmistakable signal, and because the classifier attaches no confidence score or reasoning trace, a misclassification is indistinguishable from a correct one until someone manually reviews it. Reviewer overrides that would reveal the pattern never feed back into rubric refinement, so the same ambiguous criteria keep producing the same class of miss.

**Example**
```
A support agent receives a message reporting that a customer's account shows
signs of unauthorized access (login from an unrecognized country, password
reset the customer didn't request). The agent classifies it as a routine
"account access question" (P3) instead of a security incident (P1), so it
sits in the standard 24-hour queue instead of triggering immediate fraud-team
escalation. By the time it's reviewed, the attacker has already changed the
account's payment details.
```

**Contributing Factors**
- Severity rubric criteria are vague or not explicitly tied to specific issue signals (e.g., "unauthorized access" isn't hardcoded to trigger P1).
- No confidence score or reasoning trace attached to severity classification, making misclassifications hard to catch before escalation delay causes harm.
- High volume of routine issues creates pressure to default to lower severity absent an unambiguous signal.
- No feedback loop from reviewer overrides back into rubric refinement or agent retraining.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Security-signal issue | Message reports unrecognized login + unauthorized password reset | Classified P1, immediate fraud-team escalation | Classified P3/routine, no immediate escalation |
| Ambiguous severity | Issue with mixed signals (minor complaint but from a high-risk customer) | Agent's confidence score reflects ambiguity, routes to secondary review | Agent classifies confidently with no reasoning trace despite ambiguity |
| Routine low-risk issue | Standard order-status inquiry | Classified P4, no unnecessary escalation | Agent over-classifies routine issue as high severity |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| severity_misclassification_rate_eval_percent | < 2% | % of eval cases where classification doesn't match expert-labeled ground truth |
| p1_misclassification_rate_eval_percent | < 1% | % of eval cases where a true P1 issue is under-classified |

---

Fixing this means hardcoding unambiguous signals to force specific severity levels instead of leaving classification to a loose rubric.

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
| severity_misclassification_rate_percent | > 5% |
| p1_misclassification_rate_percent | > 1% |
| escalation_speed_by_severity_sla_met_percent | < 100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Issue Misclassified as Minor | P1-level issue classified as P3/P4 | Critical |
| Escalation SLA Miss | Issue not escalated within SLA for its severity level | Warning |
| Low Confidence Severity Classification | Classification confidence < 0.60 | Warning |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
