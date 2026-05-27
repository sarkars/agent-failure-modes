# Agent Self-Attribution Errors

## Issue: Agent Claims It Will Perform Actions Beyond Its Capabilities

**Frequency**: Common

**Symptoms**
- Agent says "I'll send you..." when it cannot send anything
- "I'll make sure..." promises about team actions
- Implies personal follow-up it won't perform
- Claims to be scheduling, booking, or processing
- Uses "I" for team actions creating false expectations
- Confuses permission capture with action commitment

**Root Cause**
Voice agents capture information and permissions, but rarely execute follow-up actions directly. When using first-person language ("I'll send the playbook"), the agent implies personal capability and commitment. Callers expect the agent—not some backend process—to fulfill the promise. This creates accountability gaps and broken expectations.

**Example**
```
Scenario 1: Send attribution error

Agent: "Great! I'll send you the playbook on WhatsApp 
        right after this call."

Reality: Agent captures permission; separate system sends
← Agent cannot send anything
← "I'll send" creates false personal commitment

Better: "Can the team share the playbook on WhatsApp?"

---

Scenario 2: Follow-up attribution

Agent: "I'll make sure someone reaches out to you 
        by tomorrow."

Reality: Agent has no control over team follow-up timing
← Promises specific timeline agent can't guarantee
← Creates expectation of personal accountability

Better: "The next steps are in the playbook."

---

Scenario 3: Scheduling attribution

Agent: "I'll schedule a callback for you this evening."

Reality: Agent captures callback preference; system handles
← Implies agent is performing the scheduling
← If callback doesn't happen, caller blames agent

Better: "Noted—evening callback. The team will call back."

---

Scenario 4: Processing attribution

Agent: "I'll process your application and you'll hear 
        back within a week."

Reality: Agent captures data; review is separate process
← Agent has no role in processing
← Timeline promise it cannot keep

Better: "The playbook explains next steps."

---

Scenario 5: "I" vs "The team"

Bad: "I'll add you to the WhatsApp group."
Good: "The team will handle follow-up."

Bad: "I'll make sure you get the materials."
Good: "The playbook has all the details."

Bad: "I'll personally follow up."
Good: "Someone from the team may reach out."

---

Attribution error analysis (500 calls):
  "I'll send/share" used: 187 (37%)
  "I'll make sure" used: 89 (18%)
  "I'll process/schedule" used: 45 (9%)
  
  Total false self-attribution: 64%
  
  Follow-up complaints traced to attribution:
    "You said you'd send it": 23%
    "You promised to call back": 15%
    "You said you'd process it": 8%
```

**Key Statistics**
From Voice Agent Attribution Research (2026):
- False "I'll do X" statements: 50-70%
- Caller expectation mismatch: 40-55%
- Complaints from unmet "I" promises: 20-30%
- Trust reduction from broken attribution: 25%
- "I" vs "team" satisfaction difference: +15% for "team"

**Attribution Error Types**
| Statement | Reality | Risk |
|-----------|---------|------|
| "I'll send" | System sends | Broken promise |
| "I'll schedule" | System schedules | Wrong accountability |
| "I'll make sure" | No control | False assurance |
| "I'll process" | Separate team | Timeline mismatch |
| "I'll follow up" | Won't happen | Direct lie |

**Contributing Factors**
- First-person prompting style
- Conversational warmth using "I"
- No clear capability boundaries
- LLM defaults to "I" language
- Prompt doesn't specify attribution rules
- Agent/team/system roles conflated

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Send action | After WhatsApp permission | "Team can share" | "I'll send" |
| Follow-up | Asked about next steps | "Playbook explains" | "I'll make sure" |
| Scheduling | Callback requested | "Team will call" | "I'll schedule" |
| Processing | Asked about application | "Details in playbook" | "I'll process" |
| Any promise | Closing | No "I'll" commitments | Any "I'll" action |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| False "I'll" rate | 0% | Regex for "I'll" + action |
| Team attribution | > 95% | "Team/someone" vs "I" |
| Capability boundary | 100% | No impossible promises |
| Follow-up complaints | < 5% | "You said you'd..." |

---

## Mitigation Strategies

### Prevention
1. **Ban "I'll send/do"**: Never use for actions agent can't perform
2. **Team attribution**: "The team can..." instead of "I can..."
3. **Passive voice**: "It will be shared" vs "I'll share it"
4. **Capability clarity**: Agent captures, doesn't execute
5. **No timeline promises**: Never commit to "by tomorrow"
6. **Permission framing**: "Can I get permission" not "I'll send"

