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

## Mitigation Strategies

### Prevention
1. **Multi-Accent Training Data Pipeline**: Augment ASR training with balanced accent representation (minimum 10-15% non-standard accents). Use stratified sampling during model training to prevent majority-accent overfitting. Implement active learning to identify high-error accent regions and increase sampling. Use data augmentation techniques (pitch-shifting, tempo variation) to simulate accent variations while maintaining phonetic integrity.
2. **Accent-Specific Fine-Tuning Registry**: Maintain fine-tuned model variants for high-error accents (Indian English, African American Vernacular, Hispanic English). Deploy routing logic that detects speaker accent characteristics in first 1-2 seconds and switches to accent-optimized model. Store accent metadata with user profiles for faster routing on repeat interactions.
3. **Confidence Scoring Calibration by Dialect**: Develop separate confidence score calibration curves for each major accent group. Lower confidence thresholds (60-70% vs. 80%) for known-difficult accents to trigger earlier fallback/confirmation. Use dialect-specific smoothing in confidence estimates to reduce false-positive high-confidence errors on accented speech.

### Detection & Response
1. **Per-Accent WER Monitoring**: Track word error rate disaggregated by 10+ accent categories (Indian English, African American VE, Hispanic English, Scottish, East Asian, etc.). Set accent-specific WER targets (e.g., Indian: <8%, African American VE: <8%). Alert when any accent's WER exceeds target by >2 points. Use automated accent detection on user audio to classify and track.
2. **Retry Rate Anomaly Detection**: Segment retry/correction requests by user demographic/accent (inferred from speech or profile). Establish per-accent baseline for correction attempts (e.g., 5% baseline). Flag 2x+ deviation as signal of accent-based degradation. Correlate retry spikes with specific phrases/commands to identify accent-vulnerable patterns.
3. **Abandonment Correlation Analysis**: Monitor voice interaction abandonment rates by accent/demographic. Flag >5% relative gap between accent groups as discriminatory failure. Implement exit surveys post-abandonment asking about understanding difficulties. Aggregate feedback to identify systematic accent-specific pain points.

### Architecture Patterns
1. **Multi-Model Ensemble with Accent Routing**: Implement router that classifies speaker accent from first 500ms of speech, then routes to appropriate ASR model variant. Maintain base model (standard accents) + 5-8 specialist models (Indian, AAVE, Hispanic, Mandarin, etc.). Use confidence scoring to weight ensemble results, with higher weight to accent-matched model. Implement fallback to multi-model voting if single model confidence < 65%.
2. **Confidence-Aware Fallback Ladder**: Create escalation sequence: (1) High-confidence ASR result → use as-is; (2) Medium-confidence (60-80%) → request user confirmation; (3) Low-confidence (<60%) + accent mismatch signal → offer alternative input (spell-out, keypad). Track which rungs are hit per accent to identify needs for retraining or additional models.
3. **Federated Accent Adaptation**: Allow deployment sites to fine-tune on local dialect-specific audio (with user consent). Collect anonymized accent data from production interactions. Periodically retrain global model with accent-stratified sampling. Implement privacy-preserving accent adaptation that doesn't require centralized data collection.

### Metrics
1. **word_error_rate_by_accent**: Target: <8% across all accents (baseline 98% WER = 2% error). Track: General American, Indian English, African American VE, Hispanic English, East Asian, Scottish. Alert: Any accent WER > 10% or >2 points above 90-day rolling average.
2. **accent_detection_accuracy**: Target: 95%+ accuracy in classifying speaker accent from first 500ms. Measure: ground truth vs. inferred accent on labeled test set. Alert: <90% accuracy indicates model drift.
3. **accent_retry_rate_ratio**: Target: Retry rates parity across accents (max 1.5x difference). Track: correction/retry requests per 100 interactions, segmented by accent. Alert: >2x variance between accent groups (e.g., 8% for Indian vs. 3% for General American).
4. **accent_abandonment_gap**: Target: <5% relative gap in abandonment rates across accents. Measure: (max_abandonment - min_abandonment) / min_abandonment. Alert: >10% gap indicates discriminatory failure.
5. **confidence_calibration_by_accent**: Target: Confidence scores well-calibrated per accent (>90% of utterances with 85% confidence have 85%+ actual accuracy). Measure: Expected Calibration Error (ECE) per accent. Alert: ECE >10% for any accent group.

