# What Are the Most Common Diagnosis-Safety Failures in AI Agents?

**Diagnosis-safety failures happen when an agent's differential diagnosis or working hypothesis becomes progressively harder to revise or expand as new information arrives, or when that hypothesis is biased toward or against certain demographics or presentation types before any clinical evidence is even considered.** Diagnosis-safety failures are not hallucination failures where an agent makes up a diagnosis — they are cognitive-bias failures where an agent learns a statistical pattern from training data ("young + chest pain = anxiety more often than cardiac") and applies it with inappropriate confidence to an individual case, or where an agent reasoning over a multi-turn conversation anchors on an early hypothesis and reinterprets new, contradictory findings to preserve that anchor.

## Key Takeaways

- 10 patterns are documented, splitting into four cognitive-bias mechanisms: anchoring/confirmation bias (2 patterns), demographic and presentation-type bias (3 patterns), information-loss and truncation (2 patterns), and data-interpretation gaps (3 patterns).
- Anchoring on a first diagnosis or on a prior note's label is among the most frequently cited diagnostic failure modes in both human and LLM-assisted reasoning, and multi-turn case vignettes show measurably higher diagnostic accuracy when agents are prompted to explicitly regenerate a fresh differential at each information update.
- Atypical presentations — common in women, elderly, and underrepresented populations — appear less frequently in clinical training corpora and case-report literature, so the model's learned symptom-to-diagnosis mapping is systematically skewed toward majority-pattern presentations, reproducing documented healthcare disparities.
- Radiology report discrepancies and imaging-follow-up drops happen because summarization agents optimize for terse output and drop qualifying language in the report body ("cannot exclude," "recommend follow-up in 6 weeks") that frequently carries the actionable next step.

## Scope

- **Anchoring and confirmation bias** — [Anchoring Bias on First Diagnosis](failures/anchoring-bias-first-diagnosis.md), [Confirmation Bias from Prior Notes](failures/confirmation-bias-from-prior-notes.md). Autoregressive generation conditions each token on prior context, including the agent's own earlier assertions; once a diagnosis is stated early, subsequent generations are biased toward consistency with that prior assertion rather than performing a fresh Bayesian update. The problem recurs at two levels: within a single multi-turn conversation and across multiple encounters when a prior note's label propagates as an anchor.
- **Demographic and presentation-type bias** — [Age Bias in Symptom Interpretation](failures/age-bias-in-symptoms.md), [Atypical Presentation Blindness](failures/atypical-presentation-blindness.md), [Demographic Bias](failures/demographic-bias.md). Models learn statistical patterns from training data that correlate demographic features (age, sex, race) and presentation type (textbook vs. atypical) with diagnoses, and apply those correlations with confidence even in individual cases where the correlation is not mechanistically justified, reproducing training-data skew as systematic healthcare disparities.
- **Information loss and truncation** — [Patient History Truncation & Context Loss](failures/patient-history-truncation.md), [Lab-Value Reference-Range Misapplication](failures/lab-value-reference-range-misapplication.md). Agents with access to limited history miss longitudinal patterns; agents that apply generic reference ranges to subpopulations with different physiology (pediatric, geriatric, pregnant patients) flag normal values as abnormal and miss clinically significant trends.
- **Data interpretation and integration gaps** — [Imaging Report Discrepancy Blindness](failures/imaging-report-discrepancy-blindness.md), [Rare Disease Misses](failures/rare-disease-misses.md), [Symptom Attribution Bias](failures/symptom-attribution-bias.md). Data-interpretation-and-integration-gap patterns reflect either dropped data (radiology follow-up recommendations), structural data mismatch (class imbalance leaving rare disease underrepresented), or misweighted evidence integration (anchoring to a single symptom and under-weighting contradictory findings).

## When Diagnosis-Safety Matters

- Multi-turn conversational diagnostic reasoning where new information arrives across multiple exchanges and prior assertions can anchor the reasoning
- Longitudinal care where a prior note's diagnosis label propagates unchecked into new encounters
- Differential diagnosis generation for rare, atypical, or demographically underrepresented presentations where training-data skew is most likely

## Cross-Pattern Insight

