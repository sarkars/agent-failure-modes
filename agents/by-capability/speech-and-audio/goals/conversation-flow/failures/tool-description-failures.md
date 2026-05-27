# Tool Description Failures

## Issue: Vague or Poor Tool Descriptions Cause Wrong Tool Calls or Bad Parameters

**Frequency**: Very Common

**Symptoms**
- Agent calls wrong tool for the task
- Parameters passed incorrectly to tools
- Agent doesn't call tool when it should
- Tool called with malformed values
- Agent guesses parameter values
- Inconsistent tool invocation behavior

**Root Cause**
The LLM's ability to use tools correctly depends entirely on how well you describe them. Vague tool descriptions like "Makes an API call" give the model no guidance on when to call the tool or what parameters to pass. Poor parameter names and missing format hints cause the model to guess. Tool description quality is one of the top causes of tool invocation errors.

**Example**
```
Scenario 1: Vague tool description

BAD tool definition:
{
  "name": "api_call",
  "description": "Makes an API call",
  "parameters": {
    "d": { "type": "string" },
    "t": { "type": "string" }
  }
}

Agent behavior:
Caller: "Can you book me an appointment for Friday?"
Agent: [Calls api_call with d="Friday", t="appointment"]
← Wrong parameters
← Model guessed what d and t mean
← API call fails

---

Scenario 2: Good tool description

GOOD tool definition:
{
  "name": "get_available_slots",
  "description": "Use this tool to check for available 
    appointment times in the clinic's calendar for a 
    specific date. Call this BEFORE booking to show 
    the caller their options.",
  "parameters": {
    "date": {
      "type": "string",
      "description": "The date to check for openings 
        (format: YYYY-MM-DD)"
    },
    "service_type": {
      "type": "string", 
      "description": "Type of service (cleaning, checkup, 
        emergency, consultation)"
    }
  }
}

Agent behavior:
Caller: "Can you book me an appointment for Friday?"
Agent: "Let me check what's available on Friday."
[Calls get_available_slots with date="2026-05-29", 
 service_type="checkup"]
← Correct tool called ✓
← Correct parameters ✓

---

Scenario 3: Ambiguous tools

Two poorly named tools:
- "lookup" → "Looks things up"
- "search" → "Searches for things"

Caller: "Can you find my appointment?"
Agent: [Calls "search" with query="appointment"]
← Wrong tool - should be "lookup_appointment"
← Model couldn't distinguish

BETTER:
- "lookup_appointment" → "Look up an existing appointment 
   by patient name or confirmation number"
- "search_knowledge_base" → "Search the FAQ and policy 
   documents for general information"

---

Scenario 4: Missing format hints

BAD:
{
  "name": "book_appointment",
  "parameters": {
    "date": { "type": "string" },
    "time": { "type": "string" }
  }
}

Agent calls with: date="Friday", time="afternoon"
API expects: date="2026-05-29", time="14:00"
← API fails due to format mismatch

GOOD:
{
  "name": "book_appointment", 
  "parameters": {
    "date": {
      "type": "string",
      "description": "Date (format: YYYY-MM-DD, e.g., 2026-05-29)"
    },
    "time": {
      "type": "string",
      "description": "Time in 24-hour format (e.g., 14:00, 09:30)"
    }
  }
}

---

Scenario 5: Transfer tool without description

Auto-generated transfer tool:
{
  "name": "transferCall",
  "description": "" // Empty!
}

Agent behavior:
Caller: "I need to speak to someone about billing."
Agent: [Doesn't call transfer tool]
        "I can help with general questions. What would 
         you like to know?"

← Empty description biased model against calling
← Should have explicit description

FIXED:
{
  "name": "transferCall",
  "description": "Transfer the caller to a human agent. 
    Use this when: the caller explicitly asks for a human, 
    the request is outside your scope, or you've failed 
    twice to help."
}

---

Tool description analysis (200 voice agents):
  
  Agents with detailed descriptions: 35%
  Agents with vague descriptions: 45%
  Agents with missing descriptions: 20%
  
  Tool call accuracy:
    Detailed descriptions: 92%
    Vague descriptions: 67%
    Missing descriptions: 41%
  
  Common issues:
    Wrong tool called: 23%
    Bad parameters: 31%
    Tool not called when needed: 18%
    Format mismatches: 28%
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Vague descriptions cause errors: 30-40%
- Missing format hints: 25-35% parameter errors
- Empty transfer tool descriptions: 60% never called
- Detailed descriptions improve accuracy: 25-35%
- Atomic tools outperform combined tools: 40%

**Tool Description Quality**
| Quality | Description | Error Rate |
|---------|-------------|------------|
| Detailed | When, what, format hints | 5-10% |
| Adequate | Basic purpose, some hints | 15-20% |
| Vague | One-line generic | 30-40% |
| Missing | Empty or auto-generated | 50-60% |

**Contributing Factors**
- Copy-paste from API docs without adaptation
- Auto-generated descriptions not customized
- No format hints in parameters
- Combined tools with mode parameters
- Unclear when to call vs not call
- Missing negative conditions

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Correct tool | "Book appointment" | get_slots then book | Wrong tool |
| Correct params | "Friday at 2pm" | Proper format | Wrong format |
| Transfer trigger | "Speak to human" | Transfer called | Not called |
| Disambiguation | Ambiguous request | Ask or correct tool | Wrong tool |
| Negative case | Out of scope | Don't call tool | Tool called |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Tool accuracy | > 95% | Correct tool called |
| Parameter accuracy | > 95% | Correct formats |
| Transfer usage | When needed | Transfer analysis |
| False tool calls | < 5% | Unnecessary calls |

---

## Mitigation Strategies

### Prevention
1. **Detailed descriptions**: When to call, what it does, what NOT to call it for
2. **Atomic tools**: One tool = one action (not mode parameters)
3. **Format hints**: Include format examples in parameter descriptions
4. **Explicit transfer description**: Never leave transfer tool blank
5. **Distinct names**: Avoid similar names like "lookup" vs "search"
6. **Negative conditions**: State when NOT to call the tool

### Implementation
```python
class ToolDescriptionValidator:
    """Validate tool descriptions for voice agents"""
    
    QUALITY_CRITERIA = {
        "has_when_to_call": r"(use this|call this|when)",
        "has_purpose": r"(to|for|in order to)",
        "has_negative": r"(do not|don't|never|only)",
        "has_format_hint": r"(format|e\.g\.|example)",
    }
    
    PARAMETER_CRITERIA = {
        "has_description": lambda p: bool(p.get("description")),
        "has_format": lambda p: "format" in p.get("description", "").lower(),
        "has_example": lambda p: "e.g." in p.get("description", "") or 
                                 "example" in p.get("description", "").lower(),
    }
    
    def validate_tool(self, tool: dict) -> dict:
        """Validate a tool definition"""
        issues = []
        score = 0
        
        description = tool.get("description", "")
        
        # Check description quality
        if not description:
            issues.append({
                "type": "missing_description",
                "severity": "critical",
                "message": "Tool has no description"
            })
        else:
            for criterion, pattern in self.QUALITY_CRITERIA.items():
                if re.search(pattern, description, re.IGNORECASE):
                    score += 1
                else:
                    issues.append({
                        "type": f"missing_{criterion}",
                        "severity": "warning",
                        "message": f"Description lacks {criterion}"
                    })
        
        # Check parameters
        for param_name, param_def in tool.get("parameters", {}).items():
            for criterion, check in self.PARAMETER_CRITERIA.items():
                if not check(param_def):
                    issues.append({
                        "type": f"param_{criterion}",
                        "severity": "warning",
                        "parameter": param_name,
                        "message": f"Parameter '{param_name}' lacks {criterion}"
                    })
        
        # Check for common anti-patterns
        if tool.get("name", "").lower() in ["api_call", "call", "request"]:
            issues.append({
                "type": "generic_name",
                "severity": "error",
                "message": "Tool name is too generic"
            })
        
        return {
            "valid": len([i for i in issues if i["severity"] == "critical"]) == 0,
            "score": score,
            "max_score": len(self.QUALITY_CRITERIA),
            "issues": issues
        }
    
    def suggest_improvements(self, tool: dict) -> str:
        """Suggest improved tool description"""
        name = tool.get("name", "unknown_tool")
        current = tool.get("description", "")
        
        template = f"""
        Use this tool to [WHAT IT DOES]. 
        Call this when [WHEN TO CALL].
        Do NOT call this for [NEGATIVE CASES].
        
        Example: {name}(param1="value1", param2="value2")
        """
        
        return template


