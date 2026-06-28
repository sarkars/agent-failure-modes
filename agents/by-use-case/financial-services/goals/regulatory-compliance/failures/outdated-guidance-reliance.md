# Outdated Regulatory Guidance Reliance

## Issue: Model Uses Outdated Regulatory Rules; Recommendations Violate New Regulations Effective Retroactively or Overlooked

**Frequency**: Common

**Symptoms**
- Compliance check passes (uses old rules)
- Audit finds violation of new rules effective 6 months ago
- Rules changed but model not updated
- No automatic rule versioning or update tracking

**Root Cause**
Regulatory rules embedded in model logic or training data. When rules change, model isn't updated. Knowledge cutoff dates for regulation are implicit, not tracked. No automated mechanism to flag when rules change and model retraining is needed.

**Example**
```
Scenario: Portfolio leverage limits
Old rule (pre-2024): Margin up to 50%
New rule (2024): Margin capped at 30%
Model deployed Jan 2024: Still uses old 50% limit
Audit June 2024: Finds portfolios over-leveraged by regulation
Impact: Violation notice, potential fines
```

**Key Statistics**
- Regulatory changes: 5-10 per year per jurisdiction
- Rule update lag: 3-6 months typical
- Violation rate if not updated: 20-40%

---

## Mitigation Strategies

1. **Rule Versioning**: Track regulatory rules with effective dates in code
2. **Automated Updates**: Subscribe to regulatory change feeds (SEC, ECB, etc.)
3. **Compliance Layer**: Separate rule engine from model logic
4. **Regular Audits**: Quarterly compliance checks against latest rules

### Metrics
- Rules currency (% of rules updated within 1 month of effective date)
- Compliance violation rate (should be <1%)

### Alerts
- Potential rule violation detected → P1 (escalate to compliance)

---

## References

- [Regulatory Technology & Compliance](https://arxiv.org/abs/2105.03744)
- [Automated Compliance Monitoring](https://arxiv.org/abs/2210.14289)
