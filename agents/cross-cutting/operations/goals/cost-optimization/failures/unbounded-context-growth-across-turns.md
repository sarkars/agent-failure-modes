# Unbounded Context Growth Across Turns

## Issue: Conversation History and Tool Output Are Appended Every Turn With No Truncation or Summarization, So Total Session Cost Grows Superlinearly as the Conversation Lengthens

**Frequency**: Common

**Symptoms**
- Per-turn token cost climbs steadily over the course of a long-running session, even when each individual turn's new content is small
- No single turn looks bloated in isolation (unlike [Context Stuffing](../../cost-efficiency/failures/context-stuffing.md)'s static over-inclusion), but cumulative session cost is dominated by re-sending the full growing history on every call
- Sessions that run long (many-turn agent loops, long customer support conversations, extended coding sessions) show total cost scaling roughly with the square of turn count rather than linearly
- No truncation, summarization, or history-pruning policy exists; every turn's full transcript and tool outputs are carried forward verbatim

**Root Cause**
Because each model call in a multi-turn session is typically stateless from the API's perspective, the full conversation history (including prior tool call results) must be resent on every turn for the model to have continuity. Absent a pruning, summarization, or windowing policy, this history is carried forward and grows monotonically: turn N resends turns 1 through N-1 in full. Since cost is billed per input token on every call, and the input token count itself grows with turn count, total session cost grows roughly with the square of the number of turns, not linearly with it — a dynamic that's invisible if cost is only monitored per-turn rather than cumulatively across a session.

**Example**
```
Long-running coding-agent session, 40 turns, each turn adding ~800
tokens of new content (user message + tool output + response) to the
running context, with no truncation or summarization.

Turn 1:  800 tokens sent
Turn 2:  1,600 tokens sent (turn 1's 800 + turn 2's new 800)
Turn 10: 8,000 tokens sent
Turn 20: 16,000 tokens sent
Turn 40: 32,000 tokens sent

Sum across all 40 turns (arithmetic series): ~656,000 tokens total
Equivalent cost if history were capped/summarized at a rolling 8,000-
token window instead: ~40 x 8,000 = 320,000 tokens (linear growth)

Waste: roughly 336,000 tokens (51%) attributable purely to unbounded
history growth rather than any single turn being individually bloated.
Per-turn cost at turn 40 is 40x per-turn cost at turn 1, for a session
where no individual turn's new content changed in size.
```

**Contributing Factors**
- No history-pruning, summarization, or sliding-window policy configured for long-running sessions
- Cost dashboards track per-turn or per-call spend, which never looks anomalous in isolation, rather than cumulative per-session spend, which is where the superlinear growth becomes visible
- Fear of losing early-turn context (an instruction or fact stated early that becomes relevant later) discourages truncation without a safer alternative like summarization
- Tool outputs (which can be large) are appended to history in full on every turn rather than being summarized or referenced after their immediate use

---

## Test Scenario & Reproduction

### Scenario Setup
- A long-running agent session (many turns) with no truncation, summarization, or context-window-management policy
- Each turn adds new user/tool/response content to a running, ever-resent history
- No per-session (only per-turn) cost monitoring in place

### Trigger Mechanism
1. Run a session to 40+ turns, with each turn adding a roughly constant amount of new content
2. Log total input tokens sent on every turn
3. Compute cumulative session cost and compare its growth curve against a linear-growth baseline (what a capped/summarized history would have cost)

**Example Reproduction Steps:**
```
1. Configure a session with no history truncation/summarization
2. Run 40 turns, each contributing ~800 tokens of new content
3. Log input tokens sent on turns 1, 2, 10, 20, 30, 40
4. Confirm input tokens at turn N scale roughly as N x 800 (i.e., the
   full history is being resent, not just new content)
5. Sum total tokens sent across all 40 turns
6. Compute the equivalent total under a rolling window/summarization
   policy capped at, e.g., 8,000 tokens of history
7. Compute the percentage waste attributable to unbounded growth
```

### Expected Failure State
- Input tokens per turn grow roughly linearly with turn number (turn 40 costs ~40x what turn 1 cost), confirming the full history is resent every turn
- Cumulative session cost across all turns is dominated by history resending rather than genuinely new content, with waste exceeding 40-50% relative to a capped/summarized alternative
- No per-session cumulative cost alert exists, only per-turn monitoring, so the pattern is invisible until someone manually sums a long session's cost
- No summarization or pruning step activates as turn count increases past any threshold

---

## Mitigation Strategies

### Prevention
1. **Rolling window with periodic summarization**: Cap the verbatim history carried forward at a fixed recent-turn window (e.g., the last 10 turns) and periodically compress everything older into a running summary, so per-turn input size stabilizes instead of growing indefinitely, directly targeting the linear-per-turn-cost-growth seen in the example. Trade-off: summarization can lose fine-grained detail from early turns, and the summarization step itself costs tokens, though far less than carrying full history forward.
2. **Tool-output lifecycle management**: Since tool outputs (which can be large) are named as a contributing factor, summarize or drop a tool's full output from history once its immediate purpose in that turn is served, retaining only a compact reference (e.g., "fetched order #4021, status: shipped") rather than the full raw payload for the rest of the session. Trade-off: if a later turn genuinely needs the full raw tool output again, it must be re-fetched rather than being available in history.
3. **Explicit-instruction pinning instead of full-history retention**: Since fear of losing an early instruction is named as a reason teams avoid truncation, extract and pin specifically-flagged persistent instructions/facts (not the entire early transcript) into a small, fixed-size "pinned context" block that survives pruning, addressing the actual retention need without requiring the full history to be kept. Trade-off: requires a mechanism (manual or automatic) to identify which early content is actually worth pinning versus safely prunable.

### Detection & Response
1. **Cumulative per-session cost tracking, not just per-turn**: Monitor total tokens spent across an entire session (summed across all turns), and its growth curve versus turn count; a curve trending quadratic rather than linear is the direct signature of this failure, and it will not show up in per-turn-only dashboards.
2. **Per-turn-cost-versus-turn-number regression**: Fit per-turn input token size against turn number for active long-running sessions; a strongly positive slope (input size growing with turn count rather than staying flat) confirms history is being resent in full rather than windowed.
3. **Session-length-cost-outlier detection**: Flag sessions whose total cost is disproportionately concentrated in their later turns relative to their earlier ones, since this specifically indicates the compounding effect of unbounded growth rather than a session that was simply expensive throughout.

### Architecture Patterns
1. **Sliding-window context manager**: A dedicated context-management layer sits between the raw conversation store and the model call, applying a rolling window plus summarization policy before every call, so no individual call site in the agent's code has to remember to truncate — it's enforced centrally. Deployment consideration: the window size and summarization trigger point need tuning per use case; too aggressive a window risks losing context genuinely needed for coherence.
2. **Trajectory/history reduction as a first-class step**: Treat history compaction as an explicit pipeline stage (not an afterthought), periodically (e.g., every N turns) invoking a dedicated compression pass over the accumulated trajectory rather than relying purely on a fixed sliding window, adapting the retained detail to what later turns actually reference. Deployment consideration: adds a periodic extra model call for compression, which must be cheap relative to the savings from capping ongoing per-turn growth.
3. **Reference-based tool-output storage**: Store full tool outputs in an external, addressable store (not inline in the conversation history) and keep only a short reference/ID plus summary in the history itself, letting the agent re-fetch the full payload on demand if a later turn genuinely needs it, rather than always carrying every prior tool output forward in every call. Deployment consideration: requires the agent to recognize when it needs to re-fetch versus relying on the inline summary, and a fetch-by-reference tool to be available.

### Metrics
1. **session_cost_growth_curve_exponent**: Target ≈ 1.0 (linear) across turn count; Alert if > 1.5 (trending toward quadratic, matching the unbounded-growth failure mode).
2. **input_tokens_per_turn_at_turn_40_vs_turn_1_ratio**: Target < 3x (indicating windowing/summarization is capping growth); Alert if > 20x (matching the example's ~40x).
3. **pct_sessions_exceeding_context_window_management_threshold**: Target 0% of sessions past a defined turn-count threshold run without an active windowing/summarization policy; Alert if > 5%.
4. **tool_output_retention_size_in_history**: Target < 10% of history tokens are raw, unsummarized tool output payloads more than 2 turns old; Alert if > 40%.

### Alerts
1. **Quadratic-Cost-Growth-Detected** (P2): Condition - session_cost_growth_curve_exponent exceeds 1.5 for an active long-running session. Action: apply an emergency history-summarization pass and confirm a windowing policy is active going forward for that session type.
2. **No-Windowing-Policy-On-Long-Session** (P2): Condition - a session exceeds the turn-count threshold with pct_sessions_exceeding_context_window_management_threshold showing no active policy. Action: enable the rolling-window/summarization context manager for that session type and audit for others missing the same configuration.

## References

- [Reducing Cost of LLM Agents with Trajectory Reduction](https://arxiv.org/pdf/2509.23586) - compressing accumulated agent trajectories/history to control the superlinear cost growth of long-running sessions
- [LLM Token Optimization: Cut Costs & Latency in 2026](https://redis.io/blog/llm-token-optimization-speed-up-apps/) - unmanaged message histories named as a primary driver of agentic token cost beyond simple prompt wording
- [Related Pattern: Context Stuffing](../../cost-efficiency/failures/context-stuffing.md) - the static, single-turn over-inclusion failure; this pattern is the distinct turn-over-turn accumulation failure, not addressed by relevance filtering alone
