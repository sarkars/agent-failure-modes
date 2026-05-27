# Disfluency Calibration Failures

## Issue: Agent's Filler Words and Speech Disfluencies Don't Match Persona or Context

**Frequency**: Common

**Symptoms**
- Professional agent sounds too casual ("um, like, you know")
- Casual agent sounds robotic (no fillers at all)
- Fillers feel forced or poorly timed
- Caller senses "uncanny valley" but can't articulate why
- Disfluency increases for time-pressed callers (annoying)
- Clinical/serious contexts have inappropriate casualness

**Root Cause**
LLMs default to clean, polished output. In text, this is desirable. In voice, it creates the "uncanny valley" - real humans stutter, restart sentences, and drop filler words. However, disfluency injection must match the agent's persona and adapt to caller context. A medical triage agent shouldn't say "um, like, so..." while a casual sales rep can stutter freely.

**Example**
```
Scenario 1: Professional agent too casual

[Bank fraud prevention agent - should be serious]
Agent: "Um, so like, I'm seeing some, uh, suspicious activity 
        on your account? You know, we need to, like, verify 
        some stuff."
Caller: [Concerned this isn't a real bank]

← Fraud agent needs authority, not casual fillers
← "um" and "like" undermine seriousness
← Caller may hang up thinking it's a scam

CORRECT approach:
Agent: "I'm seeing some unusual activity on your account. 
        Let me verify a few details to secure it."

---

Scenario 2: Casual agent too robotic

[Friendly sales rep for college students]
Agent: "Hello. I am calling about the campus ambassador program.
        Are you interested in chess tournaments?"
Caller: [Feels like talking to a machine]

← Zero disfluency = robotic
← Doesn't match friendly college rep persona
← Caller disengages

CORRECT approach:
Agent: "Hey! So, I'm calling about the campus ambassador 
        thing—you filled the form, right? Into chess?"

---

Scenario 3: Disfluency not calibrated to caller

[Same agent, different callers]

Chatty caller (relaxed pace):
Agent: "So, um, yeah, the ambassador role is pretty cool, 
        like, you'd be organizing tournaments and stuff..."
Caller: "Oh awesome, tell me more!"
← Disfluency matches chatty caller ✓

Time-pressed caller (rushed):
Agent: "So, um, yeah, the ambassador role is pretty cool, 
        like, you'd be organizing—"
Caller: "Can you just tell me the main points quickly?"
Agent: "Um, sure, so like, basically..."
Caller: [Frustrated with filler words]

← Same disfluency doesn't work for rushed caller
← Should adapt: "Sure! You organize tournaments, get 
   certificates, and network with players."

---

Scenario 4: Medical context with wrong calibration

[Healthcare appointment reminder]
Agent: "Hey! So like, um, you've got that colonoscopy 
        thing tomorrow? Don't forget to, you know, not 
        eat anything after midnight, haha."
Patient: [Concerned about professionalism of clinic]

← Medical context needs dignity
← "haha" completely inappropriate
← Patient may question quality of care

CORRECT approach:
Agent: "This is a reminder about your procedure tomorrow. 
        Please remember not to eat or drink after midnight. 
        Do you have any questions?"

---

Scenario 5: Forced fillers feel unnatural

[Agent with programmatic filler injection]
Agent: "I'll um check that for um you. Let me um look up 
        your um account."

← Too many fillers
← Robotic insertion pattern
← Worse than no fillers

---

Disfluency calibration analysis:
  
  Persona-disfluency mismatch rate: 35%
  Context-adaptation failure: 42%
  
  By persona type:
    Casual sales: Should have fillers, often too robotic
    Professional service: Should be clean, often too casual
    Medical/legal: Should be minimal, often inappropriate
    Tech support: Should be moderate, often inconsistent
  
  Caller satisfaction impact:
    Well-calibrated: 85% satisfaction
    Over-casual for context: 62% satisfaction
    Too robotic: 71% satisfaction
    Forced/unnatural: 58% satisfaction
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Clean LLM output feels robotic: 75% of callers
- Uncanny valley from mismatch: 45%
- Proper disfluency improves trust: 25%
- Over-disfluency annoys: 40%
- Context-adapted disfluency: +30% satisfaction

**Disfluency by Context**
| Persona/Context | Appropriate Disfluency | Inappropriate |
|-----------------|----------------------|---------------|
| Casual sales | "um", "like", "so" | Clean/formal |
| Medical triage | "let me see", "one moment" | "um", "like" |
| Bank/financial | Minimal, professional | Casual fillers |
| Tech support | Moderate, thinking words | Heavy slang |
| Legal services | Minimal, precise | Any casual filler |
| College outreach | Natural, friendly | Robotic |

**Contributing Factors**
- Same disfluency for all personas
- No adaptation to caller energy
- Forced filler injection patterns
- No context-aware calibration
- LLM default cleanliness
- Ignoring caller pace signals

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Persona match | Professional persona | Minimal fillers | "um, like" present |
| Casual match | Casual persona | Natural fillers | Robotic/clean |
| Context adapt | Medical scenario | Dignified | Casual fillers |
| Caller adapt | Rushed caller | Reduce fillers | Same filler rate |
| Natural timing | Any response | Varied placement | Robotic pattern |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Persona-filler alignment | > 85% | Human review |
| Context appropriateness | > 90% | Scenario audit |
| Natural timing variance | High | Filler position analysis |
| Caller satisfaction | > 80% | Post-call survey |

---

## Mitigation Strategies

### Prevention
1. **Persona-specific disfluency**: Define filler vocabulary per persona
2. **Context awareness**: Adapt for serious vs. casual contexts
3. **Caller energy matching**: Detect and match caller pace
4. **Natural randomization**: Vary filler placement
5. **Professional context detection**: Reduce fillers for medical/legal/financial
6. **Human evaluation**: Regular calibration checks

### Implementation
```python
class DisfluencyCalibrator:
    """Calibrate disfluency to persona and context"""
    
    PERSONA_PROFILES = {
        "casual_sales": {
            "fillers": ["um", "like", "so", "you know", "right"],
            "frequency": "high",  # 2-3 per response
            "style": "natural_casual"
        },
        "professional_service": {
            "fillers": ["let me see", "one moment", "let me check"],
            "frequency": "low",  # 0-1 per response
            "style": "thinking_professional"
        },
        "medical_clinical": {
            "fillers": ["let me confirm", "one moment"],
            "frequency": "minimal",  # Only when needed
            "style": "dignified"
        },
        "financial_banking": {
            "fillers": ["let me verify", "one moment"],
            "frequency": "minimal",
            "style": "authoritative"
        },
        "friendly_college": {
            "fillers": ["so", "yeah", "cool", "right"],
            "frequency": "moderate",
            "style": "youthful_casual"
        }
    }
    
    CONTEXT_OVERRIDES = {
        "fraud_alert": {"frequency": "minimal", "style": "authoritative"},
        "medical_serious": {"frequency": "minimal", "style": "dignified"},
        "legal_matter": {"frequency": "none", "style": "precise"},
        "appointment_reminder": {"frequency": "low", "style": "clear"},
        "casual_inquiry": {"frequency": "normal", "style": "persona_default"}
    }
    
    def __init__(self, base_persona: str):
        self.persona = self.PERSONA_PROFILES.get(
            base_persona, 
            self.PERSONA_PROFILES["professional_service"]
        )
        self.caller_energy = "normal"
    
    def detect_caller_energy(self, caller_transcript: str, 
                             speech_rate: float) -> str:
        """Detect caller energy level"""
        rushed_signals = [
            "quickly", "hurry", "brief", "just tell me",
            "short on time", "in a rush"
        ]
        
        relaxed_signals = [
            "no rush", "take your time", "curious",
            "tell me more", "interesting"
        ]
        
        text_lower = caller_transcript.lower()
        
        # Check speech rate (words per minute)
        if speech_rate > 180:  # Fast speaker
            return "rushed"
        elif speech_rate < 120:  # Slow speaker
            return "relaxed"
        
        # Check verbal signals
        if any(signal in text_lower for signal in rushed_signals):
            return "rushed"
        if any(signal in text_lower for signal in relaxed_signals):
            return "relaxed"
        
        return "normal"
    
    def get_disfluency_config(self, context: str = None) -> dict:
        """Get disfluency config for current context"""
        config = self.persona.copy()
        
        # Apply context overrides
        if context and context in self.CONTEXT_OVERRIDES:
            override = self.CONTEXT_OVERRIDES[context]
            config.update(override)
        
        # Adapt to caller energy
        if self.caller_energy == "rushed":
            # Reduce fillers for time-pressed callers
            if config["frequency"] == "high":
                config["frequency"] = "moderate"
            elif config["frequency"] == "moderate":
                config["frequency"] = "low"
            elif config["frequency"] == "low":
                config["frequency"] = "minimal"
        
        return config
    
    def inject_disfluency(self, response: str, config: dict) -> str:
        """Inject appropriate disfluency into response"""
        if config["frequency"] == "none":
            return response
        
        fillers = config["fillers"]
        frequency = config["frequency"]
        
        # Determine number of fillers
        filler_count = {
            "minimal": random.choice([0, 0, 1]),
            "low": random.choice([0, 1, 1]),
            "moderate": random.choice([1, 1, 2]),
            "high": random.choice([1, 2, 3])
        }.get(frequency, 0)
        
        if filler_count == 0:
            return response
        
        # Natural insertion points
        sentences = response.split(". ")
        
        for _ in range(min(filler_count, len(sentences))):
            idx = random.randint(0, len(sentences) - 1)
            filler = random.choice(fillers)
            
            # Vary insertion position
            position = random.choice(["start", "mid"])
            
            if position == "start" and not sentences[idx].startswith(filler):
                sentences[idx] = f"{filler.capitalize()}, {sentences[idx].lower()}"
            elif position == "mid":
                words = sentences[idx].split()
                if len(words) > 3:
                    insert_pos = random.randint(2, len(words) - 1)
                    words.insert(insert_pos, f", {filler},")
                    sentences[idx] = " ".join(words)
        
        return ". ".join(sentences)


