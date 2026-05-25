# Batch Optimization Failures

## Issue: Processing Items Individually When Batching Would Be More Efficient

**Frequency**: Common

**Symptoms**
- Sequential API calls for items that could be batched
- High per-request overhead on small items
- Rate limiting triggered by too many small requests
- Latency accumulation from sequential processing
- Token overhead from repeated context per item

**Root Cause**
Agents process items one-by-one even when the LLM could handle multiple items in a single call. Each API call has overhead (network latency, rate limit consumption, context setup), and many tasks like classification, extraction, or simple Q&A can process multiple items together. Failure to batch results in 5-20x higher costs and latency.

**Example**
```
Scenario: Document classification agent

Task: Classify 100 documents into categories

Sequential approach:
  For each document:
    - API call with document + classification prompt
    - Latency: ~500ms per call
    - Context tokens: 200 (prompt) + 500 (doc) = 700
    - Total: 100 calls × 700 tokens = 70,000 tokens
    - Total latency: 50 seconds
    - Cost: $0.35

Batched approach (10 docs per call):
  For each batch of 10:
    - API call with 10 documents + classification prompt
    - Latency: ~800ms per call
    - Context tokens: 200 (prompt) + 5,000 (10 docs) = 5,200
    - Total: 10 calls × 5,200 tokens = 52,000 tokens
    - Total latency: 8 seconds
    - Cost: $0.26

Savings:
  - Tokens: 26% reduction
  - Latency: 84% reduction
  - API calls: 90% reduction
  - Rate limit headroom: 10x more

Optimal batching:
  - Batch size limited by context window
  - Diminishing returns above certain size
  - Must handle partial failures
```

**Key Statistics**
From Batch Processing Research (2026):
- Batching reduces API costs by 20-40%
- Latency reduction: 60-90% for batch-eligible tasks
- 65% of classification/extraction tasks are batch-eligible
- Optimal batch size: 5-20 items (task-dependent)
- Per-request overhead: 50-200ms average

**Batch-Eligible Tasks**
| Task Type | Batch Potential | Typical Savings |
|-----------|-----------------|-----------------|
| Classification | High | 30-40% |
| Entity extraction | High | 25-35% |
| Translation | Medium | 20-30% |
| Summarization | Low | 10-20% |
| Complex reasoning | Low | 5-15% |

**Contributing Factors**
- Loop-based processing patterns
- No batch API support awareness
- Concerns about partial failures
- Difficulty handling mixed-size items
- Lack of batching infrastructure
- Context window size concerns

**Mitigation Strategies**
1. **Batch API usage**: Use native batch endpoints when available
2. **Dynamic batching**: Group items up to context limit
3. **Async batch processing**: Process batches in parallel
4. **Partial failure handling**: Retry only failed items
5. **Size-aware batching**: Group similar-sized items together
6. **Queue-based batching**: Accumulate items before processing

**Detection**
- Monitor requests per logical task
- Track items processed per API call
- Compare latency: sequential vs. potential batched
- Measure rate limit utilization
- Audit processing patterns for batch opportunities

## References

- [OpenAI: Batch API](https://platform.openai.com/docs/guides/batch) - Native batch processing
- [Anthropic: Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/message-batches) - Claude batch API
- [AWS: Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Cost optimization
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Efficiency patterns
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Cost runaway
