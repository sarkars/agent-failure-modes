# Filler Word Mishandling

## Issue: ASR Misinterprets or Fails to Filter Conversational Fillers

**Frequency**: Common

**Symptoms**
- "Um" and "uh" transcribed as words
- "Like" interpreted literally
- "You know" treated as question
- Hesitation sounds become garbage text
- Agent responds to filler as content

**Root Cause**
Natural speech contains fillers (um, uh, like, you know), false starts, and self-corrections. ASR may transcribe these literally, fail to filter them, or misinterpret them as meaningful words. When passed to the language model, fillers can confuse intent understanding or trigger unintended responses.

**Example**
```
Scenario: Flight booking voice agent

User: "I want to, um, book a flight to, uh, like, New York, you know?"

ASR outputs across systems:

System A (raw transcription):
  "I want to um book a flight to uh like New York you know"
  → Agent: "I found flights to New York. Did you also want to book something called 'Um'?"

System B (aggressive filtering):
  "I want to book a flight to New York"
  → Agent: "Great, searching for flights to New York" ✓

System C (partial filtering):
  "I want to um book a flight to like New York you know"
  → Agent: "Do you know someone in New York?"
  
System D (misinterpretation):
  "I want to book a flight to, like, New York"
  → Agent: "Searching for flights similar to New York..."

Filler analysis (1000 utterances):
  Utterances with fillers: 680 (68%)
  Average fillers per utterance: 2.3
  Fillers causing errors: 12% of filler utterances
```

**Key Statistics**
From Speech Research (2026):
- 60-70% of natural speech contains fillers
- Average filler rate: 2-4 per utterance
- Unflitered fillers cause 10-15% intent errors
- Aggressive filtering removes meaningful content 5%
- "Like" misinterpreted in 25% of occurrences

**Common Filler Issues**
| Filler | Misinterpretation | Frequency |
|--------|-------------------|-----------|
| "um/uh" | Transcribed as word | Very Common |
| "like" | "Similar to" meaning | Common |
| "you know" | Question trigger | Common |
| "I mean" | Correction ignored | Occasional |
| "so" | Treated as continuation | Common |

**Contributing Factors**
- ASR not trained to identify fillers
- No disfluency detection
- Fillers transcribed literally
- NLU not robust to fillers
- No preprocessing pipeline
- Different handling across ASR providers

## Mitigation Strategies

### Prevention
1. **Disfluency-Aware ASR Decoding**: Train ASR acoustic model on data with disfluencies (filler words, false starts, self-corrections). Use disfluency tokens (<filler>, <correction>, <restart>) during decoding to explicitly tag fillers rather than transcribe as words. Implement confidence penalties for filler hypothesis to deprioritize them during beam search. Use phonetic context to distinguish "um" (filler) from "umm" (thinking). Set filler confidence thresholds lower than semantic words to enable selective filtering downstream.
2. **Two-Stage Filtering Pipeline**: Stage 1: Run ASR with disfluency tokens. Stage 2: Apply rule-based filler removal (remove tagged fillers, compress whitespace). Keep parallel "with-fillers" and "without-fillers" transcriptions. Use with-fillers version for sentiment/confidence analysis (hesitation indicates uncertainty). Use without-fillers for intent/NLU. Implement context-aware filtering: keep "um" in "I'm searching for, um, flights" (clarifying) but remove in "um, okay" (pure filler).
3. **NLU Robustness Training**: Fine-tune NLU/intent models on speech transcriptions WITH fillers, disfluencies, false starts. Use data augmentation: insert random fillers into training examples. Implement intent models robust to interruptions. Test intent accuracy on both clean text and natural speech transcriptions. Use separate test sets to measure robustness (same utterance with/without fillers should yield same intent).

