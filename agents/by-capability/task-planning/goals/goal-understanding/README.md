# What Are the Most Common Goal-Understanding Failures in AI Agents?

**Goal-understanding failures happen when an agent optimizes for the wrong version of what it was asked to do** — a different meaning of an ambiguous request, a goal that quietly shifted over a long session, a metric that improved while the real outcome didn't, or a "done" state the agent invented because no one defined one. Goal-understanding failures sit upstream of everything else an agent does: a plan can be flawlessly executed and an action perfectly authorized, and the outcome is still wrong if the goal driving both was misread, drifted, or was never properly closed out.

## Key Takeaways

- 10 distinct failure patterns affect goal understanding, and none are rated "Rare but Catastrophic" — 7 are "Common" (ambiguous-goal-interpretation, business-policy-mismatch, conflicting-objectives, goal-drift-across-turns, goal-expansion-scope-creep, proxy-metric-optimization, wrong-success-criteria) and 3 are "Occasional" (hidden-requirement-miss, over-literal-goal-following, unclear-stop-condition), distinguishing goal understanding from action-execution and domain-decisions, where individual failures carry catastrophic-tier risk.
- Nearly every pattern's Prevention section replaces an inferred, re-derived-each-turn notion of "the goal" with a durable, structured, versioned object (a goal contract, a priority config, explicit termination criteria) that downstream components check mechanically instead of the model reconstructing intent from a growing conversation history.
- Detection across goal-understanding patterns consistently compares the agent's own claim against an independent signal — embedding similarity to an original goal anchor, reconciled downstream system state, or mined user-correction language — rather than trusting the agent's self-report that a goal was understood or satisfied.
- Two patterns describe opposite failure directions on the same axis: goal-drift-across-turns (the objective erodes) and goal-expansion-scope-creep (the objective balloons with unrequested extras) — both stem from the same root cause, a goal that isn't anchored to an immutable reference point.

## Scope

- **Interpretation Errors at Intake** — [Ambiguous Goal Interpretation](failures/ambiguous-goal-interpretation.md), [Over-Literal Goal Following](failures/over-literal-goal-following.md), [Hidden Requirement Miss](failures/hidden-requirement-miss.md). The agent misreads what was actually meant right from the start, before any drift or expansion has a chance to occur.
- **Goal Stability Over Time** — [Goal Drift Across Turns](failures/goal-drift-across-turns.md), [Goal Expansion / Scope Creep](failures/goal-expansion-scope-creep.md). A correctly-understood goal degrades or balloons as a long conversation or workflow progresses.
- **Objective & Metric Conflicts** — [Conflicting Objectives](failures/conflicting-objectives.md), [Proxy Metric Optimization](failures/proxy-metric-optimization.md), [Business-Policy Mismatch](failures/business-policy-mismatch.md). Multiple legitimate objectives exist simultaneously, and the agent optimizes or resolves the conflicting objectives incorrectly.
- **Completion Definition Failures** — [Unclear Stop Condition](failures/unclear-stop-condition.md), [Wrong Success Criteria](failures/wrong-success-criteria.md). The agent has no reliable way to know when the goal has actually been achieved, either looping indefinitely or declaring success prematurely.

## When Goal Understanding Matters

- Long multi-turn conversations or multi-step workflows where the original request could be diluted, reinterpreted, or quietly expanded over time
- Tasks with multiple legitimate but competing objectives — speed vs. accuracy, helpfulness vs. compliance, throughput vs. quality — where a tradeoff has to be resolved deterministically rather than ad hoc
- Autonomous agents that must decide for themselves when a task is "done" without an explicit, externally verifiable stopping signal

## Cross-Pattern Insight

