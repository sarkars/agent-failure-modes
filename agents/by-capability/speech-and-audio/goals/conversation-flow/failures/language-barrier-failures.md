# Language Barrier Failures

## Issue: Agent Cannot Communicate Due to Unsupported or Incomprehensible Language

**Frequency**: Occasional (varies by market)

**Symptoms**
- Caller speaks language agent doesn't support
- ASR produces garbage for unknown language
- Agent responds in wrong language entirely
- Regional dialects not understood
- Caller and agent talking past each other
- Repeated "I didn't understand" with no resolution

**Root Cause**
Voice agents are typically trained for specific languages. When callers speak unsupported languages, strong regional dialects, or heavily accented speech outside training distribution, the system fails entirely. Unlike code-switching (which is about switching between supported languages), language barriers involve fundamental inability to communicate.

**Example**
```
Scenario 1: Unsupported language

[Agent supports English, Hindi, Hinglish]
Caller: [Speaks Tamil] "வணக்கம், நான் படிவம் நிரப்பினேன்..."
Agent: "Sorry, I didn't catch that. Could you repeat?"
Caller: [Repeats in Tamil]
Agent: "I'm having trouble understanding. 
        Can you speak in English or Hindi?"
Caller: [Continues Tamil, confused]

← Agent should detect unsupported language quickly
← Offer to connect with Tamil-speaking team

---

Scenario 2: ASR garbage output

[Caller speaks Kannada]
ASR output: "vnkm nn pdvm nrppnn..."
Agent: [Tries to respond to garbage] "I see you mentioned 
        something about... I'm not sure I understood."

← ASR produced transliterated garbage
← Agent tried to process nonsense

---

Scenario 3: Regional dialect

[Agent trained on standard Hindi]
Caller: [Speaks Bhojpuri dialect] "हमरा के फॉर्म भरले रहीं..."
ASR: [Partially transcribes, many errors]
Agent: [Confused response] "Sorry, which form?"
Caller: [Repeats in same dialect]

← Dialect close enough to detect as Hindi
← But ASR accuracy very low
← Neither understands the other

---

Scenario 4: Heavy accent outside training

[Agent trained on Indian English]
Caller: [Strong Scottish accent] "Aye, I filled oot the form..."
ASR: "I filled out the form" ← Ok
Caller: "Ach, I dinnae ken if it's right for me though"
ASR: "I don't if it's right for me though" ← Missing words

← Agent partially understands but misses key phrases
← Conversation becomes frustrating

---

Scenario 5: No language detected

[Caller speaks very softly in unknown language]
ASR: [Empty or very low confidence]
Agent: "Hello? Are you there?"
Caller: [Speaks again]
Agent: "I can't hear you clearly..."

← Could be audio issue or language issue
← Agent doesn't know which

---

Language barrier analysis (1,000 calls in India market):
  Supported language (En/Hi/Hinglish): 920 (92%)
  Unsupported language attempted: 45 (4.5%)
  Heavy dialect issues: 25 (2.5%)
  Unknown/undetected: 10 (1%)
  
  Resolution for unsupported:
    Detected + offered alternative: 35%
    Struggled until hang-up: 45%
    Caller switched to supported: 20%
```

**Key Statistics**
From Multilingual Voice Agent Research (2026):
- Unsupported language calls: 3-10% (varies by market)
- Dialect recognition failure: 5-15%
- ASR garbage rate for unknown language: 60-90%
- Successful language negotiation: 30-50%
- Caller frustration from barrier: 80%

**Language Barrier Types**
| Type | Cause | Detection Difficulty |
|------|-------|---------------------|
| Unsupported language | Tamil, Telugu, etc. | Medium |
| Regional dialect | Bhojpuri, Marwari | Hard |
| Heavy accent | Outside training | Hard |
| Mixed language | Unknown + known | Very hard |
| Soft/unclear | Can't distinguish | Very hard |

**Contributing Factors**
- Limited language coverage
- No language detection before ASR
- ASR trained on standard dialects only
- No fallback for unsupported languages
- No human handoff option
- Accent coverage gaps

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unsupported lang | Tamil input | Detect, offer alternative | Garbage response |
| Dialect | Strong dialect | Detect difficulty, adapt | Struggle |
| Language detection | 2 seconds of speech | Identify language | Wrong language |
| Negotiation | Caller can switch | Ask for En/Hi | Keep trying |
| Handoff | Can't communicate | Offer human help | Loop forever |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Language detection | > 90% | Correct language ID |
| Unsupported detection | > 80% | Identify unsupported |
| Negotiation success | > 50% | Switch to supported |
| Handoff when needed | > 90% | Offer alternative |

---

## Mitigation Strategies

### Prevention
1. **Language detection**: Identify language before ASR
2. **Unsupported detection**: Recognize when language isn't supported
3. **Language negotiation**: Ask caller to switch
4. **Human handoff**: Connect to human for unsupported
5. **Dialect training**: Expand ASR coverage
6. **Graceful exit**: Don't loop on incomprehension

