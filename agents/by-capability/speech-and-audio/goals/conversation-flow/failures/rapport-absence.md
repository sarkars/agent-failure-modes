# Rapport Absence

## Issue: Agent Fails to React to Caller's Personal Comments or Emotional Cues

**Frequency**: Common

**Symptoms**
- Caller shares personal detail, agent ignores it
- No acknowledgment of "long Monday" or "tough day"
- Agent charges ahead with script after emotional comment
- Feels like talking to a form, not a person
- Caller engagement drops after ignored comment
- Conversation feels transactional and cold

**Root Cause**
The difference between a voice agent that feels like a form and one that feels like a conversation is rapport - reacting to what the caller says like a real person would. When callers share personal comments ("sorry, long Monday") or emotional cues, agents often ignore them and continue with the script. This destroys the human-like feel and reduces caller engagement.

**Example**
```
Scenario 1: Personal comment ignored

Agent: "So are you interested in the campus ambassador role?"
Caller: "Yeah, I think so. Sorry, it's been a long Monday."
Agent: "Great! Let me get your college name."

← Caller shared personal detail ("long Monday")
← Agent completely ignored it
← Missed opportunity: "Totally get it, Mondays are rough!"
← Conversation feels robotic

---

Scenario 2: Emotional cue ignored

Agent: "I see your order was delayed."
Caller: "Yeah, I've been waiting for three weeks and I was 
         really counting on it for my daughter's birthday."
Agent: "Let me check the tracking status."

← Caller expressed emotional context (birthday)
← Agent went straight to process
← Should: "Oh no, I'm so sorry! That's really frustrating, 
          especially with the birthday. Let me see what I can do."

---

Scenario 3: Enthusiasm not matched

Caller: "I just got accepted to MIT! And I saw your chess 
         tournament program and thought it would be amazing!"
Agent: "I see. What's your phone number?"

← Caller shared exciting news (MIT acceptance)
← Agent showed zero enthusiasm
← Should: "Wow, congrats on MIT! That's awesome! You'd be 
          perfect for this program. Let me get your details."

---

Scenario 4: Anxiety not acknowledged

Caller: "I'm a bit nervous—I've never done anything like this before."
Agent: "So you're interested in hosting a tournament?"

← Caller expressed vulnerability (nervous)
← Agent ignored emotional cue
← Should: "No worries at all! It's totally normal. We'll 
          walk you through everything. It's actually pretty fun!"

---

Scenario 5: Correct rapport handling

Caller: "Hi! Sorry, I'm at a coffee shop and it's a bit noisy."
Agent: "No worries! Coffee shops are the best. Can you hear 
        me okay?"
Caller: "Yeah, perfect!"
Agent: "Great! So you filled out the ambassador form—
        excited about chess?"
Caller: "Super excited! I've been playing since I was 8."
Agent: "Since 8? That's impressive! You'll definitely 
        connect with other players. Quick question..."

← Acknowledged environment (coffee shop)
← Matched enthusiasm ("Super excited")
← Built on personal detail (playing since 8)
← Conversation feels natural

---

Rapport pattern analysis:
  
  Calls with personal comments: 35%
  
  Agent response to personal comments:
    Acknowledged and engaged: 28%
    Brief acknowledgment: 15%
    Ignored completely: 57%
  
  Impact on call outcome:
    Rapport engaged: 78% positive outcome
    Rapport ignored: 52% positive outcome
    
  Caller satisfaction:
    With rapport: 4.2/5 average
    Without rapport: 3.1/5 average
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Callers share personal details: 35%
- Agents ignore personal cues: 55-60%
- Rapport improves conversion: 30-50%
- Satisfaction boost from rapport: +35%
- Rapport builds in 1-2 exchanges: 80%

**Rapport Opportunities**
| Caller Cue | Expected Response | Wrong Response |
|-----------|------------------|----------------|
| "Long Monday" | "Totally get it, Mondays are rough!" | [Continue script] |
| Exciting news | "Wow, that's great!" | "I see." |
| Frustration | "I'm sorry, that sounds frustrating" | "Let me check..." |
| Nervousness | "No worries, totally normal!" | [Ignore] |
| Environmental note | "Coffee shop? Love it!" | [Ignore] |
| Personal detail | Brief follow-up question | [Ignore] |

**Contributing Factors**
- Script-focused prompts ignore rapport
- No emotional cue detection
- Efficiency prioritized over connection
- Missing rapport vocabulary
- No personal detail tracking
- Agents trained on text patterns

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Long Monday | "It's been a long day" | Acknowledgment | Script continues |
| Excitement | "I'm so excited!" | Match energy | Flat response |
| Frustration | "This is frustrating" | Empathy first | Process first |
| Nervousness | "I'm a bit nervous" | Reassurance | Ignore |
| Personal fact | "I've played chess 10 years" | "Impressive!" | "I see" |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Rapport acknowledgment | > 80% | Human review |
| Emotional matching | > 75% | Sentiment analysis |
| Personal detail follow-up | > 60% | Transcript analysis |
| Caller satisfaction | > 4.0/5 | Post-call survey |

---

## Mitigation Strategies

### Prevention
1. **Rapport instruction**: Explicitly teach rapport in prompt
2. **Emotional cue detection**: Identify cues before responding
3. **Brief acknowledgment**: 1-2 sentences max, then continue
4. **Energy matching**: Match caller's emotional tone
5. **Follow-up questions**: Brief personal engagement
6. **Balance**: Rapport → Business, not Rapport only

### Implementation
```python
class RapportHandler:
    """Handle rapport-building opportunities"""
    
    PERSONAL_CUE_PATTERNS = {
        "time_of_day": [
            "long monday", "long day", "long week", 
            "early morning", "late night", "busy day"
        ],
        "excitement": [
            "excited", "can't wait", "so happy", 
            "thrilled", "amazing", "awesome"
        ],
        "frustration": [
            "frustrated", "annoying", "waited", 
            "three weeks", "multiple times", "still waiting"
        ],
        "nervousness": [
            "nervous", "first time", "never done", 
            "not sure if", "worried", "anxious"
        ],
        "personal_achievement": [
            "got accepted", "graduated", "promoted",
            "just started", "won", "achieved"
        ],
        "environment": [
            "coffee shop", "at work", "on the train",
            "bit noisy", "driving", "walking"
        ]
    }
    
    RAPPORT_RESPONSES = {
        "time_of_day": [
            "Totally get it, {day}s can be rough!",
            "I hear you! Hope the rest of your day gets better.",
            "Ha, I feel that!"
        ],
        "excitement": [
            "That's awesome!",
            "Love the energy!",
            "Same here, this is gonna be great!"
        ],
        "frustration": [
            "I'm really sorry to hear that. Let me help.",
            "That sounds frustrating. Let's sort this out.",
            "I totally understand. Let me see what I can do."
        ],
        "nervousness": [
            "No worries at all! It's totally normal.",
            "You've got this! We'll walk through it together.",
            "Don't worry, it's easier than it sounds!"
        ],
        "personal_achievement": [
            "Wow, congratulations! That's amazing!",
            "That's impressive!",
            "Nice! You should be proud of that."
        ],
        "environment": [
            "Coffee shop? Nice! Can you hear me okay?",
            "No problem! Let me know if I need to repeat anything.",
            "All good! Just let me know if you need a moment."
        ]
    }
    
    def detect_rapport_cue(self, transcript: str) -> dict:
        """Detect rapport-building opportunity"""
        transcript_lower = transcript.lower()
        
        for category, patterns in self.PERSONAL_CUE_PATTERNS.items():
            for pattern in patterns:
                if pattern in transcript_lower:
                    return {
                        "detected": True,
                        "category": category,
                        "pattern": pattern,
                        "response": self.get_response(category, pattern)
                    }
        
        return {"detected": False}
    
    def get_response(self, category: str, pattern: str) -> str:
        """Get appropriate rapport response"""
        responses = self.RAPPORT_RESPONSES.get(category, [])
        response = random.choice(responses) if responses else ""
        
        # Handle template substitutions
        if "{day}" in response:
            day = pattern.split()[1] if "long" in pattern else "those"
            response = response.replace("{day}", day.capitalize())
        
        return response
    
    def build_rapport_flow(self, cue: dict, next_question: str) -> str:
        """Build response with rapport + continuation"""
        if not cue["detected"]:
            return next_question
        
        # Rapport acknowledgment + transition + business
        rapport = cue["response"]
        
        # Short transition
        transitions = ["Anyway, ", "So, ", "Quick question - "]
        transition = random.choice(transitions)
        
        return f"{rapport} {transition}{next_question}"


