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

**Mitigation Strategies**
1. **Capability registry**: Register all agent actions with risk rating
2. **Mandatory approval review**: New features require approval assessment
3. **Default-deny**: Unknown actions require approval
4. **Aggregate gates**: Approval based on cumulative impact
5. **Approval audits**: Regular review of action-to-approval coverage
6. **Semantic matching**: Detect action variants that should require approval

**Detection**
- Audit action types vs. approval coverage
- Monitor for new action types without gates
- Track high-impact actions without approval
- Alert on disabled approval gates
- Compare action semantics to known risky patterns

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Authorization gaps
- [NIST: Access Control](https://csrc.nist.gov/publications/detail/sp/800-162/final) - Action authorization
- [OWASP: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) - Missing controls
- [SOC 2 Compliance](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) - Control requirements
