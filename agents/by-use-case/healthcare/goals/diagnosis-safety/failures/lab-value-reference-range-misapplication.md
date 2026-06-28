# Lab-Value Reference-Range Misapplication

## Issue: Agent Applies Generic Adult Reference Ranges to Lab Values Without Adjusting for Age, Sex, Pregnancy, or Assay-Specific Ranges

**Frequency**: Common

**Symptoms**
- Pediatric or geriatric lab values flagged as "normal" or "abnormal" using standard adult reference ranges
- Pregnancy-altered lab values (e.g., physiologic anemia, altered thyroid panels) misinterpreted as pathological
- Sex-specific reference ranges (e.g., creatinine, hemoglobin) not applied, causing systematic over- or under-flagging in one sex
- Cross-lab assay differences (different units or methods) ignored, causing values to be compared against the wrong range entirely

**Root Cause**
Reference ranges are not universal constants; they vary by age, sex, pregnancy status, and even by the specific assay/instrument used by the lab. Models trained on generic adult reference tables, or that fail to parse the specific reference range printed on the lab report itself, apply a one-size-fits-all threshold that produces both false positives and false negatives across populations whose physiology deviates from the "standard" adult range.

**Example**
```
Scenario: Pregnant patient's lab report shows hemoglobin 10.8 g/dL
Standard adult reference range: 12.0-15.5 g/dL (flagged as anemic)
Pregnancy-adjusted range (2nd trimester): 9.5-15.0 g/dL (within normal physiologic range)
Model action: Flags "anemia," recommends iron supplementation work-up
Reality: Value reflects normal pregnancy-related hemodilution
Impact: Unnecessary work-up, patient anxiety, potential masking of an actually abnormal trend if baseline is reset incorrectly
```

**Key Statistics**
- Sex-specific and age-specific reference range misapplication is a recurring source of false-positive lab flagging in automated clinical decision support audits
- Pregnancy-related physiologic lab shifts are frequently missed by generic reference-range logic, leading to unnecessary work-ups in a non-trivial share of obstetric chart reviews
- Cross-assay unit/method mismatches (e.g., different creatinine assay methods) account for a measurable share of lab-interpretation errors in multi-lab health systems

**Contributing Factors**
- Reference ranges hardcoded rather than parsed from the lab report's own stated range
- No structured capture of pregnancy status, age, or sex feeding into the interpretation step
- Multiple lab vendors with different assay methods feeding a single patient record

---

## Mitigation Strategies

1. **Report-Sourced Reference Ranges**: Always parse and use the reference range printed on the specific lab report rather than a hardcoded generic table
2. **Demographic-Conditional Range Selection**: Explicitly select age/sex/pregnancy-adjusted reference ranges based on structured patient data before flagging abnormal values
3. **Assay-Method Awareness**: Track which lab/assay method produced each value and avoid cross-comparing values from incompatible methods
4. **Trend-Over-Threshold**: Weight within-patient trend changes alongside absolute reference-range flagging, since a "normal" value that is a sharp change from baseline can still be clinically significant

### Metrics
- False-positive abnormal-flag rate stratified by demographic adjustment applied vs. not applied
- % of lab interpretations using report-sourced vs. hardcoded reference ranges
- Cross-assay mismatch detection rate

### Alerts
- Pregnancy status on file but pregnancy-adjusted range not applied → P2
- Lab value flagged abnormal using a reference range that doesn't match the report's stated range → P1

---

## References

- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
