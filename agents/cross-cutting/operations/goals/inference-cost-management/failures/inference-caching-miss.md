# Inference Caching Miss

## Issue
A response-cache or prompt-cache layer sits in front of (or inside) an inference service to avoid re-running expensive generation for repeated or overlapping requests, but the cache key strategy is too narrow — keying on the full raw prompt string including volatile elements like timestamps, session IDs, or reordered context chunks — so semantically identical or highly overlapping requests are treated as cache misses. The service pays full inference cost repeatedly for work it has effectively already done, and the cache exists in name only, contributing overhead without delivering the cost savings it was built for.

**Frequency**: Very Common

**Symptoms**
- Cache hit rate is far below what request-pattern analysis suggests it should be, given how repetitive the underlying prompts actually are
- Near-identical requests (same question, different capitalization, trailing whitespace, or a timestamp embedded in a system prompt) consistently miss
- Prefix/prompt-caching metrics from the underlying LLM provider show low cache-token ratios despite large shared system-prompt or few-shot-example prefixes across requests
- Cost-per-request doesn't drop after a caching layer is deployed, or drops far less than the projected savings from the initial business case
- Cache size grows rapidly with a long tail of single-use keys, indicating the key space is far more fragmented than the actual request semantics

## Root Cause
Caching effectiveness depends entirely on the key function capturing "meaningfully the same request" while ignoring irrelevant variation, but the default and easiest implementation is to hash the raw input verbatim. Any incidental difference — a request ID embedded in the prompt for tracing, a "current time" field in a system prompt, non-deterministic ordering of retrieved context chunks in a RAG pipeline, or even different whitespace/casing — produces a different hash and a guaranteed miss, even though the semantic content and therefore the correct output are identical or near-identical. This is compounded at the provider level: LLM APIs that offer prefix/prompt caching key on exact token-prefix matches, so if the shared system prompt or few-shot examples aren't placed as a stable, byte-identical prefix at the start of every request (e.g. dynamic content is interleaved before the static portion), the provider-side cache never engages either. The result is two independent caching opportunities — application-level response caching and provider-level prefix caching — both silently disabled by the same class of key-instability problem, and because a cache miss fails "safely" (it just falls through to a real inference call), nothing alerts anyone that the cache is underperforming.

## Example
```
A customer-support agent wraps every user question in a system prompt that
includes a live "Current time: 2026-07-19T14:32:07Z" field for
timestamp-aware responses, followed by 40 few-shot examples (roughly 3,200
tokens) and then the retrieved knowledge-base context, which is assembled
by concatenating the top-5 retrieved chunks in whatever order the vector
search returned them.

The team adds a response cache keyed on a hash of the full prompt string,
expecting a high hit rate since maybe 30% of user questions are close
variants of a small set of common issues ("how do I reset my password",
"where is my order").

In production, the cache hit rate is 2%. Two problems compound:
1. The embedded timestamp changes every request, so the hash never
   matches even for verbatim-identical questions asked a minute apart.
2. Provider-side prefix caching never engages either, because the
   volatile timestamp sits before the stable 3,200-token few-shot block,
   invalidating the "stable prefix" the provider's cache relies on.

The team is paying full few-shot-prefix processing cost (3,200 input
tokens at full price) on every single request, an estimated $4,800/month
in avoidable input-token cost, despite having built a caching layer
specifically to prevent this.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cache hit rates for response caches keyed on raw prompt text are commonly under 5-10% even when 25-40% of traffic is semantically near-duplicate | Typical range observed in production caching layers before key normalization |
| Restructuring prompts to place volatile content after a stable prefix commonly restores provider-side prefix-cache hit rates to 60-90% for repetitive workloads | Estimated range from prompt-engineering-for-caching case studies |
| Input-token cost reduction from effective prefix caching on few-shot-heavy prompts is commonly 40-70% for the cached portion | Typical range for workloads with large stable system-prompt/few-shot prefixes |

## Mitigations
1. **Normalize cache keys before hashing**: Strip or canonicalize volatile elements (timestamps, request IDs, whitespace, casing) from the cache key computation, keying only on the semantically meaningful content, so incidental variation doesn't force unnecessary misses.
2. **Stabilize prompt structure for prefix caching**: Restructure prompts so static content (system prompt, few-shot examples, tool schemas) forms a stable, byte-identical prefix at the start of every request, and place volatile content (timestamps, session-specific data) at the end, so provider-side prefix caching can engage.
3. **Sort or canonicalize non-deterministic context ordering**: For RAG or multi-source context assembly, apply a deterministic ordering (e.g. sort by document ID or relevance score with stable tiebreaking) rather than whatever order retrieval happened to return, so equivalent context sets produce identical cache keys.
4. **Semantic/fuzzy cache layer for near-duplicates**: For workloads where exact-match caching is insufficient, add an embedding-similarity-based cache tier that can serve a cached response for near-duplicate queries above a similarity threshold, with appropriate guardrails on when reuse is safe.
5. **Monitor and alert on cache effectiveness, not just cache existence**: Track hit rate and cost-avoided-by-cache as first-class metrics from day one of deployment, so an underperforming cache is caught immediately rather than discovered months later during a cost review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cache_hit_rate | Fraction of requests served from cache versus full inference | Alert if < expected baseline (e.g. < 15%) for a workload with known repetition |
| prefix_cache_token_ratio | Fraction of input tokens served from provider-side prefix cache versus billed at full price | Alert if < 30% for prompts with a large stable prefix by design |
| cost_avoided_by_cache | Estimated dollar cost avoided by cache hits, computed from hit count times average per-request inference cost | Alert if flat or declining week-over-week while traffic grows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cache hit rate below expected baseline | cache_hit_rate falls below the workload's modeled expected hit rate for 24+ hours | Medium | Audit cache key normalization; check for newly introduced volatile fields in cached prompts |
| Prefix cache not engaging | prefix_cache_token_ratio near zero despite a large designed-to-be-stable prompt prefix | High | Review prompt assembly order for volatile content placed before the stable prefix |

## Related Patterns
- [Batch Cost Inefficiency](./batch-cost-inefficiency.md) - both describe infrastructure meant to reduce per-request cost that silently underperforms its design intent
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - a low cache hit rate forces more requests onto the full-latency, full-cost inference path, worsening both dimensions simultaneously
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - a poorly performing cache directly depresses cost-per-successful-output even when raw throughput looks unaffected