class EmotionalMatcher:
    """Match caller's emotional energy"""
    
    ENERGY_LEVELS = {
        "high": {
            "indicators": ["excited", "amazing", "awesome", "love", 
                          "can't wait", "super", "really want"],
            "response_style": "enthusiastic",
            "modifiers": ["Awesome!", "Love it!", "That's great!"]
        },
        "low": {
            "indicators": ["frustrated", "tired", "long day", "waiting",
                          "problem", "issue", "worried"],
            "response_style": "empathetic",
            "modifiers": ["I understand.", "I'm sorry.", "I hear you."]
        },
        "neutral": {
            "indicators": [],
            "response_style": "professional",
            "modifiers": ["Got it.", "Sure.", "Okay."]
        }
    }
    
    def detect_energy(self, transcript: str) -> str:
        """Detect caller's energy level"""
        transcript_lower = transcript.lower()
        
        for level, config in self.ENERGY_LEVELS.items():
            if any(ind in transcript_lower for ind in config["indicators"]):
                return level
        
        return "neutral"
    
    def get_matching_modifier(self, energy: str) -> str:
        """Get modifier that matches caller energy"""
        config = self.ENERGY_LEVELS.get(energy, self.ENERGY_LEVELS["neutral"])
        return random.choice(config["modifiers"])
    
    def adapt_response(self, base_response: str, 
                       caller_energy: str) -> str:
        """Adapt response to match caller energy"""
        modifier = self.get_matching_modifier(caller_energy)
        
        if caller_energy == "high":
            # Add enthusiasm
            return f"{modifier} {base_response}"
        elif caller_energy == "low":
            # Lead with empathy
            return f"{modifier} {base_response}"
        else:
            return base_response
