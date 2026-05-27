# Opening Timing Mismatch

## Issue: Agent Opening Doesn't Account for Caller's Greeting State

**Frequency**: Common

**Symptoms**
- Agent starts mid-sentence when caller already greeted
- Awkward double-greeting exchanges
- Agent ignores caller's "hello" and launches into script
- Opening sounds pre-recorded or robotic
- Context disconnect between caller's state and agent's opening

**Root Cause**
Voice agents often have scripted openings triggered by call connection. But callers may answer with greetings ("Hello?", "Hi"), questions ("Who is this?"), or statements ("Yeah, speaking") before the agent speaks. Without dynamic opening adaptation, the agent's first utterance ignores the caller's state, creating an immediate disconnect.

**Example**
```
Scenario 1: Caller greeted first, agent ignores

Caller: "Hello?"
Agent: "Hi! This is Riya from Zapp Chess, you had 
        filled the Campus Ambassador form—"

← Agent should acknowledge "Hello" before launching

Better: "Hi! This is Riya from Zapp Chess..."
        (Matches the greeting, then continues)

---

Scenario 2: Double greeting

Agent: "Hi! This is—"
Caller: [simultaneously] "Hello?"
Agent: "—Riya from Zapp Chess. Hi! So you had filled—"

← Awkward overlap and double "Hi"

---

Scenario 3: Mid-pickup sound

[Call connects]
Agent: "—so I'm calling about the Campus Ambassador form 
        you filled. Do you have a minute?"

← Sounds like conversation started before connection
← Missing greeting entirely

---

Scenario 4: Caller asked who's calling

Caller: "Hello, who is this?"
Agent: "Hi! This is Riya from Zapp Chess. You had filled 
        the Campus Ambassador form—do you have a minute?"

← Good: Agent answered the question naturally

---

Scenario 5: Aggressive caller

Caller: "Yeah, what?"
Agent: "Hi! This is Riya from Zapp Chess! You had filled 
        our amazing Campus Ambassador form and we're SO 
        excited to tell you about—"

← Tone mismatch with caller's curt response

Better: "Hey, this is Riya from Zapp Chess—about the 
        ambassador form. Got a minute?"

---

Opening analysis (500 calls):
  Natural opening exchange: 312 (62%)
  Awkward/mismatched: 188 (38%)
  
  Mismatch types:
    Ignored caller greeting: 35%
    Tone mismatch: 25%
    Double greeting: 20%
    Mid-pickup sound: 12%
    Question ignored: 8%
```

**Key Statistics**
From Voice Agent Opening Research (2026):
- Opening mismatch rate: 30-45%
- Caller drops within 5 seconds (bad opening): 15-25%
- "Sounds like a bot" perception: 40-60%
- Natural opening correlation with completion: +35%

**Opening Mismatch Types**
| Type | Description | Impact |
|------|-------------|--------|
| Greeting ignored | Caller said hello, agent scripts on | Impersonal |
| Double greeting | Both say hi at same time | Awkward |
| Mid-pickup | Sounds like started before connect | Robotic |
| Tone mismatch | Enthusiastic vs curt caller | Dissonance |
| Question ignored | "Who is this?" not answered | Rude |

**Contributing Factors**
- Static scripted opening
- No wait for caller's first utterance
- No adaptation based on caller's greeting
- TTS starts immediately on connect
- No tone matching capability
- Greeting interruption disabled

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Caller says hello | "Hello?" | Natural response to hello | Script ignores |
| Caller asks who | "Who is this?" | Answer question | Launch into pitch |
| Curt response | "Yeah, what?" | Matched brief tone | Over-enthusiastic |
| No greeting | [silence] | Agent initiates | Wait too long |
| Simultaneous | Both speak | Agent yields | Agent continues |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Opening naturalness | > 85% | Human evaluation |
| Greeting acknowledgment | > 95% | Caller hello → agent responds |
| Double greeting rate | < 5% | Both say hi |
| Mid-pickup perception | < 3% | "Sounded pre-recorded" |

---

## Mitigation Strategies

### Prevention
1. **Wait for caller**: Brief pause after connect before speaking
2. **Dynamic opening**: Adapt based on caller's first words
3. **Greeting templates**: Multiple openings for different scenarios
4. **Tone matching**: Adjust energy to caller's tone
5. **Question handling**: Answer "who is this" before continuing
6. **Overlap detection**: Yield if caller starts speaking

