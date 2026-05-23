# Confidence Miscalibration

## Issue: Overconfident Wrong Answers

**Frequency**: Very Common

**Symptoms**
- High confidence scores on incorrect extractions
- Confidence doesn't correlate with accuracy
- Cannot use confidence to route to human review

**Root Cause**
VLMs are trained to produce fluent outputs, not calibrated uncertainty estimates. They express certainty linguistically even when visually uncertain.

**Example**
```
Extraction: "Total: $5,847.00" (confidence: 0.97)
Actual document: "$5,347.00"

Result: High-confidence wrong answer bypasses review queue
```

**Mitigation Strategies**
1. **Confidence recalibration**: Post-hoc calibration on held-out set
2. **Ensemble disagreement**: Multiple models, use variance as uncertainty proxy
3. **Token-level confidence**: Examine per-token probabilities, not just final score
4. **Human-in-the-loop thresholds**: Set thresholds based on empirical accuracy, not raw scores
