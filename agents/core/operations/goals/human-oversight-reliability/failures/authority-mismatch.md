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

**Mitigation Strategies**
1. **Authority matrix**: Map actions to required approver roles explicitly
2. **Expertise verification**: Check domain expertise, not just access
3. **Seniority requirements**: High-risk actions require senior approval
4. **Delegation controls**: Limit who can delegate approval authority
5. **Conflict detection**: Prevent self-approval or related-party approval
6. **Authority audit**: Regularly review who is approving what

**Detection**
- Track approver-to-action domain alignment
- Monitor junior staff approval rates
- Alert on approvals outside normal authority
- Audit delegation chains
- Compare approver expertise to action complexity

## References

- [NIST: Access Control Guidelines](https://csrc.nist.gov/publications/detail/sp/800-162/final) - Authority and access control
- [SOX Compliance](https://www.sec.gov/spotlight/sarbanes-oxley.htm) - Segregation of duties
- [MAST Taxonomy](https://arxiv.org/abs/2503.01893) - Multi-agent authorization failures
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight
