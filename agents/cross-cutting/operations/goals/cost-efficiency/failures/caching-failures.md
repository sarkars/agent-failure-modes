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

**Mitigation Strategies**
1. **Semantic caching**: Use embeddings to match similar queries
2. **Tiered caching**: Different TTLs for different content types
3. **Cache warming**: Pre-populate cache with common queries
4. **Invalidation triggers**: Refresh cache when source data changes
5. **Confidence thresholds**: Only cache high-confidence matches
6. **A/B validation**: Periodically verify cached responses

**Detection**
- Track cache hit/miss rates
- Monitor API costs relative to query volume
- Identify repeated semantic queries
- Measure staleness of cached responses
- Alert on cache invalidation failures

## References

- [GPTCache](https://github.com/zilliztech/GPTCache) - Semantic caching for LLMs
- [LangChain: Caching](https://python.langchain.com/docs/modules/model_io/llms/llm_caching) - LLM caching patterns
- [Redis: LLM Caching](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Caching strategies
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Cost optimization
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost reduction
