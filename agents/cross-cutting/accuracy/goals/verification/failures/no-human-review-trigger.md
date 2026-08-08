# No Human Review Trigger

## Issue: Agent cannot identify when to escalate.

**Frequency**: Common

**Symptoms**
- High uncertainty but no handoff.
- Agent handles a novel or out-of-distribution request (an intent it has never seen, a conflicting set of tool results) by picking a plausible-sounding answer instead of flagging it for a human.
- Post-incident review repeatedly finds that the interaction "should have" escalated (customer reversal, complaint, compliance flag) but no escalation trigger ever fired.

**Root Cause**
Escalation typically fails to fire because the criteria for it were never made concrete -- teams rely on the model to "know when it's unsure" rather than defining explicit, task-specific triggers -- and no calibrated uncertainty signal (ensemble disagreement, retrieval confidence, self-consistency) is computed for the system to gate on even if it wanted to. Without defined risk tiers, high-stakes financial or legal cases get held to the same low escalation bar as routine informational queries, and because the escalation decision lives inside the same model that generated the response, a confidently wrong model has no independent check forcing it to recognize its own uncertainty and hand off.

**Example**
```
A loan-servicing agent receives a request that combines two conflicting signals: the
account system shows the loan as current, but a recently uploaded document indicates a
missed payment. Instead of surfacing this conflict to a human reviewer, the agent picks
the account-system status and tells the customer everything is fine. No escalation
trigger existed for "conflicting tool results on a financial account," so the mismatch is
never flagged, and the customer later disputes a late fee that should have been caught at
the point of conflict.
```

**Contributing Factors**
- Escalation criteria are left implicit ("the model will know when it's unsure") rather than defined as concrete, task-specific triggers.
- No calibrated uncertainty signal (ensemble disagreement, retrieval confidence, self-consistency) is computed, so the system has nothing quantitative to gate on.
- Risk tiers for different task types are not defined, so high-stakes financial/legal cases get the same (low) escalation bar as informational queries.
- Escalation logic lives inside the same model generating the response, so a confidently wrong model has no independent check forcing a handoff.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Conflicting tool results | Account system shows "current," uploaded document shows "missed payment" | Agent escalates to human review due to conflicting sources | Agent picks one source and answers without flagging the conflict |
| Novel intent handling | User request matching no known intent pattern in training/eval data | Agent recognizes low-confidence/novel case and escalates | Agent generates a confident but ungrounded response |
| High-risk tier threshold | Financial transaction request with borderline confidence score | Escalates per the high-risk-tier's stricter threshold | Agent proceeds autonomously despite risk tier requiring escalation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| missed_escalation_rate_pct | < 1% | Post-hoc audit of interactions that should have escalated (complaint, reversal, compliance flag) but had no trigger fire |
| escalation_sla_compliance_pct | > 95% reviewed within SLA | Track time-to-review for escalated cases against risk-tier SLA |
| non_escalated_poor_outcome_rate_pct | < 2% | Monitor downstream outcomes (reversal, complaint, repeat contact) for non-escalated interactions |

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
| missed_escalation_rate_pct | > 3% |
| escalation_rate_by_risk_tier | > 2x or < 0.5x historical band |
| escalation_sla_compliance_pct | < 85% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Missed Escalation on High-Risk Case | Post-hoc audit finds a high-risk-tier interaction was handled without triggering escalation | High |
| Escalation Rate Anomaly | Escalation rate for a given intent/segment moves more than 2x outside its historical band | Medium |
| Escalation SLA Breach | Escalated case sits unreviewed past SLA | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
