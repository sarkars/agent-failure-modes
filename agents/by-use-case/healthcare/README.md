# What Are the Most Common Healthcare AI-Agent Failures?

**Healthcare AI-agent failures cluster around nine clinical domains — diagnosis, treatment, medication safety, documentation, compliance — and within each domain, failures are not hallucinations or knowledge gaps but rather architectural blind spots: checks scoped too narrowly, information dropped at agent handoffs, data treated as ground truth without verification, or a model's learned pattern applied with inappropriate confidence to an individual case.** Across all nine goals, the pattern is the same: an agent can reason correctly within its scoped input, but the scoped input is narrower than the clinical reality it is supposed to represent.

## Key Takeaways

- 38 patterns documented across 9 clinical-domain goals reveal a recurring failure taxonomy orthogonal to model capability: scope gaps (checks exclude relevant data), handoff drops (findings identified upstream fail to reach downstream agents), retrieval mismatches (similarity search or fuzzy matching substitutes wrong-but-plausible data), and individualization gaps (generic defaults applied where patient- or context-specific overrides are needed).
- Multi-agent handoff failures account for 5 of 38 patterns — a recurring architectural problem where information established by one agent is lost or deprioritized when handed to the next.
- Demographic bias and atypical-presentation blindness in diagnosis recur because training data reflects historical healthcare biases (female underrepresentation in cardiac studies, elderly underrepresentation in acute-disease research), and models reproduce those biases without explicit debiasing intervention.
- Embedding-retrieval mismatches appear across three goals (adverse-drug-interaction, lab-result-interpretation, medication-reconciliation) and trace to the same root cause: similarity search over text (drug names, assay names) is used where exact-identifier matching is required.

## Healthcare Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Adverse Drug Interaction](goals/adverse-drug-interaction/) | Pairwise and multi-way interaction gaps, supplement exclusion, organ-function dosing, causal attribution | 7 |
| [Clinical Documentation](goals/clinical-documentation/) | Unverified allergy fields, upcoding/downcoding from inflated documentation | 2 |
| [Compliance & Liability](goals/compliance-liability/) | De-identification quasi-identifier risk, informed-consent source fidelity, consent-scope handoff drops | 3 |
| [Diagnosis Safety](goals/diagnosis-safety/) | Anchoring, demographic/presentation-type bias, history truncation, rare-disease misses, data-interpretation gaps | 10 |
| [Lab Result Interpretation](goals/lab-result-interpretation/) | Critical-value alert routing, reference-range retrieval mismatches, patient-identity verification | 3 |
| [Medication Reconciliation](goals/medication-reconciliation/) | Discharge reconciliation gaps, LASA drug substitution, interaction-flag handoff drops | 3 |
| [Mental-Health Triage](goals/mental-health-triage/) | Indirect risk-language blindness, risk-disclosure handoff drops | 2 |
| [Telehealth Triage](goals/telehealth-triage/) | Urgency-flag handoff drops, missing-vitals default-to-normal | 2 |
| [Treatment Planning](goals/treatment-planning/) | Care-goal drift, comorbidity neglect, guideline-conflict blindness, specialist-contraindication handoff drops, outdated guidelines, pediatric-dosing errors | 6 |

**Total: 38 patterns**

## How the Goals Relate

The nine healthcare goals are mostly parallel concerns rather than a strict pipeline, because a healthcare agent can fail at any domain independently of whether others succeeded. Diagnosis Safety failures in the assessment step do not determine whether Medication Reconciliation or Treatment Planning will succeed, though a missed diagnosis can certainly propagate into wrong recommendations downstream. To localize an incident by symptom: **an agent identifies the wrong diagnosis entirely → Diagnosis Safety**; **a drug-drug or condition-drug interaction is missed → Adverse Drug Interaction**; **a medication from home is silently omitted from discharge → Medication Reconciliation**; **a specialist-noted contraindication to a procedure approach is not incorporated into the final plan → Treatment Planning**; **a critical lab value is not immediately notified → Lab Result Interpretation**; **vital signs are missing and the acuity score defaults to normal → Telehealth Triage**; **a patient-specific care goal set in prior visit is silently overridden → Treatment Planning**; **risk factors disclosed during intake are not propagated to scheduling → Mental-Health Triage or Telehealth Triage**; **documentation inflates or misrepresents what was discussed → Clinical Documentation or Compliance & Liability**.

## Frequently Asked Questions

### How do healthcare AI-agent failures concentrate on scope gaps rather than model capability?
Models are often capable of reasoning correctly within a well-posed question; the failures documented here are not about reasoning but about what input reaches the reasoning step. A pairwise interaction checker works correctly; the problem is it was built to check pairwise interactions and never sees condition-based contraindications. A similarity-search lookup works correctly; the problem is it retrieves a name-similar but clinically distinct drug. An agent is asked to generate a note without source verification; it generates plausible-sounding boilerplate that the source never supported. Scope-gap failures are architecture and design questions, not capability questions.

### How do you reduce multi-agent handoff failures?
Require explicit, structured fields in handoff payloads for findings that downstream agents need to act on (risk flags, contraindications, narrowed consent scopes). Implement automated reconciliation checks comparing upstream reasoning against downstream schema fields before the handoff is considered complete. Require downstream agents to explicitly acknowledge or resolve any flag present in the handoff payload before issuing their own conclusion. Consider replacing agent-local conversational summaries with a single shared case record that both agents read from and write to.

### How does demographic bias recur across diagnosis and treatment?
Training data reflects historical healthcare biases: women are underrepresented in cardiovascular-disease research, so models learn "female + chest pain" as lower-risk; elderly patients are historically underrepresented in acute-disease studies, so models learn age-driven discounting of acuity. Without explicit debiasing — stratified training data, fairness constraints, demographic-stratified outcome auditing — models reproduce the training-data biases. Mitigate by ensuring representative training data, auditing outcomes by demographic stratum, and applying demographic-aware differential expansion or symptom-threshold adjustment at inference time.

### Can a single model update fix multiple patterns across different goals?
Only partially. Some fixes are architectural (add a field to a handoff schema, split a check into two stages); some are about data and training (representative training data, calibrating to indirect risk language); some are about governance (updating guidelines quarterly, maintaining a LASA-pair list). Across all 38 patterns, the recurring theme is that verification, grounding, and structured propagation matter more than model capability.

### How do you audit for healthcare AI-agent failures in production?
Implement stratified outcome monitoring across all nine domains: diagnostic accuracy stratified by demographic group and presentation type; medication error rates stratified by polypharmacy tier; critical-value notification latency; medication-reconciliation omission rates; multi-agent handoff completeness checks comparing upstream findings against downstream schema; care-plan goal continuity; guideline freshness. Establish clear alert thresholds for each domain so systematic failures are caught before they propagate to many patients.

## Related Categories

- [Document Processing](../document-processing/) — covers OCR and multimodal failures that upstream feed into clinical note extraction and EHR data quality
- [Knowledge Retrieval](../knowledge-retrieval/) — covers guideline retrieval, knowledge freshness, and citation accuracy failures that treatment-planning and diagnosis agents depend on
