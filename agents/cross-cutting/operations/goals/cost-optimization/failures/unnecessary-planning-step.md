# Unnecessary Planning Step

## Issue: Agent Runs a Full Planning/Decomposition Call for Tasks Simple Enough to Execute Directly

**Frequency**: Very Common

**Symptoms**
- A dedicated "plan" or "think step-by-step" LLM call precedes every task, including single-tool-call lookups
- Plan output for simple tasks is a one-item list restating the user's request ("Step 1: call the weather tool")
- Planning-phase token spend is comparable to or larger than the execution phase for trivial tasks
- No task-complexity gate decides whether a planning call is warranted before issuing one

**Root Cause**
Plan-then-execute architectures are adopted uniformly across an agent's task distribution because they improve reliability on complex, multi-step work. But the same architecture is applied unconditionally to every request, including ones with an obvious single action, because there is no cheap upfront check for "does this need a plan at all." Each unnecessary planning call is a full extra model round trip billed at whatever model tier handles planning, even when the eventual plan is trivial.

**Example**
```
User: "What's the current price of AAPL stock?"

Agent architecture: mandatory plan-then-execute for all requests

Planning call (Call 1, ~450 tokens):
"Step 1: Identify that the user wants a stock price.
 Step 2: Call the get_stock_price tool with ticker AAPL.
 Step 3: Return the result to the user."

Execution call (Call 2, ~180 tokens):
get_stock_price("AAPL") -> $214.32
"AAPL is currently trading at $214.32."

Result: 2 model calls and ~630 tokens for a task that a
direct-execution path would have completed in 1 call and ~180 tokens.
Planning overhead: 71% of total token spend for zero decision value.
```

**Contributing Factors**
- No lightweight complexity classifier gating whether the planning phase runs at all
- Planning prompt template is static and always invoked, regardless of tool count or task shape
- Reliability gains from planning on hard tasks are used to justify running it on all tasks without measuring the cost on easy ones
- No per-task-type tracking of planning-call token spend versus execution-call token spend

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent configured with a mandatory plan-then-execute loop: every incoming request first goes through a dedicated planning call, then an execution call
- No complexity classifier or single-tool-call shortcut path exists
- Task set includes both single-tool-call lookups (stock price, weather, order status) and genuinely multi-step tasks (multi-source research, multi-tool workflows)

### Trigger Mechanism
1. Submit a single-tool-call-resolvable query ("What's the current price of AAPL stock?") to the agent
2. Let the mandatory planning call execute and produce a plan
3. Measure planning-call tokens versus execution-call tokens, and compare against a direct-execution baseline run without the planning step

**Example Reproduction Steps:**
```
1. Configure the agent with the mandatory plan-then-execute loop enabled
2. Submit 50 single-tool-call-resolvable queries (stock price, weather, order lookup, simple unit conversion)
3. For each, log planning-call tokens and execution-call tokens separately
4. Re-run the same 50 queries through a direct-execution path with the planning call skipped
5. Compute planning_overhead_ratio = planning_tokens / (planning_tokens + execution_tokens) for the mandatory-planning run
6. Compare total cost and task success rate between the two conditions
```

### Expected Failure State
- planning_overhead_ratio exceeds 50% for single-tool-call tasks, i.e., more tokens are spent deciding what to do than actually doing it
- Task success rate is statistically indistinguishable between the mandatory-planning and direct-execution conditions for the single-tool-call task set
- No complexity classifier or shortcut exists to route obviously simple tasks around the planning call
- The same planning-call template runs unchanged regardless of whether the task has one obvious tool or many candidate tools

---

## Mitigation Strategies

