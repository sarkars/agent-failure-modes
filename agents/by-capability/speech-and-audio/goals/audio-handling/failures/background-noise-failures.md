# Background Noise Failures

## Issue: ASR Accuracy Degrades Significantly in Noisy Environments

**Frequency**: Very Common

**Symptoms**
- More errors in noisy locations
- "What?" responses increase
- Task completion drops
- Certain environments unusable
- User must repeat multiple times

**Root Cause**
Real-world voice interactions happen in noisy places: cars, restaurants, streets, factories. Background noise—traffic, music, voices, machinery—interferes with speech recognition. Without robust noise handling, ASR accuracy drops dramatically in these common environments, making voice agents unreliable when users need them most.

**Example**
```
Scenario: Drive-through ordering in various noise conditions

Quiet environment (car, windows up):
  User: "I'd like a large coffee and a muffin"
  ASR: "I'd like a large coffee and a muffin" ✓
  WER: 0%

Moderate noise (car, windows down):
  User: "I'd like a large coffee and a muffin"
  ASR: "I'd like a large coffee and the mountain"
  WER: 18%

High noise (busy intersection):
  User: "I'd like a large coffee and a muffin"
  ASR: "I'd type of orange coffee and above in"
  WER: 55%

Extreme noise (construction nearby):
  User: "I'd like a large coffee and a muffin"
  ASR: [Unintelligible garbage]
  WER: 90%+

Noise impact analysis:
  SNR > 20dB (quiet): WER 5%
  SNR 10-20dB (moderate): WER 15-25%
  SNR 5-10dB (noisy): WER 30-50%
  SNR < 5dB (very noisy): WER 50-90%

Business impact:
  - McDonald's AI drive-thru failed in noise
  - 30% of calls from noisy environments
  - Customer frustration and abandonment
```

**Key Statistics**
From Noise Research (2026):
- WER increase in noise: 15-40% typical
- Calls with significant noise: 30%
- Noise-related failures: 25% of voice agent errors
- Noise-robust models: 50% WER reduction possible
- User retry rate in noise: 3x clean conditions

**Noise Types and Impact**
| Noise Type | Example | WER Impact |
|------------|---------|------------|
| Traffic | Cars, horns | +15-25% |
| Crowd | Restaurant, bar | +20-35% |
| Music | Radio, TV | +10-20% |
| Wind | Outdoor, driving | +25-40% |
| Machinery | Factory, construction | +30-50% |

**Contributing Factors**
- ASR trained on clean audio
- No noise suppression preprocessing
- Single microphone (no beam-forming)
- No noise level detection
- Same confidence thresholds for all conditions
- No graceful degradation for high noise

## Mitigation Strategies

### Prevention
1. **Noise Suppression Pre-Processing**: Apply spectral-subtraction or neural noise-suppression (e.g., RNNoise-class models) to the audio stream before it reaches ASR, tuned to preserve speech formants while attenuating stationary noise (traffic, HVAC). Trade-off: aggressive suppression can introduce artifacts that themselves hurt WER for already-quiet audio.
2. **Noise-Robust ASR Model Selection**: Use or fine-tune ASR models on noise-augmented training data (SNR-matched to target environments like drive-throughs or cars) rather than relying solely on clean-audio models. Trade-off: noise-robust models can underperform slightly on clean audio versus specialized clean-audio models.
3. **Multi-Microphone Beamforming**: Where hardware allows (arrays, smart speakers), use beamforming to spatially focus on the primary talker direction and reject ambient noise sources. Trade-off: requires multi-mic hardware and per-device calibration, not viable for single-mic phones.

### Detection & Response
1. **Real-Time SNR Estimation**: Continuously estimate SNR from the input stream; when SNR drops below a threshold (e.g., <10dB), switch the agent into a "noisy environment" mode — lower confidence thresholds, shorten expected utterances, and request confirmations more aggressively.
2. **Environment-Aware Confidence Adjustment**: Track ASR confidence distributions segmented by estimated noise level; when confidence is systematically low under high-noise conditions, prefer explicit reprompt ("It's noisy — could you repeat that?") over acting on a low-confidence guess.
3. **Noise-Segmented Quality Monitoring**: Tag every interaction with an estimated noise tier and monitor task completion/WER per tier so regressions specific to noisy environments (e.g., a model update that hurts noise robustness) are caught before they affect the aggregate metric.

### Architecture Patterns
1. **VAD + Noise-Suppression Front-End Pipeline**: Chain voice-activity detection with adaptive noise suppression as a dedicated pre-ASR stage, so the recognizer only receives segments classified as speech-with-noise-removed rather than raw ambient audio.
2. **Confidence-Gated Reprompt Loop**: When noise-adjusted confidence falls below threshold, route to a lightweight reprompt/clarification dialog rather than the full NLU pipeline, avoiding compounding errors from acting on garbled transcripts.
3. **Environment Profile Switching**: Maintain distinct acoustic profiles (quiet, drive-through, street, factory) with different noise-suppression parameters and confidence thresholds, selected either by device type/context or by real-time SNR classification.

### Metrics
1. **wer_by_snr_tier**: Target: < 15% WER at SNR 10-20dB; Alert threshold: > 30% WER at that tier
2. **noise_triggered_reprompt_rate_percent**: Target: 10-15% of noisy-environment interactions; Alert threshold: > 40% (suggests suppression isn't working)
3. **task_completion_rate_high_noise_percent**: Target: within 15pp of quiet-environment completion rate; Alert threshold: gap > 30pp
4. **snr_estimation_coverage_percent**: Target: 100% of calls have an SNR estimate; Alert threshold: < 95%

### Alerts
1. **Noise-Robustness Regression** (P2): Condition - WER at SNR 5-10dB tier increases > 20% week-over-week. Action: Check for recent ASR model/config changes, roll back if correlated, re-run noise-augmented eval suite.
2. **High-Noise Task Failure Spike** (P1): Condition - task completion rate in high-noise segment drops below 50%. Action: Escalate to voice AI on-call, verify noise-suppression service health, consider temporary fallback to DTMF for affected channel.
3. **Environment Misclassification** (P3): Condition - SNR estimation fails or defaults to "quiet" for > 10% of calls in a known noisy channel (e.g., drive-thru). Action: Investigate audio front-end pipeline, verify SNR estimator deployment.

## References

- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Noise issues
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Noise handling
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Environmental issues
- [Noise Robust ASR](https://arxiv.org/abs/2005.06343) - Research approaches
