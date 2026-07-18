# Granular CRUD Permission Not Enforced

## Issue
A role is defined with fine-grained access — e.g. "read-only" or "can create tickets but not delete them" — but the tool wrapper the agent calls exposes the underlying API's full create/read/update/delete surface regardless of which operations the role is actually meant to permit. The agent, having no operation-level gate in the tool itself, can invoke update or delete through a tool nominally scoped to a narrower capability.

**Frequency**: Common

**Symptoms**
- A single tool function (e.g. `manage_ticket`) accepts an `action` parameter that includes create/update/delete, even though the calling role is provisioned as create-only
- Read-only roles can successfully trigger writes because the "read" tool actually wraps a generic CRUD client library with no operation filtering
- Permission is enforced at the UI layer (grayed-out buttons) but the same backend endpoint the agent calls has no equivalent server-side operation check
- Incident review shows a delete or update action executed by a role whose documented permission set doesn't include that verb
- Tool descriptions say "for viewing X" but the tool's actual implementation passes through arbitrary CRUD calls to the underlying API

## Root Cause
Tool wrappers are often built by directly exposing a convenient underlying SDK or REST client to the LLM, then relying on the tool's name and docstring to imply a narrower purpose than the code actually allows. Because the LLM's understanding of "you should only read" is a soft, prompt-level constraint rather than a hard-coded restriction on which HTTP verbs or SDK methods the tool function is allowed to call, any tool built as a thin passthrough over a full-CRUD client silently grants the union of everything that client can do.

## Example
```
1. A knowledge-base agent is granted a "contributor" role, meant to allow creating new articles but not
   editing or deleting existing ones written by other authors.
2. The tool exposed to the agent, update_kb_article, is implemented as a thin wrapper around the
   knowledge-base SDK's generic article.save() method, which handles both creates and updates
   depending on whether an ID is passed.
3. A user asks the agent to "fix a typo in the onboarding doc," which was authored by someone else.
4. The agent calls update_kb_article with the existing article's ID, and the SDK wrapper executes an
   update against a role that is only supposed to have create permission.
5. The contributor role successfully modifies content it should never have been able to touch, because
   the tool wrapper never checked which CRUD verb the underlying call represented against the role's
   allowed operation set.
```

## Statistics
| Finding | Context |
|---------|---------|
| Thin passthrough tool wrappers over general-purpose SDKs are a common source of over-broad CRUD access in agent tool catalogs | Common finding in tool-permission audits |
| Read-only or create-only roles retaining incidental write/delete access is frequently discovered only during incident response, not design review | Typical pattern in agent security postmortems |
| Splitting CRUD verbs into separate, individually-scoped tool functions removes most over-broad-access incidents of this type | Common remediation outcome |

## Mitigations
1. **One tool function per CRUD verb**: Expose separate, narrowly-scoped tools (`create_article`, `read_article`) rather than one generic tool that branches internally on create/update/delete.
2. **Enforce operation-level checks server-side**: Validate the role's allowed verb set inside the tool handler (or the API it calls) before executing, independent of which tool name the agent invoked.
3. **Reject generic passthrough wrappers in tool review**: In tool-catalog review, flag any tool implemented as a thin wrapper over a full-CRUD SDK client without an explicit operation allow-list.
4. **Test each role against the full CRUD matrix**: For every role, write automated tests asserting that disallowed verbs (e.g. delete for a create-only role) are rejected by the tool layer, not just hidden in the UI.
5. **Log the resolved CRUD verb per tool call**: Record which actual operation (create/read/update/delete) each tool invocation performed, so audits can catch verb-role mismatches after the fact.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| crud_verb_role_mismatch_count | Tool calls where the executed CRUD verb isn't in the caller role's allowed set | > 0 per day |
| passthrough_tool_verb_coverage | Number of distinct CRUD verbs a single tool function can trigger | > 1 per tool (flag for review) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Disallowed write by scoped role | Create-only or read-only role executes an update/delete verb | Critical | Block the call, roll back if applied, review the tool's implementation |
| New tool registered spanning multiple CRUD verbs | CI detects a tool function capable of more than one CRUD verb without per-verb role checks | Warning | Block merge until split or gated |

## Related Patterns
- [Read Only Agent Write Access](./read-only-agent-write-access.md) - the specific, most common instance of this pattern where read-only access silently includes write capability
- [Role Permission Mismatch](./role-permission-mismatch.md) - both describe a gap between the intended permission model and what the tool layer actually enforces
- [Admin Operation Called By Non-Admin](./admin-operation-called-by-non-admin.md) - same root cause (missing server-side enforcement) applied at the role tier instead of the operation-verb level