```

### Prompt Design
```yaml
instructions: |
  ## RAPPORT BUILDING
  
  The difference between feeling like a form and a conversation is RAPPORT.
  
  When the caller shares something personal:
  1. ACKNOWLEDGE it briefly (1-2 sentences max)
  2. Then continue with your question
  
  EXAMPLES:
  
  Caller: "Sorry, it's been a long Monday."
  You: "Totally get it, Mondays can be rough! So anyway..."
  
  Caller: "I just got accepted to MIT!"
  You: "Wow, congrats! That's awesome! You'd be perfect for this."
  
  Caller: "I've been waiting three weeks and I'm frustrated."
  You: "I'm really sorry to hear that. Let me help sort this out."
  
  Caller: "I'm a bit nervous, never done this before."
  You: "No worries at all! It's totally normal. We'll walk through it."
  
  MATCH their energy:
  - Excited caller → Be enthusiastic
  - Frustrated caller → Be empathetic first
  - Nervous caller → Be reassuring
  
  DON'T:
  - Ignore personal comments and charge ahead
  - Spend too long on rapport (1-2 sentences max)
  - Match frustration with frustration
  - Sound robotic when they're emotional
  
  KEEP IT BRIEF: Rapport → Then business
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `rapport.acknowledgment_rate` | < 60% |
| `rapport.energy_mismatch` | > 25% |
| `rapport.cue_ignored` | > 40% |
| `caller.satisfaction` | < 3.8/5 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Low Rapport | Acknowledgment < 50% | P2 |
| Energy Mismatch | Flat response to excitement | P3 |
| Empathy Miss | Process before emotion | P2 |
| Satisfaction Drop | < 3.5/5 with rapport opps | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Rapport building
- [VapiPro: Tone and Personality](https://vapipro.com/mastering-tone-and-personality-in-voice-ai-lessons-from-vapis-prompting-guide/) - Emotional matching
- [Voice AI Optimization](https://voiceaiwrapper.com/insights/vapi-voice-ai-optimization-performance-guide-voiceaiwrapper) - Engagement techniques
- [Conversational Design](https://www.nngroup.com/articles/voice-ux/) - Human-like interaction
