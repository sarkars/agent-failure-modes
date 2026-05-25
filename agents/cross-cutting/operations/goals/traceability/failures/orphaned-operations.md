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

**Mitigation Strategies**
1. **Correlation IDs**: Propagate request ID through all operations
2. **Resource tagging**: Tag all created resources with origin
3. **Ownership tracking**: Record creating agent/session
4. **TTL enforcement**: Default expiration on temporary resources
5. **Cleanup on completion**: Automatic resource cleanup
6. **Orphan detection**: Regular scans for unlinked resources

**Detection**
- Query for resources without correlation IDs
- Scan for data without ownership metadata
- Monitor resource creation vs. cleanup rates
- Track orphan accumulation over time
- Alert on unattributed operations

## References

- [AWS: Resource Tagging Best Practices](https://docs.aws.amazon.com/tag-editor/latest/userguide/best-practices.html) - Resource tracking
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Correlation tracking
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Resource runaway
- [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/) - Distributed tracing
