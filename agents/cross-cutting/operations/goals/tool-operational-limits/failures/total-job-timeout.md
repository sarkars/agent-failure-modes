# Total Job Timeout

## Issue
Multi-step tool jobs (a batch pipeline, an orchestrated workflow, a long-running export composed of several sequential API calls) frequently have an overall wall-clock timeout for the entire job, separate from and often much stricter in aggregate than the sum of individual per-step timeouts an agent budgets for. An agent that allocates time per step, confirming each step completes within its own limit, can still have the whole job killed by the orchestrator's total-job timeout if the sum of otherwise-successful steps exceeds it — a failure the agent's step-by-step success tracking gives it no warning of until the job is terminated mid-flight, discarding whatever aggregate work was in progress at that moment.

**Frequency**: Common

**Symptoms**
- A job killed by the orchestration layer partway through its final steps, despite every individual step's logs showing success within its own allotted time
- Job-level timeout errors that reference a total elapsed time (e.g., "job exceeded maximum runtime of 15 minutes") distinct from any single step's timeout message
- Jobs that succeed reliably with fewer steps or smaller input (shorter total runtime) and fail only when the number of steps or per-step duration grows, even though no single step changed behavior
- Agents that log "all steps completed successfully" in the same run where the orchestrator simultaneously logs a job-level timeout kill, indicating a race between last-step completion and the job-level clock
- No resume capability after a total-job timeout, forcing the entire multi-step job to restart from step one even though most steps had already completed

## Root Cause
Job orchestrators impose an overall wall-clock ceiling to bound total resource consumption and prevent a single runaway job from occupying a worker or queue slot indefinitely, and this ceiling is typically configured independently of — and without direct communication to — the per-step timeout values an agent's own step-execution logic uses. Agents that plan step-by-step, verifying each step completes within its individual budget, have no mechanism by default to accumulate elapsed time across steps and compare it against the job-level ceiling, because the job-level timeout is enforced by an external orchestration layer the agent's own code often doesn't query or even know the exact value of. The result is a class of failure invisible to per-step monitoring: every component the agent tracks reports success, yet the job as a whole is terminated by a clock the agent was never tracking against.

## Example
```
An agent runs a nightly customer-data enrichment pipeline orchestrated as
a 12-step job (each step: fetch a batch of 1,000 customer records, call
an external enrichment API, write results back). Each step is budgeted
and monitored against a 90-second per-step timeout, which every step
consistently meets, averaging 75 seconds. The job orchestrator enforces a
separate total job runtime cap of 12 minutes (720 seconds). With 12 steps
averaging 75 seconds each plus ~10 seconds of inter-step overhead, total
elapsed time is 12*(75+10) = 1,020 seconds — 300 seconds over the job cap.
The orchestrator kills the job after step 9 completes (at ~765 seconds),
mid-way through step 10's enrichment API call. Steps 1-9 have already
written their results; step 10's partial work is discarded; steps 11-12
never ran. The agent's per-step logs for steps 1-9 all show "SUCCESS,"
giving no indication anything went wrong, while the orchestrator's
separate job-level log shows "job terminated: exceeded max runtime
720s" — a signal that lives in a different log stream the agent's
own completion-reporting logic never checks.
```

## Statistics
| Finding | Context |
|---------|---------|
| Job orchestrators (workflow engines, batch schedulers, serverless step functions) commonly enforce total-job wall-clock caps in the 10-60 minute range, independent of per-step timeout configuration | Common in workflow-orchestration and serverless step-function platforms |
| A job whose steps each individually complete within budget can still exceed the total-job cap purely from step count times average step duration plus inter-step overhead, a purely arithmetic risk that per-step monitoring alone doesn't surface | Structural property of the interaction between per-step and job-level timeouts |
| Total-job timeouts frequently terminate a job without a resume/checkpoint mechanism, so completed step output can be lost or left orphaned unless the agent explicitly persists progress markers | Based on typical orchestrator kill behavior on timeout |

## Mitigations
1. **Track cumulative elapsed time against the known job-level ceiling, not just per-step budgets**: Maintain a running total of elapsed time across all steps in the job and compare it against the orchestrator's documented total-job timeout, pausing or restructuring before the cumulative time approaches the ceiling.
2. **Checkpoint progress after each step so a total-job timeout is resumable**: Persist which steps have completed and their outputs durably (not just in job-local memory) so a job killed by the total-job timeout can resume from the next incomplete step rather than restarting entirely.
3. **Budget per-step time with margin proportional to step count**: When designing per-step timeouts for a job with many steps, divide the known total-job ceiling across steps with a safety margin for inter-step overhead, rather than setting each step's timeout independently of how many steps the job contains.
4. **Split large multi-step jobs into multiple independently-scheduled jobs**: Where the total-job timeout is a hard platform constraint, break a 12-step job into e.g. three 4-step jobs each comfortably within the ceiling, chained by an external scheduler rather than a single monolithic job.
5. **Cross-reference orchestrator-level logs with step-level logs in completion reporting**: Ensure the agent's success/failure determination for a job checks the orchestrator's own job-status signal, not just the aggregation of individual step results, so a job-level kill isn't missed by step-only monitoring.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `job.cumulative_elapsed_vs_total_timeout_ratio` | Running elapsed time across all completed steps divided by the known total-job timeout | Alert when ratio > 0.8 mid-job |
| `job.killed_with_all_prior_steps_successful_count` | Count of job-level timeout kills where every step that ran reported individual success | Alert if > 0 |
| `job.completed_steps_at_kill_time` | Number of steps completed when a total-job timeout kill occurs | Track to size checkpoint/resume granularity |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Total job timeout with no step failures | Orchestrator reports job killed on timeout while all executed steps show success | High | Resume from last checkpoint if supported, otherwise re-plan job into smaller sub-jobs |
| Cumulative elapsed time approaching job ceiling | Running total elapsed time exceeds 80% of known total-job timeout before job completion | Medium | Trigger proactive job split or checkpoint-and-defer remaining steps |

## Related Patterns
- [Request Timeout No Graceful Handling](./request-timeout-no-graceful-handling.md) - the single-request analogue of this pattern, without the multi-step aggregation dimension
- [Query Planning Timeout](./query-planning-timeout.md) - another timeout variant occurring at a different layer (query planning) than the overall job clock
- [Backoff Envelope Violation](./backoff-envelope-violation.md) - retry delays added between steps can themselves consume enough of the total-job budget to trigger this pattern
