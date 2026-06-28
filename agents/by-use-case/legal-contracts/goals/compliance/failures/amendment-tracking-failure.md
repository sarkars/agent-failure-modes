# Contract Amendment Tracking Failure

## Issue: Contract Modified Multiple Times; Model Analyzes Original, Ignoring Amendments; Outdated Analysis Given

**Frequency**: Common

**Symptoms**
- Original contract: 30-day payment terms
- Amendment 1: Changed to 60-day terms
- Amendment 2: Restored to 45-day terms
- Model analyzes: Original (30-day) — WRONG
- Compliance/billing based on wrong terms

**Root Cause**
Contracts often modified via amendments. Amendments may be in separate documents, not integrated into main contract. Models often see only original; amendments missed. No unified "current version" tracking. Can't reason about amendment history and current state.

**Example**
```
Scenario: Master service agreement with amendments
Original: "Vendor shall provide service at $100/month"
Amendment 1: "Price increased to $125/month effective 2024-01"
Amendment 2: "Price reduced to $110/month effective 2024-06"

Model analysis: "Cost is $100/month" (Original only)
Billing: Charged $100/month (should be $110)
Vendor: "You owe back payment for 6 months"

Impact: Billing dispute; reconciliation needed
```

**Key Statistics**
- Contracts with amendments: 50-70% of long-term agreements
- Amendment tracking failure: 30-50% of models (miss amendments)
- Financial impact of missed amendments: $10k-$1M+ per contract

---

## Mitigation Strategies

1. **Amendment Consolidation**: Merge amendments into single contract document
2. **Version Control**: Track contract versions with effective dates
3. **Temporal Reasoning**: Model contract state as time-series (what applies when)
4. **Change Tracking**: Highlight changes from previous version

### Metrics
- Amendment detection rate (should be 100% for all amendments)
- Current state accuracy (does model know current terms?)
- Version currency (is model using latest version?)

### Alerts
- Amendment found not in analyzed contract → Re-analyze with full amendment history

---

## References

- [Contract Amendment Analysis](https://arxiv.org/abs/2012.03485)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
