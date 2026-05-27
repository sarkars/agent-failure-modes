# Multi-Field Collection Overload

## Issue: Agent Asks for Multiple Data Fields in a Single Turn

**Frequency**: Very Common

**Symptoms**
- Agent asks for name, email, and phone in one sentence
- Caller answers only first item, others forgotten
- Agent must re-ask for missed fields
- Caller provides fields in wrong order
- Transcription errors multiply with combined input
- Conversation becomes frustrating loop

**Root Cause**
Collecting information over voice is harder than over text. Unlike forms where users see all fields simultaneously, voice is sequential and fleeting. When agents ask for multiple fields ("What's your name, date of birth, and phone number?"), callers forget items, provide them out of order, or only answer the first one. Each field should be collected, confirmed, and then moved on from.

**Example**
```
Scenario 1: Multiple fields, partial answer

Agent: "Great! Can I get your name, date of birth, and 
        phone number?"
Caller: "John Smith."
Agent: "Thanks John! And your date of birth and phone number?"
Caller: "Sorry, what was the second one again?"

← Agent asked 3 fields at once
← Caller only answered first one
← Must re-ask for remaining fields

---

Scenario 2: Out-of-order confusion

Agent: "What's your name, email, and college?"
Caller: "MIT, john@mit.edu, John Chen."
Agent: [Confused about which is which]
        "So your name is MIT?"
Caller: "No, MIT is my college."

← Caller answered in reverse order
← Agent couldn't parse correctly
← Requires clarification

---

Scenario 3: Transcription errors compound

Agent: "What's your phone number and email address?"
Caller: "9876543210, john.chen@gmail.com"
ASR: "9876543210 john.chen@gmail.com"

Agent: [Trying to split] "Your phone is 9876543210 john and 
        email is chen@gmail.com?"

← No clear delimiter between fields
← ASR merged them together
← Agent split incorrectly

---

Scenario 4: Cognitive overload

Agent: "I need your shipping address - street address, city, 
        state, and zip code."
Caller: "Uh... 123 Main Street... um... San Francisco... 
         wait, what else did you need?"
Agent: "State and zip code."
Caller: "California. What was the last one?"
Agent: "Zip code."
Caller: "94102."

← 4 fields is too many
← Caller forgot after 2 items
← Took 5 turns instead of 4 sequential asks

---

Scenario 5: Correct sequential collection

Agent: "What's your name?"
Caller: "John Chen."
Agent: "Got it, John Chen. And your phone number?"
Caller: "9876543210."
Agent: "9-8-7-6-5-4-3-2-1-0, correct?"
Caller: "Yes."
Agent: "And finally, your email?"
Caller: "john.chen@gmail.com"
Agent: "john.chen@gmail.com - all set!"

← One field at a time
← Confirmation after each
← No cognitive overload
← Clean transcription

---

Multi-field collection analysis:
  
  Multi-field asks: 45% of data collection
  Single-field asks: 55%
  
  Success rate:
    1 field per turn: 92% first-try success
    2 fields per turn: 71% first-try success
    3+ fields per turn: 48% first-try success
  
  Re-ask rate:
    1 field: 8%
    2 fields: 29%
    3+ fields: 52%
  
  Average turns to collect 3 fields:
    Multi-field ask: 5.2 turns (re-asks, confusion)
    Sequential asks: 3.4 turns (direct collection)
```

**Key Statistics**
From VAPI Voice Data Collection Research (2026):
- Multi-field asks cause partial answers: 60%
- Re-ask rate for multi-field: 40-50%
- Single field success rate: 90%+
- Cognitive overload at 3+ fields: significant
- Sequential collection saves 20-30% time

**Field Collection Issues**
| Fields Asked | Success Rate | Re-ask Rate | Caller Frustration |
|-------------|--------------|-------------|-------------------|
| 1 | 92% | 8% | Low |
| 2 | 71% | 29% | Medium |
| 3 | 48% | 52% | High |
| 4+ | 25% | 75% | Very High |

**Contributing Factors**
- Text form patterns applied to voice
- Efficiency assumption (more fields = faster)
- No cognitive load awareness
- Missing confirmation steps
- ASR can't delimit multiple values
- No field boundary detection

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Single field | Ask name only | Clean capture | Multiple fields asked |
| Two fields | Ask name, then phone | Sequential | Both in one question |
| Confirmation | Each field | Read back | Skip confirmation |
| Address | 4 parts | 4 sequential questions | All at once |
| Retry handling | Caller gives 1 of 2 | Re-ask second only | Re-ask both |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Fields per turn | 1 | Turn analysis |
| First-try success | > 90% | Single-attempt captures |
| Re-ask rate | < 15% | Re-collection needed |
| Confirmation rate | 100% | Confirm each field |

---

## Mitigation Strategies

### Prevention
1. **Single field per turn**: Always ask one field at a time
2. **Confirm before proceeding**: Read back each value
3. **Sequential flow**: Name → Confirm → Phone → Confirm → Email → Confirm
4. **Graceful re-ask**: Only re-ask missing fields
5. **Spell-back for names/emails**: Verify letter by letter
6. **DTMF for numbers**: Allow keypad entry when possible

