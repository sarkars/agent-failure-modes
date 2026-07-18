# Orphaned Operations

## Issue: Operations Cannot Be Linked Back to Originating Request or Agent

**Frequency**: Occasional

**Symptoms**
- Database changes with unknown source
- API calls without request context
- Side effects disconnected from triggers
- Cannot attribute actions to users or agents
- Cleanup operations miss orphaned resources

**Root Cause**
As agents perform operations, context about why the operation was initiated gets lost. A database row is created, but there's no link to the agent session, user request, or task that triggered it. When issues arise or cleanup is needed, these orphaned operations cannot be traced back to their origin or associated with related operations.

**Example**
```
Database audit reveals 10,000 orphaned records:

Records found:
  temp_calculations table:
    - 10,000 rows
    - No session_id
    - No created_by
    - No request_id
    - Created over past 6 months

Questions:
  Q: "Which agent created these?"
  A: Unknown - no agent identifier
  
  Q: "Are these still needed?"
  A: Unknown - no link to active sessions
  
  Q: "Which user requests generated them?"
  A: Unknown - no request correlation
  
  Q: "Can we safely delete them?"
  A: Unknown - might break something

Investigation cost: 40 hours
Result: Deleted after 90-day quarantine
        Some turned out to be needed
        Customer-facing bug resulted

If properly linked:
  - Immediate: "These belong to completed session X"
  - Cleanup: Automatic after session end
  - Audit: Full trace to user request
```

**Key Statistics**
From Operations Research (2026):
- 20% of agent-created resources become orphaned
- Average orphan detection time: 30+ days
- Storage costs from orphans: 10-30% of total
- Security risk from untracked data: High
- Cleanup effort: 5-10x creation effort

**Orphan Types**
| Type | Example | Risk |
|------|---------|------|
| Data orphans | DB rows without session | Data leakage |
| Resource orphans | Cloud resources without tags | Cost waste |
| Process orphans | Background jobs without parent | Resource leak |
| File orphans | Temp files never cleaned | Storage waste |
| State orphans | Cache entries without TTL | Stale data |

**Contributing Factors**
- Correlation IDs not propagated
- Background operations lose context
- Async operations disconnect from requests
- Error paths skip cleanup
- No ownership metadata on resources

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent that writes intermediate results to a `temp_calculations` table during task execution, with no schema-enforced session_id, created_by, or request_id fields and no default TTL on the rows
- No correlation-ID propagation middleware links these writes back to the originating agent session or user request
- The agent has been running in production for 6 months, accumulating temp_calculations rows with every task execution
- A database audit is triggered by rising storage costs

### Trigger Mechanism
1. Over 6 months, the agent creates temp_calculations rows for every task, none tagged with session/request/creator metadata
2. A storage-cost audit discovers 10,000 orphaned rows in the table
3. Investigators attempt to determine which agent/session created each row and whether they're still needed, finding no correlation metadata to answer either question
4. After a 40-hour investigation, the team quarantines the rows for 90 days and then deletes them, only to discover some were still needed, causing a customer-facing bug

### Example Reproduction Steps
```
1. Query: SELECT COUNT(*) FROM temp_calculations WHERE session_id IS
   NULL AND created_by IS NULL AND request_id IS NULL -> 10,000
2. Investigator: "Which agent created these?" -> unknown, no
   identifier field populated
3. Investigator: "Are these still needed?" -> unknown, no link to
   active/completed sessions
4. After 40 hours of investigation and a 90-day quarantine, rows are
   deleted
5. Customer reports a broken feature -> traced back to a deleted
   temp_calculations row that was still referenced by an active
   long-running session
```

### Expected Failure State
10,000 rows accumulate with no way to attribute them to their originating session or request, costing 40 hours of investigation to even attempt an answer, and the eventual deletion breaks a customer-facing feature because some "orphaned" rows were actually still needed. A correctly instrumented system enforces a mandatory session_id/request_id on every temp_calculations write and applies a default TTL tied to session completion, so orphan accumulation and unsafe deletion never happen in the first place.

## Mitigation Strategies

