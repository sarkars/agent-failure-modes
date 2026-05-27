# Slow Tool Silence

## Issue: Agent Goes Silent During Tool Execution Without Acknowledgment

**Frequency**: Very Common

**Symptoms**
- Dead air while tool/API call executes
- Caller asks "Are you there?" during lookup
- No "let me check" before silence
- Agent seems frozen during database query
- Callers hang up during long silence
- Silence interpreted as disconnection

**Root Cause**
Knowledge-base lookups, API requests, and database queries can take several seconds. Without an acknowledgment before the tool executes, callers hear silence and assume the agent froze or the call dropped. The prompt may tell the LLM to acknowledge, but this adds generation latency on top of tool latency. The reliable solution is configuring automatic acknowledgment messages that play when tools fire.

**Example**
```
Scenario 1: Database lookup without acknowledgment

Caller: "Can you check if my order shipped?"
[Agent calls shipping_lookup tool]
[3.5 seconds of silence]
Caller: "Hello? Are you still there?"
Agent: "Yes! Your order shipped yesterday."
Caller: "Oh, I thought the call dropped."

← No acknowledgment before tool call
← 3.5 seconds felt like forever
← Caller lost confidence

---

Scenario 2: Knowledge base search silence

Caller: "What are the side effects of this medication?"
[Agent searches medical knowledge base]
[4 seconds of silence]
Caller: "Hello?"
Agent: "Common side effects include..."
Caller: "I thought you froze."

← Medical lookup took 4 seconds
← Silence was confusing
← Should have said "Let me look that up"

---

Scenario 3: API call with LLM acknowledgment (still slow)

Caller: "Can you check my account balance?"
[LLM generates: "Let me check that for you"]  ← 600ms
[Account API call] ← 2,000ms
[LLM generates response] ← 800ms
Total: 3,400ms before useful information

← LLM-generated acknowledgment added 600ms
← Better than silence but still slow
← Pre-configured acknowledgment would be instant

---

Scenario 4: Proper tool acknowledgment

Caller: "What's the status of my refund?"
Agent: "Let me pull that up for you..."  ← Instant, pre-configured
[Refund API call: 2,500ms]
Agent: "Got it! Your refund of $45.99 was processed yesterday."

← Instant acknowledgment (not LLM-generated)
← Caller knows agent is working
← 2.5 second wait feels shorter with context

---

Scenario 5: Multiple tool calls compounding silence

Caller: "I want to change my shipping address and cancel 
         the express shipping."
[Agent calls address_update tool: 1.5s]
[No acknowledgment]
[Agent calls shipping_update tool: 2.0s]
[No acknowledgment]
[Total: 3.5 seconds of silence]
Caller: "Did that go through? Hello?"

← Two sequential tool calls
← No acknowledgment for either
← Caller assumes failure

---

Tool silence analysis (1,000 calls with tool usage):
  
  Tool calls per call: 2.3 average
  
  Tool execution times:
    < 1 second: 35%
    1-2 seconds: 40%
    2-4 seconds: 20%
    > 4 seconds: 5%
  
  Acknowledgment patterns:
    No acknowledgment: 45%
    LLM-generated acknowledgment: 35%
    Pre-configured instant ack: 20%
  
  Caller "hello?" during tool silence:
    No acknowledgment: 28%
    LLM acknowledgment: 12%
    Pre-configured: 4%
  
  Call abandonment during tool:
    No acknowledgment: 8%
    With acknowledgment: 2%
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Tool calls without acknowledgment: 40-50%
- Average tool execution time: 1.5-2.5s
- Caller "hello?" rate without ack: 25-30%
- Call abandonment during silence: 5-10%
- Pre-configured ack vs LLM ack: 600ms faster

**Tool Timing Issues**
| Tool Type | Typical Duration | Without Ack | With Ack |
|-----------|-----------------|-------------|----------|
| Database lookup | 1-2s | Confusing | Clear |
| API call | 1-3s | Frustrating | Acceptable |
| Knowledge search | 2-4s | Call drops | Patient wait |
| Multiple sequential | 3-6s | Abandonment | Engaged |

**Contributing Factors**
- No tool acknowledgment configured
- LLM acknowledgment adds latency
- Multiple tools compound silence
- No progress indicators for voice
- Silence threshold not tuned
- Prompts don't cover tool pauses

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Single tool | "Check my order" | Instant ack | Silence |
| Slow API | 3+ second call | Ack + patience | "Hello?" |
| Multiple tools | Two actions | Ack for each | Compounded silence |
| Knowledge lookup | "Tell me about..." | "Let me find that" | Dead air |
| Pre-configured | Tool fires | < 100ms to ack | 600ms+ |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Ack before tool | > 95% | Turn analysis |
| Ack latency | < 200ms | Timing measurement |
| "Hello?" during tool | < 5% | Transcript analysis |
| Abandonment during tool | < 2% | Call termination timing |

---

## Mitigation Strategies

### Prevention
1. **Pre-configured acknowledgments**: Automatic message when tool fires
2. **Tool-specific messages**: Different acks for different tools
3. **No LLM generation for ack**: Use instant playback
4. **Progress updates**: For long operations, update periodically
5. **Timeout handling**: If tool fails, acknowledge that too
6. **Parallel where possible**: Start acknowledgment while tool runs

### Implementation
```python
class ToolAcknowledgmentManager:
    """Manage acknowledgments for tool calls"""
    
    # Pre-configured acknowledgments (instant playback, no LLM)
    TOOL_ACKNOWLEDGMENTS = {
        "order_lookup": {
            "start": "Let me pull up your order...",
            "long": "Still checking, one moment...",
            "error": "I'm having trouble finding that. Let me try again."
        },
        "account_balance": {
            "start": "Checking your balance...",
            "long": "Just a moment...",
            "error": "I couldn't access your account. Let me try another way."
        },
        "knowledge_search": {
            "start": "Let me find that information...",
            "long": "Searching our database...",
            "error": "I'm not finding that. Let me rephrase."
        },
        "shipping_update": {
            "start": "Updating your shipping...",
            "long": "Processing that change...",
            "error": "The update didn't go through. Let me try again."
        },
        "default": {
            "start": "Let me check on that...",
            "long": "One moment...",
            "error": "Let me try that again."
        }
    }
    
    LONG_THRESHOLD_MS = 3000  # When to play "long" message
    
    def __init__(self, tts_player):
        self.tts = tts_player
        self.active_tools = {}
    
    def on_tool_start(self, tool_name: str, call_id: str):
        """Play acknowledgment when tool starts"""
        ack_config = self.TOOL_ACKNOWLEDGMENTS.get(
            tool_name, 
            self.TOOL_ACKNOWLEDGMENTS["default"]
        )
        
        # Play start acknowledgment immediately
        self.tts.play_instant(ack_config["start"])
        
        # Schedule long-running acknowledgment
        self.active_tools[call_id] = {
            "tool": tool_name,
            "start_time": time.time(),
            "long_played": False
        }
        
        # Schedule timeout check
        self.schedule_long_check(call_id, ack_config["long"])
    
    def schedule_long_check(self, call_id: str, long_message: str):
        """Schedule check for long-running tool"""
        async def check_and_play():
            await asyncio.sleep(self.LONG_THRESHOLD_MS / 1000)
            
            if call_id in self.active_tools:
                tool_state = self.active_tools[call_id]
                if not tool_state["long_played"]:
                    self.tts.play_instant(long_message)
                    tool_state["long_played"] = True
        
        asyncio.create_task(check_and_play())
    
    def on_tool_complete(self, call_id: str, success: bool):
        """Handle tool completion"""
        if call_id in self.active_tools:
            tool_state = self.active_tools.pop(call_id)
            
            if not success:
                tool_name = tool_state["tool"]
                ack_config = self.TOOL_ACKNOWLEDGMENTS.get(
                    tool_name,
                    self.TOOL_ACKNOWLEDGMENTS["default"]
                )
                self.tts.play_instant(ack_config["error"])


