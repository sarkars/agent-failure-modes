# Unnatural Conversational Style

## Issue: Agent Sounds Robotic, Scripted, or Inauthentically Enthusiastic

**Frequency**: Very Common

**Symptoms**
- Agent sounds like reading from a script
- Responses feel formulaic and predictable
- Over-enthusiastic tone that feels salesy or fake
- Phrases sound corporate rather than conversational
- No natural variation in delivery
- "Perfect!", "Absolutely!", "Great question!" overuse

**Root Cause**
Voice agents must balance consistency with naturalness. When agents follow prompts too literally, they produce robotic output. When they try too hard to sound friendly, they become inauthentically enthusiastic. Both trigger user distrust. Natural conversation has imperfection—brief pauses, casual phrasing, varied energy—that scripted agents lack.

**Example**
```
Scenario 1: Robotic delivery

Agent: "Hello. This is Riya from Zapp Chess. You had filled 
        the Campus Ambassador form. Do you have a minute to 
        discuss the opportunity?"

← Perfect grammar, no contractions, formal phrasing
← Sounds like reading from a teleprompter

Natural version: "Hey! This is Riya from Zapp Chess—you'd 
                  filled our ambassador form. Got a minute?"

---

Scenario 2: Over-enthusiastic/fake

Caller: "Yeah, I filled some form"
Agent: "That's AMAZING! I'm SO excited to tell you about 
        this INCREDIBLE opportunity! You're going to LOVE 
        being a Campus Ambassador!"

← Excessive enthusiasm feels manipulative
← User immediately suspects sales pitch

Natural version: "Cool! So quick context—we're looking for 
                  one ambassador per college..."

---

Scenario 3: Corporate phrasing

Agent: "I would like to take this opportunity to inform you 
        about the exciting Campus Ambassador program we are 
        currently offering."

← "Take this opportunity," "inform you," "currently offering"
← Business-speak instead of human conversation

Natural version: "So we've got this ambassador thing going—
                  basically you'd help run a chess tournament 
                  at your college."

---

Scenario 4: Predictable formulas

Every positive response: "Perfect! That's great to hear!"
Every question: "Great question! So basically..."
Every transition: "Now, moving on to..."

← Same phrases repeated feel scripted
← Users notice patterns quickly

---

Scenario 5: Missing natural imperfections

Human speech: "So like... it's basically a—you know—
              campus ambassador thing? Where you'd help 
              run a tournament at your college."

Agent speech: "This is a Campus Ambassador program where 
              you would help run a tournament at your 
              college."

← Perfect fluency signals non-human
← No hedges, restarts, or fillers

---

Naturalness analysis (1,000 calls):
  Perceived as natural: 42%
  Perceived as scripted: 35%
  Perceived as too salesy: 23%
  
  Trigger phrases (user drop correlation):
    "I'm excited to tell you": -18% completion
    "Great question!": -12% completion
    "Perfect!": -8% completion
    Formal grammar throughout: -15% completion
```

**Key Statistics**
From Voice Agent Authenticity Research (2026):
- Users detecting "bot" from style: 55-70%
- Over-enthusiasm trust reduction: 30-45%
- Script-following perception: 40-60%
- Natural style completion lift: +25-35%
- "Sounds like a real person" correlation: +40% success

**Unnatural Style Types**
| Type | Markers | Impact |
|------|---------|--------|
| Robotic | Perfect grammar, formal words | Impersonal |
| Salesy | Excessive enthusiasm, superlatives | Distrust |
| Formulaic | Repeated phrases, predictable | Obvious bot |
| Corporate | Business jargon, passive voice | Cold |
| Too perfect | No hesitation, no variation | Uncanny |

**Contributing Factors**
- Prompt emphasizes correctness over naturalness
- Training on formal text corpora
- No variation in response templates
- TTS voice sounds unnatural
- Missing conversational markers (um, like, you know)
- Energy doesn't match caller's tone

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Formality | Script delivery | Contractions, casual words | Formal grammar |
| Enthusiasm | Simple acknowledgment | Appropriate level | "AMAZING!" |
| Variation | 5 similar questions | Different phrasing | Same response |
| Filler words | Natural context | Some fillers | Perfect fluency |
| Tone match | Curt caller | Brief response | Overly warm |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Naturalness rating | > 4/5 | Human evaluation |
| "Bot" detection rate | < 20% | User survey |
| Phrase repetition | < 10% | Same phrase count |
| Formality score | Casual | Automated analysis |

---

## Mitigation Strategies

### Prevention
1. **Conversational prompting**: Instruct casual, not formal
2. **Phrase variation**: Multiple alternatives for common responses
3. **Appropriate energy**: Match caller's tone level
4. **Natural imperfections**: Allow some hedges and restarts
5. **Avoid superlatives**: Remove "amazing," "incredible," "perfect"
6. **Contraction enforcement**: "You're" not "You are"

