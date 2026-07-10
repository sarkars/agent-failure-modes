# Override Signal Failures

## Issue: Agent Fails to Detect or Respond to Conversation-Stopping Signals

**Frequency**: Common

**Symptoms**
- Agent continues pitching after caller says "busy"
- "Stop" or "not now" doesn't halt the conversation
- Agent asks questions after caller requested callback
- Urgent signals (meeting, driving) ignored
- Agent completes full script despite early termination request

**Root Cause**
Voice agents often have multi-step flows designed for complete conversations. When callers signal they need to stop immediately ("I'm busy", "in a meeting", "call me later"), the agent should override its normal flow and exit quickly. Without explicit override handling, the agent continues its script, frustrating callers and damaging brand perception.

**Example**
```
Scenario 1: Busy signal ignored

Agent: "Hi, this is Riya from the chess app—"
Caller: "Hey, I'm in a meeting right now"
Agent: "Oh great! So we're running this campus ambassador 
        program where you'd help us run tournaments—"
Caller: "I said I'm in a meeting!"
Agent: "Right, so basically the perks include..."

← Agent ignored "in a meeting" twice, continued pitch

---

Scenario 2: Partial override

Caller: "Not now, call me later"
Agent: "No problem! Just quickly—are you interested 
        in the campus ambassador role?"

← Agent acknowledged but still asked a question

---

Scenario 3: Driving/safety signal

Caller: "Sorry, I'm driving"
Agent: "This will only take a minute! So—"

← Safety-critical signal ignored

---

Scenario 4: Stop command buried

Caller: "Yeah, I filled that form but I'm busy 
        right now, can you call back?"
Agent: "Great that you filled the form! So this 
        program is about..."

← "Busy" and "call back" buried in response, missed

---

Scenario 5: Late-conversation override

[After 3 turns of conversation]
Caller: "Actually, I have to go"
Agent: "Sure, just one more question—can I confirm 
        your WhatsApp for the playbook?"

← Added question after "have to go"

---

Override detection analysis (1,000 calls):
  Explicit busy/stop signals: 234
  Correctly detected: 168 (72%)
  Ignored first time: 45 (19%)
  Ignored repeatedly: 21 (9%)
  
  Override response quality:
    Clean exit (no extra questions): 58%
    Partial (acknowledged but continued): 27%
    Failed (ignored entirely): 15%
```

**Key Statistics**
From Voice Agent Override Research (2026):
- Override signal detection: 70-85%
- First-signal response rate: 60-75%
- Clean exit rate (no trailing questions): 50-70%
- Repeated override needed: 15-25%
- User frustration from ignored override: 45%

**Override Signal Types**
| Signal | Examples | Priority |
|--------|----------|----------|
| Immediate | "Stop", "Hang up" | Critical |
| Safety | "Driving", "Emergency" | Critical |
| Temporal | "Busy", "In meeting", "Not now" | High |
| Deferral | "Call later", "Another time" | High |
| Implicit | "I have to go", "Need to run" | Medium |

**Contributing Factors**
- No interrupt priority in conversation design
- Override logic in LLM prompt not enforced
- Multi-turn context buries override signals
- Flow completion bias in training
- No real-time signal detection layer
- Override keywords not in ASR key terms

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| First-turn busy | "I'm busy right now" | Ask callback time only | Any pitch content |
| Mid-turn stop | "Actually I need to go" | Immediate close | Additional question |
| Safety signal | "I'm driving" | Immediate close | Any continuation |
| Embedded signal | "Yeah but I'm in a meeting" | Detect busy | Continue pitch |
| Call-back request | "Call me later" | Confirm time, close | Pitch before confirming |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Override detection | > 95% | Signal present vs. detected |
| First-signal response | > 90% | Response on first override |
| Clean exit rate | > 85% | No questions after override |
| Repeat override rate | < 5% | Caller repeats stop signal |

---

## Mitigation Strategies

### Prevention
1. **Real-time signal detection**: Check every turn for override signals
2. **Priority interrupts**: Override signals skip normal flow entirely
3. **No trailing questions**: After override, only ask callback preference
4. **Safety-first**: Driving/emergency signals trigger immediate exit
5. **ASR key terms**: Add override words to speech recognition hints
6. **Flow state machine**: Explicit "override" state that bypasses steps