class DisfluencyValidator:
    """Validate disfluency appropriateness"""
    
    INAPPROPRIATE_COMBINATIONS = {
        "medical": ["um", "like", "you know", "haha", "lol"],
        "legal": ["um", "like", "you know", "basically", "stuff"],
        "financial": ["like", "you know", "stuff", "thing"],
        "fraud": ["um", "like", "you know", "maybe", "I think"]
    }
    
    def validate(self, response: str, context: str) -> dict:
        """Validate response disfluency for context"""
        inappropriate = self.INAPPROPRIATE_COMBINATIONS.get(context, [])
        
        found = []
        for filler in inappropriate:
            if filler.lower() in response.lower():
                found.append(filler)
        
        return {
            "appropriate": len(found) == 0,
            "inappropriate_fillers": found,
            "context": context,
            "recommendation": self.get_recommendation(found, context)
        }
    
    def get_recommendation(self, found: list, context: str) -> str:
        if not found:
            return "Disfluency appropriate for context"
        
        return (f"Remove casual fillers ({', '.join(found)}) for "
                f"{context} context. Use 'let me confirm' or "
                f"'one moment' instead.")
```

### Prompt Design
```yaml
instructions: |
  ## DISFLUENCY CALIBRATION
  
  Your speaking style must match your PERSONA and CONTEXT:
  
  PERSONA: [Friendly college outreach rep]
  Default style: Natural, youthful, some fillers okay
  Fillers allowed: "so", "yeah", "right", "cool"
  Fillers to avoid: Medical/legal precision language
  
  CONTEXT OVERRIDES:
  - If discussing sensitive topics → reduce casual fillers
  - If caller seems rushed → be more direct, fewer fillers
  - If caller is relaxed → match their energy
  
  CALLER ADAPTATION:
  - Rushed caller: "Sure! Here are the main points..."
  - Relaxed caller: "So yeah, basically the role is..."
  
  NEVER:
  - Sound robotic (some natural hesitation is good)
  - Use heavy fillers in serious contexts
  - Keep same energy regardless of caller
  - Force fillers into every sentence
  
  NATURAL VARIATION:
  - Don't put fillers in predictable positions
  - Vary which fillers you use
  - Match filler density to conversation energy
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `disfluency.persona_mismatch` | > 15% |
| `disfluency.context_inappropriate` | > 10% |
| `disfluency.uncanny_valley_reports` | > 5% |
| `disfluency.too_casual_complaints` | > 8% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Persona Mismatch | > 20% | P2 |
| Inappropriate Context | Medical + casual | P1 |
| Robotic Reports | > 10% | P3 |
| Uncanny Valley | > 8% | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Disfluency calibration
- [Voice AI Optimization](https://voiceaiwrapper.com/insights/vapi-voice-ai-optimization-performance-guide-voiceaiwrapper) - Persona matching
- [Uncanny Valley Research](https://www.frontiersin.org/articles/voice-agent-perception) - Why clean output fails
- [VapiPro: Tone and Personality](https://vapipro.com/mastering-tone-and-personality-in-voice-ai-lessons-from-vapis-prompting-guide/) - Style calibration
