# Wrong Workflow Branch

## Issue: Agent chooses refund vs replacement, escalation vs resolution incorrectly.

**Frequency**: Common

**Symptoms**
- Business rule mismatch in branch decision.
- [Add more specific symptoms]

**Root Cause**
Agent chooses refund vs replacement, escalation vs resolution incorrectly.

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
1. **Comprehensive Decision-Tree Tests**: Create test suite covering all decision tree branches. Each branch has test cases with inputs → expected_branch. Execute tests in CI/CD before deployment. Target: 100% branch coverage.
2. **Policy Retrieval Before Branch Decision**: Before branching decision, query policy engine with case context (order_value, customer_status, product_type, etc.). Receive guidance_policy from engine. Decision must align with retrieved policy; log binding.
3. **Workflow Explainability Logging**: For each branch decision, log complete decision context: input values, conditions evaluated, matching policy rules, branch_taken, rationale. Enable post-hoc audit and analysis.

### Detection & Response
1. **Workflow Branch Anomaly Detection**: Monitor distribution of workflow branches per agent per day. Establish baseline (e.g., agent typically takes resolution 70%, escalation 20%, refund 10%). Alert on significant deviation from baseline (3σ).
2. **Outcome Consistency by Branch**: Measure outcomes by branch taken (customer satisfaction, error rate, cost, repeat issue rate). Flag branch with significantly worse outcomes than expected (e.g., refund branch has 50% repeat rate vs 5% for resolution).
3. **Policy-Decision Binding Audit**: Audit sample of decisions (e.g., 50 random decisions per week). Verify each decision matches relevant policies. Flag policy-decision misalignments for investigation.

### Architecture Patterns
1. **Declarative Workflow DSL**: Define workflow branches in declarative language (YAML/JSON) with explicit conditions for each branch. Example: 'IF order_value > 100 AND customer_tenure < 6_months THEN escalate'. Workflow engine enforces conditions strictly.
2. **Decision Audit Trail with Full Context**: Log complete decision context for each branch point: input_values, conditions_evaluated, matching_rules[], branch_taken, decision_id, timestamp, agent_id. Immutable for compliance.
3. **Policy-Linked Workflow**: Link workflow branch decisions to underlying policies. Workflow engine queries policy engine before executing branch. Branch execution validates policy alignment. Fail-closed: policy conflict = escalate to human.

### Metrics
1. **workflow_branch_policy_misalignment_rate_percent**: Target: < 0.1%; Alert threshold: > 0.5%; Track: branch, policy, misalignment_type
2. **wrong_branch_detections_per_day**: Target: 0; Any wrong-branch detection is incident
3. **branch_distribution_entropy_per_agent**: Target: within expected range (0.8-1.0 of baseline); Alert on 3σ deviation
4. **outcome_variance_by_branch_percent**: Target: < 5% unexpected variance; Higher variance indicates logic issues
5. **decision_audit_coverage_percent**: Target: 100%; Sample audit coverage

### Alerts
1. **Policy-Decision Misalignment Detected** (P1 - Critical): Condition - workflow branch selected doesn't match applicable policy guidance. Action: Block action execution, audit investigation, policy review, manual routing.
2. **Anomalous Branch Distribution** (P2 - Warning): Condition - agent branch pattern > 3σ from baseline for 5+ consecutive days. Action: Agent behavior review, decision logic audit, potential decision model retraining.
3. **Branch Outcome Degradation** (P2 - Warning): Condition - specific branch exhibits significantly worse outcomes vs baseline (e.g., 40% higher error rate). Action: Investigate branch logic, A/B test with control, potential branch disable with manual routing.

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
