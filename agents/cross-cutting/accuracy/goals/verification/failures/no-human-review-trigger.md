# No Human Review Trigger

## Issue: Agent cannot identify when to escalate.

**Frequency**: Common

**Symptoms**
- High uncertainty but no handoff.
- [Add more specific symptoms]

**Root Cause**
Agent cannot identify when to escalate.

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
1. **Explicit Escalation Criteria Definition**: Define concrete, task-specific triggers for human handoff (confidence below threshold, high-value/high-risk transaction, novel intent not seen in training data, conflicting tool results, explicit user request for a human) rather than relying on the model to organically decide to escalate.
2. **Uncertainty-Aware Response Gating**: Compute a calibrated uncertainty signal (ensemble disagreement, retrieval confidence, self-consistency across sampled generations) for each response and route below-threshold cases to human review before they reach the customer, rather than after.
3. **Risk-Tiered Escalation Policy**: Classify tasks by risk tier (informational vs. financial vs. legal/compliance) with tier-appropriate escalation thresholds — low-risk tasks tolerate higher autonomy, high-risk tiers escalate far more aggressively by design.

### Detection & Response
1. **Missed-Escalation Audit**: Sample production interactions that should have triggered escalation (via post-hoc analysis of outcome — customer complaint, reversal, compliance flag) and check whether the escalation trigger fired; track the miss rate.
2. **Escalation Rate Trend Monitoring**: Track the escalation rate over time per intent/segment; both an anomalously low rate (agent silently overconfident) and an anomalously high rate (trigger miscalibrated, over-escalating) are investigated.
3. **Downstream Outcome Correlation for Non-Escalated Cases**: For interactions the agent handled without escalation, monitor downstream outcomes (reversal, complaint, repeat contact) and feed cases with poor outcomes back into escalation-trigger calibration.

### Architecture Patterns
1. **Escalation Decision Layer**: A dedicated policy component evaluates uncertainty signals, risk tier, and business rules after the agent drafts a response but before delivery, and can force a human-in-the-loop handoff independent of the agent's own self-assessment.
2. **Confidence Calibration Service**: A separate calibration model/service converts raw model confidence or retrieval scores into a calibrated probability of correctness using held-out labeled data, since raw model confidence is poorly calibrated for escalation decisions.
3. **Human Review Queue with SLA Tracking**: Escalated cases route to a queue with priority based on risk tier, tracked against an SLA (e.g., high-risk escalations reviewed within 15 minutes), with automatic re-escalation if SLA is breached.

### Metrics
1. **missed_escalation_rate_pct**: Target: < 1% (post-hoc identified should-have-escalated cases without trigger); Alert threshold: > 3%
2. **escalation_rate_by_risk_tier**: Target: within historically calibrated band per tier; Alert threshold: > 2x or < 0.5x band
3. **escalation_sla_compliance_pct**: Target: > 95% reviewed within SLA; Alert threshold: < 85%
4. **non_escalated_poor_outcome_rate_pct**: Target: < 2%; Alert threshold: > 5%

### Alerts
1. **Missed Escalation on High-Risk Case** (P1 - Critical): Condition - post-hoc audit finds a high-risk-tier interaction (financial, legal, compliance) was handled without triggering escalation. Action: Immediate case review, customer outreach if needed, recalibrate trigger thresholds.
2. **Escalation Rate Anomaly** (P2 - Warning): Condition - escalation rate for a given intent/segment moves more than 2x outside its historical band. Action: Investigate trigger calibration or underlying intent-distribution shift.
3. **Escalation SLA Breach** (P2 - Warning): Condition - escalated case sits unreviewed past SLA. Action: Auto-reassign or re-escalate to backup reviewer, alert queue owner.

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
