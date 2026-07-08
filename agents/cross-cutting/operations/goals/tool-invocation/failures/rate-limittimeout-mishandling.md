# Rate-Limit/Timeout Mishandling

## Issue: Agent fails silently or retries destructively after API limit/timeout.

**Frequency**: Common

**Symptoms**
- Repeated errors or duplicate actions.
- [Add more specific symptoms]

**Root Cause**
Agent fails silently or retries destructively after API limit/timeout.

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
1. **Exponential Backoff with Jitter**: All tool-calling clients implement capped exponential backoff with random jitter on 429/5xx/timeout responses, respecting any `Retry-After` header the API provides, rather than immediate or unbounded retries that compound rate-limit pressure.
2. **Idempotency-Keyed Retries**: Retries after a timeout reuse the same idempotency key as the original attempt, so a retry after an ambiguous timeout (the request may have succeeded server-side) cannot create a duplicate side effect.
3. **Retry Budget with Circuit Breaker**: Each tool integration has a bounded retry budget (e.g., max 3 attempts, max 30s total) and a circuit breaker that trips after repeated failures, forcing the agent to surface an explicit failure/degraded-mode message to the user instead of looping indefinitely or retrying destructively.

### Detection & Response
1. **Silent Failure Detection**: The tool-call wrapper distinguishes "call failed and was reported to the agent" from "call failed and the agent proceeded as if it succeeded"; any case where a 429/timeout response was followed by the agent asserting success is flagged as a silent-failure incident.
2. **Retry Storm Monitoring**: Aggregate retry counts per tool per minute are tracked; sudden spikes (many agents/sessions retrying the same failing endpoint) trigger an automatic circuit-breaker trip at the gateway level to protect the downstream API and prevent cascading rate-limit violations.
3. **Ambiguous-Outcome Reconciliation**: For write actions that timed out mid-flight, a reconciliation job checks the target system for whether the action actually completed (queries by idempotency key) rather than assuming failure, preventing both false "it failed" reports and blind re-execution.

### Architecture Patterns
1. **Resilient Tool-Call Gateway**: A shared gateway wraps all external tool calls with unified backoff, jitter, retry-budget, and circuit-breaker logic, so individual tool integrations don't each reinvent (and inconsistently implement) retry handling.
2. **Dead-Letter and Manual-Resume Queue**: Actions that exhaust their retry budget are moved to a dead-letter queue with full context (payload, idempotency key, error history) for either automated later retry once the rate-limit window resets, or human review, instead of being dropped.
3. **Timeout-Outcome Reconciler Service**: A background service specifically resolves "did this timed-out write actually happen?" by querying the target API for the idempotency key or a derived lookup, updating the action's status from "ambiguous" to "confirmed"/"confirmed-failed" before any retry is allowed to fire.

### Metrics
1. **silent_failure_incident_rate_percent**: Target: 0%; Alert threshold: > 0.1% of tool calls
2. **retry_success_rate_percent**: Target: > 90% of retried calls eventually succeed; Alert threshold: < 70%
3. **circuit_breaker_trip_count_per_day**: Target: < 2 per tool; Alert threshold: > 5 per tool
4. **ambiguous_timeout_unreconciled_count**: Target: 0 outstanding after 15 min; Alert threshold: > 10 outstanding

### Alerts
1. **Silent Failure Confirmed** (P1 - Critical): Condition - the agent reported success to the user despite an underlying 429/timeout/5xx response. Action: Immediate incident, notify affected user, audit the retry/error-handling code path.
2. **Circuit Breaker Tripped** (P2 - Warning): Condition - a tool's circuit breaker opens due to repeated failures. Action: Page tool owner, investigate upstream API health/rate-limit quota, communicate degraded mode to active sessions.
3. **Ambiguous Timeout Backlog Growing** (P2 - Warning): Condition - ambiguous_timeout_unreconciled_count exceeds threshold. Action: Scale up the reconciler service, manually review the oldest unreconciled actions to prevent duplicate retries.

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

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
