# Tool Overuse

## Issue: Agent calls tools unnecessarily, increasing cost and latency.

**Frequency**: Occasional

**Symptoms**
- High tool-call count without improved answer quality.
- [Add more specific symptoms]

**Root Cause**
Agent calls tools unnecessarily, increasing cost and latency.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Per-Task Tool-Call Budget**: Assign each task type a maximum tool-call count and cost ceiling derived from historical p90 usage for successfully-resolved tasks of that type. The orchestrator warns the agent as it approaches the budget and hard-stops (forcing a final answer from available evidence) once exceeded, preventing unbounded exploratory looping.
2. **Redundant-Call Deduplication Cache**: Before dispatching a tool call, check a short-lived session cache keyed on tool name + normalized arguments; if an identical call was already made within the current task, return the cached result instead of re-invoking. This directly targets the common overuse pattern of re-querying the same read-only endpoint after context resets or plan revisions.
3. **Marginal-Value Gate Before Each Call**: Require the planner to produce a one-line justification for why the next tool call is expected to change the answer before dispatching it; calls without a plausible marginal-value justification (e.g., re-fetching data already in context) are rejected by the gate.

### Detection & Response
1. **Tool-Call-Count vs. Answer-Quality Correlation**: Track, per task, the number of tool calls made against a downstream quality signal (user satisfaction, eval score, resolution success). Sessions with call counts well above the norm but no quality improvement are flagged as overuse for review.
2. **Redundant-Call Rate Monitor**: Compute the fraction of tool calls in each session that are exact or near-duplicate of a prior call (same tool, same/overlapping args) using the dedup cache's hit-miss log; a rising rate indicates the agent is looping or has lost track of what it already retrieved.
3. **Cost-per-Resolved-Task Tracking**: Monitor the dollar/latency cost of tool usage per successfully resolved task by task category; sudden increases without a corresponding capability or quality improvement indicate overuse creeping in, often after a prompt or model change that made the agent more "cautious."

### Architecture Patterns
1. **Budget Enforcement Middleware**: A middleware layer in the tool-dispatch path tracks running call count/cost per task and enforces the configured budget, returning a "budget exceeded, synthesize final answer" signal to the agent rather than silently allowing further calls.
2. **Idempotent Read-Tool Cache**: For read-only/idempotent tools, front them with a caching layer scoped to the task session so repeated identical queries are served from cache, decoupling agent redundancy from actual backend load and cost.
3. **Planner-Critic Loop**: Introduce a lightweight critic step that scores the expected marginal information gain of the next proposed tool call against its cost before the planner commits to it, rejecting low-value calls before they reach the dispatch layer.

### Metrics
1. **avg_tool_calls_per_task**: Target: within 1.2x of historical p50 for the task type; Alert threshold: > 2x p50
2. **redundant_tool_call_rate**: Target: < 5% of calls are duplicates; Alert threshold: > 15%
3. **cost_per_resolved_task**: Target: within budgeted range per task category; Alert threshold: > 25% above rolling 7-day baseline
4. **tool_call_to_quality_correlation**: Target: positive or neutral correlation; Alert threshold: negative correlation (more calls, worse outcomes) sustained over a week

### Alerts
1. **Task Budget Repeatedly Exceeded** (P2 - Warning): Condition - > 10% of tasks in a category hit the hard tool-call budget cap in a day. Action: Review whether budget is mis-calibrated or agent is genuinely looping; investigate recent prompt changes.
2. **Redundant Call Spike** (P2 - Warning): Condition - redundant_tool_call_rate exceeds threshold for a sustained period. Action: Check dedup cache health, review context-loss patterns in long sessions.
3. **Cost Anomaly** (P1 - Critical): Condition - cost_per_resolved_task spikes > 2x baseline for a task category. Action: Immediate investigation, consider temporary budget tightening while root cause is identified.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
