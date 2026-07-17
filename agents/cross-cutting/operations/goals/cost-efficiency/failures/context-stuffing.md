# Context Stuffing

## Issue: Overloading Context with Irrelevant Information

**Frequency**: Common

**Symptoms**
- Large documents included when only snippets needed
- Entire conversation history passed every turn
- All available tools described regardless of relevance
- System prompts bloated with unused instructions

**Root Cause**
- "Just in case" inclusion of information
- No relevance filtering before context inclusion
- Static system prompts not adapted to task
- Fear of missing needed context

**Example**
```
Task: "What's the weather in NYC?"

Context included:
- 50-page user manual
- Full conversation history (100 turns)
- All 200 available tools
- Complete company knowledge base

Actual need: Weather API tool + location

Result: 100,000 tokens used, 500 needed
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent system with a static system prompt describing all 200 available tools regardless of task
- Context-assembly pipeline attaches the full conversation history and a complete company knowledge base/user manual by default, with no relevance filtering
- No intent classifier gating what gets included in the prompt before the model call

### Trigger Mechanism
1. Submit a simple, narrowly-scoped query ("What's the weather in NYC?") to the agent
2. Let the default context-assembly pipeline attach the full 50-page user manual, complete 100-turn conversation history, all 200 tool descriptions, and the full knowledge base
3. Measure total tokens sent to the model versus tokens the model actually needed/referenced to answer

**Example Reproduction Steps:**
```
1. Configure the agent's default context pipeline to include: full user manual (50 pages), full conversation history (100 turns), all 200 tool definitions, complete knowledge base
2. Send the query: "What's the weather in NYC?"
3. Capture the assembled prompt and count total tokens sent to the model
4. Identify which specific context elements the model actually cited/used in producing its answer (expected: only the weather tool description + location)
5. Compute the ratio of tokens included vs. tokens actually referenced
6. Repeat with a relevance-filtered context (only the weather tool + location) and compare token counts and latency
```

### Expected Failure State
- The unfiltered run sends roughly 100,000 tokens to the model for a query that needed roughly 500 tokens (weather tool + location)
- Context utilization ratio (referenced tokens / included tokens) is near 0%, far below any reasonable target
- Latency and cost for a trivial single-fact lookup match those of a complex, knowledge-base-spanning task
- No relevance-filtering step intervenes despite the task being classifiable as simple/single-intent

---

## Mitigation Strategies

### Prevention
1. **Relevance filtering before inclusion**: Since the root cause is "just in case" inclusion with no relevance filtering, run an intent/relevance classifier on the incoming task before assembling context, and only pull in the document sections, tools, or history relevant to that intent — e.g., a weather query should trigger only the weather tool description, not all 200 available tools. Trade-off: the classifier itself costs a small amount of latency/tokens, and misclassification risks under-including needed context.
2. **Dynamic tool loading by detected intent**: Rather than statically describing all 200 tools in every system prompt (as in the example), load only the subset of tool definitions relevant to the detected task type, addressing the "All available tools described regardless of relevance" symptom directly. Trade-off: requires an intent-to-toolset mapping that must be maintained as tools are added.
3. **Conversation pruning instead of full history replay**: Since "Full conversation history (100 turns)" was identified as a major contributor to the 100,000-vs-500-token waste, summarize or drop turns beyond a recent window rather than replaying the entire conversation on every turn. Trade-off: summarization can lose fine-grained detail from early turns that later becomes relevant.

### Detection & Response
1. **Context utilization ratio**: Measure tokens actually referenced/used by the model's response versus tokens included in the prompt; a low ratio (as in the 500-needed-of-100,000-included example) signals context stuffing is occurring and filtering logic needs tightening.
2. **Unused-section tracking**: Instrument which document chunks, tool descriptions, or history turns are cited or acted upon by the model versus which are silently ignored — sections that are never used across many tasks are candidates for removal from default context.
3. **Task-complexity-vs-context-size correlation**: Flag cases where simple tasks (like "What's the weather in NYC?") receive context sizes typical of complex tasks (50-page manuals, full knowledge bases); a mismatch indicates the relevance filter isn't scaling context to actual task need.

### Architecture Patterns
1. **Lazy/on-demand context fetching**: Instead of eagerly attaching the full knowledge base or manual, expose a retrieval tool the agent calls only when it determines specific information is needed, turning "just in case" inclusion into "just in time" fetching. Deployment consideration: adds a round-trip for cases where the context genuinely was needed, so cache frequently-fetched chunks.
2. **Tiered system prompt composition**: Build system prompts from a small core layer plus task-specific modules assembled at request time, rather than one large static prompt bloated with unused instructions (per the "Static system prompts not adapted to task" root cause). Deployment consideration: requires a prompt-assembly pipeline and versioning discipline across modules.
3. **Document chunking with relevance-ranked retrieval**: For large documents (the 50-page manual case), index and chunk content so only the top-ranked relevant sections are pulled into context rather than the entire document. Deployment consideration: chunking/embedding pipeline is extra infrastructure and needs periodic re-indexing as source documents change.

### Metrics
1. **context_utilization_rate**: Target > 60% of included tokens referenced in the model's reasoning/output; Alert if < 15% (matching the ~0.5% utilization seen in the 100,000-vs-500 example as the failure floor).
2. **avg_context_tokens_per_simple_task**: Target < 2,000 tokens for single-fact/lookup-style tasks; Alert if > 20,000.
3. **tool_definitions_loaded_per_request**: Target < 15 (task-relevant subset); Alert if > 100 (approaching the "all 200 tools" anti-pattern).
4. **conversation_history_tokens_p95**: Target < 8,000 tokens after pruning/summarization; Alert if unbounded growth exceeds 50,000.

### Alerts
1. **Context-Bloat-On-Simple-Task** (P2): Condition - a task classified as simple/single-intent triggers context assembly exceeding 20,000 tokens. Action: review the relevance filter and dynamic tool loader for the affected intent category; check for a missing intent classification rule.
2. **Utilization-Rate-Drop** (P3): Condition - context_utilization_rate falls below 15% sustained over a rolling window of tasks. Action: audit recently added "just in case" context sources (new tools, new document attachments) for removal from default inclusion.

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including context overloading
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Analysis of token waste from context stuffing
