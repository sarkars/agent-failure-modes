# Policy-Violating Action

## Issue: Agent does technically possible but disallowed action.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Audit finds policy mismatch.
- [Add more specific symptoms]

**Root Cause**
Agent does technically possible but disallowed action.

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
1. **Policy Engine Integration**: Before executing any action, query real-time policy engine with context: agent identity, action type, target resource, business context. Policy engine returns allow/deny/escalate decision. Action blocked on deny decision.
2. **Semantic Policy Validation**: Convert business policies into queryable rules (e.g., 'transfers > $10k require approval', 'cannot refund after 30 days', 'GDPR: customer data only accessed by resident team'). Validate action parameters against rules before execution. Store rules in version-controlled policy repository.
3. **Expert-Reviewed Policy Set**: Maintain policies in version-controlled repository with mandatory sign-off from domain experts (legal, compliance, business). Audit all policy changes. Implement policy staging environment for testing before production deployment.

### Detection & Response
1. **Policy Violation Logging**: Log every policy check with complete context: policy_id, agent_id, action_type, target_resource, decision (allow/deny), reason_code, timestamp, request_id. Store in dedicated policy audit log for compliance and incident investigation.
2. **Anomaly in Action Distribution**: Establish baseline of action types per agent per day (e.g., 'agent typically does 5 transfers, 10 refunds, 2 cancellations'). Flag agent exhibiting unusual action mix (e.g., suddenly performing 50 high-value transfers). Correlate with policy violation patterns.
3. **Policy Exception Pattern Detection**: Track denied actions by (agent, policy_id) tuple. Alert if same agent triggers same policy denial 5+ times in 1-hour window (potential systematic bypass attempt).

### Architecture Patterns
1. **Policy-as-Code Layer**: Implement policies as versioned, testable code (OPA/Rego or custom DSL). Deploy policy changes through CI/CD with mandatory tests. Enable policy rollback on errors. Policy evaluation is deterministic and auditable.
2. **Pre-Action Policy Gate Middleware**: Insert policy check middleware before all action execution. Gate queries policy engine, receives decision, logs result with high fidelity (decision tree path, matching rules, confidence scores). Fail-closed: no policy engine response = action blocked.
3. **Policy Audit Trail with Context Capture**: Maintain immutable log of policy checks with full context: agent_id, action, target, parameters, matching_policies[], decision, enforcement_action. Link to action execution logs for traceability. Enable post-incident analysis.

### Metrics
1. **policy_violations_per_hour**: Target: < 0.01; Alert threshold: > 0.05; Track: agent_id, policy_id, action_type
2. **policy_denial_rate_percent**: Target: < 0.1%; High denial rate indicates false positives
3. **policy_check_latency_p99_ms**: Target: < 100ms; Ensure policy engine doesn't slow actions
4. **agents_triggering_policy_denials_per_day**: Target: < 2; Identifies problematic agents
5. **policy_rule_accuracy_percent**: Target: > 99%; Measured via manual review sample of denials

### Alerts
1. **Policy Violation Blocked** (P2 - Warning): Condition - action blocked by policy rule. Action: Log to security audit, notify agent operator with policy violation reason, escalate if high-value action blocked.
2. **Policy Exception Pattern Detected** (P1 - Critical): Condition - agent triggers same policy denial 5+ times in 1-hour window. Action: Agent review triggered, investigate potential bypass attempt, potential suspension pending assessment.
3. **Policy Coverage Gap** (P2 - Warning): Condition - action matches no policy rule (coverage gap). Action: Alert compliance/security team, route to manual review, update policy set to close gap.

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

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
