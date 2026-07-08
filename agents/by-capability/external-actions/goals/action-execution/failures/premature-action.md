# Premature Action

## Issue: Agent acts before enough evidence is gathered.

**Frequency**: Common

**Symptoms**
- Low evidence count before irreversible step.
- [Add more specific symptoms]

**Root Cause**
Agent acts before enough evidence is gathered.

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
1. **Evidence Threshold Gates**: Define minimum evidence requirements for each action type (e.g., 'refund requires confidence_score > 0.85 AND customer_contact_verified = true AND refund_window_check = pass'). Block action until all evidence criteria met. Log evidence evaluation for audit.
2. **Temporal Dependencies and Preconditions**: Define preconditions that must be satisfied for action eligibility. Example: 'refund requires wait_24_hours_post_purchase = true'. Model as state machine where action only available in specific states.
3. **Expert-in-the-Loop Qualification**: For high-impact actions requiring judgment calls, implement expert review gate. Route through approval workflow with mandatory domain expert sign-off. Expert reviews evidence quality, provides rationale.

### Detection & Response
1. **Premature Action Detection**: Monitor action execution relative to required evidence. Track evidence_count and evidence_quality_score at execution time. Flag actions executed with below-threshold evidence. Correlate with negative outcomes.
2. **Outcome Verification and Correlation**: Post-execution, measure action outcomes (customer satisfaction, error rate, repeat issue rate). Correlate outcomes with evidence levels at execution time. Identify patterns of poor outcomes with low evidence.
3. **Evidence Quality Audit Trail**: Audit-trail all evidence signals used for each action decision: signal_type, value, confidence_score, source, timestamp. Flag patterns of weak evidence usage (e.g., 'agent consistently acts with confidence < 0.70').

### Architecture Patterns
1. **Evidence Requirement DSL**: Define action preconditions in declarative language (YAML/JSON). Example: 'REFUND action requires: confidence_score ≥ 0.85 AND customer_contact_verified AND refund_window ≤ 30_days AND no_prior_refund'. Deploy preconditions through policy engine.
2. **Decision Gate Pattern**: Insert decision gate pre-action. Gate queries evidence systems, evaluates all preconditions, computes overall readiness score. Blocks action if readiness < threshold. Returns detailed readiness report to agent.
3. **Evidence Audit Trail with Signal Lineage**: Log all evidence signals considered for each action with complete lineage: signal_type, value, confidence_score, source, computation_date, source_freshness. Enable post-hoc analysis and model improvement.

### Metrics
1. **premature_action_attempts_per_day**: Target: < 0.5; Alert threshold: > 2; Track: agent_id, action_type, evidence_score
2. **evidence_quality_score_pre_action_average**: Target: > 0.85; Range: 0.0-1.0; Alert if drops < 0.75
3. **action_success_rate_by_evidence_level**: Target: Trend upward with higher evidence (e.g., 95% success at evidence>0.9, 60% at evidence<0.6)
4. **precondition_failures_blocking_action_per_day**: Target: < 2; Indicates preconditions appropriate
5. **expert_approval_denial_rate_percent**: Target: < 5%; Baseline; High denial indicates over-rejection

### Alerts
1. **Premature Action Attempt** (P2 - Warning): Condition - action executed with evidence_quality_score < 0.70. Action: Log evidence audit trail, post-outcome monitor, investigate if negative outcome observed.
2. **Evidence Quality Degradation** (P2 - Warning): Condition - evidence_quality_score drops > 15% month-over-month across agent population. Action: Investigation into evidence signal reliability, potential model retraining.
3. **Precondition Bypass** (P1 - Critical): Condition - action executed while required precondition not satisfied. Action: Immediate security alert, audit log review, potential action reversal.

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

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
