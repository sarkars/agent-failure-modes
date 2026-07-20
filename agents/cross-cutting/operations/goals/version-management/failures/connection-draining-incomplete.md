# Connection Draining Incomplete

## Issue
When an old agent-serving instance is terminated during a deployment, the platform sends a shutdown signal without waiting for in-flight agent sessions — especially long-running, multi-turn, or streaming tool-use conversations — to finish. Because agent interactions routinely run far longer than a typical stateless HTTP request (a single tool-calling loop can span tens of seconds to several minutes across multiple LLM round-trips), the default drain timeout tuned for short-lived requests expires while sessions are still mid-conversation, and those sessions are hard-killed. Users see a session abruptly disconnect, a streaming response cut off mid-token, or a tool call left in an indeterminate state with no completion or error ever recorded.

**Frequency**: Common

**Symptoms**
- Streaming agent responses cut off mid-sentence during deployments, with no error surfaced to the client beyond a dropped connection
- Spike in "orphaned" tool calls — external side effects (an API POST, a database write) initiated but never confirmed, correlated with deployment timestamps
- Session-completion rate dips sharply in a narrow window immediately after each rollout
- Old instances show active connection counts still nonzero at the moment they are force-killed by the orchestrator
- Support reports of "the assistant just stopped responding" cluster in time around known deployment windows

## Root Cause
Connection draining is usually configured with a single timeout value inherited from generic web-service defaults (e.g., 30 seconds), which comfortably covers typical request/response cycles but not agent workloads where a single logical session can involve several sequential LLM calls, tool invocations, and human-in-the-loop pauses. The deployment orchestrator (Kubernetes, an ECS service, a load balancer) has no visibility into "this connection represents a multi-step agent session that is 80% through a tool-calling loop" — it only sees an open TCP/HTTP connection and applies the same fixed grace period to every one. When the drain timeout expires before the session naturally reaches a checkpoint, the orchestrator proceeds to SIGKILL the pod or forcibly close the connection, and any application-level cleanup (marking the session as interrupted, rolling back a partially-applied tool side effect, notifying the client) never runs because it depends on graceful-shutdown code that also never got to execute.

## Example
```
"AgentGateway" service runs agent sessions handling multi-step
research tasks; a typical session takes 45-90 seconds end to end
across 4-6 tool calls. Kubernetes deployment config:
terminationGracePeriodSeconds: 30 (the cluster-wide default,
never overridden for this service).

14:20:00 - rollout begins for v22, old pods (v21) receive SIGTERM
and are marked NotReady, load balancer stops sending new sessions
to them but 340 in-flight sessions are already connected.

14:20:00-14:20:30 - v21 pods attempt graceful shutdown: finish
current LLM call, avoid starting new tool calls, try to flush
partial results. Sessions that started before 14:19:45 (i.e., have
enough time left under a ~90s session budget) are still mid-loop.

14:20:30 - grace period expires. Kubernetes sends SIGKILL to all
remaining v21 pods. 61 sessions are killed mid-tool-call, including
9 where a "create calendar event" tool had already sent its API
request but the pod died before recording the tool result back into
conversation state.

Result: those 9 users have a duplicate or orphaned calendar event
with no corresponding assistant confirmation, and no error was ever
logged because the process was killed before it could write one.
```

## Statistics
| Finding | Context |
|---------|---------|
| Default web-service drain timeouts (commonly 15-30s) are frequently shorter than typical multi-step agent session duration (often 30-180s) | Typical mismatch observed across teams running agent workloads on generic container orchestration defaults |
| A meaningful share of in-flight sessions killed during deployment involve at least one tool call whose side effect had already been dispatched but not confirmed | Estimated from post-incident review of deployment-correlated orphaned tool calls |
| Session-aware draining (extending grace period based on active session state) substantially reduces forced mid-session kills compared to a fixed timeout | Reported range across teams that implemented session-aware drain logic |

## Mitigations
1. **Session-aware grace periods**: Size the termination grace period to the realistic p99 session duration for the workload rather than inheriting a generic short-request default, and extend it dynamically if the instance still reports active sessions near the deadline.
2. **Checkpoint before drain deadline**: Have the application track session progress and, as the drain deadline approaches, force sessions to a safe checkpoint (complete the current tool call, persist partial state) rather than letting them be killed at an arbitrary point mid-operation.
3. **Idempotent/resumable tool calls**: Design side-effecting tool calls to be safely retryable or resumable from persisted state, so a session interrupted mid-call can be picked up by a new instance rather than left orphaned.
4. **Stop routing new sessions before draining starts**: Ensure the load balancer or service mesh marks an instance "no new traffic" and waits a buffer period before beginning the drain countdown, so drain time is spent finishing existing work rather than racing new arrivals.
5. **Drain-kill telemetry**: Emit an explicit metric/event whenever a session is forcibly terminated by a grace-period expiry (versus completing normally), tagged with how far through its lifecycle it was, so incomplete draining is visible rather than silently absorbed as a generic connection drop.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| forced_session_kill_count | Sessions terminated by SIGKILL/grace-period expiry rather than graceful completion, per deployment | Alert if > 0.5% of concurrent sessions during a rollout |
| orphaned_tool_call_rate | Tool calls with a dispatched side effect but no recorded completion, correlated with deployment windows | Alert if any occurrence within 2 minutes of a rollout |
| drain_deadline_active_session_count | Number of sessions still active on an instance at the moment its grace period expires | Alert if > 0 for any deployment |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sessions force-killed during rollout | forced_session_kill_count > 0 for a deployment | High | Pause further rollouts, review grace period sizing, check for orphaned side effects |
| Orphaned tool call detected | A tool call side effect logged with no matching completion within its expected window, near a deployment timestamp | High | Manually reconcile the affected external state, notify affected user session owner if applicable |

## Related Patterns
- [Blue-Green Deployment Traffic Not Switched](./blue-green-deployment-traffic-not-switched.md) - both concern the mechanics of retiring an old version safely once traffic has (or hasn't) moved
- [Rollback Partial Failure](./rollback-partial-failure.md) - shares the theme of side effects left in an indeterminate state when an operation is interrupted mid-flight
- [Sticky Session Loss](./sticky-session-loss.md) - a related failure where session continuity breaks during deployment, though via routing rather than forced termination