### Implementation
```python
class NaturalnessEnforcer:
    """Make agent responses sound more natural"""
    
    FORMAL_TO_CASUAL = {
        "I would like to": "I'd like to",
        "do you have a minute": "got a minute",
        "I am": "I'm",
        "you are": "you're",
        "we are": "we're",
        "that is": "that's",
        "cannot": "can't",
        "would not": "wouldn't",
        "inform you": "tell you",
        "at this time": "right now",
        "regarding": "about",
        "prior to": "before",
        "in order to": "to",
        "utilize": "use"
    }
    
    OVERENTHUSIASTIC = [
        "amazing", "incredible", "fantastic", "wonderful",
        "absolutely", "definitely", "totally", "perfect",
        "i'm so excited", "that's great to hear",
        "great question", "excellent"
    ]
    
    PHRASE_ALTERNATIVES = {
        "perfect": ["cool", "got it", "sounds good", "nice"],
        "absolutely": ["yeah", "sure", "yep", "for sure"],
        "great question": ["so", "yeah so", "right so"],
        "that's great": ["cool", "nice", "sweet", "awesome"]
    }
    
    def naturalize(self, response: str) -> str:
        """Convert formal/salesy response to natural"""
        result = response
        
        # Apply casual replacements
        for formal, casual in self.FORMAL_TO_CASUAL.items():
            result = re.sub(
                formal, casual, result, 
                flags=re.IGNORECASE
            )
        
        # Reduce overenthusiasm
        for phrase in self.OVERENTHUSIASTIC:
            if phrase.lower() in result.lower():
                alternatives = self.PHRASE_ALTERNATIVES.get(
                    phrase.lower(), [""]
                )
                replacement = random.choice(alternatives)
                result = re.sub(
                    phrase, replacement, result,
                    flags=re.IGNORECASE
                )
        
        return result.strip()
    
    def add_natural_markers(self, response: str, 
                            probability: float = 0.2) -> str:
        """Occasionally add natural speech markers"""
        markers = ["so", "yeah", "like", "you know"]
        
        if random.random() < probability:
            # Add at sentence start occasionally
            if not response.lower().startswith(tuple(markers)):
                marker = random.choice(["So ", "Yeah so "])
                response = marker + response[0].lower() + response[1:]
        
        return response
    
    def match_caller_energy(self, response: str, 
                            caller_energy: str) -> str:
        """Adjust response energy to match caller"""
        if caller_energy == "curt":
            # Remove enthusiasm, be brief
            response = self.strip_enthusiasm(response)
            response = self.shorten(response)
        elif caller_energy == "casual":
            # Add casual markers
            response = self.add_natural_markers(response, 0.3)
        elif caller_energy == "formal":
            # Keep slightly more formal
            pass
        
        return response


class ConversationalPrompter:
    """Generate prompts that encourage natural style"""
    
    STYLE_INSTRUCTIONS = """
    STYLE RULES:
    - Sound like a friendly college senior, not a call center
    - Use contractions: "you're" not "you are"
    - Skip corporate words: "utilize," "inform," "regarding"
    - Vary your phrases—don't repeat "Perfect!" every time
    - Match the caller's energy—if they're brief, you be brief
    - It's okay to say "so," "like," "cool," "yeah"
    
    DON'T SAY:
    - "I'm so excited to..."
    - "That's amazing!"
    - "Great question!"
    - "Perfect!"
    - "Absolutely!"
    
    INSTEAD SAY:
    - "Cool, so..."
    - "Got it."
    - "Yeah, so..."
    - "Nice."
    - "Sure."
    """
```

### Prompt Design
```yaml
persona: |
  Sound like a friendly, slightly older college senior—NOT a 
  call center agent or salesperson.
  
  Your tone is:
  - Warm but not gushing
  - Casual but not sloppy
  - Confident but not pushy
  - Helpful but not desperate

style_rules: |
  USE contractions: I'm, you're, we're, that's, can't
  USE casual words: cool, got it, yeah, sure, nice
  USE natural fillers occasionally: so, like, basically
  
  AVOID:
  - "Perfect!" "Amazing!" "Absolutely!" "Definitely!"
  - "Great question!" "That's great to hear!"
  - "I would like to inform you..."
  - "At this point in time..."
  
  VARY your acknowledgments:
  - Instead of always "Perfect!": cool / got it / nice / sure
  - Instead of always "Absolutely!": yeah / sure / yep / for sure
  
  MATCH caller energy:
  - Enthusiastic caller → match warmth
  - Curt caller → be brief, direct
  - Confused caller → slow down, clarify
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `style.naturalness.rating` | < 3.5/5 |
| `style.bot_detection` | > 30% |
| `style.phrase_repetition` | > 15% |
| `style.enthusiasm_complaints` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Robotic Perception High | detection > 40% | P2 |
| Phrase Repetition | same phrase > 20% | P3 |
| Enthusiasm Complaints | rate > 15% | P2 |

---

## References

- [Conversational UX Research](https://www.beconversive.com/blog/voice-ai-challenges) - Naturalness factors
- [Voice Agent Trust](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Authenticity
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Style issues
- [Human-AI Interaction](https://arxiv.org/abs/2106.07837) - Perception of AI voice
