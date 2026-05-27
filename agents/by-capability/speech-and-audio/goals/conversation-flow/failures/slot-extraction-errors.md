# Slot Extraction Errors

## Issue: Critical Information Extracted Incorrectly or Inconsistently

**Frequency**: Common

**Symptoms**
- Phone numbers captured with wrong digits
- Permission status ambiguous (yes/no/unknown all wrong)
- Same information extracted differently across calls
- Partial information marked as complete
- Implicit confirmations missed

**Root Cause**
Voice agents extract structured data (slots) from unstructured conversation. Callers rarely provide information in expected formats. They confirm implicitly ("yeah this number's fine"), give partial info ("call me on my other number"), or provide info across multiple turns. Without robust extraction logic, critical data is corrupted, missed, or inconsistently captured.

**Example**
```
Scenario 1: Implicit confirmation missed

Agent: "Is this same number okay for WhatsApp?"
Caller: "Haan haan, yahi pe bhej do" [Yes yes, send on this one]

Extracted: whatsapp_number = "" (blank)
Correct: whatsapp_number = "same_number"

← Agent missed implicit confirmation

---

Scenario 2: Permission ambiguity

Agent: "Can the team share the playbook on WhatsApp?"
Caller: "Yeah, I guess, let me see what it's about"

Extracted: permission = "yes"
Correct: permission = "unknown" or "conditional"

← Hesitant response treated as clear permission

---

Scenario 3: Number extraction error

Caller: "My WhatsApp is 98765-43210"
Extracted: whatsapp_number = "9876543210" (missing digit)
Correct: whatsapp_number = "9876543210" (should be 10 digits)

Actually said: "98765-43210" (10 digits, correct)
ASR heard: "9876-43210" (9 digits, wrong)

---

Scenario 4: Cross-turn information

Turn 3 - Caller: "I'm at Delhi University"
Turn 5 - Caller: "Actually I meant Jamia"

Extracted: college_name = "Delhi University"
Correct: college_name = "Jamia"

← Earlier value not updated on correction

---

Slot extraction analysis (1,000 calls):
  Total slots to extract: 8,420
  Correctly extracted: 6,904 (82%)
  
  Error breakdown:
    Implicit confirmation missed: 8%
    Ambiguous response misinterpreted: 5%
    ASR error propagated: 3%
    Correction not captured: 2%
```

**Key Statistics**
From Voice Slot Filling Research (2026):
- Slot extraction accuracy: 75-85%
- Implicit confirmation miss rate: 10-20%
- Permission ambiguity rate: 15-25%
- Phone number extraction errors: 5-12%
- Cross-turn update failures: 8-15%

**Common Slot Extraction Failures**
| Slot Type | Failure Mode | Rate |
|-----------|--------------|------|
| Permission (yes/no) | Hesitant → yes | 18% |
| Phone number | Digit error | 12% |
| Same-number confirm | Implicit missed | 15% |
| Name/place | ASR error | 10% |
| Callback time | Vague → specific | 8% |

**Contributing Factors**
- No handling for implicit confirmations
- Binary extraction for non-binary responses
- ASR errors propagate to extraction
- No cross-turn slot updates
- Missing confidence scores on extraction
- Extraction prompt too literal

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Implicit yes | "Haan, yahi number" | same_number | blank |
| Hesitant permission | "I guess so" | unknown | yes |
| Number correction | "Actually it's 98765..." | Updated number | Old number |
| Partial info | "My other number is better" | prompt for number | same_number |
| Compound answer | "Yes WhatsApp, same number" | permission=yes, number=same | Either missing |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Slot accuracy | > 90% | Extracted vs. human annotation |
| Implicit handling | > 85% | Implicit confirmations captured |
| Correction capture | > 95% | Updates after caller correction |
| Permission accuracy | > 92% | yes/no/unknown classification |

---

## Mitigation Strategies

### Prevention
1. **Implicit confirmation patterns**: Detect "yahi", "same", "this one", etc.
2. **Ternary permission**: Allow yes/no/uncertain instead of binary
3. **Cross-turn tracking**: Update slots when caller corrects
4. **Confidence scores**: Mark low-confidence extractions for confirmation
5. **Structured extraction prompts**: Guide LLM with specific patterns
6. **Slot confirmation**: Repeat critical values back to caller

