# Escalation Not Triggered

## Issue: Agent Fails to Escalate to Human When Required

**Frequency**: Common

**Symptoms**
- High-risk actions executed without human review
- Threshold conditions met but no escalation sent
- Edge cases fall through escalation logic
- Escalation rules outdated or misconfigured
- Agent proceeds autonomously on ambiguous cases

**Root Cause**
Escalation triggers depend on correctly configured thresholds, properly evaluated conditions, and functioning notification systems. When any component fails—thresholds set too high, conditions not checked, notifications silently dropped—the agent proceeds without required human oversight. This is especially problematic when escalation logic doesn't account for edge cases or when confidence scores are miscalibrated.

**Example**
```
Scenario: Financial transaction agent with escalation rules

Escalation rules:
  - Escalate if amount > $10,000
  - Escalate if recipient is new
  - Escalate if confidence < 80%

Transaction:
  Amount: $9,999 (just under threshold)
  Recipient: Shell company (technically "existing" - used once 2 years ago)
  Confidence: 79.5% (rounds to 80% in display)
  
Agent evaluation:
  Amount check: $9,999 <= $10,000 ✓ No escalation
  Recipient check: Found in database ✓ No escalation  
  Confidence check: 80% >= 80% ✓ No escalation
  
Result: Transaction processed without human review

Post-incident analysis:
  - Amount was deliberately structured to avoid threshold
  - "Existing" recipient was suspicious dormant account
  - Confidence rounding masked uncertainty
  - No compound risk assessment
  - Fraud loss: $9,999
```

**Key Statistics**
From Operations Research (2026):
- 28% of escalations fail due to misconfigured thresholds
- 45% of escalation rules have untested edge cases
- 67% of missed escalations involve threshold boundary cases
- Average time to detect missed escalation: 3-7 days
- 52% of organizations review escalation thresholds less than annually

**Contributing Factors**
- Static thresholds that don't adapt to context
- Rounding errors in threshold comparisons
- Missing compound condition checks
- Notification system failures
- Outdated escalation rules
- No fallback escalation path

## Mitigation Strategies

### Prevention
1. **Fuzzy/margin-based thresholds instead of hard cutoffs**: Escalate whenever a value falls within a margin of the threshold (e.g., $9,000–$10,000 for a $10K cutoff), not just strictly over it — directly closes the example's $9,999-just-under-$10,000 structuring gap. Trade-off: widens the escalation net and increases approver workload, requiring the margin to be tuned against actual false-escalation cost.
2. **Compound risk scoring instead of independent per-condition checks**: Combine amount, recipient novelty, and confidence into a single risk score rather than evaluating each rule independently and only escalating if any one individually crosses its threshold — the example's transaction passed all three checks individually while being highly suspicious in combination (near-threshold amount + dormant shell recipient + borderline confidence). Trade-off: a compound scoring model is harder to reason about and audit than simple independent rules, and needs its own calibration and testing.
3. **Confidence-value floor before display rounding**: Evaluate escalation conditions against the raw confidence value, not a rounded display value — the example's 79.5% rounding to "80%" masked genuine uncertainty that should have triggered escalation. Trade-off: requires auditing every place a value is rounded for display versus used for a decision, since rounding-for-decision bugs are easy to reintroduce elsewhere.

### Detection & Response
1. **Threshold-boundary transaction sampling**: Specifically sample and review transactions that fall just under any escalation threshold (the exact pattern the example's fraud exploited), since boundary cases are disproportionately likely to be either deliberately structured or genuinely ambiguous.
2. **Shadow escalation logging**: Log what would have escalated under a stricter/fuzzy threshold or compound score, even while the current rules don't trigger it, to build a dataset for tuning thresholds and to retroactively catch missed cases like the $9,999 transaction within days rather than the reported 3–7 day average detection lag.
3. **Escalation-rate trend monitoring**: Track escalation rate over time and alert on unexplained drops, since a sudden drop can indicate either a genuine change in transaction mix or a broken/misconfigured threshold silently suppressing escalations.

### Architecture Patterns
1. **Compound risk-scoring service as a single escalation gate**: Replace independent boolean rule checks with a unified risk-scoring service that all escalation-relevant factors feed into, producing one score compared against a single escalate/proceed threshold. Deployment consideration: requires building and validating a risk model, which is more engineering investment than independent threshold rules but closes the compound-risk blind spot structurally.
2. **Default-to-escalate under uncertainty**: Architect the escalation decision so that any evaluation failure, missing data, or borderline confidence defaults to escalating rather than proceeding — inverting the current "escalate only on explicit trigger" design. Deployment consideration: increases human review load, especially during the rollout period before thresholds are well-tuned.
3. **Escalation-delivery confirmation loop**: Require positive confirmation that an escalation notification was received and acted upon (not just "sent"), since a silently dropped notification is functionally identical to escalation never being triggered. Deployment consideration: needs a read-receipt or acknowledgment mechanism integrated into the notification channel, which not all channels natively support.

### Metrics
1. **threshold_boundary_transaction_rate**: % of transactions falling within a defined margin of any escalation threshold; track as a leading indicator, not necessarily an alert on its own; report weekly.
2. **missed_escalation_rate**: % of transactions later found (via fraud/incident review) that should have escalated under a corrected/compound rule but didn't; target < 0.5%; alert if > 2%.
3. **escalation_rate_deviation**: Standard deviations from the rolling-30-day-average escalation rate; target within ±2 SD; alert if a sudden drop exceeds 3 SD, signaling a possible broken rule.
4. **notification_delivery_confirmation_rate**: % of triggered escalations with confirmed receipt/action by the approver; target > 99%; alert if < 95%.

### Alerts
1. **Threshold-Structuring Pattern Detected** (P1): Condition — repeated transactions from the same account cluster just under an escalation threshold (threshold_boundary_transaction_rate spike for one account/recipient). Action: force escalation regardless of individual thresholds and flag the account for fraud review.
2. **Escalation Rate Anomalous Drop** (P1): Condition — escalation_rate_deviation exceeds 3 SD below the rolling average. Action: treat as a possible broken escalation rule; page the owning team to audit recent rule/config changes before more transactions process unescalated.
3. **Notification Delivery Failure** (P2): Condition — notification_delivery_confirmation_rate falls below 95%. Action: investigate the notification channel for silent failures and manually verify pending escalations were actually seen by an approver.

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight failures
- [Anthropic: Core Views on AI Safety](https://www.anthropic.com/research/core-views-on-ai-safety) - Importance of human oversight
- [AI Incident Database](https://incidentdatabase.ai/) - Escalation failure incidents
