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

**Mitigation Strategies**
1. **Neural TTS**: Use modern neural synthesis
2. **SSML prosody**: Mark emphasis, breaks, pitch
3. **Content analysis**: Identify key words for emphasis
4. **Punctuation handling**: Map punctuation to prosody
5. **Speaking styles**: Use different styles for different content
6. **A/B testing**: Compare prosody approaches

**Detection**
- MOS (Mean Opinion Score) testing
- Comprehension testing
- Compare with human speech baseline
- Analyze user replay requests
- Survey naturalness ratings

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - TTS quality
- [SSML Prosody](https://www.w3.org/TR/speech-synthesis11/#S3.2.4) - Prosody markup
- [Neural TTS Research](https://arxiv.org/abs/2006.03575) - Prosody modeling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Speech issues