### Override Handler
```python
class OverrideHandler:
    """Detect and handle conversation override signals"""
    
    IMMEDIATE_SIGNALS = [
        "stop", "hang up", "disconnect", "end call",
        "ruk", "band karo", "bye"
    ]
    
    SAFETY_SIGNALS = [
        "driving", "drive", "car", "road",
        "emergency", "hospital", "urgent"
    ]
    
    TEMPORAL_SIGNALS = [
        "busy", "meeting", "class", "lecture",
        "not now", "can't talk", "call later",
        "call back", "another time", "bad time",
        "abhi nahi", "baad mein", "busy hun"
    ]
    
    IMPLICIT_SIGNALS = [
        "have to go", "need to go", "gotta go",
        "running late", "in the middle of",
        "jaana hai", "chalna hai"
    ]
    
    def __init__(self):
        self.override_detected = False
        self.override_type = None
    
    def check_for_override(self, transcript: str) -> dict:
        """Check transcript for override signals"""
        transcript_lower = transcript.lower()
        
        # Check by priority order
        for signal in self.IMMEDIATE_SIGNALS:
            if signal in transcript_lower:
                return {
                    "detected": True,
                    "type": "immediate",
                    "signal": signal,
                    "action": "close_now"
                }
        
        for signal in self.SAFETY_SIGNALS:
            if signal in transcript_lower:
                return {
                    "detected": True,
                    "type": "safety",
                    "signal": signal,
                    "action": "close_now"
                }
        
        for signal in self.TEMPORAL_SIGNALS:
            if signal in transcript_lower:
                return {
                    "detected": True,
                    "type": "temporal",
                    "signal": signal,
                    "action": "ask_callback_only"
                }
        
        for signal in self.IMPLICIT_SIGNALS:
            if signal in transcript_lower:
                return {
                    "detected": True,
                    "type": "implicit",
                    "signal": signal,
                    "action": "close_politely"
                }
        
        return {"detected": False}
    
    def get_override_response(self, override_info: dict,
                               language: str) -> str:
        """Generate appropriate override response"""
        action = override_info["action"]
        
        responses = {
            "close_now": {
                "english": "No problem, bye!",
                "hindi": "कोई बात नहीं, bye!",
                "hinglish": "No problem, bye!"
            },
            "ask_callback_only": {
                "english": "Got it! Evening or weekend better for a callback?",
                "hindi": "समझ गया! Evening या weekend—कब call करूं?",
                "hinglish": "Got it! Evening ya weekend better?"
            },
            "close_politely": {
                "english": "Sure, no worries. Take care!",
                "hindi": "ठीक है, कोई बात नहीं। Bye!",
                "hinglish": "Sure, no worries. Bye!"
            }
        }
        
        return responses.get(action, {}).get(
            language, responses[action]["english"]
        )
    
    def should_skip_to_close(self, override_info: dict) -> bool:
        """Determine if we should skip remaining flow"""
        skip_actions = ["close_now", "close_politely"]
        return override_info.get("action") in skip_actions


class ConversationFlow:
    """Flow with override handling"""
    
    def __init__(self):
        self.override_handler = OverrideHandler()
        self.current_step = "opening"
    
    def process_turn(self, caller_input: str, 
                     context: dict) -> dict:
        # ALWAYS check for override first
        override = self.override_handler.check_for_override(
            caller_input
        )
        
        if override["detected"]:
            # Skip normal flow
            if self.override_handler.should_skip_to_close(override):
                return {
                    "response": self.override_handler.get_override_response(
                        override, context.get("language", "english")
                    ),
                    "next_step": "close",
                    "intent": "callback" if override["type"] == "temporal" 
                              else "unable_to_continue"
                }
            
            # For temporal, ask callback preference only
            if override["action"] == "ask_callback_only":
                return {
                    "response": self.override_handler.get_override_response(
                        override, context.get("language", "english")
                    ),
                    "next_step": "capture_callback",
                    "skip_pitch": True
                }
        
        # Normal flow processing
        return self.normal_flow(caller_input, context)
```

### Prompt Design for Override
```yaml
instructions: |
  ## OVERRIDE RULES (CHECK EVERY TURN - HIGHEST PRIORITY)
  
  If caller says ANY of these, STOP IMMEDIATELY:
  - "busy", "meeting", "class", "not now", "can't talk"
  - "call later", "call back", "another time"
  - "driving", "emergency"
  - "stop", "hang up"
  
  When override detected:
  1. STOP current pitch/question immediately
  2. Do NOT add "just one thing" or "quickly"
  3. For "busy/later" → Ask ONLY: "Evening or weekend better?"
  4. For "driving/stop" → Say only "No problem, bye!"
  5. Do NOT ask any other question after override
  
  The override check happens BEFORE any other processing.
  A single "busy" anywhere in their response = override.
```

