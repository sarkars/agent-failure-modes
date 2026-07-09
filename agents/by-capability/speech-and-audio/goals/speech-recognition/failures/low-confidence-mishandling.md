# Low Confidence Mishandling

## Issue: ASR Confidence Scores Not Used Effectively

**Frequency**: Common

**Symptoms**
- Low-confidence transcriptions treated as certain
- Agent acts on uncertain input without verification
- High-confidence errors not caught
- Confidence thresholds poorly calibrated
- No graceful handling of uncertain speech

**Root Cause**
ASR systems provide confidence scores, but applications often ignore them or use them incorrectly. A transcription with 40% confidence is treated the same as one with 99%. Alternatively, thresholds are miscalibrated—rejecting good transcriptions or accepting poor ones. Confidence scores themselves may be poorly calibrated to actual accuracy.

**Example**
```
Scenario: Voice banking with confidence scores

Transaction 1:
  User: "Transfer five hundred dollars" (clear audio)
  ASR: "Transfer five hundred dollars" (confidence: 0.95)
  Action: Transfer executed ✓

Transaction 2:
  User: "Transfer [mumbled] dollars" (unclear)
  ASR: "Transfer fifteen dollars" (confidence: 0.45)
  Action: Transfer executed ← Should have verified!
  
Transaction 3:
  User: "Transfer fifty dollars" (background noise)
  ASR: "Transfer fifty dollars" (confidence: 0.52)
  Action: Transfer executed
  Actual intent: "Transfer fifteen dollars"
  
Confidence analysis:
  Transcriptions with confidence < 0.6: 18%
  Accuracy when confidence < 0.6: 62%
  Accuracy when confidence > 0.9: 97%
  
  Actions taken on low-confidence: 100% (no threshold)
  Errors from low-confidence actions: 38%
  
Potential savings with 0.7 threshold:
  Errors prevented: 340/month
  Customer complaints avoided: 85
  False verifications added: 120 (acceptable overhead)
```

**Key Statistics**
From Confidence Research (2026):
- 15-20% of transcriptions have confidence < 0.6
- Low-confidence accuracy: 50-70% (vs. 95%+ for high)
- 70% of voice agents ignore confidence scores
- Proper thresholding reduces errors by 30-50%
- Confidence calibration drift: common without monitoring

**Confidence Handling Failures**
| Failure | Description | Impact |
|---------|-------------|--------|
| Ignoring confidence | No threshold used | Errors from uncertain input |
| Threshold too low | Accepts poor transcriptions | High error rate |
| Threshold too high | Rejects good transcriptions | User frustration |
| Poor calibration | Confidence doesn't match accuracy | Wrong decisions |
| No fallback | No action for uncertain cases | Silent failures |

**Contributing Factors**
- Confidence scores not exposed by ASR
- Application ignores available confidence
- No threshold tuning process
- Static thresholds (not adaptive)
- No confidence monitoring
- Poor understanding of confidence meaning

## Mitigation Strategies

### Prevention
1. **Empirical Confidence Threshold Calibration**: Build confidence calibration curves using held-out validation set: plot confidence scores vs. actual accuracy at each decile. Identify optimal threshold that maximizes F1 score (balances false positives from low-confidence rejects vs. false negatives from accepted errors). For applications with asymmetric costs (financial transactions: P(false accept) > P(false reject)), set threshold to minimize high-cost errors. Implement per-domain thresholds: banking (0.75), e-commerce (0.70), navigation (0.60). Recalibrate monthly using rolling accuracy data.
2. **Confidence Score Normalization & Re-calibration**: ASR confidence scores often poorly calibrated (model overconfident on errors, underconfident on correct). Apply post-hoc calibration: train scaling function (temperature scaling, isotonic regression) on validation set to map raw ASR confidence to true probability. Implement per-context calibration: calibrate separately for clean audio vs. noisy, different domains, different acoustic conditions. Validate calibrated scores using reliability diagrams (Expected Calibration Error <5%).
3. **N-Best Hypothesis Scoring**: Don't rely on single best hypothesis. Generate N-best hypotheses (typically 3-5) with individual confidence scores. Implement confidence aggregation: if top 3 hypotheses have similar high confidence but differ substantially (e.g., two high-confidence candidates), flag for confirmation. Use hypothesis diversity as uncertainty signal. If only 1 hypothesis has high confidence but others low, treat as confident. Implement semantic consistency checking: if multiple hypotheses yield same semantic meaning despite different wording, increase confidence.