### Implementation
```python
class OpeningManager:
    """Manage dynamic conversation openings"""
    
    GREETING_PATTERNS = [
        "hello", "hi", "hey", "haan", "yes", "speaking",
        "bolo", "haan bolo", "ji"
    ]
    
    QUESTION_PATTERNS = [
        "who is this", "kaun", "kon bol raha", 
        "who's calling", "kahan se"
    ]
    
    CURT_PATTERNS = [
        "yeah", "what", "haan", "bol", "bolo"
    ]
    
    OPENING_TEMPLATES = {
        "standard": (
            "Hi! This is Riya from Zapp Chess—you had filled "
            "the Campus Ambassador form. Got a minute?"
        ),
        "after_hello": (
            "Hi! This is Riya from Zapp Chess, calling about "
            "the Campus Ambassador form you filled. Got a sec?"
        ),
        "answer_who": (
            "This is Riya from Zapp Chess—the chess app. "
            "You'd filled our Campus Ambassador form. "
            "Is this a good time?"
        ),
        "curt_match": (
            "Hey, Riya from Zapp Chess—about the ambassador "
            "form. Got a minute?"
        ),
        "no_greeting": (
            "Hi! This is Riya from Zapp Chess..."
        )
    }
    
    def __init__(self, wait_for_caller=True, max_wait_ms=1500):
        self.wait_for_caller = wait_for_caller
        self.max_wait_ms = max_wait_ms
    
    def analyze_caller_opening(self, transcript: str) -> dict:
        """Analyze caller's first utterance"""
        if not transcript or transcript.strip() == "":
            return {"type": "no_greeting", "tone": "neutral"}
        
        transcript_lower = transcript.lower().strip()
        
        # Check for question
        if any(q in transcript_lower for q in self.QUESTION_PATTERNS):
            return {"type": "question", "tone": "curious"}
        
        # Check for curt response
        if (len(transcript_lower.split()) <= 2 and 
            any(c in transcript_lower for c in self.CURT_PATTERNS)):
            return {"type": "greeting", "tone": "curt"}
        
        # Check for greeting
        if any(g in transcript_lower for g in self.GREETING_PATTERNS):
            return {"type": "greeting", "tone": "neutral"}
        
        return {"type": "unknown", "tone": "neutral"}
    
    def get_opening(self, caller_opening: dict) -> str:
        """Get appropriate opening based on caller's state"""
        opening_type = caller_opening.get("type", "no_greeting")
        tone = caller_opening.get("tone", "neutral")
        
        if opening_type == "question":
            return self.OPENING_TEMPLATES["answer_who"]
        
        if opening_type == "greeting" and tone == "curt":
            return self.OPENING_TEMPLATES["curt_match"]
        
        if opening_type == "greeting":
            return self.OPENING_TEMPLATES["after_hello"]
        
        return self.OPENING_TEMPLATES["standard"]
    
    def should_yield(self, caller_speaking: bool, 
                     agent_speaking: bool) -> bool:
        """Determine if agent should yield to caller"""
        # If both speaking, agent yields
        return caller_speaking and agent_speaking


class CallFlowManager:
    """Manage call connection and opening"""
    
    def __init__(self):
        self.opening_manager = OpeningManager()
    
    async def handle_call_connect(self, call_context: dict) -> dict:
        """Handle initial call connection"""
        
        # Wait briefly for caller to speak first
        caller_utterance = await self.wait_for_caller_speech(
            timeout_ms=1500
        )
        
        # Analyze what caller said (if anything)
        caller_analysis = self.opening_manager.analyze_caller_opening(
            caller_utterance
        )
        
        # Get appropriate opening
        opening = self.opening_manager.get_opening(caller_analysis)
        
        return {
            "agent_opening": opening,
            "caller_state": caller_analysis,
            "delay_ms": 200 if caller_utterance else 800
        }
    
    async def wait_for_caller_speech(self, timeout_ms: int) -> str:
        """Wait for caller's first utterance"""
        # Implementation depends on voice platform
        # Returns transcript if caller spoke, empty string if timeout
        pass
```

### Prompt Design
```yaml
instructions: |
  ## OPENING RULES
  
  The call should NOT sound like it starts mid-pickup.
  
  IF the caller has already greeted (said "hello", "hi", etc):
  → Respond naturally to their greeting before your opening
  → Example: Caller: "Hello?" → "Hi! This is Riya from..."
  
  IF the caller asks "who is this?":
  → Answer the question first
  → "This is Riya from Zapp Chess—the chess app."
  → Then continue with purpose of call
  
  IF the caller sounds curt ("yeah", "what"):
  → Match their energy—be brief, not over-enthusiastic
  → "Hey, Riya from Zapp Chess—about the ambassador form."
  
  IF there's overlap (both start talking):
  → Yield to the caller
  → Wait for them to finish, then respond
  
  TONE MATCHING:
  - Enthusiastic caller → Warm and upbeat
  - Neutral caller → Friendly and professional  
  - Curt/busy caller → Brief and direct
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `opening.mismatch.rate` | > 20% |
| `opening.greeting.ignored` | > 10% |
| `opening.double_greeting` | > 10% |
| `opening.drop.5sec` | > 15% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Opening Mismatch | mismatch > 30% | P2 |
| Greeting Ignored | ignored > 15% | P2 |
| Early Call Drops | 5sec_drop > 20% | P1 |

---

## References

- [Conversational Opening Research](https://arxiv.org/abs/2106.07837) - Turn initiation
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - First impressions
- [AppInventiv: Voice Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Opening issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
