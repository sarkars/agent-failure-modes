# Permission Cascade Incorrect

## Issue
Permissions in a hierarchical system are meant to narrow as they cascade down (an org-level admin has broad rights, a team-level member has fewer, a specific user within that team has only what's explicitly granted), but the agent's logic for resolving effective permission at a given level applies the wrong tier's rules — either inheriting a broader ancestor permission that should have been narrowed, or failing to inherit a permission that should have propagated down, resulting in over- or under-granted access.

**Frequency**: Common

**Symptoms**
- A user with only team-level access can perform actions that should require org-level admin rights
- A permission explicitly granted at the org level doesn't take effect for a team nested under it, requiring redundant per-team re-grants
- Effective-permission calculations differ between the agent's tool layer and the underlying platform's own permission resolution, giving inconsistent results for the same user
- Removing a permission at a parent level (org) doesn't revoke it at child levels (team, user) that had inherited it
- The agent's permission-check function takes only the immediate role, not the full hierarchy path, as input

## Root Cause
Correctly resolving cascading permissions requires walking the full ancestor chain (or a materialized/cached equivalent) and applying the correct combination rule at each level — typically "most restrictive wins" for narrowing scopes, or explicit override semantics where a child-level grant/deny takes precedence over a parent's. Agent tool layers frequently implement a shortcut: checking only the user's most specific role assignment, or only the top-level org role, instead of resolving the full hierarchy, because the shortcut is simpler to build and passes tests written against a single level of the hierarchy rather than multi-level scenarios.

## Example
```
1. A document-management agent enforces permissions across org -> team -> user. The intended rule: a
   user's effective permission is the most restrictive of (their org role, their team role, any explicit
   user-level grant/deny), with an explicit user-level deny always taking precedence.
2. An org admin sets org-wide document access to "view only" following a compliance review.
3. The agent's permission-check function, when asked "can this user edit document X," queries only the
   user's team-level role, which still says "editor" from before the org-wide change -- it never checks
   the org-level override.
4. A user whose org-level access is now view-only successfully edits the document through the agent,
   because the cascade logic checked the wrong tier of the hierarchy.
5. The org-wide restriction intended to apply everywhere silently fails to propagate to any team that had
   a pre-existing team-level grant.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-level permission hierarchies (org/team/user or similar) are a common source of authorization bugs because most test suites cover only single-level scenarios | Common finding in permission-system code review |
| "Most restrictive wins" cascade logic is frequently implemented inconsistently across different tools that share the same underlying hierarchy | Typical pattern in agent tool-catalog audits |
| Centralizing cascade resolution into one shared, well-tested function removes most inconsistency-driven over-grants | Common remediation outcome |

## Mitigations
1. **Resolve effective permission through one shared function**: Implement a single, centrally-tested `resolve_effective_permission(user, resource)` that walks the full hierarchy, and require every tool to call it rather than reimplementing cascade logic.
2. **Explicitly define and test the combination rule**: Document whether the system uses most-restrictive-wins, most-permissive-wins, or explicit-override-wins, and add tests covering conflicting grants at each level.
3. **Invalidate cached effective permissions on any ancestor change**: When a permission changes at the org or team level, proactively invalidate any cached per-user effective-permission values instead of waiting for a TTL.
4. **Reject shortcut checks against a single hierarchy level**: In code review, flag any authorization check that queries only one level (e.g. only team role) for a resource governed by a multi-level hierarchy.
5. **Add hierarchy-change regression tests**: Specifically test that narrowing a parent-level permission correctly narrows access for children that previously had broader inherited access.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cascade_resolution_divergence | Cases where two different tools compute different effective permissions for the same user/resource pair | > 0 per day |
| stale_inherited_permission_count | Users whose effective permission still reflects a parent-level value that was since changed | > 0 after any org/team policy change |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Org-level restriction not propagated | A user retains broader access than the current org-level policy allows | Critical | Force cache invalidation, audit affected users, re-run cascade resolution |
| Cascade logic divergence between tools | Two tools disagree on effective permission for the same user/resource | High | Freeze the diverging tool, route all checks through the shared resolver |

## Related Patterns
- [Role Permission Mismatch](./role-permission-mismatch.md) - both concern the mapping from an intended permission model to the model actually enforced by the tool layer
- [Delegation Impersonation Not Limited](./delegation-impersonation-not-limited.md) - both involve authority that is supposed to narrow as it passes down a chain
- [Conditional Permission Logic](./conditional-permission-logic.md) - both are cases of incorrect evaluation logic producing an over- or under-grant