### Alerts
1. **Accent-Specific WER Degradation** (P2): Condition - WER for any accent group increases 2+ points from 7-day baseline in 1-hour window. Action: Immediate alert to ML team, trigger accent-specific evaluation on latest model, compare to prior checkpoint, consider rollback if >3 point jump.
2. **Accent Disparity Detection** (P2): Condition - Retry rate ratio (max/min across accents) > 2.0 over 24-hour window. Action: Alert product/ML team, segment error analysis by accent, identify high-error phrases for targeted improvement, consider pausing deployment if ratio > 3.0.
3. **Discriminatory User Experience** (P1): Condition - Abandonment rate gap between accent groups > 10% relative over 7-day window, AND average WER gap > 3 points. Action: Immediate escalation to executive team, freeze model deployments, initiate emergency retraining on balanced accent data, prepare customer communication plan.

## Chat assistant examples

### Children's and atypical speech

Illustrative example: a US library's voice-enabled reading helper on a tablet. A child is searching for a book by voice. Lines marked (voice) are planned voice input; lines marked (tap) are text or touch.

Before:

```
Bot:   Say the title of the book you want.
Child: (voice) "The Very Hungry Cat-cat-caterpillar"
Bot:   I heard "The Very Hungry Cat cat cat". I can't find that book.
Child: (voice) "Caterpillar!"
Bot:   Sorry, I didn't catch that.
Child: (voice) "The Very Hungry Caterpillar!"
Bot:   Sorry, I didn't catch that.
Bot:   I can't help with that right now.
```

After:

```
Bot:   Say the title of the book you want, or tap Type It.
Child: (voice) "The Very Hungry Cat-cat-caterpillar"
Bot:   I think you want "The Very Hungry Caterpillar". Is that right?
       [Yes] [No, let me type it]
Child: (tap) Yes
Bot:   Here it is. Want me to read it, or do you want to read it to me?
```

**What the user experiences:** a child (or an adult who stutters or has aphasia) says the title the way they naturally say it, is told "I didn't catch that" three times, and learns that the helper is not for them.

**Fix:** do not treat a repeated sound or a pause as the end of the answer, and do not repeat the same failure prompt more than once. Offer a tap or typed path after the first miss, and offer a best guess for the person to confirm. Report word error rate by cohort (child, stutter, aphasia, Deaf speech) so the gap is visible. In research on people who stutter, systems often cut speakers off early, and technical changes to the recognizer reduced both early cutoffs and word error rate (["From User Perceptions to Technical Improvement"](https://arxiv.org/abs/2302.09044v3), abstract read). Related pattern: [voice repair failure](../../../../human-machine-interface/goals/voice/failures/repair-failure.md).

This is design guidance, not clinical advice, and it needs expert review (for example, a speech-language pathologist and a child-safety reviewer) before use.

### Wrong recognition model for the speaker

Illustrative example: a US pharmacy refill phone line. The locale setting is a configuration value, not something the caller says. Here it was left at a non-US English variant after a test. We found no source showing that a locale mismatch alone causes these exact mishearings, so the errors below show the symptom, not a measured cause; check it on your own recordings.

Before:

```
Config: recognition locale = en-IN   (caller is in Ohio and speaks US English)
Bot:    Say your prescription number.
Caller: (voice) "four seven two, nine zero one"
Bot:    I heard "for seven to nine oh one". That is not a valid number.
Caller: (voice) "four seven two nine zero one"
Bot:    I heard "for seven too nine zero one". That is not a valid number.
Bot:    Let me transfer you to an agent.
```

After:

```
Config: recognition locale = en-US   (set from the caller's number and account region, reviewed weekly)
Bot:    Say your prescription number.
Caller: (voice) "four seven two, nine zero one"
Bot:    Four seven two, nine zero one. Is that right?
Caller: (voice) "Yes"
Bot:    Found it. Your refill is ready for pickup today.
```

**What the user experiences:** the caller speaks normally, the number is mis-heard twice, and they are sent to an agent for a task the bot should have finished.

**Fix:** set the locale and model from what is known about the caller (account region, number, stated language) and keep a per-deployment locale check in the test plan. Report word error rate by locale setting, so a wrong setting shows up as one bad bucket instead of a general "voice is flaky". When the first attempt fails, ask the caller to confirm the language or region rather than retrying the same model; Google's Speech-to-Text docs show the primary language code is set on each request and that extra candidate languages can be listed, so a mismatch is a setting you can change ([Google Cloud docs](https://docs.cloud.google.com/speech-to-text/docs/enable-language-recognition-speech-to-text), page read). Related pattern: [voice repair failure](../../../../human-machine-interface/goals/voice/failures/repair-failure.md).

---

## References

- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Accent issues
- [Stanford: Racial Disparities in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Bias research
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Accent handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Recognition issues
