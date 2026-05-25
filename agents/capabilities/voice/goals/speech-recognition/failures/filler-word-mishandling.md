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

**Mitigation Strategies**
1. **Filler detection**: Identify and tag fillers in ASR
2. **Selective filtering**: Remove fillers before NLU
3. **Disfluency models**: Train NLU on speech with fillers
4. **False start handling**: Detect and handle self-corrections
5. **Context preservation**: Keep fillers for timing/sentiment
6. **Tunable filtering**: Adjust based on application needs

**Detection**
- Track filler-related intent errors
- Monitor transcriptions for common fillers
- Compare filtered vs. unfiltered performance
- Analyze false start handling
- Review cases where fillers caused issues

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Speech patterns
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real-world issues
- [Speech Disfluency Research](https://www.isca-speech.org/archive/interspeech_2023/) - Filler handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Common errors