### Implementation
```python
class AttributionCorrector:
    """Correct self-attribution errors in responses"""
    
    FORBIDDEN_SELF_ACTIONS = [
        r"i('ll| will) send",
        r"i('ll| will) share",
        r"i('ll| will) schedule",
        r"i('ll| will) process",
        r"i('ll| will) make sure",
        r"i('ll| will) follow up",
        r"i('ll| will) add you",
        r"i('ll| will) book",
        r"i('ll| will) arrange",
        r"i('ll| will) personally",
    ]
    
    CORRECTIONS = {
        r"i('ll| will) send (you |it |the )?(on whatsapp|the playbook)?":
            "the team can share",
        r"i('ll| will) make sure (you |someone )?":
            "",  # Remove entirely
        r"i('ll| will) follow up":
            "someone from the team may reach out",
        r"i('ll| will) schedule (a |your )?callback":
            "the team will call back",
        r"i('ll| will) process":
            "that'll be reviewed",
        r"i('ll| will) add you to":
            "you may be added to",
    }
    
    def check_attribution(self, response: str) -> list:
        """Find self-attribution errors"""
        errors = []
        response_lower = response.lower()
        
        for pattern in self.FORBIDDEN_SELF_ACTIONS:
            if re.search(pattern, response_lower):
                errors.append({
                    "pattern": pattern,
                    "severity": "high"
                })
        
        return errors
    
    def correct(self, response: str) -> str:
        """Correct self-attribution to team attribution"""
        result = response
        
        for pattern, replacement in self.CORRECTIONS.items():
            result = re.sub(pattern, replacement, result, 
                           flags=re.IGNORECASE)
        
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    def reframe_as_permission(self, response: str) -> str:
        """Reframe sending as permission capture"""
        # "I'll send the playbook" → "Can the team share the playbook?"
        send_patterns = [
            (r"i('ll| will) send (you )?the playbook",
             "can the team share the playbook on WhatsApp"),
            (r"i('ll| will) share (the )?details",
             "want me to note down that the team can share details"),
        ]
        
        result = response
        for pattern, replacement in send_patterns:
            result = re.sub(pattern, replacement, result,
                           flags=re.IGNORECASE)
        
        return result


class CapabilityBoundaryEnforcer:
    """Enforce agent capability boundaries"""
    
    AGENT_CAN = [
        "capture information",
        "ask questions",
        "explain program",
        "note preferences",
        "get permission"
    ]
    
    AGENT_CANNOT = [
        "send messages",
        "schedule callbacks",
        "process applications",
        "make decisions",
        "guarantee timelines",
        "follow up personally"
    ]
    
    def get_appropriate_framing(self, action: str) -> str:
        """Get correct framing for action"""
        framings = {
            "send_playbook": 
                "Can the team share the playbook on WhatsApp?",
            "schedule_callback":
                "Evening or weekend—when's better for a callback?",
            "process_application":
                "The playbook has next steps.",
            "follow_up":
                "The next steps are in the playbook.",
            "add_to_group":
                "The format is explained in the playbook."
        }
        return framings.get(action, "")
```

### Prompt Design
```yaml
instructions: |
  ## ATTRIBUTION RULES (CRITICAL)
  
  You capture information. You do NOT execute follow-up.
  
  NEVER SAY:
  - "I'll send you..."
  - "I'll share..."  
  - "I'll make sure..."
  - "I'll follow up..."
  - "I'll schedule..."
  - "I'll process..."
  - "I'll personally..."
  
  INSTEAD SAY:
  - "Can the TEAM share the playbook on WhatsApp?"
  - "The TEAM will handle follow-up."
  - "SOMEONE from the team may reach out."
  - "That's noted for the TEAM."
  - "The playbook has next steps."
  
  WHY: You cannot send messages, schedule calls, or process
  applications. Saying "I'll" creates false expectations.
  
  PERMISSION FRAMING:
  - You ask: "Can the team share X?"
  - You capture: "yes" or "no"
  - You do NOT: promise it will be sent
  
  TIMELINE:
  - Never promise "by tomorrow" or "within X days"
  - You don't control when the team acts
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `attribution.i_will.rate` | > 0% |
| `attribution.team.rate` | < 90% |
| `attribution.complaints` | > 5% |
| `attribution.timeline_promise` | > 0% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Self-Attribution Detected | Any "I'll send" | P2 |
| Timeline Promise | Any occurrence | P1 |
| Attribution Complaints | > 10% | P2 |

---

## References

- [Voice Agent Accountability](https://www.beconversive.com/blog/voice-ai-challenges) - Attribution design
- [Conversational AI Promises](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Commitment handling
- [Dialog System Design](https://arxiv.org/abs/2009.07261) - Role clarity
- [Agent Capability Boundaries](https://arxiv.org/abs/2106.07837) - What agents can/cannot do
