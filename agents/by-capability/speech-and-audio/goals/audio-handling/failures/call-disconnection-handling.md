# Call Disconnection Handling

## Issue: Agent Fails to Handle Mid-Call Disconnections Gracefully

**Frequency**: Common (5-15% of calls)

**Symptoms**
- Call drops with no recovery attempt
- No detection that caller disconnected
- Agent continues talking after disconnect
- No callback or follow-up mechanism
- Data captured before disconnect lost
- No differentiation between intentional vs accidental drop

**Root Cause**
Voice calls can disconnect for many reasons: network issues, caller accidentally hung up, phone died, caller entered dead zone. Without proper disconnection handling, captured data may be lost, callbacks aren't triggered, and there's no way to distinguish intentional hang-ups from accidents.

**Example**
```
Scenario 1: Network drop mid-qualification

Agent: "Great! And what's your college name?"
Caller: "I'm at Del—"
[CALL DROPPED - Network issue]

What should happen:
- Detect disconnect
- Save partial data (interest: yes, permission: pending)
- Mark as "disconnected - incomplete"
- Trigger callback attempt

What often happens:
- Call ends with no outcome classification
- Data not saved
- No callback triggered
- Caller must re-explain everything if called back

---

Scenario 2: Accidental hang-up

[Caller accidentally pressed end button]

Agent: [Continues talking to dead line]
Agent: "...so the perks include certificate and trophy..."
[30 seconds pass]
Agent: [Finally detects no response, closes call]

← Should detect disconnect immediately
← Wasted 30 seconds talking to no one

---

Scenario 3: Phone died

[At 85% through qualified conversation]
Caller: "Yes, WhatsApp is fine on this num—"
[Phone battery died]

Outcome: "Unable to continue"
Should be: "Disconnected at 85% - callback"

← Lost a nearly-complete qualification
← Should trigger priority callback

---

Scenario 4: Intentional vs accidental

Intentional: Caller says "bye" then hangs up ✓
Accidental: Mid-sentence disconnect ✗
Frustrated: Hangs up without goodbye (might be upset)

Agent should handle these differently but often treats all same.

---

Disconnection analysis (1,000 calls):
  Clean ending (goodbye + hang up): 720 (72%)
  Mid-call disconnection: 145 (14.5%)
  
  Disconnection causes (estimated):
    Network issues: 45%
    Accidental: 25%
    Phone/battery: 15%
    Frustrated hang-up: 10%
    Other: 5%
  
  Recovery actions taken:
    Callback triggered: 23%
    Data saved: 56%
    Proper classification: 34%
```

**Key Statistics**
From Voice Call Disconnection Research (2026):
- Mid-call disconnection rate: 5-15%
- Accidental disconnection: 25-35% of drops
- Network-related drops: 40-50%
- Recovery callback success: 50-70%
- Data loss from improper handling: 30-45%

**Disconnection Types**
| Type | Signal | Appropriate Action |
|------|--------|-------------------|
| Network drop | Sudden silence mid-word | Save data, callback |
| Accidental | Silence after talking | Short wait, callback |
| Phone died | Sudden silence | Save data, callback later |
| Frustrated | Hang up after objection | Don't callback immediately |
| Clean end | "Bye" then silence | Normal close |

**Contributing Factors**
- No real-time connection monitoring
- No partial data persistence
- No disconnect vs. silence differentiation
- Missing callback trigger logic
- No frustration detection
- Single outcome for all disconnects

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Mid-word drop | Disconnect at "Del—" | Save partial, mark callback | Data lost |
| After permission | Disconnect post-yes | Save permission, callback | No data saved |
| Detection speed | Sudden silence | Detect < 3s | Continue talking |
| Frustrated drop | Hang up after objection | Mark frustrated, no callback | Callback triggered |
| Network recovery | Brief drop, reconnect | Resume conversation | Start over |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Disconnect detection | < 3s | Time to detect silence |
| Partial data save | > 95% | Data saved on disconnect |
| Callback trigger | > 80% | When appropriate |
| Recovery success | > 50% | Successful callback conversion |

---

## Mitigation Strategies

### Prevention
1. **Real-time connection monitoring**: Detect drops immediately
2. **Partial data persistence**: Save progress continuously
3. **Disconnect classification**: Differentiate types
4. **Callback triggering**: Automatic for accidental drops
5. **Frustration detection**: Identify angry hang-ups
6. **Resume capability**: Continue where left off on callback

