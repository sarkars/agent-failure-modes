# Verbosity Despite Brevity Instructions

## Issue: Agent Produces Long Responses Despite Explicit Length Constraints

**Frequency**: Very Common

**Symptoms**
- Turns exceed word count limits
- Call duration far exceeds target
- Multiple sentences when one would suffice
- Unnecessary elaboration on simple points
- Listing items when summary was requested
- Repetition of already-stated information

**Root Cause**
LLMs are trained on corpora where longer, more detailed responses often correlate with quality. Explicit length constraints in prompts compete with this training. The model "knows" the constraint but its generation patterns favor completeness over brevity. Without post-generation enforcement, verbosity wins.

**Example**
```
Scenario 1: Word count exceeded

Instruction: "Keep turns to 5-12 words"

Agent response:
"So basically this is a campus ambassador program where 
you'd be the only ambassador at your college and you'd 
help us run one online chess tournament and we'll provide 
all the creatives and support and there's also a five 
hundred rupee cash prize for the campus winner and you'd 
get a certificate and trophy and T-shirt based on your 
tier and the LinkedIn founder shoutout is really cool too."

Word count: 73 words ← 6x the maximum

---

Scenario 2: Call duration exceeded

Instruction: "Keep full call to 45-60 seconds"

Actual call: 3 minutes 45 seconds

Breakdown:
- Opening: 25 seconds (target: 10)
- Hook: 45 seconds (target: 15)
- Interest check: 30 seconds (target: 10)
- College/WhatsApp: 60 seconds (target: 20)
- Closing: 25 seconds (target: 5)

---

Scenario 3: Unnecessary listing

Caller: "What perks are there?"

Instruction: "Mention perks briefly in one sentence"

Agent response:
"So the perks are really great! First, you get an official 
certificate that you can add to your resume. Second, there's 
a trophy for top performers. Third, you get a T-shirt based 
on your tier level. Fourth, the campus winner gets five 
hundred rupees cash. And fifth, top ambassadors get a 
LinkedIn shoutout from our founder which is really valuable."

← Listed all perks individually instead of brief summary

---

Scenario 4: Repetition

Turn 3 - Agent explained perks
Turn 5 - Caller asks about interest
Turn 5 - Agent: "So just to recap, you'd be getting a 
                 certificate, trophy, T-shirt, the cash 
                 prize, and founder shoutout..."

← Re-explained already-stated information

---

Scenario 5: Over-elaboration

Simple question: "Can I share the playbook on WhatsApp?"
Expected: "Yes" or "Sure" or "Sounds good"

Agent: "Absolutely, I would really appreciate that! So 
        yes, please do share the playbook on WhatsApp 
        and I'll definitely go through it and get back 
        to you if I have any questions about the program."

← Simple "yes" became 40 words

---

Verbosity analysis (500 calls):
  Turns within word limit: 234 (47%)
  Turns 1-2x limit: 156 (31%)
  Turns 2-5x limit: 87 (17%)
  Turns >5x limit: 23 (5%)
  
  Call duration vs target:
    Within range: 38%
    1-2x target: 35%
    2-3x target: 20%
    >3x target: 7%
```

**Key Statistics**
From Voice Agent Verbosity Research (2026):
- Word limit compliance: 40-60%
- Average over-length: 2.3x stated limit
- Duration target hit: 30-50%
- User "too long" complaints: 20-35%
- Correlation: verbosity ↔ lower completion: -25%

**Verbosity Patterns**
| Pattern | Example | Impact |
|---------|---------|--------|
| Listing | Enumerated perks | 3x length |
| Elaboration | Extra context | 2x length |
| Repetition | Re-stating known info | User fatigue |
| Hedging | "So basically..." | Wasted words |
| Redundancy | "Great! That's great!" | Empty calories |

**Contributing Factors**
- LLM training favors completeness
- Length constraints low priority
- No post-generation truncation
- Complex topics encourage detail
- Politeness inflates length
- No real-time duration feedback

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Single question | "What's the program?" | < 15 words | > 30 words |
| Yes/no | "Can I WhatsApp you?" | < 5 words | > 10 words |
| Full call | Complete conversation | < 60 seconds | > 90 seconds |
| Perk summary | "What do I get?" | One sentence | Multiple sentences |
| Already explained | Re-ask about perks | "As mentioned..." | Full re-explanation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Word limit compliance | > 90% | Words per turn |
| Call duration | < 60s | Total call time |
| Repetition rate | < 5% | Same info restated |
| Listing avoidance | > 85% | Enumerated lists |

---

## Mitigation Strategies

### Prevention
1. **Post-generation truncation**: Enforce limits after generation
2. **Token budget**: Hard limit on response tokens
3. **Structured output**: Force specific sentence count
4. **Example-based prompting**: Show exact response lengths
5. **Duration feedback**: Real-time call length monitoring
6. **Brevity scoring**: Reward concise responses in training

