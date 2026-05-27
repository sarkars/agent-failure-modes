# Scope Boundary Violations

## Issue: Agent Answers Questions or Provides Information Outside Approved Knowledge

**Frequency**: Very Common

**Symptoms**
- Agent invents program details not in instructions
- Questions about process answered with fabricated specifics
- Commitments made beyond agent's authority
- Future actions promised without backing
- Operational details guessed instead of deferred

**Root Cause**
LLMs are trained to be helpful and provide complete answers. When callers ask questions outside the agent's approved knowledge scope, the model's default behavior is to generate a plausible answer rather than acknowledge limits. Without explicit scope boundaries and deflection strategies, agents confidently provide fabricated or unauthorized information.

**Example**
```
Scenario 1: Process details fabricated

Approved knowledge: "Ambassador program with perks"
NOT in scope: Selection process, timeline, duties

Caller: "So how does the selection work?"
Agent: "We review applications and select based on your 
        college reach and social media presence. You should 
        hear back within a week."

← Fabricated selection criteria and timeline

Correct: "The playbook covers the full process—can I 
         share it on WhatsApp?"

---

Scenario 2: Commitment beyond authority

Caller: "Will there be any weekly meetings?"
Agent: "No, there won't be any mandatory meetings. 
        It's very flexible, you just run one tournament."

← Made commitment about meeting policy (not authorized)

Correct: "The playbook explains the format and what's 
         involved. Want me to share it?"

---

Scenario 3: Operational details guessed

Caller: "How do I get the creatives for the tournament?"
Agent: "We'll add you to a WhatsApp group where the team 
        shares all materials. You'll also get a drive link."

← Invented distribution method

Correct: "That's covered in the playbook—shall I share it?"

---

Scenario 4: Future actions promised

Caller: "Will someone call me after I read the playbook?"
Agent: "Yes, someone from the team will follow up within 
        24-48 hours to answer any questions."

← Promised follow-up process (not authorized)

Correct: "This call is just to check interest and share 
         the playbook. The playbook has next steps."

---

Scenario 5: Eligibility invented

Caller: "Do I need to know chess to be an ambassador?"
Agent: "Not at all! You don't need to know chess. We just 
        need someone who can promote the tournament."

← Made eligibility claim not in instructions

Correct: "The playbook covers what's involved—want to 
         take a look?"

---

Scope violation analysis (500 calls):
  Questions outside scope: 312
  Correctly deferred: 187 (60%)
  Fabricated answer: 94 (30%)
  Partial fabrication: 31 (10%)
  
  Most common fabrications:
    - Selection process: 25%
    - Timeline: 22%
    - Duties/requirements: 20%
    - Future contact: 18%
    - Eligibility: 15%
```

**Key Statistics**
From Voice Agent Scope Research (2026):
- Out-of-scope questions: 40-60% of calls
- Fabricated answers: 25-40%
- Correct deferrals: 50-70%
- User complaints from wrong info: 15-25%
- Commitment violations: 10-20%

**Scope Violation Types**
| Type | Example | Risk |
|------|---------|------|
| Process details | Selection criteria | False expectations |
| Timeline | "Hear back in a week" | Broken promise |
| Eligibility | "No chess knowledge needed" | Wrong participants |
| Commitments | "No mandatory meetings" | Contractual issue |
| Future actions | "Team will follow up" | Undelivered promise |

**Contributing Factors**
- LLM helpfulness training
- No explicit "don't know" behavior
- Scope boundaries buried in long prompts
- Deflection phrasing not provided
- Pressure to answer quickly
- No post-response scope check

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Selection process | "How do you select?" | Defer to playbook | Any specifics |
| Timeline | "When will I hear back?" | Defer to playbook | Any timeframe |
| Requirements | "What do I need to do?" | Defer to playbook | Duty list |
| Future contact | "Will you call again?" | Explain this call only | Promise of follow-up |
| Eligibility | "Do I need to be good at X?" | Defer to playbook | Yes/no answer |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Scope adherence | > 95% | Answers within approved knowledge |
| Correct deferral | > 90% | Out-of-scope → playbook redirect |
| Fabrication rate | 0% | Invented details detected |
| Unauthorized commitments | 0% | Promises beyond scope |

---

## Mitigation Strategies

### Prevention
1. **Explicit scope definition**: List exactly what agent knows
2. **Deflection templates**: Provide exact phrases for out-of-scope
3. **"I don't know" training**: Reinforce uncertainty expression
4. **Scope-first checking**: Check scope before generating answer
5. **Commitment blocklist**: Never promise specific actions
6. **Post-response validation**: Check for scope violations

