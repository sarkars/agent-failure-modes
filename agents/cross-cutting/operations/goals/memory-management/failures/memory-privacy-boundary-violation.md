# Memory Privacy Boundary Violation

## Issue
Memory intended to be scoped to a single user, tenant, or session leaks into a different user's, tenant's, or session's context — a shared vector index queried without a tenant filter, a session-ID collision, a caching layer that keys on the wrong scope, or a retrieval query broad enough to pull in another user's records because embeddings happen to be similar. The agent then surfaces one person's private facts, preferences, or history to someone else, without any error or access-denied signal, because from the retrieval system's point of view the query simply "worked" and returned relevant-looking results.

**Frequency**: Rare

**Symptoms**
- Agent references facts, names, or history belonging to a different user than the one it's currently serving
- A multi-tenant deployment shows one tenant's data surfacing in another tenant's session
- Issue reproduces only under specific similarity conditions (two users' data happen to be semantically close) rather than consistently
- No access-control error is logged, because the underlying query executed successfully and returned "relevant" results
- Root cause traces to a missing or incorrectly-applied scope/tenant filter in a retrieval query, not a broken authentication check

## Root Cause
Shared memory infrastructure (a single vector index or database serving many users/tenants for cost and operational simplicity) requires every retrieval query to explicitly filter by the correct scope — user ID, tenant ID, session ID — because the underlying similarity search or lookup mechanism has no inherent concept of privacy boundaries; it will happily return the nearest semantic matches regardless of whose data they belong to unless a filter constrains the search space. This filter is easy to omit in a specific code path (a new feature added without threading the scope parameter through, a fallback/debug query path, a caching layer keyed on a coarser identifier than intended), and because the query still executes successfully and returns plausible results, there is no natural failure signal — the bug looks identical to a normal, correct retrieval unless someone notices the content is wrong for who's asking.

## Example
```
Multi-tenant support agent, memory store is a single shared vector
index with records tagged { tenant_id, user_id, text, embedding }.

A new "quick recap" feature is added: when a user returns to a
chat, the agent retrieves recent relevant memories via
  search(query=user_message, top_k=5)
implemented by an engineer who copied an internal debug utility
that queries the full index without adding the tenant_id/user_id
filter present in the rest of the retrieval codebase.

User from Tenant B (a small business) opens a new chat and asks,
"What did we discuss last time about my subscription?"

The unfiltered search returns the top 5 semantically closest
matches across the *entire* shared index, including a record
from Tenant A (an unrelated company): "Tenant A's admin, Priya
Shah, reported billing issues and requested a refund of $2,400
citing a duplicate charge on card ending 4471."

Agent response to the Tenant B user: "Last time, you mentioned a
billing issue and a $2,400 refund request for a duplicate charge
on a card ending in 4471" — surfacing another company's employee's
name, billing detail, and partial card information to a completely
unrelated tenant, because the one code path handling this feature
never applied the tenant filter every other retrieval path in the
system does.
```

## Statistics
| Finding | Context |
|---------|---------|
| Missing or incorrectly-scoped filters in a subset of retrieval code paths are a common root cause of cross-tenant data exposure in shared-index multi-tenant systems | Reported pattern across multi-tenant retrieval system audits |
| Privacy boundary violations in memory systems are typically low in raw frequency but high in severity, often surfacing only through user report or periodic access audit rather than automated detection | Typical pattern for access-control gaps in retrieval-heavy systems |
| Enforcing scope filters at the index/storage layer rather than relying on every calling code path to apply them correctly eliminates the class of bug where a single omitted filter causes exposure | Estimated from teams that moved to storage-enforced tenant isolation |

## Mitigations
1. **Storage-enforced scoping**: Enforce user/tenant isolation at the storage layer itself (separate indexes per tenant, or a mandatory filter the query engine cannot bypass) rather than relying on every calling code path to remember to apply a filter.
2. **Mandatory scope parameter**: Make the retrieval API's signature require a scope/tenant identifier as a non-optional parameter with no unscoped query path available, so a missing filter is a compile-time or startup error, not a silent runtime gap.
3. **Cross-tenant leakage testing**: Include automated tests that specifically attempt to retrieve another tenant's seeded data through every retrieval code path, run as part of CI rather than relying on manual audit.
4. **Response-time provenance checks**: Before surfacing retrieved content to a user, verify each result's tenant/user tag matches the requesting session's scope as a defense-in-depth check, independent of the query-time filter.
5. **Access audit logging**: Log the scope filter actually applied on every retrieval query (not just the query itself) so post-hoc audits can identify any query that ran without proper scoping, even if no user noticed at the time.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unscoped_query_count | Count of retrieval queries executed without a detected tenant/user scope filter | Alert if > 0 |
| cross_tenant_result_rate | Rate at which a response-time provenance check finds a result tagged to a different tenant than the requester | Alert if > 0 |
| scope_filter_coverage | Fraction of retrieval code paths verified (via test) to enforce scope filtering | Alert if < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-tenant data surfaced | A response-time provenance check detects a result belonging to a different tenant than the requester | High | Immediately block the response, initiate privacy incident review, patch the offending retrieval path |
| Unscoped query detected | A retrieval query executes without an applied scope filter | High | Block the query path, page on-call, audit for prior unnoticed occurrences |

## Related Patterns
- [Memory Inconsistency Between Agents](./memory-inconsistency-between-agents.md) - both involve a shared memory store serving unintended or incorrect views, though this pattern is a security boundary failure rather than a consistency lag
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - an unfiltered query can return high-similarity-scored results from the wrong tenant, compounding a scoping bug with an over-trusted relevance signal
- [Memory Corruption Detection Failure](./memory-corruption-detection-failure.md) - both are failures where a retrieval succeeds and returns plausible-looking content that should have been rejected before reaching the agent