### Prevention
1. **Mandatory correlation-ID propagation on every resource-creating operation**: Require every database write, background job, and temp-resource creation to carry the originating request_id and session_id as a schema-enforced field, not an optional column — the example's `temp_calculations` table having zero rows with session_id, created_by, or request_id across 10,000 records shows this wasn't optional in practice, it just wasn't enforced. Trade-off: adding mandatory correlation fields to every write path requires touching every resource-creation code path, which is significant retrofit work in an existing system.
2. **Default TTL enforcement on temporary resources**: Give every temporary/intermediate resource (like `temp_calculations` rows) a default expiration at creation time so orphaned records age out automatically rather than accumulating for 6 months before an audit discovers them. Trade-off: a default TTL can be wrong for legitimately long-lived temporary data, deleting something still needed if the TTL is set too aggressively — exactly the failure the example's "some turned out to be needed" outcome shows on the deletion side.
3. **Cleanup-on-completion tied to session/task lifecycle**: Automatically clean up (or explicitly archive with ownership intact) resources created during a session when that session completes, rather than leaving cleanup as a separate, easily-skipped step — the example's "if properly linked: cleanup automatic after session end" describes exactly the missing capability. Trade-off: automatic cleanup on session end needs to correctly distinguish resources that should outlive the session (durable outputs) from those that shouldn't (true temp data), which requires resource-type classification at creation time.

### Detection & Response
1. **Regular orphan-scan for resources missing correlation/ownership metadata**: Periodically query for resources lacking a request_id, session_id, or created_by field and treat any nonzero count as an active gap to close, rather than discovering the accumulation only during a 40-hour ad hoc audit as in the example.
2. **Resource creation-vs-cleanup rate monitoring**: Track the ratio of resources created versus resources cleaned up per resource type over time; a persistent gap (creation rate exceeding cleanup rate) is a leading indicator of the exact accumulation pattern that produced 10,000 orphaned records over 6 months.
3. **Orphan-accumulation trend tracking with proactive quarantine review**: Rather than waiting for storage costs or an audit to trigger investigation, track orphan count growth over time and review/quarantine on a rolling basis, avoiding the example's outcome where the eventual 90-day-quarantine deletion caused a customer-facing bug because some orphans "turned out to be needed."

### Architecture Patterns
1. **Correlation-ID propagation as shared middleware, not per-team convention**: Build request/session correlation-ID propagation into the shared framework/middleware layer that every service and background job uses by default, so it can't be silently skipped the way it evidently was for the `temp_calculations` writes. Deployment consideration: requires a single, consistently-adopted correlation mechanism across all services, including any legacy or third-party components that weren't built with this in mind.
2. **Resource-tagging-and-ownership registry**: Maintain a central registry mapping every created resource (DB rows, cloud resources, background jobs, temp files, cache entries) to its creating agent/session/request, queryable independently of the resource's own storage, so "which agent created these" and "can we safely delete them" are answerable without a 40-hour investigation. Deployment consideration: requires instrumenting every resource-creation path to register with the central system, adding a dependency to otherwise-simple write operations.
3. **Automated orphan detection and safe-quarantine pipeline**: Build a scheduled scan that identifies resources without correlation/ownership metadata, checks whether their originating session/request is still active, and moves genuinely orphaned resources to a reviewable quarantine (rather than either leaving them indefinitely or deleting outright), reducing both the storage-cost risk and the "some turned out to be needed" deletion risk. Deployment consideration: needs a safe, reversible quarantine mechanism and a defined review process so quarantined-then-needed resources can still be recovered before permanent deletion.

### Metrics
1. **unlinked_resource_rate**: % of newly created resources missing a correlation ID (request_id/session_id/created_by); target < 1%; alert if > 5%.
2. **orphan_accumulation_rate**: Net growth in orphaned resource count per month (creations minus cleanups for resources without ownership links); target ≈ 0; alert if sustained positive growth exceeds baseline for 2+ months.
3. **orphan_detection_latency**: Time between a resource becoming orphaned and being detected by a scan; target < 7 days; alert if > 30 days (matches the example's "average orphan detection time: 30+ days" baseline to beat).
4. **quarantine_recovery_rate**: % of quarantined-then-deleted resources later found to have been needed (customer-facing issues traced to deletion); target 0%; alert on any nonzero occurrence.

### Alerts
1. **Unlinked Resource Creation Detected** (P2): Condition — unlinked_resource_rate exceeds 5% for a resource type over a rolling week. Action: identify the code path creating resources without correlation IDs and patch it to enforce the mandatory field before more orphans accumulate.
2. **Orphan Accumulation Trend Confirmed** (P2): Condition — orphan_accumulation_rate shows sustained positive growth for 2+ months. Action: investigate the responsible resource-creation path, add TTL enforcement or session-based cleanup, and quarantine existing accumulated orphans for review.
3. **Post-Deletion Recovery Needed** (P1): Condition — quarantine_recovery_rate registers a nonzero event (a deleted orphan turns out to have been needed, causing a customer-facing issue). Action: treat as an incident; review and lengthen the quarantine window or improve ownership-linking so future deletions are safer, and restore the affected data if still possible.

## References

- [AWS: Resource Tagging Best Practices](https://docs.aws.amazon.com/tag-editor/latest/userguide/best-practices.html) - Resource tracking
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Correlation tracking
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Resource runaway
- [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/) - Distributed tracing
