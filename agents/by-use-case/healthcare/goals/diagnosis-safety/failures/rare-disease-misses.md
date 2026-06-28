# Rare Disease Misdiagnosis & Missing Rare Conditions

## Issue: Model Trained on Common Diseases; Misses or Misdiagnoses Rare Conditions

**Frequency**: Common

**Symptoms**
- Model confident on common diagnosis for rare disease
- Rare disease presentation goes unrecognized
- Patient receives wrong treatment for months
- Sensitivity for rare diseases <50%

**Root Cause**
Training data imbalanced; common diseases (diabetes, hypertension) vastly outnumber rare ones (Ehlers-Danlos, Marfan). Models learn "most likely" = "most common." Rare disease patterns are underrepresented; model never learns them. Class imbalance not corrected.

**Example**
```
Scenario: Symptom-to-diagnosis model
Patient: Connective tissue disorder (Ehlers-Danlos Syndrome)
Symptoms: Joint hypermobility, easy bruising, skin hyperextensibility
Model trained on: 95% common diseases (no rare disease samples)

Model prediction: "Most likely: Joint hypermobility syndrome (common)" → Wrong
Actual: Ehlers-Danlos (rare, serious)
Impact: Patient treated for wrong condition; complications escalate
```

**Key Statistics**
- Sensitivity for rare disease: 20-50% (vs. 90%+ for common diseases)
- False negative rate for rare disease: 50-80%
- Class imbalance ratio: 1000:1 or worse

---

## Mitigation Strategies

1. **Oversampling/Synthetic**: Oversample rare diseases or use SMOTE
2. **Specialist Models**: Train separate expert model for rare disease screening
3. **Differential Diagnosis**: When common diagnosis doesn't fit, investigate rare alternatives
4. **Case-Based Learning**: Use case studies of rare diseases to augment data

### Metrics
- Sensitivity for rare diseases (should be >80%)
- False negative rate for rare diseases
- Coverage (% of rare diseases detectable)

### Alerts
- Rare disease detection <70% → P1

---

## References

- [Class Imbalance in Medical AI](https://arxiv.org/abs/2012.03816)
- [Rare Disease Diagnosis with ML](https://arxiv.org/abs/2105.11234)
