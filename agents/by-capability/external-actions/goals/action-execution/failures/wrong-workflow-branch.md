# AI Agent Picks the Wrong Workflow Branch (Refund vs. Replacement, Escalate vs. Resolve): Causes and Fixes

## Issue: AI agent chooses the wrong path in a decision workflow — refund vs. replacement, escalation vs. resolution — based on surface pattern-matching instead of the applicable rule.

**Frequency**: Common

**Symptoms**
- Business rule mismatch in branch decision.
- Agent offers a replacement for a case that policy says should be a refund (or vice versa), based on surface-level similarity to past cases rather than the actual applicable rule.
- Case is resolved directly by the agent when the specific combination of factors (value, customer tier, product type) should have triggered escalation.
- Commonly reported in graph-based orchestration frameworks like LangGraph, where a conditional edge free-forms its branch decision from context instead of evaluating explicit routing rules.

**Root Cause**
The branch decision is learned from the most frequent historical pattern rather than evaluated against the specific policy conditions (value thresholds, customer tenure, product type) that actually govern the current case, because those conditions are only implicit in training examples rather than queried explicitly at decision time. With no decision-tree or rule engine backing the choice, the agent free-forms a branch from context, and when a case superficially resembles the common pattern but differs on exactly the condition that should redirect it, the surface-level resemblance wins because nothing structurally forces a check against the differentiating rule before the branch is taken.

**Example**
```
A customer reports a damaged high-value item ($800) from a first-time buyer. Policy states
that damaged items over $500 from customers with no order history must be escalated to a
human reviewer (fraud/damage-claim risk). The agent instead follows its general pattern
for damaged-item complaints — offer a replacement directly — because that branch is the
most common path in its training examples, missing the value-and-tenure condition that
should have routed this case to escalation.
```

**Contributing Factors**
- Decision logic learned from the most frequent historical pattern rather than the specific policy conditions for the current case.
- Policy conditions (value thresholds, customer tenure, product type) not queried or evaluated at decision time, only implicit in training examples.
- No explicit decision-tree or rule engine backing the branch choice — the agent free-forms the decision from context.
- Overlapping or ambiguous policy documentation where multiple rules could plausibly apply to the same case.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Escalation-triggering combination | High-value damaged item + no order history (meets escalation criteria) | Agent escalates per policy instead of resolving directly | Agent resolves directly via replacement/refund, bypassing escalation |
| Common-pattern override | Case superficially resembles the most frequent historical case type but differs on a policy-relevant condition | Agent's branch decision reflects the specific policy condition, not the surface pattern | Agent selects the branch typical for the surface pattern, ignoring the differentiating condition |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| workflow_branch_policy_misalignment_rate_percent | < 0.1% | Sampled decisions where the branch taken doesn't match the policy engine's expected branch for that case |

---

**How to fix it**: back the branch decision with an explicit decision-tree or rule engine keyed on the actual policy conditions, not learned surface similarity — see Mitigation Strategies below.

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
| workflow_branch_policy_misalignment_rate_percent | > 0.5% |
| branch_distribution_entropy_per_agent | > 3σ from baseline |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Policy-Decision Misalignment Detected | Workflow branch selected doesn't match applicable policy guidance | Critical |
| Anomalous Branch Distribution | Agent's branch pattern deviates more than 3σ from baseline for 5+ consecutive days | Warning |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
