# Unnecessary Data Collection

## Issue: Agent Requests Personal Information Beyond What's Needed

**Frequency**: Occasional

**Symptoms**
- Agent asks for name when not required
- Collects email when only WhatsApp needed
- Requests detailed personal info for simple tasks
- Asks for information already in context
- Multiple verification questions before simple action
- Data collection feels interrogative

**Root Cause**
Agents sometimes follow data collection patterns from traditional forms or CRM requirements without considering call context. In voice, every unnecessary question adds friction and reduces completion. Asking for name, email, age, or detailed info when only WhatsApp permission is needed creates suspicion and drop-off.

**Example**
```
Scenario 1: Name not needed

Agent: "Before we continue, can I get your name?"
Caller: "Why do you need my name?"
Agent: "Just for our records. So, what's your name?"

← Name wasn't required for the task
← Created unnecessary friction
← Caller now suspicious

Better: Don't ask for name at all

---

Scenario 2: Already in context

[Outbound call to known phone number]
Agent: "Can you confirm your phone number?"
Caller: "You just called me..."
Agent: "Yes, but I need to verify for our records."

← Number is already known from the call
← Verification feels bureaucratic

Better: Only verify if they give alternate WhatsApp

---

Scenario 3: Over-collection

Task: Get WhatsApp permission for playbook

Agent: "Great! Can I get your full name, email address, 
        college name, year of study, and WhatsApp number?"

← Task only needs WhatsApp permission
← Multiple unnecessary fields requested
← Feels like filling a form, not a conversation

Better: "Which college?" + "WhatsApp okay for the playbook?"

---

Scenario 4: Unnecessary verification

Caller: "Yes, you can WhatsApp me"
Agent: "Great! To confirm, you're authorizing Zapp Chess 
        to send you messages on WhatsApp at the number 
        ending in 3210, is that correct?"

← Over-formal verification
← Makes simple permission feel legal

Better: "Cool, same number or different WhatsApp?"

---

Scenario 5: Sequential interrogation

Agent: "What's your college?"
Agent: "What year are you in?"
Agent: "What's your major?"
Agent: "How did you hear about us?"
Agent: "Have you participated in tournaments before?"

← Each question adds friction
← Feels like an interrogation
← Most not needed for task

---

Data collection analysis (500 calls):
  Only necessary data requested: 234 (47%)
  1-2 extra fields: 156 (31%)
  3+ extra fields: 78 (16%)
  Full form approach: 32 (6%)
  
  Completion by collection level:
    Minimal (necessary only): 72% completion
    Light extra (1-2 fields): 58% completion
    Heavy (3+ fields): 34% completion
```

**Key Statistics**
From Voice Data Collection Research (2026):
- Unnecessary field requests: 40-60%
- Drop-off per extra question: 8-12%
- "Why do you need that?" rate: 15-25%
- Minimal collection → completion: +25-35%
- Trust reduction from over-collection: 20-30%

**Over-Collection Types**
| Data | Usually Needed? | When Actually Needed |
|------|-----------------|---------------------|
| Name | Rarely | Legal/financial tasks |
| Email | Sometimes | Email-based follow-up |
| Phone | Context has it | If different WhatsApp |
| Full address | Rarely | Delivery |
| DOB/Age | Rarely | Age-gated services |
| ID numbers | Rarely | Verification tasks |

**Contributing Factors**
- CRM field requirements carried to voice
- Form-filling mindset in design
- No friction analysis per field
- Verification theater (not actual need)
- Compliance over-interpretation
- "Good to have" data collection

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Name request | Simple qualification | Don't ask | Asks for name |
| Phone verify | Outbound call | Don't verify | Asks to confirm |
| Email request | WhatsApp task | Don't ask | Asks for email |
| Multiple fields | Single action | 1-2 questions | 3+ fields |
| Context data | Data already known | Don't re-ask | Asks again |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Extra fields requested | 0 | Beyond task need |
| Questions per task | < 3 | Count questions |
| "Why do you need" rate | < 5% | User pushback |
| Completion vs questions | Track correlation | Drop per question |

---

## Mitigation Strategies

### Prevention
1. **Minimal collection principle**: Only ask what's needed for this task
2. **Context awareness**: Don't ask for data already in context
3. **Question budget**: Max questions per call type
4. **Friction analysis**: Measure drop-off per field
5. **Progressive collection**: Get essentials first, details later
6. **Skip optional**: Don't ask "nice to have" fields

