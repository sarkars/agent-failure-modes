# What Are the Most Common External Action-Execution Failures in AI Agents?

**Action-execution failures happen when an agent's decision to act is correct but the act itself — its authorization, target, timing, or mechanics — is not**, so the agent ends up charging the wrong account, deleting something it can't restore, or looping a retry into a runaway cost. Action-execution failures matter more than most because the failures are the point where an agent stops reasoning and starts changing the state of a real external system — a payment processor, a ticketing system, a production deployment — where mistakes carry their own blast radius independent of whatever reasoning produced the mistake.

## Key Takeaways

- 11 distinct failure patterns affect action execution, and 7 of the 11 patterns (duplicate-action, insufficient-rollback, irreversible-action-without-confirmation, policy-violating-action, unauthorized-action, unbounded-action-loop, wrong-target-action) are rated "Rare but Catastrophic" — the highest concentration of catastrophic-tier patterns of any goal in the by-capability taxonomy, reflecting that action execution is where reasoning errors become irreversible real-world consequences.
- Nearly every pattern's metrics table sets a target of exactly 0 or 100% (zero unauthorized actions, zero duplicate attempts, 100% rollback success) rather than an acceptable error rate — action execution is treated as a zero-tolerance surface, not one to be optimized incrementally.
- The dominant architecture across all 11 patterns is a fail-closed gateway sitting between the agent and the real system: idempotency middleware, capability tokens, policy engines, and confirmation gates all share the same shape — no valid authorization/registry/confirmation entry means the call is blocked by default, not allowed by default.
- Four patterns (unauthorized-action, policy-violating-action, irreversible-action-without-confirmation, wrong-target-action) all require a pre-action gate that checks against an external source of truth (a capability token, a policy engine, a confirmation record, a target summary) rather than trusting the agent's own judgment about whether the action is appropriate.

## Scope

- **Authorization & Policy Boundary** — [Unauthorized Action](failures/unauthorized-action.md), [Policy-Violating Action](failures/policy-violating-action.md), [Irreversible Action Without Confirmation](failures/irreversible-action-without-confirmation.md). The agent executes an action it never had standing to take at all, or takes an irreversible action without the required human sign-off.
- **Execution Integrity** — [Duplicate Action](failures/duplicate-action.md), [Partial Execution](failures/partial-execution.md), [Unbounded Action Loop](failures/unbounded-action-loop.md). The action is authorized and correctly targeted, but the execution mechanics themselves break down — it fires twice, it half-completes while reporting success, or it never stops firing.
- **Targeting & Timing Correctness** — [Wrong Target Action](failures/wrong-target-action.md), [Wrong Workflow Branch](failures/wrong-workflow-branch.md), [Premature Action](failures/premature-action.md). The action is authorized and executes cleanly, but is aimed at the wrong entity, takes the wrong branch of a decision tree, or fires before enough evidence justified it.
- **Containment & Blast Radius** — [Insufficient Rollback](failures/insufficient-rollback.md), [External Side-Effect Surprise](failures/external-side-effect-surprise.md). Once the action executes, the system has no way to contain or reverse its consequences — either there's no undo path, or the action triggered effects (notifications, billing, cascades) nobody accounted for.

## When Action Execution Matters

- An agent has write or mutate access to external systems — billing, CRM, infrastructure, ticketing — rather than read-only or advisory access
- Actions under agent control are irreversible or expensive to reverse: deletes, payments, deployments, customer-facing sends
- The agent operates autonomously across multi-step or retry-heavy workflows, where a loop or a partial failure can compound cost or damage before a human notices

## Cross-Pattern Insight

All 11 action-execution patterns converge on the same architectural answer: separate "technically able to call this API" from "authorized and safe to call this API right now," and enforce that separation with a gateway the agent cannot bypass. Concretely, that means idempotency keys and state-transition guards for execution integrity, capability tokens and policy engines for authorization, target-confirmation summaries and evidence-threshold gates for targeting and timing, and pre-declared rollback/compensation plans plus side-effect manifests for containment. The common thread in every Detection & Response section is also structural: don't trust the agent's own success report — reconcile the actual state of the external system (audit trail divergence, state integrity checks, resource orphaning detection) against what the agent claims it did, because an agent that got the action wrong will often still report success.

## Frequently Asked Questions

### What's the difference between unauthorized-action and policy-violating-action?
Unauthorized-action means the agent lacks permission for the action or target resource at all — an identity/capability failure caught by a capability token or namespace check. Policy-violating-action means the agent has generic permission to perform that action type, but the specific instance breaks a business rule (e.g., a refund policy's dollar cap or time window) — caught by a policy engine evaluating the action's parameters, not just its identity.

### How does wrong-target-action differ from wrong-workflow-branch?
Wrong-target-action is the right action taken against the wrong entity — refunding the wrong customer's order. Wrong-workflow-branch is the right entity but the wrong action type chosen for it — issuing a refund when a replacement was the correct branch. Both are targeting/decision failures, but one is about "who," the other about "which path."

### Can idempotency keys alone prevent duplicate-action?
No. The duplicate-action mitigation pairs idempotency keys with state-transition guards and audit-trail divergence monitoring, because idempotency keys only catch a retry that reuses the same key — they don't catch two independently-initiated requests for the same real-world outcome, which requires comparing the intended action against the actual system-state delta.

### Which action-execution patterns require a human-in-the-loop step by design?
Irreversible-action-without-confirmation is explicitly built around mandatory human confirmation before execution. Insufficient-rollback and no-rollback-plan-adjacent patterns route to human approval whenever an action is classified as irreversible with no defined compensation. Premature-action and policy-violating-action both route to expert-in-the-loop review when evidence or policy checks fail.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Duplicate Action](failures/duplicate-action.md) | Agent creates duplicate tickets, emails, orders, or charges |
| [External Side-Effect Surprise](failures/external-side-effect-surprise.md) | Agent misses that an action triggers notifications, billing, shipment, or deployment |
| [Insufficient Rollback](failures/insufficient-rollback.md) | Agent cannot undo a bad action once executed |
| [Irreversible Action Without Confirmation](failures/irreversible-action-without-confirmation.md) | Agent deletes, sends, pays, or deploys without required approval |
| [Partial Execution](failures/partial-execution.md) | Agent completes only some steps of a multi-step action but reports full success |
| [Policy-Violating Action](failures/policy-violating-action.md) | Agent performs a technically possible but disallowed action |
| [Premature Action](failures/premature-action.md) | Agent acts before enough evidence is gathered |
| [Unauthorized Action](failures/unauthorized-action.md) | Agent performs an action without permission |
| [Unbounded Action Loop](failures/unbounded-action-loop.md) | Agent repeats an action until quota, cost, or damage accumulates |
| [Wrong Target Action](failures/wrong-target-action.md) | Agent acts on the wrong account, order, file, or user |
| [Wrong Workflow Branch](failures/wrong-workflow-branch.md) | Agent chooses the wrong branch — refund vs. replacement, escalation vs. resolution |

**Total: 11 patterns**

## Related Goals

- [Planning](../../../task-planning/goals/planning/) — no-rollback-plan and missing-prerequisite-step cover the planning-time gaps that directly cause insufficient-rollback and premature-action at execution time
- [Domain Decisions](../../../domain-expertise/goals/domain-decisions/) — domain-rule-miss and regulatory-threshold-miss are the judgment failures that often precede a policy-violating-action
- [Goal Understanding](../../../task-planning/goals/goal-understanding/) — wrong-success-criteria covers the false-completion-report failure at the task-outcome level, alongside partial-execution's action-level version
