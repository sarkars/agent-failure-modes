# Wrong Number / Wrong Person Handling

## Issue: Agent Fails to Detect or Handle When Call Reaches Unintended Recipient

**Frequency**: Common (5-10% of outbound calls)

**Symptoms**
- Agent pitches to wrong person entirely
- Caller says "wrong number" but agent continues
- Third party (friend, family) answers, agent proceeds as if target
- No verification that right person is on the line
- Privacy breach by discussing details with wrong person
- Wasted calls and negative brand impression

**Root Cause**
Outbound calls may reach the wrong person: number was reassigned, caller gave wrong number on form, someone else answered the phone, or number belongs to a shared device. Without proper verification and wrong-person detection, agents deliver pitches to confused strangers or discuss personal matters with unauthorized parties.

**Example**
```
Scenario 1: Reassigned number

Agent: "Hi! This is Riya from Zapp Chess—you filled our 
        Campus Ambassador form..."
Caller: "What? I've never heard of Zapp Chess."
Agent: "Oh, you filled the form on our website last week?"
Caller: "No, I think you have the wrong number."
Agent: "Are you sure? This is +91-98765-43210?"
Caller: "Yes, but I didn't fill any form."

← Number was reassigned to new owner
← Agent should have stopped immediately

---

Scenario 2: Someone else answered

[Call to college student's number]
Parent: "Hello?"
Agent: "Hi! You filled our Campus Ambassador form—
        interested in running a chess tournament?"
Parent: "What? Who is this?"
Agent: "Zapp Chess! So are you a college student?"
Parent: "No, I'm 50 years old. This is my daughter's phone."

← Should have asked if target person is available
← Pitched to wrong person

---

Scenario 3: Wrong number on form

[Applicant entered wrong digit in phone number]
Random person: "Hello?"
Agent: "Hi, calling about the ambassador form you filled!"
Random: "I didn't fill any form."
Agent: "Oh, maybe you forgot? It was for Zapp Chess..."

← Agent is insisting despite clear denial
← Should mark as wrong number immediately

---

Scenario 4: Shared device / business line

Receptionist: "ABC Company, how may I help you?"
Agent: "Hi! This is about the Campus Ambassador program..."
Receptionist: "This is a business line. Who are you trying to reach?"

← Agent didn't recognize business context
← Should have asked for specific person

---

Scenario 5: Correct handling

Agent: "Hi, is this the person who filled the Campus 
        Ambassador form for Zapp Chess?"
Caller: "No, that's my roommate. Let me get her."
[Pause]
Target: "Hello?"
Agent: "Hi! You filled the ambassador form—got a minute?"

← Asked if right person
← Waited for correct person
← Then continued

---

Wrong number/person analysis (1,000 outbound calls):
  Correct person answered: 850 (85%)
  Wrong number: 67 (6.7%)
  Someone else answered: 58 (5.8%)
  Business/shared line: 25 (2.5%)
  
  Detection rate:
    Detected and handled correctly: 68%
    Pitched to wrong person: 22%
    Argued with caller: 10%
```

**Key Statistics**
From Outbound Call Research (2026):
- Wrong number/person rate: 8-15%
- Number reassignment rate: 3-5% annually
- Someone else answering: 10-15%
- Correct detection rate: 60-80%
- Privacy complaints from wrong-person: 2-5%

**Wrong Person Scenarios**
| Scenario | Signal | Correct Action |
|----------|--------|----------------|
| Number reassigned | "Never heard of you" | Apologize, close, update CRM |
| Someone else answered | Different voice/name | Ask for target person |
| Wrong number on form | "Didn't fill form" | Apologize, close, flag data |
| Business line | Company greeting | Ask for specific person |
| Shared device | "Whose form?" | Ask for form filler |

**Contributing Factors**
- No verification question in opening
- Assumed phone number = target person
- Ignored "wrong number" signals
- No handling for third-party answer
- Continued pitch despite denial
- No CRM update for bad numbers

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Clear wrong number | "Wrong number" | Apologize, close | Continue pitch |
| Never heard | "Never filled form" | Verify, then close | Argue |
| Someone else | "That's my son" | Ask for son | Pitch to parent |
| Business line | "ABC Company" | Ask for person | Pitch to receptionist |
| Denial + confirm | "Not me" → verify → "Still not me" | Close gracefully | Push further |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Wrong number detection | > 95% | When caller denies |
| Wrong person detection | > 90% | When not target |
| First-signal response | > 90% | Stop on first indication |
| Privacy complaints | < 1% | Complaints from wrong recipient |

---

## Mitigation Strategies

### Prevention
1. **Verification opening**: Confirm identity before pitch
2. **Wrong-number detection**: Catch "wrong number" phrases
3. **Third-party handling**: Ask if target is available
4. **Graceful exit**: Apologize and close immediately
5. **CRM flagging**: Mark bad numbers for data cleanup
6. **Privacy protection**: Don't share details until verified