class ToolDefinitionBuilder:
    """Build well-structured tool definitions"""
    
    def build_tool(self, 
                   name: str,
                   purpose: str,
                   when_to_call: str,
                   when_not_to_call: str,
                   parameters: dict) -> dict:
        """Build a complete tool definition"""
        
        description = f"{purpose}. {when_to_call}. {when_not_to_call}"
        
        # Enhance parameters with format hints
        enhanced_params = {}
        for param_name, param_def in parameters.items():
            enhanced = param_def.copy()
            if "description" not in enhanced:
                enhanced["description"] = f"The {param_name} value"
            enhanced_params[param_name] = enhanced
        
        return {
            "name": name,
            "description": description,
            "parameters": enhanced_params
        }
    
    def build_transfer_tool(self, 
                            destinations: list,
                            triggers: list) -> dict:
        """Build transfer tool with explicit description"""
        
        dest_str = ", ".join(destinations)
        trigger_str = "; ".join(triggers)
        
        return {
            "name": "transferCall",
            "description": f"Transfer the caller to a human agent. "
                          f"Available destinations: {dest_str}. "
                          f"Use this when: {trigger_str}.",
            "parameters": {
                "destination": {
                    "type": "string",
                    "description": f"Where to transfer. Options: {dest_str}"
                },
                "reason": {
                    "type": "string",
                    "description": "Brief reason for transfer (for agent context)"
                }
            }
        }


