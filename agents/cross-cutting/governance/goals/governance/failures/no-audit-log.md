# No Audit Log

## Issue: Cannot reconstruct what the agent saw, decided, and did.

**Frequency**: Common

**Symptoms**
- Missing trace/tool/action logs.
- Incident responders cannot reconstruct the sequence of tool calls that led to a bad outcome, so root-cause analysis stalls.
- Compliance requests for "show us what the agent did for user X" cannot be fulfilled.
- Disputes with users about what the agent said or did cannot be resolved because no record exists to check against.

**Root Cause**
Logging is architected as an afterthought bolted onto execution rather than a precondition for it, so an action can complete and its log write can simply fail with nothing blocking the action or raising an alarm. Without a shared trace_id threading the user's input, the agent's reasoning, and the resulting tool calls into one chain, and with log schemas that vary by integration so some actions are richly captured while others are barely noted, gaps accumulate invisibly — and because no one monitors the logging pipeline itself for silent failures, those gaps are only discovered after an incident forces a manual reconstruction.

**Example**
```
A user disputes that the agent authorized a $2,300 charge on their
account, claiming they never approved it. Support pulls up the case to
verify.

The agent's runtime logs only the final API call result ("charge:
success"), not the reasoning that led to it, the user message that
triggered it, or which tool the agent selected and why. There is no
trace_id linking the charge back to the specific conversation turn.

Support cannot confirm or refute the user's claim. The charge is
refunded as a precaution, and the incident is escalated to engineering,
who spend two days manually correlating disparate application logs to
reconstruct what likely happened — with no certainty the reconstruction
is complete.
```

**Contributing Factors**
- Logging is treated as a best-effort side effect of execution rather than a hard precondition for it.
- No shared trace_id links the user's input, the agent's reasoning, and the resulting tool calls into a single reconstructable chain.
- Log schema is inconsistent across tools/integrations, so some actions are logged richly and others barely at all.
- Logging pipeline failures are not monitored, so gaps accumulate silently until an incident forces someone to notice.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Full chain reconstruction | A completed agent session with multiple tool calls | Perceive-decide-act chain is fully reconstructable from trace_id | One or more steps in the chain are missing from the log |
| Log-then-act enforcement | Simulated logging service outage during an action attempt | Action is blocked until log write is confirmed | Action executes despite failed log write |
| Retention retrievability | Query a log record within its required retention window | Record is retrievable | Record is missing or inaccessible before retention period ends |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| trace_reconstruction_success_rate | 100% | Sample completed sessions and verify each can be fully replayed from trace_id alone |
| log_then_act_enforcement_rate | 100% | Simulate logging failures and verify no downstream action executes without a confirmed write |
| retention_retrieval_success_rate | 100% | Query logs at random points within the retention window and confirm successful retrieval |

---

## Mitigation Strategies

### Prevention
1. **Mandatory Structured Trace Logging**: Instrument the agent runtime to emit a structured event for every perception (input received), decision (reasoning/tool selection), and action (tool call + result) with a shared trace_id, before the agent is allowed to run in any environment above local dev. No action executes without a preceding log write succeeding.
2. **Immutable Append-Only Storage**: Write trace logs to an append-only store (e.g., write-once object storage or an event log with retention lock) so records cannot be edited or deleted post-hoc, including by the agent itself or by engineers under incident pressure.
3. **Schema Enforcement at Write Time**: Require every trace event to conform to a fixed schema (timestamp, trace_id, agent_id, actor, input_snapshot, decision_rationale, tool_calls, output, session_id) validated at write time, so gaps or malformed entries are rejected rather than silently accepted as partial logs.

### Detection & Response
1. **Trace Completeness Monitoring**: For every agent session, verify that the full perceive-decide-act chain is present (no orphaned actions without a preceding decision event, no decisions without a logged input). Flag sessions with gaps as incomplete audit trails.
2. **Log Pipeline Health Checks**: Monitor the logging pipeline itself (ingestion lag, write failure rate, storage availability) since a failure here silently produces the exact blind spot this pattern describes. Alert on any drop in event volume relative to agent activity volume.
3. **Retention Compliance Scanning**: Periodically verify that logs older than the review window but within the required retention period are still retrievable, and that no logs have been deleted ahead of their retention policy.

### Architecture Patterns
1. **Centralized Trace Collector**: Route all agent perceive/decide/act events through a dedicated logging service (e.g., OpenTelemetry-style collector) that stamps each event with trace_id and session_id, decoupled from the agent process so a crashed or compromised agent can't suppress its own logging.
2. **Log-Then-Act Enforcement**: Architect the action-execution path so the tool-call dispatcher requires a confirmed log write acknowledgment before forwarding the call to the underlying tool/API, making logging a hard dependency of execution rather than a best-effort side effect.
3. **Session Replay Service**: Build a query/replay layer over the trace store that reconstructs a full session timeline (input to output) for a given trace_id, used by incident responders and auditors instead of grepping raw logs.

### Metrics
1. **trace_completeness_rate_percent**: Target: 100%; Alert threshold: < 99.5% of sessions have full perceive-decide-act chains
2. **log_write_failure_rate_percent**: Target: < 0.01%; Alert threshold: > 0.1%
3. **logging_pipeline_lag_seconds**: Target: < 5s p99; Alert threshold: > 60s
4. **retention_compliance_rate_percent**: Target: 100% of required-retention logs retrievable; Alert threshold: < 100%

### Alerts
1. **Action Without Log Record** (P1 - Critical): Condition - an executed agent action has no corresponding trace event. Action: Treat as a compliance incident, freeze the agent pending investigation, notify security and compliance.
2. **Logging Pipeline Degradation** (P1 - Critical): Condition - event ingestion volume drops sharply relative to agent activity. Action: Page on-call, consider pausing agent execution until logging is confirmed healthy.
3. **Retention Gap Detected** (P2 - Warning): Condition - logs within required retention window are missing or unretrievable. Action: Escalate to compliance, document gap for audit disclosure.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| trace_completeness_rate_percent | < 99.5% of sessions have full perceive-decide-act chains |
| log_write_failure_rate_percent | > 0.1% |
| logging_pipeline_lag_seconds | > 60s |
| retention_compliance_rate_percent | < 100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Action Without Log Record | Executed agent action has no corresponding trace event | Critical |
| Logging Pipeline Degradation | Event ingestion volume drops sharply relative to agent activity | Critical |
| Retention Gap Detected | Logs within required retention window are missing or unretrievable | Warning |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
