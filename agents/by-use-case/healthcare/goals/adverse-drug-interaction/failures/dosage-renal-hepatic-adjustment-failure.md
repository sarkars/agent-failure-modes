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

### Prevention

1. **Mandatory organ-function gating before dose recommendation**: Implement a required pre-recommendation gate that triggers only after: (a) Drug's clearance profile is identified (renal % vs. hepatic %), (b) Patient's current lab values retrieved (eGFR from last 30 days, AST/ALT/bilirubin from last 30 days), (c) Drug-specific adjustment table selected from indexed database. Fail-safe: if organ-function data missing, return "cannot dose - missing renal/hepatic function labs" instead of defaulting to standard adult dose. Root cause mitigation: Prevents reliance on training-data-learned standard dosing by enforcing explicit lab-based override logic.

2. **Typed drug-specific adjustment tables with non-linear mappings**: Build centralized dose-adjustment library indexed by: drug name, clearance route (renal/hepatic), and parametric dosing rules. For renal: map eGFR ranges to percent-of-standard-dose (e.g., "eGFR 30-50 → 75% dose; eGFR <30 → 50% dose or contraindicated"). For hepatic: map Child-Pugh class to dose adjustments. Use pharmaceutical compendia (Micromedex, UpToDate, drug-package-inserts) as source of truth. Root cause: Avoids generic percentage reductions by encoding nonlinear, drug-specific rules.

3. **Alternative-agent recommendation with clearance hierarchy**: When recommended drug cannot be safely dosed for patient's organ function, surface tier-1 alternatives with more favorable clearance profiles (e.g., "Patient eGFR 20: contraindicated for Ciprofloxacin; suggest Levofloxacin (50% renally cleared) or Moxifloxacin (hepatic metabolism)"). Root cause: Prevents "no safe dose exists" dead-ends by proactively suggesting alternatives.

### Detection & Response

1. **Organ-function check instrumentation**: For every drug recommendation with expected renal/hepatic clearance, log: (a) drug name, (b) patient's eGFR and LFTs, (c) which adjustment table was applied, (d) recommended dose, (e) rationale. Alert when adjustment tables not applied despite clearance pathway indicating need. Target: 100% of renally/hepatically-cleared drugs show documented organ-function check in audit logs.

2. **Lab-update-triggered dose re-evaluation**: When new lab results (eGFR decline, LFT elevation) recorded in chart, automatically flag existing prescriptions that may need dose adjustment. Run batch job daily to identify patients with eGFR change >10 points in past 7 days; flag for pharmacist review. Target: Re-evaluation completed within 24 hours of significant lab change.

### Architecture Patterns

1. **Organ-Function Clearance Classification Engine**: Indexed database of drugs with metadata: {drug_name, routes_of_elimination: [{route: "renal", percent: 80}, {route: "hepatic", percent: 20}], adjustment_tables: {renal: [...], hepatic: [...]}}. Before dosing, classification engine returns required organ-function parameters and corresponding adjustment table.

2. **Parametric Dose Adjustment Service**: Input: (drug_name, patient_eGFR, patient_child_pugh_class) → Output: (adjusted_dose, rationale, confidence_level). Service queried synchronously before recommendation finalized. Backed by Micromedex and drug-package-insert data, updated quarterly.

3. **Lab-Change Alert Service**: Batch job monitoring lab results table. On eGFR change >10 or LFT elevation >20% of ULN, flags all active prescriptions for drugs requiring dose adjustment in this new organ-function state. Creates task for clinical pharmacist.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Organ-Function Check Completeness | 100% | <99% | % of renally/hepatically-cleared drug recommendations with documented organ-function lookup in audit log |
| Dose Appropriateness Rate | >99% | <98% | # of doses matching adjustment-table recommendation / total doses for renally/hepatically-cleared drugs |
| eGFR-Adjusted Dosing Accuracy | >98% | <95% | # of doses matching eGFR-specific table entries / total renal-cleared drug recommendations |
| Child-Pugh-Adjusted Dosing Accuracy | >98% | <95% | # of doses matching Child-Pugh class / total hepatically-cleared drugs in patients with cirrhosis/elevated LFTs |
| Lab-Change Response Time | <24 hours | >48 hours | Time from significant lab change to pharmacist review of affected prescriptions |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Renally-Cleared Drug Without eGFR Check | Drug recommended with renal clearance >50% but no eGFR lookup documented in audit trail | CRITICAL | Block recommendation; require eGFR lookup and dose adjustment before prescriber sees recommendation |
| Dose Exceeds Adjustment Table Maximum | Recommended dose exceeds maximum allowed for patient's documented organ function (eGFR, Child-Pugh) | CRITICAL | Alert to prescriber; require pharmacist override with explicit justification; escalate if override given |
| Lab Change Not Triggering Re-evaluation | eGFR declined >10 points or LFT elevated >20% in past 7 days; existing prescriptions not flagged for re-evaluation | HIGH | Auto-generate pharmacist task; review all renal/hepatic-cleared drugs for potential dose adjustment |

---

## References

- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
