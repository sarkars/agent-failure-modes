# Age Bias in Symptom Interpretation

## Issue: Model Misinterprets Symptoms Differently Based on Patient Age; Younger Patients Undertreated, Older Patients Overtreated

**Frequency**: Very Common

**Symptoms**
- Young patient with same symptoms as older patient gets different diagnosis
- Young: "Probably anxiety, monitor at home"
- Old: "Probable cardiac event, admit immediately"
- Age acts as implicit feature in model; diagnosis changes with age

**Root Cause**
Disease prevalence varies by age. Older patients more likely to have serious conditions; younger patients more likely to have benign causes. Models learn "young + chest pain = anxiety" pattern. But this is correlation, not causation — young people CAN have heart attacks. Age biases toward under-treatment in youth, over-treatment in elderly.

**Example**
```
Scenario: Chest pain triage
30-year-old: Chest pain, shortness of breath
Model: "Anxiety. Discharge home. Probability cardiac: 5%"
Actual: Myocardial infarction (happens in young people too!)
Impact: Patient sent home; heart attack progresses; cardiac damage

70-year-old: Chest pain, shortness of breath
Model: "Acute coronary syndrome. Admit ICU. Probability: 90%"
Actual: Panic attack; no cardiac event
Impact: Unnecessary admission, ICU bed usage, cost
```

**Key Statistics**
- Age as implicit feature: Correlation with diagnosis 0.4-0.6
- Age-bias gap: 20-40% difference in treatment intensity between young/old same symptoms
- Missed cardiac events in young: 2-3x baseline due to underestimation

---

## Mitigation Strategies

1. **Age-Stratified Models**: Separate models for different age groups
2. **Remove Age**: Train without age feature; evaluate on both old/young
3. **Equalize Priors**: Use population prevalence, not training data prevalence
4. **Fairness Audit**: Ensure identical symptoms → identical recommendations regardless of age

### Metrics
- Recommendation consistency (same input → same output regardless of age)
- Sensitivity/Specificity by age group
- Fairness metric (disparate impact ratio >0.8)

### Alerts
- Treatment recommendation differs by age → Red flag

---

## References

- [Age Bias in Medical AI](https://arxiv.org/abs/2007.04786)
- [Fairness in Diagnostic Systems](https://arxiv.org/abs/2102.13232)
