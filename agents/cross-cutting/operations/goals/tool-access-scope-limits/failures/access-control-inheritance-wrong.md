# Access Control Inheritance Wrong

## Issue
An agent's tool permissions are computed by inheriting from a parent context — the invoking user's role, the calling service's credentials, or a parent agent's session — rather than being independently assigned. When the inheritance logic doesn't map cleanly (e.g., a support agent inherits an admin's broad scope because the admin happened to trigger the workflow, or a background job inherits a service account's org-wide scope instead of the specific user's narrower one), the agent ends up with either far more access than the task requires or, less often, too little to complete legitimate work.

**Frequency**: Common

**Symptoms**
- Agent successfully reads/writes records that no individual policy explicitly grants it access to
- Access grants change unexpectedly when the same automation is triggered by different users
- Audit logs show the agent's effective permission set doesn't match its declared tool scope
- Over-privileged incidents cluster around admin-triggered or system-triggered runs, not regular user runs
- Under-privileged failures appear when a narrowly-scoped user triggers a workflow that needs broader lookup access

## Root Cause
Most agent frameworks resolve tool permissions at invocation time by walking up a context chain (session → user → team → service account) and taking the first or broadest match, rather than computing an explicit, task-scoped permission set. This conflates "who can invoke the agent" with "what the agent should be allowed to touch while running," so any elevated permission anywhere in the chain propagates silently into the agent's runtime capability.

## Example
```
A billing-support agent is built to run identically whether triggered by a
front-line support rep or by an internal ops-admin dashboard. Both invocation
paths pass through the same session-inheritance middleware, which sets the
agent's tool scope to "whatever the invoking principal can do."

When triggered by the ops-admin dashboard (itself authenticated with an
org-admin service account for unrelated reasons), the agent inherits
org-admin scope. A user asks it to "look up this customer's refund
history" — the agent's underlying tool call to the billing API is not
scoped to that customer's account, so it queries and returns refund
records across all customers matching a loose text filter, because
nothing in the tool layer clipped the inherited admin scope down to the
single-customer task at hand.
```

## Statistics
| Finding | Context |
|---------|---------|
| Over-privileged agent sessions are estimated to account for 20-35% of excess-access findings in agentic tool-access audits | Internal security reviews of production agent deployments |
| Inheritance-related scope defects are disproportionately found on admin- or system-triggered code paths versus regular end-user paths | Common pattern across incident postmortems |
| Median time-to-detection for silently over-scoped agents is measured in weeks, since the excess access is rarely exercised until an unusual query triggers it | Typical of coarse-grained access architectures |

## Mitigations
1. **Explicit task-scoped permission computation**: Compute the agent's tool scope from the specific task/intent being executed, not from a walk up the invocation chain — treat inherited context as an input to a scoping function, never as the scope itself.
2. **Scope ceiling, not scope pass-through**: Define a maximum permission ceiling per agent role independent of the caller, and intersect (never union) the caller's permissions with that ceiling.
3. **Per-invocation scope logging with diffing**: Log the resolved effective scope on every invocation and alert when the same agent/workflow resolves to a materially different scope across runs triggered by different principals.
4. **Deny by default on ambiguous inheritance**: When the context chain is ambiguous or has multiple candidate parents (e.g., both a user and a service account), fail closed to the narrowest interpretation rather than the broadest.
5. **Periodic inheritance-chain audits**: Regularly enumerate all invocation paths for each agent and confirm the resolved scope matches the documented least-privilege policy for that task, not just for the most common path.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `scope_variance_by_invoker` | Standard deviation of resolved permission-set size across invocations of the same agent/workflow | Alert if variance > 0 for workflows declared "fixed scope" |
| `admin_triggered_excess_access_rate` | Share of admin/system-triggered runs where resolved scope exceeds the task's declared minimum requirement | Alert threshold: > 5% |
| `unscoped_query_result_size` | Rows/records returned per tool call relative to the task's expected single-entity cardinality | Alert threshold: > 10x expected cardinality |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Inherited Scope Mismatch | Resolved effective scope for a given workflow differs from its documented least-privilege baseline | P2 | Freeze the invocation path, review the inheritance chain, patch the scoping function |
| Cross-Principal Scope Drift | Same automation invoked by two different principals resolves to permission sets differing by more than the expected per-user delta | P2 | Audit both invocation paths, confirm intended vs. accidental elevation |

## Related Patterns
- [Scope Downgrade Not Enforced](./scope-downgrade-not-enforced.md) - both involve a permission-narrowing step that silently fails to apply
- [Record-Level Access Not Enforced](./record-level-access-not-enforced.md) - inherited over-broad scope often manifests as missing record-level checks downstream
- [Workspace Isolation Bypass](./workspace-isolation-bypass.md) - inheritance from a system/service account is a common root cause of cross-workspace leakage