class InstantTTSPlayer:
    """Play pre-synthesized TTS instantly"""
    
    def __init__(self):
        # Pre-synthesize common acknowledgments
        self.cache = {}
        self.preload_acknowledgments()
    
    def preload_acknowledgments(self):
        """Pre-synthesize all acknowledgment audio"""
        all_acks = []
        for config in ToolAcknowledgmentManager.TOOL_ACKNOWLEDGMENTS.values():
            all_acks.extend(config.values())
        
        for text in set(all_acks):
            self.cache[text] = self.synthesize(text)
    
    def synthesize(self, text: str) -> bytes:
        """Synthesize text to audio (cached)"""
        # TTS synthesis
        return tts_engine.synthesize(text)
    
    def play_instant(self, text: str):
        """Play cached audio instantly"""
        if text in self.cache:
            audio = self.cache[text]
        else:
            audio = self.synthesize(text)
            self.cache[text] = audio
        
        # Play immediately - no LLM latency
        self.audio_output.play(audio)


class ToolCallWrapper:
    """Wrapper to handle tool calls with acknowledgments"""
    
    def __init__(self, ack_manager: ToolAcknowledgmentManager):
        self.ack = ack_manager
    
    async def call_with_ack(self, tool_name: str, 
                             tool_func: callable, 
                             **kwargs) -> dict:
        """Call tool with automatic acknowledgment"""
        call_id = str(uuid.uuid4())
        
        # Play acknowledgment immediately
        self.ack.on_tool_start(tool_name, call_id)
        
        try:
            # Execute tool
            result = await tool_func(**kwargs)
            self.ack.on_tool_complete(call_id, success=True)
            return {"success": True, "result": result}
        
        except Exception as e:
            self.ack.on_tool_complete(call_id, success=False)
            return {"success": False, "error": str(e)}
