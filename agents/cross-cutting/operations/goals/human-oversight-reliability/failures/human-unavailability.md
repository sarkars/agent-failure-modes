# Human Unavailability

## Issue: No Fallback When Required Approver Is Unavailable

**Frequency**: Common

**Symptoms**
- Tasks blocked waiting for unavailable approver
- No delegation or escalation path
- Single point of failure in approval chain
- Weekend/holiday gaps in approval coverage
- Critical actions delayed for hours/days

**Root Cause**
Approval workflows are designed assuming approvers are always available. When the designated approver is on vacation, sick, in a meeting, or simply not checking notifications, tasks requiring approval are indefinitely blocked. Systems lack fallback approvers, escalation paths, or mechanisms to detect and route around unavailability.

**Example**
```
Scenario: Production deployment requiring VP approval

Friday 5:00 PM:
  Agent: "Critical security patch ready for production"
  Required approver: VP of Engineering
  Approval sent: ✓
  
Friday 5:30 PM:
  VP status: Left for weekend camping trip
  Phone: No service
  Delegation: None configured
  
Saturday 10:00 AM:
  Security team: "Vulnerability being actively exploited"
  Patch status: Awaiting approval
  VP status: Still unreachable
  Escalation path: None defined

Saturday 6:00 PM:
  CEO manually intervenes
  Emergency override used
  Patch deployed
  
Impact:
  - 25-hour delay on critical security fix
  - Active exploitation during window
  - 3 systems compromised
  - Incident response activated
  
Root cause:
  - No backup approver for VP
  - No escalation after X hours
  - No emergency approval process
  - Weekend coverage not planned
```

**Key Statistics**
From Operations Research (2026):
- 52% of organizations have single-approver bottlenecks
- Average unavailability-caused delay: 8-24 hours
- 34% of critical approvals blocked by unavailability
- Only 28% have defined backup approvers
- Weekend/holiday delays cost $50K+ per incident

**Unavailability Scenarios**
| Scenario | Duration | Mitigation |
|----------|----------|------------|
| Meeting | 1-2 hours | Wait or escalate |
| End of day | 12-16 hours | After-hours coverage |
| Vacation | Days to weeks | Delegation required |
| Sick leave | Unpredictable | Backup approvers |
| Terminated | Permanent | Role-based approval |

**Contributing Factors**
- Person-based rather than role-based approval
- No delegation mechanism
- No unavailability detection
- Missing escalation timeouts
- No emergency bypass process

**Mitigation Strategies**
1. **Role-based approval**: Approve by role, not individual
2. **Backup approvers**: Define fallback for each approver
3. **Delegation**: Allow temporary delegation with audit trail
4. **Escalation timeouts**: Auto-escalate after N hours
5. **Availability detection**: Check calendar/status before routing
6. **Emergency process**: Defined bypass for critical situations

**Detection**
- Track approval latency by approver
- Monitor for repeated unavailability
- Alert on approaching timeout without response
- Audit single-approver bottlenecks
- Report on coverage gaps (weekends, holidays)

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight availability
- [PagerDuty: On-Call Best Practices](https://www.pagerduty.com/resources/learn/on-call-best-practices/) - Coverage patterns
- [NIST: Business Continuity](https://csrc.nist.gov/publications/detail/sp/800-34/rev-1/final) - Availability planning
- [SOC 2: Availability](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) - Control availability