### Implementation
```python
class LanguageBarrierHandler:
    """Handle language barrier situations"""
    
    SUPPORTED_LANGUAGES = ["english", "hindi", "hinglish"]
    
    UNSUPPORTED_INDICATORS = [
        "low_asr_confidence",  # < 0.3 average
        "high_unknown_ratio",  # > 50% unknown words
        "repeated_failures",   # 3+ "didn't understand"
        "no_response_fit"      # Response doesn't match any expected
    ]
    
    NEGOTIATION_PHRASES = {
        "english": "I'm sorry, I can only speak English or Hindi. "
                  "Can you switch to one of those?",
        "hindi": "Sorry, mujhe sirf English ya Hindi aati hai. "
                "Kya aap English ya Hindi mein baat kar sakte hain?",
    }
    
    HANDOFF_PHRASES = {
        "english": "I'm having trouble understanding. Let me connect "
                  "you with someone who can help better.",
        "hindi": "Mujhe samajh nahi aa raha. Main aapko kisi aur se "
                "connect karta hoon."
    }
    
    def __init__(self):
        self.failure_count = 0
        self.detected_language = None
    
    def detect_language(self, audio_segment) -> dict:
        """Detect language from audio before ASR"""
        # Use language ID model
        language_probs = self.language_id_model.predict(audio_segment)
        
        top_language = max(language_probs, key=language_probs.get)
        confidence = language_probs[top_language]
        
        return {
            "detected": top_language,
            "confidence": confidence,
            "supported": top_language in self.SUPPORTED_LANGUAGES,
            "all_probs": language_probs
        }
    
    def check_comprehension(self, asr_result: dict) -> dict:
        """Check if we understood the input"""
        confidence = asr_result.get("confidence", 0)
        transcript = asr_result.get("transcript", "")
        
        # Check for indicators of barrier
        issues = []
        
        if confidence < 0.3:
            issues.append("low_confidence")
        
        if len(transcript.split()) < 2 and confidence < 0.5:
            issues.append("near_empty")
        
        if self.contains_garbage(transcript):
            issues.append("garbage_text")
        
        if issues:
            self.failure_count += 1
        else:
            self.failure_count = 0
        
        return {
            "understood": len(issues) == 0,
            "issues": issues,
            "failure_count": self.failure_count,
            "needs_action": self.failure_count >= 2
        }
    
    def get_action(self, comprehension: dict, 
                   language_detection: dict) -> dict:
        """Determine appropriate action for barrier"""
        if not language_detection["supported"]:
            return {
                "action": "language_negotiation",
                "phrase": self.NEGOTIATION_PHRASES["english"],
                "fallback": "handoff"
            }
        
        if comprehension["failure_count"] >= 3:
            return {
                "action": "handoff",
                "phrase": self.HANDOFF_PHRASES["english"],
                "reason": "repeated_comprehension_failure"
            }
        
        if comprehension["failure_count"] >= 2:
            return {
                "action": "negotiate",
                "phrase": self.NEGOTIATION_PHRASES["english"]
            }
        
        return {"action": "continue"}
    
    def handle_barrier(self, detection: dict, 
                        comprehension: dict) -> str:
        """Handle language barrier situation"""
        action = self.get_action(comprehension, detection)
        
        if action["action"] == "handoff":
            # Trigger human handoff
            self.trigger_handoff(
                reason="language_barrier",
                detected_language=detection.get("detected")
            )
            return action["phrase"]
        
        if action["action"] in ["negotiate", "language_negotiation"]:
            return action["phrase"]
        
        return None  # Continue normally


class LanguageNegotiator:
    """Negotiate language with caller"""
    
    def __init__(self, supported=["english", "hindi"]):
        self.supported = supported
        self.negotiation_attempts = 0
        self.max_attempts = 2
    
    def negotiate(self, current_language: str) -> dict:
        """Attempt to negotiate language switch"""
        self.negotiation_attempts += 1
        
        if self.negotiation_attempts > self.max_attempts:
            return {
                "success": False,
                "action": "handoff",
                "message": "I'm sorry, let me connect you with "
                          "someone who speaks your language."
            }
        
        return {
            "success": "pending",
            "message": "I can speak English or Hindi. "
                      "Can you use one of those?",
            "listen_for": self.supported
        }
```

### Prompt Design
```yaml
instructions: |
  ## LANGUAGE BARRIER HANDLING
  
  Supported languages: English, Hindi, Hinglish
  
  If you CAN'T UNDERSTAND the caller:
  
  1. FIRST attempt: Ask to switch language
     "Sorry, I can only speak English or Hindi. 
      Can you use one of those?"
  
  2. SECOND attempt: Repeat ask, speak slower
     "I'm still having trouble. English ya Hindi—
      which do you prefer?"
  
  3. THIRD failure: Offer handoff
     "I'm having trouble understanding. Let me connect 
      you with someone who can help."
  
  SIGNS of language barrier:
  - Your response doesn't make sense to them
  - They keep speaking in unknown language
  - You can't parse what they're saying
  - 2+ "I didn't understand" in a row
  
  DO NOT:
  - Loop endlessly asking to repeat
  - Pretend to understand when you don't
  - Generate random responses to garbage input
  - Get frustrated or apologize repeatedly
  
  OUTCOME for unsupported language:
  - "unable_to_continue" with reason "language_barrier"
  - Or "handoff_requested" if transferring
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `language.unsupported.rate` | > 10% |
| `language.negotiation.success` | < 40% |
| `language.repeated_failure` | > 5% |
| `language.handoff.rate` | Monitor |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Unsupported Rate | > 15% | P2 |
| Low Negotiation Success | < 30% | P3 |
| Repeated Failures | > 8% | P2 |

---

## References

- [Multilingual ASR](https://arxiv.org/abs/2006.13979) - Language coverage
- [Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Language barriers
- [Accent Bias in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Coverage gaps
- [Dialect Recognition](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Regional issues
