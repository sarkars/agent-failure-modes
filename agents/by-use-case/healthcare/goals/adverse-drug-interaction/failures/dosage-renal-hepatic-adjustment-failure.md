# Dosage Renal/Hepatic Adjustment Failure

## Issue: Agent Recommends Standard Adult Dosing Without Adjusting for Impaired Renal or Hepatic Clearance

**Frequency**: Very Common

**Symptoms**
- Standard dose recommended despite chart-documented low eGFR or elevated liver enzymes
- Model checks for drug-drug interactions but not for organ-function-based dosing adjustments
- Renally-cleared drugs (e.g., certain antibiotics, anticoagulants) dosed without referencing creatinine clearance
- Hepatically-metabolized drugs dosed without considering Child-Pugh class in patients with documented cirrhosis

**Root Cause**
Dose adjustment for renal or hepatic impairment requires combining a drug's pharmacokinetic profile with patient-specific lab values (eGFR, creatinine clearance, liver function tests) and applying drug-specific adjustment tables (which are often nonlinear, not a simple percentage reduction). General-purpose recommendation agents frequently default to label-standard adult dosing because that is the most common pattern in training data, and they lack a forced step that queries the patient's renal/hepatic function before finalizing a dose.

**Example**
```
Scenario: Patient with eGFR 25 mL/min/1.73m^2 (stage 4 CKD) needs an anticoagulant for new-onset AFib
Model recommendation: Standard full-dose anticoagulant per label
Correct approach: Renally-adjusted reduced dose per CKD-specific dosing table, or alternative agent
Impact: Drug accumulation risk, bleeding complications, preventable with eGFR-based dose adjustment
```

**Key Statistics**
- Renal dose-adjustment omission is among the most frequently cited categories of preventable medication errors in patients with chronic kidney disease
- A meaningful share of hospitalized patients with significant renal impairment receive at least one medication at an inappropriately high dose for their renal function in chart-review studies
- Hepatic dose-adjustment errors are similarly common for drugs with high first-pass hepatic metabolism in patients with documented cirrhosis or elevated liver enzymes

---

## Mitigation Strategies

1. **Mandatory Renal/Hepatic Function Lookup**: Require the agent to retrieve current eGFR/creatinine clearance and liver function tests before finalizing any dose for renally- or hepatically-cleared drugs
2. **Drug-Specific Adjustment Tables**: Encode structured, drug-specific renal/hepatic dose-adjustment tables rather than applying a generic percentage reduction
3. **Alternative-Agent Suggestion**: When a drug has no safe adjustment for the patient's organ function, surface alternative agents with more favorable clearance profiles
4. **Dose-Adjustment Audit Trail**: Log which renal/hepatic values were used and which adjustment table was applied, for clinical review

### Metrics
- % of renally/hepatically-cleared drug recommendations with documented organ-function check
- Inappropriate-dose rate stratified by renal/hepatic function category
- Time from new lab result (eGFR/LFT change) to re-evaluation of existing dosing

### Alerts
- Renally-cleared drug recommended with no eGFR check in chart → P1
- Recommended dose exceeds adjustment-table maximum for documented renal/hepatic function → P1

---

## References

- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
