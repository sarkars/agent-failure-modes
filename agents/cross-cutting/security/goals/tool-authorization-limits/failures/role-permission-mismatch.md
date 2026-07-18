# Role Permission Mismatch

## Issue
An agent is assigned a role intended to convey a specific level of access (e.g. "support-tier-1"), but the mapping from that role to the underlying tool's actual permission model is incomplete, outdated, or was translated incorrectly during integration — so the agent ends up able to do meaningfully more, or less, than the role's name and documentation suggest. Unlike a missing check, the check exists and runs; it's the mapping table itself that's wrong.

**Frequency**: Common

**Symptoms**
- The role-to-permission mapping is maintained in application config, separate from the underlying system's own role/permission definitions, and the two have drifted apart
- A role named narrowly (e.g. "billing-viewer") maps to an underlying API scope that is actually broad (e.g. full billing read/write)
- New capabilities added to an underlying platform (a new API endpoint, a new admin action) are automatically included in an existing role's granted scope because the mapping uses wildcard or "all available" scopes rather than an explicit allow-list
- Two roles that are supposed to differ in access turn out, on inspection, to map to identical underlying permission sets
- Permission mapping was defined once at integration time and never revisited as the underlying tool's own permission model evolved

## Root Cause
Agent frameworks and the third-party tools/APIs they call often use different permission vocabularies (an internal "role" concept versus the tool's own scope/grant system), requiring an explicit translation layer. That translation is typically built once, by hand, at integration time, and isn't kept in sync as either side evolves — the underlying API adds new scopes that get swept into a wildcard grant, or the internal role taxonomy changes without a corresponding update to the mapping table. The mismatch is invisible in normal operation because most requests exercise only the subset of permissions both sides agree on.

## Example
```
1. An internal "support-tier-1" role is mapped to a third-party CRM's OAuth scope "crm.read crm.write"
   at integration time, because at that time crm.write only covered updating ticket status, which
   support-tier-1 agents were meant to do.
2. Months later, the CRM vendor expands the crm.write scope to also cover bulk contact deletion and
   billing plan changes, as part of an unrelated platform update -- the scope name stays crm.write but
   its coverage grows.
3. No one revisits the internal role-to-scope mapping when the vendor's scope semantics change.
4. A support-tier-1 agent, whose documented role is "read tickets, update ticket status only," is now
   able to bulk-delete contacts and modify customer billing plans, because the OAuth scope it was granted
   long ago silently expanded underneath it.
5. The mismatch is only discovered when a support agent, following an ambiguous instruction, deletes a
   batch of contacts -- an action nobody realized support-tier-1 could perform.
```

## Statistics
| Finding | Context |
|---------|---------|
| Role-to-permission mapping drift is a common finding whenever an underlying third-party API's scope model changes after initial integration | Common finding in third-party integration security reviews |
| Wildcard or broad-scope grants used as a shortcut during integration are disproportionately represented in over-permissioned agent roles | Typical pattern in agent access audits |
| Periodic reconciliation between internal role definitions and underlying tool scopes catches most of this drift before exploitation | Standard remediation for scope-drift findings |

## Mitigations
1. **Use explicit allow-lists instead of wildcard scopes**: Map each internal role to a specific, enumerated list of underlying permissions/actions rather than a broad scope name that can silently expand.
2. **Reconcile role mappings on a recurring schedule**: Periodically diff each role's granted underlying permissions against its documented intent, especially after third-party API/scope updates.
3. **Version and review the mapping table like code**: Treat the role-to-permission mapping as a reviewed artifact with change history, not a one-time config set at integration.
4. **Subscribe to vendor scope-change notifications**: For third-party tools, monitor changelogs or API version notes for scope semantic changes and re-validate mappings when they occur.
5. **Test roles against expected negative cases**: For each role, maintain a test asserting specific actions are NOT permitted, so scope expansion that grants unintended access breaks a test rather than going unnoticed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| role_actual_vs_documented_permission_diff | Count of underlying permissions granted to a role beyond its documented allow-list | > 0 after any mapping reconciliation |
| wildcard_scope_role_count | Number of internal roles mapped to a wildcard or "all" scope rather than an explicit list | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Role exercises undocumented permission | A role performs an action not present in its documented allow-list | High | Investigate scope drift, tighten mapping, review recent actions by that role |
| Vendor scope semantics changed | Third-party API changelog indicates a scope used in an existing mapping now covers new actions | Medium | Re-review and re-approve the mapping before the change takes effect for the agent |

## Related Patterns
- [Admin Operation Called By Non-Admin](./admin-operation-called-by-non-admin.md) - both result in a role having more effective access than intended, via different mechanisms
- [Permission Cascade Incorrect](./permission-cascade-incorrect.md) - both are cases of the enforced permission model diverging from the intended one
- [Granular CRUD Permission Not Enforced](./granular-crud-permission-not-enforced.md) - a common specific symptom of role-permission mismatch at the operation-verb level
