# Domain Rule Miss

## Issue: Agent misses industry-specific rule or exception.

**Frequency**: Common

**Symptoms**
- Wrong decision under domain policy.
- [Add more specific symptoms]

**Root Cause**
Agent misses industry-specific rule or exception.

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
1. **Domain Rule Engine Integration**: Implement rule engine (e.g., Drools, OPA) with comprehensive domain rules. Rules encoded as: IF [conditions] THEN [decision]. Each rule has: description, priority, exception_conditions, owner (domain expert). Agent queries rule engine before making domain-specific decision.
2. **Expert-Reviewed Rule Set**: All domain rules must be reviewed and signed off by domain experts (legal, compliance, subject matter experts). Rules version-controlled with change history. Annual audit of rule accuracy. Rules tested against case law, regulatory guidance, precedents.
3. **Exception Handling Framework**: Define explicit exception paths for edge cases. Example: 'Standard refund policy is 30 days, BUT exception for defective products = 60 days, AND exception for VIP customers = 90 days'. Encode exceptions as rules with priority ranking.

### Detection & Response
1. **Rule Violation Detection**: Monitor all domain decisions. For each decision, verify it matches applicable rule from rule engine. Log: decision_id, applied_rules[], decision, alignment_status. Alert on misalignment.
2. **Expert Audit Sampling**: Randomly audit 5-10% of decisions per week (stratified by decision type). Domain expert rates each as correct/incorrect per domain rules. Track accuracy by decision type and agent.
3. **Rule Exception Pattern Detection**: Track when exceptions are invoked. Alert if agent invokes exceptions at unusually high rate (indicates potential rule circumvention) or low rate (indicates under-utilization of exceptions).

### Architecture Patterns
1. **Decision Audit Trail with Rule Binding**: For each decision, log: input_context, queried_rule_engine, matching_rules[], selected_rule_id, decision, rationale, timestamp. Link to actual decision in outcome logs.
2. **Rule Change Impact Analysis**: Before deploying new/modified rules, analyze impact (which prior decisions would have been different?). Test against historical decision logs. Ensure changes align with business intent.
3. **Rule Conflict Resolution Framework**: When multiple rules apply (conflicts), define resolution strategy (priority ranking, human escalation, weighted voting). Log conflict resolution for learning.

### Metrics
1. **domain_rule_violation_rate_percent**: Target: < 0.5%; Alert threshold: > 1%; Track: rule_id, violation_type, agent
2. **expert_audit_agreement_rate_percent**: Target: > 95%; Domain experts agree with agent decision
3. **rule_exception_invocation_rate_percent**: Target: 2-5% (domain-specific); Alert if outside range
4. **rule_coverage_percent**: Target: 100%; All decision types covered by rules
5. **rule_accuracy_by_type_percent**: Target: > 98%; Measured via expert audit

### Alerts
1. **Domain Rule Violation** (P2 - Warning): Condition - decision doesn't match applicable rule from rule engine. Action: Log violation, notify domain expert, potential decision reversal, rule review.
2. **Exception Abuse Pattern** (P2 - Warning): Condition - agent invokes exceptions 3+ times per week or > 20% of decisions. Action: Agent review, potential rule refinement, domain expert audit.
3. **Rule Conflict Unresolved** (P1 - Critical): Condition - multiple conflicting rules apply and resolution fails. Action: Escalate to domain expert, manual decision, rule conflict resolution update.

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

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
