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

1. **Multi-Source Contraindication Checking**: Cross-reference new prescriptions against medication list, problem list, allergy list, lab values, and demographics — not medication-pairs alone
2. **Condition-Drug Contraindication Database**: Maintain and query a structured condition-to-drug-class contraindication table (not just drug-drug)
3. **Lab-Triggered Contraindication Rules**: Encode lab-value-based rules (renal function, QTc, liver function) that trigger contraindication flags independent of the medication list
4. **Full-Chart Review Requirement**: Require the agent to explicitly enumerate which chart sections (meds, problems, allergies, labs, demographics) were checked before approving a prescription recommendation

### Metrics
- % of contraindication checks that include problem-list and lab-value cross-referencing
- Contraindication detection rate stratified by source type (DDI vs. condition-based vs. lab-based)
- Preventable adverse drug event rate attributable to missed condition-based contraindications

### Alerts
- New prescription recommended without problem-list cross-check → P1
- Lab-value-triggered contraindication present but not flagged → P1

---

## References

- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
