# State Machine Violation

## Issue
An entity that an agent manages (an order, a support ticket, a workflow run) is meant to move through a defined sequence of states with specific allowed transitions, but the agent — due to a missing guard, a race, or a direct write that bypasses the transition logic — moves it into a state or a state sequence the state machine should have forbidden. The entity ends up in a combination of fields that no valid path through the workflow should ever produce, and downstream logic that assumes the state machine's invariants hold then behaves unpredictably.

**Frequency**: Occasional

**Symptoms**
- Records found with a combination of fields that no legal transition path could produce (e.g. "refunded" with no prior "paid" state)
- Downstream code throws unexpected errors or produces nonsensical output when handling a record, traceable to an assumption the state machine was supposed to guarantee
- Transition logs show a jump directly from state A to state D, skipping the required intermediate states B and C
- The same entity has two active workflows both believing they're responsible for it, because a terminal-state guard didn't block a duplicate start
- Manual "fix-up" scripts are periodically run to correct records stuck in states the application code doesn't know how to handle

## Root Cause
State machine invariants are only as strong as the code path that enforces them, and agent systems frequently have multiple ways to write to the same entity — the primary workflow engine, an admin tool, a retry/compensation path, a direct database fix — not all of which route through the same transition-validation logic. An agent making a tool call to "update ticket status" often has no visibility into the full state machine definition; it just calls an API with a target state, and if that API (or the underlying data layer) doesn't itself enforce "only states X and Y may transition to Z," the agent's LLM-driven decision becomes the only thing standing between the entity and an illegal state, and LLM decisions are not guaranteed to respect constraints that aren't explicitly represented in its context.

## Example
```
A subscription-management agent handles ticket workflows with the
state machine: created -> paid -> active -> {cancelled, expired}.
Only "active" may transition to "cancelled".

An agent handling a batch of customer cancellation requests processes
ticket #9931, which is currently in state "created" (the customer
never completed payment - it's an abandoned checkout).

The agent's tool for "cancel subscription" doesn't validate the
current state before writing; it directly sets status to "cancelled"
in response to the user's cancellation request, without checking that
the subscription was ever "active".

Ticket #9931 is now in state "cancelled" having skipped "paid" and
"active" entirely. Two days later, the billing reconciliation job
processes the ticket, expects "cancelled" records to have an
associated payment and pro-rated refund amount, finds none, and
throws a NullPointerException that halts the entire nightly
reconciliation batch for all 40,000 tickets in the run.
```

## Statistics
| Finding | Context |
|---------|---------|
| 5-12% of "impossible state" incidents in workflow-driven agent systems trace back to a write path that bypassed the primary transition validator | Typical range observed in production agent telemetry |
| Centralizing all writes through a single transition-guard function reduces illegal-state incidents by an estimated 80-95% | Reported range across teams that consolidated write paths |
| Illegal states are disproportionately introduced by admin/override tools and retry-after-failure paths rather than the primary happy-path flow | Estimated from incident postmortems in workflow-heavy agent deployments |

## Mitigations
1. **Single enforcement point for all writes**: Route every write to the entity's state field — including admin tools, retries, and compensation logic, not just the primary agent flow — through one shared transition-validation function that rejects illegal transitions.
2. **Database-level transition constraints**: Where the data layer supports it, encode the allowed-transition table as a database constraint or trigger, so even a bug in application code can't physically write an illegal state.
3. **Explicit precondition checks in tool definitions**: Give the agent's state-changing tools their own precondition checks (e.g. "cancel" tool requires current state == active) with a clear rejection message, rather than trusting the agent's judgment to only call it when appropriate.
4. **Periodic invariant scanning**: Run a scheduled job that scans for entities in field combinations the state machine should make impossible, and alert immediately rather than waiting for downstream code to crash on them.
5. **Transition audit log with replay capability**: Log every attempted and actual transition (including rejected ones) so illegal-state incidents can be traced to the exact write path and tool call that caused them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| illegal_transition_attempt_count | Count of transitions rejected by the validation layer as not allowed from the current state | Alert if > 0 for high-value entity types |
| invariant_violation_scan_hits | Count of entities found by the periodic scan in an impossible field combination | Alert if > 0 |
| write_path_bypass_rate | Fraction of entity writes that did not go through the central transition-validation function | Alert if > 0% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Impossible state detected | Invariant scan finds an entity in a field combination no legal transition path produces | High | Page on-call, quarantine the entity from automated processing, trace the write path that caused it |
| Downstream crash on state assumption | A consumer process throws an error traceable to a violated state-machine invariant | High | Halt the affected batch job, patch the illegal record, add a guard at the write path identified |

## Related Patterns
- [Concurrent State Modification](./concurrent-state-modification.md) - concurrent writers racing on the same entity is one common mechanism that produces an illegal transition
- [State Consistency Timeout](./state-consistency-timeout.md) - acting on stale state from a timed-out check can itself drive a transition the current true state wouldn't have allowed
- [State Version Incompatibility](./state-version-incompatibility.md) - a version mismatch in the transition logic itself (old code enforcing an outdated state machine) can also produce illegal transitions
