# Token Explosion

## Issue: Exponential Token Usage Growth

**Frequency**: Common

**Symptoms**
- Token usage grows exponentially across conversation turns
- Context window fills rapidly
- Costs far exceed estimates
- Agent becomes slower as context grows

**Root Cause**
Several patterns cause token counts to explode:
- Accumulating full conversation history without summarization
- Including verbose tool outputs in context
- Repeatedly passing large documents
- Multi-agent handoffs duplicating context
- Chain-of-thought reasoning generating excessive tokens

**Example**
```
Turn 1: 1,000 tokens
Turn 2: 2,500 tokens (includes turn 1)
Turn 3: 5,000 tokens (includes turns 1-2)
Turn 4: 10,000 tokens
Turn 5: Context window exceeded

Result: Quadratic growth instead of linear
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Multi-turn conversation where each turn's prompt includes the full verbatim history of all prior turns, with no summarization or sliding window
- No reference-by-ID mechanism for large documents/tool outputs reused across turns
- Fixed context window with no per-turn token budget enforcement

### Trigger Mechanism
1. Start a conversation and record the token count at Turn 1 (baseline)
2. At each subsequent turn, append the new turn's content to the full unmodified history of all prior turns rather than summarizing or windowing
3. Continue the conversation and track token count growth turn over turn
4. Observe what happens once the accumulated token count approaches the context window limit

**Example Reproduction Steps:**
```
1. Configure the agent to include full, unmodified conversation history in every prompt (no summarization, no sliding window)
2. Run a multi-turn conversation and log prompt token count at each turn: Turn 1, Turn 2, Turn 3, Turn 4, Turn 5
3. Verify Turn 2's prompt includes Turn 1 in full, Turn 3's includes Turns 1-2 in full, and so on
4. Compute the turn-over-turn growth ratio (expect roughly 2x: 1,000 -> 2,500 -> 5,000 -> 10,000)
5. Continue to Turn 5 and check whether the prompt exceeds the model's context window
6. Re-run the same conversation with periodic summarization enabled and compare the growth curve (expect roughly linear instead of quadratic)
```

### Expected Failure State
- Token count per turn grows at a roughly doubling (quadratic) rate rather than linearly: approximately 1,000 -> 2,500 -> 5,000 -> 10,000 tokens across turns 1-4
- By Turn 5, the accumulated context exceeds the model's context window and the request fails outright
- No summarization or truncation step intervenes before the hard context-window failure occurs
- Growth rate diverges sharply from a linear-growth baseline well before the actual failure turn, but no alert fires on the trend itself

---

## Mitigation Strategies

### Prevention
1. **Periodic context summarization instead of full accumulation**: Since the example shows tokens doubling each turn (1,000 → 2,500 → 5,000 → 10,000) because each turn "includes" all prior turns verbatim, compress conversation history into a running summary at fixed intervals (e.g., every 3-5 turns) so growth becomes roughly linear instead of the quadratic pattern described. Trade-off: summarization can lose fine-grained details from earlier turns that later prove relevant, and the summarization call itself costs tokens.
2. **Reference-by-ID for repeated documents**: Since "repeatedly passing large documents" and "multi-agent handoffs duplicating context" are named root causes, store large documents/tool outputs once and pass a reference ID or pointer in subsequent turns instead of re-embedding the full content each time. Trade-off: requires a retrieval mechanism the agent (or handoff target) can use to dereference the ID when it actually needs the content, adding an extra round-trip when content is genuinely needed again.
3. **Sliding-window with hard per-turn token budget**: Cap included context to only the most recent N turns rather than the full history, paired with an explicit token budget per turn that forces truncation/summarization before the budget is exceeded, directly preventing the "Turn 5: Context window exceeded" failure in the example. Trade-off: dropping older turns risks losing context that becomes relevant again later in long-running conversations.

### Detection & Response
1. **Per-turn token growth rate**: Track tokens-per-turn across a conversation and compute the growth rate turn-over-turn; the example's pattern (roughly doubling each turn) is a clear quadratic-growth signature that should trigger alerting well before the context window is actually exceeded.
2. **Context-window headroom tracking**: Monitor remaining context window capacity as a percentage at each turn; a conversation trending toward 0% headroom within a small number of remaining turns (as in "Turn 5: Context window exceeded") should trigger automatic summarization before the hard failure occurs.
3. **Actual-vs-expected token usage comparison**: Compare observed token usage per turn against a linear-growth expectation baseline; sustained divergence (actual growing faster than linear) indicates one of the named root causes (unsummarized history, verbose tool outputs, duplicated handoff context, or excessive chain-of-thought) is active.

### Architecture Patterns
1. **Rolling summarization pipeline**: A background or inline process that periodically collapses older turns into a compact summary, replacing raw turn history in the context sent to the model, directly implementing the "Context summarization" and "Sliding window" strategies as enforced infrastructure. Deployment consideration: needs tuning of summarization frequency/aggressiveness against the risk of losing detail needed for task correctness.
2. **Document/tool-output store with reference passing**: A content-addressable store (keyed by document ID or content hash) that agents and multi-agent handoffs reference instead of re-serializing full documents into every prompt, addressing the "multi-agent handoffs duplicating context" root cause specifically. Deployment consideration: requires all agents in a handoff chain to support dereferencing IDs, so partial rollout (some agents still inlining content) doesn't fully solve the problem.
3. **Tool-output truncation/summarization layer**: Insert a post-processing step on verbose tool outputs (e.g., large API responses, file contents) that trims or summarizes before the output enters context, rather than passing raw output through unmodified. Deployment consideration: truncation logic must preserve the specific fields the agent actually needs, which requires some awareness of what the output will be used for.

### Metrics
1. **token_growth_rate_per_turn**: Target linear growth (< 1.2x turn-over-turn ratio); Alert if growth ratio exceeds 1.8x for 2+ consecutive turns (approaching the ~2x-per-turn pattern in the example).
2. **context_window_headroom_pct**: Target > 30% headroom remaining at any given turn; Alert if < 10% headroom (imminent risk of the "context window exceeded" failure).
3. **avg_tokens_per_conversation_at_turn_10**: Target < 15,000 tokens (reflecting effective summarization); Alert if > 40,000 tokens (indicating unmitigated accumulation).
4. **duplicated_document_reinclusion_count**: Target 0 instances of the same full document being re-embedded in context within one task/handoff chain; Alert if any detected.

### Alerts
1. **Context-Window-Imminent-Exceeded** (P1): Condition - context_window_headroom_pct drops below 10% mid-conversation. Action: force immediate summarization/truncation of oldest turns before the next model call, and log the conversation for review of why summarization didn't trigger earlier.
2. **Quadratic-Growth-Detected** (P2): Condition - token_growth_rate_per_turn exceeds 1.8x for 2+ consecutive turns. Action: check whether summarization or sliding-window logic is disabled/misconfigured for this conversation/agent path.
3. **Duplicated-Document-Reinclusion** (P3): Condition - the same document/tool-output is detected verbatim in context more than once within a task or handoff chain. Action: route that content through the reference-by-ID store instead of inline re-embedding.

## References

- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Analysis of token consumption patterns in agentic AI
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including token explosion
