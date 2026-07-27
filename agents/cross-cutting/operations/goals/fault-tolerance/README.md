# What Are the Most Common Fault-Tolerance Failures in AI Agents?

**Agent systems fail constantly — services time out, data becomes corrupted, dependencies crash, and network partitions split systems. Fault-tolerance failures occur when agents don't detect failures quickly, don't recover from them cleanly, or apply recovery procedures that introduce new failures, such as cascading timeouts, partial rollbacks that leave data inconsistent, or failover delays so long that SLAs are already violated.**

## Key Takeaways

1. **Cascading Timeouts Amplify Failures**: When Agent A times out waiting for Agent B, and Agent A's timeout is longer than Agent B's recovery time, agents pile up waiting on each other, saturating thread pools. Timeouts must be aggressive and decrease at each layer to prevent cascade amplification.

2. **Failover Delays Violate Recovery Time Objectives**: Teams measure mean time to recovery (MTTR) in seconds or minutes, but automatic failover often takes 30-60 seconds just to detect the primary is down. By the time failover completes, SLA windows are already violated. Detection and failover must happen in milliseconds, not seconds.

3. **Partial Failures Leave Data Inconsistent**: When a subset of steps in a recovery procedure succeed and the rest fail, the system is left in a partial state that cascades new failures downstream. Recovery procedures must be all-or-nothing, or intermediate states must be explicitly handled.

4. **Recovery Procedures Are Untested Until They Fail**: A recovery procedure that was never executed during steady state may fail in production the first time it's needed, because it encounters conditions that only appear during actual failure. Recovery paths must be tested regularly under failure scenarios.

## Scope

Fault-tolerance failures cluster into five categories:

- **Cascade Mechanisms**: Failures in one agent trigger failures in others due to timeouts, resource exhaustion, or cascading rollbacks. (cascade-amplification, cascade-detection-failure, cascade-isolation-failure, cascade-timeout-interaction)
- **Divergent Recovery**: After a failure, different agents recover to different states, leading to inconsistency or data corruption. (cascade-divergent-recovery, failover-state-corruption, recovery-data-corruption, recovery-divergence)
- **Failover Delays & Detection**: The system doesn't detect that a primary has failed, or the detection takes too long, or failover is blocked waiting on the primary. (failover-correctness-failure, failover-delay-too-long, failover-data-loss)
- **Recovery Timing & Completeness**: Recovery procedures take too long or only partially recover, missing steps that lead to cascading failures or SLA violations. (recovery-ordering-violation, recovery-partial-failure, recovery-procedure-untested, recovery-time-objective-miss)
- **Redundancy & Coordination**: Redundant copies of data or services don't stay coordinated during failure, or coordination mechanisms themselves fail. (redundancy-coordination-failure, single-point-of-failure, recovery-point-objective-miss)

## When Fault-Tolerance Matters

1. **Mission-Critical Workflows**: Systems where failures must be detected and recovered from in seconds, not minutes. Financial transactions, safety-critical control loops, or high-SLA services.

2. **Multi-Agent Distributed Systems**: Systems with many agents running on different hardware. Any single component's failure can cascade into failures in dependent agents if tolerance mechanisms aren't in place.

3. **Stateful Services & Data Consistency**: Systems where agents maintain state (orders, accounts, session data) that must be recovered consistently across failovers. Partial or divergent recovery corrupts that state.

## Cross-Pattern Insight

Fault-tolerance is fundamentally about **managing the time between failure and recovery**. A failure is inevitable; the question is whether the system detects it fast enough and recovers cleanly enough to meet the SLA. Every fault-tolerance mechanism adds latency: detection takes milliseconds, failover takes more milliseconds, recovery procedures take seconds. But applications have SLAs measured in seconds or tens of seconds. If detection takes 5 seconds and recovery takes 10 seconds, the SLA is already violated before recovery completes. Robust fault-tolerance requires aggressive timeouts (hundreds of milliseconds, not seconds), rapid detection (through heartbeats or explicit pings, not waiting for requests to fail), and fast failover (into standby replicas, not rebuilding from scratch). Recovery procedures must be all-or-nothing (not leaving the system in a partial state), regularly tested (not just theoretically sound), and faster than the SLA window. Without these, fault-tolerance is only a hope, not a guarantee.

## Frequently Asked Questions

**What is the difference between failover delay and recovery time objective?**
Failover delay is the time from when a primary fails to when the system detects the failure and switches to a backup. Recovery time objective (RTO) is the total time from failure to when the system is fully recovered and accepting traffic. Failover is just one component of RTO. If detection takes 5 seconds and failover takes 10 seconds and recovery takes 20 seconds, the total RTO is 35 seconds. If the SLA is 30 seconds, RTO is already violated.

**How can an agent detect that a dependency has failed if it's not getting requests?**
Active health checks: periodically send a ping or health check to a dependency and record the response. Don't rely on request failures to detect dependencydown; by that time, your own requests are queued up timing out. Implement health checks at intervals much shorter than the timeout window (e.g., every 500ms for a 5-second timeout).

