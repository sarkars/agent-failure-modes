# Multi-Tenant Data Leakage

## Issue: Agent Leaks Data Between Tenants Due to Insufficient Isolation

**Frequency**: Occasional

**Symptoms**
- Agent returns data from different customer in response
- Context bleeding between conversations
- References to other users' information
- Data persists across tenant boundaries
- Insufficient cleanup between requests

**Root Cause**
In multi-tenant SaaS deployments, agents share infrastructure but must isolate data per tenant. When isolation is weak (no request-scoped state, shared caches, thread-local storage), tenant A's data can leak into tenant B's response. This is especially dangerous with caching.

**Example**
```
Multi-tenant SaaS with shared agent pool:

Tenant A (Company Alpha):
- User asks: "What's our Q3 revenue?"
- Agent queries data, gets: "$5M"
- Response cached with tenant_id=A

Tenant B (Company Beta):
- User asks: "What's our revenue?"
- Agent retrieves from cache: "$5M" (WRONG COMPANY)
- No cache invalidation between tenants

OR

Tenant A conversation:
- User asks about "Project X, budget $50M"
- Agent stores in memory: project_x_budget = $50M

Tenant B conversation:
- User asks: "What's our project budget?"
- Agent memory still has: $50M (from Tenant A!)
- Returns wrong answer

Impact:
- Competitive intelligence leaked
- Contract terms exposed
- Financial data exposure
- Regulatory violations (GDPR, HIPAA)
- Customer trust loss
```

**Key Statistics**
- 15-20% of multi-tenant SaaS systems have data leakage vulnerabilities
- Average leakage detection time: 3-6 months (discovered by customer)
- Cost of data breach: $1M-100M+ (varies by data sensitivity)
- 80% of leakages due to insufficient cache isolation

**Contributing Factors**
- Shared agent instances across tenants
- Global caches without tenant keys
- Thread-local storage not cleared
- No request-scoped isolation
- Cache never invalidated between requests

---

## Test Scenario & Reproduction

### Scenario Setup
- Shared agent pool serving multiple tenants with a global cache or in-memory store not keyed by tenant_id
- No request-scoped context isolation between concurrent tenant sessions
- No automated isolation test verifying Tenant A cannot retrieve Tenant B's cached/stored data

### Trigger Mechanism
1. Run a query from Tenant A that populates a cache or agent memory with tenant-specific data
2. Immediately run a semantically similar query from Tenant B against the same shared agent pool
3. Observe whether Tenant B's response contains Tenant A's data

**Example Reproduction Steps:**
```
1. As Tenant A, ask: "What's our Q3 revenue?" — record the returned figure
2. Immediately as Tenant B, ask: "What's our revenue?"
3. Compare Tenant B's answer against Tenant A's figure
4. Repeat for a memory-based scenario: Tenant A states a project budget, then Tenant B asks about "our project budget"
5. Measure: % of cross-tenant query pairs where Tenant B's answer matches Tenant A's data
```

### Expected Failure State
- Tenant B receives Tenant A's cached figure or memory-stored fact
- No tenant_id mismatch is detected or blocked at the cache/memory layer
- No automated isolation-test alert fires despite a live cross-tenant leak

---

## Mitigation Strategies

### Prevention

1. **Request-Scoped Context Isolation**: Use request-scoped containers/contexts that automatically isolate per request. Every request gets a fresh context; data cannot leak across requests even with shared agent instances.

2. **Tenant-Keyed Caching**: Every cache entry must include tenant_id as part of the key. Lookups must include tenant_id. Disable cross-tenant cache hits.

3. **Memory Isolation Testing**: Before multi-tenant deployment, run "isolation tests" that simulate concurrent tenant access and verify no data leakage occurs.

### Detection & Response

1. **Audit Logging of Data Access**: Log every data access with tenant_id, user_id, timestamp, and data accessed. Compare logs across tenants to detect anomalies.

2. **Automated Isolation Verification**: Periodically run automated checks: "Can Tenant A access Tenant B's data?" If yes, alert immediately.

3. **Cache Invalidation Monitoring**: Track cache hit rates per tenant. If Tenant B gets cache hit with Tenant A's data (identified by tag), alert.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cross_tenant_cache_hits` | Cache hits with wrong tenant_id | >0 |
| `data_access_without_tenant_check` | Queries missing tenant_id filter | >0 |
| `isolation_test_failures` | % of isolation tests that fail | >0% |
| `audit_log_anomalies` | Tenant accessing other tenant's data | >0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-Tenant Cache Hit | Cache returned data for different tenant | P1 | Investigate immediately; clear cache; notify customers |
| Data Access Anomaly | Query returned wrong tenant's data | P1 | Incident response; audit affected data |
| Isolation Breach Detected | Automated test found isolation failure | P1 | Fix isolation immediately; halt deployments |
| Audit Log Anomaly | Tenant accessed another tenant's data | P1 | Investigate and escalate to security |

---

## References

- [OWASP: Broken Object Level Authorization](https://owasp.org/www-project-api-security/API3_BROKEN_OBJECT_LEVEL_AUTHORIZATION) — Multi-tenant authorization failures
- [SaaS Security Best Practices](https://owasp.org/www-community/attacks/Multi-Tenant_Authorization) — Tenant isolation patterns
