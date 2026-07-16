# Caching Failures

## Issue: Redundant LLM Calls for Identical or Similar Requests

**Frequency**: Common

**Symptoms**
- Same questions answered repeatedly with new API calls
- No semantic similarity matching for cached responses
- Cache keys too specific (miss on minor variations)
- Cache keys too broad (return wrong cached response)
- Stale cache served when fresh data needed

**Root Cause**
LLM calls are expensive, but organizations fail to implement effective caching. Either no cache exists, or the cache strategy is flawed—exact-match caching misses semantically identical queries, while overly aggressive caching returns stale or incorrect responses. The probabilistic nature of LLM outputs also complicates cache validation.

**Example**
```
Scenario: FAQ bot without semantic caching

Hour 1 queries (100 requests):
  "What's your return policy?" - API call #1
  "What is the return policy?" - API call #2 (no cache hit)
  "Return policy?" - API call #3 (no cache hit)
  "How do I return something?" - API call #4 (no cache hit)
  "What are your return rules?" - API call #5 (no cache hit)
  ... 95 more variations of same question

Result:
  All 100 queries → 100 API calls
  Cost: $0.50 (100 × $0.005)

With semantic caching:
  First query → API call, cached
  99 similar queries → Cache hit
  Cost: $0.005 + cache lookup
  
Waste: $0.495 (99% redundant)

At scale (1M queries/month):
  Without cache: $5,000
  With semantic cache: $500
  Annual savings: $54,000
```

**Key Statistics**
From Caching Research (2026):
- 30-60% of LLM queries are semantically similar to prior queries
- Semantic caching reduces API costs by 40-70%
- Exact-match caching captures only 5-15% of redundant queries
- Cache invalidation errors cause 8% of incorrect responses
- Average cache hit rate with proper implementation: 45-65%

**Caching Strategy Failures**
| Strategy | Problem | Result |
|----------|---------|--------|
| No cache | All queries hit API | Maximum cost |
| Exact match | Minor variations miss | Low hit rate |
| Over-broad | Wrong responses served | Quality issues |
| No TTL | Stale data returned | Incorrect answers |
| No invalidation | Outdated info persists | Trust erosion |

**Contributing Factors**
- No caching infrastructure for LLM calls
- Exact-match-only cache keys
- No semantic similarity matching
- Missing cache invalidation logic
- No TTL for time-sensitive data
- Fear of returning incorrect cached response

---

## Test Scenario & Reproduction

### Scenario Setup
- FAQ-style agent with no caching, or exact-match-only caching, in front of the LLM
- No semantic similarity matching or embedding-based cache lookup
- No cache-hit-rate monitoring against the expected 30-60% query-redundancy baseline

### Trigger Mechanism
1. Send a batch of semantically identical but textually varied queries (paraphrases of the same question)
2. Observe how many result in a fresh API call vs. a cache hit
3. Measure total cost/latency against what a semantic cache would have achieved

**Example Reproduction Steps:**
```
1. Send 5 paraphrased variants of the same question to the agent: "What's your return policy?", "What is the return policy?", "Return policy?", "How do I return something?", "What are your return rules?"
2. Log whether each triggers a fresh LLM API call or a cache hit
3. Repeat with 100 total queries drawn from a small set of paraphrased FAQ variants
4. Measure: cache_hit_rate achieved vs. the 45-65% "proper implementation" benchmark
5. Compare total cost against the semantic-cache cost estimate in the example
```

### Expected Failure State
- Every paraphrased variant triggers a separate API call (cache_hit_rate near 0%)
- No semantic similarity matching catches near-duplicate queries
- Measured cost is far above the semantic-cache benchmark for the same query volume

---

## Mitigation Strategies

