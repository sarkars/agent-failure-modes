# Contract Ambiguity Detection Failure

## Issue: Model Misses Ambiguous or Conflicting Clauses in Contracts; Leads to Dispute When Parties Interpret Differently

**Frequency**: Common

**Symptoms**
- Clause says "deliver within 30 days" and also "subject to availability"
- Ambiguity: Is 30-day deadline hard or soft?
- Model approves contract; parties interpret differently
- Dispute arises; expensive litigation

**Root Cause**
Ambiguity detection requires deep legal reasoning; understanding multiple valid interpretations. Models trained on contracts do surface-level parsing. Don't flag sentences that have multiple reasonable interpretations. Hard for even lawyers to spot ambiguities.

**Example**
```
Scenario: Service level agreement
Clause: "Vendor will provide 99% uptime within 30 days"
Interpretation 1: "Within 30 days of contract start, achieve 99% uptime"
Interpretation 2: "Average 99% uptime, measured over 30-day windows"
Interpretation 3: "Vendor guarantees 99% uptime; if breached, customer gets refund within 30 days"

Model: "Uptime clause present" ✓ (misses ambiguity)
Dispute: Customer denied refund because vendors interpret #1 (startup grace period)

Impact: Litigation cost; relationship damaged
```

**Key Statistics**
- Ambiguous clauses: 10-20% of typical contracts
- Detection rate by model: 20-40% (high false negatives)
- Dispute litigation cost: $100k-$1M+

---

## Mitigation Strategies

1. **Ambiguity Flag**: Train model to detect sentences with multiple interpretations
2. **Legal Review**: All ambiguous clauses escalated to lawyer for clarification
3. **Definition Section**: Require clear definitions for key terms
4. **Dispute Examples**: Provide interpretation guide (if X happens, then...)

### Metrics
- Ambiguity detection rate (recall)
- False positive rate (false flags on clear clauses)
- Dispute rate post-deployment

### Alerts
- Ambiguous clause detected → Escalate for clarification

---

## References

- [Ambiguity in NLP & Contract Analysis](https://arxiv.org/abs/2104.14641)
- [Contract Interpretation & Dispute Resolution](https://arxiv.org/abs/2105.08432)
