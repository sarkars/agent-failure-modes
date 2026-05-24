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

**Mitigation Strategies**
1. **Noise suppression**: Preprocess audio with noise reduction
2. **Noise-robust ASR**: Use models trained on noisy data
3. **Noise detection**: Detect noise level and adjust behavior
4. **Multi-microphone**: Beam-forming with multiple mics
5. **Confidence adjustment**: Lower thresholds in noise
6. **Graceful degradation**: "It's noisy, please speak clearly"

**Detection**
- Track WER by estimated SNR
- Monitor task completion by environment
- Detect noise level in audio
- Segment performance by noise type
- Survey user about environmental issues

## References

- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Noise issues
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Noise handling
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Environmental issues
- [Noise Robust ASR](https://arxiv.org/abs/2005.06343) - Research approaches
