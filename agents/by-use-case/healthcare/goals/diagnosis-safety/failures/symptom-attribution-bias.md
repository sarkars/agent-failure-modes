# Symptom Attribution Bias (Wrong Diagnosis Due to Anchoring)

## Issue: Model Anchors on Initial Symptom; Misses True Diagnosis Because Anchored to Wrong Hypothesis

**Frequency**: Very Common

**Symptoms**
- Model gets one symptom; overcommits to diagnosis
- Ignores contradictory symptoms
- Fails to revise diagnosis when new info arrives
- "Tunnel vision" diagnosis (ignores context)

**Root Cause**
Models learn statistical associations (chest pain → heart disease, 90% of time). But 10% of chest pain is not cardiac. Model overweights early evidence; doesn't properly update with Bayesian reasoning. Anchoring bias (psychological effect) replicated in AI.

**Example**
```
Scenario: Chest pain triage
Patient: Middle-aged male + chest pain
Model probability: "Cardiac event" = 85%
Actually: Pulmonary embolism (rare for this demographic but present)
Other symptoms: Leg swelling, shortness of breath (consistent with PE, not MI)
Model: Ignores leg symptoms (low weight in training); sticks with MI diagnosis
Impact: Patient gets wrong treatment; life-threatening delay
```

**Key Statistics**
- Sensitivity to contradictory evidence: 20-40% (models slow to change)
- Bayesian update deficit: Models underweight new evidence vs. prior

---

## Mitigation Strategies

1. **Explainable Reasoning**: Show reasoning for diagnosis; allow clinician to challenge
2. **Alternative Hypotheses**: Generate top-3 diagnoses, not just 1
3. **Evidence Weighting**: Require certain contradictory symptoms to override diagnosis
4. **Conditional Probabilities**: Model P(symptoms|diagnosis) properly, not just P(diagnosis|symptoms)

### Metrics
- Sensitivity to contradictory evidence (does model update?)
- Diagnostic accuracy when multiple hypotheses plausible
- Calibration of confidence

### Alerts
- Confidence >90% with contradictory evidence → Warn clinician

---

## References

- [Diagnostic Reasoning in AI](https://arxiv.org/abs/2107.14272)
- [Bayesian Updating in Medical AI](https://arxiv.org/abs/2108.00672)
