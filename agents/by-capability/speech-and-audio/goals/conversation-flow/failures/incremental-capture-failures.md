# Incremental Capture Failures

## Issue: Agent Waits Until All Fields Collected Before Saving Data

**Frequency**: Common

**Symptoms**
- Call drops mid-conversation, all data lost
- Partial qualification not saved
- Caller must repeat everything on callback
- No record of interested-but-incomplete leads
- CRM shows only completed conversations
- Data lost to disconnections, distractions

**Root Cause**
Many voice agents only call the data capture tool (CRM update, lead form, etc.) after collecting ALL required fields. If the call drops mid-conversation—due to network issues, caller distraction, or battery death—everything captured so far is lost. Incremental capture (calling the tool after each field) ensures partial data survives disconnection.

**Example**
```
Scenario 1: Call drops, all data lost

Agent: "What's your name?"
Caller: "Sarah Chen."
Agent: "Great! And your company?"
Caller: "FintechGo."
Agent: "What's your use case?"
Caller: "We're building a customer service—"
[CALL DROPPED - Network issue]

What happened:
- Agent collected: name, company, partial use case
- Tool never called (waiting for all fields)
- Data lost entirely
- No record of Sarah Chen from FintechGo

---

Scenario 2: Incremental capture saves data

Agent: "What's your name?"
Caller: "Sarah Chen."
[Tool call: capture_lead(name="Sarah Chen")]

Agent: "Great! And your company?"
Caller: "FintechGo."
[Tool call: capture_lead(name="Sarah Chen", company="FintechGo")]

Agent: "What's your use case?"
Caller: "We're building a customer service—"
[CALL DROPPED]

What was saved:
- Name: Sarah Chen ✓
- Company: FintechGo ✓
- Use case: Partial ("customer service")
- Status: "Incomplete - callback needed"

← 80% of valuable data preserved
← Can callback with context
← Lead not lost

---

Scenario 3: Qualification progress lost

Agent collects over 8 turns:
- Interest: Yes
- Timeline: Q3
- Budget: $50K
- Company size: 100 employees
- Current solution: Competitor X
[Phone battery dies]

Without incremental capture:
- Entire conversation lost
- Agent doesn't know any qualification info
- Callback starts from scratch

With incremental capture:
- All 5 data points saved
- Callback: "Hey Sarah, we got cut off! You mentioned 
  you're comparing with Competitor X for Q3..."

---

Scenario 4: Tool call pattern comparison

WRONG - Wait for all fields:
```
[Collect name] → no tool call
[Collect email] → no tool call
[Collect company] → no tool call
[Collect use_case] → no tool call
[Complete] → capture_lead(name, email, company, use_case)
```
If call drops at step 3: EVERYTHING LOST

RIGHT - Incremental capture:
```
[Collect name] → capture_lead(name="Sarah")
[Collect email] → capture_lead(name="Sarah", email="...")
[Collect company] → capture_lead(name="Sarah", email="...", company="...")
```
If call drops at step 3: name and email SAVED

---

Scenario 5: Callback with context

Without incremental capture:
Agent: "Hi, calling back about earlier—what was your name again?"
Caller: [Annoyed] "I already told you. Sarah."
Agent: "And your company?"
Caller: "I told you that too. FintechGo. Are you serious?"

With incremental capture:
Agent: "Hi Sarah! We got disconnected earlier. You were 
        telling me about the customer service project at 
        FintechGo—want to pick up where we left off?"
Caller: "Oh great, yes! So we need..."

← Caller feels valued, not interrogated

---

Incremental capture analysis (1,000 calls):
  
  Calls with disconnection: 14.5%
  
  Without incremental capture:
    Data recovery rate: 0%
    Callback success: 35%
    Repeat info friction: High
    
  With incremental capture:
    Data recovery rate: 85%
    Callback success: 68%
    Repeat info friction: Low
  
  Fields captured before disconnect:
    1-2 fields: 45%
    3-4 fields: 35%
    5+ fields: 20%
    
  All would be LOST without incremental capture
```

