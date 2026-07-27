# What Are the Most Common External-Action Failures in AI Agents?

**AI agents most often fail at external actions not in deciding what to do, but in the mechanics of doing it safely** — acting without authorization, hitting the wrong target, firing the same action twice, or executing an action with no way to undo it. External-action failures matter more than most because external actions are the point where an agent stops reasoning internally and starts changing the state of a real system — a payment processor, a production deployment, a customer's account — where the consequences of a mistake exist independently of whatever reasoning produced the mistake.

## Key Takeaways

- External actions currently cover 1 goal — Action Execution — and 11 failure patterns, the largest single-goal pattern count among capability categories reviewed alongside it.
- 7 of the 11 patterns (duplicate-action, insufficient-rollback, irreversible-action-without-confirmation, policy-violating-action, unauthorized-action, unbounded-action-loop, wrong-target-action) are rated "Rare but Catastrophic" — the highest concentration of catastrophic-tier patterns of any capability goal, because action execution is where a reasoning error becomes an irreversible real-world consequence.
- Nearly every pattern sets its production metric target at exactly 0 or 100% rather than an acceptable tolerance band, treating action execution as a zero-tolerance surface rather than one to optimize incrementally.
- The shared architecture across all 11 patterns is a fail-closed gateway between the agent and the real system — idempotency middleware, capability tokens, policy engines, confirmation gates — where the default behavior on missing authorization is to block, not to allow.

## External Actions Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Action Execution](goals/action-execution/) | Authorization, targeting, execution integrity, and containment when an agent acts on external systems | 11 |

**Total: 11 patterns**

## How the Goals Relate

External actions is currently a single-goal category, so there's no internal pipeline to describe — Action Execution covers the full arc from whether an action is authorized at all, through whether it's aimed at the right target and fires cleanly exactly once, to whether its consequences can be contained or undone. If a debugging session narrows to "the agent's decision was right but something went wrong when it acted on it," Action Execution is the goal to check, and which pattern applies depends on which part of that arc broke: authorization, execution mechanics, targeting/timing, or rollback/containment.

## Frequently Asked Questions

### What's the difference between an action-execution failure and a domain-decision failure?
A domain-decision failure means the agent chose the wrong course of action given the facts (e.g., approving a refund a policy doesn't allow). An action-execution failure means the agent's chosen course of action was correct, but something broke in carrying it out — it hit the wrong target, fired twice, or executed with no rollback path. Policy-violating-action sits at the boundary: the decision to violate policy and the act of violating it happen in the same step. See [Domain Expertise](../domain-expertise/).

### Can a better or more capable model fix action-execution failures on its own?
No. Every pattern's Prevention section relies on infrastructure the model doesn't control directly — idempotency keys, capability tokens, policy engines, target-confirmation UIs, rollback registries — because action-execution failures are zero-tolerance failure modes where the fix has to be enforced by a gateway the agent cannot bypass, not by hoping the model reasons its way to the right call every time.

### Which action-execution pattern should a developer check first when debugging an unwanted external action?
Start with what went wrong: if the agent shouldn't have been able to act at all, check unauthorized-action or policy-violating-action; if the action itself misfired, check duplicate-action, partial-execution, or unbounded-action-loop; if it hit the wrong entity or branch, check wrong-target-action, wrong-workflow-branch, or premature-action; if the aftermath couldn't be contained, check insufficient-rollback or external-side-effect-surprise.

## Related Categories

- [Domain Expertise](../domain-expertise/) — the judgment failures (rule misses, authority overreach) that often precede a policy-violating or unauthorized action
- [Task Planning](../task-planning/) — the planning-time gaps (no-rollback-plan, missing-prerequisite-step) that directly cause several action-execution failures downstream
- [Multi-Agent Systems](../multi-agent-systems/) — coordination failures between multiple agents that can independently trigger the same external action, compounding duplicate-action risk