### Robust Extraction
```python
class SlotExtractor:
    """Extract slots with implicit handling and confidence"""
    
    IMPLICIT_CONFIRMATIONS = {
        "same_number": [
            "yahi", "isi pe", "same", "this one", 
            "this number", "is number pe", "haan yahi"
        ],
        "yes": [
            "haan", "yes", "sure", "okay", "ok", 
            "bilkul", "theek hai", "chalo"
        ]
    }
    
    HESITANT_MARKERS = [
        "i guess", "maybe", "let me see", "i suppose",
        "shayad", "dekhte hain", "pata nahi"
    ]
    
    def extract_permission(self, transcript: str, 
                           context: list) -> dict:
        """Extract permission with confidence"""
        transcript_lower = transcript.lower()
        
        # Check for hesitant markers first
        if any(m in transcript_lower for m in self.HESITANT_MARKERS):
            return {
                "value": "unknown",
                "confidence": 0.7,
                "needs_confirmation": True
            }
        
        # Check for clear yes
        if any(m in transcript_lower 
               for m in self.IMPLICIT_CONFIRMATIONS["yes"]):
            # But also check for negation
            if "no" in transcript_lower or "nahi" in transcript_lower:
                return {"value": "no", "confidence": 0.85}
            return {"value": "yes", "confidence": 0.9}
        
        # Check for clear no
        if "no" in transcript_lower or "nahi" in transcript_lower:
            return {"value": "no", "confidence": 0.9}
        
        return {"value": "unknown", "confidence": 0.5}
    
    def extract_whatsapp_number(self, transcript: str,
                                 called_number: str) -> dict:
        """Extract WhatsApp number with same-number detection"""
        transcript_lower = transcript.lower()
        
        # Check for same-number confirmation
        for pattern in self.IMPLICIT_CONFIRMATIONS["same_number"]:
            if pattern in transcript_lower:
                return {
                    "value": "same_number",
                    "resolved": called_number,
                    "confidence": 0.9
                }
        
        # Try to extract explicit number
        numbers = self.extract_phone_numbers(transcript)
        if numbers:
            return {
                "value": numbers[0],
                "confidence": 0.8,
                "needs_confirmation": True
            }
        
        return {"value": None, "confidence": 0.0}
    
    def update_slots(self, current_slots: dict, 
                     new_transcript: str,
                     turn_num: int) -> dict:
        """Update slots with correction handling"""
        correction_markers = [
            "actually", "i meant", "sorry i meant",
            "matlab", "actually not", "correction"
        ]
        
        has_correction = any(m in new_transcript.lower() 
                            for m in correction_markers)
        
        if has_correction:
            # Re-extract with priority to new values
            new_extraction = self.extract_all(new_transcript)
            for slot, value in new_extraction.items():
                if value["value"] is not None:
                    current_slots[slot] = value
                    current_slots[slot]["updated_turn"] = turn_num
        
        return current_slots
```

### Extraction Prompt Template
```
Extract the following information from the caller's response.
Use ONLY what the caller explicitly said or clearly implied.

Slots to extract:
- permission_to_send_playbook: "yes" | "no" | "unknown"
  - Use "yes" only for clear affirmative (haan, sure, ok)
  - Use "unknown" for hesitant responses (maybe, I guess, let me see)
  - Use "no" for clear decline

- whatsapp_number: 
  - "same_number" if they confirm the called number works
  - Actual 10-digit number if they provide different number
  - null if not mentioned or unclear

Implicit confirmations to recognize:
- "yahi number", "isi pe", "this one" → same_number
- "haan haan" → yes (if in response to permission question)

Current conversation turn:
{transcript}

Previous context:
{context}
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `slot.extraction.accuracy` | < 85% |
| `slot.implicit.miss_rate` | > 15% |
| `slot.permission.ambiguous` | > 20% |
| `slot.number.error_rate` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Extraction Accuracy Drop | accuracy < 80% | P2 |
| Permission Confusion High | ambiguous > 25% | P2 |
| Phone Number Errors | error > 12% | P1 |

---

## References

- [Slot Filling in Dialog](https://arxiv.org/abs/2009.13570) - Extraction techniques
- [Task-Oriented Dialog](https://arxiv.org/abs/2003.07490) - Slot tracking
- [Voice Commerce Research](https://www.beconversive.com/blog/voice-ai-challenges) - Extraction failures
- [AssistYou: ASR Issues](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Propagated errors
