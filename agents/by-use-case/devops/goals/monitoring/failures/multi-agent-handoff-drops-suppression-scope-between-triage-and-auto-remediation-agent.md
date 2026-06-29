# Multi-Agent Handoff Drops Suppression Scope Between Triage and Auto-Remediation Agent

## Issue: A Triage Agent That Determines, in Its Own Reasoning, That a Specific Alert Pattern Is a Known False Positive Only Under a Narrow Set of Conditions -- e.g., During a Specific Nightly Batch Job's Run Window, for a Specific Metric Threshold -- Hands Off a Suppression Decision to a Downstream Auto-Remediation Agent Through a Structured Ticket That Carries Only the Alert Name and a Boolean Suppress Flag, Not the Conditions That Scoped the Suppression, So the Auto-Remediation Agent Suppresses the Same-Named Alert Unconditionally Going Forward, Including When It Fires for a Genuinely Different, Unrelated Cause

**Frequency**: Occasional

**Symptoms**
- Triage agent's reasoning explicitly scopes a false-positive determination to specific conditions (a time window, a specific job, a threshold range), but the structured suppression record contains only the alert name and a suppress flag
- Auto-remediation agent suppresses every subsequent firing of the same-named alert, including occurrences well outside the original scoping conditions
- A genuinely new incident sharing the same alert name as the previously-scoped false positive is auto-suppressed and never reaches on-call
- The suppression's original scoping conditions are recoverable from the triage agent's transcript, but the auto-remediation agent's workflow never consumes that transcript, only the structured suppress flag
- The pattern surfaces specifically when the same alert name later fires for an unrelated, genuine cause outside the original false-positive's narrow conditions

**Root Cause**
The structured suppression-record schema used for the handoff between the triage agent and the auto-remediation agent has a field for whether to suppress an alert by name, but no field for the conditions under which that suppression should apply. The triage agent's scoped reasoning -- correct and narrow when it was made -- is reduced to an unconditional boolean at the handoff boundary, so the auto-remediation agent has no way to distinguish "suppress this alert name always" from "suppress this alert name only under these specific conditions," even though the triage agent never intended the former.

**Example**
```
Nightly batch job "data-reindex" reliably triggers a transient "queue depth high" alert for 90 seconds during its known startup ramp, every night at 02:00 UTC
Triage agent investigates the first occurrence and concludes: "Confirmed false positive -- specific to data-reindex's startup ramp, 02:00-02:02 UTC window, queue depth 500-800 range; not a genuine issue"
Triage agent creates a suppression record: { alert_name: "queue-depth-high", suppress: true } -- no field exists for the time-window or job-specific scoping
Auto-remediation agent applies the suppression to all future firings of "queue-depth-high", at any time, for any cause
Three days later, "queue-depth-high" fires at 14:00 UTC due to a genuine consumer outage unrelated to data-reindex; auto-remediation agent suppresses it per the standing rule
Genuine incident goes unpaged for over an hour until a downstream effect (a separate alert) finally reaches on-call
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent failure analysis identifies information loss at agent-to-agent handoff boundaries -- where one agent's correctly-scoped internal determination is not propagated into the structured interface the next agent consumes -- as one of the most common recurring failure categories | [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) |
| Failure taxonomies for platform-orchestrated agentic workflows describe handoff schemas lacking fields for conditional context the upstream agent determined as a structural driver of downstream errors | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Multi-agent orchestration research for incident-response-adjacent workflows notes that decision quality downstream depends on what is explicitly carried across agent boundaries, not on what any single upstream agent internally concluded | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |

**Contributing Factors**
- Suppression-record schema has only a name-keyed boolean suppress flag, no field for scoping conditions (time window, source job, threshold range)
- Auto-remediation agent's workflow consumes only the structured suppression record, not the triage agent's investigation transcript
- No expiration or re-validation requirement on suppression records, so a narrowly-scoped determination persists indefinitely as if it were unconditional
- No check compares a newly-firing alert's context (time, magnitude, associated job) against the original suppression's scoping conditions before applying it

---

## Mitigation Strategies

1. **Structured Scoping Fields**: Extend the suppression-record schema to capture the specific conditions (time window, source job, threshold range) under which the triage agent determined an alert to be a false positive, not only the alert name
2. **Condition-Match Validation**: Require the auto-remediation agent to check a newly-firing alert's context against the suppression record's scoping conditions before applying suppression, rather than matching on alert name alone
3. **Suppression Expiration**: Default all suppression records to expire after a configurable window or number of occurrences, requiring re-confirmation rather than persisting indefinitely as an unconditional rule
4. **Transcript-Aware Suppression Review**: Periodically audit standing suppression records against the original triage transcript that justified them, flagging any suppression whose structured record is broader than the original reasoning

### Metrics
- Rate of suppressed alerts whose firing context falls outside the original suppression's scoping conditions
- Number of genuine incidents auto-suppressed under a same-named alert's standing suppression rule
- Mean age of active suppression records without re-validation against current firing context

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Out-of-scope suppression applied | A firing alert is suppressed despite its context (time, magnitude, source) falling outside the original suppression's scoping conditions | P1 | Un-suppress; page on-call; audit suppression record |
| Suppressed alert correlates with downstream incident | A suppressed alert's window overlaps with a separately-detected genuine incident | P1 | Treat as missed page; review suppression scoping enforcement |
| Stale unconditional suppression | A suppression record older than its review window has never been re-validated | P3 | Force re-validation against current alert-firing context |

---

## References

- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