```

### Prompt Design
```yaml
instructions: |
  ## TOOL CALL HANDLING
  
  When you need to call a tool (lookup, API, search):
  
  1. DO NOT generate an acknowledgment yourself
     (This adds ~600ms latency on top of tool time)
  
  2. The system will automatically play:
     - "Let me check on that..." when tool starts
     - "One moment..." if tool takes > 3 seconds
     - Error message if tool fails
  
  3. Just call the tool - acknowledgment is automatic
  
  WRONG (adds latency):
  ```
  LLM: "Let me look that up for you"  ← 600ms generation
  [Tool call: 2000ms]
  LLM: "Your order shipped..."  ← 800ms generation
  Total: 3400ms
  ```
  
  CORRECT (instant ack):
  ```
  [Tool fires → instant "Let me check..."]  ← 0ms
  [Tool call: 2000ms]
  LLM: "Your order shipped..."  ← 800ms
  Total: 2800ms (600ms faster)
  ```
  
  For MULTIPLE tools:
  - Each tool gets its own acknowledgment
  - Don't let silence compound
  
  If you MUST speak before a tool (unusual case):
  - Keep it to 3-4 words max
  - "Checking now" not "Let me go ahead and check that for you"
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `tool.ack_before_call` | < 90% |
| `tool.silence_duration` | > 2s without ack |
| `tool.caller_hello_rate` | > 10% |
| `tool.abandonment_during` | > 3% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| No Acknowledgment | < 80% of tool calls | P2 |
| Long Silence | > 4s without update | P2 |
| High "Hello?" Rate | > 15% during tools | P2 |
| Tool Abandonment | > 5% | P1 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Tool acknowledgment
- [VAPI Tool Configuration](https://docs.vapi.ai/tools) - Request-start messages
- [Voice AI Latency](https://hamming.ai/resources/testing-and-monitoring-livekit-voice-agents-production) - Tool timing
- [Voice Pipeline](https://docs.vapi.ai/customization/voice-pipeline-configuration) - Optimization
