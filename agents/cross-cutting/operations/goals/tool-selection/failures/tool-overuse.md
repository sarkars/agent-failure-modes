# Tool Overuse

## Issue: Agent calls tools unnecessarily, increasing cost and latency.

**Frequency**: Occasional

**Symptoms**
- High tool-call count without improved answer quality.
- Exact or near-duplicate tool calls (same tool, same/overlapping arguments) issued multiple times within a single task.
- Tool-call count for a task runs well above the historical p50/p90 baseline for that task type with no corresponding gain in answer quality.
- Agent re-issues a search or lookup it already performed earlier in the session after losing track of context.
- Cost-per-resolved-task rises for a task category without any capability or quality improvement to justify it.

**Root Cause**
Without a per-task budget on tool calls, nothing forces the agent to stop exploring and synthesize an answer once it already has enough evidence, so it keeps calling as long as another call seems marginally plausible. That tendency is amplified by a planning loop that re-evaluates its approach after every result without first checking whether the information it's about to fetch is already sitting in context, and because there's no deduplication cache, an identical query re-issued after a plan revision goes straight back to the live tool instead of being served from what was already retrieved. No gate requires the agent to justify why the next call will actually change the answer, and because nobody tracks the relationship between call count and answer quality, this drift toward excessive tool use isn't caught until the cost anomaly itself becomes visible.

**Example**
```
User: "What are the key differences between X and Y?"
Agent calls: web_search("X vs Y comparison")
Agent calls: web_search("differences between X and Y")  # near-duplicate
Agent calls: web_search("X vs Y comparison")  # exact duplicate
...continues for 15+ calls before producing a final answer that is
no more accurate than a 3-call baseline would have produced.
```

**Contributing Factors**
- No per-task tool-call budget exists, so nothing forces the agent to synthesize a final answer once it has sufficient evidence.
- No redundant-call deduplication cache, so identical queries re-issued after a plan revision or context reset are dispatched again instead of served from cache.
- The planner re-evaluates its approach after each result without checking whether the needed information is already in context.
- No marginal-value gate requires justification for why a next tool call is expected to change the answer, so low-value calls go through unchecked.
- No tool-call-count vs. answer-quality correlation tracking exists, so overuse regressions after a prompt or model change go unnoticed until cost anomalies appear.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Duplicate-Call Detection Probe | Task where the agent issues the same web_search query twice within one session | Second identical call is served from the dedup cache, not re-dispatched to the tool | Tool is invoked twice with identical normalized arguments, both hitting the live backend |
| Budget Enforcement Probe | Task type with a p90 historical budget of 3 calls, agent attempts a 4th | Orchestrator returns "budget exceeded, synthesize final answer" and blocks the 4th call | Agent's 4th+ call is dispatched without a budget-exceeded signal |
| Marginal-Value Gate Probe | Agent proposes a tool call that would only re-fetch data already present in context | Gate rejects the call for lacking a plausible marginal-value justification | Call is dispatched despite no new information being sought |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_avg_tool_calls_per_task | Within 1.2x of the task type's historical p50 baseline on the eval suite | Run the fixed eval task set, compare average tool-call count per task against stored baseline |
| eval_redundant_call_rate | < 5% of calls in the eval suite are exact/near-duplicates | Run eval tasks known to be resolvable with a small fixed number of distinct calls, count duplicate calls issued |
| eval_quality_per_call_efficiency | Positive or flat quality score as call count increases | Score eval task answers with the standard quality rubric, correlate against tool-call count across the suite |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a research agent with access to a web-search tool, with no per-task tool-call budget, no redundant-call deduplication cache, and no marginal-value gate before each call
- The agent's planning logic re-evaluates its approach after each search result, sometimes re-issuing a search it already made when it loses track of what it retrieved
- No tool-call-count vs. answer-quality correlation tracking is in place

### Trigger Mechanism
1. A user asks a research question requiring a handful of targeted searches
2. The agent issues an initial search, then re-issues near-identical searches multiple times as it revises its plan, without checking whether it already has the needed information in context
3. The agent continues calling the search tool well beyond what's needed to answer confidently, with no budget or dedup cache stopping it
4. The final answer quality is no better than what a handful of searches would have produced, but the task consumed significantly more cost and latency

### Example Reproduction Steps
```
1. User: "What are the key differences between X and Y?"
2. Agent calls: web_search("X vs Y comparison")
3. Agent calls: web_search("differences between X and Y") (near-
   duplicate of call 2, same intent)
4. Agent calls: web_search("X vs Y comparison") again (exact
   duplicate of call 2)
5. ...continues for 15+ total calls before producing a final answer
6. Compare avg_tool_calls_per_task against the historical p50 for
   this task type -> current task's call count is 5x+ the baseline
7. Compare answer quality/eval score against tasks resolved with the
   baseline call count -> no measurable quality improvement
```

### Expected Failure State
The agent makes 15+ tool calls to answer a question that historically resolves well within 3, including exact-duplicate searches, with no improvement in answer quality to justify the extra cost and latency. A correctly defended system either serves the duplicate second and third calls from a redundant-call deduplication cache, or has the orchestrator enforce a per-task budget that forces the agent to synthesize a final answer once the historical p90 call count is reached.

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
| avg_tool_calls_per_task | > 2x p50 |
| redundant_tool_call_rate | > 15% |
| cost_per_resolved_task | > 25% above rolling 7-day baseline |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Task Budget Repeatedly Exceeded | > 10% of tasks in a category hit the hard tool-call budget cap in a day | Warning |
| Redundant Call Spike | redundant_tool_call_rate exceeds threshold for a sustained period | Warning |
| Cost Anomaly | cost_per_resolved_task spikes > 2x baseline for a task category | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
