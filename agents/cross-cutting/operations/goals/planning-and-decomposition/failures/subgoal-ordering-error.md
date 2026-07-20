# Subgoal Ordering Error

## Issue
A planner decomposes a task into subgoals whose dependency graph is acyclic and individually valid, but sequences those subgoals in the wrong relative order because it reasoned about each subgoal's readiness or priority in isolation rather than against a complete precedence model. Unlike a circular dependency, there is a valid execution order available — the planner simply didn't pick it, instead ordering subgoals by something like generation order, apparent urgency, or estimated ease, and only implicitly (and incorrectly) assuming that order also respects real-world preconditions between subgoals that were never captured as an explicit dependency edge.

**Frequency**: Common

**Symptoms**
- A subgoal executes successfully in isolation but fails or produces a wrong result because a precondition established by a later subgoal in the plan hadn't happened yet
- The same set of subgoals, resequenced by a human or a different planner run, completes the task correctly — indicating the subgoals themselves were right but their order wasn't
- Execution logs show a subgoal referencing a resource, value, or state that a different subgoal (appearing later in the plan) was responsible for producing
- The plan passes structural/cycle validation (no circular dependency exists) but still fails at execution because of an implicit ordering constraint the planner never encoded as an edge
- Subgoal order correlates with generation order or a shallow heuristic (alphabetical, shortest-first, most-confident-first) rather than with any actual precedence analysis

## Root Cause
LLM-driven decomposition commonly generates subgoals and only loosely infers their relative order, often defaulting to the order in which the subgoals were generated or to a heuristic like tackling the easiest or most clearly-specified subgoal first — rather than building an explicit precedence model of which subgoals establish preconditions that others require. This differs from a dependency cycle: the graph the planner reasons about has no contradiction, because the planner never represented the relevant precedence relationship as an edge at all. The missing edge is a soft or implicit real-world constraint (e.g., "the discount code must be applied before the total is calculated," where nothing in either subgoal's description explicitly states this) that a human would recognize from domain knowledge but that the planner's local, pairwise reasoning about "does subgoal X reference subgoal Y's output" fails to surface, because the constraint isn't expressed as a data dependency, only as a real-world sequencing requirement.

## Example
```
An expense-reporting agent decomposes "submit my March expenses"
into subgoals: (1) apply the pending per-diem adjustment, (2)
calculate the total reimbursement amount, (3) submit the report for
approval. No explicit dependency edge connects (1) and (2) in the
planner's dependency graph, since (2)'s description ("sum all
line-item amounts") doesn't reference (1) by name.

The planner orders subgoals roughly by the order line items appeared
in the source data, executing (2) calculate total before (1) apply
per-diem adjustment, because nothing in its representation flagged
that the adjustment needed to land first.

The report is submitted with a total calculated before the per-diem
adjustment was applied, understating the reimbursement by the
adjustment amount. The submission subtask (3) succeeds without error,
since it has no way to know the total it's submitting is based on a
stale calculation - the plan was acyclic, individually valid at each
step, and simply executed in the wrong order.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of multi-subgoal plans that fail at execution despite passing structural (cycle) validation trace back to an unencoded precedence constraint rather than a missing capability or tool failure | Estimated from postmortems of decomposition-driven agent task failures |
| Resequencing a failed plan's subgoals into a different, still-acyclic order frequently resolves the failure without any change to the subgoals themselves | Typical finding when manually debugging subgoal-ordering incidents |
| Plans generated with an explicit precondition/precedence-elicitation step show substantially fewer ordering-related failures than plans where order is inferred implicitly from generation sequence | Typical improvement range reported after adding explicit precedence modeling to decomposition prompts |

## Mitigations
1. **Explicit precondition elicitation during decomposition**: When generating subgoals, separately prompt for "what must already be true before this subgoal can correctly run" rather than inferring order from generation sequence or apparent urgency, surfacing implicit real-world preconditions as explicit edges.
2. **Domain-aware ordering heuristics over generation-order defaults**: Where domain knowledge specifies canonical sequencing rules (adjustments before totals, authentication before data access), encode those rules as constraints the planner must apply rather than leaving the ordering to default heuristics like ease or confidence.
3. **Validate order against declared side effects, not just declared inputs**: Extend dependency analysis to consider what state each subgoal changes (not only what it reads), since ordering errors often stem from a later subgoal depending on an earlier one's side effect rather than its formal output.
4. **Dry-run / simulate before committing to an order**: Where feasible, simulate the planned order against a model of preconditions and effects before execution, catching cases where a subgoal's assumed starting state doesn't match the actual state left by the subgoal preceding it in the chosen order.
5. **Post-hoc reordering suggestion on failure**: When a subgoal fails due to an unmet precondition, check whether reordering the remaining plan (rather than only retrying the failed step in place) resolves the issue, since ordering errors are often fixable by resequencing without regenerating the subgoals themselves.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| precondition_violation_rate | Rate at which a subgoal fails or produces incorrect output due to a precondition that a later subgoal in the same plan was responsible for establishing | Alert if > 1% of multi-subgoal plans |
| reorder_resolves_failure_rate | Share of failed plans that succeed when the same subgoals are resequenced without modification | High values indicate the decomposition is sound but ordering logic is systematically weak |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Precondition violation detected | A subgoal's execution references a resource/value in a state inconsistent with what a later subgoal was meant to establish | High | Halt plan execution, resequence, re-validate before resuming |
| Order sensitive to non-semantic factor | Analysis shows subgoal order correlating with generation order or a shallow heuristic rather than a declared precedence model | Medium | Add explicit precondition elicitation to the decomposition step |

## Related Patterns
- [Plan Dependency Cycle](./plan-dependency-cycle.md) - a related but distinct failure where the dependency graph is genuinely unexecutable (a true cycle), rather than acyclic-but-wrongly-ordered
- [Plan Parallelization Error](./plan-parallelization-error.md) - a related planning-time misclassification, where subgoals are wrongly deemed independent enough to run in parallel rather than wrongly ordered when run sequentially
- [Sequencing Errors](../../tool-reliability/failures/sequencing-errors.md) - a related but narrower failure at the individual tool-call level rather than the higher-level subgoal-decomposition level
- [Tool Invocation Ordering Dependency](../../tool-selection-sequencing/failures/tool-invocation-ordering-dependency.md) - a related failure where the missing precedence signal lives in undocumented tool relationships rather than in unencoded subgoal preconditions
