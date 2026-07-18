# Non-Reproducible Execution

## Issue: Cannot Replay Agent Execution to Reproduce or Debug Issues

**Frequency**: Common

**Symptoms**
- Bug disappears when trying to reproduce
- Same input produces different outputs
- Cannot recreate production issue in test
- "Works on my machine" for agents
- Debugging requires guessing at state

**Root Cause**
Agent execution depends on many factors beyond the immediate input: model state, retrieved context, tool responses, timing, random seeds, and environmental variables. Without capturing all these factors, the same nominal input can produce completely different behavior, making bugs impossible to reproduce and fixes impossible to verify.

**Example**
```
Production bug report:
  "Agent recommended selling all customer's stocks"
  
Reproduction attempt:
  Input: Same customer query
  Model: Same version
  Result: Agent recommends balanced portfolio
  
  Input: Same query + same timestamp
  Result: Still recommends balanced approach
  
  Input: Same query + same market data snapshot
  Result: Recommends minor rebalancing
  
What was different in production?
  - Retrieved news articles (now updated)
  - Market data feed values (no longer available)
  - Model temperature randomness (different seed)
  - Previous conversation context (not captured)
  - Tool response latencies (affected reasoning)
  
Result: 
  - Cannot reproduce the bug
  - Cannot verify any fix
  - Cannot prove it won't happen again
  - Customer trust damaged
```

**Key Statistics**
From Debugging Research (2026):
- LLM outputs inherently non-deterministic (temperature > 0)
- RAG retrieval changes with index updates
- Tool responses change over time
- Most agent bugs cannot be reproduced
- "Heisenbug" rate much higher for agents than traditional software

**Non-Reproducibility Sources**
| Source | Variability | Capturable? |
|--------|-------------|-------------|
| Model randomness | Per-token | Yes (seed) |
| RAG retrieval | Per-query | Yes (snapshot) |
| Tool responses | Per-call | Yes (record) |
| Time-based logic | Per-second | Yes (mock) |
| External APIs | Per-call | Yes (record) |
| Conversation history | Per-session | Yes (log) |

**Contributing Factors**
- Non-determinism seen as feature, not bug
- Replay infrastructure expensive to build
- External dependencies hard to mock
- State captured incompletely
- Test environments don't match production

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a financial-advisory agent whose recommendations depend on retrieved news articles, a live market-data feed, model sampling temperature/seed, and prior conversation context, none of which are recorded together as a single execution bundle
- No snapshot-and-freeze mechanism preserves the exact tool/API responses returned in production; replay attempts re-fetch "current" values from live services
- A customer reports the agent recommended selling all their stocks, an unusually aggressive recommendation

### Trigger Mechanism
1. Engineers attempt to reproduce the bug using the same customer query and same model version, but get a "balanced portfolio" recommendation instead
2. They add the same timestamp, still get a balanced-approach result
3. They add the same market-data snapshot, and get a "minor rebalancing" result, closer but still not the reported "sell everything" outcome
4. They realize the retrieved news articles have since been updated, the model's random seed differed, prior conversation context wasn't captured, and tool response latencies (which affected reasoning) are also unrecorded — all varying simultaneously in the original production run

### Example Reproduction Steps
```
1. Production bug report: "Agent recommended selling all customer's
   stocks"
2. Reproduction attempt 1: same query, same model version ->
   "balanced portfolio" (different result)
3. Reproduction attempt 2: + same timestamp -> "balanced approach"
   (still different)
4. Reproduction attempt 3: + same market data snapshot -> "minor
   rebalancing" (still different)
5. Check for recorded: news articles retrieved (not captured, since
   updated), model seed (not captured), conversation history (not
   captured), tool response latencies (not captured)
6. Conclude: reproduction_success_rate for this bug = 0%; fix cannot
   be verified
```

### Expected Failure State
Despite three escalating reproduction attempts each fixing one variable, engineers cannot recreate the "sell everything" recommendation because several non-deterministic inputs (seed, news retrieval, conversation history, tool latencies) all differed simultaneously and none were recorded, leaving the team unable to confirm any fix actually addresses the root cause. A correctly instrumented system records the full execution bundle — seed, retrieved content snapshot, tool responses, and conversation state — at production time, enabling deterministic replay that reproduces the exact "sell everything" recommendation on demand.

## Mitigation Strategies

