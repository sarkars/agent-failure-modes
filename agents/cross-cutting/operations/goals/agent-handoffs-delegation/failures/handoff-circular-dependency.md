# Handoff Circular Dependency

## Issue
Two (or more) agents are each configured to hand off a task to the other under specific conditions, and those conditions form a cycle: Agent A decides the task needs Agent B's capability and hands it off, Agent B decides the task actually needs Agent A's capability and hands it back, and neither agent's handoff logic contains a way to recognize that the task has already been through this loop. The task bounces indefinitely (or until an unrelated resource limit like a timeout or step cap kills it) without either agent making progress on the underlying work.

**Frequency**: Occasional

**Symptoms**
- A task's handoff log shows the same two (or more) agent IDs alternating repeatedly
- Task processing time or step count grows without bound until an external timeout or budget cap intervenes
- Neither agent's individual logs show an error — each handoff is locally "correct" given that agent's routing rules
- The task's actual payload/state is unchanged across many consecutive handoff events

## Root Cause
Handoff routing is typically implemented as local, per-agent decision logic — each agent evaluates "does this task match my capability, or should I route it elsewhere?" independently, with no global view of the task's routing history. When two agents' routing rules are complementary in a way the designers didn't anticticipate (A routes anything with condition X to B, B routes anything with condition Y back to A, and a given task satisfies both X and Y), the cycle is invisible to either agent because each only sees the task as it currently is, not the sequence of hops that produced it. Without a shared, task-attached history of prior hops, there is nothing to compare against to detect that the loop is repeating rather than progressing.

## Example
```
A support-ticket workflow has a "billing-agent" and a "technical-agent."
billing-agent's rule: if a ticket mentions an error message or stack
trace, route to technical-agent (likely a technical issue, not billing).
technical-agent's rule: if a ticket mentions a charge, invoice, or dollar
amount, route to billing-agent (likely a billing issue, not technical).

Ticket #7734: "I was charged twice and got error E-4021 when I tried to
get a refund through the portal."

billing-agent sees "error E-4021" -> routes to technical-agent.
technical-agent sees "charged twice" -> routes to billing-agent.
billing-agent sees "error E-4021" again -> routes to technical-agent.

This repeats 40 times over 6 minutes until the orchestrator's per-task
hop-count limit (40) kills the task and files it as "unresolved: hop
limit exceeded." No agent ever attempted to resolve the actual ticket,
which required both a refund adjustment and clearing a portal error --
a case neither agent's single-condition routing rule was built to
recognize as "needs both."
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 2-5% of multi-agent routing failures in systems with 3+ interacting routing agents involve a two- or three-agent cycle | Typical range observed in workflow orchestration incident data |
| Adding hop-count and repeat-pair detection to routing logic catches the large majority of circular handoffs before any hard timeout is hit | Reported range across teams adding cycle detection |
| Tasks caught in circular handoffs before mitigation typically consume 5-15x the compute/step budget of a normally routed task before failing | Estimated from orchestrator telemetry on hop-limited tasks |

## Mitigations
1. **Handoff history attached to task state**: Carry a list of prior agent hops with the task itself, so each routing decision can check "have I already sent this exact task to this agent before?" and refuse to repeat a hop.
2. **Cycle detection at the orchestrator**: Have the orchestration layer (not individual agents) track the hop sequence per task and halt with an escalation when a repeating pattern (A→B→A→B) is detected, rather than relying on a generic hop-count ceiling alone.
3. **Joint-condition routing rules**: Where two agents' routing conditions can both match the same task, add an explicit joint-ownership or "needs both" rule rather than leaving two independent either/or rules that can chain into each other.
4. **Hop budget with meaningful failure mode**: Cap total hops per task, but route hop-limit failures to a human triage queue with the full hop history attached, not to a generic "unresolved" bucket that discards the diagnostic trail.
5. **Routing rule conflict testing**: Before deploying new routing rules, simulate them against representative task payloads to check for rule pairs that could form a cycle, similar to testing for infinite loops in code review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| repeated_agent_pair_hops | Count of times the same ordered pair of agents appears consecutively in a task's hop history | Alert if >= 2 |
| task_hop_count | Total number of handoffs a single task has undergone | Alert if > 3x the workflow's median hop count |
| hop_limit_exceeded_rate | Rate of tasks failing due to hitting the maximum hop count | Alert if > 0.5% of tasks |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Routing cycle detected | The same agent-pair sequence repeats twice or more for a single task | High | Halt routing for the task, escalate to human triage with full hop history |
| Hop budget near exhaustion | task_hop_count reaches 80% of the configured maximum | Medium | Flag task for review before the hard cutoff discards routing context |

## Related Patterns
- [Handoff Timing Mismatch](./handoff-timing-mismatch.md) - both involve handoff logic that is locally correct but globally dysfunctional across agent boundaries
- [Handoff Accountability Loss](./handoff-accountability-loss.md) - a circularly-routed task also has no single owner, compounding the difficulty of noticing the loop
- [Handoff Context Incompleteness](./handoff-context-incompleteness.md) - incomplete context about prior routing decisions is often what allows a cycle to go undetected
