# What Are the Most Common Planning-and-Decomposition Failures in AI Agents?

**Agents often need to break complex tasks into subtasks, order the steps, and adapt plans when conditions change. Planning-and-decomposition failures occur when agents create invalid plans (missing steps, circular dependencies), hallucinate steps that don't exist, fail to adapt when circumstances invalidate the plan, or execute subgoals in the wrong order, resulting in wasted effort, impossible tasks, or cascading downstream failures.**

## Key Takeaways

1. **Plan Hallucination Is Plausible but Wrong**: Agents can generate plans that sound reasonable (all subtasks are listed, logic appears sound) but are fundamentally unachievable or omit critical steps. The agent has no way to validate that a plan is executable without actually attempting it.

2. **Circular Dependencies in Plans Cause Infinite Loops**: A plan that requires subtask A to complete before B, and B to complete before A, is circular. The agent may execute indefinitely or timeout without recognizing the cycle. Circular plans must be detected at plan-generation time, not at execution time.

3. **Cost Estimation in Plans Is Wildly Inaccurate**: Agents estimate that a plan will cost X tokens or take Y seconds, but execution costs 10x more or takes 100x longer. Plans that looked reasonable based on estimated cost are infeasible under actual costs.

4. **Plan Invalidation Is Silent**: Circumstances change (a dependency is no longer available, a constraint is now impossible), but the agent is executing a plan based on old assumptions. Plan invalidation detection requires continuous re-evaluation of preconditions and constraints during execution.

## Scope

Planning-and-decomposition failures cluster into five categories:

- **Invalid Plans at Generation**: Plans are missing steps, have circular dependencies, or are hallucinated. (plan-hallucination-detection-failure, plan-dependency-cycle, contingency-plan-missing)
- **Subgoal Ordering & Parallelization**: Subgoals are executed in wrong order or parallelized incorrectly, violating dependencies. (subgoal-ordering-error, plan-parallelization-error)
- **Plan Adaptation & Invalidation**: Plans become invalid during execution; agent continues with invalidated plan. (plan-invalidation-not-detected, plan-adaptability-failure)
- **Plan Optimization Pathologies**: Plan optimization produces worse outcomes than unoptimized plans. (plan-optimization-pathological)
- **Cost Estimation & Backtracking**: Estimated cost was wrong; plan needs to be aborted or backtracked. (plan-cost-estimation-failure, plan-backtracking-failure)

## When Planning-and-Decomposition Matters

1. **Complex Multi-Step Tasks**: Tasks that require ordering (task A must complete before task B), or conditional logic (if X, then do Y, else do Z). Poor planning leads to wasted effort and impossible tasks.

2. **Resource-Constrained Agents**: Agents with limited budget (tokens, time, compute). Poor cost estimation causes plans to exceed budget mid-execution.

3. **Dynamic, Changing Environments**: Systems where assumptions can be invalidated (a service goes down, a dependency changes). Plans must detect and adapt to changed conditions.

## Cross-Pattern Insight

Planning and decomposition is fundamentally about **executing complex tasks without actually doing all the work beforehand**. An agent can't feasibly try all possible plans and measure which is best; it must decompose the task, estimate what will work, and execute. But estimates are often wrong, hallucination is common, and environments change. Robust planning requires: (1) validating generated plans for structural soundness (no circular dependencies, required steps are present); (2) continuously re-evaluating plan preconditions during execution (is dependency X still available?); (3) detecting when cost estimates are wildly off (if spent tokens exceed 3x estimated, abort and replan); (4) having a fallback plan or contingency (if plan A fails, what's plan B?); and (5) regular testing of failure scenarios (chaos engineering for planning). Without these, agents execute plans that are hallucinated, circular, or invalidated, wasting resources and failing to make progress.

## Frequently Asked Questions

**How can an agent validate that a generated plan is achievable before executing it?**
Run a simplified version of the plan to check for obvious failures (circular dependencies, missing preconditions). Use domain-specific validators if available. Estimate the cost to execute the plan; if cost is very high, ask a human or fallback to a simpler plan. Don't just trust that a plausible-sounding plan is achievable; validate.

