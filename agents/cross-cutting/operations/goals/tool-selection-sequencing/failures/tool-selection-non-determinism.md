# Tool Selection Non-Determinism

## Issue
The same task, given to the same agent with the same available tools, results in a different tool being selected across separate runs — one run calls a REST API tool, another run calls a functionally-overlapping SQL tool, a third calls a third-party search integration — with no change in the input that would justify the difference. Because downstream behavior, cost, and reliability differ by tool, this non-determinism makes the agent's behavior unpredictable and hard to test, debug, or give consistent guarantees about.

**Frequency**: Common

**Symptoms**
- Identical task inputs produce different tool-call traces across repeated runs
- Automated tests that assert "task X should call tool Y" are flaky, passing and failing across otherwise-identical CI runs
- Support/debugging is harder because reproducing a reported issue requires the same tool to have been chosen, which isn't guaranteed by simply re-running the same input
- Cost and latency for logically identical requests vary run to run, since different tools have different pricing and performance
- A/B-style behavior differences appear in production with no corresponding change in code or user input, traceable to LLM sampling variance in the tool-selection step

## Root Cause
LLM-based tool selection is a sampling process, not a deterministic lookup — even at low temperature, next-token sampling can land on a different tool name when multiple tools have similar or overlapping relevance scores for the given context, and many agent frameworks don't pin temperature to zero (or even at temperature zero, floating-point non-determinism in batched inference across different hardware/load conditions can still cause variance). When two or more tools are near-equally good matches for a task's phrasing — overlapping descriptions, redundant capability — the selection step is effectively picking among near-ties, and near-ties are exactly the case most sensitive to sampling noise, so those are the situations where non-determinism shows up most visibly.

## Example
```
An agent has both send_notification (a lightweight push-notification
tool) and send_email (a full email tool) available, both described
as suitable for "notifying the user of an update," because the
notification tool was added later without updating email's
description to disambiguate the two use cases.

Given the identical task "let the user know their report is ready,"
across 50 separate runs with the same input:
  - 31 runs select send_email
  - 17 runs select send_notification
  - 2 runs select both, sending a duplicate notification

Because send_email has a ~2 second delivery latency and costs $0.002/
send, while send_notification delivers in under 200ms and costs
$0.0001/send, the task's cost and user-perceived latency vary by
roughly 20x between runs with no visible cause. A downstream analytics
dashboard tracking "average notification cost" shows wide, unexplained
variance that takes an engineer two days to trace back to tool-
selection non-determinism rather than a data or pricing issue.
```

## Statistics
| Finding | Context |
|---------|---------|
| Near-tied tool relevance (two or more tools scoring within a small margin for the same task phrasing) accounts for the large majority of observed selection non-determinism | Typical range observed in production agent telemetry |
| Pinning temperature to 0 for the tool-selection step reduces but does not eliminate variance, given remaining infrastructure-level non-determinism | Estimated from teams that tuned sampling parameters for this purpose |
| Disambiguating overlapping tool descriptions (adding "use X for A, use Y for B" guidance) reduces selection variance for near-tied tool pairs by an estimated 50-80% | Reported range across teams that revised tool descriptions to resolve overlap |

## Mitigations
1. **Disambiguate overlapping tool descriptions**: Explicitly state when to prefer each tool in cases of near-identical applicability (e.g. "use send_notification for time-sensitive, low-content updates; use send_email for anything requiring formatting or an audit trail"), removing the ambiguity that produces near-ties.
2. **Deterministic routing for well-defined task categories**: For task shapes where the correct tool choice is knowable in advance, bypass LLM-based selection entirely with explicit rule-based routing, reserving LLM judgment for genuinely ambiguous cases.
3. **Low or zero temperature on the selection step**: Pin sampling temperature as low as the framework allows specifically for the tool-selection decision, even if other parts of the agent's reasoning use higher temperature, to minimize (though not fully eliminate) run-to-run variance.
4. **Tool consolidation to remove true redundancy**: Where two tools genuinely overlap in capability with no meaningful distinction, merge them into one tool or clearly deprecate one, since no amount of prompt tuning fully resolves selection variance between truly redundant options.
5. **Selection-variance monitoring**: Track, for recurring task categories, the distribution of which tool gets selected across runs, and treat a wide or shifting distribution as a signal to disambiguate rather than as expected/acceptable noise.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| tool_selection_entropy_by_task_category | Measure of how spread out tool selection is across repeated instances of the same task category | Alert if entropy exceeds expected baseline for a category |
| cost_variance_same_task_category | Variance in per-task cost for logically identical task categories | Alert if variance exceeds a defined multiple of the mean |
| duplicate_action_from_multi_select_rate | Rate at which the agent selects and executes more than one overlapping tool for a single sub-goal | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High selection entropy for a task category | tool_selection_entropy_by_task_category exceeds threshold, indicating unpredictable tool choice | Medium | Review overlapping tool descriptions for that category, consider deterministic routing |
| Duplicate action from ambiguous selection | The agent calls two overlapping tools for what should be a single action | High | Notify workflow owner, add explicit mutual-exclusivity guidance or a selection gate |

## Related Patterns
- [Tool Selection Greedy Suboptimal](./tool-selection-greedy-suboptimal.md) - near-tied, ambiguous tool choices are also where greedy selection is most likely to pick a locally-plausible but globally-worse option
- [Tool Composition Complexity Explosion](./tool-composition-complexity-explosion.md) - a larger, more overlapping toolkit increases both the complexity cost and the rate of near-tied, non-deterministic selections
- [Tool Output Format Mismatch](./tool-output-format-mismatch.md) - non-deterministic tool choice means downstream steps must handle a wider, less predictable range of output formats
