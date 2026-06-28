# Patient History Truncation & Context Loss

## Issue: Medical Diagnosis Model Trained on Limited Patient History; Misses Patterns Evident Only in Full Longitudinal Record

**Frequency**: Common

**Symptoms**
- Model uses last 2 years of records; doesn't see 10-year history
- Chronic pattern (e.g., recurring infections) not detected
- Important past diagnosis missed because >2 years old
- Model can't reason about disease trajectory

**Root Cause**
Training data limited to recent history (cost, accessibility). Longitudinal medical records span decades; models trained on subsets miss patterns. Also, EHR systems often show only recent visits; full history requires manual dig. Models don't have access to complete history by default.

**Example**
```
Scenario: Recurrent infection diagnosis
Patient history:
- Age 20-30: Frequent sinusitis (treated with antibiotics)
- Age 30-40: Infections less frequent
- Age 40-50: Recurring infections restarted
- Age 50: New presentation (fever, cough)

Model trained on: Last 2 years data (doesn't see age 20-40 pattern)
Model diagnosis: "Probable new infection; treat with antibiotics"
Specialist review of full history: "Pattern of recurrence suggests immune deficiency; needs investigation not just antibiotics"

Impact: Wrong treatment path; chronic condition not identified
```

**Key Statistics**
- Relevant history beyond 2 years: 20-40% of diagnostic cases
- Longitudinal analysis impact: 10-30% improvement in accuracy
- History truncation error rate: 5-15%

---

## Mitigation Strategies

1. **Full History Access**: Ensure model has access to complete patient history
2. **Longitudinal Features**: Extract time-series features (trend, volatility) from full history
3. **Chronic Disease Models**: Separate models for chronic vs. acute conditions
4. **Pattern Mining**: Look for rare but important patterns in decade-long records

### Metrics
- Diagnosis accuracy with full vs. limited history (gap should be <5%)
- Chronic disease detection rate (should be >90%)
- Pattern discovery from long-term history

### Alerts
- Diagnosis changes when full history reviewed → History truncation issue

---

## References

- [Longitudinal Patient Data Analysis](https://arxiv.org/abs/2104.05762)
- [Chronic Disease Prediction with Time Series](https://arxiv.org/abs/2008.07267)