### Implementation
```python
class DataCollectionMinimizer:
    """Ensure only necessary data is collected"""
    
    TASK_REQUIREMENTS = {
        "qualification_call": {
            "required": ["interest", "whatsapp_permission"],
            "optional": ["college_name", "whatsapp_number"],
            "never": ["name", "email", "age", "address", 
                     "phone_verification"]
        },
        "support_call": {
            "required": ["issue_description"],
            "optional": ["order_number"],
            "never": ["name", "email"]  # Already in context
        },
        "appointment": {
            "required": ["preferred_time"],
            "optional": ["alternate_time"],
            "never": ["full_address", "insurance"]  # Unless needed
        }
    }
    
    def __init__(self, task_type: str, context: dict):
        self.requirements = self.TASK_REQUIREMENTS.get(
            task_type, {"required": [], "optional": [], "never": []}
        )
        self.context = context  # Data already available
        self.collected = {}
    
    def should_ask(self, field: str) -> bool:
        """Determine if field should be asked"""
        # Never ask for "never" fields
        if field in self.requirements["never"]:
            return False
        
        # Don't ask for data already in context
        if field in self.context and self.context[field]:
            return False
        
        # Don't ask again if already collected
        if field in self.collected:
            return False
        
        # Required fields: yes
        if field in self.requirements["required"]:
            return True
        
        # Optional: only if conversation naturally leads there
        return False
    
    def get_question_budget(self) -> int:
        """Get remaining question budget"""
        required_remaining = len([
            f for f in self.requirements["required"]
            if f not in self.collected and f not in self.context
        ])
        return required_remaining + 1  # +1 for one optional
    
    def validate_collection_plan(self, 
                                  planned_questions: list) -> dict:
        """Validate planned data collection"""
        issues = []
        
        for question in planned_questions:
            field = self.extract_field(question)
            
            if field in self.requirements["never"]:
                issues.append({
                    "field": field,
                    "issue": "Never collect this field",
                    "severity": "high"
                })
            
            if field in self.context:
                issues.append({
                    "field": field,
                    "issue": "Already in context",
                    "severity": "medium"
                })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "question_count": len(planned_questions),
            "budget": self.get_question_budget()
        }


class FrictionAnalyzer:
    """Analyze friction from data collection"""
    
    DROP_RATES = {
        # Estimated drop-off per question type
        "name": 0.15,
        "email": 0.12,
        "phone": 0.10,
        "address": 0.20,
        "dob": 0.18,
        "verification": 0.08,
        "optional_general": 0.08
    }
    
    def estimate_drop_off(self, questions: list) -> float:
        """Estimate cumulative drop-off from questions"""
        completion = 1.0
        
        for q in questions:
            field_type = self.classify_question(q)
            drop_rate = self.DROP_RATES.get(field_type, 0.08)
            completion *= (1 - drop_rate)
        
        return 1 - completion  # Total drop-off
    
    def recommend_removal(self, questions: list, 
                           target_completion: float) -> list:
        """Recommend questions to remove to hit target"""
        current = 1 - self.estimate_drop_off(questions)
        
        if current >= target_completion:
            return []  # Already meeting target
        
        # Sort by drop rate, recommend removing highest
        scored = [(q, self.DROP_RATES.get(
            self.classify_question(q), 0.08
        )) for q in questions]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        removals = []
        for q, rate in scored:
            if q not in ["interest", "whatsapp_permission"]:
                removals.append(q)
                current = current / (1 - rate)
                if current >= target_completion:
                    break
        
        return removals
```

### Prompt Design
```yaml
instructions: |
  ## DATA COLLECTION RULES
  
  ONLY collect what you need for THIS task:
  - WhatsApp permission: yes/no
  - Same number or different WhatsApp
  - College name (optional)
  
  DO NOT ask for:
  - Caller's name (you don't need it)
  - Email address (WhatsApp is the channel)
  - Phone number (you already called them)
  - Age, year of study, major, etc.
  - "How did you hear about us"
  
  DO NOT verify data already in context:
  - Don't ask "Can you confirm your number?"
  - You called them—you have the number
  
  FRICTION BUDGET: 
  - Max 3 questions total
  - Required: interest + WhatsApp permission + number confirm
  - Optional: college (if natural)
  
  If not strictly needed for playbook delivery, don't ask.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `collection.extra_fields` | > 0 |
| `collection.questions_asked` | > 4 |
| `collection.pushback_rate` | > 10% |
| `collection.completion_correlation` | Monitor |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unnecessary Name Ask | Any occurrence | P3 |
| Over-Collection | > 4 questions | P2 |
| High Pushback | "Why do you need" > 15% | P2 |

---

## References

- [Data Minimization Principles](https://gdpr-info.eu/art-5-gdpr/) - GDPR Article 5
- [Voice UX Friction](https://www.beconversive.com/blog/voice-ai-challenges) - Question impact
- [Conversational Form Design](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Collection patterns
- [Privacy by Design](https://ico.org.uk/for-organisations/guide-to-data-protection/) - Minimal collection
