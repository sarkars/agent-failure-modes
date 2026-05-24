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

**Mitigation Strategies**
1. **Fuzzy thresholds**: Escalate when "close to" threshold, not just over
2. **Compound risk scoring**: Consider multiple factors together
3. **Escalation confirmation**: Verify escalation was received
4. **Regular threshold review**: Quarterly audit of escalation rules
5. **Shadow escalation**: Log what would have escalated for analysis
6. **Default to escalate**: When uncertain, escalate rather than proceed

**Detection**
- Monitor escalation rates over time (sudden drops = potential issue)
- Sample non-escalated actions for review
- Track threshold boundary transactions
- Alert on notification delivery failures
- Audit escalation rule coverage

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight failures
- [Anthropic: Core Views on AI Safety](https://www.anthropic.com/research/core-views-on-ai-safety) - Importance of human oversight
- [AI Incident Database](https://incidentdatabase.ai/) - Escalation failure incidents
