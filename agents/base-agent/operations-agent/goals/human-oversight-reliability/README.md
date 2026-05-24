# Goal: Human Oversight Reliability

Ensure human oversight mechanisms function correctly in agent workflows. These failures occur when approval workflows break, escalations don't trigger, or human feedback isn't incorporated—distinct from security attacks on HitL controls.

## Business Context

- Critical actions require human approval before execution
- Escalation paths must trigger reliably when thresholds are exceeded
- Human feedback should influence agent behavior
- Approval workflows must handle edge cases (timeouts, unavailability)
- Compliance often mandates human sign-off for certain actions

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Escalation Not Triggered](failures/escalation-not-triggered.md) | Common | High |
| [Approval Timeout Mishandling](failures/approval-timeout-mishandling.md) | Common | High |
| [Stale Approval Reuse](failures/stale-approval-reuse.md) | Occasional | High |
| [Authority Mismatch](failures/authority-mismatch.md) | Occasional | High |
| [Feedback Not Incorporated](failures/feedback-not-incorporated.md) | Common | Medium |
| [Missing Approval Gates](failures/missing-approval-gates.md) | Common | High |
| [Approval Queue Overflow](failures/approval-queue-overflow.md) | Occasional | Medium |
| [Human Unavailability](failures/human-unavailability.md) | Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 73% of AI incidents involve inadequate human oversight | AI Incident Database 2026 |
| Average approval timeout: 4 hours, but 40% of actions can't wait | Enterprise workflow analysis |
| 28% of escalations fail due to misconfigured thresholds | Operations research |
| Human feedback incorporated in only 12% of agent corrections | LLM behavior studies |
| Approval fatigue leads to 60% rubber-stamping after 20+ requests | HitL research |

## Key Metrics

- Escalation trigger accuracy rate
- Approval timeout resolution rate
- Human feedback incorporation rate
- Approval authority verification rate
- Approval queue depth and latency

## Related Patterns

- [Human-Loop Bypass](../../security-agent/goals/safety-security/failures/human-loop-bypass.md) - Security attacks on HitL controls (different focus: attacks vs. operational failures)
