# Integration Order Dependency

## Issue
An agent's workflow calls multiple external integrations where one system's call must complete and be acknowledged before another system's call is valid — a payment must be authorized before an inventory hold is placed, a user record must be created before a permissions grant references it — but nothing in the agent's orchestration logic encodes that ordering requirement as a hard constraint. When the agent parallelizes calls for latency, retries them independently after a partial failure, or is composed by an LLM planner that doesn't know the hidden sequencing rule, calls fire out of order and the downstream system either rejects the request against a resource that doesn't exist yet or, worse, silently accepts it and creates a dangling or orphaned record.

**Frequency**: Common

**Symptoms**
- A downstream integration call intermittently fails with a "referenced resource not found" or "invalid state" error that resolves on retry, because the retry happens to land after the prerequisite call has by then completed
- Orphaned or dangling records appear in one system that reference an entity in another system which was never actually created (a permission grant for a user ID that has no user record)
- The failure rate for a specific integration correlates with request concurrency or latency variance rather than with the request content itself — the same payload succeeds under low load and fails under high load
- An LLM-driven planner or agent occasionally reorders or parallelizes a sequence of tool calls that a human-written workflow always executed in a fixed order, since the ordering constraint was implicit in the original code rather than expressed as an explicit dependency
- Post-incident review finds the ordering requirement was known and documented only in a comment, a runbook, or one engineer's memory, not enforced anywhere in code

## Root Cause
Ordering requirements between integrations are frequently implicit — encoded in the fact that a human-written script happened to call things in the right sequence — rather than being an explicit, machine-checkable dependency declared alongside the integration itself. This works until the calling code changes: a refactor introduces concurrency for performance, a retry mechanism resubmits one call without re-verifying its prerequisite still holds, or (increasingly) an LLM-based planner composes the same set of tool calls based on their individual descriptions without any signal that call B requires call A's side effect to exist first, since tool schemas typically describe a single call's inputs/outputs and not its relationship to other calls in the same workflow. Without an explicit precondition check or dependency graph the orchestration layer enforces, the ordering constraint holds only by accident, and any change to timing, concurrency, or call composition can violate it.

## Example
```
An onboarding agent provisions a new employee across three systems:
1. Identity Provider (IdP): creates the user account, returns a user_id
2. Permissions Service: grants role-based access, requires an existing
   user_id to attach the grant to
3. Notification Service: sends a welcome email, requires the
   Permissions Service grant to exist so it can include the correct
   list of accessible systems in the email

The agent's tool-calling loop is given all three tools with independent
schemas and a natural-language instruction to "onboard the new
employee using the available tools." The planner, optimizing for
speed, issues the IdP call and immediately fires the Permissions call
in parallel with a placeholder retry-until-ready loop, since the tool
schema doesn't indicate the Permissions call depends on the IdP call's
output being durably readable yet (there's a few hundred milliseconds
of eventual-consistency lag in the IdP's read replica).

The Permissions call's first attempt hits the read replica before the
new user_id has propagated, gets a "user not found" error, and per its
own retry policy retries after a short backoat - succeeding on retry 2.
This looks like a transient error and goes unnoticed until the
Notification Service call, fired concurrently with the Permissions
retry rather than after it, sends the welcome email before the
permissions grant exists - the email lists "your accessible systems"
as an empty list, confusing the new employee and generating a support
ticket.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of intermittent, retry-resolved integration errors in multi-system workflows trace back to an unenforced ordering dependency rather than a genuine transient fault | Estimated from postmortems of "flaky" integration failures later found to be ordering-related |
| Introducing concurrency or LLM-driven tool composition into a previously sequential workflow measurably increases the rate of order-dependency violations if the dependency isn't made explicit | Typical pattern observed when migrating scripted workflows to agentic orchestration |
| Workflows with explicit, declared preconditions between integration steps show substantially fewer orphaned-record incidents than workflows relying on implicit call ordering | Reported range across teams comparing declared-dependency vs. implicit-ordering workflow designs |

## Mitigations
1. **Declare explicit preconditions between dependent tool calls**: Encode the ordering requirement as a machine-checkable precondition (call B requires call A's output as an input parameter, not just as an earlier step in a prompt), so a planner or orchestrator cannot issue B without A's result in hand, structurally preventing reordering.
2. **Verify durable read-after-write before dependent calls, not just call completion**: When a prerequisite system has eventual-consistency lag, don't treat the prerequisite call's response as sufficient — explicitly confirm the created resource is readable (a follow-up read-your-write check) before triggering dependent calls.
3. **Model the workflow as an explicit dependency graph, not a flat tool list**: Give the orchestration layer (or the planner) a directed dependency graph between integration steps rather than a flat set of independently-described tools, so ordering constraints are structural rather than left to be inferred from a natural-language instruction.
4. **Idempotent, order-tolerant downstream handling where possible**: For integrations where strict ordering can't be fully guaranteed, design the downstream system to queue or defer an out-of-order request (rather than rejecting or silently accepting it) until its precondition is satisfied.
5. **Fail closed, not open, on missing prerequisites**: Ensure dependent calls explicitly check for and reject execution when a required prior step's result is absent, rather than proceeding with a default/placeholder value that lets the workflow silently continue in a broken state.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| order_dependency_violation_rate | Rate of downstream calls rejected due to a missing prerequisite resource | Alert if rate correlates with concurrency/load rather than staying flat |
| retry_resolved_reference_error_rate | Rate of "resource not found"/"invalid state" errors that succeed only on retry | Alert if sustained above baseline, as a proxy for hidden ordering races |
| orphaned_record_count | Count of records in a downstream system referencing a nonexistent upstream entity | Alert on any nonzero count for critical workflows |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Ordering violation spike | order_dependency_violation_rate rises after a change to workflow concurrency or planner composition | High | Roll back the concurrency/composition change, add explicit precondition checks before re-enabling |
| Orphaned record detected | orphaned_record_count increases for a critical cross-system workflow | High | Reconcile the orphaned record, audit the workflow's call ordering for the affected step pair |

## Related Patterns
- [Integration Data Consistency](./integration-data-consistency.md) - order violations are one specific mechanism that produces the cross-system state disagreement this sibling pattern describes
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - both involve one integration's call proceeding before another's true completion state is known, one from timing/timeout assumptions and one from missing sequencing constraints
- [Recovery Ordering Violation](../../fault-tolerance/failures/recovery-ordering-violation.md) - the same out-of-order-execution mechanism applied specifically to recovery/replay after a failure, rather than to normal-path multi-system orchestration