### Prevention
1. **Lightweight complexity gate before planning**: Run a cheap, fast classification (a small model, a heuristic on tool-count/intent, or a rule like "single named tool with all required arguments already present in the request") to decide whether the task needs a planning call at all; route obviously single-step tasks directly to execution. Trade-off: the classifier itself must run on every request, so it needs to be materially cheaper than the planning call it's meant to skip, or the savings evaporate.
2. **Plan-then-execute reserved for tasks crossing a step-count or tool-count threshold**: Since plan-then-execute earns its cost on genuinely multi-step work, apply it only when the task appears to require 2+ tool calls, cross-referencing multiple data sources, or has ambiguous ordering — not uniformly. Trade-off: misclassifying a task as "simple" when it actually needed multi-step planning risks a wrong or incomplete direct execution that then requires a costlier corrective round trip.
3. **Merge planning into the execution call for simple cases**: For tasks likely to need at most one tool call, fold the "what should I do" reasoning into the same call that issues the tool call (single combined call) rather than a separate upstream planning call, eliminating the extra round trip entirely for the common case. Trade-off: a combined call can't benefit from a cheaper model tier being used for planning versus a more capable tier for execution.

### Detection & Response
1. **Planning-overhead-ratio monitoring per task type**: Track planning_tokens / total_tokens per task type; task types where this ratio is consistently high (as in the AAPL example's 71%) despite low actual step count are candidates for bypassing planning.
2. **Plan-output triviality detection**: Flag plans that reduce to a single step restating the user's request almost verbatim — these are a direct signal that the planning call added no decision-making value and could have been skipped.
3. **A/B cost-and-success comparison**: Periodically route a sample of traffic through a direct-execution path (no planning call) alongside the standard mandatory-planning path, and compare cost and task success rate; a null difference in success rate for a task type justifies permanently bypassing planning for it.

### Architecture Patterns
1. **Two-tier request router**: A fast, cheap classification step sits in front of the agent loop and routes each request to either "direct execution" (single call) or "plan-then-execute" (two or more calls), so the planning phase becomes conditional infrastructure rather than a hardcoded step. Deployment consideration: the router needs its own accuracy monitoring, since a misrouted complex task sent to direct execution risks a lower-quality result that then needs costly correction.
2. **Cached plan-shape reuse for common intents**: For task types that recur frequently with the same shape (e.g., "look up X"), reuse a known-good plan skeleton instead of re-generating one from scratch, turning the planning cost into a one-time cost amortized across many occurrences. Deployment consideration: overlaps with plan-template reuse; requires a mechanism to detect when a new task doesn't match any cached shape and needs fresh planning.
3. **Single-call function-calling for shallow tasks**: For tasks that map directly onto one tool with arguments extractable from the request text, use direct function-calling (model emits a tool call in the same turn it receives the request) rather than a plan-then-invoke pipeline, structurally removing the planning round trip for this task class. Deployment consideration: requires tool schemas expressive enough that the model doesn't need a separate reasoning pass to select among them.

### Metrics
1. **planning_overhead_ratio_by_task_type**: Target < 20% for single-tool-call task types; Alert if > 50% (matching the AAPL example's failure case).
2. **plan_triviality_rate**: Target < 10% of plans reduce to a single step restating the request; Alert if > 30%.
3. **direct_vs_planned_success_rate_delta**: Target within ±2 percentage points for task types being considered for a direct-execution bypass; Alert if planning meaningfully outperforms direct execution (signal that bypass would be premature).
4. **avg_model_calls_per_single_tool_task**: Target ≈ 1; Alert if consistently ≥ 2.

### Alerts
1. **High-Overhead-Simple-Task** (P3): Condition - planning_overhead_ratio_by_task_type exceeds 50% for a task type with historically ≤1 required tool call. Action: review whether that task type qualifies for the direct-execution bypass path.
2. **Trivial-Plan-Rate-Elevated** (P3): Condition - plan_triviality_rate rises above 30% over a rolling week. Action: audit the complexity gate/classifier for missing rules that should route these tasks around planning.

## References

- [Plan-then-execute cost trade-off framing](https://www.correlation-one.com/blog/how-to-manage-ai-token-costs-in-the-enterprise-the-2026-playbook) - Correlation One 2026 enterprise token-cost playbook, on when planning calls are and aren't worth their cost
- [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/abs/2506.14852) - motivates conditional/reused planning versus per-task fresh planning calls
- [Implementing Prompt Compression to Reduce Agentic Loop Costs](https://machinelearningmastery.com/implementing-prompt-compression-to-reduce-agentic-loop-costs/) - broader context on agentic loop cost drivers including planning overhead