### Prevention
1. **Embedding-based semantic cache lookup**: Since exact-match caching captures only 5-15% of redundant queries (per the FAQ bot example where "What's your return policy?" vs. "Return policy?" both miss), embed each incoming query and compare against cached query embeddings with a cosine-similarity threshold before hitting the LLM. Trade-off: embedding computation and vector search add latency (typically 10-50ms) to every request, even cache misses.
2. **Tiered TTLs by content volatility**: Because the failure table shows "No TTL" causes stale data and "No invalidation" causes trust erosion, classify content by how often it changes (e.g., static FAQ answers vs. time-sensitive order status) and assign TTLs accordingly rather than one global TTL. Trade-off: tiering adds a content-classification step that must be maintained as new query types are added.
3. **Confidence-gated cache writes**: Only cache a response when the model's confidence (or a validation pass) exceeds a threshold, addressing the "Over-broad" cache failure mode where wrong responses get served to slightly different queries. Trade-off: this reduces effective hit rate somewhat since more first-time queries won't be cached.

### Detection & Response
1. **Cache hit rate vs. expected redundancy**: Since 30-60% of queries are semantically similar to prior ones, a measured hit rate well below the 45-65% "proper implementation" benchmark signals the semantic matching threshold is miscalibrated or absent.
2. **Near-duplicate query clustering**: Periodically cluster logged queries (like the "What's your return policy?" / "Return policy?" / "How do I return something?" variants) that resulted in separate API calls; a large cluster size indicates missed semantic cache opportunity.
3. **Invalidation-triggered incorrect-response reports**: Track user-reported or QA-flagged incorrect answers and correlate against cache age; since cache invalidation errors cause 8% of incorrect responses, spikes here indicate the invalidation trigger logic isn't firing on source-data changes.

### Architecture Patterns
1. **GPTCache-style semantic cache layer**: Deploy a vector-store-backed cache (e.g., GPTCache, or a Redis vector index) sitting in front of the LLM call, returning cached responses above a similarity threshold; deployment consideration is choosing the similarity threshold carefully — too loose returns wrong answers (the "Over-broad" failure), too strict degrades to exact-match behavior.
2. **Cache warming for high-frequency intents**: Pre-populate the cache with known common queries (e.g., top FAQ variants) at deploy time so the first live occurrence of each variant is already a hit, addressing the "first query → API call" cold-start cost in the example. Deployment consideration: requires periodically refreshing the warm set as query distribution shifts.
3. **Event-driven invalidation hooks**: Wire cache invalidation to source-data change events (e.g., a policy-document update publishes an invalidation message) rather than relying purely on TTL expiry, directly addressing the "Missing cache invalidation logic" contributing factor. Deployment consideration: requires the source system to reliably emit change events, which may not exist for all data sources.

### Metrics
1. **cache_hit_rate**: Target 45-65% (per the "proper implementation" benchmark); Alert if < 30%.
2. **cost_per_1k_queries**: Target < $50 (per the semantic-cache example: 1M queries/month at $500 = $0.50/1k); Alert if > $200 (approaching the uncached $5,000/1M = $5/1k baseline).
3. **cache_staleness_incident_rate**: Target < 8% of incorrect responses attributable to stale cache (matching research baseline as ceiling, not target); Alert if > 8%.
4. **semantic_match_precision**: Target > 95% of served cache hits judged correct on spot-check/A-B validation; Alert if < 90%.

### Alerts
1. **Cache-Hit-Rate-Collapse** (P2): Condition - cache_hit_rate drops below 30% for a sustained 1-hour window on a previously well-cached query pattern (e.g., FAQ traffic). Action: check whether the embedding service or vector index is degraded/unreachable, causing silent fallback to always-miss behavior.
2. **Stale-Response-Spike** (P2): Condition - staleness-related incorrect-response reports exceed the 8% baseline in a rolling 24h window. Action: audit invalidation triggers for the affected content type and manually flush the relevant cache tier.
3. **Cost-Per-Query-Regression** (P3): Condition - cost_per_1k_queries rises above $200 despite stable traffic volume. Action: investigate whether cache TTLs were tightened excessively or a recent deploy bypassed the cache lookup path.

## References

- [GPTCache](https://github.com/zilliztech/GPTCache) - Semantic caching for LLMs
- [LangChain: Caching](https://python.langchain.com/docs/modules/model_io/llms/llm_caching) - LLM caching patterns
- [Redis: LLM Caching](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Caching strategies
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Cost optimization
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost reduction
