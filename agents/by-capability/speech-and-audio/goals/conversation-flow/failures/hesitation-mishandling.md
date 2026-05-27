# Hesitation Mishandling

## Issue: Agent Pressures Hesitant Callers Instead of Providing Low-Friction Options

**Frequency**: Common

**Symptoms**
- Agent pushes for commitment when caller is unsure
- "Maybe" treated as "no" requiring persuasion
- No low-pressure alternatives offered
- Hesitation triggers more aggressive pitch
- Caller feels cornered into decision
- Soft interest escalated to hard commitment ask

**Root Cause**
Voice agents are often designed for binary outcomes: interested or not interested. Hesitation—"I'm not sure," "maybe," "let me think"—falls between these categories. Without specific handling for uncertainty, agents either treat it as rejection (and re-pitch) or as acceptance (and push forward), both of which frustrate hesitant callers.

**Example**
```
Scenario 1: Pushing for commitment

Caller: "I don't know, maybe... I'd have to think about it"
Agent: "I totally understand! But let me tell you, this is 
        a really great opportunity—you'd get a certificate, 
        trophy, and the LinkedIn shoutout is amazing..."

← Caller said "think about it"
← Agent re-pitched instead of giving space

Better: "No pressure! I can share the playbook—you can 
        read it and decide. Sound okay?"

---

Scenario 2: Treating maybe as yes

Caller: "Hmm, I guess it could be interesting"
Agent: "Great! So which college are you at?"

← Caller was tentative ("I guess")
← Agent rushed to next step as if confirmed

Better: "Cool—want me to share the details so you can 
        take a look first?"

---

Scenario 3: Binary framing

Agent: "So are you interested—yes or no?"
Caller: "I mean... I'm not NOT interested, but..."
Agent: "Perfect, so you ARE interested! Let me get your 
        WhatsApp—"

← Forced binary choice
← Interpreted hesitation as agreement

Better: "Sounds like you're curious but not sure. Want 
        the playbook to check it out? No commitment."

---

Scenario 4: No low-friction option

Caller: "This sounds like a lot of work"
Agent: "It's actually not! You just need to run one 
        tournament and we provide everything—"

← Addressed the objection
← But didn't offer a low-pressure next step

Better: "Fair! The playbook shows exactly what's involved. 
        Want me to send it? You can decide after reading."

---

Scenario 5: Escalating pressure

Turn 1 - "I'm not sure" → Agent explains benefits
Turn 2 - "Still thinking" → Agent adds more perks
Turn 3 - "Maybe later" → Agent asks for commitment anyway

← Each hesitation met with more pressure
← Should have offered exit/deferral earlier

---

Hesitation handling analysis (300 hesitant responses):
  Low-pressure option offered: 112 (37%)
  Re-pitched/pressured: 134 (45%)
  Treated as yes: 54 (18%)
  
  Outcome by handling:
    Low-pressure → 52% eventual qualification
    Pressure → 23% eventual qualification
    Treat as yes → 15% valid qualification
```

**Key Statistics**
From Voice Agent Hesitation Research (2026):
- Hesitant responses: 25-40% of calls
- Correct low-pressure handling: 30-50%
- Pressure after hesitation: 35-50%
- Conversion from low-pressure path: 45-55%
- Conversion from pressure path: 15-25%
- User satisfaction drop from pressure: -35%

**Hesitation Types**
| Expression | Meaning | Correct Response |
|------------|---------|------------------|
| "Maybe" | Needs more info | Offer details, no pressure |
| "I guess" | Tentative interest | Confirm before proceeding |
| "Not sure" | Uncertain | Provide low-friction next step |
| "Let me think" | Wants time | Offer to send info |
| "Sounds like a lot" | Concern | Address, offer easy option |

**Contributing Factors**
- Binary intent classification
- Conversion pressure in design
- No "curious but uncommitted" flow
- Hesitation treated as objection
- Missing deferral options
- Prompt emphasizes closing

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Maybe | "Maybe, I'm not sure" | Low-pressure option | Re-pitch |
| Let me think | "Let me think about it" | Offer playbook | Push for answer |
| I guess | "I guess it's interesting" | Confirm before next step | Rush forward |
| Not NOT interested | "I'm not saying no..." | Acknowledge uncertainty | Treat as yes |
| Sounds like a lot | "That's a lot of work" | Easy next step | Counter-argue |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Low-pressure offer rate | > 80% | When hesitation detected |
| Pressure after hesitation | < 10% | Re-pitch detection |
| Hesitant → Qualified | > 40% | Via low-pressure path |
| Satisfaction (hesitant callers) | > 4/5 | Post-call survey |

---

## Mitigation Strategies

### Prevention
1. **Hesitation detection**: Identify uncertainty markers
2. **Low-pressure defaults**: Always offer easy next step
3. **Confirmation before progress**: Don't treat "I guess" as "yes"
4. **Information without commitment**: Offer to send details
5. **Exit ramps**: Make it easy to defer or decline
6. **No re-pitching uncertainty**: Accept hesitation gracefully

