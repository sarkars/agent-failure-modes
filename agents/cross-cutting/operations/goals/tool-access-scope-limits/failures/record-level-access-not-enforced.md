# Record-Level Access Not Enforced

## Issue
An agent is correctly granted access to a tool or table in general — it's allowed to call "get ticket" or "list documents" — but the underlying implementation doesn't check whether the specific record being requested actually belongs to, or is otherwise authorized for, the requesting user or context. Because the tool-level grant is real and the agent is "supposed" to be able to use this tool, the missing per-record ownership check is easy to overlook: every individual call looks legitimate, and only in aggregate does it become clear the agent can read (and sometimes write) any record in the table, not just the ones it should.

**Frequency**: Very Common

**Symptoms**
- Agent can retrieve a record by ID (e.g., ticket #4821) that belongs to a different user than the one it's operating on behalf of, simply by referencing the ID
- No error or access-denied response occurs for out-of-scope record requests — the tool returns the record as if access were normal
- Ownership/ACL columns exist in the record schema (e.g., `owner_id`, `assigned_team`) but the tool's query never filters or checks against them
- The issue is discovered via enumeration testing (incrementing an ID) rather than through a specific user complaint
- Different tools built against the same table enforce record-level checks inconsistently — one filters by owner, another doesn't

## Root Cause
Authorization is frequently modeled and tested at the level of "can this principal call this tool/endpoint at all," which is the layer most access-control frameworks and API gateways operate on by default. Record-level (sometimes called object-level or instance-level) authorization requires an additional check comparing the specific requested record's ownership/ACL metadata against the requester's identity, and that check has to be implemented inside the tool's business logic rather than at the gateway — a step that's easy to skip, especially when the underlying data store makes any valid ID trivially queryable regardless of ownership.

## Example
```
A project-management agent is granted general access to the "tasks" API
so it can help users manage their own to-do items. The tasks API
supports `get_task(task_id)`, which was implemented as a straightforward
primary-key lookup: fetch the row where `id = task_id`, no additional
filter.

A user asks the agent, "what's the status of task 9214?" — a task ID
they saw referenced in a shared Slack channel but don't actually own or
have visibility into per the product's sharing rules. The agent calls
`get_task(9214)`, and the tool happily returns the full task record,
including its description and any private comments, because the only
check performed was "is this agent allowed to call get_task at all,"
which it is — there's no secondary check verifying task 9214 belongs to
or is shared with the requesting user.
```

## Statistics
| Finding | Context |
|---------|---------|
| Broken object-level authorization is consistently ranked among the top API security risks in industry vulnerability classifications (e.g., OWASP API Security Top 10) | Well-established finding across API security research |
| ID-enumeration-based record access is one of the most commonly exploited classes of vulnerability in bug bounty programs for API-backed products | Common in public bug bounty disclosure data |
| Record-level authorization gaps are disproportionately found in internally-built or auto-generated CRUD APIs, where a scaffolding tool creates lookup-by-ID endpoints without owner-scoping by default | Typical of framework-generated API layers |

## Mitigations
1. **Mandatory ownership check on every record-returning call**: Require every tool that fetches a record by ID to compare the record's ownership/ACL fields against the requester's identity before returning data, with no code path that skips this check.
2. **Scoped queries instead of ID-only lookups**: Change the underlying query pattern from "fetch by ID" to "fetch by ID and requester scope" (e.g., `WHERE id = ? AND owner_id = ?`), so an unauthorized ID simply returns no result rather than requiring a separate post-fetch check that might be forgotten.
3. **Automated ID-enumeration testing**: Run regular automated tests that attempt to access record IDs known to belong to other users/accounts, treating any successful unauthorized fetch as a release-blocking failure.
4. **Centralized authorization middleware**: Implement record-level checks once in a shared middleware or ORM-level policy layer applied to all record-returning queries, rather than leaving each tool author to reimplement the check.
5. **Access-denial auditing over silent success**: Log and monitor rejected out-of-scope record requests as a leading indicator of enumeration attempts or missing checks elsewhere in the system.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `out_of_scope_record_return_count` | Count of returned records whose ownership/ACL metadata doesn't match the requester | Alert threshold: > 0 (any occurrence) |
| `id_enumeration_test_pass_rate` | Pass rate of automated tests attempting unauthorized record access via ID enumeration | Alert threshold: < 100% |
| `unscoped_query_pattern_count` | Count of record-fetch queries missing an ownership/scope predicate | Alert threshold: > 0 for any new tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Out-of-Scope Record Access | A record is returned to a requester whose identity doesn't match its ownership/ACL fields | P1 | Halt the tool path, patch the missing check, audit recent logs for the extent of exposure |
| Enumeration Test Failure | Automated ID-enumeration test successfully retrieves an unauthorized record | P1 | Block release, add the missing ownership predicate before deploy |

## Related Patterns
- [Record Ownership Not Validated](./record-ownership-not-validated.md) - the write-path counterpart: this pattern covers reads, that one covers updates/writes without an ownership check
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - a related gap one level down in granularity, restricting fields rather than whole records
- [Access Control Inheritance Wrong](./access-control-inheritance-wrong.md) - over-broad inherited scope often compounds with missing record-level checks to produce this failure
