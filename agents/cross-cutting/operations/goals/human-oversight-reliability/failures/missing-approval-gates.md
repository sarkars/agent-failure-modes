# Missing Approval Gates

## Issue: Workflow Lacks Required Approval Step for High-Risk Action

**Frequency**: Common

**Symptoms**
- High-risk actions execute without any approval request
- New action types bypass existing approval flows
- Edge cases fall outside approval requirements
- Approval gates removed or disabled
- Composite actions avoid per-component approval

**Root Cause**
Workflows are designed with approval gates for known high-risk actions, but new actions or edge cases slip through without gates. As systems evolve, new capabilities are added without corresponding approval requirements. Composite actions may execute multiple risky sub-actions without triggering approval for any individual component. Approval logic may be disabled for "efficiency" or testing and never re-enabled.

**Example**
```
Scenario: Data management agent with partial approval coverage

Original design (2024):
  - DELETE single record: No approval (routine)
  - DELETE > 100 records: Requires approval
  - EXPORT data: Requires approval
  
New feature added (2025):
  - ARCHIVE records: Moves to cold storage
  - Implemented as: Move + mark inactive
  - Approval requirement: Not added (oversight)
  
Incident:
  Agent: "Archive all records older than 2020"
  Records affected: 2.3 million
  Approval requested: None (ARCHIVE not in approval list)
  
Result:
  - 2.3M records moved to cold storage
  - 47 active customer accounts affected
  - Data retrieval took 3 days
  - Customer complaints: 23
  
Root cause:
  - ARCHIVE was effectively DELETE but without approval
  - New action type bypassed approval matrix
  - No review process for new capabilities
  - Impact threshold not evaluated
```

**Key Statistics**
From Workflow Research (2026):
- 38% of high-risk actions lack approval gates
- 56% of new features ship without approval review
- Average time to add approval after incident: 2 days
- 42% of approval gaps discovered via incidents
- Composite actions bypass gates in 67% of cases

**Gap Categories**
| Category | Example | Detection |
|----------|---------|-----------|
| New actions | Feature added without gate | Capability audit |
| Renamed actions | DELETE → ARCHIVE | Semantic analysis |
| Composite actions | Loop of small actions | Aggregate tracking |
| Disabled gates | Testing mode in prod | Config audit |
| Threshold gaps | $9,999 avoiding $10K gate | Boundary analysis |

**Contributing Factors**
- Approval requirements not updated with features
- No mandatory approval review for new capabilities
- Approval logic in code, not configuration
- Test/dev bypass not removed
- Missing aggregate impact assessment

## Mitigation Strategies

### Prevention
1. **Mandatory approval review as a feature-launch gate**: Require every new agent capability to go through an explicit approval-requirement assessment before shipping, rather than launching and discovering the gap after an incident — ARCHIVE shipped in 2025 as "Move + mark inactive" without anyone evaluating that it was functionally DELETE-equivalent. Trade-off: adds a review step to feature development that can slow time-to-ship for genuinely low-risk features.
2. **Default-deny for unregistered action types**: Any agent action not explicitly registered with a risk rating and approval requirement is blocked or forced through approval by default, rather than silently executing because it "wasn't in the approval list" — this directly inverts the example's failure mode where ARCHIVE bypassed the matrix simply by not being in it. Trade-off: can block legitimate new low-risk actions until they're formally registered, adding friction to rapid iteration.
3. **Semantic equivalence matching against known risky patterns**: Detect when a new action's actual effect (data becomes inaccessible/moved, records marked inactive) semantically matches an already-gated risky pattern (DELETE) even if it has a different name — would have flagged ARCHIVE as DELETE-equivalent despite the rename. Trade-off: semantic matching is imprecise and needs human judgment to avoid over-flagging genuinely different actions that happen to share surface similarity.

### Detection & Response
1. **Action-type-to-approval-coverage audit**: Regularly enumerate every registered agent action and check it against the approval matrix, surfacing any action (like ARCHIVE) with no corresponding approval requirement before it's exercised at scale.
2. **High-impact-action-without-approval monitoring**: Track actions that affect large volumes of records or resources (2.3 million records in the example) and flag any such action that executed without an approval request, regardless of its declared risk category.
3. **Aggregate/cumulative-impact tracking for composite actions**: Monitor cumulative effect across repeated small actions (a loop of single-record operations) that individually stay under an approval threshold but combine into a large-scale change, since composite actions bypass gates in a majority of cases per the pattern's own statistics.

### Architecture Patterns
1. **Capability registry with mandatory risk rating**: Maintain a central registry every agent action must be declared in, including an explicit risk rating and approval requirement, so "new action ships without approval review" becomes structurally impossible rather than a process that can be skipped. Deployment consideration: requires enforcing registry declaration in the deployment pipeline (e.g., a CI check that blocks shipping an undeclared action), not just a documentation convention.
2. **Aggregate-impact gate independent of per-action thresholds**: Add a gate that evaluates cumulative impact across an entire task/session (total records touched, total value moved) regardless of whether any individual action cleared its own threshold, closing the composite-action bypass. Deployment consideration: requires tracking running totals across a task's full execution, which is more state to maintain than per-call threshold checks.
3. **Config-as-code with drift detection for approval gates**: Keep approval-gate configuration in version-controlled config (not ad hoc code toggles) with automated drift detection that alerts if a gate is disabled and not re-enabled within an expected window, addressing the "disabled for testing and never re-enabled" failure mode. Deployment consideration: requires migrating any inline/hardcoded approval logic to the config system, which is a refactor for legacy workflows.

### Metrics
1. **action_approval_coverage_rate**: % of registered agent actions with an explicit, current approval-requirement rating; target 100%; alert if < 95%.
2. **unregistered_action_execution_count**: Count of agent actions executed that aren't in the capability registry at all; target 0; alert on any nonzero count.
3. **composite_action_bypass_rate**: % of high-cumulative-impact task executions that completed without triggering an aggregate-impact approval gate; target < 5%; alert if > 20% (baseline research cites 67%, which is the failure state to avoid).
4. **disabled_gate_duration**: Time an approval gate remains disabled (e.g., for testing) before either re-enabling or being flagged; target < 24 hours; alert if > 72 hours.

### Alerts
1. **Unregistered Action Executed** (P1): Condition — unregistered_action_execution_count registers any event. Action: immediately halt further execution of that action type pending registration and risk assessment; review the impact of the already-executed instance.
2. **High-Impact Action Without Approval** (P1): Condition — an action affecting more than a defined volume/value threshold (e.g., >100K records or equivalent to the 2.3M-record archive) executes without a logged approval request. Action: treat as an incident; assess reversibility and customer impact immediately, and add the action to the approval matrix before it can run again.
3. **Approval Gate Left Disabled** (P2): Condition — disabled_gate_duration exceeds 72 hours. Action: escalate to the gate owner to confirm whether disabling was intentional and permanent (requiring a formal policy change) or an oversight requiring immediate re-enablement.

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Authorization gaps
- [NIST: Access Control](https://csrc.nist.gov/publications/detail/sp/800-162/final) - Action authorization
- [OWASP: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) - Missing controls
- [SOC 2 Compliance](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) - Control requirements
