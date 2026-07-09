# No Approval Boundary

## Issue: Unclear which actions require human approval.

**Frequency**: Common

**Symptoms**
- Inconsistent HITL decisions across use cases.
- [Add more specific symptoms]

**Root Cause**
Unclear which actions require human approval.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Explicit Action-to-Approval Matrix**: Enumerate every action class the agent can take (read, write, send, refund, delete, external API call, etc.) and assign each a required approval mode (auto-approve, human-in-loop, human-in-command) before the agent is deployed. Store this matrix as versioned config, not tribal knowledge, so no action ships without a defined boundary.
2. **Default-to-Approval for Unclassified Actions**: Configure the agent runtime so that any action not explicitly present in the approval matrix fails closed and routes to human review by default, rather than defaulting to auto-execute. This removes the ambiguity that causes inconsistent HITL decisions for edge-case or newly introduced tools.
3. **Approval Boundary Review at Tool Onboarding**: Require every new tool or capability added to the agent to go through a checklist step that assigns it an approval tier before it is wired into the agent's toolset, blocking deployment until the classification is signed off by the risk/product owner.

### Detection & Response
1. **HITL Consistency Monitoring**: Log every action alongside its applied approval mode, and run periodic analysis grouping by action type to detect cases where the same action class was sometimes auto-approved and sometimes routed to a human. Inconsistency above a threshold triggers a matrix review.
2. **Unclassified Action Detection**: Monitor for any executed action whose type does not match an entry in the current approval matrix. Since these should fail closed, any occurrence indicates either a matrix gap or a bypass, both of which warrant investigation.
3. **Approval Override Tracking**: Track every instance where a human overrides the default routing (approves something flagged for auto-execute-only, or bypasses a required approval). Spikes in override frequency for a given action type signal the matrix is miscalibrated and needs updating.

### Architecture Patterns
1. **Policy-as-Code Approval Gateway**: Implement a gateway service that intercepts every agent action before execution, looks up the action type in the versioned approval matrix, and routes to auto-execute, a human approval queue, or hard block accordingly. The agent has no direct execution path that bypasses this gateway.
2. **Approval Matrix Version Control**: Store the action-to-approval mapping in a git-backed config with required review on changes, so boundary changes are auditable, diffable, and revertible like code.
3. **Human Approval Queue with SLA**: Route human-in-loop actions to a dedicated queue (ticketing system or dashboard) with visibility into pending count and age, ensuring approval requests don't silently stall the agent or get rubber-stamped under time pressure.

### Metrics
1. **unclassified_action_rate_percent**: Target: 0%; Alert threshold: > 0% of executed actions lack a matrix entry
2. **hitl_consistency_score_percent**: Target: 100% (same action type always gets same routing); Alert threshold: < 98%
3. **approval_override_rate_percent**: Target: < 2% of routed actions; Alert threshold: > 5%
4. **avg_approval_queue_wait_time_minutes**: Target: < 15 min for time-sensitive actions; Alert threshold: > 60 min

### Alerts
1. **Unclassified Action Executed** (P1 - Critical): Condition - agent executed an action type with no entry in the approval matrix. Action: Halt further executions of that action type, page on-call, require emergency matrix classification before resuming.
2. **HITL Routing Inconsistency Detected** (P2 - Warning): Condition - same action type routed differently across 3+ consecutive occurrences within a day. Action: Freeze matrix entry, escalate to risk owner for clarification.
3. **Approval Queue Backlog** (P3 - Info): Condition - pending human approvals exceed SLA wait time. Action: Notify approval queue owner, consider temporary reviewer reassignment.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
