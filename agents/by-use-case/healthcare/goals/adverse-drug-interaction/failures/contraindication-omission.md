# Contraindication Omission

## Issue: Agent Recommends or Approves a Medication Without Checking Patient-Specific Contraindications Beyond Drug-Drug Interactions

**Frequency**: Common

**Symptoms**
- Drug-drug interaction checks pass, but the model misses condition-based contraindications (e.g., beta-blockers in decompensated asthma, NSAIDs in renal failure)
- Allergy history present in the chart but not cross-checked against the recommended drug class
- Contraindications tied to lab values (e.g., QT-prolonging drugs with a known prolonged QTc) are not flagged because the agent only checks the medication list, not the full chart
- Pregnancy/lactation contraindications missed when the model's interaction check is scoped only to other medications

**Root Cause**
Most automated interaction-checking focuses narrowly on pairwise drug-drug interactions because that is the most structured and widely available dataset (RxNorm/DDI databases). Condition-based, lab-based, and demographic-based contraindications require integrating across the medication list, problem list, lab results, and patient demographics simultaneously — a broader reasoning task that narrow DDI-checking pipelines do not perform, and that general-purpose LLM agents may skip unless explicitly prompted to check each category.

**Example**
```
Scenario: Patient with chart-documented severe asthma and chronic renal insufficiency
New prescription: Non-selective beta-blocker for hypertension + standing NSAID for pain
Drug-drug interaction check: Passes (no interaction between the two new drugs)
Missed contraindications: Beta-blocker contraindicated in severe asthma; NSAID contraindicated in renal insufficiency
Impact: Risk of bronchospasm and further renal decline; both preventable with chart-aware contraindication checking
```

**Key Statistics**
- Condition-based contraindications are missed at a meaningfully higher rate than drug-drug interactions in systems that scope checking to medication-pair lookups only
- A substantial share of preventable adverse drug events in hospitalized patients stem from contraindications relative to a pre-existing condition, not drug-drug interactions
- Integrating problem-list and lab-value data into contraindication checking has been shown to materially increase detection of clinically significant contraindications versus medication-list-only checks

---

## Mitigation Strategies

### Prevention

1. **Mandatory multi-source contraindication matrix validation**: Implement a structured pre-prescription gate that requires explicit checking across five dimensions before recommendation: (a) medication-interaction matrix (DDI), (b) condition-contraindication lookup (patient problems + drug class), (c) lab-value range validation (renal function, QTc, LFTs), (d) allergy/intolerance database cross-check, (e) demographic rules (pregnancy, pediatric, geriatric). Fail-safe: if any dimension incomplete, return "cannot recommend - missing data" rather than proceed. Root cause mitigation: Prevents narrow DDI-only checking by enforcing breadth of constraint checking.

2. **Typed contraindication database with inheritance rules**: Build contraindication knowledge base indexed by: drug-class (not just single drug), condition (hierarchical: asthma → reactive-airway-disease), lab-ranges (eGFR <30, QTc >450ms), and demographic flags. Use RxNorm drug hierarchy to catch class-level contraindications. Root cause: Catches contraindications that would be missed by single-drug-code lookup.

3. **Chart-aware recommendation workflow with decision audit trail**: Modify recommendation generation to output structured justification: "Checked: [medication-list: OK], [problem-list: [asthma flagged]], [labs: [eGFR 25]], [allergies: OK], [demographics: OK]. Gate check result: [BLOCKED - beta-blocker contraindicated in asthma]". Require this audit trail visible to prescriber before approval. Root cause: Explicit enumeration prevents omission of key data sources.

### Detection & Response

1. **Contraindication detection stratified by source**: Instrument prescription recommendations to track: (a) % requiring DDI-only check (medication-list lookup), (b) % requiring condition-based check (problem-list), (c) % requiring lab-based check (vital-signs/labs). Alert when condition-based or lab-based checks are systematically skipped. Target: 100% of recommendations include all 5 dimensions checked.

2. **Adverse event root-cause attribution**: Post-adverse-event analysis: for each adverse event, retroactively check if known contraindication existed at recommendation time. Classify events by contraindication type (DDI, condition-based, lab-based). Alert when >2 events in 30 days share same missed contraindication type.

### Architecture Patterns

1. **Multi-Layer Contraindication Engine**: Centralized service with five rule layers: (1) PharmGKB DDI database, (2) Mayo-Clinic condition-contraindication taxonomy, (3) Lab-value rule engine (eGFR thresholds, QTc intervals), (4) Allergy database (SNOMED CT), (5) Demographic rules. Each layer returns [OK / WARN / BLOCK]. Recommendation blocked if any layer returns BLOCK.

2. **Chart-Aware Recommendation Gate**: Recommendation engine passes full chart context (medications, problems, labs, allergies, demographics) to contraindication service. Service returns structured decision with audit trail. Prescriber sees decision + rationale before approval.

3. **Lab-Triggered Rules Engine**: Automated rule generation from clinical guidelines: "IF eGFR < 30 THEN flag NSAIDs, ACE-inhibitors, certain antibiotics". Rules updated quarterly from current guidelines (UpToDate, KDIGO, etc.).

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Multi-Source Check Completeness | 100% | <99% | % of recommendations where all 5 dimensions (meds, problems, labs, allergies, demographics) explicitly checked |
| Condition-Based Contraindication Detection Rate | >95% | <90% | # of condition-contraindications correctly identified / total condition-contraindication opportunities |
| Lab-Value-Triggered Detection Rate | >95% | <90% | # of lab-triggered contraindications correctly identified / total lab-triggered opportunities (eGFR, QTc, LFTs, etc.) |
| Preventable Adverse Event Rate (Condition-Based) | <0.01% | >0.05% | # of adverse events caused by missed condition-contraindication / total prescriptions |
| Chart Completeness at Recommendation Time | >98% | <95% | % of recommendations made with complete chart data available (no missing problem-list, labs, or allergies) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Missing Multi-Source Check | Recommendation made without checking all 5 dimensions (detected via audit trail analysis) | CRITICAL | Flag recommendation for prescriber review; audit contraindication engine logs; potential mandatory review of all recent recommendations from same agent |
| Condition-Contraindication Missed | Patient chart shows problem (asthma, renal insufficiency) that contradicts recommended drug, but agent did not flag | CRITICAL | Halt similar recommendations; notify prescriber; pharmacist review required for future; escalate to pharmacy committee |
| Lab-Triggered Rule Bypass | Lab value (eGFR <30, QTc >450ms) present in chart but contraindication not flagged for guideline-specified drugs | CRITICAL | Investigate contraindication engine; potential patient safety issue; retrospective chart review for similar cases |

---

## References

- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