### Detection & Response
1. **Filler-Induced Intent Error Tracking**: Monitor cases where transcription contains fillers AND intent changes from expected. Example: filtered="book flight to New York" (correct intent), unfiltered="book flight to like New York" (wrong intent). Alert when filler-related intent errors exceed 1% of utterances. Segment by filler type: "um"/"uh", "like", "you know", "I mean". Flag specific filler+context combinations with high error rates (e.g., "like" + product names).
2. **False Start Detection**: Identify and track self-corrections/false starts (e.g., "I want to go to, no wait, I want to go to Boston"). Count utterances with detected false starts. Track error rate on false-start-containing utterances vs. clean utterances. Alert if false-start error rate 2x+ baseline. Use punctuation/timing cues to detect restarts.
3. **Filler Filtering Impact Measurement**: For subset of utterances, generate both filtered and unfiltered transcriptions. Measure NLU performance impact: intent accuracy, entity extraction accuracy, downstream action accuracy. Target: intent accuracy same with/without filler filtering (within 1 point). Alert if filtering degrades accuracy >2 points.

### Architecture Patterns
1. **Disfluency-Tagged Transcription Stream**: Modify ASR output format to include disfluency markers: `I want to <filler>um</filler> book a flight to <filler>uh</filler> New York`. Pass full tagged transcription through pipeline. Allow downstream consumers (NLU, sentiment analysis) to selectively use or ignore fillers. Implement disfluency confidence scores (how confident ASR is that <filler> tag is correct) to enable probabilistic handling.
2. **Context-Aware Filler Filtering**: Build filtering rules that consider conversational context and application semantics. For flight booking: remove "um"/"uh" but preserve "like" (might be product name). For document editing: keep all hesitation markers (indicate uncertainty). Use ML-based filter tuning: train classifier on (transcription, application_type) → (filter_strategy) to learn domain-specific filler handling.
3. **Filler-Robust Intent Classification**: Implement intent model that explicitly handles disfluencies. Use sequence model (LSTM/Transformer) that learns to ignore filler tokens. Separate "filler bias" from "intent signal". Implement fallback: if intent confidence <70% on transcription-with-fillers, retry on filtered version. Use ensemble of (filler-aware model + filler-filtered model) for robustness.

### Metrics
1. **filler_transcription_rate_percent**: Target: <5% of utterances transcribed with filler words appearing literally (not filtered). Measure: utterances_with_literal_fillers / total_utterances. Alert: >7%, indicates ASR filler detection failure.
2. **filler_induced_intent_error_rate**: Target: <1% of intent errors attributable to filler handling. Measure: (errors_where_filtered_transcription_correct AND unfiltered_incorrect) / total_utterances. Track by filler type. Alert: >1.5%, escalate to NLU tuning.
3. **false_start_detection_accuracy**: Target: 90%+ accuracy detecting self-corrections. Measure: (correctly_detected_false_starts) / (total_false_starts). Alert: <85%, retrain false-start detector.
4. **filtering_accuracy_impact**: Target: Intent accuracy within 1 point (filtered vs. unfiltered). Measure: intent_accuracy_on_unfiltered - intent_accuracy_on_filtered. Alert: >2 point difference, revert filter or retrain NLU.
5. **filler_confidence_calibration**: Target: Filler tags have <60% confidence (lower than semantic words). Measure: average_confidence_of_filler_hypotheses. Alert: >70% confidence on fillers, indicates poor disfluency modeling.

### Alerts
1. **Filler Misinterpretation Loop** (P2): Condition - 3+ consecutive user corrections where issue is filler handling (user says "um, [command]" → agent responds to "um" part). Action: Alert product team, review NLU filler robustness, enable aggressive filler filtering for problematic user, offer text-input fallback.
2. **False Start Handling Failure** (P2): Condition - >5% of utterances with detected false starts result in wrong intent compared to <2% for normal utterances. Action: Trigger false-start detector retraining, implement explicit user confirmation for self-correction scenarios.
3. **Filler Filtering Accuracy Drop** (P2): Condition - Intent accuracy on filtered transcriptions drops >2 points from baseline in 1-hour window. Action: Alert ML team, revert recent ASR or filtering changes, investigate root cause (disfluency model regression, overly aggressive filtering).

---

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Speech patterns
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real-world issues
- [Speech Disfluency Research](https://www.isca-speech.org/archive/interspeech_2023/) - Filler handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Common errors
