# Premature Call Ending

## Issue: Agent Ends Call When Caller Pauses, Interrupts, or Shows Confusion

**Frequency**: Common

**Symptoms**
- Agent ends call during brief caller silence
- Interruption interpreted as hang-up signal
- Confused fragment ("hmm", "ok") triggers goodbye
- Agent says goodbye while caller is thinking
- Call ends before natural conclusion
- No "still there?" check before ending

**Root Cause**
Agents may be overly eager to end calls, interpreting brief silences, interruptions, or confused fragments as signals to wrap up. Without proper rules for when to end vs. when to wait, agents end calls prematurely—sometimes while the caller is mid-thought or briefly distracted. This leaves callers frustrated and tasks incomplete.

**Example**
```
Scenario 1: Silence interpreted as goodbye

Agent: "Is there anything else I can help you with?"
Caller: [Thinking for 3 seconds]
Agent: "Great, thanks for calling! Have a wonderful day!"
Caller: "Wait, I actually had another question—"
[Call ended]

← 3 seconds of silence triggered goodbye
← Caller was just thinking
← Should have waited or checked in

---

Scenario 2: Interruption misread as exit

Agent: "So your appointment is confirmed for—"
Caller: [Interrupts] "Oh hold on, someone's at the door"
[Caller briefly mutes/walks away]
Agent: [Interprets silence as end] "Okay, bye!"
[Ends call]
Caller: [Returns] "Sorry, I'm back—hello?"

← Caller said "hold on" (not goodbye)
← Agent didn't wait for return
← Should have paused and waited

---

Scenario 3: Confused fragment triggers end

Agent: "Does that answer your question?"
Caller: "Hmm... ok..."
Agent: "Perfect! Thanks for calling, goodbye!"
Caller: "No wait, I'm confused about—"
[Call ended]

← "Hmm... ok..." was confusion, not agreement
← Agent interpreted as satisfaction
← Should have asked "Any questions on that?"

---

Scenario 4: Background noise as goodbye

Agent: "Can I help with anything else?"
[Caller says something to someone else off-mic]
Agent: [Hears muffled noise] "Okay, have a great day!"
[Ends call]

← Caller was talking to someone else
← Not a goodbye signal
← Should have waited for clear response

---

Scenario 5: Correct ending behavior

Agent: "Is there anything else?"
Caller: [5 seconds of silence]
Agent: "Still there?"
Caller: "Yeah, sorry—just checking something. Actually, 
         one more question..."
Agent: "Of course, go ahead!"

← Waited appropriate time
← Check-in instead of goodbye
← Caller got to finish

---

Premature ending analysis (500 calls):
  
  Calls ended prematurely: 12%
  
  Triggers for premature end:
    Brief silence (3-10s): 45%
    Confused fragment: 25%
    Interruption/distraction: 20%
    Background noise: 10%
  
  Caller behavior after premature end:
    Called back: 35%
    Gave negative feedback: 28%
    Task incomplete: 42%
  
  Correct ending signals:
    Clear "goodbye": 100% appropriate to end
    "That's all": 95% appropriate
    "I'm good": 90% appropriate
    Brief silence: Only 40% actually done
```

**Key Statistics**
From Voice AI Call Analysis (2026):
- Premature call endings: 10-15%
- Silence misinterpreted: 40-50%
- Callbacks due to premature end: 30-40%
- "Still there?" prevents early end: 70%
- Clear goodbye signals reliable: 95%+

**Ending Signal Reliability**
| Signal | Actually Done? | Correct Action |
|--------|----------------|----------------|
| "Goodbye" | 100% | End call |
| "That's all" | 95% | End call |
| "Thanks, bye" | 98% | End call |
| Brief silence | 40% | Check in first |
| "Hmm" / "Ok" | 30% | Ask clarifying question |
| Interruption | 10% | Wait for return |
| Background noise | 5% | Wait and check |

**Contributing Factors**
- Aggressive silence detection
- No distinction between silence types
- Missing "still there?" logic
- Fragment interpreted as agreement
- No wait-after-interruption rule
- Efficiency over completeness

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Brief silence | 5s pause | "Still there?" | Goodbye |
| Interruption | "Hold on" | Wait | End call |
| Confused | "Hmm... ok" | "Any questions?" | End call |
| Clear goodbye | "Thanks, bye" | End call | Continue |
| Background | Off-mic talking | Wait | End call |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Premature endings | < 5% | Call analysis |
| Check-in before end | > 80% | After silence |
| Callback rate | < 10% | Same number, 5 min |
| Task completion | > 95% | Flow completion |

---

## Mitigation Strategies

### Prevention
1. **Explicit end signals**: Only end on clear goodbye
2. **Check-in on silence**: "Still there?" after 10-15s
3. **Wait after interruption**: Caller said "hold on" = wait
4. **Fragment clarification**: "Hmm" → "Any questions?"
5. **Background detection**: Don't end on off-mic noise
6. **Confirmation before end**: "Was there anything else?"

