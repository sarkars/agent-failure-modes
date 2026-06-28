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
