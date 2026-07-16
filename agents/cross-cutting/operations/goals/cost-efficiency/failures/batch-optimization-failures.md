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

---

## Test Scenario & Reproduction

### Scenario Setup
- Batch-eligible workload (e.g., document classification) implemented as a loop issuing one API call per item
- No dynamic batcher, request-coalescing queue, or native batch endpoint integration
- No items_per_api_call monitoring

### Trigger Mechanism
1. Run a batch-eligible task (classification/extraction) over a representative item set through the existing sequential loop
2. Measure total API calls, tokens, latency, and cost
3. Re-run the same workload through a batched implementation (e.g., 10 items per call) and compare

**Example Reproduction Steps:**
```
1. Take 100 documents needing classification
2. Run the existing sequential per-document loop; record API call count, total tokens, wall-clock latency, and cost
3. Implement/run a batched version (10 docs per call) over the same 100 documents
4. Compare: items_per_api_call, total tokens, latency, cost between the two runs
5. Measure: % reduction achieved by batching vs. the sequential baseline
```

### Expected Failure State
- Sequential implementation shows items_per_api_call near 1, with 100 API calls for 100 documents
- Token cost and latency are measurably higher than the batched alternative (per the 26% token / 84% latency reduction shown in the example)
- No batching alerting flagged the batch-eligible workload running sequentially

---

## Mitigation Strategies

### Prevention
1. **Batch API adoption for batch-eligible task types**: For classification, extraction, and translation workloads — the task types with High batch potential per the table above — route through native batch endpoints (Anthropic Message Batches, OpenAI Batch API) instead of the loop-based sequential pattern described in the root cause. This directly targets the 90% API-call reduction and 20-40% cost reduction the research shows. Trade-off: batch APIs introduce async completion delays (often minutes to hours), so they're unsuitable for latency-sensitive interactive flows.
2. **Dynamic batch sizing within context limits**: Since the example shows a 10-doc batch dropping tokens from 700/doc to 520/doc, build a batcher that accumulates items up to a size/token ceiling (the 5-20 item optimal range noted in the file) before dispatching, rather than a fixed batch size that either underfills (losing overhead savings) or overfills (hitting diminishing returns or context limits). Trade-off: dynamic sizing adds queuing latency for the first items in a batch while it waits to fill.
3. **Size-aware grouping to avoid mixed-batch waste**: Group items of similar token size together before batching, since the "difficulty handling mixed-size items" contributing factor causes either padding waste or oversized batches that risk truncation. Trade-off: sorting/grouping is an extra pre-processing pass that adds latency for small workloads.

### Detection & Response
1. **Items-per-API-call ratio**: Monitor the ratio of items processed to API calls issued for classification/extraction/translation tasks; a ratio near 1:1 signals the sequential anti-pattern from the root cause is active and batching opportunity is being missed.
2. **Batch-eligibility audit on task logs**: Periodically scan logged task traces for loop-based sequential API call patterns against the Batch-Eligible Tasks table (Classification, Entity extraction = High potential) and flag high-potential task types still running sequentially.
3. **Partial-failure retry rate**: Track what fraction of a batch fails and requires individual retry — if this is high, the fear-of-partial-failure contributing factor may be causing engineers to avoid batching entirely, which should be addressed with better retry-only-failed-items logic rather than abandoning batching.

### Architecture Patterns
1. **Native batch endpoint integration**: Use Anthropic's Message Batches API or OpenAI's Batch API directly for offline/async classification and extraction jobs; deployment consideration is that these are priced and rate-limited separately from synchronous calls, so cost dashboards must track them as a distinct line item.
2. **Request coalescing queue**: A queue-based accumulator that buffers incoming items (with a max wait time, e.g. 500ms-2s) and flushes a batch API call when either the size or time threshold is hit, addressing the "accumulate items before processing" mitigation; deployment consideration is tuning the wait threshold so it doesn't add unacceptable latency to interactive paths.
3. **Partial-failure isolation and retry**: Process each batch response item independently so a single failed item triggers only a targeted single-item retry rather than re-running or discarding the whole batch, directly addressing the partial-failure contributing factor called out as a reason teams avoid batching.

### Metrics
1. **items_per_api_call**: Target > 8 for batch-eligible task types (classification, extraction); Alert if < 3 for tasks flagged as batch-eligible.
2. **batch_eligible_task_batch_rate**: Target > 80% of classification/extraction/translation task volume routed through batch endpoints; Alert if < 50%.
3. **cost_per_1k_items_processed**: Target < $2.60 (per the batched example: 10 calls × 5,200 tokens for 100 docs); Alert if > $3.50 (approaching the sequential-processing cost of $3.50/100 docs).
4. **partial_batch_failure_rate**: Target < 2% of items per batch requiring individual retry; Alert if > 10%.

### Alerts
1. **Sequential-Processing-On-Batch-Eligible-Workload** (P2): Condition - a task type classified as High/Medium batch potential (per the eligibility table) shows items_per_api_call < 2 for a sustained 24h window. Action: page the owning team to review whether batch API integration was skipped, and check for regressions in the dynamic batcher.
2. **Batch-Cost-Regression** (P3): Condition - cost_per_1k_items_processed exceeds the sequential-processing baseline ($3.50/100 docs equivalent) for a batch-eligible workload. Action: investigate whether batch size has collapsed to near-1 (defeating the purpose) or whether per-request overhead has increased.

## References

- [OpenAI: Batch API](https://platform.openai.com/docs/guides/batch) - Native batch processing
- [Anthropic: Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/message-batches) - Claude batch API
- [AWS: Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Cost optimization
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Efficiency patterns
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Cost runaway
