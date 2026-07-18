# Field-Level Access Not Restricted

## Issue
A table or record type has some fields an agent should be permitted to see (e.g., order status, ticket subject) and others it shouldn't (e.g., internal margin, a customer's raw payment token), but the access-control system was built to grant or deny access at the record level only. Once an agent is authorized to read a record at all, every field on it — including the ones that were never meant to be exposed to that agent or context — comes along for free, because there's no enforcement point that operates below record granularity.

**Frequency**: Very Common

**Symptoms**
- Agent authorized to view "customer support tickets" also returns internal-only fields like agent notes, escalation flags, or cost data attached to the same record
- Permission model documentation distinguishes "viewable" from "internal" fields, but the API/tool response includes both once record-level access is granted
- Field-level exposure is discovered ad hoc, usually by someone reading raw tool output rather than by a policy check catching it
- The same record type is served with different field sets by different tools, because field filtering is implemented inconsistently per integration rather than centrally
- Removing a field from agent exposure requires a code change per tool rather than a policy update, because there's no shared enforcement layer

## Root Cause
Access control is most naturally modeled at the level of an authorization check on an entity (can this principal read this record?), and many permission frameworks — role-based access control (RBAC) systems especially — stop there because record-level checks are simpler to reason about and audit. Extending the same rigor to individual fields requires either a field-level permission matrix or a response-shaping layer applied after the record-level check passes, and that additional layer is frequently skipped or only partially implemented, leaving the full record object as the default response shape.

## Example
```
A recruiting agent is granted access to the "candidates" table so it can
answer scheduling and status questions for hiring managers. The table
includes fields like `name`, `interview_stage`, and `status`, which
hiring managers should see, alongside `recruiter_private_notes`,
`salary_expectation`, and `background_check_result`, which are meant to
stay visible only to recruiters and HR.

The access-control layer checks only whether the requesting hiring
manager (via the agent) is authorized to view the candidate record at
all — which they are, since they're on the hiring panel — and returns
the full row. When a hiring manager asks the agent "what's the status of
this candidate," the agent's tool call retrieves the entire record,
including `recruiter_private_notes` and `salary_expectation`, and the
agent's response synthesis has no way to know those fields were meant to
be withheld, so it may reference them directly if asked a follow-up
question.
```

## Statistics
| Finding | Context |
|---------|---------|
| Field-level access gaps are among the most common findings in access-control audits of systems that only implement RBAC at the object/record level | Common in enterprise permission-model reviews |
| Systems retrofitted with agent tooling frequently expose more fields to agents than the equivalent human-facing UI did, because the UI's field-level rendering logic isn't reused by the API layer the agent calls | Typical of agent-tooling rollouts on top of legacy record-level ACL systems |
| A significant share of "unintended field exposure" incidents are resolved by adding response-shaping filters rather than by database or storage changes, indicating the data was never actually protected below the record boundary | Common remediation pattern |

## Mitigations
1. **Field-level permission matrix**: Define an explicit per-role, per-field visibility matrix independent of record-level access, and enforce it as a mandatory response-shaping step after every record-level check passes.
2. **Default-deny response shaping**: Build tool responses from an explicit allowlist of fields per caller role rather than returning the full record object and trying to strip disallowed fields after the fact — allowlisting fails safe, denylisting doesn't.
3. **Centralized response-shaping layer**: Implement field filtering once in a shared middleware or serialization layer used by every tool that reads the record type, rather than per-tool, to eliminate inconsistent field sets across integrations.
4. **Schema-level field tagging**: Tag each field in the schema with its minimum required role/clearance, and have the response-shaping layer read that tag automatically rather than relying on each tool author to hardcode the field list.
5. **Automated field-exposure diffing**: Continuously compare the fields present in raw storage against the fields present in each tool's response, flagging any newly added storage field that isn't yet classified and filtered.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unfiltered_field_exposure_count` | Count of responses containing a field outside the caller's field-level allowlist | Alert threshold: > 0 (any occurrence) |
| `tool_response_field_set_variance` | Number of distinct field sets returned for the same record type across different tools | Alert threshold: > 1 for a single record type without documented justification |
| `unclassified_new_field_count` | Count of schema fields with no field-level classification tag | Alert threshold: > 0 for any field reachable by an agent tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Restricted Field in Response | A tool response includes a field tagged above the caller's clearance | P1 | Patch the response-shaping filter immediately, review recent conversation logs for exposure |
| New Field Missing Classification | A newly added schema field reaches an agent tool without a field-level classification | P2 | Block exposure pending classification review |

## Related Patterns
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - a specific case where the unrestricted field is a known-sensitive one like salary or health status
- [Masked Field Unmasking](./masked-field-unmasking.md) - a related failure where a field-level control exists but is bypassed rather than absent
- [Data Classification Access Not Enforced](./data-classification-access-not-enforced.md) - the same enforcement gap at record/document granularity instead of field granularity
