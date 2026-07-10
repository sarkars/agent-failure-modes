# Atypical Presentation Blindness

## Issue: Model Trained Predominantly on "Textbook" Symptom Presentations Misses Atypical Presentations Common in Women, Elderly, and Diverse Populations

**Frequency**: Common

**Symptoms**
- Classic-presentation diagnoses (e.g., crushing chest pain for MI) are recognized; atypical equivalents (fatigue, nausea, jaw pain) are missed or under-prioritized
- Elderly patients with blunted or absent typical symptoms (e.g., silent MI, afebrile sepsis) receive lower urgency triage
- Diagnostic confidence is highest for presentations matching majority-population training data patterns
- Differential diagnosis lists rank atypical-but-correct conditions below typical-but-incorrect ones

**Root Cause**
Clinical training corpora and case-report literature historically over-represent "classic" presentations and the demographic groups most studied in the foundational literature (disproportionately middle-aged men for cardiovascular disease, for example). Atypical presentations — common in women, the elderly, and underrepresented populations — appear less frequently in training data, so the model's learned symptom-to-diagnosis mapping is systematically skewed toward majority-pattern presentations.

**Example**
```
Scenario: 58-year-old woman presents with fatigue, indigestion, and mild back pain
Model differential: GERD, musculoskeletal strain, anxiety (ranked highest)
Missing consideration: Atypical MI presentation, common in women, ranked low or absent
Actual diagnosis: Acute coronary syndrome
Impact: Delayed cardiac workup; treatment delay increases morbidity risk
```

**Key Statistics**
- Atypical-presentation underdiagnosis is a well-documented disparity in cardiovascular care for women, and LLM diagnostic models trained on literature reflecting this disparity reproduce it
- Diagnostic accuracy on atypical-presentation case vignettes is measurably lower than on textbook-presentation vignettes across published LLM medical-reasoning benchmarks
- Silent/blunted presentations in elderly patients (afebrile sepsis, painless MI) are systematically under-triaged when symptom checklists assume typical presentation thresholds

---

## Mitigation Strategies

1. **Atypical-Presentation Training Augmentation**: Explicitly curate and oversample atypical-presentation case data across demographics in fine-tuning and few-shot prompting
2. **Demographic-Aware Differential Expansion**: When patient demographics match a population known for atypical presentation (women, elderly), force inclusion of high-risk conditions even with atypical symptom profiles
3. **Symptom-Threshold Adjustment by Demographic**: Lower the symptom-severity threshold for triggering urgent workup in populations known for blunted presentations
4. **Bias Audit on Case Vignette Suite**: Regularly test diagnostic accuracy stratified by demographic presentation type, not just aggregate accuracy

### Prevention

1. **Demographic-aware differential expansion with atypical-pattern prioritization**: Implement gating: on patient intake, system identifies demographic risk factors (age >65, female gender for cardio, etc.) known to present atypically for high-risk diagnoses. For these patients, FORCE inclusion in differential of high-mortality diagnoses (MI, sepsis, PE, stroke) even if symptom profile is atypical. Example: "58F with fatigue + indigestion → even without classic chest pain, ACS must be included in differential at high rank". Use clinical literature (e.g., AHA guidelines on women's ACS presentations) to define atypical-pattern triggers. Root cause mitigation: Prevents majority-pattern bias by explicitly listing atypical-presentation conditions for at-risk demographics.

2. **Demographic-stratified symptom-threshold adjustment**: Encode demographic-specific sensitivity settings for diagnostic thresholds: "Elderly patients: lower fever threshold for sepsis (afebrile sepsis common); women: lower chest-pain threshold for ACS (fatigue, nausea more common)". Implement as model-input instruction or as hard-coded rules: "Patient age >70 + elevated WBC alone → consider sepsis workup (no fever required)". Root cause: Catches presentations that would be under-triaged under majority-population thresholds.

3. **Atypical-presentation case data augmentation in few-shot prompting**: In each diagnostic session, include few-shot examples of atypical presentations for high-risk conditions stratified by patient demographic: "Here are 3 examples of MI in women with atypical presentations (fatigue, indigestion)...". This in-context learning corrects training-data skew. Root cause: Compensates for training-corpus over-representation of typical presentations.

### Detection & Response

1. **Demographic-stratified diagnostic accuracy audit logging**: For every diagnosis, log: (a) patient demographics (age, gender), (b) presentation type (typical vs. atypical for that diagnosis), (c) differential diagnosis ranking, (d) whether high-mortality conditions included in differential despite atypical presentation, (e) actual outcome (correct/missed diagnosis). Quarterly audit: compute diagnostic accuracy stratified by demographic + presentation type. Alert if accuracy on atypical presentations <90% (vs. typical >95%).

2. **Presentation-pattern cohort tracking**: Track cases by presentation type (typical MI, atypical MI, etc.). Compare diagnostic accuracy and time-to-diagnosis by cohort. Alert on disparities: "Atypical-MI detection rate: women 70%, men 85% → demographic disparity detected; escalate to clinical review".

### Architecture Patterns

1. **Demographic-Risk Stratifier**: On patient intake, computes demographic risk profile. Input: (age, gender, comorbidities) → Output: (atypical_presentation_risk_list: ["MI_atypical", "sepsis_afebrile", ...], adjusted_symptom_thresholds). Routes patient to appropriate diagnostic pathway.

2. **Atypical-Pattern Differential Enforcer**: Input: (demographic_risk_list, symptom_profile) → Forces inclusion of high-risk diagnoses per demographic pattern regardless of symptom "fit" → Applies demographic-specific thresholds → Output: differential_diagnosis with atypical conditions prioritized.

3. **Presentation-Stratified Audit Engine**: Tracks diagnostic outcomes by (demographic, presentation_type) cohort. Computes accuracy per stratum. Generates alerts on disparities and surfaces for clinical review.

### Metrics
- Diagnostic accuracy stratified by typical vs. atypical presentation
- Diagnostic accuracy stratified by demographic group
- Rank position of correct diagnosis in differential for atypical cases

### Alerts
- Atypical-presentation diagnostic accuracy >15pp below typical-presentation accuracy → P2
- High-risk condition (MI, sepsis) absent from top-5 differential for at-risk demographic with compatible atypical symptoms → P1

---

## References

- [Automating Expert-Level Medical Reasoning Evaluation of Large Language Models](https://arxiv.org/abs/2507.07988)
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