### Detection & Response

1. **Real-time override-signal detection with priority-based action**: For every caller turn, OverrideHandler.check_for_override() runs first (highest priority, before any other processing). Signals prioritized: IMMEDIATE_SIGNALS (stop, hang up, end call) → SAFETY_SIGNALS (driving, emergency) → TEMPORAL_SIGNALS (busy, meeting) → IMPLICIT_SIGNALS (have to go). On detection, agent: (a) immediately stops normal flow, (b) generates context-appropriate response (close_now vs. ask_callback_only vs. close_politely), (c) transitions to close or callback-only state, (d) logs override: {signal_detected, signal_type, caller_language, response_given, agent_action}.

2. **Post-call override-compliance audit**: After call completes, audit: did agent correctly recognize and respond to override signals? Check: (a) any override signals in transcript? (b) if yes, did agent detect? (c) if detected, did agent immediately stop pitch? (d) if temporal override, did agent ask only callback preference (no other questions)? (e) Calculate override_compliance_score for call. Log failures: {call_id, override_signal_missed: Y/N, trailing_questions_after_override: count}. Alert if: >10% of calls with override signals show compliance failure.

### Architecture Patterns

1. **Priority-Based Override State Machine**: On every turn, check OverrideHandler BEFORE entering normal flow. IMMEDIATE_SIGNALS trigger "close_now" state. SAFETY_SIGNALS trigger "close_now" state with urgency. TEMPORAL_SIGNALS trigger "ask_callback_only" state. IMPLICIT_SIGNALS trigger "close_politely" state. Normal flow only executes if no override detected.

2. **Override-Signal Detector with Language-Specific Patterns**: Maintains lists of signals in multiple languages (English, Hindi, Hinglish). NLP-based pattern matching (not just string matching) recognizes synonyms and variations. E.g., "I'm really busy" or "totally swamped" should match "busy" signal.

3. **Callback-Preference Capture (Temporal Override Only)**: For temporal overrides ("busy", "meeting", "call later"), agent transitions to "ask_callback_only" state. Single question: "Evening or weekend better for a callback?" Captures preference. No other questions or pitch elements.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Override Signal Detection Rate | >99% | <90% | # of override signals in call detected by agent / total override signals in call transcript (audited manual check) |
| Immediate-Signal Response Time | <2 sec | >5 sec | Time from signal spoken to agent stops pitch and responds |
| Clean Exit Rate (No Trailing Questions) | 100% | <85% | # of override calls with no questions asked after override / total override calls |
| Temporal-Override Callback-Only Compliance | 100% | <95% | # of temporal overrides where agent asked only callback preference / total temporal overrides |
| Safety-Signal Missed Rate | 0% | >0% | # of calls with safety signals (driving, emergency) that agent failed to detect / total safety-signal calls |
| Override Repeat Rate | <5% | >10% | # of calls where caller had to repeat override signal >1 time / total override calls |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Immediate-Signal Ignored | Agent continues pitch after caller says "stop", "hang up", "end call" | CRITICAL | Immediate call termination; escalate to agent review; may indicate agent malfunction |
| Safety-Signal Missed | Agent continues after caller indicates driving, emergency, or safety concern | CRITICAL | Immediate call termination; escalate to safety review; may indicate agent danger |
| Trailing Questions After Override | Agent asks questions after detecting override (e.g., "Got it! Quick question though—") | HIGH | Flag call for compliance violation; escalate to training; may impact caller satisfaction |
| Temporal Override, No Callback Captured | Caller signals "call me later" or "not now" but agent doesn't ask callback preference | MEDIUM | Flag call as incomplete; may attempt callback without knowing caller preference |
| Override Signal Not Detected | Agent continues normally despite override signal in transcript | HIGH | Audit signal-detection patterns; may indicate NLP model degradation; may require model retraining |

---

## References

- [Conversational AI Interrupts](https://arxiv.org/abs/2106.07837) - Priority handling
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - User frustration
- [AppInventiv: Voice Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Override issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
