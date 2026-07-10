# Prosody Mismatch

## Issue: Speech Rhythm, Stress, and Intonation Don't Match Content

**Frequency**: Common

**Symptoms**
- Monotone delivery of varied content
- Questions sound like statements
- Emphasis on wrong words
- Unnatural pauses in sentences
- Reading lists without proper rhythm

**Root Cause**
Prosody—the rhythm, stress, and intonation of speech—conveys meaning beyond words. Questions should rise in pitch; important words need emphasis; lists need pauses. Basic TTS often applies uniform prosody regardless of content, making speech sound robotic. Even neural TTS may fail to match prosody to semantic content.

**Example**
```
Scenario: Appointment confirmation

Text: "Your appointment is on Tuesday at 3pm. 
       Would you like me to send a reminder?"

Problematic TTS (flat prosody):
  "Your appointment is on Tuesday at three PM 
   would you like me to send a reminder"
  
  Issues:
    - No emphasis on "Tuesday" and "3pm" (key info)
    - Question sounds like statement (no rising pitch)
    - No pause between sentences
    - Sounds robotic and hard to parse

Good TTS (natural prosody):
  "Your appointment is on TUESDAY at THREE PM.
   [pause]
   Would you like me to send a reminder?" ↗ [rising]
   
---

List example:
Text: "You ordered: a burger, fries, and a drink"

Flat: "You ordered a burger fries and a drink"
Natural: "You ordered: a burger, [pause] fries, [pause] and a drink"

---

Prosody analysis:
  Appropriate emphasis: 60% (should be 90%+)
  Question intonation: 70%
  Sentence boundary pauses: 75%
  List rhythm: 55%
```

**Key Statistics**
From Prosody Research (2026):
- Monotone TTS: 40% of basic systems
- Question intonation accuracy: 70-85%
- Emphasis placement accuracy: 60-80%
- User comprehension impact: 15-20% reduction with poor prosody
- Naturalness rating (MOS): 3.2 (flat) vs 4.1 (good prosody)

**Prosody Failures**
| Element | Failure | Impact |
|---------|---------|--------|
| Pitch | Flat, no variation | Monotone |
| Emphasis | Wrong word stressed | Confusion |
| Pacing | Too fast/slow | Comprehension |
| Pauses | Missing or wrong | Hard to parse |
| Question tone | Statement intonation | Doesn't sound like question |

**Contributing Factors**
- Basic concatenative TTS
- No semantic understanding for emphasis
- Missing SSML prosody markup
- No punctuation-to-prosody mapping
- Single speaking style
- No content-aware synthesis

## Mitigation Strategies

### Prevention
1. **Neural TTS with Learned Prosody**: Use neural TTS models trained to predict prosody (pitch, stress, pacing) from semantic/syntactic content rather than basic concatenative synthesis with uniform prosody, directly addressing the monotone delivery and misplaced emphasis described in the root cause. Trade-off: neural prosody models can still misjudge emphasis on novel/ambiguous sentence structures and need evaluation against domain-specific content.
2. **Punctuation-to-Prosody Mapping Rules**: Explicitly map punctuation and sentence structure to prosodic targets — question marks to rising terminal pitch, commas/list items to pauses, periods to falling pitch and full stop — as a rules layer that supplements (and can override) the model's default prosody when it's known to be unreliable for a construct (e.g., lists).
3. **SSML Prosody Markup for Key-Information Emphasis**: For content where specific words carry critical information (date, time, amount), explicitly mark emphasis via SSML `<emphasis>` or pitch/rate tags rather than relying on the TTS model to infer which words matter.

### Detection & Response
1. **Question-Intonation Accuracy Sampling**: Specifically test and monitor whether question-type utterances receive rising terminal intonation (not just overall MOS), since flat question delivery is a distinct, correctable failure mode separate from general naturalness.
2. **Comprehension-Impact A/B Testing**: Periodically A/B test prosody-enhanced vs. flat delivery on comprehension-sensitive content (lists, confirmations) and measure task success/replay-request rate, quantifying the real-world cost of prosody mismatches rather than relying on subjective naturalness scores alone.
3. **Replay-Request Rate as Proxy Signal**: Track how often users ask the agent to repeat itself; correlate spikes with specific message templates or content types to identify where prosody (or pacing) is likely impairing comprehension.

### Architecture Patterns
1. **Punctuation-Aware SSML Generation Layer**: Insert a deterministic text-to-SSML transformation stage between response generation and TTS synthesis that converts sentence structure/punctuation into explicit prosody markup, giving predictable behavior for lists and questions independent of the underlying model's learned prosody.
2. **Content-Type-Specific Speaking Styles**: Define distinct prosody/speaking-style profiles for different content types (confirmations, lists, questions, alerts) and select the profile based on the response template's declared type, rather than one uniform style for all output.
3. **Human-Baseline Comparison Harness**: Maintain a benchmark suite comparing synthesized prosody against human speech recordings of the same scripts (MOS and objective pitch/timing comparison) run in CI against TTS model/config changes.

### Metrics
1. **question_intonation_accuracy_percent**: Target: > 90%; Alert threshold: < 70%
2. **emphasis_placement_accuracy_percent**: Target: > 85%; Alert threshold: < 60%
3. **mos_naturalness_score**: Target: > 4.0; Alert threshold: < 3.5
4. **replay_request_rate_percent**: Target: < 5%; Alert threshold: > 15%

### Alerts
1. **Question Intonation Regression** (P2): Condition - question-intonation accuracy on eval set drops below 70%. Action: Review recent TTS model/SSML-layer changes, verify punctuation-to-prosody rules still applied correctly.
2. **Naturalness MOS Drop** (P2): Condition - rolling MOS naturalness score falls below 3.5. Action: Investigate TTS model/version changes, compare against human-baseline harness results.
3. **Replay Request Spike** (P2): Condition - replay-request rate exceeds 15% for a specific message template/content type. Action: Review prosody/pacing for that template, consider adding explicit SSML emphasis/pause markup.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - TTS quality
- [SSML Prosody](https://www.w3.org/TR/speech-synthesis11/#S3.2.4) - Prosody markup
- [Neural TTS Research](https://arxiv.org/abs/2006.03575) - Prosody modeling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Speech issues
