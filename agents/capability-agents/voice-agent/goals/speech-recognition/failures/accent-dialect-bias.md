# Accent and Dialect Bias

## Issue: ASR Performs Significantly Worse on Non-Standard Accents

**Frequency**: Very Common

**Symptoms**
- Higher error rates for non-native speakers
- Regional dialects consistently misunderstood
- Certain demographics abandon voice interfaces
- "Please repeat that" loops for specific users
- Accent-correlated customer satisfaction drops

**Root Cause**
ASR models are trained predominantly on standard accents (General American, RP British). Speakers with different accents—regional American, Indian English, African accents, non-native speakers—experience significantly higher error rates. This creates a discriminatory user experience where voice AI works well for some users and poorly for others.

**Example**
```
Scenario: Banking voice assistant

User (Indian English accent): 
  "I want to transfer five hundred dollars to my savings account"

ASR transcription attempts:
  Attempt 1: "I want to transfer pipe under dollars to my savings account"
  Attempt 2: "I want to transfer five hundred dollars to my savings a cow"
  Attempt 3: "I want to transfer five hundred dollars to my savings account"
  
Same utterance, General American accent:
  Attempt 1: "I want to transfer five hundred dollars to my savings account" ✓

Accuracy comparison:
  General American: 98% WER
  Indian English: 84% WER (-14 points)
  Nigerian English: 81% WER (-17 points)
  Scottish English: 86% WER (-12 points)

Business impact:
  - 3x more retries for accented speakers
  - 40% higher abandonment rate
  - Customer complaints: "Your system doesn't understand me"
  - Potential discrimination liability
```

**Key Statistics**
From Accent Bias Research (2026):
- ASR accuracy drops 10-20 points for non-standard accents
- African American Vernacular English: 15-20% higher WER
- Non-native speakers: 2x error rate
- Only 5% of training data from non-Western accents
- Accent-based abandonment: 25-40% for affected groups

**Accent Performance Gaps**
| Accent | Typical WER Increase | Affected Population |
|--------|---------------------|---------------------|
| Indian English | 12-18% | 125M+ speakers |
| African American VE | 15-20% | 40M+ speakers |
| Hispanic English | 10-15% | 60M+ speakers |
| Scottish/Irish | 8-12% | 10M+ speakers |
| East Asian English | 12-16% | 500M+ speakers |

**Contributing Factors**
- Training data biased toward standard accents
- Acoustic models tuned for majority speakers
- Limited accent-specific adaptation
- No accent detection and routing
- Testing only with standard accents
- Phoneme inventories don't cover all accents

**Mitigation Strategies**
1. **Diverse training data**: Include accented speech in training
2. **Accent adaptation**: Fine-tune models for specific accents
3. **Accent detection**: Detect accent and route to specialized model
4. **Confidence thresholds**: Lower thresholds for known-difficult accents
5. **Fallback options**: Offer text input for repeated failures
6. **Regular auditing**: Track accuracy by demographic

**Detection**
- Segment WER by user demographics
- Track retry rates by accent/region
- Monitor abandonment patterns
- A/B test accent-adapted models
- Survey affected user groups

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Accent issues
- [Stanford: Racial Disparities in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Bias research
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Accent handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Recognition issues
