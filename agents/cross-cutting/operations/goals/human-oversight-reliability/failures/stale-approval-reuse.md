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

## Mitigation Strategies

### Prevention
1. **Context binding to specific parameters, not the action category**: Store the approval as scoped to "deploy v2.1.0" specifically, not the generic "deployment" action, so a version bump to v2.1.1 doesn't inherit an approval that was never actually granted for it — this directly targets the example's root cause, where "approval scope was implicitly v2.1.0 but stored as deployment." Trade-off: finer-grained scoping means more frequent re-approval requests for iterative workflows, which can feel like friction to teams used to blanket sign-off.
2. **Approval fingerprinting via context hash**: Hash the material context of the approved action (version, code diff hash, amount, environment) at approval time, and require the hash to still match at execution time or trigger re-approval — would have caught the Tuesday hotfix merge changing the code content even though the "deployment" label stayed the same. Trade-off: requires defining what counts as "material" context precisely enough that trivial changes (e.g., a timestamp) don't force unnecessary re-approval churn.
3. **Change-triggered re-approval on any code/content diff, not just version-string bumps**: Treat any merged change since the original approval — including a hotfix that doesn't bump a major version identifier — as invalidating the prior approval, closing the gap where "no re-approval requested (same 'deployment' action)" let a materially different artifact ship under an old sign-off. Trade-off: needs reliable diff/change detection between the approved artifact and the one about to be deployed, which adds pipeline complexity.

### Detection & Response
1. **Current-context-to-approval-context comparison at execution time**: Before executing an approved action, re-derive the current context (version, amount, environment) and compare it against what was actually approved, rejecting or re-routing the action if they don't match — the exact check that would have stopped v2.1.1 from deploying under a v2.1.0 approval.
2. **"Would have been denied" rate tracking on reused approvals**: For approvals that get reused across a context change, retroactively check whether the approver would have denied the request had they seen the actual current context (in the example, the lead developer "unaware of v2.1.1 changes" would likely have caught the regression) — this quantifies real harm from stale-approval reuse, not just its frequency.
3. **Approval reuse pattern monitoring**: Track how often a single approval token/state gets referenced across multiple distinct executions, since legitimate one-time approvals being invoked repeatedly is itself a signal of scope-creep risk even before a concrete incident occurs.

### Architecture Patterns
1. **Explicit-scope approval records instead of boolean approval state**: Store approvals as structured records of exactly what was approved (specific version, specific amount, specific environment) rather than a simple "approved: true" flag attached to an action type, making the object of "what was actually approved" queryable and enforceable. Deployment consideration: requires migrating existing boolean-style approval storage to a structured schema, which touches every approval-consuming workflow.
2. **Fingerprint-based automatic invalidation service**: Build a shared service that computes and stores a context fingerprint at approval time and automatically invalidates the approval when a fresh fingerprint computed at execution time doesn't match, rather than relying on each individual workflow to remember to check. Deployment consideration: needs a canonical, deterministic way to fingerprint each action type's material context, which varies by domain (code diff hash vs. dollar amount vs. environment tag).
3. **Combined time-based and change-based expiry**: Expire approvals on whichever comes first — an elapsed-time TTL or a detected material context change — rather than time-based expiry alone, since the example's approval was still within any reasonable time window (one day) when it was misapplied to a changed artifact. Deployment consideration: change-based expiry requires the fingerprinting/diff infrastructure above; without it, only the weaker time-based half is enforceable.

### Metrics
1. **stale_approval_reuse_rate**: % of executed actions using an approval whose recorded context doesn't match current context; target < 1%; alert if > 5%.
2. **would_have_been_denied_rate**: % of reused approvals that, on retroactive review, the original approver would have denied given the actual current context; target < 5%; alert if > 20% (baseline research cites 42%, the failure state to avoid).
3. **context_fingerprint_mismatch_rate**: % of execution attempts where the context fingerprint doesn't match the approval-time fingerprint; target < 2%; alert if > 10%.
4. **approval_scope_specificity_rate**: % of approval records storing explicit scoped parameters (vs. a generic action-type boolean); target 100%; alert if < 80%.

### Alerts
1. **Context Fingerprint Mismatch at Execution** (P1): Condition — an action is about to execute using an approval whose fingerprint doesn't match current context. Action: block execution and force re-approval before proceeding; do not allow override without explicit approver sign-off on the new context.
2. **High-Impact Stale Approval Reuse Detected** (P1): Condition — stale_approval_reuse_rate spikes for a high-risk action category (deployments, financial transactions). Action: halt the affected pipeline, retroactively review recently executed actions under stale approvals, and require re-approval for anything still reversible.
3. **Would-Have-Been-Denied Rate Elevated** (P2): Condition — would_have_been_denied_rate exceeds 20% over a rolling month. Action: tighten context-binding granularity for the affected approval type and review recent incidents traceable to reused approvals.

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Authorization failures
- [OWASP: API Security](https://owasp.org/API-Security/) - Token and authorization patterns
- [Google: Zanzibar Authorization](https://research.google/pubs/pub48190/) - Contextual authorization
