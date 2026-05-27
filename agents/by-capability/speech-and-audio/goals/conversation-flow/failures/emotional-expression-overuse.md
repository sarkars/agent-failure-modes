# Emotional Expression Overuse

## Issue: Agent Overuses Laughter, Exclamation Marks, and Emotional Cues

**Frequency**: Common

**Symptoms**
- Every turn opens with "haha"
- Excessive exclamation marks in TTS
- "Amazing!" and "Great!" on every response
- Elongated words overused ("niiice", "ohhh")
- Agent sounds manic or performative
- Emotional reactions without genuine trigger

**Root Cause**
Without frequency controls, LLMs tend to overuse emotional expressions. Every turn becomes "haha, that's great!" and the agent sounds manic rather than natural. Emotional expressions like laughter are powerful because they're rare—overusing them makes the agent seem fake. Frequency rules are needed to make emotions feel genuine.

**Example**
```
Scenario 1: Every turn starts with laughter

Agent: "Haha, I'd be happy to help with that!"
Caller: "I need to reschedule my appointment."
Agent: "Haha, sure thing! When works better?"
Caller: "Maybe Thursday?"
Agent: "Haha, Thursday works! Morning or afternoon?"
Caller: "...are you okay?"

← "Haha" on every turn
← No actual humor triggered it
← Sounds manic/fake

---

Scenario 2: Exclamation overload

Agent: "Great! I can help with that! Let me check! 
        Perfect! Thursday at 2 is available! 
        Wonderful! Should I book that!"

← Every sentence ends with "!"
← TTS reads with constant high energy
← Exhausting to listen to

---

Scenario 3: "Amazing" fatigue

Caller: "My name is John."
Agent: "Amazing! Great to meet you, John!"
Caller: "I'm at 123 Main Street."
Agent: "Amazing! Got it!"
Caller: "Thursday works."
Agent: "Amazing! I'll book that!"

← "Amazing" for mundane information
← Word loses all meaning
← Feels insincere

---

Scenario 4: Laughter without humor

Caller: "I need to cancel because of a family emergency."
Agent: "Haha, no problem! I'll cancel that for you!"

← Laughter is wildly inappropriate
← Serious context requires empathy
← Damaged rapport severely

---

Scenario 5: Correct emotional calibration

Caller: "I signed up because my competitor just launched 
         the exact same feature."
Agent: "Oh man, that's rough. Nothing like a competitor 
        launch to light a fire."
Caller: "Haha, exactly!"
Agent: "Well, let's get you set up fast then."
[Later in conversation]
Caller: "And then the demo just... crashed."
Agent: "Ohhh no. That's the worst timing."

← Emotional response matched context
← "Haha" only when genuinely funny
← Empathy when appropriate
← Sparing use makes it feel real

---

Emotional expression analysis (200 calls):
  
  Calls with emotional overuse: 38%
  
  Overuse patterns:
    "Haha" every turn: 22%
    Exclamation every sentence: 35%
    "Amazing/Great/Perfect" overuse: 41%
    Laughter at inappropriate times: 8%
  
  Caller perception:
    "Felt fake": 45%
    "Agent seemed manic": 28%
    "Hard to take seriously": 32%
    
  Correct calibration impact:
    Trust: +40%
    Satisfaction: +35%
    "Felt like real person": +55%
```

**Key Statistics**
From Voice AI Emotional Expression Research (2026):
- Agents that overuse emotion: 35-40%
- "Haha" on consecutive turns: feels fake to 80%
- Appropriate laughter frequency: 1 in 4-5 turns max
- Exclamation overuse fatigue: 60%
- Calibrated emotion improves trust: 40%

**Expression Frequency Guidelines**
| Expression | Max Frequency | Context Required |
|------------|---------------|------------------|
| "Haha" / laughter | 1 in 4-5 turns | Real comedic beat |
| Exclamation (!) | 1 in 3-4 sentences | Genuine excitement |
| "Amazing/Great" | 1 per conversation | Actual achievement |
| Elongation ("niiice") | 1 in 5+ turns | Strong positive moment |
| Empathy ("oh no") | When genuinely bad | Negative context only |

