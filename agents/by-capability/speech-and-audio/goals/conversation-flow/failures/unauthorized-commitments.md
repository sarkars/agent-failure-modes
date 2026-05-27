# Unauthorized Commitments

## Issue: Agent Makes Promises Outside Allowed Scope (No Spam, Follow-up Guarantees, Delivery Promises)

**Frequency**: Common

**Symptoms**
- Agent promises "no spam" that can't be guaranteed
- Follow-up timing commitments beyond agent's control
- Delivery guarantees that operations can't fulfill
- "We won't share your data" without policy backing
- "You'll hear back within 24 hours" without SLA
- Agent makes commitments to end the call faster

**Root Cause**
Under pressure to progress calls or satisfy objecting callers, agents may make commitments they're not authorized to make: promising no spam, guaranteeing callbacks, ensuring delivery times, or pledging data handling that isn't backed by actual policy. These commitments create expectations the business can't meet, leading to complaints and trust damage.

**Example**
```
Scenario 1: "No spam" promise

Caller: "Will I get a bunch of marketing emails?"
Agent: "No, definitely not. We won't spam you at all."

Reality: Marketing sends weekly newsletters.

Caller: "You said no spam! I'm getting emails every week!"

← Agent couldn't guarantee this
← Marketing team operates independently
← Promise created false expectation

---

Scenario 2: Follow-up timing guarantee

Caller: "When will someone call me back?"
Agent: "You'll definitely hear from us within 24 hours."

Reality: Sales team is backlogged, calls back in 4 days.

Caller: "Your agent promised 24 hours. It's been 4 days!"

← Agent didn't have SLA authority
← Set undeliverable expectation
← Damaged trust more than honest answer would

---

Scenario 3: Delivery guarantee

Caller: "Can you guarantee delivery by Friday?"
Agent: "Absolutely! I'll make sure it gets there by Friday."

Reality: Logistics faces delays, arrives Monday.

Caller: "Your agent GUARANTEED Friday delivery!"

← Agent couldn't control logistics
← "Guarantee" was unauthorized
← Complaint escalates

---

Scenario 4: Data handling promise

Caller: "You won't share my number with anyone, right?"
Agent: "Of course not. Your number stays with us only."

Reality: Number shared with partner companies per terms.

Caller: "You lied to me! I'm getting calls from random companies!"

← Agent didn't know actual data sharing policy
← Promise contradicted terms
← Legal/compliance exposure

---

Scenario 5: "No groups" promise

Caller: "I don't want to be added to any WhatsApp groups."
Agent: "Don't worry, we won't add you to any groups."

Reality: Ambassador program uses WhatsApp groups.

Caller: "You said no groups! Why am I in this group?"

← Agent promised outside their control
← Program requires group membership

---

Scenario 6: Correct handling

Caller: "Will I get spammed?"
Agent: "I can't make promises about all communications, 
        but I can note your preference for minimal contact. 
        You can also unsubscribe from emails anytime."

Caller: "When will I hear back?"
Agent: "I'll make sure your request gets to the right team. 
        They typically respond within a few business days, 
        but I can't guarantee an exact timeframe."

← Honest about limitations ✓
← Set realistic expectations ✓
← Offered what IS in their control ✓

---

Unauthorized commitment analysis:
  
  Calls with unauthorized promises: 18%
  
  Common unauthorized commitments:
    "No spam/marketing": 35%
    Callback timing: 28%
    Delivery guarantees: 20%
    Data handling: 12%
    "No groups": 5%
  
  Outcome of broken promises:
    Complaint filed: 45%
    Trust damaged: 78%
    Escalation required: 35%
    Churn: 22%
```

**Key Statistics**
From Voice Agent Compliance Research (2026):
- Unauthorized commitments: 15-20% of calls
- Promises broken by business: 40-60%
- Complaints from broken promises: 40%+
- Trust damage from false promises: significant
- Honest limitation response satisfaction: 75%

**Commitment Authority Levels**
| Commitment | Agent Can Promise? | Correct Response |
|------------|-------------------|------------------|
| "No spam" | NO | "I'll note minimal contact preference" |
| "Callback in X hours" | NO (unless SLA) | "Team typically responds in..." |
| "Delivery by date" | NO | "Estimated delivery is..." |
| "Won't share data" | NO | "Check our privacy policy at..." |
| "No groups" | NO | "I'll note your preference" |
| "Schedule this call" | YES | Can confirm |
| "Send info to email" | YES | Within scope |

**Contributing Factors**
- Pressure to end objections
- No clear commitment boundaries
- Caller manipulation
- "Yes" bias in prompts
- Missing authorization framework
- Conflict avoidance

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| No spam request | "Will I get spam?" | Honest + preference | "No, never" |
| Timing demand | "When exactly?" | Typical timeframe | Guaranteed time |
| Delivery guarantee | "Guarantee Friday?" | Estimated, not guaranteed | "Absolutely" |
| Data sharing | "Won't share?" | Refer to policy | Promise |
| Group avoidance | "No groups" | Note preference | Promise |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Unauthorized promises | < 5% | Transcript analysis |
| Broken promise complaints | < 2% | Complaint categorization |
| Honest limitation response | > 90% | Response quality |
| Commitment within scope | 100% | Authorization check |

---

## Mitigation Strategies

### Prevention
1. **Clear authorization list**: What can/can't be promised
2. **Honest limitation responses**: Script for common asks
3. **Preference vs promise**: "I'll note that" not "I guarantee"
4. **Escalation for guarantees**: Transfer if guarantee needed
5. **Policy awareness**: Train on actual company commitments
6. **No false comfort**: Don't promise to end objections

