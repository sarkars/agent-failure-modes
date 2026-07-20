# Memory Loss on Reboot

## Issue
An agent accumulates state — working memory, in-progress task tracking, session-scoped facts — purely in the host process's memory (a Python dict, an in-memory cache, an unpersisted object graph) without writing it to durable storage. When the process restarts — a deploy, a crash, an autoscaler recycling the instance, an out-of-memory kill — all of that state disappears instantly and irrecoverably, and the agent resumes (or a fresh instance picks up the workload) with no record that the state, or the work in progress, ever existed.

**Frequency**: Common

**Symptoms**
- Agent "forgets" everything about an in-progress task immediately after a deploy or restart, with no gradual degradation
- Users report having to re-explain context they provided minutes before a routine deployment
- In-flight multi-step workflows silently restart from scratch after an infrastructure event, sometimes redoing already-completed side effects
- No error is logged for the lost state — the process simply comes back up with empty memory, which looks identical to a legitimately new session
- Incidents cluster tightly around deploy windows, autoscaling events, or OOM-kill timestamps

## Root Cause
Holding session or working-memory state purely in process memory is the simplest implementation and is often sufficient during initial development, when the process rarely restarts and testing happens within a single long-lived run. Persisting that state to a durable store (database, distributed cache, disk-backed log) adds latency, complexity, and a consistency story that's easy to defer. As the system moves to production, where processes restart routinely for deploys, autoscaling, and crash recovery, the gap between "state that should survive a restart" and "state that actually does" becomes a production incident rather than a development inconvenience — and because nothing fails loudly (the process just starts up empty), the gap frequently isn't discovered until a real restart during active use destroys real in-progress work.

## Example
```
A document-processing agent runs as a stateless-looking HTTP service,
but tracks the state of a long multi-step extraction job (12 steps,
~4 minutes total) in an in-memory dictionary keyed by job_id, because
that was the fastest way to prototype it: job_state[job_id] = {...}.

14:20:00 - User submits a document for extraction, job_abc123 begins.
14:20:45 - Steps 1-6 complete (structure parsing, entity extraction).
14:21:00 - A routine autoscaling event terminates this instance to
            scale down after a traffic dip; a new instance starts
            with an empty job_state dict.
14:21:05 - User polls for job_abc123 status.
Response: "Job not found."

The 45 seconds of extraction work (and the API costs incurred
running it) are gone with no trace, no error logged pointing to
the actual cause, and no way for the user to know whether to
resubmit or wait — from their perspective the job simply vanished.
```

## Statistics
| Finding | Context |
|---------|---------|
| Services relying solely on in-memory state typically experience process restarts multiple times per week purely from routine deploys and autoscaling, independent of any actual failure | Typical range for actively-deployed production services |
| In-progress multi-step agent workflows without durable checkpointing show a nonzero completion-loss rate directly proportional to how often the host process restarts mid-workflow | Estimated from workflow-duration vs. restart-frequency overlap analysis |
| Adding durable checkpointing at each workflow step reduces total-loss incidents to near zero, at the cost of added write latency per step | Reported range across teams that added step-level persistence |

## Mitigations
1. **Durable checkpointing per step**: Persist workflow/task state to a durable store (database, durable queue, disk-backed cache) after each meaningful step, not just at job completion, so a restart can resume from the last checkpoint.
2. **Graceful shutdown draining**: On receiving a shutdown signal (SIGTERM from an orchestrator), flush in-flight in-memory state to durable storage before the process exits, rather than relying solely on periodic checkpoints.
3. **Externalize session state**: Move session/working-memory state out of process memory entirely into a shared store (Redis, a database) from the start, treating the process itself as fully stateless and disposable.
4. **Idempotent resumability**: Design multi-step workflows so each step can be safely re-run or resumed from a checkpoint without duplicating side effects, so recovery after a crash doesn't require perfect checkpoint granularity.
5. **Restart-loss monitoring**: Explicitly track and alert on jobs/sessions that disappear coincident with a process restart, rather than treating "job not found" as an undifferentiated user-facing error.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| in_flight_state_loss_count | Count of in-progress jobs/sessions that become unresolvable coincident with a process restart | Alert if > 0 |
| checkpoint_lag | Time/steps elapsed since a workflow's last durable checkpoint | Alert if exceeds one full step interval |
| restart_to_job_loss_correlation | Correlation between process restart events and "job not found" errors within the following minute | Alert if correlation is strongly positive |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| State loss on restart | A job/session with no durable checkpoint is unresolvable immediately following a process restart | High | Notify affected user/caller, add durable checkpointing to the affected workflow |
| Deploy-correlated job loss spike | Job-not-found error rate spikes within a short window of a deploy | High | Treat as a deploy regression, review whether new code path lost durability coverage |

## Related Patterns
- [Memory Not Updated Stale Retrieval](./memory-not-updated-stale-retrieval.md) - both are consistency gaps between what the system believes is durable and what actually is, though this pattern loses data entirely rather than serving an old version
- [Context Window Awareness Failure](./context-window-awareness-failure.md) - both are silent, undetected loss-of-state failures the agent has no visibility into when they occur
- [Memory Priority Inversion](./memory-priority-inversion.md) - checkpointing added to fix reboot loss can itself introduce write contention that delays higher-priority memory operations
