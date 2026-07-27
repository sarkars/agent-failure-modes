# What Are the Most Common Agent-Handoffs-Delegation Failures in AI Agents?

**Multi-agent workflows rely on one agent successfully transferring a task to the next, but handoffs often fail due to missing context, broken accountability, or timing mismatches. Agent-handoffs-delegation failures occur when the sending agent doesn't transfer sufficient information, the receiving agent doesn't acknowledge receipt, or the orchestration layer doesn't enforce handoff preconditions, leaving tasks orphaned, executed without approval, or duplicated.**

## Key Takeaways

1. **Handoff Accountability Matters**: Tasks marked "handed off" must be explicitly owned by a receiving agent, monitored for progress, and escalated if stalled. Without active ownership tracking across agent boundaries, tasks silently stall for hours or days.

2. **Context Transfer Is Not Optional**: Handoffs that pass only summarized context result in 20-35% of receiving agents re-requesting information already gathered upstream, effectively doubling latency and tool usage. Full state transfer or structured checkpoints are required.

3. **Approval Gates Must Be Structural, Not Suggestive**: Fire-and-forget approval requests that timeout to "proceed" (rather than "block and escalate") fail to block unapproved actions in 10-20% of asynchronous workflows. The receiving agent must validate a cryptographic token, not just check that a handoff message exists.

4. **Handoff Timing Requires Synchronization Primitives**: Receiving agents that aren't ready, queue systems with filters that mismatch payload metadata, or protocol version skew between sender and receiver cause handoffs to be silently dropped or misinterpreted. Explicit readiness checks and version negotiation are required.

## Scope

Agent-handoffs-delegation failures cluster into five categories:

- **Ownership & Accountability**: Sending agent considers the task "done" but no entity actively owns the downstream work. (Handoff Accountability Loss, Handoff State Loss)
- **Context & State Transfer**: Receiving agent lacks the information, constraints, or permissions needed to execute. (Handoff Context Incompleteness, Handoff Permission Downgrade)
- **Approval & Gating**: Mandatory approval checks are bypassed or skipped due to race conditions or timeout defaults. (Handoff Approval Skipped)
- **Synchronization & Timing**: Receiving agents miss or reject handoffs due to timing, version, or readiness mismatches. (Handoff Timing Mismatch, Handoff Protocol Version Mismatch, Handoff Circular Dependency)
- **Idempotency & Rollback**: Handoff retries or rollbacks cause duplicate executions, or rollbacks fail because no owner can be found. (Handoff Idempotency Violation, Handoff Rollback Failure)

## When Agent-Handoffs-Delegation Matters

1. **Multi-Stage Approval Workflows**: Payment processing, deployment pipelines, or contract reviews that require stage-gates or human sign-offs. Handoff failures here leak unapproved actions into production.

2. **Long-Running Task Chains**: Customer support escalations, data processing pipelines, or cross-team project handoffs spanning hours or days. Handoff failures here create orphaned work that no one is actively resolving.

3. **Heterogeneous Agent Clusters**: Systems where different agent versions, tool sets, or schemas need to cooperate on the same task. Handoff failures here occur when sending and receiving agents use incompatible protocols or have diverged permissions.

## Cross-Pattern Insight

All handoff failures share a common root: **the sending agent defines "done" as transmission, not completion**. Ownership, context, approval, and timing are all treated as implicit rather than explicit. A receiving agent is assumed to own the task by default, context is assumed to be sufficient because the sender thought it was relevant, approval is assumed to have succeeded if the timeout expired, and protocol compatibility is assumed because the agents worked yesterday. Each implicit assumption is individually fragile, and when multiple agents are chained together, implicit assumptions about ownership, context, approval, and timing compound. A system where handoffs are reliable treats every assumption as a precondition: the receiving agent must explicitly acknowledge ownership, the handoff payload must match a schema, the approval token must be cryptographically valid, and the versions must be negotiated. Without explicit precondition enforcement, handoff failures are inevitable in multi-agent systems of any scale.

## Frequently Asked Questions

**Can the receiving agent be responsible for validating handoff completeness?**
Partially. A receiving agent can refuse to act if context is incomplete (constraint-checking) or if an approval token is missing (gating). However, the sending agent is still responsible for ensuring the handoff payload meets the defined schema and for acknowledging the receiving agent's state before initiating the transfer. If the receiving agent is in a degraded or temporarily unavailable state, the sending agent has no way to know unless handoff preconditions include an explicit readiness check.