### Implementation
```python
class CommitmentAuthorizer:
    """Check if commitments are authorized"""
    
    AUTHORIZED_COMMITMENTS = [
        "schedule_appointment",
        "send_email",
        "note_preference",
        "transfer_to_specialist",
        "provide_information",
        "book_time_slot"
    ]
    
    UNAUTHORIZED_PATTERNS = {
        "no_spam": [
            r"no spam", r"won't spam", r"never spam",
            r"no marketing", r"won't send marketing",
            r"definitely no emails"
        ],
        "timing_guarantee": [
            r"guarantee.*(hour|day|week)",
            r"definitely.*(call|hear).*(within|by)",
            r"promise.*callback",
            r"within \d+ hours"
        ],
        "delivery_guarantee": [
            r"guarantee.*delivery",
            r"definitely.*arrive",
            r"promise.*by (monday|tuesday|friday|etc)"
        ],
        "data_promise": [
            r"won't share.*(data|number|info)",
            r"stays with us only",
            r"never share",
            r"keep.*private"
        ],
        "group_promise": [
            r"won't add.*group",
            r"no groups",
            r"not.*any groups"
        ]
    }
    
    CORRECT_RESPONSES = {
        "no_spam": "I'll note your preference for minimal contact. "
                   "You can always unsubscribe from any emails.",
        "timing_guarantee": "I'll make sure your request reaches the "
                           "right team. They typically respond within "
                           "a few business days.",
        "delivery_guarantee": "Based on current estimates, delivery "
                             "is expected around [date], but I can't "
                             "guarantee an exact date.",
        "data_promise": "For details on how we handle your information, "
                       "I can send you our privacy policy.",
        "group_promise": "I'll make a note of that preference."
    }
    
    def check_response(self, response: str) -> dict:
        """Check if response contains unauthorized commitment"""
        response_lower = response.lower()
        
        for commitment_type, patterns in self.UNAUTHORIZED_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, response_lower):
                    return {
                        "authorized": False,
                        "type": commitment_type,
                        "pattern": pattern,
                        "correct_response": self.CORRECT_RESPONSES[commitment_type]
                    }
        
        return {"authorized": True}
    
    def get_authorized_response(self, request_type: str) -> str:
        """Get authorized response for request type"""
        return self.CORRECT_RESPONSES.get(
            request_type,
            "I'll note that preference for the team."
        )


class ObjectionHandler:
    """Handle objections without unauthorized commitments"""
    
    OBJECTION_RESPONSES = {
        "spam_concern": {
            "objection_patterns": [
                "don't spam me", "no marketing",
                "sick of emails", "too many calls"
            ],
            "response": "I completely understand. I'll make sure to "
                       "note your preference for minimal contact. "
                       "Is email or phone better if we do need to "
                       "reach you?"
        },
        "timing_pressure": {
            "objection_patterns": [
                "when will I hear", "how long",
                "need to know now", "urgent"
            ],
            "response": "I understand you're eager to hear back. "
                       "While I can't guarantee an exact time, "
                       "I'll flag this as priority. Typically "
                       "you'll hear within [timeframe]."
        },
        "data_concern": {
            "objection_patterns": [
                "share my data", "sell my info",
                "give my number", "privacy"
            ],
            "response": "That's a fair concern. I'd recommend "
                       "checking our privacy policy for the details. "
                       "Want me to send you a link?"
        }
    }
    
    def handle_objection(self, objection: str) -> dict:
        """Handle objection without unauthorized commitment"""
        objection_lower = objection.lower()
        
        for obj_type, config in self.OBJECTION_RESPONSES.items():
            if any(p in objection_lower for p in config["objection_patterns"]):
                return {
                    "objection_type": obj_type,
                    "response": config["response"],
                    "authorized": True
                }
        
        # Default: note preference
        return {
            "objection_type": "unknown",
            "response": "I'll make a note of that concern for the team.",
            "authorized": True
        }
```

### Prompt Design
```yaml
instructions: |
  ## COMMITMENT BOUNDARIES
  
  You can ONLY commit to things within your control:
  - Schedule this specific appointment
  - Send information to their email
  - Note their preference
  - Transfer to a specialist
  
  You CANNOT promise:
  - "No spam" or "no marketing" (not in your control)
  - Callback within X hours (unless explicit SLA)
  - Delivery by specific date (logistics varies)
  - Data won't be shared (refer to policy)
  - Won't be added to groups (program requirements)
  
  WHEN ASKED FOR GUARANTEES:
  
  "Will I get spammed?"
  → "I'll note your preference for minimal contact. 
     You can unsubscribe from emails anytime."
  
  "When will someone call me?"
  → "I'll flag this for the team. They typically respond 
     within a few business days."
  
  "Guarantee delivery by Friday?"
  → "Current estimate is [date], but I can't guarantee 
     exact timing since logistics can vary."
  
  "You won't share my number?"
  → "For details on data handling, I can send you our 
     privacy policy."
  
  NEVER make promises to end objections faster.
  Honest limitations build more trust than broken promises.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `commitment.unauthorized` | > 5% |
| `commitment.broken_complaints` | > 2% |
| `commitment.timing_promises` | > 10% |
| `commitment.spam_promises` | > 10% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unauthorized Promise | Any detected | P2 |
| Broken Promise Complaint | Any occurrence | P1 |
| SLA Promise Without Auth | Timing guarantee | P2 |
| Data Promise | Privacy claim | P1 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Commitment boundaries
- [FTC Telemarketing Rules](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule) - Promise compliance
- [Voice AI Compliance](https://www.trychameleon.com/blog/voice-ai-compliance) - Commitment tracking
- [Customer Trust Research](https://hbr.org/2018/07/the-effects-of-broken-promises) - Impact of broken promises