### Implementation
```python
class DisconnectionHandler:
    """Handle call disconnections gracefully"""
    
    DISCONNECT_TYPES = {
        "clean_end": {
            "signals": ["goodbye detected", "thank you + silence"],
            "action": "normal_close",
            "callback": False
        },
        "network_drop": {
            "signals": ["mid-word silence", "sudden cut"],
            "action": "save_and_callback",
            "callback": True,
            "priority": "high"
        },
        "accidental": {
            "signals": ["mid-conversation silence", "no goodbye"],
            "action": "save_and_callback",
            "callback": True,
            "priority": "medium"
        },
        "frustrated": {
            "signals": ["after_objection", "abrupt after negative"],
            "action": "save_no_callback",
            "callback": False,
            "cooldown": "24h"
        }
    }
    
    def __init__(self, silence_threshold_ms=3000):
        self.silence_threshold = silence_threshold_ms
        self.last_audio_timestamp = None
        self.conversation_state = {}
    
    def monitor_connection(self, audio_stream) -> dict:
        """Monitor for disconnection"""
        silence_duration = self.get_silence_duration(audio_stream)
        
        if silence_duration > self.silence_threshold:
            disconnect_type = self.classify_disconnect()
            return {
                "disconnected": True,
                "type": disconnect_type,
                "action": self.DISCONNECT_TYPES[disconnect_type]["action"],
                "data_to_save": self.get_conversation_state()
            }
        
        return {"disconnected": False}
    
    def classify_disconnect(self) -> str:
        """Classify type of disconnection"""
        # Check last message sentiment
        if self.last_message_was_negative():
            return "frustrated"
        
        # Check if goodbye was said
        if self.goodbye_detected():
            return "clean_end"
        
        # Check if mid-word
        if self.was_mid_utterance():
            return "network_drop"
        
        return "accidental"
    
    def handle_disconnect(self, disconnect_type: str) -> dict:
        """Handle disconnection appropriately"""
        config = self.DISCONNECT_TYPES.get(disconnect_type)
        
        # Always save partial data
        saved_data = self.save_partial_conversation()
        
        result = {
            "saved_data": saved_data,
            "outcome": f"disconnected_{disconnect_type}",
        }
        
        # Trigger callback if appropriate
        if config.get("callback"):
            result["callback"] = {
                "trigger": True,
                "priority": config.get("priority", "medium"),
                "delay": "5_minutes" if disconnect_type == "network_drop" 
                        else "1_hour"
            }
        
        return result
    
    def save_partial_conversation(self) -> dict:
        """Save all captured data before disconnect"""
        return {
            "timestamp": datetime.now(),
            "progress_percentage": self.calculate_progress(),
            "captured_fields": self.conversation_state,
            "last_step": self.current_step,
            "last_agent_message": self.last_agent_message,
            "last_caller_message": self.last_caller_message,
            "disconnect_point": self.get_disconnect_point()
        }


class CallbackManager:
    """Manage callbacks for disconnected calls"""
    
    def __init__(self):
        self.callback_queue = []
    
    def schedule_callback(self, call_data: dict, 
                          priority: str,
                          delay: str) -> dict:
        """Schedule a callback for disconnected call"""
        callback = {
            "original_call_id": call_data.get("call_id"),
            "phone_number": call_data.get("phone_number"),
            "saved_state": call_data.get("saved_data"),
            "priority": priority,
            "scheduled_time": self.calculate_callback_time(delay),
            "attempt": 1,
            "max_attempts": 2,
            "resume_from": call_data.get("last_step")
        }
        
        self.callback_queue.append(callback)
        return callback
    
    def get_callback_opening(self, saved_state: dict) -> str:
        """Generate opening for callback based on prior context"""
        progress = saved_state.get("progress_percentage", 0)
        
        if progress > 70:
            return ("Hey, we got disconnected earlier! You were "
                   "almost done—can we finish up real quick?")
        elif progress > 30:
            return ("Hey, our call got cut off. You seemed "
                   "interested—got a minute to continue?")
        else:
            return ("Hey, we got disconnected earlier. "
                   "Is now a better time?")
```

### Prompt Design
```yaml
instructions: |
  ## DISCONNECTION HANDLING
  
  If caller suddenly goes silent mid-conversation:
  
  1. DETECT quickly (< 3 seconds of silence)
  2. DO NOT continue talking to empty line
  3. CLASSIFY the disconnect:
     - Clean end: They said bye first
     - Accidental/Network: Mid-sentence or mid-conversation
     - Frustrated: After negative response
  
  4. SAVE all captured data immediately:
     - Interest level
     - Any permissions given
     - College name if captured
     - Last step completed
  
  5. OUTCOME should reflect disconnect:
     - "disconnected_callback" (if need callback)
     - "disconnected_complete" (if was finishing)
     - "disconnected_frustrated" (if after objection)
  
  On CALLBACK to disconnected caller:
  - Acknowledge the disconnect
  - Don't start from scratch
  - "Hey, we got cut off! You were interested—want to continue?"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `disconnect.rate` | > 15% |
| `disconnect.detection_time` | > 5s |
| `disconnect.data_saved` | < 90% |
| `disconnect.callback_success` | < 40% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Disconnect Rate | > 20% | P2 |
| Slow Detection | > 10s | P3 |
| Data Loss on Disconnect | > 20% | P1 |

---

## References

- [Voice Call Quality](https://www.beconversive.com/blog/voice-ai-challenges) - Connection issues
- [Telecom Reliability](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Drop handling
- [Callback Best Practices](https://getbluejay.ai/resources/voice-agent-production-failures) - Recovery
- [Session Management](https://arxiv.org/abs/2106.07837) - State persistence
