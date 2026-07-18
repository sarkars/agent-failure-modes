# Approval Waiver Abuse

## Issue
An emergency waiver mechanism, designed to let an agent bypass the normal approval process under genuinely urgent conditions (an active outage, a security incident), gets invoked repeatedly for routine, non-urgent actions because it is faster and has less friction than the real approval path. Over time this erodes the approval control entirely: the "emergency" path becomes the default path, and the actions it was meant to gate no longer receive meaningful human review.

**Frequency**: Common

**Symptoms**
- Waiver usage rate climbing steadily rather than spiking only during actual incidents
- Waivers invoked for actions with no corresponding incident ticket or declared emergency
- The same requester or agent using waivers on a recurring schedule (e.g., every Friday deploy) rather than sporadically
- Post-hoc waiver justifications that are generic or copy-pasted rather than specific to an actual urgent event
- Waiver approval rate near 100% because the waiver itself requires little or no scrutiny by design

## Root Cause
Waiver mechanisms are deliberately built with low friction — that's what makes them useful in a genuine emergency — but low friction also makes them attractive as a way to route around the normal approval process when it's simply inconvenient or slow. Without usage monitoring, a mandatory linkage to a real incident record, or after-the-fact review, there is no counterforce pushing usage back toward genuinely urgent cases, so the population of waiver invocations gradually shifts toward routine use.

## Example
```
1. An organization introduces an emergency waiver: if an agent's action is
   tagged "incident-critical," it can proceed without waiting for standard
   approval, logged for after-the-fact review.
2. During a real outage, an engineer uses the waiver to push a critical fix,
   exactly as intended.
3. Two weeks later, facing a routine but time-pressured feature deadline,
   the same engineer tags a non-emergency deploy as "incident-critical" to
   skip the approval queue, without an actual incident open.
4. No one reviews waiver usage against actual incident records, so this
   goes unnoticed.
5. Other engineers observe that waivers are an easy way to move faster and
   begin using the same pattern for their own deploys.
6. Within a few months, a large share of production changes are going out
   under the "emergency" waiver path, and the standard approval process --
   still nominally in place -- reviews only a small minority of actual
   changes.
```

## Statistics
| Finding | Context |
|---------|---------|
| Waiver/emergency-bypass mechanisms, once introduced, are commonly observed to account for a growing share of total approvals over time absent active monitoring, in some cases reaching 20-30% of all approvals within a year | Typical drift pattern reported in change-management audits |
| A large share of waiver invocations reviewed after the fact lack a corresponding incident or emergency record | Common finding when waiver usage is not required to link to an incident system |
| Organizations that require waivers to link to an active incident ticket see substantially lower waiver-to-total-approval ratios than those that don't | Consistent with linkage acting as a natural throttle |

## Mitigations
1. **Mandatory incident linkage**: Require every waiver invocation to reference an active, verifiable incident or emergency record (e.g., an incident management system ticket) rather than accepting a free-text justification alone.
2. **Waiver usage rate monitoring with trend alerting**: Track waiver usage as a share of total approvals over time and alert when the ratio trends upward, rather than only reviewing waivers individually.
3. **Mandatory post-hoc review of every waiver**: Route every waiver invocation to a governance reviewer within a fixed window after use, with escalation if a pattern of non-emergency use is found for a given requester or team.
4. **Escalating friction for repeat waiver use**: Automatically increase scrutiny (e.g., require a second sign-off) for any requester or agent whose waiver usage exceeds a defined frequency threshold.
5. **Time-boxed and auto-expiring waiver grants**: Scope each waiver narrowly to the specific action and a short validity window, so it cannot be reused or stretched to cover unrelated subsequent actions.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `waiver_share_of_total_approvals` | Waivers as a percentage of all approval decisions in a rolling window | > 10% sustained over 30 days |
| `waiver_without_incident_link_rate` | Share of waiver invocations lacking a linked incident record | > 5% |
| `repeat_waiver_requester_count` | Number of requesters/agents exceeding a defined waiver-frequency threshold | > 0 requesters above threshold per month |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Waiver used without incident link | A waiver is invoked with no corresponding active incident record | Critical | Require immediate justification, flag for governance review within 24 hours |
| Waiver usage trending upward | Rolling waiver share of total approvals increases for 3+ consecutive review periods | Warning | Governance review of waiver policy and top requesters, consider tightening linkage requirements |

## Related Patterns
- [Approval Timeout Expiration](./approval-timeout-expiration.md) - both involve a path where an action proceeds without a genuine, scrutinized approval decision
- [Policy Exception Not Authorized](./policy-exception-not-authorized.md) - both involve a bypass mechanism used outside its intended, properly authorized scope
- [Approval Scope Mismatch](./approval-scope-mismatch.md) - both represent ways the real-world use of a control drifts from its documented intent
