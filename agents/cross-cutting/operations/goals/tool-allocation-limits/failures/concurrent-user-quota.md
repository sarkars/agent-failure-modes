# Concurrent User Quota

## Issue
Many SaaS tools license access by concurrent "seats" or "sessions" rather than by request volume. When an agent authenticates as if it were a human user — holding a persistent session or logging in under a shared service account — it consumes one of those concurrent slots. This either locks the agent out when human users have filled the pool, or worse, silently evicts a human user's active session when the agent logs in and the license enforces a hard cap.

**Frequency**: Common

**Symptoms**
- Human users report being unexpectedly logged out or seeing "session terminated elsewhere" messages
- Agent login attempts fail with "maximum concurrent users reached" during business hours but succeed overnight
- Intermittent authentication failures that correlate with headcount growth or new hires, not with the agent's own behavior
- Agent holds an idle session open indefinitely, consuming a seat it isn't actively using
- Support tickets from users unable to log in coincide with agent job run times

## Root Cause
Concurrent-user licensing models (common in legacy enterprise tools like CRMs, ERPs, and some analytics platforms) were designed around the assumption that "user" means a person at a keyboard, with sessions that are short-lived and self-limiting. An agent doesn't behave like a person: it can open a session and never close it, run many parallel workers each opening their own session, or reconnect faster than the license pool can free up a slot. The licensing server has no way to distinguish "automated consumer treating this as infrastructure" from "person who stepped away," so it simply enforces the numeric cap.

## Example
```
1. Company's CRM license allows 25 concurrent user sessions.
2. A data-sync agent authenticates once at startup and keeps its session alive for the
   entire day to avoid re-login overhead, holding 1 of the 25 slots permanently.
3. At 9:15 AM, sales team logs in for the day; by 9:40 AM all 25 slots are in use,
   including the agent's idle one.
4. A 26th salesperson tries to log in and is rejected with "concurrent user limit reached."
5. IT support, unaware the agent is holding a slot, spends 30 minutes checking the
   salesperson's account before finding the agent's long-lived session in admin logs.
6. Killing the agent's session frees the slot, but the agent's next scheduled sync fails
   mid-run because its session was terminated without warning.
```

## Statistics
| Finding | Context |
|---------|---------|
| Concurrent-seat licensing is used by an estimated 15-25% of enterprise SaaS tools still in production, especially legacy CRM/ERP systems | Typical for tools predating modern API-key/OAuth models |
| Agent-held idle sessions have been observed to occupy licensed seats for 4-12x longer than the agent's actual active work time | Common when agents don't implement session teardown |
| Orgs report concurrent-quota lockouts spike 2-3x during month-end/quarter-end when both automation and human usage peak simultaneously | Consistent with combined batch-job and human-user overlap |

## Mitigations
1. **Dedicated service seats**: Provision a separate license seat/account class for automated consumers where the vendor supports it, so agents never compete with human users for the same pool.
2. **Aggressive session teardown**: Explicitly log out or close the agent's session immediately after each task completes rather than holding it open for reuse; treat idle-session-holding as a bug, not an optimization.
3. **Concurrency-aware scheduling**: Cap the number of parallel agent workers that can hold sessions simultaneously, and schedule batch jobs outside peak human-usage hours where the tool's usage pattern allows it.
4. **Pre-flight slot check**: Before authenticating, query the tool's admin/usage API (if available) for current concurrent-session count and defer or queue the agent's login if the pool is near capacity.
5. **Session-eviction monitoring**: Alert when the agent's own session gets forcibly terminated, distinguishing "we ran out of retries" from "a human user's login evicted us," so the on-call response differs accordingly.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `concurrent_sessions.agent_held_duration_s` | How long the agent has continuously held a licensed session slot | Alert above 3600s (1 hour) of idle hold |
| `concurrent_sessions.pool_utilization_pct` | Current concurrent sessions / licensed max | Alert above 90% |
| `auth.concurrent_limit_rejections` | Count of login attempts rejected due to concurrent-user cap, agent or human | Alert on any occurrence during business hours |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Human user locked out by agent session | Login rejection logged for a human account while an agent session has been idle >30 min | High | Force-terminate agent's idle session, notify affected user |
| Concurrent pool near saturation | `pool_utilization_pct` > 90% for 10 minutes | Medium | Throttle non-critical agent jobs, review seat count with vendor |

## Related Patterns
- [Api Key Quota Per Account](./api-key-quota-per-account.md) - both involve an agent unknowingly competing with other consumers for a shared allocation
- [Storage Quota Shared Across Agents](./storage-quota-shared-across-agents.md) - shared-pool exhaustion pattern applied to storage rather than sessions
- [Execution Time Quota](./execution-time-quota.md) - another case where the agent's usage pattern diverges from the assumptions baked into the tool's limit