### Prevention
1. **Full execution recording of every non-deterministic input**: Capture the random seed, retrieved news articles, market data snapshot, tool response latencies, and prior conversation context together at the time of production execution — not just the nominal query — since the example's reproduction attempts each varied only one factor (timestamp, then market snapshot) while missing that news articles, seed, and conversation history all differed simultaneously. Trade-off: capturing every non-deterministic input at full fidelity is expensive to store and can itself introduce compliance concerns (e.g., logging full retrieved content or conversation history containing PII).
2. **Snapshot-and-freeze external state at execution time**: Record the exact tool/API responses (market data feed values, news retrieval results) as they were returned in production, rather than allowing replay to re-fetch "current" values from live services that have since updated — the example explicitly found market data "no longer available" and news articles "now updated" as reproduction blockers. Trade-off: requires storage and versioning infrastructure for every external response, and stale snapshots can themselves mislead debugging if not clearly marked as historical.
3. **Version-pinning across model, prompts, tools, and config as a single reproducibility unit**: Treat model version, prompt template version, tool version, and configuration as one atomic bundle recorded per execution, so "same model version" alone (as attempted in the example) isn't mistaken for full reproducibility when prompts or tool versions also matter. Trade-off: requires disciplined versioning and immutable storage of every component in the bundle, which is significant infrastructure investment.

### Detection & Response
1. **Reproduction-success-rate tracking**: Explicitly measure what fraction of reported bugs can actually be reproduced with recorded execution data, quantifying the "most agent bugs cannot be reproduced" baseline and giving a concrete target to improve against as recording infrastructure is built out.
2. **Environment-parity metrics between production and test/replay**: Track how closely test/replay environments match production in the dimensions that matter (data freshness, model version, tool response behavior), since the example's escalating reproduction attempts (same query → same timestamp → same market snapshot) each closed one parity gap but still missed several others.
3. **Fix-verification-failure-rate tracking**: Track how often a proposed fix cannot be verified because the original triggering conditions can't be reconstructed — the example's stated consequence ("cannot verify any fix, cannot prove it won't happen again") is directly measurable as this rate, and a high rate signals recording infrastructure gaps rather than fix-quality issues.

### Architecture Patterns
1. **Deterministic replay mode built on recorded execution bundles**: Build a replay system that, given a recorded execution bundle (seed, retrieved content, tool responses, conversation state, timestamps), can force fully deterministic re-execution — turning "cannot reproduce the bug" into a solved, tooling-supported capability rather than a per-incident manual reconstruction effort. Deployment consideration: requires the recording infrastructure above to exist first, and every non-deterministic call site in the agent pipeline must support being fed a recorded value instead of a live one.
2. **Mocked-time and mocked-external-dependency test harness**: Support replaying an execution at its original timestamp with all external dependencies (market data, news retrieval, tool APIs) served from recorded snapshots rather than live calls, directly enabling the "same query + same market data snapshot" reproduction attempt in the example to actually succeed rather than partially failing. Deployment consideration: every external dependency needs a mockable interface, which requires refactoring tightly-coupled integrations.
3. **Full-session conversation-state capture as part of execution recording**: Log complete prior conversation context (not just the current query) as part of what's captured for later replay, since the example identifies "previous conversation context (not captured)" as one of the specific factors that differed between production and reproduction attempts. Deployment consideration: full conversation capture increases storage volume and requires privacy-conscious handling of potentially sensitive conversation content.

### Metrics
1. **reproduction_success_rate**: % of reported bugs reproducible using recorded execution data; target > 80%; alert if < 40%.
2. **environment_parity_score**: Composite measure of how closely replay conditions match original production conditions (data freshness, model/prompt/tool version match); target > 90%; alert if < 60%.
3. **fix_verification_failure_rate**: % of proposed fixes that cannot be verified due to inability to reconstruct triggering conditions; target < 10%; alert if > 30%.
4. **non_deterministic_input_capture_rate**: % of known non-deterministic input sources (seed, retrieval, tool responses, timing, conversation state) actually captured per execution; target 100%; alert if < 80%.

### Alerts
1. **Reproduction Success Rate Critical** (P2): Condition — reproduction_success_rate falls below 40% over a rolling quarter. Action: prioritize building out execution-recording infrastructure for the highest-value input sources (external tool responses and retrieval snapshots first, per the example's specific gaps).
2. **Fix Verification Blocked** (P1): Condition — a fix for a customer-impacting bug (e.g., an incorrect financial recommendation) cannot be verified due to non-reproducibility. Action: treat the underlying bug as unresolved regardless of the proposed fix, and prioritize recording infrastructure for that specific execution path before declaring the issue closed.
3. **Non-Deterministic Input Capture Gap** (P2): Condition — non_deterministic_input_capture_rate drops below 80% for a given input source (e.g., tool response snapshots). Action: add recording instrumentation for that specific source before the next production incident in that path.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Debugging challenges
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Replay requirements
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Debug difficulties
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Production debugging
