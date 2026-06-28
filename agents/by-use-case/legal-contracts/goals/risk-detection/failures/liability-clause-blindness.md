# Liability Clause Blindness

## Issue: Model Fails to Flag Dangerous Liability/Indemnification Clauses; Exposes Organization to Unquantified Risk

**Frequency**: Common

**Symptoms**
- Contract approved by model; contains unlimited liability clause
- Model flags wrong clauses; misses critical ones
- Liability exposure not quantified
- Client later sues; exposure exceeds expected risk

**Root Cause**
Liability clauses are complex legal constructs. Models trained on successful contracts don't see enough failed deals with bad liability terms. Danger is in subtle wording ("reasonable" vs. "any", "direct" vs. "indirect + consequential"). Models learn surface patterns, miss legal nuance.

**Example**
```
Scenario: SaaS service agreement
Clause: "Vendor indemnifies Customer for any damages arising from Service"
Interpretation: Unlimited indemnification? Or reasonable limits?
Model: "Indemnification clause present - normal" ✓
Legal review: "This is UNLIMITED liability! We're exposed to billions!"
Impact: Massive unquantified risk exposure; cannot get insurance
```

**Key Statistics**
- Liability clauses flagged: 40-60% detection rate
- False negatives: 40-60% (dangerous clauses missed)
- Financial exposure missed: $1M-$100M+ per contract

---

## Mitigation Strategies

1. **Clause Dictionary**: Curate examples of dangerous liability language
2. **Legal Review**: All liability clauses must be reviewed by lawyer, not just model
3. **Quantified Limits**: Flag unlimited liability; require caps
4. **Insurance Check**: Coordinate with insurance (is exposure insurable?)

### Metrics
- Liability clause detection rate
- False negative rate (missed dangerous clauses)
- Liability cap accuracy

### Alerts
- Unlimited liability detected → P1 (escalate to legal)

---

## References

- [Contract Risk Analysis with NLP](https://arxiv.org/abs/2108.02435)
- [Legal Liability in AI Contracts](https://arxiv.org/abs/2110.08521)