### Implementation
```python
class HesitationHandler:
    """Handle hesitant responses with low-pressure options"""
    
    HESITATION_MARKERS = [
        "maybe", "not sure", "i guess", "i don't know",
        "let me think", "thinking about it", "possibly",
        "might be", "could be", "sounds like a lot",
        "i'm not saying no", "shayad", "pata nahi",
        "sochna padega", "dekhte hain"
    ]
    
    SOFT_INTEREST = [
        "i guess", "could be interesting", "might be",
        "not not interested", "maybe interested"
    ]
    
    LOW_PRESSURE_RESPONSES = {
        "needs_info": [
            "No pressure! Want me to share the playbook so you "
            "can take a look? You can decide after.",
            
            "Totally get it. How about I send the details and "
            "you can check it out when you have time?",
            
            "Fair enough! I can share more info on WhatsApp—"
            "no commitment. Sound okay?"
        ],
        "needs_time": [
            "No rush! Want the playbook to read through first?",
            
            "Take your time. I can send the details and you "
            "can get back whenever.",
            
            "Sure, think it over. Want me to send the info so "
            "you have it when you're ready?"
        ],
        "concerns": [
            "The playbook shows exactly what's involved—want me "
            "to share it so you can see?",
            
            "I get that. Might help to see the details first. "
            "Can I send the playbook?"
        ]
    }
    
    def is_hesitant(self, transcript: str) -> bool:
        """Detect hesitation in response"""
        transcript_lower = transcript.lower()
        return any(marker in transcript_lower 
                   for marker in self.HESITATION_MARKERS)
    
    def classify_hesitation(self, transcript: str) -> str:
        """Classify type of hesitation"""
        transcript_lower = transcript.lower()
        
        if any(m in transcript_lower for m in 
               ["think", "time", "later", "sochna"]):
            return "needs_time"
        
        if any(m in transcript_lower for m in 
               ["lot", "work", "busy", "commitment"]):
            return "concerns"
        
        return "needs_info"
    
    def get_low_pressure_response(self, 
                                   hesitation_type: str) -> str:
        """Get appropriate low-pressure response"""
        options = self.LOW_PRESSURE_RESPONSES.get(
            hesitation_type, 
            self.LOW_PRESSURE_RESPONSES["needs_info"]
        )
        return random.choice(options)
    
    def should_confirm_before_proceeding(self, 
                                          transcript: str) -> bool:
        """Check if we need to confirm soft interest"""
        transcript_lower = transcript.lower()
        return any(marker in transcript_lower 
                   for marker in self.SOFT_INTEREST)


class HesitationAwareFlow:
    """Conversation flow that handles hesitation properly"""
    
    def __init__(self):
        self.handler = HesitationHandler()
    
    def process_interest_response(self, 
                                   caller_response: str) -> dict:
        # Check for hesitation
        if self.handler.is_hesitant(caller_response):
            hesitation_type = self.handler.classify_hesitation(
                caller_response
            )
            
            return {
                "classification": "hesitant",
                "response": self.handler.get_low_pressure_response(
                    hesitation_type
                ),
                "next_step": "offer_playbook",
                "do_not": ["re-pitch", "push_for_commitment", 
                           "ask_more_questions"]
            }
        
        # Check for soft interest that needs confirmation
        if self.handler.should_confirm_before_proceeding(
            caller_response
        ):
            return {
                "classification": "soft_interest",
                "response": "Sounds like you're curious—want me to "
                           "share the details so you can see more?",
                "next_step": "confirm_before_college",
                "do_not": ["assume_commitment", "skip_to_whatsapp"]
            }
        
        # Clear interest
        return {
            "classification": "interested",
            "next_step": "capture_college"
        }
```

### Prompt Design
```yaml
instructions: |
  ## HESITATION HANDLING (IMPORTANT)
  
  When caller seems UNSURE ("maybe", "not sure", "I guess",
  "let me think", "sounds like a lot"):
  
  DO:
  - Offer the playbook as a no-commitment next step
  - Give them space to decide
  - Make it easy to say no or defer
  
  DON'T:
  - Re-pitch or add more benefits
  - Push for a yes/no answer
  - Treat "I guess" as confirmed interest
  - Ask the next script question
  
  LOW-PRESSURE PHRASES:
  - "No pressure! Want me to share the playbook?"
  - "Take your time—I can send the details."
  - "No commitment—just something to look at."
  
  NEVER SAY after hesitation:
  - "But let me tell you..."
  - "The thing is..."
  - "You should really consider..."
  - "It's actually not that much work..."
  
  If they're hesitant, the goal becomes:
  "Get playbook permission" NOT "Get full qualification"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `hesitation.low_pressure.rate` | < 70% |
| `hesitation.repitch.rate` | > 20% |
| `hesitation.conversion` | < 30% |
| `hesitation.satisfaction` | < 3.5/5 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Pressure After Hesitation | repitch > 30% | P2 |
| Low Conversion (Hesitant) | conversion < 25% | P3 |
| Satisfaction Drop | rating < 3/5 | P2 |

---

## References

- [Conversational Persuasion](https://arxiv.org/abs/2106.07837) - Pressure vs. facilitation
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - Handling uncertainty
- [Sales Conversation Research](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Soft interest
- [Dialog Design](https://arxiv.org/abs/2009.07261) - Decision support