**What should an agent do if a plan's cost estimation is wildly wrong (estimated 10 tokens, actually 100)?**
Detect the divergence early: after the first few steps, measure actual cost vs. estimated cost. If actual cost is >3x estimate, abort the plan and replan. Don't continue executing a plan that's proven its estimates wrong; you'll waste resources trying to complete an infeasible plan.

**How can an agent detect that plan preconditions have become invalid?**
Before each subgoal, re-check the preconditions that were assumed when the plan was generated. For example, if the plan assumed "API X is available," check that API X is still available before executing a step that depends on it. If a precondition is no longer true, abort or replan.

**What is the difference between plan backtracking and plan adaptation?**
Backtracking: the agent realizes a subgoal failed and returns to a previous step to try a different path. Adaptation: the agent detects that the original plan is no longer achievable (due to changed circumstances) and creates a new plan. Backtracking is recovery within a single plan; adaptation is changing strategies.

**Can an agent avoid circular dependencies in plans entirely?**
Through validation: after generating a plan, construct the dependency graph and check for cycles using standard graph algorithms. If cycles are detected, the plan is invalid and should be rejected before execution. This check must happen before execution, not during.

## Failure Patterns

| Pattern | Description |
|---------|-------------|
| [Contingency Plan Missing](failures/contingency-plan-missing.md) | Agent has a primary plan but no contingency if the primary fails; when primary fails, agent is stuck. |
| [Plan Adaptability Failure](failures/plan-adaptability-failure.md) | Plan becomes invalid (dependencies no longer available, constraints infeasible); agent doesn't adapt and continues with invalid plan. |
| [Plan Backtracking Failure](failures/plan-backtracking-failure.md) | Agent needs to backtrack to a previous step after a failed subgoal; backtracking logic fails or leaves state inconsistent. |
| [Plan Cost Estimation Failure](failures/plan-cost-estimation-failure.md) | Estimated cost to execute plan is wildly inaccurate; plan exceeds budget mid-execution. |
| [Plan Dependency Cycle](failures/plan-dependency-cycle.md) | Plan contains a circular dependency (A must complete before B, B must complete before A); impossible to execute. |
| [Plan Hallucination Detection Failure](failures/plan-hallucination-detection-failure.md) | Plan contains hallucinated steps (steps agent generated but can't actually execute); agent doesn't detect and attempts to execute. |
| [Plan Invalidation Not Detected](failures/plan-invalidation-not-detected.md) | Circumstances change during execution, invalidating plan preconditions; agent continues with invalidated plan. |
| [Plan Optimization Pathological](failures/plan-optimization-pathological.md) | Optimization to improve plan actually makes it worse (slower, more expensive, or infeasible). |
| [Plan Parallelization Error](failures/plan-parallelization-error.md) | Agent parallelizes subgoals that have undetected dependencies; parallel execution violates the dependencies. |
| [Subgoal Ordering Error](failures/subgoal-ordering-error.md) | Agent executes subgoals in wrong order, violating explicit or implicit dependencies. |

**Total: 10 patterns**

## Related Goals

- [Fault-Tolerance](../fault-tolerance/README.md) — plan backtracking and adaptation are recovery strategies; fault-tolerance mechanisms support replanning
- [Agent-Handoffs-Delegation](../agent-handoffs-delegation/README.md) — decomposed subgoals are often handed off to other agents; handoff failures manifest as planning failures
- [Multi-Agent-Orchestration](../multi-agent-orchestration/README.md) — orchestration layer must enforce subgoal ordering and detect circular dependencies
- [Cost-Efficiency](../cost-efficiency/README.md) — cost estimation in planning affects overall cost efficiency
- [Monitoring-and-Alerting](../monitoring-and-alerting/README.md) — detecting plan invalidation and cost divergence requires active monitoring
