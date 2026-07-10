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

### Prevention

1. **Age-invariant symptom interpretation with symptom-severity baseline**: Implement dual-path symptom analysis: (Path A) Symptom-only reasoning (age-blind): given symptom profile, generate primary differential diagnoses without age information, using age-adjusted prevalence priors (e.g., "chest pain + SOB: consider ACS with base rate 15% across all ages"). (Path B) Age-stratified refinement: apply age-specific epidemiology to refine probability bounds (e.g., "in young patient [<40], broaden differential to include atypical presentations; in elderly, increase ACS probability by 2x"). Require both paths and compare: if age shifts diagnosis >20% probability, flag as "[AGE BIAS RISK]" and require additional supporting evidence before recommending age-dependent treatment difference. Root cause mitigation: Prevents age-driven treatment recommendations by separating symptom interpretation from age-specific epidemiology.

2. **Fairness-audit gate with symptom-pair equivalence checking**: Before finalizing recommendation, run fairness check: "If same patient with same symptoms were age 30 vs. 70, would recommendations differ?" For any symptom combination, compute recommendations across age-ranges [20, 40, 60, 80]. Alert if recommendations differ substantially (e.g., cardiac probability <10% at age 30 vs. >50% at age 70 for identical chest pain + SOB). For high-disparity cases, require explicit justification: clinical guideline citation showing age-based epidemiology supports difference, not algorithmic bias. Root cause: Detects age-driven divergence and forces evidence-based justification.

3. **Calibrated age-adjusted prevalence priors from population epidemiology**: Rather than learning disease prevalence from training data (which may reflect biased past referral patterns), use published epidemiological studies to set priors: "Acute MI prevalence: 2/10K per year age 30-40, 50/10K per year age 60-70". Scale differential diagnoses based on these calibrated priors rather than training-data-learned patterns. Root cause: Prevents training-data-learned correlation bias by grounding in population epidemiology.

### Detection & Response

1. **Age-bias detection monitoring**: For each diagnosis or treatment recommendation, compute: (a) Recommendation if age unknown, (b) Recommendation given patient's actual age, (c) Delta = (b) - (a). Alert when delta >20% probability for any diagnosis (indicates age shifting recommendation substantially). Monthly report: "Diagnoses with age-bias delta >20%: [list]". Audit highest-delta cases for bias patterns.

2. **Outcome disparity monitoring by age**: Track outcomes stratified by age group: sensitivity, specificity, missed-diagnosis rate per age band. Alert when missed-diagnosis rate (e.g., "missed ACS") differs >1.5x between age groups (e.g., "ACS missed 3% of young patients, 2% of old patients" suggests under-detection in young). Escalate to clinical review for bias mitigation.

### Architecture Patterns

1. **Dual-Path Age-Invariant Interpreter**: Input: (symptom_profile, age, labs, imaging) → Process: (Path A) Age-blind reasoning: symptom + calibrated priors → differential_diagnoses_age_invariant. (Path B) Age-stratified refinement: apply epidemiology multipliers → differential_diagnoses_age_adjusted. Compare: if delta >20%, flag "[AGE BIAS CHECK]". Output: recommendation with both paths visible + bias flag.

2. **Fairness Validation Service**: Symptom-based comparison engine. Input: (symptom_set, age_range) → Generates recommendations for [age 30, 50, 70] → Computes divergence metrics → Flags high-disparity cases. Service integrates with recommendation approval workflow.

3. **Calibrated-Prevalence Database**: Population-epidemiology-sourced prevalence priors. Input: (condition, age_band) → Output: population_prevalence (from published studies, not training data). Updated annually from CDC, WHO epidemiology databases.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Age-Invariant Recommendation Consistency | >95% | <90% | % of symptom combinations where recommendations differ <10% across age groups [30, 50, 70, 90] |
| Age-Bias Delta Magnitude | <10% | >20% | Mean absolute difference in diagnosis probability when age is known vs. unknown (lower = less bias) |
| False-Negative Rate Ratio (Young:Old) | 1.0 (equal) | >1.5 | Missed-diagnosis rate age 20-40 / missed-diagnosis rate age 60-80 (ratio close to 1 = fair; >1.5 = bias against young) |
| High-Disparity Diagnoses | 0 | >5% | % of diagnosis categories with >20% probability change based solely on age (should be rare, only justified by epidemiology) |
| Outcome Disparity Audit | <5% | >10% | Difference in sensitivity/specificity between age groups (audited quarterly; flag >10% gaps) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Age-Driven Recommendation Divergence | Same symptom profile produces substantially different diagnosis/treatment based on age (delta >20%), insufficient epidemiologic justification | HIGH | Require explicit guideline citation justifying age-based difference; escalate to clinical review if not justified |
| Missed-Diagnosis Rate Disparity | Missed-diagnosis rate (e.g., ACS) differs >1.5x between age groups (e.g., young under-detected, elderly over-detected) | HIGH | Escalate to clinical leadership; audit cases with diagnosis disparity; consider model retraining with age-adjusted targets |
| Symptom-Pair Age Bias | Identical symptom profile (e.g., chest pain + SOB) receives different triage level or admission recommendation based on age alone | MEDIUM | Audit for fairness; require clinical justification for age-based difference; retrain or modify if bias confirmed |

---

## References

- [Age Bias in Medical AI](https://arxiv.org/abs/2007.04786)
- [Fairness in Diagnostic Systems](https://arxiv.org/abs/2102.13232)
