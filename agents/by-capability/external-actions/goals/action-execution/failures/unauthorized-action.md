# Unauthorized Action

## Issue: Agent performs an action without permission.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Action trace lacks user/admin authorization.
- [Add more specific symptoms]

**Root Cause**
Agent performs an action without permission.

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
1. **Capability-Based Security Model**: Implement a capability token system where agents are only granted explicit permissions for specific actions on specific resources. Use signed tokens (JWT) with role claims that verify both agent identity and action scope, with mandatory token rotation every 24hrs.
2. **Multi-Stage Authorization Gates**: Require both pre-action policy checks (does agent have permission for this action type?) and runtime authorization verification (does agent have permission for this target resource?). Implement tiered approval system where sensitive actions (delete, modify critical fields) require explicit user/admin approval before execution.
3. **Namespace Isolation with Tenant Checks**: Ensure agents operate within bounded namespaces with automatic tenant/resource ownership validation. Each action must verify the target resource belongs to the authorized scope. Reject cross-tenant actions at enforcement layer.

### Detection & Response
1. **Authorization Audit Logging**: Log all action attempts with complete context: actor identity, target resource, requested action type, authorization decision (allow/deny), decision reason, timestamp, request ID. Store in immutable audit log with tamper detection. Alert on write-once violations.
2. **Real-Time Authorization Failure Detection**: Monitor authorization_failure_count metric in 1-minute windows. Trigger alert if count > 0 (zero-tolerance). Track unique agents initiating failures per hour. Escalate to security team on any failure.
3. **Behavioral Anomaly Detection**: Establish per-agent baseline of action attempts per hour. Flag 3σ+ deviation from baseline as potential privilege escalation or attack. Correlate failed auth attempts with time-of-day, source IP, tool invocations for pattern detection.

### Architecture Patterns
1. **Action Interceptor Pattern**: Place authorization layer between agent and action execution. All tool invocations route through security gate that validates permission (check capability token + resource scope) before delegating to actual tool. Fail-closed: no capability token = rejected.
2. **JWT-Based Capability Tokens**: Use cryptographically signed JWT tokens encoding: agent_id, allowed_actions[], resource_scopes[], expiry_time. Validate token signature and expiry on every action. Implement token revocation list for emergency access denial.
3. **Immutable Audit Journal**: Append-only log of all authorization decisions with transaction ID, actor, resource_id, action, decision, denial_reason, timestamp. Use cryptographic hashing to detect tampering. Enable compliance audits.

### Metrics
1. **authorization_failures_per_hour**: Baseline 0.0; Alert threshold: > 0.1; Target: < 0.01 (1 failure per 100 hours)
2. **unauthorized_action_attempts_per_day**: Target: 0 (any unauthorized attempt is critical); Track: count, actor, target, time
3. **action_authorization_latency_p99_ms**: Target: < 50ms; Monitor: token validation overhead doesn't impact agent performance
4. **agents_with_failed_auth_unique_per_day**: Target: 0; Identifies compromised/misconfigured agents
5. **authorization_check_coverage_percent**: Target: 100%; Verify every action validated before execution

### Alerts
1. **Authorization Failure Detected** (P1 - Critical): Condition - authorization_failures_per_hour > 0 OR single failed auth attempt. Action: Immediate audit log review, isolate agent from executing new actions, notify security team within 5min, initiate incident response.
2. **Privilege Escalation Attempt** (P1 - Critical): Condition - agent attempts action 3+ times outside its authorized scope within 1-hour window. Action: Immediate agent suspension, comprehensive security audit of agent history, notify resource owner, potential threat intelligence analysis.
3. **Authorization Bypass Pattern** (P1 - Critical): Condition - same agent fails auth on same resource 5+ times in 1-hour window. Action: Rate-limit agent action throughput, escalate to security, implement additional manual approval gates, analyze attack patterns.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
