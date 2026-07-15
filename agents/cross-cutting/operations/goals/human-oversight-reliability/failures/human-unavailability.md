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

## Mitigation Strategies

### Prevention
1. **Role-based approval with a defined backup chain**: Route approval requests to a role (VP of Engineering on-call, not "this specific VP") with a pre-configured ordered list of qualified backups, so a single person's weekend camping trip can't create a 25-hour blocking bottleneck. Trade-off: requires maintaining backup-approver rosters per role and ensuring backups are genuinely qualified, not just available.
2. **Severity-based escalation timeout, tuned for security-critical actions**: Set auto-escalation timeouts scaled to the action's urgency (an actively-exploited vulnerability should escalate in minutes, not wait through a full weekend) rather than relying on someone to manually notice and intervene, as the CEO ultimately did in the example. Trade-off: overly aggressive timeouts on lower-urgency actions increase noise and can undermine confidence in the escalation system if it fires too often.
3. **Defined emergency-bypass process for active-incident scenarios**: Pre-authorize a documented emergency approval path (who can invoke it, what actions it covers, what audit trail it requires) for situations like active exploitation, rather than leaving it to an ad hoc "CEO manually intervenes" response improvised under pressure. Trade-off: an emergency bypass is inherently a reduced-oversight path and needs strict scoping and post-hoc review to avoid becoming a routine shortcut.

### Detection & Response
1. **Approval-latency-by-approver tracking with availability correlation**: Monitor how long each approver takes to respond and correlate with calendar/out-of-office status, surfacing patterns like "this approver is the sole approver for a role and is frequently unavailable" before a critical patch gets stuck behind it.
2. **Coverage-gap reporting for weekends/holidays**: Explicitly report on which approval roles have no active coverage during off-hours windows, since the example's VP-only approval chain had exactly this gap and nobody had mapped it until the incident happened.
3. **Approaching-timeout alerting before the window closes**: Alert on a pending high-risk approval that's nearing its escalation timeout without a response, so a human can intervene proactively (say, Friday evening) rather than waiting for someone to notice 24+ hours in, as happened in the example.

### Architecture Patterns
1. **Role-based approval routing service, not person-based**: Build approval routing around roles/permission groups with an ordered on-call-style fallback list (similar to incident-response paging), so the routing layer itself guarantees a live human is always reachable for a given role. Deployment consideration: requires integrating with an on-call/paging system (e.g., PagerDuty-style rotation) rather than static person-to-approval mappings.
2. **Availability-aware pre-routing check**: Before sending an approval request, check the target approver's calendar/status and route directly to a backup if they're marked unavailable, instead of sending to an unavailable person and only escalating after a timeout. Deployment consideration: requires calendar/status API integration, which may not be available for every approver or every calendar system in use.
3. **Documented emergency-bypass workflow with mandatory post-hoc review**: Implement a formal emergency-approval mechanism (who can invoke, what it authorizes, automatic incident-ticket creation) so an emergency override is a designed control with an audit trail, not an improvised CEO intervention. Deployment consideration: needs clear governance on who can invoke it and mandatory retroactive review to prevent misuse.

### Metrics
1. **single_approver_bottleneck_count**: Number of approval roles with only one designated approver and no configured backup; target 0 for high-risk roles; alert if any critical role has zero backups.
2. **unavailability_caused_delay**: Median and p95 delay attributable to approver unavailability; target < 2 hours for critical actions; alert if p95 > 8 hours (the example's 25-hour delay is the failure case).
3. **weekend_holiday_coverage_gap_count**: Number of high-risk approval roles with no active coverage during off-hours windows; target 0; alert on any nonzero count for security-critical roles.
4. **emergency_bypass_invocation_rate**: Frequency of emergency-bypass use; track as a leading indicator of unresolved coverage gaps, not necessarily bad on its own, but investigate any spike.

### Alerts
1. **Critical Action Blocked by Unavailable Sole Approver** (P1): Condition — a security- or safety-critical approval is pending beyond a short threshold (e.g., 1 hour) with the designated approver marked unavailable and no backup configured. Action: page the emergency-bypass process immediately rather than waiting for manual escalation to happen organically.
2. **Coverage Gap on Critical Role Detected** (P2): Condition — weekend_holiday_coverage_gap_count is nonzero for a security-critical role. Action: require the role owner to configure a backup approver before the next off-hours window.
3. **Emergency Bypass Invoked** (P2): Condition — emergency_bypass_invocation_rate registers any event. Action: trigger mandatory post-hoc review of the bypass justification and use it as input to fix the underlying coverage gap that necessitated it.

## References

- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human oversight availability
- [PagerDuty: On-Call Best Practices](https://www.pagerduty.com/resources/learn/on-call-best-practices/) - Coverage patterns
- [NIST: Business Continuity](https://csrc.nist.gov/publications/detail/sp/800-34/rev-1/final) - Availability planning
- [SOC 2: Availability](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) - Control availability
