# Retry Storms

## Issue: Aggressive Retries Multiply Costs

**Frequency**: Common

**Symptoms**
- Failed operations trigger immediate retries
- Multiple agents retry simultaneously
- Downstream services overwhelmed
- Costs multiply with each retry wave

**Root Cause**
Retry logic without proper backoff and coordination:
- No exponential backoff between retries
- Multiple agents not coordinating retry timing
- Retrying non-retriable errors
- No distinction between transient and permanent failures

**Example**
```
Agent 1: API fails, retry immediately
Agent 2: API fails, retry immediately  
Agent 3: API fails, retry immediately
(All hit rate limit)

All three retry simultaneously, all fail again
Repeat 100x before any succeeds

Result: 300 API calls instead of 3
```

## Mitigation Strategies

### Prevention
1. **Exponential backoff with jitter**: Since the example shows all three agents retrying "immediately" and hitting the rate limit "simultaneously," each retry must wait an exponentially increasing delay (e.g., 1s, 2s, 4s...) plus randomized jitter so agents don't resynchronize on the same retry tick, which is exactly what turned 3 failed calls into 300. Trade-off: backoff increases end-to-end latency for the operation that's retrying, which may be unacceptable for user-facing synchronous flows.
2. **Error classification gate before retry**: The root cause explicitly names "retrying non-retriable errors" and "no distinction between transient and permanent failures" — classify the failure (rate limit/timeout = retriable; auth error/bad request = terminal) before entering the retry path, so permanent failures fail fast instead of consuming a full retry budget for no chance of success. Trade-off: misclassifying a genuinely transient error as terminal causes an avoidable immediate failure.
3. **Retry budget ceiling per operation**: Cap total retries per logical operation (not per agent) so that even with backoff, a persistently failing dependency doesn't get hammered indefinitely across "100x" repeat cycles as in the example. Trade-off: a hard ceiling means some genuinely-recoverable-after-many-attempts operations will fail permanently instead of eventually succeeding.

### Detection & Response
1. **Retry-rate spike per operation type**: Monitor retry counts per operation/endpoint; a sudden multi-agent synchronized spike (the "300 API calls instead of 3" pattern) is directly visible as a retry-rate spike correlated across multiple agent instances hitting the same endpoint in the same window.
2. **Time-to-success-including-retries**: Track how long an operation takes end-to-end including all retry attempts; a blowout in this metric versus the no-retry baseline indicates the backoff/coordination strategy isn't preventing pile-up.
3. **Error-type-to-retry correlation**: Log which error types trigger retries; if non-transient errors (e.g., 400-class client errors) show up frequently in the retry log, the error classification gate described above is missing or misconfigured.

### Architecture Patterns
1. **Circuit breaker per downstream dependency**: Once failures for a given API/endpoint exceed a threshold within a window, open the circuit and fail fast for a cooldown period instead of letting every agent instance keep attempting calls, directly preventing the "repeat 100x" cascade in the example. Deployment consideration: circuit state should be shared (e.g., via a distributed cache) across agent instances, otherwise each agent maintains its own blind circuit and the storm still occurs collectively.
2. **Coordinated/shared backoff state**: Since the example's core problem is three independent agents each unaware of the others' retry timing, a shared rate-limit-aware coordinator (e.g., a token-bucket rate limiter agents check before retrying) prevents synchronized retry waves even when each agent has its own backoff logic. Deployment consideration: adds a shared-state dependency (cache/coordinator) that itself must be highly available, or it becomes a new single point of failure.
3. **Retry budget enforcement at the client library level**: Bake a global max-retry ceiling and jittered exponential backoff into the shared HTTP/API client library used by all agents, rather than leaving retry logic to be reimplemented per-agent inconsistently. Deployment consideration: requires auditing all call sites to ensure they route through the shared client rather than ad hoc retry loops.

### Metrics
1. **retry_rate_per_operation**: Target < 5% of calls requiring any retry under normal conditions; Alert if > 30% within a 5-minute window (signals a downstream degradation triggering storm risk).
2. **synchronized_retry_burst_count**: Target 0 detected bursts where 3+ agent instances retry the same operation within the same 1-second window; Alert if any burst detected (this is the exact precursor to the 3-calls-to-300-calls blowup).
3. **retry_amplification_factor**: Target < 3x (total calls including retries ÷ unique logical operations); Alert if > 20x (approaching the 100x observed in the example).
4. **non_retriable_error_retry_rate**: Target 0% of terminal/non-transient errors entering the retry path; Alert if > 1%.

### Alerts
1. **Retry-Storm-Detected** (P1): Condition - retry_amplification_factor exceeds 20x for any operation within a 10-minute window, or synchronized_retry_burst_count > 0. Action: trip the circuit breaker for the affected dependency immediately, page on-call, and check downstream service health before allowing retries to resume.
2. **Non-Retriable-Error-Looping** (P2): Condition - non_retriable_error_retry_rate exceeds 1% for a sustained period. Action: audit the error classification logic for the affected operation type and add the missing terminal-error rule.
3. **Backoff-Coordination-Gap** (P3): Condition - multiple distinct agent instances show retry timestamps clustering within the same sub-second window against a shared dependency. Action: verify jitter configuration is active and shared rate-limit coordination is functioning.

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including retry storms
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Overview of agent failure modes and mitigation strategies
