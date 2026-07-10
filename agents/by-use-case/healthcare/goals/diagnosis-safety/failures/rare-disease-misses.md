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

### Prevention

1. **Class-balanced rare-disease detection with oversampling and expert-model gating**: Implement dual-model approach: (a) General model for common-disease screening (trained on balanced class weights), (b) Specialist rare-disease screening model (trained with oversampling/SMOTE on rare-disease cases, e.g., Ehlers-Danlos, Marfan, vasculitis). On every diagnosis session: common model generates top-5 differential → if top-diagnosis confidence <75% OR if presentation has "unusual features" (extreme joint mobility, atypical skin findings, vascular anomalies), route to specialist rare-disease screener. Specialist screening output is required for final diagnosis. Root cause mitigation: Prevents class-imbalance bias by explicitly deploying expert model for cases where rare disease likely.

2. **Feature-level rare-disease highlighting with decision rules**: Encode hard-coded decision rules for rare-disease red-flags: "Hypermobility + easy bruising + skin elasticity → MUST consider Ehlers-Danlos"; "Short stature + lens dislocation + aortic root dilation → MUST consider Marfan"; etc. Clinical-guideline-sourced rules ensure rare-disease consideration even if not statistically likely. Root cause: Prevents omission via explicit rules.

3. **Rare-disease case-augmented few-shot prompting**: In each diagnostic session, include few-shot examples of rare diseases matching current symptom profile: "Here are 3 documented cases of EDS presenting with [symptoms]..." This in-context learning augments training data imbalance. Root cause: Compensates for training-data class imbalance via few-shot.

### Detection & Response

1. **Rare-disease detection audit with sensitivity tracking by condition**: For each diagnosis, log: (a) whether specialist rare-disease screening was triggered, (b) rare-disease flags detected, (c) differential ranking for each condition, (d) actual diagnosis if follow-up available. Quarterly audit: compute sensitivity/specificity per rare disease. Alert if sensitivity for any rare disease <80% (e.g., "EDS sensitivity 65% vs. 80% target").

2. **Undiagnosed-case tracking and rare-disease signal detection**: Track cases where diagnosis delayed or changed after initial recommendation. For cases >30-day diagnostic delay, analyze: was a rare disease missed initially? Build "diagnostic-delay cohort" database and use to refine rare-disease detection heuristics.

### Architecture Patterns

1. **Dual-Model Rare-Disease Gating**: Input: (symptoms, lab, imaging) → Common-Disease Model → {top-5 differential, confidence}. If confidence <75% or rare-disease-flag detected → route to Specialist Rare-Disease Model (trained with oversampled rare diseases). Specialist output merged with common-model output.

2. **Rare-Disease Red-Flag Detector**: Hardcoded clinical-guideline rules. Input: (symptom_set, lab_values, imaging) → Outputs: (rare_disease_flags: ["EDS", "Marfan", ...], trigger_threshold). Feeds specialist model routing.

3. **Balanced Training Pipeline**: Training data resampling: oversample rare diseases or generate synthetic cases (SMOTE) for underrepresented conditions. Separate specialist model for rare-disease screening, trained on balanced dataset.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Rare-Disease Sensitivity | >80% | <70% | # of rare-disease cases where condition identified in differential / total rare-disease cases (per condition type) |
| Rare-Disease False-Negative Rate | <10% | >20% | # of rare-disease cases where diagnosis missed or ranked <3 in differential / total rare-disease cases |
| Common vs. Rare Sensitivity Gap | <10% | >20% | Sensitivity for common diseases (>90%) minus sensitivity for rare (<80%); lower gap = less bias |
| Specialist Model Activation Rate | 5-15% | <3% | % of cases where rare-disease specialist model triggered (indicates good problem-case detection) |
| Diagnostic-Delay Detection | <30 days | >60 days | Mean time from symptom onset to rare-disease diagnosis (audit sample) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Rare-Disease Sensitivity Below Target | Rare-disease sensitivity <70% for specific condition (e.g., EDS <70% vs. 80% target) | HIGH | Escalate to clinical leadership; audit missed cases; retrain specialist model with additional examples |
| Diagnostic Delay in Rare-Disease Case | Diagnosis delayed >30 days; rare disease initially missed in differential | HIGH | Root-cause analysis; audit red-flag detection; investigate why specialist model not triggered |
| Rare-Disease Red-Flag Missed | Patient has documented rare-disease-flag (EDS red-flags: hypermobility+bruising+skin elasticity) but specialist model not triggered | CRITICAL | Investigate red-flag detection failure; audit similar cases; potential patient safety issue |

---

## References

- [Class Imbalance in Medical AI](https://arxiv.org/abs/2012.03816)
- [Rare Disease Diagnosis with ML](https://arxiv.org/abs/2105.11234)
