# Polypharmacy Cascade Failures (Multi-Drug Interaction Explosion)

## Issue: Patient on 5+ Medications; Pairwise Interaction Checking Misses Three-Way or Four-Way Drug Interactions

**Frequency**: Common

**Symptoms**
- Model checks Drug A + Drug B: OK
- Model checks Drug A + Drug C: OK
- Model checks Drug B + Drug C: OK
- But A + B + C together causes severe adverse event
- Three-way interactions not checked (exponential combinations)

**Root Cause**
Drug-drug interaction databases mostly document pairwise interactions (2-drug combos). Three-way+ interactions rare, under-studied. Exponential explosion of combinations (10 drugs = 120 pairwise + 1000s of 3-way combos). Models trained only on pairwise can't flag three-way risks.

**Example**
```
Scenario: Elderly patient on multiple medications
Medications:
- Warfarin (blood thinner)
- Aspirin (pain reliever)
- NSAIDs (ibuprofen for arthritis)

Pairwise checks:
- Warfarin + Aspirin: Increased bleeding risk (known) ✓ Flagged
- Warfarin + NSAID: Increased bleeding risk (known) ✓ Flagged
- Aspirin + NSAID: GI bleeding risk (known) ✓ Flagged

Three-way interaction:
- Warfarin + Aspirin + NSAID together: Risk multiplied (synergistic)
- Model: Each pair flagged individually; doesn't model synergy
- Result: Patient gets all three (because no explicit three-way contraindication)
- Outcome: Severe GI bleeding requiring transfusion

Impact: Preventable adverse event; patient harm
```

**Key Statistics**
- Polypharmacy patients (5+ drugs): 30-50% of elderly population
- Known 3-way interactions: <5% of total interaction space (sparse)
- Adverse event rate in polypharmacy: 2-5x higher than monotherapy

---

## Mitigation Strategies

1. **Pharmacist Review**: All polypharmacy (5+ drugs) requires pharmacist approval
2. **Simulation**: Computationally simulate drug metabolism; detect potential interactions
3. **Collateral Damage**: Flag when multiple drugs hit same target (synergistic risk)
4. **Deprescribing**: Recommend stopping lowest-value drugs if interaction risk high

### Metrics
- Polypharmacy coverage (% patients with 5+ drugs reviewed)
- Three-way interaction detection capability
- Adverse event rate in polypharmacy (should trend down)

### Alerts
- Patient on 5+ drugs → Pharmacist review required
- High-risk combination detected → P1

---

## References

- [Polypharmacy & Drug-Drug Interactions](https://arxiv.org/abs/2005.01742)
- [Adverse Drug Events in Elderly](https://arxiv.org/abs/2012.04356)
