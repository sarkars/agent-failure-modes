# Silent Tool Failures

## Issue: Tools Fail Without Alerting the Agent

**Frequency**: Common

**Symptoms**
- Tool returns success but action didn't complete
- Partial execution not communicated
- Error swallowed by tool wrapper
- Agent proceeds assuming success

**Root Cause**
- Tools returning success on partial completion
- Error handling that catches and hides exceptions
- Async operations not confirming completion
- Tools not validating their own output

**Example**
```
Agent: send_notification(user_id: 123, message: "Alert!")

Tool response: { "status": "success" }

Reality: Notification service was down, message queued indefinitely

Agent tells user: "I've sent your notification"

Result: User never receives notification, thinks it was sent
```

### Domain Examples
The same mechanism — a tool call returns an error, timeout, or empty payload, and the agent's downstream narrative treats that absence of data as a substantive negative result rather than a failed check — recurs across domains, previously documented as separate by-use-case patterns before being consolidated here:
- **Content marketing / compliance**: a claim-substantiation database call returns a 500 with an empty body during a deployment window; the agent's compliance summary states "claim substantiation confirmed" instead of surfacing the failed lookup, and unsubstantiated content is published.
- **Insurance / policy renewal**: an MVR (motor-vehicle-record) lookup returns an empty payload during a provider rate-limit window; the agent narrates the renewal as "clean driving record confirmed" instead of a failed check, and a batch of renewals is priced without the verification that was supposed to happen.

In both cases the fix is identical to the notification example above: the tool/agent boundary must structurally distinguish "checked and found nothing" from "the check itself didn't happen," and the agent's narrative generation must be gated on that distinction rather than defaulting to the most fluent reading of an empty response.

---

## Test Scenario & Reproduction

### Scenario Setup
- Notification tool returns `{"status": "success"}` upon enqueue rather than confirmed delivery
- No downstream confirmation check or dead-letter/stuck-job monitoring
- Agent trusts the tool's reported status at face value with no independent verification

### Trigger Mechanism
1. Simulate the downstream notification service being unavailable (queue accepts messages but never delivers)
2. Have the agent call the notification tool as part of a normal task
3. Observe whether the tool reports success and whether the agent's user-facing message matches reality

**Example Reproduction Steps:**
```
1. Take the downstream notification service offline while leaving the queue accepting writes
2. Ask the agent to notify a user: send_notification(user_id: 123, message: "Alert!")
3. Capture the tool's raw response
4. Capture the agent's user-facing summary of the action
5. Check the downstream system's delivery log for whether the message was ever actually delivered
6. Measure: gap between claimed success and confirmed downstream delivery
```

### Expected Failure State
- Tool returns `{"status": "success"}` despite the message being stuck in an undelivered queue
- Agent tells the user "I've sent your notification" with no caveat
- No stuck-job or claimed-vs-confirmed monitoring flags the discrepancy

---

## Mitigation Strategies

### Prevention
1. **Never return `{"status": "success"}` on enqueue alone**: The example failure is specifically that `send_notification` reported success the instant the message was queued, not when it was actually delivered — fix this by making the tool's success response contingent on confirmed delivery (or, for genuinely async operations, on returning an explicit `{"status": "queued", "job_id": ...}` rather than a bare "success"). Trade-off: waiting for true completion increases the tool call's latency, which is exactly why "async operations not confirming completion" became the shortcut in the first place.
2. **Ban blanket try/except that swallows exceptions without re-raising a structured signal**: Since the root cause names "error handling that catches and hides exceptions" as a direct driver, enforce (via lint rule or code review) that every except block in a tool implementation either re-raises or returns an explicit failure object — a bare `except: pass` or `except: return {"status": "success"}` should be treated as a bug class, not a style preference. Trade-off: requires auditing all existing tool implementations for this anti-pattern, which is a one-time but potentially large remediation effort.
3. **Require tools to validate their own output before returning success**: A notification tool should check the downstream service's actual response (was the message accepted for delivery, or just accepted into a local queue that may never drain) rather than assuming its own successful invocation implies the intended real-world effect happened — this directly targets "tools not validating their own output."