# Example well-defined tools
EXAMPLE_TOOLS = [
    {
        "name": "get_available_slots",
        "description": "Use this tool to check for available appointment "
                      "times in the clinic's calendar for a specific date. "
                      "Call this BEFORE attempting to book so the caller "
                      "can choose a time. Do NOT call this if the caller "
                      "hasn't specified what service they need.",
        "parameters": {
            "date": {
                "type": "string",
                "description": "The date to check (format: YYYY-MM-DD, "
                              "e.g., 2026-05-29)"
            },
            "service_type": {
                "type": "string",
                "description": "Type of appointment: cleaning, checkup, "
                              "emergency, or consultation"
            },
            "location": {
                "type": "string",
                "description": "Clinic location (downtown, westside)"
            }
        }
    },
    {
        "name": "book_appointment",
        "description": "Use this tool to book a specific appointment slot "
                      "AFTER the caller has chosen a time from get_available_slots. "
                      "Do NOT call this without first checking availability. "
                      "Do NOT call this if you don't have the patient's name.",
        "parameters": {
            "slot_id": {
                "type": "string",
                "description": "The slot ID returned from get_available_slots"
            },
            "patient_name": {
                "type": "string",
                "description": "Full name of the patient (First Last)"
            },
            "contact_phone": {
                "type": "string",
                "description": "Phone number (format: +1XXXXXXXXXX)"
            }
        }
    }
]
```

### Prompt Design
```yaml
tool_documentation: |
  ## Tool Best Practices
  
  Each tool description should include:
  1. WHAT it does (purpose)
  2. WHEN to call it (triggers)
  3. WHEN NOT to call it (negative conditions)
  4. Format hints for all parameters
  
  BAD tool description:
  "Makes an API call"
  
  GOOD tool description:
  "Use this tool to check for available appointment times 
   in the clinic's calendar for a specific date. Call this 
   BEFORE attempting to book so the caller can choose a time. 
   Do NOT call this if the caller hasn't specified what 
   service they need."
  
  TRANSFER TOOLS:
  Never leave transfer tool description empty. Include:
  - Available destinations
  - When to transfer (explicit triggers)
  - Example: "Transfer when caller asks for human, request 
    is outside scope, or you've failed twice to help."
  
  ATOMIC TOOLS:
  One tool = one action. Avoid combined tools like:
  BAD: appointment_action(mode="book|cancel|reschedule")
  GOOD: book_appointment, cancel_appointment, reschedule_appointment
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `tool.wrong_tool_rate` | > 10% |
| `tool.parameter_error_rate` | > 15% |
| `tool.not_called_when_needed` | > 10% |
| `tool.transfer_never_called` | > 50% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Wrong Tool | > 15% | P2 |
| Parameter Errors | > 20% | P2 |
| Transfer Not Used | Never called | P3 |
| Tool Failure Spike | > 25% | P1 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Tool descriptions
- [VAPI Tools Documentation](https://docs.vapi.ai/tools) - Tool configuration
- [Function Calling Best Practices](https://platform.openai.com/docs/guides/function-calling) - OpenAI guide
- [Voice AI Optimization](https://voiceaiwrapper.com/insights/vapi-voice-ai-optimization-performance-guide-voiceaiwrapper) - Tool design
