# Bad Concession/Commitment

## Issue: Agent promises refund, waiver, legal/commercial term, or SLA it cannot honor.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Unauthorized promise in transcript.
- [Add more specific symptoms]

**Root Cause**
Agent promises refund, waiver, legal/commercial term, or SLA it cannot honor.

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
1. **Commitment Allowlist with Authorization Levels**: Maintain allowlist of commitments agent can make (refund_up_to_$X, extension_up_to_Y_days, waive_fee_category_Z). Each commitment has: scope, max_amount/duration, approval_requirements, SLA. Agent can only make allowlisted commitments within bounds.
2. **Approval Gates for High-Impact Commitments**: High-impact commitments (multi-year contract modification, high-value refund, legal term change) require human approval before agent can promise. Agent drafts commitment, submits for approval, can only make commitment if approved.
3. **Commitment Verification Pre-Send**: Before sending response containing commitment, verify: commitment in allowlist, within authorization bounds, terms legally binding, required approvals obtained. Block response if verification fails.

### Detection & Response
1. **Unauthorized Commitment Detection**: Monitor all agent communications for commitments (refund, waiver, extension, SLA, legal term). Verify commitment against allowlist + bounds. Alert on unauthorized promises. Log in audit trail.
2. **Commitment Fulfillment Verification**: For each commitment made, verify it was fulfilled. Example: if agent promises 'refund within 48 hours', verify refund posted within 48hrs. Flag unfulfilled commitments.
3. **Commitment Context Analysis**: Analyze commitment patterns by agent. Alert if agent makes excessive high-value commitments (potential value-giveaway pattern). Alert if commitments frequently get challenged/reversed (indicates customer dissatisfaction with terms).

### Architecture Patterns
1. **Commitment Authorization Gate**: Before agent sends response containing commitment language, analyze text for commitment keywords/patterns. Extract commitment details. Verify against allowlist + bounds + approvals. Fail-closed: unauthorized commitment blocked.
2. **Commitment Tracking System**: Maintain commitment tracker linking: commitment_id, agent_id, customer_id, commitment_text, commitment_type, amount/duration, fulfillment_status, deadline, actual_fulfillment_date. Enable SLA tracking.
3. **Commitment Audit Trail**: Store all commitment-related events: agent_proposal, approval_request, approval_decision, commitment_communication_to_customer, fulfillment_attempt, fulfillment_status. Immutable for compliance.

### Metrics
1. **unauthorized_commitment_attempts_per_day**: Target: 0; Alert threshold: > 0; Any unauthorized attempt is critical
2. **commitment_authorization_coverage_percent**: Target: 100%; All commitment types in allowlist
3. **commitment_fulfillment_sla_met_rate_percent**: Target: 100%; All commitments honored on time
4. **high_value_commitment_density_per_agent**: Target: < 5% of interactions; Alert if > 10%
5. **commitment_reversal_rate_percent**: Target: < 1%; Reversals indicate misaligned commitments

### Alerts
1. **Unauthorized Commitment Detected** (P1 - Critical): Condition - agent promised commitment outside allowlist or bounds. Action: Block communication, alert compliance, require human review, potential customer outreach to clarify/renegotiate.
2. **Commitment Fulfillment Failure** (P1 - Critical): Condition - commitment not fulfilled by deadline (refund not posted, extension not applied, etc.). Action: Immediate escalation, fulfillment enforcement, customer compensation consideration.
3. **High-Value Commitment Abuse** (P2 - Warning): Condition - agent makes 5+ high-value commitments in 1 day or 20+ in 1 week. Action: Agent review, pattern investigation, potential authorization suspension.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
