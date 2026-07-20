# Tool Selection Greedy Suboptimal

## Issue
At each step, the agent picks whichever tool looks most immediately useful for the current sub-goal — the one whose description best matches the current phrasing — without considering how that choice constrains or costs more in later steps. This locally-good, globally-suboptimal selection pattern repeatedly leads the agent down a path that technically makes progress at each step but ends up more expensive, slower, or less accurate overall than a different tool choice earlier on would have been.

**Frequency**: Common

**Symptoms**
- The agent completes tasks successfully but consistently uses more tool calls, more tokens, or more wall-clock time than a hand-constructed optimal plan would need
- A tool chosen early in a task turns out to lack a capability needed later, forcing extra corrective calls or a full restart with a different tool
- The agent picks the tool with the most appealing-sounding name/description for the immediate step rather than one that would set up a cheaper or more reliable path for subsequent steps
- Comparing successful task traces shows a wide variance in cost/step-count for logically identical tasks, correlating with which tool was picked first
- The agent never seems to "plan ahead" — each tool choice is explicable by the immediately preceding context alone, not by anticipated future steps

## Root Cause
LLM-driven tool selection is typically implemented as a per-step decision: given the current state and the immediate sub-goal, pick the best next tool call. This mirrors a greedy algorithm, which is computationally cheap and often adequate, but greedy algorithms are only optimal for problems with specific structure (e.g. matroid-like independence), and general multi-step task planning doesn't have that structure — an early choice can foreclose better later options. Full lookahead (evaluating how each candidate tool choice affects the cost of every subsequent step) is expensive to compute and, for LLM-based planners, expensive in context and reasoning tokens, so most agent architectures don't attempt it and instead accept greedy, myopic selection as the practical default.

## Example
```
A data-analysis agent is asked to "find the average order value for
customers in the Northeast region over the last quarter."

Available tools: query_orders_api (returns paginated JSON, 100 rows/
page, no aggregation support), and run_sql_query (executes arbitrary
SQL against the same underlying data warehouse, supports aggregation
server-side).

The agent's first-step tool selection picks query_orders_api because
its description ("retrieve order records") most directly matches the
literal phrase "find... order value" in the task, and it's the first
tool alphabetically listed with "order" in its name.

Having started down that path, the agent now must: call
query_orders_api repeatedly across 34 pages to retrieve all ~3,400
matching orders (34 tool calls), manually sum and count the amounts
across all returned pages in its own reasoning, and handle a rate
limit that kicks in after page 20, requiring a backoff-and-retry
loop.

The equivalent task via run_sql_query would have been a single call:
SELECT AVG(order_value) FROM orders WHERE region='Northeast' AND
quarter=current_quarter. The agent completes the task correctly via
the paginated path, but uses 34x the tool calls, takes 6 minutes
instead of 8 seconds, and hits the rate limit once along the way -
none of which was visible as a problem at the moment of the first,
locally-reasonable tool choice.
```

## Statistics
| Finding | Context |
|---------|---------|
| Greedy tool selection is estimated to produce task completions using 2-10x more tool calls than an optimal plan for the same task, particularly for aggregation/multi-record tasks | Typical range observed in production agent telemetry |
| Adding even one step of lookahead (evaluate top-2 candidate tools against the expected remaining plan) recovers a substantial share of the gap versus full lookahead | Estimated from workflows instrumented with plan-cost comparison |
| Tool descriptions emphasizing capability scope (e.g. "supports aggregation, filtering, and joins" vs. "retrieves records") measurably shift selection away from the greedy default | Reported range across teams that revised tool descriptions for this purpose |

## Mitigations
1. **Capability-aware tool descriptions**: Write tool descriptions that surface not just what a tool does for the immediate ask but its broader capability scope (aggregation, filtering, bulk operations), giving the planner more signal to avoid a narrow, literal-match selection.
2. **Plan-level cost estimation before execution**: Have the planner sketch the full expected sequence of steps and a rough cost estimate before committing to the first tool call, and prefer plans with lower total estimated cost over the locally-best first step.
3. **Bounded lookahead**: Where full lookahead is too expensive, evaluate at least the top few candidate tools against a one- or two-step-ahead projection of remaining work, catching the most common single-choice-forecloses-everything cases without needing exhaustive search.
4. **Tool selection retrospectives**: Periodically sample completed task traces and compare actual tool-call cost against a hand-constructed optimal plan, using the gap to identify systematic greedy-selection patterns and fix them via better tool descriptions or explicit routing rules.
5. **Explicit routing for known task shapes**: For recurring task categories where the optimal tool choice is well understood (aggregation queries should use SQL, not paginated REST), add explicit routing logic or few-shot examples that override the default greedy selection.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| tool_call_count_vs_optimal_ratio | Ratio of actual tool calls used to an estimated optimal call count for the task category | Alert if > 3x for a recurring task shape |
| task_completion_cost_variance | Variance in cost/latency for logically identical tasks | Alert if high variance correlates with initial tool choice |
| rate_limit_hit_rate | Rate of hitting downstream rate limits, often a symptom of an inefficient high-call-count path | Alert if > baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Task cost far exceeds optimal for its category | tool_call_count_vs_optimal_ratio exceeds threshold for a task category with a known better path | Medium | Review the tool descriptions or add explicit routing for that task category |
| Rate limit hit during a high-call-count trace | A task trace shows both elevated call count and a rate-limit error | Low | Flag for retrospective review, no immediate user-facing action needed if task still completed |

## Related Patterns
- [Tool Composition Complexity Explosion](./tool-composition-complexity-explosion.md) - a large tool space makes greedy, myopic selection more likely since full evaluation becomes infeasible
- [Tool Selection Non-Determinism](./tool-selection-non-determinism.md) - greedy selection based on surface-level phrasing match is also more sensitive to run-to-run prompt variance
- [Tool Invocation Ordering Dependency](./tool-invocation-ordering-dependency.md) - a greedy first choice can also violate an ordering dependency that a lookahead-aware plan would have respected