**How do structured state transfers differ from free-text summaries?**
Structured state transfers (e.g., a JSON object with required fields for constraints, decisions, and metadata) allow a receiving agent to programmatically check for missing fields before acting. Free-text summaries require the receiving agent to parse prose and infer what's important, which is lossy. Teams comparing summary-based vs. structured handoff payloads report markedly fewer downstream correctness errors with structured transfers.

**What is the difference between handoff idempotency and handoff approval?**
Idempotency concerns whether replaying the same handoff (due to sender-side retry or network redelivery) causes the receiving agent to execute twice. Approval concerns whether the sender is authorized to make the handoff at all. Both can fail independently: an approved handoff might be re-executed idempotently, or an unapproved handoff might execute only once but still violate audit requirements.

**How can a team detect handoff failures in production?**
1. Instrument the orchestration layer to track "handoff initiated" and "receiving agent acknowledged ownership" as separate events, and alert if the gap exceeds a configured threshold.
2. Maintain a queryable registry of all tasks with a non-terminal state and their current owner; periodically reconcile against agent activity logs.
3. For approval-gated handoffs, continuously reconcile "approval granted" events against "downstream action taken" events by task ID, and alert on any action lacking a matching approval.

**What happens if the receiving agent crashes before acknowledging ownership?**
The ownership TTL should trigger: if the owning agent hasn't produced a status update or completion signal before the TTL expires, the orchestrator should automatically escalate to a human or reassign to a fallback agent. Without explicit ownership tracking, silent stalling of unowned tasks is completely invisible.

## Failure Patterns

| Pattern | Description |
|---------|-------------|
| [Handoff Accountability Loss](failures/handoff-accountability-loss.md) | Tasks marked "handed off" sit in a queue with no active owner, stalling silently for hours or days. |
| [Handoff Approval Skipped](failures/handoff-approval-skipped.md) | Mandatory approval gates are bypassed due to fire-and-forget requests that timeout to "proceed" instead of "block and escalate". |
| [Handoff Circular Dependency](failures/handoff-circular-dependency.md) | Agent A hands off to agent B, which hands off to agent C, which hands back to agent A, creating a loop. |
| [Handoff Context Incompleteness](failures/handoff-context-incompleteness.md) | Receiving agent receives a summarized context and lacks critical details, re-requesting information already gathered upstream. |
| [Handoff Idempotency Violation](failures/handoff-idempotency-violation.md) | Retrying or replaying a handoff causes the receiving agent to execute the task twice. |
| [Handoff Permission Downgrade](failures/handoff-permission-downgrade.md) | Receiving agent has fewer permissions than the sending agent and cannot complete the task. |
| [Handoff Protocol Version Mismatch](failures/handoff-protocol-version-mismatch.md) | Sending and receiving agents use incompatible handoff payload schemas, causing silent parsing failures. |
| [Handoff Rollback Failure](failures/handoff-rollback-failure.md) | An action taken post-handoff cannot be rolled back because the original owning agent is no longer available. |
| [Handoff State Loss](failures/handoff-state-loss.md) | Receiving agent receives a handoff with no working state, having to re-derive or re-fetch everything from scratch. |
| [Handoff Timing Mismatch](failures/handoff-timing-mismatch.md) | Receiving agent isn't ready when the handoff arrives, or filtering/queue configuration causes it to be silently dropped. |

**Total: 10 patterns**

## Related Goals

- [Input-Output-Handling](../input-output-handling/README.md) — handoff failures often manifest as the receiving agent receiving malformed or incomplete input
- [State-Tracking](../state-tracking/README.md) — maintaining task state through handoff transitions is a prerequisite for detecting ownership gaps
- [Dependency-Management](../dependency-management/README.md) — handoff chains are a form of task dependency; broken dependencies lead to orphaned handoffs
- [Multi-Agent-Orchestration](../multi-agent-orchestration/README.md) — orchestration layer must enforce handoff preconditions to prevent accountability loss
- [Fault-Tolerance](../fault-tolerance/README.md) — handoff failures are a category of transient fault; recovery requires explicit ownership and idempotency checks