### Detection & Response
1. **Confidence Calibration Monitoring**: Track Expected Calibration Error (ECE) and Brier score daily. Compute calibration curves (actual accuracy vs. predicted confidence at each decile). Alert if ECE increases >5% from baseline (indicates miscalibration/model drift). Separately track calibration for different acoustic conditions (SNR buckets, speaker types). Monthly detailed audit: sample 200 transcriptions across confidence bands, measure actual accuracy, verify calibration curve matches training calibration.
2. **Low-Confidence Decision Tracking**: Monitor actions taken on low-confidence transcriptions (<70%). Segment by confidence band: 40-50%, 50-60%, 60-70%. For each band, track subsequent user corrections/complaints. Target: <5% error rate on low-confidence transcriptions even with confirmation. Alert if error rate on low-confidence actions >10%. Use this feedback to retrain confidence calibration model.
3. **Confidence Score Distribution Anomaly Detection**: Establish baseline distribution of confidence scores (histogram) on daily basis. Monitor for shifts: sudden increase in low-confidence transcriptions (might indicate audio quality issues), collapse of confidence range (might indicate broken confidence module). Alert if mean confidence drops >5% or variance increases >20% in 1-hour window.

### Architecture Patterns
1. **Tiered Confidence-Based Fallback Ladder**: Implement routing based on confidence tiers: (1) Confidence >0.80 → auto-execute action; (2) 0.65-0.80 → request lightweight confirmation ("Did you say yes?" button tap); (3) 0.50-0.65 → ask user to repeat or offer text input; (4) <0.50 → escalate to human or error message. For critical domains (healthcare, finance), raise all thresholds by 0.1. Implement domain-specific routing: some operations (information retrieval) allow lower thresholds, others (money transfer) require higher.
2. **Confidence-Aware NLU/Intent Model**: Integrate ASR confidence into downstream NLU. Instead of hard decision, pass confidence score to NLU model. Use confidence as feature: NLU should learn that low-confidence transcriptions need higher semantic certainty for action. Implement joint optimization: train NLU to output action confidence that combines ASR confidence + semantic confidence. Only execute action if combined confidence >threshold.
3. **Acoustic Quality Feedback Loop**: Monitor acoustic signal-to-noise ratio (SNR) or other quality metrics from audio stream. Use quality estimate to adjust confidence thresholds dynamically: noisy audio (SNR <15dB) → raise confidence threshold; clean audio (SNR >25dB) → lower confidence threshold. Implement soft adjustment: scale confidence scores by quality factor (e.g., confidence_adjusted = confidence * (1 - 0.3 * noise_factor)).

### Metrics
1. **confidence_calibration_error**: Target: Expected Calibration Error (ECE) <5%. Measure: average |predicted_confidence - actual_accuracy| across confidence bins. Alert: ECE >8%.
2. **low_confidence_error_rate_percent**: Target: <5% errors on transcriptions with 50-70% confidence, <2% on 70-80% confidence. Measure: errors_in_confidence_band / total_in_band. Alert: >8% on any band.
3. **confidence_threshold_f1_score**: Target: F1 score of threshold decision (correct accept/reject) > 0.85. Measure: F1 = 2 * (precision * recall) / (precision + recall). Alert: F1 <0.75, indicates threshold miscalibration.
4. **actions_on_low_confidence_percent**: Target: <15% of actions taken on confidence <0.70. Measure: (actions_confidence<0.70) / total_actions. Alert: >25%, indicates over-aggressive threshold or poor confidence scores.
5. **confidence_score_calibration_brier_score**: Target: Brier Score <0.05. Measure: average (predicted_probability - actual_outcome)^2 across transcriptions. Alert: >0.08%, indicates poor calibration.

### Alerts
1. **Confidence Score Degradation** (P2): Condition - Mean confidence drops >5% from 7-day rolling average in 1-hour window, OR ECE increases >10% in 24 hours. Action: Check for ASR model issues, review recent deployments, verify audio quality, consider rolling back confidence-related changes.
2. **Low-Confidence Action Error Spike** (P1): Condition - Error rate on actions taken with confidence <0.70 exceeds 10% over 1-hour window. Action: Immediately raise confidence threshold, enable confirmations for all sub-0.70 transcriptions, audit recent actions, contact affected users.
3. **Calibration Drift Detection** (P2): Condition - Calibration curve significantly diverges from training curve (ECE >15% or max bin error >25%). Action: Trigger recalibration workflow on recent production data, evaluate if model overfitting to training set, implement monitoring for future drift.

---

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Confidence handling
- [Google Cloud Speech: Confidence Scores](https://cloud.google.com/speech-to-text/docs/basics) - Score usage
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Error handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Confidence issues