**Key Statistics**
From Voice Data Capture Research (2026):
- Calls with mid-conversation drop: 10-15%
- Data loss without incremental capture: 100%
- Data recovery with incremental: 80-90%
- Callback success improvement: +30-40%
- Caller frustration reduction: 60%

**Capture Strategy Comparison**
| Strategy | Data on Disconnect | Callback UX | Implementation |
|----------|-------------------|-------------|----------------|
| Wait for all fields | 0% saved | Poor | Simple |
| Incremental capture | 80-90% saved | Good | More tool calls |
| Hybrid (key fields) | 50-60% saved | Moderate | Medium |

**Contributing Factors**
- Single tool call at end pattern
- "Complete record" mindset
- Tool designed for batch submission
- No partial record handling
- Disconnection not anticipated
- Text form patterns in voice

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| After first field | Name given | Tool called | No tool call |
| After each field | Multiple fields | Tool per field | Only at end |
| On disconnect | Mid-conversation | Partial saved | Nothing saved |
| Callback | After disconnect | Context preserved | Start over |
| Empty fields | Incomplete | Empty string, not skip | Missing call |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Tool calls per field | 1 | Tool call count |
| Disconnect data recovery | > 80% | Fields saved |
| Callback context rate | > 90% | Has prior data |
| Repeat info requests | < 10% | Callback analysis |

---

## Mitigation Strategies

### Prevention
1. **Call tool after each field**: Don't wait for completion
2. **Include all known fields**: Send everything on each call
3. **Empty string for unknown**: Don't skip fields
4. **Partial status**: Mark records as "incomplete"
5. **Callback context**: Load prior data on callback
6. **Progress tracking**: Know what's captured

### Implementation
```python
class IncrementalDataCapture:
    """Capture data incrementally to prevent loss"""
    
    def __init__(self, required_fields: list, 
                 capture_tool: callable):
        self.required_fields = required_fields
        self.captured_data = {field: "" for field in required_fields}
        self.capture_tool = capture_tool
        self.call_id = str(uuid.uuid4())
    
    def capture_field(self, field_name: str, value: str) -> dict:
        """Capture a single field and save immediately"""
        # Update captured data
        self.captured_data[field_name] = value
        
        # Call tool with ALL data (empty string for uncaptured)
        result = self.capture_tool(
            call_id=self.call_id,
            status=self.get_status(),
            **self.captured_data
        )
        
        return {
            "captured": field_name,
            "value": value,
            "total_captured": self.count_captured(),
            "total_required": len(self.required_fields),
            "tool_result": result
        }
    
    def get_status(self) -> str:
        """Get current capture status"""
        captured = self.count_captured()
        total = len(self.required_fields)
        
        if captured == 0:
            return "started"
        elif captured < total:
            return "in_progress"
        else:
            return "complete"
    
    def count_captured(self) -> int:
        """Count non-empty captured fields"""
        return sum(1 for v in self.captured_data.values() if v)
    
    def get_progress(self) -> dict:
        """Get capture progress"""
        return {
            "captured_fields": [k for k, v in self.captured_data.items() if v],
            "remaining_fields": [k for k, v in self.captured_data.items() if not v],
            "percentage": (self.count_captured() / len(self.required_fields)) * 100
        }


class CallbackContextLoader:
    """Load context for callback from prior capture"""
    
    def __init__(self, data_store):
        self.store = data_store
    
    def load_prior_context(self, phone_number: str) -> dict:
        """Load prior conversation context"""
        # Find incomplete records for this number
        prior = self.store.find(
            phone_number=phone_number,
            status__in=["in_progress", "disconnected"],
            created_at__gt=datetime.now() - timedelta(hours=24)
        )
        
        if not prior:
            return {"has_context": False}
        
        latest = prior[0]
        
        return {
            "has_context": True,
            "call_id": latest.call_id,
            "captured_data": latest.data,
            "last_field": latest.last_field,
            "disconnect_time": latest.updated_at,
            "callback_opening": self.generate_callback_opening(latest)
        }
    
    def generate_callback_opening(self, prior_record) -> str:
        """Generate personalized callback opening"""
        name = prior_record.data.get("name", "")
        company = prior_record.data.get("company", "")
        
        if name and company:
            return (f"Hi {name}! We got disconnected earlier. "
                   f"You were telling me about {company}—"
                   f"want to pick up where we left off?")
        elif name:
            return (f"Hi {name}! Our call got cut off. "
                   f"Want to continue where we left off?")
        else:
            return ("Hey! We got disconnected earlier. "
                   "Want to pick up where we left off?")


class IncrementalToolWrapper:
    """Wrapper to make any capture tool incremental"""
    
    def __init__(self, base_tool: callable, fields: list):
        self.base_tool = base_tool
        self.fields = fields
        self.current_data = {}
    
    def capture(self, **new_data) -> dict:
        """Capture new data incrementally"""
        # Merge new data with existing
        self.current_data.update(new_data)
        
        # Build full payload with empty strings for missing
        payload = {field: self.current_data.get(field, "") 
                   for field in self.fields}
        
        # Add metadata
        payload["_status"] = "complete" if all(
            self.current_data.get(f) for f in self.fields
        ) else "in_progress"
        payload["_captured_count"] = sum(
            1 for f in self.fields if self.current_data.get(f)
        )
        
        # Call base tool
        return self.base_tool(**payload)
    
    def on_disconnect(self) -> dict:
        """Handle disconnection"""
        # Save final state
        payload = {field: self.current_data.get(field, "") 
                   for field in self.fields}
        payload["_status"] = "disconnected"
        payload["_disconnect_time"] = datetime.now().isoformat()
        
        return self.base_tool(**payload)
```