**Contributing Factors**
- No frequency rules in prompt
- LLM defaults to enthusiasm
- No context checking for emotion
- Same emotional response regardless of content
- Lack of negative emotion vocabulary
- Text-style excitement in voice

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Consecutive turns | 3 normal exchanges | No repeat "haha" | "Haha" each turn |
| Mundane info | "My name is John" | "Got it, John" | "Amazing!" |
| Sad context | "Family emergency" | Empathy | Laughter |
| Genuine humor | Caller jokes | One laugh | No laugh or overlaugh |
| Excitement | Real good news | Enthusiasm | Flat |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Consecutive "haha" | 0% | Transcript analysis |
| Exclamations per turn | < 1 | Punctuation count |
| Context-appropriate | > 95% | Human review |
| Emotion variety | High | Expression diversity |

---

## Mitigation Strategies

### Prevention
1. **Frequency rules**: Max 1 laugh per 4-5 turns
2. **Context checking**: Only laugh at actual humor
3. **Emotion vocabulary**: Use variety, not same word
4. **Negative emotions**: Include empathy options
5. **No consecutive repeats**: Different expression each time
6. **Energy matching**: Match caller, don't overwhelm

### Implementation
```python
class EmotionalExpressionManager:
    """Manage emotional expressions in responses"""
    
    EXPRESSIONS = {
        "laughter": ["haha", "ha", "hehe", "lol"],
        "positive_exclaim": ["amazing", "great", "perfect", "wonderful", "awesome"],
        "elongation": ["niiice", "ohhh", "yeaah", "riiight"],
        "empathy": ["oh no", "ugh", "that's rough", "ouch"]
    }
    
    FREQUENCY_LIMITS = {
        "laughter": 5,      # Max 1 in 5 turns
        "positive_exclaim": 4,
        "elongation": 5,
        "empathy": 3        # Can use more often when appropriate
    }
    
    def __init__(self):
        self.turn_count = 0
        self.last_expression_turn = {
            "laughter": -10,
            "positive_exclaim": -10,
            "elongation": -10,
            "empathy": -10
        }
    
    def can_use_expression(self, expression_type: str) -> bool:
        """Check if expression can be used"""
        limit = self.FREQUENCY_LIMITS.get(expression_type, 4)
        turns_since_last = self.turn_count - self.last_expression_turn[expression_type]
        return turns_since_last >= limit
    
    def use_expression(self, expression_type: str):
        """Record expression usage"""
        self.last_expression_turn[expression_type] = self.turn_count
    
    def increment_turn(self):
        """Increment turn counter"""
        self.turn_count += 1
    
    def validate_response(self, response: str, 
                          context: dict) -> dict:
        """Validate emotional expressions in response"""
        issues = []
        
        response_lower = response.lower()
        
        # Check for each expression type
        for exp_type, expressions in self.EXPRESSIONS.items():
            for exp in expressions:
                if exp in response_lower:
                    # Check frequency
                    if not self.can_use_expression(exp_type):
                        issues.append({
                            "type": "frequency_violation",
                            "expression": exp,
                            "message": f"'{exp}' used too recently"
                        })
                    
                    # Check context appropriateness
                    if exp_type == "laughter":
                        if not self.context_warrants_laughter(context):
                            issues.append({
                                "type": "context_mismatch",
                                "expression": exp,
                                "message": "Laughter without comedic trigger"
                            })
                    
                    if exp_type == "positive_exclaim":
                        if context.get("sentiment") == "negative":
                            issues.append({
                                "type": "context_mismatch",
                                "expression": exp,
                                "message": "Positive exclaim in negative context"
                            })
        
        # Check exclamation frequency
        exclaim_count = response.count('!')
        if exclaim_count > 1:
            issues.append({
                "type": "exclamation_overuse",
                "count": exclaim_count,
                "message": "Too many exclamation marks"
            })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def context_warrants_laughter(self, context: dict) -> bool:
        """Check if context has comedic element"""
        humor_signals = [
            "joke", "funny", "haha", "lol", "kidding",
            "hilarious", "laughing", "cracked up"
        ]
        
        last_caller_msg = context.get("last_caller_message", "").lower()
        return any(signal in last_caller_msg for signal in humor_signals)
    
    def suggest_alternative(self, expression: str, 
                           context: dict) -> str:
        """Suggest alternative to overused expression"""
        alternatives = {
            "haha": ["nice", "oh", "yeah", "right"],
            "amazing": ["got it", "cool", "nice", "sounds good"],
            "great": ["perfect", "works for me", "okay"],
            "!": [".", "—"]
        }
        
        return random.choice(alternatives.get(expression, [""]))


class ContextualEmotionSelector:
    """Select appropriate emotion for context"""
    
    def select_emotion(self, context: dict) -> dict:
        """Select appropriate emotional expression"""
        sentiment = context.get("sentiment", "neutral")
        caller_emotion = context.get("caller_emotion", "neutral")
        content_type = context.get("content_type", "informational")
        
        if sentiment == "negative" or caller_emotion in ["frustrated", "sad"]:
            return {
                "expression_type": "empathy",
                "options": ["I understand", "That's frustrating", 
                           "I'm sorry to hear that"]
            }
        
        if content_type == "joke" or context.get("humor_detected"):
            return {
                "expression_type": "laughter",
                "options": ["Ha", "Haha", "That's funny"]
            }
        
        if content_type == "achievement":
            return {
                "expression_type": "positive_exclaim",
                "options": ["Nice!", "That's great!", "Congrats!"]
            }
        
        # Default to neutral acknowledgment
        return {
            "expression_type": "neutral",
            "options": ["Got it", "Okay", "Sure", "I see"]
        }
```

