# Workspace Isolation Bypass

## Issue
In a multi-workspace or multi-project system (e.g., separate Slack-style workspaces, Notion-style team spaces, or per-project environments within a single customer account), an agent operating in the context of one workspace is able to access or modify data belonging to a different workspace. Unlike a multi-tenant/account failure, this typically happens within a single customer's account across their own workspaces, and is usually rooted in shared backend infrastructure — a single search index, vector store, or cache — that wasn't partitioned by workspace ID as strictly as the application layer assumes.

**Frequency**: Occasional

**Symptoms**
- An agent scoped to "Workspace A" returns search results, documents, or messages that actually belong to "Workspace B" under the same customer account
- Isolation holds for direct record lookups but breaks for search, semantic retrieval, or aggregation features built on a shared index
- The bypass is intermittent and correlates with a specific feature (e.g., cross-workspace search suggestions, shared embeddings cache) rather than being present on every request
- Workspace administrators report seeing content they never created and don't recognize appearing in agent-generated summaries
- The underlying storage layer (e.g., a shared vector database namespace) doesn't enforce workspace boundaries as strictly as the application's access-control layer assumes it does

## Root Cause
Workspace isolation is often implemented as an application-layer convention — every query is expected to include a `workspace_id` filter — layered on top of infrastructure that is not itself workspace-aware, such as a shared full-text search index, a shared embedding/vector store, or a shared cache keyed loosely enough that entries can collide or bleed across workspaces. When a new feature (particularly one involving retrieval-augmented generation, semantic search, or cross-workspace "smart suggestions") is built against that shared infrastructure without threading the workspace filter all the way through the retrieval path, isolation that holds for ordinary CRUD operations silently fails for the new feature.

## Example
```
A team-collaboration product gives each customer account multiple
isolated workspaces (e.g., "Marketing" and "Engineering"), each meant to
be fully separate — different members, different content, no
cross-visibility by default. An AI assistant is added that uses
semantic search over a shared vector database to answer "find related
documents" questions, with embeddings for all workspaces stored in a
single collection for operational simplicity, distinguished only by a
`workspace_id` metadata field on each vector.

The assistant's retrieval query is built to filter by workspace using
that metadata field, but the approximate-nearest-neighbor index used
for the semantic search step retrieves the top-K nearest vectors first
and applies the workspace filter as a post-retrieval step, rather than
as a pre-filter on the index itself. When too few Marketing-workspace
vectors fall within the top-K results for a query, the retrieval logic
backfills the answer set with the next-nearest vectors regardless of
workspace, and the assistant, working for a Marketing-workspace user,
surfaces Engineering-workspace document excerpts as "related content"
because the isolation was enforced as a filter that could be silently
worked around by the retrieval algorithm's own fallback behavior.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cross-workspace data leakage in RAG/semantic-search features built on shared vector stores is an increasingly common finding in security reviews of AI-assisted collaboration products | Emerging pattern specific to retrieval-augmented agent architectures |
| Isolation gaps are disproportionately found in newer AI/search features layered onto existing multi-workspace products, compared to the products' original core CRUD isolation, which is typically well-tested | Common in feature-addition security reviews |
| Post-retrieval filtering (filter-after-search) is a recurring root cause of workspace/tenant leakage in vector-search systems, compared to pre-filtering (filter-as-part-of-search), which is more resistant to fallback-driven leaks | Well-documented risk in vector database implementation guidance |

## Mitigations
1. **Pre-filter, not post-filter, at the index layer**: Use vector/search index features that support filtering as part of the nearest-neighbor query itself (metadata pre-filtering or per-workspace namespaces/collections) rather than retrieving broadly and filtering the result set afterward.
2. **Per-workspace physical or logical partitioning**: Where feasible, use separate index collections, namespaces, or shards per workspace rather than a single shared collection distinguished only by a metadata field, so a filtering bug can't cross a boundary that doesn't structurally exist.
3. **No cross-workspace fallback without explicit opt-in**: Disable any retrieval fallback behavior that backfills results from outside the requested scope when too few in-scope results are found; return fewer results rather than silently expanding scope.
4. **Cross-workspace canary testing for retrieval features**: Specifically test semantic search, recommendation, and "related content" features (not just direct CRUD lookups) with known cross-workspace content to confirm isolation holds under retrieval, not just under exact-match queries.
5. **Workspace-tagged response verification**: Verify every retrieved result's workspace tag against the requesting context immediately before it's included in an agent's response, as a final backstop independent of the retrieval query's own filtering.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cross_workspace_result_count` | Count of retrieval results whose workspace tag doesn't match the requesting workspace | Alert threshold: > 0 (any occurrence) |
| `post_filter_fallback_trigger_rate` | Rate at which retrieval logic falls back to out-of-scope results due to insufficient in-scope matches | Alert threshold: > 0% (fallback should be disabled) |
| `shared_index_isolation_canary_pass_rate` | Pass rate of scheduled cross-workspace canary tests against shared search/retrieval infrastructure | Alert threshold: < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-Workspace Content Surfaced | A response includes content tagged to a workspace other than the requesting one | P1 | Halt the retrieval feature, notify affected workspace admins, patch the pre-filtering gap |
| Isolation Canary Failure | Scheduled cross-workspace canary test detects a leak | P1 | Page on-call, disable the affected retrieval feature until fixed |

## Related Patterns
- [Account-Level Data Scope](./account-level-data-scope.md) - the same class of failure at customer/tenant granularity rather than workspace granularity
- [Data Scope Boundary Violation](./data-scope-boundary-violation.md) - a related soft-boundary failure, typically within a single shared database rather than shared retrieval infrastructure
- [Scope Downgrade Not Enforced](./scope-downgrade-not-enforced.md) - a sub-agent with an unenforced scope downgrade can trigger this same cross-workspace exposure
