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

**Mitigation Strategies**
1. **Threshold tuning**: Set confidence thresholds empirically
2. **Verification flow**: Confirm low-confidence transcriptions
3. **Graceful degradation**: "I'm not sure I heard that correctly..."
4. **Adaptive thresholds**: Adjust based on acoustic conditions
5. **Confidence monitoring**: Track calibration over time
6. **N-best alternatives**: Use multiple hypotheses when uncertain

**Detection**
- Plot confidence vs. accuracy (calibration curve)
- Track error rate by confidence band
- Monitor low-confidence action rates
- Alert on confidence distribution shifts
- Audit low-confidence errors

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Confidence handling
- [Google Cloud Speech: Confidence Scores](https://cloud.google.com/speech-to-text/docs/basics) - Score usage
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Error handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Confidence issues