### Implementation
```python
class CallEndingManager:
    """Manage call endings appropriately"""
    
    CLEAR_GOODBYE_SIGNALS = [
        "goodbye", "bye", "bye bye", "that's all",
        "that's it", "nothing else", "i'm good",
        "all set", "thanks bye", "thank you bye",
        "gotta go", "have to go"
    ]
    
    HOLD_SIGNALS = [
        "hold on", "one sec", "one second", "wait",
        "hang on", "just a moment", "let me check",
        "someone's at the door", "brb"
    ]
    
    CONFUSION_SIGNALS = [
        "hmm", "um", "uh", "ok...", "okay...",
        "i guess", "maybe", "not sure"
    ]
    
    SILENCE_THRESHOLD_SECONDS = 15
    CHECK_IN_THRESHOLD_SECONDS = 10
    
    def __init__(self):
        self.in_hold_mode = False
        self.last_speech_time = time.time()
    
    def should_end_call(self, last_utterance: str,
                        silence_seconds: float) -> dict:
        """Determine if call should end"""
        utterance_lower = last_utterance.lower().strip()
        
        # Clear goodbye - end call
        if any(signal in utterance_lower 
               for signal in self.CLEAR_GOODBYE_SIGNALS):
            return {
                "should_end": True,
                "confidence": "high",
                "action": "end_warmly"
            }
        
        # Hold signal - wait
        if any(signal in utterance_lower 
               for signal in self.HOLD_SIGNALS):
            self.in_hold_mode = True
            return {
                "should_end": False,
                "action": "wait_silently",
                "max_wait": 60  # Wait up to 60 seconds
            }
        
        # Confusion signal - clarify
        if any(signal in utterance_lower 
               for signal in self.CONFUSION_SIGNALS):
            return {
                "should_end": False,
                "action": "clarify",
                "response": "Any questions on that?"
            }
        
        # Silence handling
        if silence_seconds > self.CHECK_IN_THRESHOLD_SECONDS:
            if silence_seconds > self.SILENCE_THRESHOLD_SECONDS:
                return {
                    "should_end": False,
                    "action": "check_in",
                    "response": "Still there?"
                }
            return {
                "should_end": False,
                "action": "wait"
            }
        
        return {"should_end": False, "action": "continue"}
    
    def handle_return_from_hold(self, utterance: str) -> dict:
        """Handle caller returning from hold"""
        if self.in_hold_mode:
            self.in_hold_mode = False
            return {
                "action": "welcome_back",
                "response": "Welcome back! Where were we?"
            }
        return {"action": "continue"}
    
    def get_ending_response(self, ending_type: str) -> str:
        """Get appropriate ending response"""
        endings = {
            "warm": "Thanks so much for calling! Have a great day!",
            "after_task": "Glad I could help! Take care!",
            "after_silence": "Okay, if you need anything else, "
                           "just give us a call. Bye!",
            "after_hold_timeout": "Looks like you might have stepped away. "
                                 "Feel free to call back anytime!"
        }
        return endings.get(ending_type, endings["warm"])


class SilenceClassifier:
    """Classify type of silence"""
    
    def classify(self, 
                 silence_duration: float,
                 last_utterance: str,
                 conversation_context: dict) -> str:
        """Classify the silence type"""
        
        # After question, short silence = thinking
        if conversation_context.get("last_turn_was_question"):
            if silence_duration < 8:
                return "thinking"
        
        # After "hold on", any silence = waiting
        if any(hold in last_utterance.lower() 
               for hold in ["hold on", "one sec", "wait"]):
            return "caller_away"
        
        # After completing a task, silence may be done
        if conversation_context.get("task_completed"):
            if silence_duration > 10:
                return "possibly_done"
        
        # Long silence without context
        if silence_duration > 15:
            return "needs_check_in"
        
        return "normal_pause"
    
    def get_action(self, silence_type: str) -> dict:
        """Get action for silence type"""
        actions = {
            "thinking": {"action": "wait", "max_wait": 10},
            "caller_away": {"action": "wait", "max_wait": 60},
            "possibly_done": {"action": "check_anything_else"},
            "needs_check_in": {"action": "check_still_there"},
            "normal_pause": {"action": "wait", "max_wait": 5}
        }
        return actions.get(silence_type, {"action": "wait"})
```

### Prompt Design
```yaml
instructions: |
  ## WHEN TO END THE CALL
  
  END the call when:
  - Caller gives clear goodbye ("bye", "thanks, bye", "that's all")
  - Flow is complete AND you've asked "anything else?" AND they say no
  - Caller explicitly says they need to go
  
  DO NOT end the call when:
  - Caller goes quiet (they might be thinking)
  - Caller says "hold on" or "one sec" (wait for them)
  - Caller makes confused sounds ("hmm", "ok...") - clarify instead
  - You hear background noise or off-mic talking
  - Caller interrupts you mid-sentence
  
  SILENCE HANDLING:
  - 5-10 seconds: Wait patiently (they're thinking)
  - 10-15 seconds: Check in: "Still there?"
  - 15+ seconds with no response: "Looks like you might have 
    stepped away. Feel free to call back anytime!"
  
  CONFUSION HANDLING:
  - "Hmm..." → "Any questions on that?"
  - "Ok..." (uncertain) → "Does that make sense?"
  - "I guess..." → "Want me to explain that differently?"
  
  INTERRUPTION HANDLING:
  - If caller says "hold on" or "one sec": Wait silently
  - When they return: "Welcome back! Where were we?"
  - Don't end the call just because they stepped away
  
  CLOSING SEQUENCE:
  1. Complete the task
  2. "Is there anything else I can help with?"
  3. Wait for clear "no" or "that's all"
  4. "Thanks so much for calling! Have a great day!"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `ending.premature_rate` | > 10% |
| `ending.no_check_in` | > 20% |
| `ending.callback_rate` | > 15% |
| `ending.incomplete_task` | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Premature End | > 15% | P2 |
| No Check-in | > 30% | P3 |
| High Callback | > 20% | P2 |
| Incomplete Tasks | > 10% | P1 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Call endings
- [Voice AI Speech Config](https://docs.vapi.ai/customization/speech-configuration) - Silence handling
- [Turn-Taking Research](https://www.isca-speech.org/archive/interspeech_2023/) - Pause interpretation
- [Call Flow Design](https://www.nngroup.com/articles/voice-ux/) - Closing patterns