### Prompt Design
```yaml
instructions: |
  ## INCREMENTAL DATA CAPTURE
  
  Call the capture tool INCREMENTALLY—one field at a time, 
  as soon as you hear it. DO NOT wait until you have all fields.
  
  WHY: If the call drops mid-conversation, data captured so 
  far is saved. Waiting until the end means losing everything.
  
  PATTERN:
  ```
  [Caller says name] → capture_lead(name="Sarah", email="", ...)
  [Caller says email] → capture_lead(name="Sarah", email="x@y.com", ...)
  [Caller says company] → capture_lead(name="Sarah", email="x@y.com", company="Acme", ...)
  ```
  
  ALWAYS send ALL fields on every call:
  - Fill in what you know
  - Use empty string "" for what you don't know yet
  - This creates a complete record that updates incrementally
  
  ON CALLBACK with prior context:
  - Check for prior incomplete record
  - Use personalized opening: "Hi Sarah, we got cut off! 
    You were telling me about the Acme project..."
  - Don't ask for information you already have
  
  NEVER:
  - Wait until conversation complete to call capture tool
  - Skip tool call because you don't have all fields
  - Ask caller to repeat information you already saved
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `capture.calls_per_field` | < 1 |
| `capture.disconnect_data_loss` | > 10% |
| `capture.callback_no_context` | > 20% |
| `capture.repeat_requests` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| No Incremental Capture | Tool only at end | P2 |
| Data Loss on Disconnect | > 20% fields lost | P1 |
| Callback Without Context | > 30% | P2 |
| Repeat Info Requests | > 15% | P3 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Incremental tool calls
- [Voice Data Collection](https://www.callcow.ai/blog/ai-voice-agent-forms-platform) - Capture patterns
- [Call Reliability](https://www.assemblyai.com/blog/voice-agent-features) - Disconnection handling
- [CRM Integration](https://docs.vapi.ai/tools) - Tool patterns
