# Multilingual Code-Switching Failures

## Issue: Agent Fails to Match or Maintain Caller's Language Choice

**Frequency**: Common in multilingual deployments

**Symptoms**
- Agent responds in wrong language after caller's first reply
- Random mid-conversation language switches
- Mixing multiple languages unnaturally in single response
- Ignoring explicit language change requests
- Defaulting to English when caller uses regional language

**Root Cause**
Multilingual voice agents must detect the caller's preferred language from their first substantive reply and maintain consistency. Without explicit language state tracking, the LLM may switch languages based on individual words, topic shifts, or training data biases. Code-switching (mixing languages) is natural in some contexts (Hinglish) but agents often do it inappropriately or inconsistently.

**Example**
```
Scenario: Outbound qualification call (India market)

Agent: "Hi, this is Riya from the app. You had filled our 
       ambassador form—do you have a minute?"
Caller: "Haan, bolo" [Yes, speak - Hindi]
Agent: "Great! So basically we're running this campus ambassador 
       program..." [Continues in English]

← Agent should have switched to Hindi after "Haan, bolo"

---

Scenario: Mid-call language drift

Turn 1 - Caller uses Hindi, Agent responds in Hindi ✓
Turn 2 - Caller uses Hindi, Agent responds in Hindi ✓
Turn 3 - Caller mentions "WhatsApp", Agent switches to English ✗
Turn 4 - Agent continues in English, caller confused ✗

---

Scenario: Over-mixing languages

Agent: "Toh basically आपको certificate मिलेगा, 
       plus trophy भी, और LinkedIn पर 
       founder shoutout which is really cool!"

← Three-language mixing (Hindi + Devanagari + English) 
   in one sentence sounds unnatural

---

Language consistency analysis (1,000 calls):
  Correct language detection: 72%
  Wrong language after first reply: 18%
  Mid-call drift: 23%
  Over-mixing (3+ languages): 8%
  Ignored explicit language request: 5%
```

**Key Statistics**
From Multilingual Voice Agent Research (2026):
- Language detection accuracy from first reply: 70-85%
- Unwanted code-switching rate: 15-25%
- User drop-off from language mismatch: 20-30%
- Explicit language request ignored: 5-10%
- Hindi-English (Hinglish) most challenging: 60% consistency

**Code-Switching Failure Types**
| Type | Description | Impact |
|------|-------------|--------|
| Detection failure | Wrong language from first reply | Immediate disconnect |
| Drift | Gradual shift away from caller's language | Confusion |
| Over-mixing | Too many languages per response | Unnatural |
| Keyword trigger | Brand terms trigger language switch | Jarring |
| Request ignored | "Hindi mein bolo" not followed | Frustration |

**Contributing Factors**
- No explicit language state variable
- LLM training bias toward English
- Brand/technical terms only in English
- No language consistency enforcement
- Missing language detection from prosody
- Treating code-switching as error vs. valid style

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Hindi detection | Caller replies "Haan bolo" | Hindi response | English response |
| Language persistence | 5 turns in Hindi | All Hindi | Any English turn |
| Explicit request | "English please" | Switch to English | Continue Hindi |
| Hinglish handling | Caller uses Hinglish | Consistent Hinglish | Pure Hindi or English |
| Brand terms | Technical term in non-English | Stay in caller's language | Switch to English |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Language detection accuracy | > 90% | First reply → response language match |
| Language consistency | > 95% | Same language across all turns |
| Mixing rate | < 2 languages/turn | Count distinct languages per response |
| Request compliance | > 98% | Explicit language requests honored |

---

## Mitigation Strategies

### Prevention
1. **Explicit language state**: Track detected language as conversation variable
2. **First-reply detection**: Use dedicated classifier on caller's first substantive reply
3. **Consistency enforcement**: System prompt includes "continue in {language} until caller switches"
4. **Brand term handling**: Keep technical terms in English but frame in caller's language
5. **Prosody-based detection**: Use tone/accent cues alongside text

### Language Management
```python
class LanguageManager:
    def __init__(self):
        self.detected_language = None
        self.explicit_request = None
        
    def detect_from_reply(self, transcript: str) -> str:
        """Detect language from first substantive reply"""
        # Check for explicit markers first
        if self.has_hindi_script(transcript):
            return "hindi"
        if self.has_hinglish_markers(transcript):
            return "hinglish"
        
        # Use classifier for ambiguous cases
        return self.language_classifier.predict(transcript)
    
    def get_response_language(self, turn_num: int, 
                               caller_transcript: str) -> str:
        """Determine language for agent response"""
        # Check for explicit language request
        if "english" in caller_transcript.lower():
            self.explicit_request = "english"
        elif "hindi" in caller_transcript.lower():
            self.explicit_request = "hindi"
        
        # Explicit request overrides detection
        if self.explicit_request:
            return self.explicit_request
        
        # Detect on first turn
        if turn_num == 1:
            self.detected_language = self.detect_from_reply(
                caller_transcript
            )
        
        # Detect shift if caller switches
        current_lang = self.detect_from_reply(caller_transcript)
        if current_lang != self.detected_language:
            # Only switch if clearly different (not just brand terms)
            if self.is_definite_switch(caller_transcript):
                self.detected_language = current_lang
        
        return self.detected_language
    
    def format_prompt(self, base_prompt: str) -> str:
        """Add language instruction to prompt"""
        lang_instruction = {
            "english": "Respond in English with Indian casual phrasing.",
            "hindi": "Respond in Hindi using Devanagari script.",
            "hinglish": "Respond in natural Hinglish."
        }
        
        return f"{base_prompt}\n\n{lang_instruction[self.detected_language]}"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `language.detection.accuracy` | < 85% |
| `language.consistency.rate` | < 90% |
| `language.switch.unintended` | > 10% |
| `language.mixing.excessive` | > 15% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Detection Failure Spike | accuracy < 80% | P2 |
| Consistency Degraded | drift > 20% | P2 |
| Request Ignored | compliance < 95% | P3 |

---

## References

- [Multilingual Conversational AI](https://arxiv.org/abs/2004.06080) - Code-switching in dialog systems
- [Voice AI India Market](https://www.beconversive.com/blog/voice-ai-challenges) - Multilingual challenges
- [Sarvam AI STT](https://sarvam.ai) - Indic language speech recognition
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Language handling issues