### Implementation
```python
class BrevityEnforcer:
    """Enforce response length constraints"""
    
    def __init__(self, max_words=12, max_sentences=2):
        self.max_words = max_words
        self.max_sentences = max_sentences
    
    def check_length(self, response: str) -> dict:
        """Check if response exceeds limits"""
        words = response.split()
        sentences = response.count('.') + response.count('?') + \
                    response.count('!')
        
        return {
            "word_count": len(words),
            "sentence_count": sentences,
            "words_over": max(0, len(words) - self.max_words),
            "compliant": len(words) <= self.max_words
        }
    
    def truncate(self, response: str) -> str:
        """Truncate response to limits"""
        words = response.split()
        
        if len(words) <= self.max_words:
            return response
        
        # Find sentence boundary within limit
        truncated_words = words[:self.max_words]
        truncated = ' '.join(truncated_words)
        
        # Try to end at sentence boundary
        last_period = truncated.rfind('.')
        last_question = truncated.rfind('?')
        last_boundary = max(last_period, last_question)
        
        if last_boundary > len(truncated) * 0.6:
            return truncated[:last_boundary + 1]
        
        # Otherwise just truncate and add period
        return truncated.rstrip('.,!? ') + '.'
    
    def rewrite_concise(self, response: str, 
                        context: dict) -> str:
        """Request a more concise version"""
        # Use LLM to compress
        compression_prompt = f"""
        Rewrite this to under {self.max_words} words.
        Keep the same meaning. No filler words.
        
        Original: {response}
        
        Concise version:
        """
        # Call LLM with compression prompt
        return self.llm_compress(compression_prompt)


class CallDurationMonitor:
    """Monitor and enforce call duration"""
    
    def __init__(self, target_seconds=60, max_seconds=90):
        self.target = target_seconds
        self.max = max_seconds
        self.start_time = None
        self.warnings_given = 0
    
    def start(self):
        self.start_time = time.time()
    
    def get_elapsed(self) -> float:
        if not self.start_time:
            return 0
        return time.time() - self.start_time
    
    def get_remaining(self) -> float:
        return max(0, self.target - self.get_elapsed())
    
    def should_wrap_up(self) -> bool:
        """Check if we should start wrapping up"""
        return self.get_elapsed() > self.target * 0.8
    
    def is_over_max(self) -> bool:
        return self.get_elapsed() > self.max
    
    def get_response_budget(self, step: str) -> dict:
        """Get word budget based on remaining time"""
        remaining = self.get_remaining()
        
        # Rough estimate: 150 words per minute speech
        words_remaining = int(remaining * 2.5)  # 150/60 = 2.5
        
        step_allocations = {
            "opening": 0.15,
            "hook": 0.25,
            "interest": 0.15,
            "capture": 0.30,
            "close": 0.15
        }
        
        allocation = step_allocations.get(step, 0.2)
        step_budget = int(words_remaining * allocation)
        
        return {
            "max_words": min(step_budget, 20),
            "remaining_total": words_remaining,
            "should_be_brief": remaining < 20
        }


class ConciseResponseGenerator:
    """Generate responses that respect length constraints"""
    
    FILLER_WORDS = [
        "basically", "so", "just", "actually", "really",
        "simply", "definitely", "absolutely", "totally"
    ]
    
    REDUNDANT_PHRASES = [
        "I wanted to",
        "I just wanted to",
        "So basically",
        "What I mean is",
        "In other words"
    ]
    
    def remove_filler(self, response: str) -> str:
        """Remove filler words and phrases"""
        result = response
        
        for phrase in self.REDUNDANT_PHRASES:
            result = result.replace(phrase, "")
        
        words = result.split()
        filtered = [w for w in words 
                   if w.lower() not in self.FILLER_WORDS]
        
        return ' '.join(filtered).strip()
    
    def enforce_single_sentence_for(self, response: str,
                                     question_type: str) -> str:
        """Enforce single sentence for certain question types"""
        single_sentence_types = [
            "yes_no", "confirmation", "permission"
        ]
        
        if question_type in single_sentence_types:
            # Take only first sentence
            for end in ['.', '?', '!']:
                idx = response.find(end)
                if idx > 0:
                    return response[:idx + 1]
        
        return response
```

### Prompt Design
```yaml
instructions: |
  ## BREVITY RULES (ENFORCED)
  
  WORD LIMITS:
  - Normal turns: 5-12 words
  - Maximum any turn: 20 words
  - Full call: 45-60 seconds
  
  SENTENCE LIMITS:
  - Most turns: 1-2 sentences
  - Never more than 2 sentences per turn
  
  EXAMPLES OF CORRECT LENGTH:
  ✓ "Got it! Evening or weekend better?"  (6 words)
  ✓ "Cool, which college are you at?"  (6 words)
  ✓ "Can the team share it on WhatsApp?"  (7 words)
  
  EXAMPLES OF TOO LONG:
  ✗ "So basically what we're looking for is someone who 
     can help us run a chess tournament at their college 
     and we'll provide all the support..."  (25+ words)
  
  TECHNIQUES:
  - Skip "So" and "Basically" at start
  - Don't list perks—summarize
  - Don't repeat what you already said
  - Don't elaborate unless asked
  - Answer yes/no questions in < 5 words
  
  If a response is getting long, STOP and simplify.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `brevity.word_compliance` | < 80% |
| `brevity.call_duration` | > 90s average |
| `brevity.turn_average` | > 15 words |
| `brevity.max_turn` | > 30 words |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Verbosity High | compliance < 70% | P2 |
| Calls Too Long | avg > 120s | P2 |
| Turn Length Spike | average > 20 words | P3 |

---

## References

- [Controllable Text Generation](https://arxiv.org/abs/2201.05337) - Length control
- [LLM Verbosity Research](https://arxiv.org/abs/2303.18223) - Why LLMs over-explain
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - Brevity importance
- [Conversational Design](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Length issues
