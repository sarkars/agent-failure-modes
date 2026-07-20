# Concurrent Session Not Licensed

## Issue
A tool's license agreement caps the number of simultaneous active sessions (e.g., a data-provider API allows 3 concurrent connections per account, a desktop-automation tool allows 1 active session per seat), but the agent architecture spins up multiple parallel task instances — sub-agents, worker threads, or concurrent user requests — that each open their own session against the same licensed tool without any shared awareness of how many sessions are already open. The N+1th session either gets rejected outright or, worse, silently kicks an existing session offline mid-task.

**Frequency**: Occasional

**Symptoms**
- Intermittent authentication or connection failures on a tool that work fine in isolation but fail under concurrent load
- Error messages referencing "maximum concurrent sessions exceeded" or "session terminated by another login" appearing in logs correlated with periods of high parallel task volume
- A running task's tool session unexpectedly drops mid-execution with no local cause, coinciding with another task starting
- Concurrency limits discovered only in production, because development and testing were done with a single active user/session

## Root Cause
Session concurrency limits live in the tool vendor's licensing system, not in the agent's own code, so nothing in the agent's control flow inherently knows how many sessions are currently open against a given license. When an agent framework scales horizontally — spawning parallel sub-agents, handling multiple user requests concurrently, or retrying a task in a new process after a timeout without confirming the old session closed — each new execution path independently authenticates against the tool with no shared session counter. The mismatch between the agent architecture's implicit assumption ("each task gets its own fresh, unconstrained connection") and the tool's actual constraint ("only N total connections allowed, system-wide, at any moment") isn't visible until concurrent load exceeds N.

## Example
```
A research-assistant platform gives each user's query its own sub-agent
instance, and each sub-agent independently logs into "MarketData Pro"
using a single shared company API credential that the vendor licenses
for 5 concurrent sessions.

During a normal week, usage stays under 5 concurrent sub-agents. During
a product launch, traffic spikes to 14 simultaneous user queries, each
spawning its own sub-agent that authenticates against MarketData Pro.

Sessions 1-5 connect successfully. Session 6 receives a "concurrent
session limit exceeded" error and the sub-agent's retry logic, not
recognizing this as a rate/capacity issue, retries immediately --
which, per the vendor's session-management behavior, evicts session 3
(the oldest active session) to make room. The sub-agent handling
session 3's original task now fails mid-execution with a "session
terminated" error, and its user sees a request fail with no clear
explanation while 13 other sessions churn through the same 5-slot pool
for the next 20 minutes.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of agent platforms using a shared vendor credential across parallel task instances have no session-count enforcement at the agent layer | Typical range observed in agent platforms integrating seat- or session-limited tools |
| Concurrency-limit incidents disproportionately surface first during traffic spikes or product launches rather than steady-state load | Reported range across teams reviewing capacity-related incidents |
| Adding a session pool/semaphore in front of a concurrency-limited tool typically eliminates the large majority of eviction-related mid-task failures | Estimated from teams retrofitting connection pooling around licensed tools |

## Mitigations
1. **Session pool with a semaphore**: Implement a shared, in-process or distributed semaphore matching the tool's licensed concurrency limit, and have every task acquire a slot before opening a session, queuing rather than exceeding the limit.
2. **Session reuse across tasks**: Where the tool supports it, reuse a small pool of already-authenticated sessions across multiple sequential tasks instead of opening a new session per task.
3. **Graceful queuing over blind retry**: On a concurrency-limit error, queue and wait for a slot to free up rather than immediately retrying, which can trigger evictions of other active sessions.
4. **Per-license usage monitoring**: Track real-time concurrent session count against the licensed limit and alert as usage approaches capacity, before failures start.
5. **Licensed capacity planning tied to scaling limits**: When scaling agent concurrency (more parallel sub-agents, more simultaneous users), explicitly review every licensed tool in the chain for concurrency caps and provision additional seats/sessions ahead of expected peak load.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| concurrent_session_count | Real-time count of active sessions against a concurrency-limited tool | Alert if > 80% of licensed limit |
| session_eviction_count | Count of sessions terminated due to a new session exceeding the concurrency limit | Alert if > 0 |
| concurrency_limit_error_rate | Rate of tool calls failing specifically due to concurrent session limits | Alert if > 0.5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Session limit near capacity | concurrent_session_count reaches 80% of the licensed limit | Medium | Queue new session requests, notify capacity owner to consider provisioning more seats |
| Active session evicted | A running task's session is terminated due to another session exceeding the concurrency cap | High | Fail the affected task gracefully with a clear retry-later message, investigate load spike |

## Related Patterns
- [License Expiration Not Checked](./license-expiration-not-checked.md) - both stem from the agent treating a licensed tool's usage terms as unconstrained rather than actively tracking them
- [Feature Entitlement Limit](./feature-entitlement-limit.md) - a related licensing-boundary failure where the constraint is on account tier/feature access rather than session count