### Detection & Response
1. **Downstream confirmation rate tracking**: For every tool that reports success, independently verify against the actual downstream system state (e.g., did the notification service's delivery webhook fire) at a sampled rate; a gap between tool-reported success and confirmed downstream success is exactly the silent-failure pattern in the example.
2. **Queued-but-never-delivered tracking**: Since the example's root cause is "notification service was down, message queued indefinitely," specifically monitor queue age/depth for async operations and treat "success" responses whose underlying job never completes within an expected window as retroactive failures requiring an alert.
3. **User-facing claim vs. system-of-record mismatch audits**: Sample agent responses like "I've sent your notification" against the actual notification-service delivery log; any claim unsupported by a confirmed delivery record is a silent failure that reached the user undetected.

### Architecture Patterns
1. **Idempotent job-status pattern with explicit terminal states**: Return a job ID immediately for async operations like notification delivery, with defined states (`queued`, `sent`, `delivered`, `failed`) rather than a single premature "success," and require the agent (or a background poller) to check for a terminal state before telling the user it's done; deployment consideration — needs a job-status store with retention/TTL and a polling or webhook mechanism the agent can use.
2. **Dead-letter queue for stuck async jobs**: When a queued notification (or similar async action) doesn't reach a terminal state within an expected window, move it to a dead-letter queue and surface that as a distinct, alertable failure rather than letting it sit "queued indefinitely" as in the example; deployment consideration — requires defining a reasonable timeout per operation type, which varies (a notification vs. a batch report have very different normal durations).
3. **Health check before dispatch**: Check the dependent service's health/availability (e.g., is the notification service actually up) before accepting the request, so a known-down downstream produces an immediate, honest failure rather than a queued message with no realistic delivery prospect; deployment consideration — health checks add latency and can themselves be a source of false negatives if the check itself is flaky.

### Metrics
1. **claimed_vs_confirmed_success_gap**: Target < 0.5% of tool "success" responses lacking independent downstream confirmation; Alert if > 3% over a 1-hour window.
2. **async_job_stuck_rate**: Target < 1% of queued jobs failing to reach a terminal state within their expected SLA window; Alert if > 5%.
3. **swallowed_exception_count**: Target: 0 tool code paths with a bare except that doesn't re-raise or return a structured failure (enforced via static analysis); Alert on any new occurrence introduced in a code review/CI check.
4. **user_facing_false_success_rate**: Target: 0% of user-facing "I've done X" claims unsupported by a confirmed system-of-record success; Alert on any detected occurrence.

### Alerts
1. **Confirmed Silent Failure** (P1): Condition - a tool reported success but downstream confirmation shows the action never completed (e.g., notification never delivered). Action: page immediately, notify the affected user if identifiable, patch the tool to require real completion confirmation before reporting success.
2. **Async Job Stuck Beyond SLA** (P2): Condition - async_job_stuck_rate exceeds 5% for a given operation type over an hour. Action: investigate the downstream dependency's health, move affected jobs to the dead-letter queue, alert the owning team.
3. **New Swallowed-Exception Code Path** (P2): Condition - static analysis detects a new bare except/error-suppression pattern merged into a tool implementation. Action: block or flag the PR in review, require explicit structured error handling before merge.

## Related Patterns

**This pattern focuses on INDIVIDUAL TOOL failures that go undetected.**

For failures that propagate SILENTLY across a multi-stage pipeline (different stages using incomplete/degraded data), see:
- **[Silent Failures in Multi-Stage Pipelines](../../observability-monitoring/failures/silent-failures-in-multi-stage-pipelines.md)** — When failures occur silently at one stage but aren't caught before being used by downstream stages

For failures caused by insufficient observability/instrumentation, see:
- **[Blind Spots in Observability](../../observability-monitoring/failures/blind-spots-in-observability.md)** — When critical code paths are completely unmonitored

---

## References

- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - How silent errors go undetected in agent systems
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Common agent failure patterns including silent failures
