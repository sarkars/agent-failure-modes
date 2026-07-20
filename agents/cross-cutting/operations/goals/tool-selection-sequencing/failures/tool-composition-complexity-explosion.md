# Tool Composition Complexity Explosion

## Issue
As the number of available tools and the depth of a plan grow, the number of possible tool-call sequences the agent could construct grows combinatorially, and the planning process either times out, truncates its search, or falls back to a shallow heuristic that ignores most of the space. The agent isn't failing on any single tool call — it's failing to reason about which combination and ordering of many tools is correct, because the branching factor has outgrown what the planner can actually evaluate within its context or time budget.

**Frequency**: Occasional

**Symptoms**
- Planning latency grows sharply, not linearly, as more tools are added to the agent's available set
- The agent produces noticeably shallower or more repetitive plans once the tool count crosses some threshold
- Increasing the number of available tools degrades task success rate even when every individual tool works correctly in isolation
- The agent picks an obviously suboptimal tool sequence that a simpler subset of tools would have made easy to get right
- Truncated or timed-out planning runs correlate with tasks that have many valid tool combinations rather than tasks that are inherently hard

## Root Cause
An agent selecting a sequence of N tool calls from a toolkit of size K faces a search space that grows roughly as K^N (before considering that many valid orderings and combinations also exist for realistic tasks), and LLM-based planners approximate this search rather than solving it exactly — they reason token-by-token about "what tool next," effectively doing a greedy or beam-limited walk through a space too large to fully evaluate. As the toolkit grows (more integrations added over time, more fine-grained tool variants introduced), the planner's fixed context window and fixed reasoning budget don't scale with it, so the fraction of the combination space it can meaningfully consider shrinks, and it increasingly falls back on surface pattern-matching (which tool's description sounds most relevant) rather than genuine multi-step reasoning about the composition.

## Example
```
An agent starts with 6 tools (search, fetch_page, summarize, send_email,
create_calendar_event, save_note) and reliably composes 3-4 step plans
for tasks like "research X and email me a summary."

Over 8 months, the toolkit grows to 47 tools as more integrations are
added: 6 variants of search (web, internal-docs, code, image, video,
academic), 5 email-related tools (send, draft, reply, forward,
schedule-send), 8 calendar tools, a dozen data-transform tools, etc.

Given the same class of task - "research X and email me a summary" -
the agent now has to choose among 6 search variants, decide whether to
chain 2-3 of them, choose among 5 email tools, and consider whether a
draft-then-review step is warranted. The planning step's chain-of-
thought grows from ~200 tokens to ~2,400 tokens, latency roughly
quadruples, and in 1 run out of roughly 6 the agent selects
"schedule-send" instead of "send" for a task with no scheduling
component, because in the compressed reasoning it fell back to matching
on the word "send" among visually similar tool descriptions rather
than fully reasoning through which of the 5 email tools was correct.
```

## Statistics
| Finding | Context |
|---------|---------|
| Task success rate for agents with 40+ available tools is estimated to be 10-25% lower than the same tasks run against a curated 10-15 tool subset | Typical range observed in production agent deployments |
| Planning latency has been observed to grow super-linearly, often quadratically or worse, as tool-set size increases past a few dozen | Estimated from workflows instrumented with tool-count vs. latency tracking |
| Tool-set curation/scoping (presenting only task-relevant tools per request) reduces misselection rates by roughly 30-50% | Reported range across teams that added dynamic tool filtering |

## Mitigations
1. **Dynamic tool scoping per request**: Rather than exposing the full toolkit to every planning call, pre-filter to a task-relevant subset (via retrieval, categorization, or explicit routing) so the planner's effective branching factor stays manageable.
2. **Hierarchical tool organization**: Group related tools under higher-level categories the planner selects first (e.g. "email action" before "which email tool"), reducing a flat K-way choice into a shallower tree.
3. **Explicit decomposition before tool selection**: Require the agent to first produce a high-level step plan in natural language, then select tools per step, rather than jointly reasoning about steps and tool choice in one pass.
4. **Tool deduplication and consolidation**: Periodically audit the toolkit for near-duplicate or rarely-differentiated tools (multiple "send email" variants) and consolidate or deprecate the ones that add combinatorial cost without adding real capability.
5. **Complexity-aware timeouts and fallback plans**: Detect when a task's plausible tool-combination space exceeds a budget and fall back to a simpler, more constrained planning mode (or ask a clarifying question) rather than letting the planner silently truncate its search.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| planning_latency_p95 | 95th-percentile time spent in the tool-selection/planning step | Alert if trending upward with tool-set growth |
| available_tool_count | Number of tools exposed to the planner for a given request | Track alongside success-rate trend, no fixed threshold |
| task_success_rate_by_toolset_size | Success rate bucketed by how many tools were available for the request | Alert if success rate drops > 15% at higher bucket sizes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Planning latency spike correlated with toolset growth | planning_latency_p95 increases significantly following a toolset addition | Medium | Review recently added tools for redundancy, consider dynamic scoping |
| Success rate regression after tool addition | task_success_rate_by_toolset_size drops after a new tool is added to the shared toolkit | High | Roll back or scope the new tool, audit for overlapping tool descriptions |

## Related Patterns
- [Tool Selection Greedy Suboptimal](./tool-selection-greedy-suboptimal.md) - the shallow-heuristic fallback that complexity explosion tends to push planners toward
- [Tool Selection Non-Determinism](./tool-selection-non-determinism.md) - a large, ambiguous tool space also increases run-to-run variance in which tool gets picked
- [Tool Invocation Ordering Dependency](./tool-invocation-ordering-dependency.md) - ordering constraints compound the combinatorial cost that complexity explosion describes
