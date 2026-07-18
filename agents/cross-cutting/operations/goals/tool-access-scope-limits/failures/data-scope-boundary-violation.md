# Data Scope Boundary Violation

## Issue
An agent scoped to operate within a specific business boundary — a department, project, or team — issues a tool query that crosses into a sibling boundary it was never intended to see, because the boundary is a soft, business-logic construct rather than a hard constraint enforced at the tool layer. Unlike multi-tenant or workspace isolation, these boundaries usually live inside a single shared database and account, distinguished only by a filter (e.g., `department = 'Engineering'`) that the application is expected to apply consistently but doesn't always.

**Frequency**: Common

**Symptoms**
- Agent scoped to one project or department returns records tagged to a different one in the same organization
- The offending query is syntactically valid and returns real data — no error is raised, so the violation goes unnoticed until reviewed
- Boundary violations increase after new tools or query paths are added that reuse existing data models without re-adding the department/project filter
- Filters that enforce the boundary exist in some code paths (e.g., the UI) but not others (e.g., a newer agent tool built against the same underlying API)
- Employees in one department report seeing data "helpfully" surfaced by an assistant that belongs to a different team's project

## Root Cause
Departmental or project boundaries are typically modeled as an attribute on shared records (a `department_id` or `project_id` column) rather than as a structural partition like a separate database or tenant. Enforcement therefore depends on every single query path remembering to add the corresponding `WHERE` clause or equivalent filter. Agent tools, especially those built by composing existing internal APIs or by giving an LLM broad query-building capability (e.g., natural-language-to-SQL), frequently omit or under-apply this filter because it isn't a structural constraint the underlying data layer enforces on its own.

## Example
```
An internal analytics agent lets employees ask natural-language questions
that get translated into SQL against a shared "projects" database.
Access is intended to be scoped so that an agent invoked from within the
"Consumer Product" team's workspace only queries records where
`department = 'Consumer Product'`.

A user in Consumer Product asks the agent, "which projects are behind
schedule and by how much?" The agent's natural-language-to-SQL step
generates a query against the `projects` table ordered by schedule
variance, but the department filter is applied only as a prompt
instruction ("only discuss Consumer Product projects") rather than as a
hard WHERE clause in the generated SQL. The LLM, optimizing for a
complete and helpful answer, omits the filter in some generated queries,
and the agent surfaces schedule-variance details for the "Enterprise
Platform" team's confidential project timeline, which the Consumer
Product user was never meant to see.
```

## Statistics
| Finding | Context |
|---------|---------|
| Boundary-enforcement gaps are disproportionately found in natural-language-to-query agent architectures compared to fixed-parameter APIs, since the filter logic is generated rather than hardcoded | Common finding in NL-to-SQL agent deployments |
| A large share of internal-boundary violations are discovered through user reports rather than automated detection, since the query itself is syntactically valid and produces no error | Typical of soft-boundary architectures |
| Boundary violations correlate strongly with the introduction of new agent tools that reuse an existing shared data model without re-implementing its filtering logic | Common pattern in tool-sprawl incidents |

## Mitigations
1. **Structural boundary enforcement**: Where feasible, move critical boundaries from a soft filter attribute to a structural partition (separate schema, view, or row-level security policy) so the boundary is enforced by the data layer itself, not by every query author remembering to apply it.
2. **Mandatory row-level security policies**: For boundaries that must remain attribute-based, implement database-level row-level security keyed to the requester's department/project context so even a query missing the filter is constrained by the database engine.
3. **Query-generation guardrails**: For natural-language-to-query agents, inject the boundary filter programmatically into the generated query after generation (not just as a prompt instruction), and reject any generated query that doesn't include the expected filter clause.
4. **Cross-boundary result auditing**: Sample agent tool responses and verify every returned record's boundary attribute matches the requester's declared scope, flagging any mismatch for review.
5. **Boundary-filter regression testing**: Add automated tests for every new tool built against a shared data model that assert boundary filtering is present and effective before the tool ships.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `boundary_mismatch_record_count` | Count of returned records whose department/project attribute doesn't match the requester's scope | Alert threshold: > 0 (any occurrence) |
| `unfiltered_generated_query_rate` | Share of NL-to-query generations missing the expected boundary filter clause | Alert threshold: > 0.5% of generations |
| `new_tool_boundary_test_coverage` | Share of newly shipped tools against shared data models with a passing boundary-filter regression test | Alert threshold: < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-Boundary Record Return | A returned record's boundary attribute doesn't match the requester's scope | P2 | Review the query path, add or fix the missing filter, notify affected teams if sensitive |
| Missing Filter in Generated Query | Query-generation guardrail detects a generated query lacking the boundary clause | P2 | Block the query, log the generation for prompt/guardrail tuning |

## Related Patterns
- [Account-Level Data Scope](./account-level-data-scope.md) - the same failure mode at tenant/account granularity instead of department/project
- [Workspace Isolation Bypass](./workspace-isolation-bypass.md) - a related boundary-crossing failure in multi-workspace systems
- [Record-Level Access Not Enforced](./record-level-access-not-enforced.md) - boundary violations often co-occur with missing per-record ownership checks
