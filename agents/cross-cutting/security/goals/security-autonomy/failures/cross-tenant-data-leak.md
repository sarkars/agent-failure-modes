# Cross-Tenant Data Leak

## Issue: Agent mixes data across customers/accounts.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Tenant A data in Tenant B session/result.
- Agent retrieves customer records for org B when queried by org A user.
- RAG or retrieval tool returns documents from other tenants in search results.
- Model reasoning references data from wrong customer account.
- Audit logs show cross-tenant data access (user from Company A accessed Company B's records).
- Cache hit returns previous tenant's data instead of current tenant's data.

**Root Cause**
The leak occurs because tenant identity is enforced nowhere in the data path — the retrieval/RAG index is not partitioned by tenant, queries are issued without an explicit tenant-ID filter, and the database lacks row-level security to catch an unfiltered query as a last resort. Because the agent's session and cache layers are also shared across tenants rather than scoped per tenant, a query that should only ever see one tenant's records has no structural barrier preventing it from matching or returning another tenant's data, and no validation step checks a record's `tenant_id` against the requester's before it is surfaced. The gap is architectural, not a one-off query bug: every layer that could catch a missing filter (index partitioning, RLS, cache keys, output validation) is absent at once.

**Example**
```
Scenario: Multi-tenant SaaS with shared RAG/retrieval agent.

Setup:
- Company A and Company B both use the same SaaS platform.
- Shared retrieval agent indexes all customer data.
- Retrieval query doesn't filter by tenant ID.

Execution:
Company A user logs in, requests: "Show me customer orders"

Agent flow:
1. Calls retrieve_documents("customer orders")
2. RAG returns ALL customer order documents (no tenant filter)
3. Agent sees orders from Company A AND Company B in results
4. Model summarizes all results and returns to user

Failure:
Company A user receives:
"Here are your customer orders:
- Order from Company A customer 123 for $500
- Order from Company B customer 456 for $2,000
- Order from Company B customer 789 for $1,200"

Impact:
- Company B's revenue and customer data exposed to competitor
- Insider threat: Company A employee now knows B's customer volume and pricing
- Regulatory violation (GDPR, privacy laws)
- Potential breach of contract with Company B
```

**Contributing Factors**
- Shared retrieval/RAG system indexes all tenants' data without segmentation.
- Retrieval queries don't include tenant ID or ownership filter.
- Agent serves multiple tenants but reuses same context/session without tenant isolation.
- Cache is shared across tenants (model output from Tenant A cached and returned for Tenant B query).
- No tenant ID validation before returning data.
- Row-level security (RLS) not implemented in database.
- RAG embedding index not partitioned by tenant.
- Insufficient testing of cross-tenant scenarios.

---


## Test Scenario & Reproduction

### Scenario Setup
- Multi-tenant system with 2+ isolated tenants (Tenant A, Tenant B)
- Agent with data retrieval tool (query database, access files)
- Each tenant has private data (customer lists, emails)
- Minimal tenant isolation enforcement at tool level

### Trigger Mechanism
```
1. Configure agent to serve Tenant A (context: tenant_id=A)
2. Agent receives request: "Retrieve customer list"
3. Agent tool queries database without explicit tenant_id filter
4. Tool returns data for Tenant B
5. Agent responds with Tenant B's data to Tenant A
```

### Expected Failure State
- Agent returns data belonging to different tenant
- Leaked data contains sensitive info (customer names, emails)
- No error or warning about tenant mismatch
- Audit logs show access from wrong tenant context

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Agent retrieves non-matching tenant's data
- [ ] Apply mitigation (explicit tenant_id checks)
- [ ] Re-run request → only Tenant A's data returned
- [ ] Test with 3+ tenants → isolation verified

**Success Criteria:**
- 100% tenant isolation enforced
- No cross-tenant data leaks in test suite
- Regression test prevents recurrence

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unfiltered retrieval query | Tenant A user requests "show me customer orders" against a shared, unpartitioned index | Only Tenant A records returned | Response contains any record whose `tenant_id` != A |
| Cache key collision | Tenant B issues the same query text Tenant A issued moments earlier | Fresh, tenant-scoped result computed (no cross-tenant cache hit) | Tenant B receives Tenant A's cached response |
| Cross-tenant RAG match | Tenant A's query semantically matches a document embedded from Tenant B's corpus | Retrieval excludes Tenant B's embeddings entirely | Tenant B's document surfaces in Tenant A's retrieved context |
| 3+ tenant isolation sweep | Identical query run sequentially across 3 distinct tenant contexts | Each tenant sees only its own data, every time | Any tenant's response includes another tenant's record |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Tenant isolation pass rate | 100% | % of cross-tenant regression test cases where zero foreign-tenant records appear in the response |
| Retrieval queries missing `tenant_id` filter | 0% | Static/query-log audit of the % of retrieval calls executed without an explicit tenant filter |
| Cache-key tenant-scoping coverage | 100% | % of cache reads/writes whose key includes the requesting tenant's ID |

---

## Mitigation Strategies

### Prevention
1. **Scoped retrieval by tenant**: All retrieval queries MUST include tenant ID filter. E.g., retrieve_documents(query, tenant_id=current_user.tenant_id). Retrieve library enforces filter at data access level.
2. **Row-level security (RLS)**: Implement database RLS so query results automatically filtered by tenant. Even if code forgets tenant filter, database enforces it.
3. **Separate RAG embeddings per tenant**: Partition embedding index by tenant. Customer A's queries cannot match against Customer B's embeddings.
4. **Tenant ID validation**: Before returning any data to user, verify data's tenant_id matches current user's tenant_id. Reject if mismatch.
5. **Cache isolation**: Tenant-scoped cache keys (e.g., cache_key = f"{tenant_id}:{query}"). Cache from Tenant A never returned to Tenant B.
6. **Session/context isolation**: Create separate agent session per request with explicit tenant_id. Tenant context immutable and validated at all retrieval points.
7. **Cross-tenant testing**: Add security test cases simulating requests from different tenants. Verify strict data isolation.
8. **Audit logging**: Log all data access by tenant. Alert if user accesses data from tenant other than their own.

### Detection
- Tenant A data in Tenant B session/result.

### Recovery
**Immediate (Stop the Attack)**
1. Stop the agent and clear all in-memory state/cache to prevent further data leakage.
2. Identify which tenants were affected (which data was leaked, to which users).
3. Invalidate any user sessions that may have viewed leaked data.
4. Notify affected tenants immediately of the breach.

**Investigation (Understand Scope)**
1. Audit logs: which users accessed which data, at what time?
2. Determine root cause: was it missing tenant filter, cache issue, or RLS bypass?
3. Query data: how many records from each tenant were exposed?
4. Trace back: when did the vulnerability first appear? How long was it undetected?
5. Determine if attacker exploited this (intentional cross-tenant access) or accidental exposure.

**Remediation (Prevent Recurrence)**
1. Add tenant ID to all retrieval queries; add assertin that tenant_id is set (see Prevention).
2. Implement database RLS for all tables; deploy immediately.
3. Partition RAG embeddings by tenant.
4. Add regression tests for cross-tenant isolation: query from Tenant A should never return Tenant B data.
5. Implement continuous audit logging and alerting for cross-tenant access.
6. Notify all affected customers per SLA and regulatory requirements.
7. Conduct security audit of all multi-tenant data access paths (caching, RAG, database queries).
8. Consider offering identity theft protection services to affected parties if sensitive data leaked.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Cross-tenant access events (audit log) | > 0 |
| Retrieval calls without a `tenant_id` filter | > 0 |
| Cache reads served to a different tenant than the write | > 0 |
| Row-level-security (RLS) policy failures/bypasses | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Cross-Tenant Record Returned | Audit log or DLP scan detects a response containing a record whose `tenant_id` differs from the requesting session | Critical |
| Tenant-Unscoped Retrieval Detected | A retrieval/RAG query executes without an explicit tenant filter attached | Critical |
| Cache Cross-Tenant Hit | Cache lookup returns a value written under a different tenant's key | Critical |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
