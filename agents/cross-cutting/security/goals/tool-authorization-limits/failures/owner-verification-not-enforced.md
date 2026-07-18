# Owner Verification Not Enforced

## Issue
Before performing a mutating action on a specific resource (cancel this subscription, delete this file, update this profile), the agent authenticates that a valid user is making the request but never verifies that this specific user is the owner or authorized party for this specific resource. Any authenticated user can therefore direct the agent to mutate resources belonging to someone else simply by supplying that resource's identifier.

**Frequency**: Very Common

**Symptoms**
- The agent accepts a resource ID from user input and acts on it without cross-checking it against the requesting user's own resource list
- Two different users can reference the same numeric/UUID resource ID and both get it acted upon
- Tool functions take a `resource_id` parameter but no `requesting_user_id` ownership check inside the handler
- Support tickets where a user reports seeing or modifying data that isn't theirs, sourced from a chat/agent interaction rather than a UI bug
- Ownership checks exist for read operations but not for the corresponding write/delete operations on the same resource type

## Root Cause
This is a classic insecure direct object reference (IDOR) pattern transplanted into agentic tool-calling. Authentication (who is this user?) is often implemented and tested carefully, while authorization-per-resource (does this user own this specific object?) is assumed to be handled somewhere else in the stack — frequently it isn't, because the tool function was written to trust whatever identifier appears in the conversation or the LLM's generated arguments, rather than deriving the resource scope from the authenticated session.

## Example
```
1. A subscription-management agent has a tool cancel_subscription(subscription_id) used to let customers
   cancel their own plans through chat.
2. Subscription IDs are sequential integers, visible to a user in their own confirmation emails.
3. A user, out of curiosity or malice, tells the agent: "Please cancel subscription 48213" -- an ID that
   belongs to a different customer, not the one chatting.
4. The agent calls cancel_subscription(48213). The tool handler checks that the caller is a logged-in,
   authenticated user, and that subscription 48213 exists, but never checks that subscription 48213's
   owner_id matches the authenticated caller's user_id.
5. A different customer's active subscription is canceled by an unrelated user, with no ownership
   verification anywhere in the path.
```

## Statistics
| Finding | Context |
|---------|---------|
| Missing per-resource ownership checks (IDOR-class issues) are consistently among the most common vulnerability classes found in application security testing, and agent tool layers reproduce the same pattern | Well-established finding across web app security testing, applicable to agent tool handlers |
| Mutating operations (write/delete) are more likely to be missing ownership checks than read operations in the same codebase | Common finding in agent tool-handler audits |
| Deriving resource scope from the session rather than trusting caller-supplied IDs removes the large majority of these issues | Standard remediation for IDOR-class findings |

## Mitigations
1. **Scope queries to the authenticated user by default**: Fetch resources via `WHERE owner_id = session.user_id AND id = requested_id` rather than `WHERE id = requested_id` alone, so a non-owned ID simply returns not-found.
2. **Never trust caller-supplied IDs for authorization**: Treat any resource identifier appearing in agent input or LLM-generated tool arguments as untrusted; always re-derive or verify ownership server-side before acting.
3. **Apply ownership checks uniformly across the CRUD surface**: Ensure read, update, and delete handlers for a resource type all share the same ownership-check code path, rather than reimplementing it inconsistently.
4. **Return generic not-found rather than forbidden for non-owned resources**: Avoid confirming a resource's existence to non-owners, which also prevents enumeration of valid IDs.
5. **Add ownership-check tests to the tool test suite**: For every mutating tool, include a test where a valid, authenticated but non-owning user attempts the action and assert it is rejected.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cross_owner_mutation_attempts | Requests where the resource's owner_id differs from the authenticated caller's user_id | > 0 per hour |
| ownership_check_coverage | Fraction of mutating tool handlers with an automated ownership-check test | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-owner mutation succeeded | A mutating action executed against a resource not owned by the caller | Critical | Reverse the action if possible, notify affected owner, patch the handler |
| Tool handler missing ownership filter | Static analysis detects a mutating handler querying by resource ID alone | High | Block deploy until an ownership filter is added |

## Related Patterns
- [Conditional Permission Logic](./conditional-permission-logic.md) - both require the agent to correctly evaluate specific runtime facts about a resource before acting
- [Delegation Impersonation Not Limited](./delegation-impersonation-not-limited.md) - both concern the agent acting on behalf of the wrong party
- [Granular CRUD Permission Not Enforced](./granular-crud-permission-not-enforced.md) - complementary check: even for the correct owner, the allowed verb set must still be enforced
