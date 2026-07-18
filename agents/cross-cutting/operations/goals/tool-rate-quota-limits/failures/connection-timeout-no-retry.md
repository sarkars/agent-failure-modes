# Connection Timeout No Retry

## Issue
A tool call's underlying TCP/TLS connection times out — a transient blip caused by network jitter, a brief DNS hiccup, or a momentary vendor load spike — and the agent has no retry logic wrapping the call. Instead of treating the timeout as a one-off, recoverable event, the agent surfaces it as a hard tool failure: it aborts the current task, marks the tool "unavailable," or hands the user a generic error, even though a second attempt a moment later would very likely have succeeded.

**Frequency**: Very Common

**Symptoms**
- A single connection timeout causes the agent to abandon an entire multi-step task rather than just the one call
- The same tool call succeeds on manual re-run seconds after the agent reported failure
- Error logs show exactly one attempt per failed call — no retry attempts, no backoff, no second connection
- Task failure rate spikes during known network-flaky periods (e.g., cross-region calls, VPN handoffs, vendor deploys) without any change in the tool's actual availability
- Users report "it worked when I tried it again" as their primary workaround

## Root Cause
Many tool-calling code paths are written assuming the happy path and propagate the first exception straight up the call stack without any retry wrapper, on the (often implicit) assumption that the underlying HTTP client or SDK already retries transient failures — which most do not by default for connection-level timeouts (as opposed to idempotent GETs in a handful of libraries). A `ConnectTimeout` or `ReadTimeout` is functionally indistinguishable, without explicit handling, from a permanent failure like an invalid API key, so the agent's error-handling logic treats both identically: fail fast, surface to the caller, stop.

## Example
```
An agent's "OrderLookup" step calls the InventoryAPI connector to check stock for a customer's order. The underlying network path crosses a load balancer that is mid-rollout, causing a 1.5-second connection stall.

The InventoryAPI client's default connect timeout is 1 second.
The call raises ConnectTimeoutError after 1 second — the request never even reached the server.
The agent's tool-call wrapper has no try/retry logic around this call; it catches the exception, logs "InventoryAPI unavailable," and returns a failure to the orchestrator.
The orchestrator, seeing a hard tool failure, aborts the entire "process customer order" workflow and tells the user to "try again later," even though the load balancer rollout finished 400ms after the timeout and the very next request would have connected in 60ms.
```

## Statistics
| Finding | Context |
|---------|---------|
| 60-80% of tool-call connection timeouts in production agent systems are transient and would succeed on an immediate retry | Typical of cloud-hosted API traffic patterns |
| Agents lacking any retry wrapper report 2-4x higher end-to-end task failure rates than functionally identical agents with a basic exponential-backoff retry on connection errors | Comparison across agent deployments with and without retry middleware |
| Adding a bounded 2-3 attempt retry with jittered backoff typically reduces connection-timeout-driven task failures by over 70% | Typical outcome of retry middleware rollout |

## Mitigations
1. **Wrap all tool calls in a bounded retry with backoff**: Apply a standard retry policy (e.g., 3 attempts, exponential backoff with jitter, starting at 200-500ms) specifically for connection-level errors (`ConnectTimeout`, `ConnectionResetError`, DNS failures), distinct from application-level errors like 4xx responses which should not be blindly retried.
2. **Distinguish transient from permanent failures**: Classify exceptions explicitly — connection timeouts, resets, and 502/503/504 are retryable; 401/403/404/422 are not — so the retry layer doesn't waste attempts on errors that will never succeed, and doesn't give up on ones that would.
3. **Set connect timeouts realistically, not aggressively**: Tune the connect-timeout value against observed p99 connection-establishment latency for the tool rather than an arbitrary short default, so normal network variance doesn't masquerade as a hard failure in the first place.
4. **Fail the call, not the task**: Structure orchestration so a single tool-call failure after exhausting retries surfaces as a retryable sub-task failure, allowing the orchestrator to retry or route around it, rather than cascading into aborting the whole multi-step workflow.
5. **Log attempt count and outcome per call**: Emit structured logs recording every retry attempt and its result, so post-incident analysis can tell "one blip, recovered" apart from "genuinely down" without guesswork.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.connection_timeout_rate` | Fraction of tool calls failing with a connection-level timeout (pre-retry) | Alert if exceeds 5% over a 10-minute window |
| `tool.retry_success_rate` | Fraction of retried connection timeouts that succeeded on attempt 2 or 3 | If this stays high (>60%) but no retry logic exists, flag as a missing-mitigation gap |
| `task.abort_on_single_tool_failure` | Count of tasks aborted after exactly one tool-call failure | Alert if greater than 0 for tools known to have retry logic configured |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retry-less timeout cascade | Task abort rate spikes in lockstep with connection-timeout rate, with zero recorded retry attempts | Warning | Confirm retry middleware is deployed and wrapping this tool's call path |
| Sustained connection failures post-retry | `connection_timeout_rate` stays above 5% even after 3 retries per call | Critical | Escalate to vendor; this is no longer transient |

## Related Patterns
- [Connection Pool Exhaustion](./connection-pool-exhaustion.md) - a different cause of connection-layer failure that is also frequently missing retry handling
- [Rate Limit Grace Period Missing](./rate-limit-grace-period-missing.md) - both involve an agent giving up too early instead of backing off and retrying
- [Adaptive Rate Limiting](./adaptive-rate-limiting.md) - retry strategy design overlaps: both need backoff tuned to the failure's actual transience rather than a fixed assumption
