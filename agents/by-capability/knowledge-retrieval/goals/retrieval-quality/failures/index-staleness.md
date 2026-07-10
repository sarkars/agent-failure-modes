# Index Staleness

## Issue: Retrieved Documents Are Outdated

**Frequency**: Common

**Symptoms**
- Answers based on superseded information
- Old policies/procedures cited
- Deprecated features described as current
- Version numbers or dates incorrect

**Root Cause**
Index not updated when source documents change. Old versions remain indexed alongside or instead of current versions.

**Example**
```
Current policy (updated last week): 
"Remote work requires manager approval"

Indexed version (6 months old):
"Employees may work remotely 2 days per week without approval"

User query: "Can I work from home?"
Retrieved: Old policy

Agent: "You can work remotely 2 days per week without approval"

Result: Employee violates current policy
```

## Mitigation Strategies

### Prevention
1. **Event-Driven Incremental Indexing**: Subscribe to source-system change events (CMS webhook, document-store commit log) and re-index within minutes of a change, instead of relying on periodic batch crawls that leave a stale window like the six-month-old policy in the example. Trade-off: requires reliable event delivery infrastructure from every source system.
2. **Single-Current-Version Enforcement**: When a document is superseded, mark the prior version as archived/non-retrievable at ingestion time rather than merely lower-ranked, so both versions can never simultaneously surface for the same query.
3. **Source-of-Truth Change Detection**: For sources without webhook support, use checksum or last-modified comparison against the canonical source on a tight polling interval, closing the freshness gap for systems that can't push change events.

### Detection & Response
1. **Index-vs-Source Staleness Audit**: Periodically diff a sample of indexed documents' content/timestamp against the live source system; alert when the delta exceeds the freshness SLA.
2. **High-Traffic Stale-Document Flagging**: Cross-reference documents with high retrieval frequency against their last-indexed timestamp, prioritizing re-indexing for popular-but-old documents like the remote work policy first.
3. **Superseded-Policy Usage Tracking**: When a document is marked superseded, log and alert on any subsequent retrieval that still surfaces it, since that indicates the archival step failed.

### Architecture Patterns
1. **TTL-Based Expiry With Forced Refresh**: Assign a max-age TTL per document type (e.g., policy documents: 7 days) after which the document is automatically re-fetched and re-indexed, or flagged if unreachable.
2. **Freshness-Boosted Ranking**: Incorporate document age as a ranking feature so the most recently updated version among semantically similar candidates is preferred, providing defense-in-depth even if the archival pipeline lags.
3. **Versioned Document Graph**: Maintain explicit supersession links between document versions; retrieval resolves to the latest version in the chain rather than treating each version as an independent, competing document.

### Metrics
1. **index_staleness_hours**: Target: < 4h (P50); Alert threshold: > 24h
2. **stale_document_retrieval_rate**: Target: < 1%; Alert threshold: > 3%
3. **high_traffic_stale_doc_count**: Target: 0; Alert threshold: any occurrence for docs with > 100 monthly retrievals
4. **superseded_doc_leak_rate**: Target: 0%; Alert threshold: any nonzero occurrence

### Alerts
1. **Stale Policy Surfaced** (P1): Condition - a document marked superseded is retrieved and used in synthesis. Action: immediately purge from the index, audit the archival pipeline, notify the content owner.
2. **Freshness SLA Breach** (P2): Condition - index_staleness_hours exceeds 24h for any source feed. Action: check webhook/polling health, manually trigger a re-index.
3. **High-Traffic Staleness** (P2): Condition - a document with > 100 monthly retrievals exceeds the staleness SLA. Action: prioritize immediate re-index over normal queue order.

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Stale data issues
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Enterprise RAG challenges
