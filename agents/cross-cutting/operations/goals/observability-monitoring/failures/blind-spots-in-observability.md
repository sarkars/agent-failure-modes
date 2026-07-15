# Blind Spots in Observability

## Issue: Critical Failures Occur in Unmonitored Agent Code Paths

**Frequency**: Common

**Symptoms**
- Tool failures (API calls, database queries) not logged
- Silent retries happening without visibility
- Errors swallowed by exception handlers without alerting
- Performance degrades but no metrics show why
- Outages discovered by user complaints, not alerts
- Audit impossible: no trace of what agent did

**Root Cause**
When building agents, observability is often added reactively (after outages) rather than proactively. Critical code paths like tool calls, error handling, and retry logic have no logging or metrics. Failures are swallowed silently, degradation is invisible, and incident response requires reverse-engineering from user complaints.

**Example**
```
Agent Architecture:
├─ [Monitored] LLM call: Full logging, latency metrics ✓
├─ [Unmonitored] Tool call to external API: No logging ✗
├─ [Unmonitored] Retry logic: Silent retries, no count ✗
├─ [Unmonitored] Error handling: Exception caught, not logged ✗
├─ [Monitored] Final response: Logged ✓

Failure Scenario:
1. API call fails (timeout, 500 error) - NOT LOGGED
2. Retry 3 times - NO VISIBILITY
3. Exception caught in handler - SWALLOWED
4. Agent returns default response - LOOKS NORMAL
5. User sees wrong answer - DISCOVERS THE BUG

Result: 3-hour outage before anyone noticed
Cost: Customer complaints, lost trust, emergency response
```

**Key Statistics**
- 40-60% of agent codebases have blind spots in observability
- Tool failures are logged only 30-50% of the time
- Average MTTR with blind spots: 2-4 hours (vs. 15 minutes with full observability)
- 80% of production incidents traced to unmonitored code paths

**Contributing Factors**
- Observability seen as "non-critical" / "optimization"
- Instrumentation time-consuming, not prioritized
- No observability checklist at code review
- Error handling doesn't include logging
- Retry logic invisible (no attempt counter)

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent has multiple code paths: main flow, error handling, retries, tool calls
- Some paths are monitored (logs, metrics), others aren't
- Failure occurs in unmonitored path

### Trigger Mechanism
1. Identify unmonitored code paths (tool calls, retries, error handlers)
2. Inject failure into unmonitored path
3. Observe: No alert, no log, no visibility

**Example Reproduction Steps:**
```
1. Map agent code: main flow, error handling, retries, tool calls
2. Identify: Which paths are logged/metriced? Which aren't?
3. For each unmonitored path:
   a. Inject failure (timeout, exception, empty result)
   b. Observe: Agent behavior, logs produced, alerts fired
   c. Measure: Time to detection (user complaint vs. automated alert)
4. Calculate: % of code paths with zero observability
```

### Expected Failure State
- Failure occurs in unmonitored path
- No logs produced
- No metrics updated
- No alerts fire
- Failure invisible until user complains
- Debugging requires manual trace-through code

---

## Mitigation Strategies

### Prevention

1. **Observability as Non-Negotiable Requirement**: Add observability checklist to code review: "Tool calls logged? Retries metered? Errors include context?" Make observability as mandatory as error handling.

2. **Structured Logging Standard**: Require all critical operations (tool calls, retries, errors, state changes) to emit structured logs with: timestamp, operation, status, latency, relevant context. Use logging framework that enforces structure.

3. **Metrics for All Critical Paths**: Instrument: tool call success rate, retry counts, error rates, latency percentiles for each critical code path. No blind spots.

### Detection & Response

1. **Observability Gap Audits**: Periodically audit code to find unmonitored paths. Ask: "If this path fails silently, when would we notice?" If answer is "user complaint", that's a blind spot.

2. **Synthetic Testing of Monitoring**: Run synthetic tests that trigger failures in critical paths. Verify: logs produced, metrics updated, alerts fire. If not, add instrumentation.

3. **Tool-Driven Observability**: Use APM (Application Performance Monitoring) tools to automatically instrument code. Don't rely on manual logging.

### Architecture Patterns

1. **Observability by Default with Minimal Opt-Out**: Framework automatically logs/metrics all function calls. Developers opt-out only if performance-critical. Invert default: instrument first, optimize after.

2. **Structured Logging with Context Propagation**: Every log entry includes: request_id, user_id, operation_name, status, duration, error (if any). Context automatically propagated through call stack.

3. **Metric Proxy Wrapping Critical Operations**:
   ```
   def call_tool(tool_name, params):
       with metrics.timer(f"tool_call.{tool_name}"):
           try:
               result = tool.execute(params)
               metrics.increment(f"tool_call.{tool_name}.success")
               return result
           except Exception as e:
               metrics.increment(f"tool_call.{tool_name}.failure")
               logger.error(f"Tool failed: {tool_name}", error=e, params=params)
               raise
   ```

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unmonitored_code_paths_percentage` | % of critical code paths with no instrumentation | >10% |
| `tool_call_visibility_rate` | % of tool calls that are logged | <95% |
| `error_logging_coverage` | % of exceptions that include structured logs | <90% |
| `retry_visibility` | % of retries that are metered | <80% |
| `mttr_vs_baseline` | MTTR compared to before-blind-spots | >2x |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Blind Spot Detected | Code path logs nothing when failure occurs | P1 | Add instrumentation immediately |
| Low Observability Coverage | Tool calls visibility <90% | P2 | Audit tool wrappers and add logging |
| Tool Failure Not Logged | Tool exception caught but not logged | P1 | Fix error handler to include logging |
| Retry Storm Not Metered | Multiple retries occurring without metrics | P2 | Add retry counter metrics |

### Dashboard Panels
- Panel 1: Observability coverage by component (% instrumented)
- Panel 2: Blind spots (unmonitored code paths)
- Panel 3: Tool call success rates (by tool)
- Panel 4: Error logging coverage (% with structured logs)
- Panel 5: MTTR trend (should improve with observability)

---

## References

- [Observability Engineering Book](https://www.oreilly.com/library/view/observability-engineering/9781492076438/) — Structured logging and observability principles
- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — Best practices for production systems
- [Distributed Tracing for Microservices](https://opentelemetry.io/) — OpenTelemetry standard for instrumentation
