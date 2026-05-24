# Stale Approval Reuse

## Issue: Agent Uses Old Approval for New or Changed Context

**Frequency**: Occasional

**Symptoms**
- Actions executed using approval from different context
- Approval granted for X, used for Y
- Time-sensitive approvals used after expiry
- Approval scope creep over iterations
- Cached approvals bypass current review

**Root Cause**
Approval tokens or states are cached and reused beyond their intended scope. An approval for "deploy version 1.2" gets reused for "deploy version 1.3". An approval for "$1,000 budget" gets reused when the budget increases. Approvals may have implicit expiry (context changed) but systems track only explicit expiry (time elapsed). This allows agents to proceed on stale authorizations that no longer reflect human intent.

**Example**
```
Scenario: Code deployment agent with approval caching

Initial approval:
  Request: "Deploy v2.1.0 to staging"
  Approver: Lead developer
  Approval: "Approved for staging deployment"
  Timestamp: Monday 9:00 AM

Tuesday - Code changes:
  - Hotfix merged for critical bug
  - Version now v2.1.1
  - No re-approval requested (same "deployment" action)

Agent reasoning:
  "Deployment already approved on Monday"
  "This is same type of action"
  "Approval still valid"
  
Result: v2.1.1 deployed without review

Post-incident:
  - Hotfix introduced regression
  - Lead developer unaware of v2.1.1 changes
  - Would have caught issue in review
  - Staging environment broken for 6 hours
  
Root cause:
  - Approval was for specific version, reused for different version
  - No invalidation when code changed
  - Approval scope was implicitly "v2.1.0" but stored as "deployment"
```

**Key Statistics**
From Approval Research (2026):
- 34% of organizations cache approvals beyond intended scope
- 56% of approval systems don't track what specifically was approved
- Average staleness before reuse detection: 2-5 days
- 42% of reused approvals would have been denied if re-requested
- Scope creep occurs in 28% of iterative workflows

**Staleness Dimensions**
| Dimension | Example | Detection |
|-----------|---------|-----------|
| Time | Approval from last week | TTL expired |
| Version | Approved v1, used for v2 | Version mismatch |
| Scope | Approved $100, used for $500 | Threshold exceeded |
| Context | Approved for test, used in prod | Environment mismatch |
| Entity | Approved for user A, used for B | Identity mismatch |

**Contributing Factors**
- Approval stored as boolean, not as scope
- No context hash to detect changes
- Time-based expiry only (no context-based)
- Approval inheritance across iterations
- No re-approval triggers on material changes

**Mitigation Strategies**
1. **Context binding**: Bind approval to specific parameters, invalidate on change
2. **Approval fingerprinting**: Hash context, require re-approval if hash changes
3. **Explicit scope**: Store what was approved, not just that it was approved
4. **Automatic expiry**: Time-based and change-based expiration
5. **Re-approval triggers**: Material changes require new approval
6. **Approval audit trail**: Track what approval was originally for

**Detection**
- Compare current context to approval context
- Alert on approvals used after context change
- Monitor approval reuse patterns
- Track "would have been denied" rate on reused approvals
- Audit approval scope vs. actual action scope

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Authorization failures
- [OWASP: API Security](https://owasp.org/API-Security/) - Token and authorization patterns
- [Google: Zanzibar Authorization](https://research.google/pubs/pub48190/) - Contextual authorization
