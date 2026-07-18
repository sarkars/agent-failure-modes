# Join Depth Limit

## Issue
Query tools built on relational or graph data — GraphQL APIs, ORM-backed REST query endpoints, relational-API query builders — commonly cap how many joins or nested relations can be traversed in a single query, for example a maximum of 5 levels of nested relations. An agent that dynamically constructs a query to satisfy a broad information-gathering goal (e.g., "get the order, its customer, their company, the company's account manager, and that manager's team") can easily exceed this depth without realizing it, especially when the query is assembled programmatically by chaining relation names rather than authored by a person who would naturally notice the query getting unwieldy.

**Frequency**: Common

**Symptoms**
- Queries rejected with errors referencing maximum join/relation depth, occurring only for certain data paths and not others
- Agents that work correctly for shallow queries (2-3 relations) and fail only when a task requires deeper traversal
- Query construction logic that adds a `.join()` or nested-field call per step of a multi-hop reasoning chain, with no depth counter or limit awareness
- Errors that appear late in a multi-step agent plan, after several dependent steps have already committed side effects, wasting the earlier work
- Workarounds where developers manually flatten a query that an agent could not construct within the depth limit, indicating the agent silently failed at a task a human could still accomplish differently

## Root Cause
Join-depth limits exist to bound query-planning cost and prevent pathological queries (especially in GraphQL, where a naive recursive schema can allow arbitrarily deep nesting) from overwhelming the database or query engine. Agents that build queries programmatically — walking a relation graph to satisfy a data-gathering goal — treat relation traversal as a logical operation with no inherent cost, because from the agent's perspective "just follow one more relation" looks the same at depth 2 as at depth 8. Without an explicit depth counter tied to the tool's documented limit, the agent has no signal to stop extending the query and instead must discover the ceiling via a rejected request, often after already having planned subsequent steps assuming the deep query would succeed.

## Example
```
An agent researching a compliance question needs to trace a payment back
through several relations: payment -> invoice -> order -> customer ->
account -> parent_organization -> compliance_officer. It constructs a
single GraphQL query nesting all seven relations to fetch this chain in
one round trip. The GraphQL server enforces a max query depth of 6. The
query is rejected at parse time with
{"errors": [{"message": "Query exceeds maximum depth of 6 (actual: 7)"}]}
before any data is returned. The agent's error handling recognizes generic
GraphQL errors but has no depth-specific fallback, so it retries the
identical query twice more (each failing identically) before falling back
to a much slower path: seven separate single-hop queries, each requiring
a full round trip, turning a task that should take one call into eight.
```

## Statistics
| Finding | Context |
|---------|---------|
| GraphQL and similar query APIs commonly enforce max depth limits in the 5-15 level range | Observed as a standard defensive configuration for public and internal GraphQL schemas |
| Deep-traversal queries that exceed depth limits are typically rejected at parse/validation time, before any execution cost is incurred, unlike complexity-score rejections which may occur later | Structural property of depth-limit enforcement vs. cost-based limits |
| Agents lacking a depth-tracking mechanism in query-construction code have no way to anticipate a depth-limit rejection before submission, since depth is only implicitly encoded in the query string being built | Based on typical programmatic query-builder patterns |

## Mitigations
1. **Track traversal depth explicitly during query construction**: Maintain a depth counter as the agent walks a relation graph and stop extending the query (splitting into multiple queries instead) once it approaches the tool's documented max depth.
2. **Split deep traversals into sequential shallower queries**: When a full traversal would exceed the limit, decompose it into a chain of queries each within the depth limit, using the result of one to parameter the next.
3. **Cache intermediate relation results to avoid re-traversal**: If a deep chain is queried repeatedly across tasks, cache intermediate nodes (e.g., customer -> account mapping) so future queries can start from a cached midpoint rather than re-walking the full depth.
4. **Prefer denormalized or purpose-built endpoints when available**: Many APIs expose a flatter, purpose-specific endpoint (e.g., a "compliance chain" lookup) precisely to avoid deep ad hoc joins; check for these before constructing a maximal nested query.
5. **Validate query depth client-side before submission**: Parse the constructed query (or track depth during construction) and compare against the tool's known max depth, rejecting and rebuilding before the round trip rather than after.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `query.max_depth_constructed` | Deepest nesting level in agent-constructed queries against a given tool | Alert when within 1 level of the tool's documented max |
| `query.depth_limit_rejection_count` | Count of queries rejected specifically for exceeding max depth | Alert if > 0 |
| `query.fallback_multi_call_rate` | Rate at which single deep queries are replaced by multiple shallow fallback calls | Track as a proxy for depth-limit friction |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Query depth limit exceeded | Query rejected with a max-depth validation error | Medium | Decompose into sequential shallower queries, log relation path for query-builder review |
| Repeated identical deep-query retries | Same over-depth query resubmitted unchanged 2+ times | High | Disable naive retry, route to depth-aware query decomposition |

## Related Patterns
- [Query Complexity Limit](./query-complexity-limit.md) - a cost-based sibling limit that can reject a query even when depth alone is within bounds
- [Nesting Depth Limit](./nesting-depth-limit.md) - the same depth-limiting concept applied to payload structure rather than query relation traversal
- [Query Planning Timeout](./query-planning-timeout.md) - deep or complex queries that pass depth/complexity checks can still time out during planning before execution