### Prompt Design
```yaml
instructions: |
  ## EMOTIONAL EXPRESSION CONTROL
  
  Emotional expressions are powerful because they're RARE.
  
  LAUGHTER RULES:
  - Laugh at most once every 4-5 turns
  - Never open two consecutive turns with "haha"
  - Only laugh when there's a real comedic beat
  - If no clear joke, use "oh" or "yeah" instead
  
  POSITIVE EXPRESSIONS:
  - "Amazing" / "Great" / "Perfect": Max once per conversation
  - Reserve for actual achievements, not mundane info
  - "My name is John" → "Got it, John" (NOT "Amazing!")
  
  EXCLAMATION MARKS:
  - Maximum one per response
  - Most sentences should end with periods
  - Constant enthusiasm is exhausting
  
  ELONGATION ("niiice"):
  - Max once every 5+ turns
  - Only for genuinely exciting moments
  
  EMPATHY:
  - Use when context is genuinely negative
  - "That's rough" / "I'm sorry" / "Ugh, that's frustrating"
  - Don't laugh at someone's problems
  
  CONTEXT MATCHING:
  - Serious context (emergency, complaint) → No laughter
  - Mundane info (name, address) → Neutral acknowledgment
  - Genuine humor → One laugh okay
  - Good news → Enthusiasm appropriate
  
  SELF-CHECK:
  If your last turn started with "haha", this turn should not.
  If the caller shared bad news, do not express positive excitement.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `emotion.consecutive_laughs` | > 0% |
| `emotion.exclamations_per_response` | > 1.5 |
| `emotion.context_mismatch` | > 5% |
| `emotion.amazing_frequency` | > 2 per call |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Consecutive Laughter | 2+ turns | P2 |
| Exclamation Overuse | > 2 per response | P3 |
| Context Mismatch | Laugh at sad news | P1 |
| Expression Fatigue | Same word 3+ times | P3 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Emotional frequency
- [Voice AI Optimization](https://voiceaiwrapper.com/insights/vapi-voice-ai-optimization-performance-guide-voiceaiwrapper) - Expression calibration
- [Conversational AI Design](https://www.nngroup.com/articles/voice-ux/) - Natural expression
- [TTS Emotional Modeling](https://arxiv.org/abs/2305.07691) - Expression perception