Every goal-understanding pattern fixes the same underlying gap the same way: give the goal a durable, external representation — a goal contract object, a ranked objective-priority config, an explicit termination-criteria spec, a requirement checklist — and have an independent component check the agent's behavior against that representation, rather than letting the same model that is executing the task also self-certify that it understood, preserved, or completed the goal correctly. The recurring failure signature across Detection & Response sections is silence: an agent reinterprets, drifts, expands scope, or declares false success without any explicit signal that something changed, which is why nearly every mitigation pairs a structural anchor with continuous, automated divergence monitoring rather than a one-time check at task start.

## Frequently Asked Questions

### What's the difference between goal drift and scope creep?
Goal-drift-across-turns is the original objective itself eroding or shifting over a long session — later actions no longer match the initial goal statement. Goal-expansion-scope-creep is the agent layering additional, unrequested actions on top of a goal that hasn't necessarily changed — extra API calls, extra messages, side effects nobody asked for. Both stem from the same missing anchor, but drift changes what the agent is pursuing, and scope creep changes how much it does in pursuit of it.

### How is wrong-success-criteria different from unclear-stop-condition?
Unclear-stop-condition means the agent doesn't know when to stop and keeps looping, retrying, or asking because "done" was never defined. Wrong-success-criteria means the agent believes it's done and reports success, but the real-world downstream state never actually changed — one is a failure to stop, the other is a false claim of completion.

### Can better prompting alone fix ambiguous-goal-interpretation?
No. Its Prevention section calls for a structured goal-restatement gate and interpretation-enumeration scoring that blocks auto-execution when multiple plausible readings exist — a structural clarification checkpoint outside the model's own discretion, not a prompt instruction to "ask if unsure."

### Which patterns matter most for agents optimized against a training or business metric?
Proxy-metric-optimization directly covers an agent improving an easy metric while harming the real outcome, and conflicting-objectives and business-policy-mismatch cover the adjacent failure of a compliance or policy objective losing out to a more heavily-weighted objective like helpfulness or speed.

### Is goal drift only a risk in very long conversations?
The mitigation strategies target sessions above roughly 10-15 turns with periodic re-anchoring checkpoints, but the underlying risk — recency bias diluting an earlier goal statement — starts accumulating from the first turn where intervening context begins to outweigh the original goal statement in the model's effective context.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Ambiguous Goal Interpretation](failures/ambiguous-goal-interpretation.md) | Agent optimizes for a different meaning of the user's or business goal |
| [Business-Policy Mismatch](failures/business-policy-mismatch.md) | Agent completes a technical action that violates company policy |
| [Conflicting Objectives](failures/conflicting-objectives.md) | Agent cannot resolve tradeoffs like speed vs. accuracy or helpfulness vs. compliance |
| [Goal Drift Across Turns](failures/goal-drift-across-turns.md) | Agent's objective changes over long conversations or workflows |
| [Goal Expansion / Scope Creep](failures/goal-expansion-scope-creep.md) | Agent performs additional actions that were never requested |
| [Hidden Requirement Miss](failures/hidden-requirement-miss.md) | Agent misses unstated but critical constraints such as policy, geography, role, or SLA |
| [Over-Literal Goal Following](failures/over-literal-goal-following.md) | Agent follows the wording but violates user intent or common-sense constraints |
| [Proxy Metric Optimization](failures/proxy-metric-optimization.md) | Agent improves an easy-to-measure metric while harming the real outcome |
| [Unclear Stop Condition](failures/unclear-stop-condition.md) | Agent keeps looping, retrying, or asking because "done" was never defined |
| [Wrong Success Criteria](failures/wrong-success-criteria.md) | Agent reports success when the real-world task outcome is not actually complete |

**Total: 10 patterns**

## Related Goals

- [Planning](../planning/) — sequencing and decomposition failures that occur after the goal is understood but before it's correctly translated into steps
- [Action Execution](../../../external-actions/goals/action-execution/) — wrong-success-criteria's task-level false-completion failure has a direct action-level counterpart in partial-execution
- [Domain Decisions](../../../domain-expertise/goals/domain-decisions/) — business-policy-mismatch and conflicting-objectives connect to domain-rule-miss when the competing objective is a compliance rule rather than a generic policy
