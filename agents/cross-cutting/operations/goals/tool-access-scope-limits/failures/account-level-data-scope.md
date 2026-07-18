# Account-Level Data Scope

## Issue
In a multi-tenant SaaS product, a tool call made on behalf of one customer account is scoped using the wrong tenant/account identifier, causing the agent to read or write data belonging to a different customer entirely. This typically happens when the account ID is derived from a stale cache, a URL/session parameter that wasn't re-validated, or a default value used when the true tenant context is missing from the request.

**Frequency**: Occasional

**Symptoms**
- Agent surfaces a competitor's or unrelated customer's records in response to a routine lookup
- Support agent "sees" tickets, invoices, or configuration that don't belong to the account it's currently helping
- Cross-tenant data appears only intermittently, correlated with session reuse or connection pooling
- Downstream write operations (e.g., updating a subscription) apply to the wrong tenant's record
- Incident reports describe the agent as "confidently wrong" about which account it's operating on

## Root Cause
The tool layer trusts a tenant/account identifier passed implicitly through session state, a connection-pooled database client, or a cached lookup rather than requiring it to be explicitly re-derived and validated on every call. When that implicit context is stale, reused across requests (e.g., a pooled connection that wasn't reset), or defaults to a fallback account when missing, the query executes against the wrong tenant's data partition without raising an error, because the underlying query itself is syntactically valid — it's just scoped to the wrong `account_id`.

## Example
```
A customer-support agent uses a connection pool to a shared multi-tenant
Postgres database, where every table has a row-level `account_id` column.
The agent's tool wrapper sets the tenant context via a session variable
(`SET app.current_account_id = ...`) at the start of a conversation.

Due to connection pool reuse, a new conversation for Account B reuses a
pooled connection that still has Account A's session variable set from a
prior conversation, because the pooling middleware doesn't reset session
state between checkouts. The agent, working on behalf of Account B, calls
the "get recent invoices" tool. The query executes with Account A's
tenant context still active, returning Account A's invoices — including
line-item pricing — into a conversation with Account B's support rep.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cross-tenant data exposure is one of the most commonly reported classes of incidents in multi-tenant SaaS security audits, frequently tied to connection pooling or caching layers | Common finding in SaaS penetration tests and bug bounty reports |
| Session-variable-based tenant scoping (vs. per-query explicit parameterization) is disproportionately implicated when cross-tenant leaks occur | Typical of row-level-security implementations layered on shared connection pools |
| Time between introduction of a pooling/caching change and detection of a cross-tenant leak is often measured in weeks to months, since the failure is intermittent | Typical for latent multi-tenancy defects |

## Mitigations
1. **Explicit per-call tenant parameterization**: Pass the account/tenant ID as an explicit, required parameter on every tool call rather than relying on ambient session or connection state; reject any call missing it.
2. **Connection pool tenant isolation**: Reset or re-validate tenant-scoping session variables on every connection checkout, or use per-tenant connection pools instead of a shared pool with mutable session state.
3. **Row-level security with query-time verification**: Enforce database-level row-level security (RLS) keyed to the tenant ID passed in the query itself, so even a mis-scoped application-layer call is blocked at the data layer.
4. **Tenant-boundary canary queries**: Periodically run synthetic cross-tenant queries in production (using known test accounts) and alert immediately if any query returns data outside its expected tenant.
5. **Response-side tenant tagging and verification**: Tag every record returned from a tool call with its source `account_id` and have the agent runtime verify it matches the active conversation's account before surfacing the result.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cross_tenant_record_mismatch_count` | Count of returned records whose `account_id` doesn't match the requesting conversation's account | Alert threshold: > 0 (any occurrence) |
| `pooled_connection_session_reset_failures` | Rate of connection checkouts where tenant session state wasn't successfully reset | Alert threshold: > 0.1% of checkouts |
| `implicit_tenant_context_calls` | Count of tool calls executed without an explicit tenant parameter, relying on ambient context | Alert threshold: > 0 for any new tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-Tenant Data Return | A response-side verification check finds a record's `account_id` doesn't match the active conversation's account | P1 | Immediately halt the conversation, quarantine the connection pool member, notify security |
| Canary Tenant Query Failure | Synthetic cross-tenant canary query returns data for the wrong tenant | P1 | Page on-call, disable the affected tool pending root-cause fix |

## Related Patterns
- [Workspace Isolation Bypass](./workspace-isolation-bypass.md) - same class of failure at workspace rather than account/tenant granularity
- [Data Scope Boundary Violation](./data-scope-boundary-violation.md) - shares the pattern of an unenforced boundary at the query layer
- [Record-Level Access Not Enforced](./record-level-access-not-enforced.md) - account-level scoping failures often compound with missing per-record checks