### Implementation
```python
class ScopeManager:
    """Manage agent knowledge boundaries"""
    
    APPROVED_KNOWLEDGE = {
        "program_type": "Campus Ambassador program",
        "basic_role": "Help run one chess tournament at college",
        "perks_high_level": [
            "Certificate",
            "Trophy", 
            "T-shirt (tier-based)",
            "LinkedIn founder shoutout (top tier)",
            "500 rupee campus winner prize"
        ],
        "support": "Creatives provided",
        "details_source": "Playbook"
    }
    
    OUT_OF_SCOPE = [
        "selection_process",
        "selection_criteria", 
        "timeline",
        "response_time",
        "duties_specific",
        "requirements_detailed",
        "eligibility_detailed",
        "meeting_requirements",
        "weekly_commitment",
        "group_membership",
        "future_contact",
        "follow_up_process",
        "onboarding_steps"
    ]
    
    NEVER_SAY = [
        "you don't need to",
        "there won't be",
        "we'll call you",
        "team will reach out",
        "you'll hear back",
        "within X days",
        "no mandatory",
        "very flexible",
        "we'll add you to"
    ]
    
    DEFLECTION_TEMPLATE = (
        "The playbook covers {topic}—can I share it on WhatsApp?"
    )
    
    def is_in_scope(self, question: str) -> bool:
        """Check if question is within approved knowledge"""
        out_of_scope_triggers = [
            "how does selection",
            "when will",
            "how long",
            "what do I need to do",
            "will there be",
            "do I need to",
            "will you call",
            "will someone contact",
            "what happens after",
            "is there a group",
            "weekly",
            "mandatory"
        ]
        
        question_lower = question.lower()
        return not any(trigger in question_lower 
                       for trigger in out_of_scope_triggers)
    
    def get_deflection(self, question: str) -> str:
        """Generate appropriate deflection for out-of-scope question"""
        # Map question types to topic phrases
        topic_map = {
            "selection": "the selection process",
            "when": "the timeline",
            "what do I": "what's involved",
            "do I need": "the requirements",
            "will there": "the format",
            "group": "how it works",
            "weekly": "the commitment level",
            "after": "the next steps"
        }
        
        question_lower = question.lower()
        for trigger, topic in topic_map.items():
            if trigger in question_lower:
                return self.DEFLECTION_TEMPLATE.format(topic=topic)
        
        # Generic deflection
        return "The playbook explains all of that—want me to share it?"
    
    def validate_response(self, response: str) -> dict:
        """Check response for scope violations"""
        violations = []
        
        response_lower = response.lower()
        for phrase in self.NEVER_SAY:
            if phrase in response_lower:
                violations.append({
                    "type": "forbidden_phrase",
                    "phrase": phrase,
                    "severity": "high"
                })
        
        # Check for specific commitments
        commitment_patterns = [
            r"within \d+ (days|hours|weeks)",
            r"by (monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
            r"(we'll|we will|team will) (call|contact|reach|send)",
            r"you('ll| will) (get|receive|hear)"
        ]
        
        for pattern in commitment_patterns:
            if re.search(pattern, response_lower):
                violations.append({
                    "type": "unauthorized_commitment",
                    "pattern": pattern,
                    "severity": "critical"
                })
        
        return {
            "valid": len(violations) == 0,
            "violations": violations
        }


class ResponseGenerator:
    """Generate responses within scope"""
    
    def __init__(self):
        self.scope = ScopeManager()
    
    def generate(self, question: str, context: dict) -> str:
        """Generate response, checking scope first"""
        
        # Check if in scope
        if not self.scope.is_in_scope(question):
            return self.scope.get_deflection(question)
        
        # Generate from approved knowledge
        response = self.generate_from_knowledge(question, context)
        
        # Validate before returning
        validation = self.scope.validate_response(response)
        if not validation["valid"]:
            # Fall back to deflection
            return self.scope.get_deflection(question)
        
        return response
```

### Prompt Design
```yaml
instructions: |
  ## KNOWLEDGE BOUNDARIES (CRITICAL)
  
  You know ONLY:
  - This is a Campus Ambassador program for Zapp Chess
  - Role: Help run one online chess tournament at their college
  - Perks: Certificate, trophy, T-shirt (tier), 500 rupee winner prize,
           LinkedIn founder shoutout (top tier)
  - Support: Creatives provided
  - Details: In the playbook
  
  You DO NOT know (defer ALL questions about):
  - Selection process or criteria
  - Timeline or response time
  - Specific duties or requirements
  - Eligibility details
  - Meeting/group requirements
  - Weekly commitment level
  - What happens after reading playbook
  - Whether team will call/contact/follow up
  - Onboarding process
  
  For ANY question outside your knowledge:
  → "The playbook covers that—can I share it on WhatsApp?"
  
  NEVER say:
  - "You don't need to..."
  - "There won't be..."
  - "Team will..."
  - "You'll hear back..."
  - Any timeline (days, hours, weeks)
  - Any commitment about future actions
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `scope.violation.rate` | > 5% |
| `scope.fabrication.detected` | > 0% |
| `scope.commitment.unauthorized` | > 0% |
| `scope.deferral.rate` | < 80% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Fabrication Detected | Any occurrence | P1 |
| Unauthorized Commitment | Any occurrence | P1 |
| Low Deferral Rate | deferral < 70% | P2 |
| Scope Violation Spike | violations > 10% | P2 |

---

## References

- [LLM Hallucination Research](https://arxiv.org/abs/2311.05232) - Fabrication patterns
- [Conversational Boundaries](https://www.beconversive.com/blog/voice-ai-challenges) - Scope design
- [Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Over-promising
- [Controllable Generation](https://arxiv.org/abs/2201.05337) - Boundary enforcement