### Implementation
```python
class SequentialFieldCollector:
    """Collect fields one at a time with confirmation"""
    
    def __init__(self, required_fields: list):
        self.fields = required_fields
        self.collected = {}
        self.current_index = 0
        self.awaiting_confirmation = False
        self.pending_value = None
    
    def get_next_prompt(self) -> dict:
        """Get next collection prompt"""
        if self.awaiting_confirmation:
            return self.get_confirmation_prompt()
        
        if self.current_index >= len(self.fields):
            return {"done": True, "collected": self.collected}
        
        field = self.fields[self.current_index]
        
        return {
            "done": False,
            "field": field,
            "prompt": self.field_prompts.get(
                field, f"What's your {field}?"
            )
        }
    
    field_prompts = {
        "name": "What's your name?",
        "phone": "And your phone number?",
        "email": "What's your email address?",
        "college": "Which college are you from?",
        "dob": "What's your date of birth?"
    }
    
    def process_response(self, value: str) -> dict:
        """Process caller's response"""
        field = self.fields[self.current_index]
        
        if self.awaiting_confirmation:
            return self.handle_confirmation(value)
        
        # Store pending value, await confirmation
        self.pending_value = value
        self.awaiting_confirmation = True
        
        return {
            "action": "confirm",
            "prompt": self.get_confirmation_prompt()
        }
    
    def get_confirmation_prompt(self) -> dict:
        """Get confirmation prompt for current field"""
        field = self.fields[self.current_index]
        value = self.pending_value
        
        confirmations = {
            "phone": f"That's {self.format_phone(value)}, correct?",
            "email": f"So that's {self.spell_out_email(value)}?",
            "name": f"Got it, {value}. Did I get that right?",
            "default": f"I heard {value}. Is that correct?"
        }
        
        return {
            "field": field,
            "prompt": confirmations.get(field, confirmations["default"])
        }
    
    def handle_confirmation(self, response: str) -> dict:
        """Handle confirmation response"""
        if self.is_affirmative(response):
            # Store confirmed value
            field = self.fields[self.current_index]
            self.collected[field] = self.pending_value
            self.current_index += 1
            self.awaiting_confirmation = False
            self.pending_value = None
            
            return {
                "action": "next",
                "prompt": self.get_next_prompt()
            }
        else:
            # Re-ask current field
            self.awaiting_confirmation = False
            self.pending_value = None
            
            return {
                "action": "re-ask",
                "prompt": f"Sorry, let me get that again. " + 
                         self.get_next_prompt()["prompt"]
            }
    
    def is_affirmative(self, response: str) -> bool:
        """Check if response is affirmative"""
        affirmatives = [
            "yes", "yeah", "yep", "correct", "right", 
            "that's right", "uh-huh", "haan", "ha"
        ]
        return any(a in response.lower() for a in affirmatives)
    
    def format_phone(self, phone: str) -> str:
        """Format phone for spoken confirmation"""
        digits = ''.join(filter(str.isdigit, phone))
        return '-'.join([digits[i:i+3] for i in range(0, len(digits), 3)])
    
    def spell_out_email(self, email: str) -> str:
        """Spell out email for confirmation"""
        return email.replace("@", " at ").replace(".", " dot ")


class MultiFieldDetector:
    """Detect and prevent multi-field questions"""
    
    MULTI_FIELD_PATTERNS = [
        r"your (name|phone|email).*(and|,).*(name|phone|email)",
        r"(name|phone|email).*(,|and).*(name|phone|email)",
        r"need.*(name|phone|email).*(and|,)",
        r"(first|last) name.*(phone|email)"
    ]
    
    def check_prompt(self, prompt: str) -> dict:
        """Check if prompt asks for multiple fields"""
        prompt_lower = prompt.lower()
        
        # Count distinct fields mentioned
        fields = ["name", "phone", "email", "address", 
                  "date of birth", "dob", "college"]
        found_fields = [f for f in fields if f in prompt_lower]
        
        if len(found_fields) > 1:
            return {
                "multi_field": True,
                "fields": found_fields,
                "recommendation": self.suggest_split(found_fields)
            }
        
        return {"multi_field": False}
    
    def suggest_split(self, fields: list) -> list:
        """Suggest how to split into sequential asks"""
        return [
            f"Step {i+1}: Ask for {field}, then confirm"
            for i, field in enumerate(fields)
        ]
```

### Prompt Design
```yaml
instructions: |
  ## DATA COLLECTION RULES
  
  ALWAYS collect ONE field at a time:
  
  1. Ask for ONE piece of information
  2. Wait for response
  3. Confirm/read back what you heard
  4. Wait for confirmation
  5. Move to next field
  
  CORRECT:
  Agent: "What's your name?"
  Caller: "John Smith"
  Agent: "John Smith, got it. And your phone number?"
  Caller: "9876543210"
  Agent: "9-8-7-6-5-4-3-2-1-0, correct?"
  Caller: "Yes"
  Agent: "Finally, your email?"
  
  WRONG:
  Agent: "What's your name, phone, and email?"
  Caller: "John Smith 9876543210..."
  Agent: [Confused]
  
  SPELL BACK for names and emails:
  - "That's J-O-H-N at gmail dot com?"
  
  For phone numbers, read back in groups:
  - "9-8-7, 6-5-4, 3-2-1-0"
  
  If caller gives multiple fields unprompted:
  - Capture what you can
  - Confirm each separately
  - Ask for anything missed
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `collection.multi_field_asks` | > 10% |
| `collection.re_ask_rate` | > 20% |
| `collection.first_try_success` | < 85% |
| `collection.turns_per_field` | > 1.5 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Multi-Field Asks | > 20% | P2 |
| High Re-ask Rate | > 30% | P2 |
| Low First-Try Success | < 75% | P1 |
| No Confirmation | < 80% | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - One field at a time
- [Voice AI Data Collection](https://www.callcow.ai/blog/ai-voice-agent-forms-platform) - Best practices
- [Assembly AI: Voice Agent Features](https://www.assemblyai.com/blog/voice-agent-features) - Collection patterns
- [Brilo AI: Structured Data](https://learn.brilo.ai/en/articles/13856788) - DTMF and confirmation