### Implementation
```python
class WrongPersonDetector:
    """Detect wrong number / wrong person scenarios"""
    
    WRONG_NUMBER_SIGNALS = [
        "wrong number", "wrong person", 
        "never heard of", "don't know what",
        "didn't fill", "never filled",
        "who is this for", "what form",
        "I'm not", "that's not me",
        "galat number", "yeh mera nahi"
    ]
    
    THIRD_PARTY_SIGNALS = [
        "that's my", "this is his", "this is her",
        "let me get", "she's not here", "he's not here",
        "hold on", "one second", "unka phone",
        "who should I say", "may I ask who"
    ]
    
    BUSINESS_SIGNALS = [
        "company", "office", "reception",
        "how may I help", "how can I direct",
        "business hours"
    ]
    
    def detect(self, transcript: str) -> dict:
        """Detect wrong person/number scenarios"""
        transcript_lower = transcript.lower()
        
        # Check for wrong number
        if any(signal in transcript_lower 
               for signal in self.WRONG_NUMBER_SIGNALS):
            return {
                "type": "wrong_number",
                "action": "apologize_and_close",
                "update_crm": "flag_bad_number"
            }
        
        # Check for third party
        if any(signal in transcript_lower 
               for signal in self.THIRD_PARTY_SIGNALS):
            return {
                "type": "third_party",
                "action": "ask_for_target",
                "script": "Is [target] available?"
            }
        
        # Check for business line
        if any(signal in transcript_lower 
               for signal in self.BUSINESS_SIGNALS):
            return {
                "type": "business_line",
                "action": "ask_for_specific_person",
                "script": "Could you connect me to the person "
                         "who filled our form?"
            }
        
        return {"type": "likely_correct"}
    
    def get_response(self, detection: dict, 
                     language: str = "english") -> str:
        """Get appropriate response for scenario"""
        responses = {
            "wrong_number": {
                "english": "Oh sorry, my bad! Wrong number. Bye!",
                "hindi": "Arrey sorry, galat number. Bye!",
                "hinglish": "Oh sorry, wrong number. Bye!"
            },
            "third_party": {
                "english": "Oh, is the person who filled the form available?",
                "hindi": "Accha, jo form bhara tha woh available hai?",
                "hinglish": "Oh, is the person who filled form available?"
            },
            "business_line": {
                "english": "Sorry to bother! Could you help me reach "
                          "someone who filled our campus form?",
                "hindi": "Sorry! Kya aap mujhe connect kar sakte hain?",
                "hinglish": "Sorry! Can you connect me to the person?"
            }
        }
        
        action_type = detection["type"]
        return responses.get(action_type, {}).get(
            language, responses[action_type]["english"]
        )


class VerificationOpening:
    """Opening that verifies right person"""
    
    VERIFICATION_OPENINGS = {
        "soft_verify": [
            "Hi! Is this the person who filled the Campus "
            "Ambassador form for Zapp Chess?",
            
            "Hey! Did you fill the Zapp Chess ambassador "
            "form recently?"
        ],
        "post_third_party": [
            "Hey! You filled the ambassador form—got a minute?",
            
            "Hi! Following up on the form you filled. "
            "Got a quick sec?"
        ]
    }
    
    def should_verify(self, call_context: dict) -> bool:
        """Determine if verification needed"""
        # Always verify on outbound if not warm transfer
        return call_context.get("direction") == "outbound"
    
    def get_verification_opening(self, scenario: str) -> str:
        """Get appropriate verification opening"""
        openings = self.VERIFICATION_OPENINGS.get(
            scenario, self.VERIFICATION_OPENINGS["soft_verify"]
        )
        return random.choice(openings)
```

### Prompt Design
```yaml
instructions: |
  ## WRONG NUMBER / WRONG PERSON HANDLING
  
  OPENING should verify identity:
  - "Hi! Is this the person who filled the Zapp Chess form?"
  - Wait for confirmation before pitching
  
  If caller says ANY of these, STOP IMMEDIATELY:
  - "Wrong number"
  - "Never heard of you/this"
  - "Didn't fill any form"
  - "Who?"
  - "That's not me"
  
  Response: "Oh sorry, my bad! Bye!"
  
  Do NOT:
  - Argue ("Are you sure?")
  - Insist ("You must have forgotten")
  - Continue pitch
  
  If SOMEONE ELSE answered:
  - "That's my daughter" → "Is she available?"
  - "He's not here" → "When's a good time to call back?"
  - "This is his mom" → Don't pitch to mom
  
  If BUSINESS LINE:
  - "ABC Company" → "Could you connect me to [person]?"
  - Don't pitch to receptionist
  
  Mark outcome as:
  - "wrong_number" - if number is wrong
  - "not_available" - if target not there
  - Continue only if you reach the right person
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `wrong_number.detection` | < 90% |
| `wrong_number.pitched_anyway` | > 10% |
| `wrong_person.detection` | < 85% |
| `wrong_number.privacy_complaints` | > 1% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Wrong Number Not Detected | detection < 85% | P2 |
| Pitched to Wrong Person | > 15% | P1 |
| Privacy Complaint | Any occurrence | P1 |

---

## References

- [Outbound Call Quality](https://www.beconversive.com/blog/voice-ai-challenges) - Verification
- [Voice Agent Privacy](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Wrong person issues
- [CRM Data Quality](https://getbluejay.ai/resources/voice-agent-production-failures) - Bad numbers
- [Identity Verification](https://arxiv.org/abs/2106.07837) - Voice verification
