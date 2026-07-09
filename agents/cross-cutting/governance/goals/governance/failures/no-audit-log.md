# No Audit Log

## Issue: Cannot reconstruct what the agent saw, decided, and did.

**Frequency**: Common

**Symptoms**
- Missing trace/tool/action logs.
- [Add more specific symptoms]

**Root Cause**
Cannot reconstruct what the agent saw, decided, and did.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
