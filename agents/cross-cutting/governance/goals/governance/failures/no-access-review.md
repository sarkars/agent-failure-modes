# No Access Review

## Issue: Agent permissions are not periodically reviewed.

**Frequency**: Common

**Symptoms**
- Stale credentials/permissions remain active.
- Departed employees' or decommissioned agents' credentials remain active with full scope.
- Permission scope grows monotonically over time as new tools are added but old ones are never revoked.
- Security audits discover agents holding access to systems no longer relevant to their current task.

**Root Cause**
Agent permissions are not periodically reviewed.

**Example**
```
Agent "vendor-onboarding-bot" was granted write access to the finance ERP
system 18 months ago to auto-create vendor records during a one-time
migration project. The migration ended after 3 weeks, but the credential
was never revoked.

Month 14: The finance team rotates its ERP access policy and runs a
routine credential audit. They discover vendor-onboarding-bot still holds
standing write access, unused for over a year, with no owner able to
explain why.

Security investigation reveals: the agent's API key was never scoped to
expire, no recertification process exists, and the original requester
left the company 8 months prior. The stale credential is flagged as a
potential attack surface during the next penetration test.
```

**Contributing Factors**
- Credentials/permissions are provisioned with no default expiration, so they persist indefinitely absent manual revocation.
- No scheduled recertification cadence exists to force owners to re-justify standing access.
- Access requests are approved as one-off exceptions without linking to the task/project they support, making it hard to tell later whether the grant is still needed.
- Ownership of a granted credential is not tracked, so when the original requester leaves or changes roles, nobody is positioned to revoke it.
- Security teams lack visibility into the full inventory of agent credentials across all integrated systems, so audits are manual and infrequent.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Expired credential enforcement | A credential passes its 90-day expiry without recertification | Access is auto-revoked and a ticket is opened | Credential remains active past expiry with no revocation |
| Orphaned owner detection | Owner of a granted credential departs the company (simulated HR event) | Credential is flagged and quarantined within 24h | Credential remains fully active with no flag raised |
| Recertification prompt delivery | Grant approaches its review date | Owner receives a recertification task via the configured workflow tool | No recertification prompt is sent; grant silently continues |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| stale_grant_detection_rate | 100% | Seed a test registry with grants unused for 30+ days and verify the scanner flags all of them |
| recertification_prompt_delivery_rate | 100% | Verify every grant approaching its review date generates a recertification task in the test harness |
| auto_revocation_accuracy | 100% | Confirm grants that miss their recertification deadline are auto-revoked without affecting still-valid grants |

---

## Mitigation Strategies

### Prevention
1. **Time-Boxed Credential Expiry**: Issue all agent credentials, API keys, and tool-scoped permissions with mandatory expiration dates (e.g., 90 days for standing access, 24 hours for elevated/break-glass access). Renewal requires an explicit recertification request routed to the resource owner, so access silently ages out instead of persisting by default.
2. **Quarterly Access Recertification Workflow**: Run a scheduled recertification campaign where each agent's grants (tools, data scopes, downstream system credentials) are listed against the owner's actual current use case, and the owner must affirmatively re-approve, downscope, or revoke each one. Auto-revoke any grant not recertified by the deadline.
3. **Least-Privilege Provisioning at Grant Time**: Require every new agent permission request to specify the task it supports and a default expiry; deny open-ended "just in case" scopes. Pair this with a permissions catalog that maps each scope to the business justification on file, so reviewers aren't reconstructing intent from scratch.

### Detection & Response
1. **Stale Grant Scanner**: Run a nightly job comparing each active credential/permission against its last-used timestamp and expiry date. Flag any grant unused for 30+ days or past its recertification date, and auto-generate a revocation ticket assigned to the owner.
2. **Orphaned Access Detection**: Cross-reference the agent permission registry against the employee/team roster and project inventory; flag grants tied to a decommissioned agent, a departed owner, or a sunset project. These are the highest-risk stale grants because no one is watching them.
3. **Privilege Drift Alerting**: Diff each agent's currently granted scopes against its declared least-privilege baseline. Alert when actual grants exceed baseline (privilege creep) so security can investigate whether the excess was ever justified or just never cleaned up.

### Architecture Patterns
1. **Centralized Permission Registry**: Maintain a single source of truth (e.g., an IAM/PAM system or internal service) mapping agent_id → granted_scope → owner → grant_date → expiry_date → last_used_at. All agent tool/API access is issued and checked against this registry rather than embedded in per-integration config.
2. **Automated Recertification Pipeline**: A scheduled service queries the registry for grants approaching their review date, opens a recertification task in the owner's workflow tool (ticketing/Slack), and enforces auto-expiry if no response is received within the SLA window.
3. **Just-In-Time Access Broker**: For high-sensitivity scopes, replace standing grants with a broker that issues short-lived credentials on request, tied to a specific task and automatically expiring at task completion, eliminating the need to review dormant standing access at all.

### Metrics
1. **stale_grant_count**: Target: 0; Alert threshold: > 0 grants unused for 30+ days
2. **recertification_completion_rate_percent**: Target: 100% within SLA window; Alert threshold: < 95%
3. **avg_grant_age_days**: Target: < 90 days for standing access; Alert threshold: > 180 days
4. **orphaned_grant_count**: Target: 0; Alert threshold: > 0 grants tied to decommissioned agents/departed owners

### Alerts
1. **Recertification Deadline Missed** (P1 - Critical): Condition - grant passes its recertification deadline without owner action. Action: Auto-revoke the grant, notify owner and security, log revocation in audit trail.
2. **Orphaned Grant Detected** (P2 - Warning): Condition - active grant tied to a decommissioned agent or departed owner. Action: Quarantine the credential, escalate to security for manual revocation review.
3. **Privilege Drift Detected** (P3 - Info): Condition - agent's active scopes exceed its declared least-privilege baseline. Action: Flag for owner review at next recertification cycle, no auto-revocation.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| stale_grant_count | > 0 grants unused for 30+ days |
| recertification_completion_rate_percent | < 95% |
| avg_grant_age_days | > 180 days |
| orphaned_grant_count | > 0 grants tied to decommissioned agents/departed owners |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Recertification Deadline Missed | Grant passes recertification deadline without owner action | Critical |
| Orphaned Grant Detected | Active grant tied to decommissioned agent or departed owner | Warning |
| Privilege Drift Detected | Agent's active scopes exceed declared least-privilege baseline | Info |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
