# What Are the Most Common Plan-Construction and Execution Failures in AI Agents?

**Planning failures happen when the plan an agent builds — or its absence — doesn't match what the task actually requires**, whether that means splitting the work into the wrong subtasks, inventing tools that don't exist, skipping a prerequisite check, or continuing to execute a plan the world has already invalidated. Planning sits between goal understanding and action execution, and a broken plan produces the same downstream damage as a broken action even when the agent's authorization, targeting, and intent were all otherwise correct.

## Key Takeaways

- 10 distinct failure patterns affect planning, and only 2 carry elevated catastrophic risk on their own — no-rollback-plan ("Rare but Catastrophic") and over-planning ("Rare") — while the other 8 are "Common" or "Occasional," meaning most planning failures are frequent but individually correctable rather than singularly catastrophic.
- Planning is the only goal in the by-capability taxonomy that documents a bidirectional failure pair on the same axis: no-plan-before-action (too little planning) and over-planning (too much planning) — proof that planning has a correct middle, not a "more planning is always safer" rule.
- The dominant architecture pattern across the majority of planning's 10 patterns is a decoupled validator or gate service — a planner-critic loop, a plan validator microservice, a DAG ordering engine, a finalize-gate service — that checks the plan independently of the model that generated it, rather than the planning model grading its own output.
- Plan-hallucination's Prevention section is unusually structural among LLM failure patterns: it recommends constraining plan generation to schema-validated function-calling against a live tool registry, so a fabricated tool name is rejected by the output format itself, not caught after the fact.

## Scope

- **Plan Construction Errors** — [Bad Task Decomposition](failures/bad-task-decomposition.md), [Plan Hallucination](failures/plan-hallucination.md), [Missing Prerequisite Step](failures/missing-prerequisite-step.md). The plan itself is wrong, fabricated, or incomplete at the moment it's created.
- **Plan-Reality Synchronization** — [Plan-State Mismatch](failures/plan-state-mismatch.md), [Wrong Order Of Operations](failures/wrong-order-of-operations.md). The plan doesn't match the actual state of the world or the safe sequencing constraints at the moment it's executed.
- **Planning/Execution Balance** — [No Plan Before Action](failures/no-plan-before-action.md), [Over-Planning](failures/over-planning.md). The agent gets the tradeoff between deliberation and action wrong in either direction.
- **Completion & Resilience** — [Premature Finalization](failures/premature-finalization.md), [Single-Path Planning](failures/single-path-planning.md), [No Rollback Plan](failures/no-rollback-plan.md). The plan lacks the robustness to finish correctly, recover from a failed step, or survive contact with an irreversible action.

## When Planning Matters

- Multi-step or multi-tool agentic workflows, as opposed to single-turn question-answering where there's effectively nothing to decompose or sequence
- Tasks involving irreversible or costly actions, where a missing rollback step or an out-of-order operation compounds a later mistake instead of just producing a wrong answer
- Long-running workflows where new tool results or user corrections can arrive mid-execution and invalidate assumptions the original plan was built on

## Cross-Pattern Insight

The majority of planning's 10 patterns fix planning quality the same way: introduce a component that checks the plan and is architecturally separate from the component that generated it — a critic pass that scores decomposition coverage, a plan-validator microservice that resolves every tool reference against a live registry, a DAG engine that rejects out-of-order calls, a finalize-gate that blocks incomplete checklists, and a stale-plan detector that fingerprints the world state a plan was built against. The reason that separation recurs across every construction, synchronization, and completion pattern is the same: a model that produced a flawed plan is systematically unreliable at grading that same plan as flawed, so independent validation catches what self-review misses.

## Frequently Asked Questions

### What's the difference between no-plan-before-action and bad-task-decomposition?
No-plan-before-action is skipping planning altogether — the agent jumps straight into tool calls on a complex task with no decomposition step at all. Bad-task-decomposition means the agent did plan, but split the task into subtasks that don't cover the actual acceptance criteria, leaving gaps even though a plan exists.

### How is plan-hallucination different from plan-state-mismatch?
Plan-hallucination is a plan referencing tools, data sources, or permissions that never existed in the first place — a fabrication problem, caught by validating references against a live registry. Plan-state-mismatch is a plan that referenced real things correctly at creation time, but the world has since changed (a user correction, a contradicting tool result) and the agent keeps executing the now-stale plan anyway.

### Is over-planning as risky as under-planning?
No — over-planning is rated "Rare" while no-plan-before-action is rated "Common," making under-planning the far more frequent failure in production. Both are handled by the same class of fix (a budget enforced at the orchestrator level), just applied in opposite directions: a floor that forces planning to happen, and a ceiling that forces planning to stop.

### What's the single biggest reliability fix that generalizes across planning failures?
A decoupled plan-validator or gate service — see the Cross-Pattern Insight above. It appears in some form (critic loop, validator microservice, DAG engine, finalize gate, stale-plan detector) in nearly every one of the 10 patterns' Architecture Patterns sections.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Bad Task Decomposition](failures/bad-task-decomposition.md) | Agent splits a task into the wrong subtasks, causing missed work |
| [Missing Prerequisite Step](failures/missing-prerequisite-step.md) | Agent skips a required validation, lookup, permission check, or confirmation |
| [No Plan Before Action](failures/no-plan-before-action.md) | Agent jumps into tool calls without decomposing the workflow first |
| [No Rollback Plan](failures/no-rollback-plan.md) | Agent performs irreversible actions without a defined recovery strategy |
| [Over-Planning](failures/over-planning.md) | Agent spends excessive time re-planning instead of acting |
| [Plan Hallucination](failures/plan-hallucination.md) | Agent invents tools, data, permissions, or workflow steps that don't exist |
| [Plan-State Mismatch](failures/plan-state-mismatch.md) | Agent continues executing an old plan after new evidence has invalidated it |
| [Premature Finalization](failures/premature-finalization.md) | Agent returns a final answer before completing required subtasks |
| [Single-Path Planning](failures/single-path-planning.md) | Agent has no fallback strategy when its first route fails |
| [Wrong Order Of Operations](failures/wrong-order-of-operations.md) | Agent executes steps in an unsafe or ineffective order |

**Total: 10 patterns**

## Related Goals

- [Goal Understanding](../goal-understanding/) — unclear-stop-condition and wrong-success-criteria cover the goal-level version of the same completion-definition gap that premature-finalization addresses at the plan level
- [Action Execution](../../../external-actions/goals/action-execution/) — single-path-planning and wrong-order-of-operations are the planning-time root causes behind several execution-time failures like premature-action
- [Domain Decisions](../../../domain-expertise/goals/domain-decisions/) — missing-prerequisite-step often surfaces as a domain-rule-miss or regulatory-threshold-miss when the skipped prerequisite was a compliance check
