# Multi-Party Obligation Tracking Failure

## Issue: Complex Contracts with Multiple Parties Have Obligations Model Fails to Track; Confuses Who Owes What

**Frequency**: Common

**Symptoms**
- Contract has 3+ parties; model misattributes obligations
- "Company A pays" vs. "Company B pays" — model gets confused
- Dependency chains not tracked (Party A pays only if Party B delivers)
- Obligations lost or misunderstood at execution

**Root Cause**
Multi-party contracts have complex graphs of obligations. Models trained on simpler 2-party contracts don't generalize well. Pronouns and references ("the said party", "such obligations") are ambiguous. Conditional obligations ("if X happens, then Y pays") require reasoning models don't do well.

**Example**
```
Scenario: Three-party service agreement
Parties: Customer, Vendor, Subcontractor
Obligations:
- Customer pays Vendor $100k
- Vendor pays Subcontractor $60k (if Subcontractor delivers by date X)
- If Subcontractor misses date, Vendor pays penalty to Customer

Model summary: "Vendor pays Customer $100k" (WRONG)
Correct: Vendor receives $100k; pays $60k; pays penalty if late

Impact: Budget miscalculation; cash flow crisis
```

**Key Statistics**
- Accuracy on 2-party contracts: 90%+
- Accuracy on 3-party contracts: 60-75%
- Accuracy on 4+ party contracts: <50%

---

## Mitigation Strategies

1. **Entity Tagging**: Explicitly tag all parties and their relationships
2. **Obligation Graphing**: Build explicit graph of who-owes-what-to-whom
3. **Conditional Parsing**: Parse if/then obligations separately
4. **Manual Verification**: For complex multi-party, require legal review

### Metrics
- Obligation tracking accuracy by number of parties
- Conditional obligation parsing accuracy

### Alerts
- 3+ parties detected → Manual legal review required

---

## References

- [NLP for Contract Extraction](https://arxiv.org/abs/1906.11419)
- [Semantic Parsing of Legal Text](https://arxiv.org/abs/2104.08671)
