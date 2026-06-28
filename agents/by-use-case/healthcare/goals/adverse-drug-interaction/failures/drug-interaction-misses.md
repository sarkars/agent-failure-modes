# Drug Interaction Misses & Contraindication Blindness

## Issue: Model Recommends Drug Combination Without Flagging Known Dangerous Interactions

**Frequency**: Common

**Symptoms**
- Model recommends two drugs known to interact dangerously
- Interaction database not consulted or outdated
- New drug interactions discovered post-deployment
- Patient takes dangerous drug combo; adverse event

**Root Cause**
Drug interactions are discrete rules (Drug A + Drug B → risk level X). Models sometimes learn statistical patterns but miss logical rules. Interaction database must be comprehensive and up-to-date. Missing one rare but dangerous interaction is a patient safety issue.

**Example**
```
Scenario: Medication recommender system
Patient: On warfarin (blood thinner)
Model recommends: Ibuprofen (analgesic) for pain
Known interaction: Warfarin + NSAID → Increased bleeding risk
Model: Doesn't flag (interaction not in training data or database outdated)
Patient: Takes both; develops GI bleeding
Impact: Life-threatening adverse event; liability
```

**Key Statistics**
- Known interactions: 30,000+ documented
- Coverage of interactions in training: Often <50%
- New interactions discovered: 100-200 per year

---

## Mitigation Strategies

1. **Interaction Database**: Use authoritative database (DrugBank, Micromedex); update regularly
2. **Hard Constraints**: Flag known dangerous interactions as must-not combinations
3. **Monitoring**: Prospective pharmacovigilance for new interactions
4. **Alternative Suggestions**: If interaction detected, suggest safe alternatives

### Metrics
- Interaction detection rate (should be 100% for known interactions)
- False negative rate (missed interactions)
- False positive rate (flagged but not really dangerous)

### Alerts
- Known interaction not flagged → P1

---

## References

- [Drug Interaction Prediction with ML](https://arxiv.org/abs/2004.12653)
- [Pharmacovigilance & Adverse Events](https://arxiv.org/abs/2106.11267)
