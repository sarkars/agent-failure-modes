# AI Agent Misses an Industry-Specific Rule or Exception: Causes and Fixes

## Issue: The agent applies the general-case policy and misses an industry-specific rule or exception, producing a wrong decision.

**Frequency**: Common

**Symptoms**
- Wrong decision under domain policy.
- Agent applies the general-case rule where an industry-specific exception clearly applied.
- Compliance or legal review flags a decision as violating a rule that was never encoded in the agent's reasoning or rule engine.

**Root Cause**
Domain rules exist as tribal knowledge and scattered policy documents rather than a queryable, versioned rule engine, so exceptions — jurisdiction-specific carve-outs, product-specific windows — are never systematically captured alongside the general rule they modify. Because the agent has no "rule uncertain" signal that would trigger escalation, and no review cadence exists to catch rule-set gaps before they cause repeated wrong decisions, the agent defaults to whichever general rule it does have encoded, silently and confidently, even when an exception it was never given clearly applies.

**Example**
```
An insurance-claims agent processes a claim under the standard 30-day filing
window, denying a claim filed on day 35. It misses the state-specific
exception that extends the filing window to 60 days for claims involving a
hospitalization, because that exception was never encoded in the agent's
rule set — only the general policy was. The denial is later overturned by a
regulator, and the insurer faces a compliance finding for improperly denied
claims across the affected state.
```

**Contributing Factors**
- Domain rules exist as tribal knowledge or scattered documents rather than a queryable, versioned rule engine.
- Jurisdiction- or product-specific exceptions are not systematically captured alongside the general rule.
- No domain-expert review cadence to catch rule set gaps before they cause repeated wrong decisions.
- Agent has no mechanism to flag "rule uncertain" and escalate rather than defaulting to the general case.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Known jurisdictional exception applies | Claim filed day 35, state grants 60-day hospitalization exception | Agent applies exception, approves claim | Agent applies general 30-day rule, denies claim |
| No matching rule found | Novel case not covered by any encoded rule | Agent escalates to domain expert rather than guessing | Agent invents a plausible-sounding but unverified rule application |
| Conflicting rules | Two applicable rules give different outcomes | Agent applies documented conflict-resolution priority or escalates | Agent silently picks one rule without following resolution strategy |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| domain_rule_coverage_eval_percent | 100% | % of eval decision types with a corresponding rule in the rule engine |
| domain_rule_violation_rate_eval_percent | < 0.5% | % of eval decisions that don't match the applicable rule per domain-expert review |

---

Fixing this means moving domain exceptions into a queryable, versioned rule engine instead of leaving them as tribal knowledge.

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
| domain_rule_violation_rate_percent | > 1% |
| rule_exception_invocation_rate_percent | outside domain-specific baseline |
| rule_coverage_percent | < 100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Domain Rule Violation | Decision doesn't match applicable rule from rule engine | Warning |
| Exception Abuse Pattern | Agent invokes exceptions 3+ times/week or > 20% of decisions | Warning |
| Rule Conflict Unresolved | Multiple conflicting rules apply and resolution fails | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
