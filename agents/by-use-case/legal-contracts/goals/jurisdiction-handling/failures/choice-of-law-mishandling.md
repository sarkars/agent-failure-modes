# Choice-of-Law & Jurisdiction Mishandling

## Issue: Model Fails to Properly Interpret Choice-of-Law Clauses; Applies Wrong Jurisdiction's Laws to Obligations

**Frequency**: Common

**Symptoms**
- Contract choice-of-law: New York law
- Model analyzes under California law (or no law analysis)
- Contract enforceability different under correct jurisdiction
- Disputes later reveal wrong jurisdiction assumed

**Root Cause**
Choice-of-law clauses define legal framework for contract. Models trained on single jurisdiction don't generalize to multi-jurisdictional reasoning. Different jurisdictions have different rules (statute of limitations, damages limits, etc.). Models often miss or misinterpret choice-of-law clause.

**Example**
```
Scenario: International services contract
Choice-of-law: "This agreement shall be governed by the laws of Delaware"
Model analysis: Analyzes under general US law
Specific Delaware rule: Non-compete agreements unenforceable
Analysis result: "Non-compete clause is enforceable"
Actual (Delaware law): Non-compete is void
Impact: Non-compete not enforceable; model recommendation wrong
```

**Key Statistics**
- Choice-of-law detection: 80%+ (mostly correct)
- Correct application of chosen law: 40-60% (error rate high)
- Jurisdiction mismatch causing wrong advice: 15-25%

---

## Mitigation Strategies

1. **Choice-of-Law Extraction**: Explicitly identify and extract choice-of-law clause
2. **Jurisdiction Database**: Map clause to specific jurisdiction rules
3. **Jurisdiction-Specific Analysis**: Apply correct jurisdiction's law
4. **Multi-Jurisdiction Check**: If relevant, analyze under multiple jurisdictions

### Metrics
- Choice-of-law clause detection rate
- Correct jurisdiction application rate
- Analysis accuracy under correct jurisdiction

### Alerts
- Ambiguous or missing choice-of-law → Escalate to legal

---

## References

- [Jurisdiction Prediction in Contracts](https://arxiv.org/abs/2012.14856)
- [Cross-Border Contract Analysis](https://arxiv.org/abs/2108.03876)
