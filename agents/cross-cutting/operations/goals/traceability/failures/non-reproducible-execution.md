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

**Mitigation Strategies**
1. **Execution recording**: Capture all inputs, responses, and random seeds
2. **Deterministic replay mode**: Force reproducible execution for debugging
3. **Snapshot external state**: Record tool/API responses for replay
4. **Version everything**: Model, prompts, tools, and configs
5. **Time mocking**: Support replaying at original timestamps
6. **Conversation capture**: Full session state logging

**Detection**
- Reproduction success rate tracking
- Environment parity metrics
- "Cannot reproduce" bug rate
- Debug session duration trends
- Fix verification failure rate

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Debugging challenges
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Replay requirements
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Debug difficulties
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Production debugging