**Why do partial failures leave the system in an inconsistent state?**
Because agents operate asynchronously and independently. If a recovery procedure is supposed to roll back changes in agents A, B, and C, and agent B's rollback fails, agents A and C have already rolled back but B hasn't. The system is now inconsistent. Mitigations: (1) make recovery all-or-nothing (stop the procedure if any step fails), (2) make recovery idempotent (safe to retry any step), or (3) explicitly handle partial states in downstream agents.

**How can cascade amplification be prevented if timeouts are necessary?**
Use timeouts that decrease at each layer. Layer 1 (client -> API) might timeout at 5 seconds, Layer 2 (API -> backend service) at 4 seconds, Layer 3 (backend -> database) at 3 seconds. This ensures that if Layer 3 is slow, Layer 2 detects and fails fast before Layer 1 times out. Also use circuit breakers to fail fast if a dependency is already returning errors.

**What should be tested for recovery procedures?**
At minimum: (1) recovery completes within RTO, (2) recovery produces a fully consistent state (run the same verification checks as in steady state), (3) recovery is idempotent (replaying recovery steps produces the same result), (4) recovery doesn't produce cascading failures (downstream agents can resume normal operation), and (5) recovery works with partial prior failures (e.g., if some agents are already down before recovery starts).

## Failure Patterns

| Pattern | Description |
|---------|-------------|
| [Cascade Amplification](failures/cascade-amplification.md) | A failure in one agent triggers timeouts in others, which trigger timeouts in their dependencies, amplifying latency across the system. |
| [Cascade Branching](failures/cascade-branching.md) | A single failure branches into multiple dependent failure cascades, affecting different parts of the system simultaneously. |
| [Cascade Detection Failure](failures/cascade-detection-failure.md) | The system doesn't detect that a cascade has begun, allowing it to spread unchecked. |
| [Cascade Divergent Recovery](failures/cascade-divergent-recovery.md) | Different agents in a cascade recover to different states, leaving the system inconsistent. |
| [Cascade Isolation Failure](failures/cascade-isolation-failure.md) | A failure spreads from one agent or service to others because isolation mechanisms didn't work. |
| [Cascade Resilience Failure](failures/cascade-resilience-failure.md) | Resilience mechanisms (circuit breakers, rate limiters) fail under cascade load or misconfiguration. |
| [Cascade Timeout Interaction](failures/cascade-timeout-interaction.md) | Timeouts at different layers compound or interact, causing cascading failures instead of graceful degradation. |
| [Failover Correctness Failure](failures/failover-correctness-failure.md) | Failover to a backup produces incorrect results because the backup is out of sync or misconfigured. |
| [Failover Data Loss](failures/failover-data-loss.md) | Data in flight or recently committed is lost when failing over from primary to backup. |
| [Failover Delay Too Long](failures/failover-delay-too-long.md) | Detection and failover take so long that SLA is already violated before the system recovers. |
| [Failover State Corruption](failures/failover-state-corruption.md) | State on the backup diverges from the primary during normal operation; failover switches to corrupt state. |
| [Recovery Data Corruption](failures/recovery-data-corruption.md) | Recovery procedure inadvertently corrupts data while attempting to restore consistency. |
| [Recovery Divergence](failures/recovery-divergence.md) | Different agents executing recovery procedures independently end up with divergent state. |
| [Recovery Ordering Violation](failures/recovery-ordering-violation.md) | Recovery steps are applied out of order, leaving the system in an invalid intermediate state. |
| [Recovery Partial Failure](failures/recovery-partial-failure.md) | Some recovery steps succeed while others fail, leaving the system in a partially recovered state. |
| [Recovery Point Objective Miss](failures/recovery-point-objective-miss.md) | Data loss during a failure exceeds the configured recovery point objective (RPO). |
| [Recovery Procedure Untested](failures/recovery-procedure-untested.md) | A recovery procedure was never executed until needed in production and fails when invoked. |
| [Recovery Time Objective Miss](failures/recovery-time-objective-miss.md) | Recovery takes longer than the configured recovery time objective (RTO). |
| [Redundancy Coordination Failure](failures/redundancy-coordination-failure.md) | Redundant copies become uncoordinated; failover switches to a stale or divergent replica. |
| [Single Point of Failure](failures/single-point-of-failure.md) | A component lacks redundancy; its failure brings down the entire system. |

**Total: 20 patterns**

## Related Goals

- [Cascade-Failures](../cascading-failures/README.md) — cascade propagation mechanisms are the primary concern in cascading-failures; fault-tolerance addresses recovery from cascades
- [Recovery-Mechanisms](../recovery-mechanisms/README.md) — dedicated to recovery procedures and ensuring they complete within RTO
- [Monitoring-and-Alerting](../monitoring-and-alerting/README.md) — rapid detection of failures is a prerequisite for fast recovery
- [State-Consistency](../state-consistency/README.md) — divergent recovery often stems from inconsistent state management
- [Dependency-Management](../dependency-management/README.md) — dependencies are a common failure source; timeouts and circuit breakers mitigate dependent failures
