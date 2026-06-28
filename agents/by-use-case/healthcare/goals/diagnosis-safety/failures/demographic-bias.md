# Demographic Bias in Diagnosis & Treatment Recommendations

## Issue: Model Biased Toward/Against Certain Demographics (Race, Gender, Age); Different Accuracy for Different Groups

**Frequency**: Very Common

**Symptoms**
- Accuracy 95% for demographic A, 65% for demographic B
- Same condition misdiagnosed more often in one group
- Recommendations differ by demographic (treatment disparity)
- Model trained on skewed population data

**Root Cause**
Training data reflects historical biases in healthcare. Certain demographics underrepresented in training data (e.g., women underrepresented in cardiac disease research). Genetic/physiological differences between populations sometimes real, but often model captures training bias not biology.

**Example**
```
Scenario: Cardiovascular disease risk model
Trained on: 80% male, 20% female data
Model learns: "Chest pain in women = less urgent" (correlation from data)
Reality: Women's cardiac symptoms different; model dangerously underestimates risk
Result: Women receive lower-risk classification; delayed treatment
Impact: Disparity in outcomes; liability
```

**Key Statistics**
- Accuracy gap by demographic: 10-30% (worse for minorities)
- Underrepresentation: Female in cardiac studies 40% vs. 50% population

---

## Mitigation Strategies

1. **Representative Training Data**: Ensure demographics represented proportionally
2. **Stratified Evaluation**: Test accuracy separately by demographic
3. **Fairness Constraints**: Enforce equal sensitivity/specificity across groups
4. **Explainability**: Show which features drive demographic disparities

### Metrics
- Sensitivity/Specificity by demographic group
- Demographic parity (equal treatment across groups)
- Disparate impact ratio (should be >80% per legal standard)

### Alerts
- Accuracy gap >10% between groups → P1 (fairness issue)

---

## References

- [Bias in Medical AI](https://arxiv.org/abs/2004.14089)
- [Fair Machine Learning in Healthcare](https://arxiv.org/abs/2102.13232)
