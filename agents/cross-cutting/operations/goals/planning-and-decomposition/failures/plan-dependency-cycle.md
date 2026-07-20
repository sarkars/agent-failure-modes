# Plan Dependency Cycle

## Issue
When a planner decomposes a task into subtasks, it sometimes produces a set of dependencies where subtask A requires subtask B to complete first, B requires C, and C requires A — a circular dependency that has no valid execution order. Because the planner reasons about each dependency relationship locally (does this subtask need that one) rather than validating the full dependency graph globally, the cycle isn't caught at planning time, and the executor discovers the plan is structurally unexecutable only when it tries to find a starting point.

**Frequency**: Occasional

**Symptoms**
- The executor unable to find any subtask with zero unmet dependencies to start with
- Plan validation (if present) reporting a graph cycle rather than a clean topological order
- Subtasks that each reference "output of" or "requires completion of" another subtask in a way that traces back to themselves through the chain
- Plans that look individually reasonable at each dependency edge but never terminate when traced as a whole
- The failure surfacing only at execution time rather than during plan generation, since cycle detection wasn't run before execution began

## Root Cause
LLM-driven decomposition typically generates subtasks and their dependencies incrementally or dependency-by-dependency, evaluating "does subtask X need subtask Y's output" as a local, pairwise judgment rather than constructing and validating a full directed graph before finalizing the plan. This makes it easy to introduce a cycle without noticing: a natural-sounding chain like "finalize the report after review, but review needs a draft, and the draft needs the report's outline, which the finalization step was supposed to define" can loop back on itself across three or four hops, each individual edge locally sensible, while the full chain is circular. Without an explicit topological-sort or cycle-detection validation step run against the complete dependency graph before execution, this class of error isn't caught until the executor tries to schedule the subtasks and finds none are ready to start.

## Example
```
A software-release planning agent decomposes "ship version 2.4" into
subtasks with dependencies:

  Subtask A: "Write release notes" -- depends on: Subtask C (final
             changelog must be generated first)
  Subtask B: "Run final QA pass" -- depends on: Subtask A (QA needs
             release notes to verify user-facing claims)
  Subtask C: "Generate changelog" -- depends on: Subtask B (changelog
             should only be finalized after QA confirms which fixes
             actually shipped)

Each dependency, read individually, sounds reasonable: release notes
need the changelog, QA needs release notes to check claims, and the
changelog should reflect QA-confirmed fixes. But traced as a graph:
A -> C -> B -> A is a closed cycle. No subtask has zero unmet
dependencies, so the executor has no valid starting point. The
orchestrator either stalls waiting for a dependency that will never
clear, or throws a generic "unable to schedule" error with no indication
of where in the three-subtask chain the cycle actually is, and an
engineer has to manually trace the dependency graph to find it.
```

## Statistics
| Finding | Context |
|---------|---------|
| Dependency cycles are estimated to appear in a small but non-trivial share of LLM-generated multi-subtask decompositions, rising with the number of subtasks and the density of cross-references between them | Typical range observed in agent planning trace reviews |
| Plans with 4 or more interdependent subtasks show disproportionately higher cycle rates than simpler 2-3 subtask decompositions | Estimated from analysis of decomposition trace complexity |
| Adding a topological-sort validation pass before execution is reported to catch effectively all structural cycles before they reach the executor, converting a runtime stall into a plan-time rejection | Reported range across teams that added graph validation to their planning pipeline |

## Mitigations
1. **Topological sort validation before execution**: Run a standard cycle-detection algorithm (e.g. Kahn's algorithm) against the full dependency graph as a mandatory gate before any subtask begins execution, rejecting or flagging plans that don't reduce to a valid linear order.
2. **Explicit graph construction over incremental pairwise edges**: Have the planner emit the complete dependency graph as a single structured artifact and validate it as a whole, rather than deriving dependencies as isolated local judgments that are never checked against each other.
3. **Cycle-aware re-planning prompt**: When a cycle is detected, feed the specific cycle (the chain of subtasks and their circular dependency) back to the planner and ask it to specifically resolve that cycle, rather than regenerating the entire plan from scratch.
4. **Dependency direction heuristics**: Encode domain knowledge about typical valid dependency directions (e.g. "verification steps should depend on generation steps, never the reverse") as a check the planner or a validator applies before finalizing dependencies.
5. **Human-readable dependency graph review**: For complex plans, render the dependency graph visually or as an ordered list before execution and require a review step, since cycles are often much easier for a human to spot visually than for the planner to catch in isolated pairwise reasoning.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| dependency_cycle_detection_rate | Fraction of generated plans that fail topological-sort validation due to a cycle | Alert if > 2% |
| unschedulable_plan_rate | Fraction of plans where the executor finds zero subtasks with satisfied dependencies at start | Alert if > 0% (should be caught before execution) |
| cycle_length_distribution | Number of subtasks involved in detected cycles | Track for planner improvement; no fixed threshold |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Plan rejected for dependency cycle | Topological-sort validation detects a cycle before execution begins | Medium | Route back to planner with the specific cycle identified for resolution |
| Executor unable to schedule any subtask | A plan reaches execution with zero subtasks having satisfied dependencies | High | Halt execution immediately, this indicates cycle validation was bypassed or failed |

## Related Patterns
- [Subgoal Ordering Error](./subgoal-ordering-error.md) - a related but distinct failure where the dependency graph is acyclic but the chosen execution order still violates logical prerequisites
- [Plan Parallelization Error](./plan-parallelization-error.md) - both concern incorrect reasoning about the dependency graph, one missing a hidden dependency and the other introducing a nonexistent circular one
- [Plan Backtracking Failure](./plan-backtracking-failure.md) - a plan discovered to be cyclic partway through partial execution requires clean backtracking of whatever subtasks did execute before the cycle was found
