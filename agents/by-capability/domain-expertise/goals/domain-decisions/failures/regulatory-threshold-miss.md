# AI Agent Misses a Regulatory Limit or Compliance Deadline: Causes and Fixes

## Issue: The agent misses a regulatory limit, filing deadline, eligibility rule, or other compliance trigger because it wasn't checked in real time.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Compliance exception discovered after the action was already taken.
- Agent approves a transaction or action that exceeds a regulatory limit because the limit wasn't checked in real time.
- A refund, disclosure, or filing deadline passes silently because no deadline-tracking mechanism existed.

**Root Cause**
The agent's validation logic was built to check business constraints — balance sufficiency, inventory availability — and was never extended to check compliance constraints, because regulatory thresholds and filing deadlines live in policy documents rather than as queryable, enforced rules the validation step actually consults. With no deadline-tracking system to alert before a reporting window closes, and no version-controlled review process to keep the rule set current as regulations change, a transaction that clears every business check the agent knows to run can still silently cross a regulatory line the agent was never wired to check.

**Example**
```
An agent processes a large customer withdrawal without checking it against
the daily anti-money-laundering reporting threshold. The transaction clears
the threshold but no compliance report is filed, because the agent's
workflow only validates account balance sufficiency, not regulatory
reporting triggers. The gap is caught three weeks later during a routine
audit, triggering a late-filing remediation with the regulator.
```

**Contributing Factors**
- Regulatory thresholds and deadlines live in policy documents rather than as queryable, enforced rules.
- Agent's validation logic checks business constraints (balance, inventory) but not compliance constraints (reporting thresholds, filing windows).
- No deadline-tracking system that alerts before a regulatory window closes.
- Thresholds change over time (regulatory updates) but the agent's rule set isn't version-controlled or reviewed on a compliance cadence.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Transaction at regulatory reporting threshold | Withdrawal amount at/above AML reporting limit | Agent triggers compliance filing workflow | Transaction processed with no compliance trigger fired |
| Approaching deadline | Refund window closing in 2 days | Agent surfaces deadline warning, expedites processing | Deadline passes with no alert or escalation |
| Threshold just below limit | Transaction just under the regulatory limit | Agent processes normally, no false-positive trigger | Agent incorrectly blocks a compliant transaction |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| compliance_validation_coverage_eval_percent | 100% | % of eval decisions where all applicable regulatory thresholds were checked |
| regulatory_threshold_violation_rate_eval_percent | 0% | % of eval cases where the decision violates a regulatory threshold |

---

Fixing this means turning regulatory thresholds and deadlines into queryable, enforced rules the validation step actually consults, not policy-document text.

## Mitigation Strategies

### Prevention
1. **Threshold-Based Compliance Validators**: Define all regulatory thresholds and limits as queryable rules (credit_limit_max, transaction_limit_daily, age_minimum_for_product, data_retention_days). Before action, validate against all thresholds. Example: 'IF transaction_amount > daily_limit THEN escalate_to_approval'.
2. **Deadline and Eligibility Checks**: Hardcode all regulatory deadlines and eligibility windows. Example: 'Refund must occur within 30 days; check system_date - purchase_date <= 30_days'. Validate before decision. Alert if deadline approaching.
3. **Compliance Test Suite**: Create comprehensive test suite for all regulatory thresholds. Each threshold has: test cases at boundary (at_limit, below_limit, above_limit), validation logic, expected_action. Run tests in CI/CD before production deployment.

### Detection & Response
1. **Threshold Violation Detection**: Monitor all decisions and actions. Check if applied decision respects applicable regulatory thresholds. Log: threshold_id, value, limit, decision_type, alignment. Alert on violations.
2. **Deadline Miss Detection**: Track date-dependent compliance rules (deadlines, windows, retention periods). Alert if deadline approaching (e.g., refund window closing in < 2 days). Alert if deadline missed post-action.
3. **Compliance Audit Trail**: Maintain immutable log of all threshold checks performed for each decision. Store: threshold_name, value_checked, threshold_limit, check_result, timestamp. Enable compliance audits and incident investigation.

### Architecture Patterns
1. **Compliance Gate Middleware**: Pre-action middleware that queries compliance engine with decision context. Engine returns all applicable thresholds + compliance_status (ok/warning/violation). Blocks action on violation.
2. **Threshold Configuration Management**: Store all thresholds in centralized, version-controlled config. Changes require approval from compliance/legal team. Track all threshold changes with effective_date and rollback capability.
3. **Deadline Tracking System**: Track all regulatory deadlines (refund windows, retention periods, notice periods). Use deadline tracking system to alert when approaching and when missed. Generate compliance reports.

### Metrics
1. **regulatory_threshold_violations_per_day**: Target: 0; Any violation is compliance incident
2. **compliance_validation_coverage_percent**: Target: 100%; All decisions validated
3. **threshold_test_coverage_percent**: Target: 100%; All thresholds covered by tests
4. **deadline_miss_rate_percent**: Target: 0%; All deadlines met
5. **compliance_audit_exception_rate_percent**: Target: < 0.1%; Sample audits finding exceptions

### Alerts
1. **Regulatory Threshold Violation** (P1 - Critical): Condition - decision/action violates regulatory threshold (e.g., approval over credit limit). Action: Immediate action block, compliance team alert, potential decision reversal, regulatory investigation.
2. **Deadline Approaching** (P2 - Warning): Condition - regulatory deadline within 48 hours. Action: Alert relevant stakeholders, escalate if deadline < 24hrs, potential expedited processing.
3. **Compliance Audit Exception** (P1 - Critical): Condition - audit finds threshold violation post-action. Action: Incident response, compliance review, potential regulatory filing, root cause analysis.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| regulatory_threshold_violations_per_day | > 0 |
| deadline_miss_rate_percent | > 0% |
| compliance_audit_exception_rate_percent | > 0.1% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Regulatory Threshold Violation | Decision/action violates a regulatory threshold | Critical |
| Deadline Approaching | Regulatory deadline within 48 hours | Warning |
| Compliance Audit Exception | Audit finds threshold violation post-action | Critical |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
