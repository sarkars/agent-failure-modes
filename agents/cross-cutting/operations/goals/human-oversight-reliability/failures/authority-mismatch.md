# Authority Mismatch

## Issue: Wrong Person Approves Action

**Frequency**: Occasional

**Symptoms**
- Approvals from unauthorized personnel
- Junior staff approving senior-level decisions
- Cross-department approvals without authority
- Approval delegation to unqualified parties
- Rubber-stamp approvals from disinterested parties

**Root Cause**
Approval workflows route requests to people who lack the authority, expertise, or context to make informed decisions. A database deletion request goes to a frontend developer. A $50,000 purchase gets approved by an intern with system access. Approval authority is often based on system permissions rather than organizational authority, leading to technically valid but organizationally inappropriate approvals.

**Example**
```
Scenario: IT change management agent

Change request:
  Action: Modify production database schema
  Risk level: High
  Required approver: Database administrator or higher
  
Routing logic:
  Find user with "database" in role title
  Check: Has system access to approve
  
Request routed to:
  Name: Junior Database Analyst
  Role: "Database" in title ✓
  System access: Can click "approve" ✓
  Actual authority: Entry-level, 2 weeks on job
  
Approval granted:
  "Looks fine to me" - clicked approve
  
Result:
  - Schema change deployed
  - Broke 3 dependent applications
  - 2-hour production outage
  
Post-incident findings:
  - Analyst didn't understand implications
  - Senior DBA was on vacation
  - System didn't verify seniority or expertise
  - No escalation for high-risk changes
```

**Key Statistics**
From Authorization Research (2026):
- 31% of approvals come from people without domain expertise
- 47% of organizations don't verify approver authority level
- "Any manager" approval policies cover 62% of workflows
- 23% of approval denials are overridden by unauthorized parties
- Authority verification adds 15 minutes but prevents 40% of issues

**Authority Mismatch Types**
| Type | Example | Risk |
|------|---------|------|
| Seniority | Intern approves executive decision | Uninformed approval |
| Domain | Frontend dev approves backend change | Missing expertise |
| Department | Marketing approves engineering change | Wrong context |
| Delegation | Approver delegates to assistant | Authority dilution |
| Conflict | Requester approves own request | Self-dealing |

**Contributing Factors**
- Permission-based routing (has access vs. has authority)
- Generic "manager approval" without specialization
- No expertise verification
- Vacation/absence coverage by unqualified staff
- Approval fatigue leading to delegation

## Mitigation Strategies

### Prevention
1. **Authority matrix keyed to role and seniority, not title substring match**: Replace routing logic like "find user with 'database' in role title" with an explicit matrix mapping each action's risk level to specific qualifying roles/seniority tiers — this directly closes the example's gap, where a "Junior Database Analyst" title-matched into a request that required a senior DBA. Trade-off: requires maintaining an accurate, up-to-date org/role mapping as staff and titles change, which drifts if not actively owned.
2. **Tenure/expertise gate for high-risk approvals**: For high-risk changes, require a minimum verified tenure or a demonstrated expertise credential (not just system access) before a user can be routed as an approver — would have excluded the 2-weeks-on-the-job analyst in the example regardless of title match. Trade-off: needs a maintained expertise/tenure record per employee, and rigid tenure cutoffs can wrongly exclude a genuinely qualified newer hire.
3. **Escalation-on-absence instead of silent fallback to whoever's available**: When the properly-authorized approver (senior DBA) is unavailable, escalate to another qualified senior approver rather than letting the routing logic fall through to whoever else technically has "database" in their title and system access. Trade-off: requires a defined backup chain of equally-qualified approvers, which not every organization has depth to staff.

### Detection & Response
1. **Approver-to-action domain/seniority alignment audit**: Continuously check whether the approver who granted each decision actually matches the required domain and seniority tier for that action type, flagging mismatches like a junior analyst approving a production schema change after the fact if not caught beforehand.
2. **Junior-staff high-risk approval rate tracking**: Specifically monitor what fraction of high-risk approvals are granted by staff below a seniority threshold; a nonzero rate for schema-change-tier actions is a direct signal the routing logic (not just this one incident) is broken.
3. **Post-incident authority root-cause tagging**: When an incident follows an approval (as the 2-hour outage followed the analyst's approval), explicitly tag whether an authority mismatch contributed, building a dataset that quantifies how often "technically valid but organizationally inappropriate" approvals correlate with bad outcomes.

### Architecture Patterns
1. **Role-based access control layered with an authority-verification service**: Separate "has system permission to click approve" from "has organizational authority to approve this specific action," with the approval system calling an authority-verification service before accepting a decision — implements the matrix as enforced infrastructure, not just documented policy. Deployment consideration: requires integrating with HR/org-chart systems as the source of truth for seniority and domain, which may not be readily API-accessible.
2. **Self-dealing and delegation-chain guards**: Build explicit checks that block a requester from approving their own request and cap how far delegation can chain (e.g., no more than one hop, and only to someone at equal-or-higher authority) before a request routes to a human. Deployment consideration: needs consistent identity linkage between requester and potential approver across systems to detect self-dealing reliably.
3. **Vacation/absence-aware routing with qualified backups only**: Integrate calendar/absence status into routing so that when a primary approver is out, the system routes only to pre-designated, equally-qualified backups rather than defaulting to "anyone with matching title and access." Deployment consideration: requires maintaining a backup-approver list per authority tier, which needs active upkeep as staff change roles.

### Metrics
1. **authority_mismatch_rate**: % of approvals granted by someone below the required seniority/domain tier for that action; target < 2%; alert if > 10%.
2. **junior_staff_high_risk_approval_rate**: % of high-risk approvals granted by staff below a defined seniority threshold; target 0%; alert on any nonzero rate for the highest risk tier.
3. **self_approval_rate**: % of approvals where requester and approver are the same person or a flagged related party; target 0%; alert on any occurrence.
4. **post_approval_incident_correlation**: % of production incidents traceable to an approval later found to be an authority mismatch; target < 1%; alert if this exceeds 5% of incidents in a quarter.

### Alerts
1. **Junior/Unqualified Approver on High-Risk Action** (P1): Condition — junior_staff_high_risk_approval_rate registers a nonzero event for a high-risk action type. Action: immediately hold or roll back the approved change if still reversible, and require re-approval by a qualified senior approver.
2. **Self-Approval Detected** (P1): Condition — self_approval_rate registers any occurrence. Action: block the action if not yet executed; if executed, escalate for mandatory retroactive review and treat as a compliance/segregation-of-duties incident.
3. **Authority Mismatch Rate Trending Up** (P2): Condition — authority_mismatch_rate exceeds 10% over a rolling month. Action: audit the routing logic (likely a title-matching pattern like the example's) and replace with the explicit authority matrix.

## References

- [NIST: Access Control Guidelines](https://csrc.nist.gov/publications/detail/sp/800-162/final) - Authority and access control
- [SOX Compliance](https://www.sec.gov/spotlight/sarbanes-oxley.htm) - Segregation of duties
- [MAST Taxonomy](https://arxiv.org/abs/2503.01893) - Multi-agent authorization failures
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight
