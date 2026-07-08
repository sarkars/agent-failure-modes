# Conflicting Objectives

## Issue: Agent cannot resolve tradeoffs like speed vs accuracy, helpfulness vs compliance.

**Frequency**: Common

**Symptoms**
- Answer/action violates one explicit objective while satisfying another.
- [Add more specific symptoms]

**Root Cause**
Agent cannot resolve tradeoffs like speed vs accuracy, helpfulness vs compliance.

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
1. **Explicit Objective Priority Ordering**: Declare a strict, lexicographic ranking of objectives (e.g., compliance > safety > accuracy > speed) in the system config consumed by the planner, so a tradeoff has a deterministic resolution instead of being resolved implicitly and inconsistently by the model at generation time.
2. **Constraint vs. Preference Separation**: Model hard constraints (compliance, safety) as non-negotiable filters applied before soft preferences (speed, helpfulness) are optimized at all, so the two categories cannot trade off against each other by construction — a candidate action that fails a hard constraint is never even scored on the soft preferences.
3. **Pre-Action Conflict Detection**: Evaluate every candidate action against each declared objective independently before execution; if two objectives disagree on the same action, flag it as a conflict and route through the priority order or an escalation path rather than letting the agent pick ad hoc.

### Detection & Response
1. **Objective Violation Tagging**: Tag every response with which declared objectives it satisfied versus violated, using rubric-based judges or rule checks. Track the violation rate per objective pair over time to catch systemic tradeoff failures, not just isolated incidents.
2. **Tradeoff Pattern Clustering**: Cluster logged conflicts by objective pair and task context (e.g., "helpfulness vs. compliance" spiking specifically in refund flows) to find where the priority ordering or constraint set needs a targeted fix rather than a global rule change.
3. **Escalation on Unresolved Conflict**: When the conflict detector fires and no priority rule cleanly resolves it (e.g., two hard constraints disagree), escalate to a human reviewer instead of letting the agent default to whichever objective it weighted more heavily by chance.

### Architecture Patterns
1. **Objective Priority Config Service**: A centralized, versioned config defines the ranked objective list per domain/task type, consumed independently by the planner and a downstream validator, so priority changes are an ops change rather than a model retrain.
2. **Multi-Objective Validator**: A post-generation validation step scores the candidate response against each declared objective and rejects/regenerates any response that violates a higher-priority objective in favor of a lower-priority one.
3. **Conflict Resolution Router**: A dedicated component intercepts flagged conflicts and routes each to a deterministic rule, a human review queue, or a safe fallback action, decoupled from the main generation path so conflict handling doesn't depend on the same model that produced the conflict.

### Metrics
1. **objective_conflict_detection_rate_percent**: Target: tracked against domain baseline; Alert threshold: > 50% relative drop (detector likely broken)
2. **higher_priority_objective_violation_rate_percent**: Target: < 1%; Alert threshold: > 3%
3. **unresolved_conflict_escalation_backlog**: Target: cleared within SLA; Alert threshold: > 20 unresolved
4. **objective_pair_violation_concentration_percent**: Target: no single pair > 40% of all violations; Alert threshold: exceeded (signals a systemic gap for that pair)

### Alerts
1. **Compliance-Losing Conflict Resolution** (P1 - Critical): Condition - a detected instance where a compliance or safety objective was violated in favor of a lower-priority objective. Action: immediate review, roll back the action if possible, tighten the validator rule for that objective pair.
2. **Conflict Detector Silent Failure** (P2 - Warning): Condition - objective_conflict_detection_rate drops sharply with no corresponding drop in multi-objective task volume. Action: audit the detector for a logic regression, backfill missed conflicts from logs.
3. **Escalation Queue Backlog** (P3 - Info): Condition - unresolved conflict queue exceeds its SLA (e.g., 24h). Action: add reviewer capacity or tighten auto-resolution rules for known low-risk objective pairs.

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

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
