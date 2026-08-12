# Multi-Agent Handoff Drops Maintenance-Window Suppression Flag Between Scheduler and Alert Router

## Issue: A Maintenance-Scheduling Agent That Reasons, in Its Own Planning Output, That a Specific Set of Alerts Should Be Suppressed During a Planned Maintenance Window Hands Off to the Alert-Routing Agent Through a Structured Calendar Entry That Carries Only the Window's Time Range, Not the Specific Alert-Suppression Scope It Actually Determined, So the Router Pages On-Call for Expected Noise

**Frequency**: Frequent

**Symptoms**
- The alert-routing agent pages on-call for every replica-3 alert that fires inside the maintenance window, including the latency and connection-pool alerts the scheduling agent had already reasoned should stay silent
- Before the window opens, the scheduling agent's planning transcript names the exact alert types to mute; none of that reasoning reaches the calendar entry the router actually reads, which carries only a start time, end time, and service name
- Muting an entire service for the duration of a window works without incident, because "everything off for replica-3" fits the existing time-range-plus-service fields; the failure surfaces specifically when only some of a service's alert types should go quiet while others stay live
- On-call engineers acknowledge and begin triaging each page before recognizing it maps to a maintenance window whose suppression scope had already been worked out
- The calendar system was adopted for this handoff because it already existed for scheduling meetings and generic maintenance windows -- alert-type granularity was never part of what it was built to hold

**Root Cause**
The scheduling agent's planning reasons at the level of individual alert types -- keep replica-3's error-rate alerts live, mute its latency and connection-pool alerts -- but writes that determination into a calendar entry whose schema (start_time, end_time, service) was inherited wholesale from generic meeting scheduling, a system that predates alert suppression as one of its uses. The alert-routing agent's matching logic was built against that same inherited schema, so it has no field to check for alert-type scope and no path back to the scheduling agent's planning narrative where that scope actually lives; a distinction the scheduling agent worked out in full is, from the router's perspective, simply absent.

**Example**
```
Scheduling agent plans a database maintenance window, reasoning: "This will cause expected latency spikes on the read-replica service; suppress latency and connection-pool alerts for replica-3 only, error-rate alerts should remain active"
Scheduling agent creates a calendar entry with start_time, end_time, and service: "replica-3" -- no field exists for which specific alert types to suppress
Alert-routing agent reads the calendar entry, sees only the time range and service name, and pages on-call for every replica-3 alert that fires during the window, including the expected latency spikes
On-call engineer acknowledges and investigates three pages before recognizing they correspond to the known maintenance window
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a constraint or conclusion established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent system designs are shown to require explicit, structured task and constraint specification between agents, since narrative planning output alone does not reliably propagate to a downstream agent acting on a fixed schema | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Multi-agent orchestration research for incident and operations workflows identifies structured state handoff fidelity, rather than individual agent accuracy, as the primary driver of downstream coordination failures | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |

**Contributing Factors**
- The calendar entry schema used for maintenance-window handoff has no field for alert-type or partial-suppression scope, only time range and service name
- The alert-routing agent's suppression logic checks only the structured calendar entry, never the scheduling agent's planning transcript
- No reconciliation step compares the suppression scope described in the scheduling agent's planning output against what the calendar entry actually encodes before the window goes active

---

## Mitigation Strategies

1. **Structured Suppression-Scope Field on Maintenance Windows**: Extend the calendar entry schema to carry an explicit, structured list of alert types or alert IDs to suppress, and require the scheduling agent to populate it directly from its own planning determination rather than leaving scope implicit in time range alone
2. **Pre-Window Suppression-Scope Reconciliation**: Before a maintenance window goes active, automatically compare the scheduling agent's planning transcript for suppression-scope language against the structured calendar entry, flagging any mismatch for review
3. **Default-to-No-Suppression on Missing Scope**: When a calendar entry has a time range but no structured suppression scope, default to full alert visibility (paging as normal) and surface a warning, rather than silently suppressing or silently paging through everything without review
4. **Post-Incident Suppression-Gap Logging**: Log every page acknowledged during an active maintenance window and review whether it corresponds to a suppression-scope gap, feeding recurring gaps back into schema design

### Metrics
- Rate of maintenance windows where the calendar entry has no structured suppression scope despite the scheduling agent's planning output specifying one
- Number of on-call pages acknowledged during active maintenance windows that correspond to expected, plannable noise
- Time between maintenance-window start and first suppression-gap-related page

### Alerts
- An on-call page fires for an alert type the scheduling agent's planning transcript explicitly intended to suppress during an active maintenance window → P2
- A maintenance window goes active with a calendar entry containing no structured suppression scope at all → P3
- Suppression-gap page rate during maintenance windows exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