Every diagnosis-safety pattern documented here reflects a gap between how a model learns from training data and how a diagnostic decision should be made. Models learn statistical patterns efficiently ("young patients with chest pain are usually not having heart attacks"), but apply those patterns with inappropriate confidence in individual cases, or apply them rigidly even when presented with contradictory evidence. Models trained on skewed datasets reproduce those skews ("atypical MI presentations were underrepresented in my training data, so I weight them lower now"). The recurring mitigation is the same across all patterns: force periodic de-biasing resets (explicit differential re-ranking at each information update), bring unrepresented populations into the reasoning path (demographic-aware differential expansion, atypical-pattern case augmentation), and make information loss visible (access to full history, explicit representation of missing data rather than imputation to normal).

## Frequently Asked Questions

### How do you detect and fix anchoring bias in a multi-turn diagnostic conversation?
Force a fresh differential-diagnosis regeneration every 2-3 new information items, explicitly discarding prior assertions; red-flag situations where a new symptom contradicts prior reasoning, rather than rationalizing it as "consistent" with prior diagnosis; and implement a devil's-advocate reasoning pass asking "what if the leading diagnosis is wrong?" to surface competing alternatives.

### Can demographic bias in diagnostic models be eliminated?
It can be substantially reduced but never to zero without deliberate mitigation. Stratify training data to represent minorities and underrepresented populations proportionally; use fairness constraints during training to enforce equal sensitivity/specificity across demographic groups; and audit diagnostic accuracy explicitly by demographic stratum. But the underlying pattern — that training data reflects past healthcare system biases — remains, so ongoing monitoring and re-training are necessary.

### How do agents miss rare diseases when more common diagnoses fit the symptoms?
Training data imbalance: common diseases vastly outnumber rare ones, so models learn "most likely" as "most common." Add a specialist rare-disease screening model (trained with oversampled rare-disease cases) that activates when confidence is low or when red-flag symptoms are present; maintain hard-coded clinical-guideline rules for rare-disease triggers (e.g., "hypermobility + easy bruising + skin elasticity → must consider Ehlers-Danlos").

### What causes atypical-presentation underdiagnosis?
Atypical presentations — common in women, elderly, and underrepresented populations — appear less frequently in training corpora, so the model's learned symptom-to-diagnosis mapping is skewed toward majority-pattern presentations. Mitigate by explicitly curating and oversampling atypical-presentation case data, adjusting symptom thresholds by demographic group, and including few-shot atypical-presentation examples in each diagnostic session.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Age Bias in Symptom Interpretation](failures/age-bias-in-symptoms.md) | Diagnosis probability shifts substantially based on age alone, without epidemiologic justification |
| [Anchoring Bias on First Diagnosis](failures/anchoring-bias-first-diagnosis.md) | Model fixates on initial diagnosis despite contradicting later evidence; differential ranking never re-opened |
| [Atypical Presentation Blindness](failures/atypical-presentation-blindness.md) | Atypical but correct presentations missed because training data over-represents textbook cases |
| [Confirmation Bias from Prior Notes](failures/confirmation-bias-from-prior-notes.md) | Prior visit diagnosis label anchors agent; new contradictory findings reinterpreted as consistent with prior |
| [Demographic Bias](failures/demographic-bias.md) | Diagnostic accuracy differs substantially across demographic groups due to training-data skew |
| [Imaging Report Discrepancy Blindness](failures/imaging-report-discrepancy-blindness.md) | Radiology impression extracted but qualifying language, follow-up recommendations, and comparison-to-prior changes dropped |
| [Lab-Value Reference-Range Misapplication](failures/lab-value-reference-range-misapplication.md) | Generic adult reference ranges applied to pediatric, geriatric, or pregnant patients without adjustment |
| [Patient History Truncation & Context Loss](failures/patient-history-truncation.md) | Limited access to longitudinal history misses chronic patterns evident only in full decade-long records |
| [Rare Disease Misses](failures/rare-disease-misses.md) | Model confident on common diagnosis for rare disease; rare-disease patterns underrepresented in training |
| [Symptom Attribution Bias](failures/symptom-attribution-bias.md) | Model overweights early symptom evidence; fails to properly update differential as new contradictory symptoms arrive |

**Total: 10 patterns**

## Related Goals

- [Lab Result Interpretation](../lab-result-interpretation/) — handles reference-range and lab-identity issues at higher detail; shares demographic-adjustment mechanisms with diagnosis-safety
- [Treatment Planning](../treatment-planning/) — planning failures often cascade from missed or biased diagnoses
