# What Are the Most Common Task-Planning Failures in AI Agents?

**AI agents most often fail at task planning not by being unable to plan, but by misreading the goal before planning starts or building a plan that doesn't survive contact with reality** — an ambiguous request answered with the wrong interpretation, a goal that quietly drifts over a long session, a plan built around a hallucinated tool, or a plan kept running after the world it was built for has already changed. Task planning sits upstream of action execution: a flawlessly authorized, correctly-targeted action still produces the wrong outcome if the goal or plan driving it was wrong to begin with.

## Key Takeaways

- Task planning spans 2 goals and 20 failure patterns: Goal Understanding (10 patterns, covering interpretation, stability, objectives, and completion definition) and Planning (10 patterns, covering construction, synchronization, planning/execution balance, and resilience).
- No pattern in either goal is rated "Rare but Catastrophic" except one — no-rollback-plan — making task planning the lowest catastrophic-risk-concentration category among the ones reviewed alongside it, since planning failures are usually correctable before they cause irreversible harm.
- Both goals independently converge on the same fix: replace an inferred, re-derived-each-turn notion of "the goal" or "the plan" with a durable, structured, versioned object, checked by a component separate from the one that generated it — a goal contract, a termination-criteria spec, a plan-validator microservice, a DAG ordering engine.
- Planning documents the only bidirectional failure pair in the by-capability taxonomy on a single axis — no-plan-before-action (too little planning) and over-planning (too much) — showing that the planning/execution tradeoff has a correct middle, not a monotonic "more planning is safer" rule.

## Task Planning Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Goal Understanding](goals/goal-understanding/) | Interpreting, preserving, and correctly closing out the user's or business's actual goal across a session | 10 |
| [Planning](goals/planning/) | Decomposing, sequencing, validating, and executing a plan that matches what the task and the world actually require | 10 |

**Total: 20 patterns**

## How the Goals Relate

Goal Understanding runs first, conceptually: an agent has to correctly interpret and anchor the goal before a plan can be built to serve it. Planning runs next, translating an understood goal into a decomposed, ordered, validated sequence of steps. The two goals share failure shapes rather than a strict pipeline, though — goal-drift and plan-state-mismatch are the same underlying problem (a stale reference point) expressed at different altitudes, and unclear-stop-condition/wrong-success-criteria (goal level) pair directly with premature-finalization (plan level) as the same completion-definition gap. To localize an incident by symptom: the agent solved the wrong problem entirely → **Goal Understanding**; the agent understood the ask but the steps taken to get there were wrong, missing, or out of order → **Planning**; the agent's plan and goal were both fine but something broke when acting on the finalized plan → [Action Execution](../external-actions/goals/action-execution/).

## Frequently Asked Questions

### What's the difference between a goal-understanding failure and a planning failure?
Goal-understanding failures happen before any plan exists — the agent misreads, loses track of, or falsely completes the underlying goal itself. Planning failures happen after the goal is correctly understood — the agent builds the wrong subtasks, the wrong order, or a plan that no longer matches the current state of the world. Wrong-success-criteria and premature-finalization sit closest to the boundary: one is a false claim about the whole task, the other a false claim about a single step within a plan.

### Can a stronger model fix task-planning failures on its own?
No. Both goals' Prevention sections rely on external structure the model can't provide by itself — a goal-contract object checked by a drift detector, a plan-validator microservice that resolves tool references against a live registry, a DAG engine that enforces safe ordering. A stronger model may make fewer individual mistakes, but the two goals' mitigations exist because the failure mode is architectural (no independent check on the model's own claim about the goal or plan), not a capability gap.

### Which goal should a developer check first when an agent's output is clearly wrong?
Ask whether the agent solved the right problem at all: if it answered a different question than intended, expanded scope unasked, or declared success without the real-world state changing, check [Goal Understanding](goals/goal-understanding/). If it correctly understood the ask but the steps taken were incomplete, wrongly ordered, or built on a hallucinated tool, check [Planning](goals/planning/).

### How does task planning differ from long-horizon execution?
Task planning covers the correctness of the plan and the understanding of the goal driving it at any timescale, including single-session tasks. Long-horizon execution is specifically about compounding errors that only emerge over many hours or days of autonomous operation — a different failure surface even though a planning mistake early in a long-horizon task can be the seed of a later compounding failure. See [Long-Horizon Execution](../long-horizon-execution/).

## Related Categories

- [External Actions](../external-actions/) — where a correctly understood goal and validated plan get executed against real systems, and where planning-time gaps like missing-prerequisite-step and no-rollback-plan surface as action-execution failures
- [Domain Expertise](../domain-expertise/) — the domain-specific judgment layer that a plan's individual steps often depend on getting right
- [Long-Horizon Execution](../long-horizon-execution/) — compounding failures specific to multi-hour or multi-day autonomous execution, distinct from single-session planning correctness
