# Qualification Flow Violations

## Issue: Agent Skips Required Steps or Asks Questions Out of Sequence

**Frequency**: Common

**Symptoms**
- Permission requested before interest confirmed
- WhatsApp number asked before permission granted
- Closing before required information captured
- Multiple questions asked in single turn
- Steps repeated unnecessarily
- Qualification marked complete with missing data

**Root Cause**
Multi-step qualification flows have dependencies: interest before permission, permission before contact details. LLMs optimize for conversation efficiency and may combine questions, skip steps, or mark completion prematurely. Without explicit step tracking, the model loses track of what's been captured and what's still needed.

**Example**
```
Scenario 1: Permission before interest

Agent: "Hi, can I send you details on WhatsApp?"
← Asked permission before explaining program or checking interest

Correct flow: Explain → Check interest → Ask permission

---

Scenario 2: Combined question violation

Agent: "Can I send the playbook on WhatsApp, and 
        is this number okay for that?"

← Combined permission AND number confirmation in one question

Required: Ask permission first, then ask number in separate turn

---

Scenario 3: Skipped interest check

Agent: [Explains program]
Agent: "Which college are you at?"
← Jumped to college question without checking interest

Correct: "Does this sound interesting?" → If yes → "Which college?"

---

Scenario 4: Premature qualification

Caller: "Yeah sounds cool, you can WhatsApp me"
Agent: [Routes to qualified close]

← Missing: Confirmation whether same number or different number

Required: Permission captured ✓, but number confirmation missing ✗

---

Scenario 5: Repeated step

Turn 3 - Agent: "Can I share this on WhatsApp?"
Caller: "Yes"
Turn 5 - Agent: "So is it okay to send on WhatsApp?"

← Permission already captured, asked again unnecessarily

---

Flow compliance analysis (500 calls):
  Correct step sequence: 62%
  Skipped interest check: 18%
  Combined questions: 15%
  Premature close: 12%
  Repeated question: 8%
  
  Qualification completeness:
    All required fields: 71%
    Missing number confirmation: 15%
    Missing permission: 8%
    Missing college (optional): 40%
```

**Key Statistics**
From Voice Qualification Flow Research (2026):
- Step sequence compliance: 55-70%
- Combined question violations: 10-20%
- Premature qualification rate: 10-18%
- Repeated question rate: 5-12%
- Incomplete qualification pushed through: 15-25%

**Flow Violation Types**
| Type | Description | Impact |
|------|-------------|--------|
| Step skip | Missing required step | Incomplete data |
| Wrong order | Steps out of sequence | Confusion |
| Combined | Multiple questions per turn | Overwhelmed caller |
| Repeated | Same question asked twice | Annoyance |
| Premature close | Close before completion | Data loss |

**Contributing Factors**
- No explicit step state tracking
- LLM optimizes for efficiency
- Long instructions lose step sequence
- No validation before routing to close
- Implicit completion signals misread
- Caller responses span multiple steps

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Step order | Full conversation | Interest→Permission→Number | Any reorder |
| No combining | Permission turn | Single question | Multiple questions |
| No repeat | Already answered | Skip to next step | Same question again |
| Complete close | Qualified route | All fields populated | Any field missing |
| Interest gate | Before pitch | Must check interest | Skip to permission |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Step sequence | > 90% | Order of step transitions |
| Single question/turn | > 95% | Questions per agent turn |
| Repeat rate | < 3% | Same question asked twice |
| Complete qualification | > 95% | All required fields on close |

---

## Mitigation Strategies

### Prevention
1. **Explicit step tracking**: Track current step as conversation variable
2. **Step validation**: Check prerequisites before advancing
3. **Single-question enforcement**: Post-process to split combined questions
4. **Completion gate**: Validate all fields before close routing
5. **Captured-field tracking**: Log what's been captured, skip if present
6. **Step transition prompts**: Tell model exactly which step to execute

### Flow State Machine
```python
class QualificationFlow:
    """Enforce step sequence with validation"""
    
    STEPS = [
        "opening",
        "availability_check",
        "pitch",
        "interest_check",
        "college_capture",  # optional
        "permission_request",
        "number_confirmation",
        "close"
    ]
    
    REQUIRED_FOR_CLOSE = {
        "qualified": ["permission", "whatsapp_number"],
        "callback": ["callback_time"],
        "not_interested": [],
        "dnc": []
    }
    
    def __init__(self):
        self.current_step = "opening"
        self.captured = {}
        self.step_history = []
    
    def can_advance_to(self, target_step: str) -> tuple:
        """Check if we can advance to target step"""
        current_idx = self.STEPS.index(self.current_step)
        target_idx = self.STEPS.index(target_step)
        
        # Check for skips
        if target_idx > current_idx + 1:
            skipped = self.STEPS[current_idx + 1:target_idx]
            # Check if skipped steps are optional
            required_skipped = [s for s in skipped 
                               if not self.is_optional(s)]
            if required_skipped:
                return False, f"Cannot skip required steps: {required_skipped}"
        
        # Check prerequisites for specific steps
        prereqs = self.get_prerequisites(target_step)
        missing = [p for p in prereqs if p not in self.captured]
        if missing:
            return False, f"Missing prerequisites: {missing}"
        
        return True, None
    
    def get_prerequisites(self, step: str) -> list:
        """Get required captured data for step"""
        prereqs = {
            "permission_request": ["interest"],  # Must have interest
            "number_confirmation": ["permission"],  # Must have permission
            "close": []  # Depends on outcome
        }
        return prereqs.get(step, [])
    
    def is_optional(self, step: str) -> bool:
        return step in ["college_capture"]
    
    def advance_step(self, to_step: str) -> dict:
        """Advance to next step with validation"""
        can_advance, reason = self.can_advance_to(to_step)
        
        if not can_advance:
            return {
                "success": False,
                "error": reason,
                "stay_at": self.current_step
            }
        
        self.step_history.append(self.current_step)
        self.current_step = to_step
        
        return {
            "success": True,
            "current_step": to_step,
            "prompt_hint": self.get_step_prompt(to_step)
        }
    
    def capture_data(self, field: str, value: any) -> None:
        """Record captured data"""
        if field not in self.captured:
            self.captured[field] = value
        # Don't overwrite unless it's a correction
    
    def can_close(self, outcome: str) -> tuple:
        """Check if we have required data for this close type"""
        required = self.REQUIRED_FOR_CLOSE.get(outcome, [])
        missing = [f for f in required if f not in self.captured]
        
        if missing:
            return False, missing
        return True, []
    
    def get_step_prompt(self, step: str) -> str:
        """Get instruction for specific step"""
        prompts = {
            "interest_check": 
                "Ask ONE casual interest question. "
                "Do not ask about WhatsApp or permission yet.",
            "permission_request":
                "Ask ONLY for WhatsApp permission. "
                "Do not ask about the number yet.",
            "number_confirmation":
                "Ask ONLY whether same number or different number. "
                "Permission already captured."
        }
        return prompts.get(step, "")


class QuestionValidator:
    """Ensure single question per turn"""
    
    QUESTION_PATTERNS = [
        r'\?',
        r'^(can|could|would|do|does|is|are|what|which|how)',
        r'(okay|right|correct)\?'
    ]
    
    def count_questions(self, response: str) -> int:
        """Count number of questions in response"""
        # Simple: count question marks
        return response.count('?')
    
    def has_combined_questions(self, response: str) -> bool:
        """Check if response has multiple distinct questions"""
        question_count = self.count_questions(response)
        return question_count > 1
    
    def split_if_combined(self, response: str) -> list:
        """Split combined questions into separate turns"""
        if not self.has_combined_questions(response):
            return [response]
        
        # Split at question marks, keeping first question only
        parts = response.split('?')
        first_question = parts[0] + '?'
        
        return [first_question.strip()]
```

### Prompt for Step Enforcement
```yaml
instructions: |
  ## CONVERSATION STEPS (MUST FOLLOW IN ORDER)
  
  STEP 1: OPENING - Greet, remind about form, check availability
          → Only proceed if caller is available NOW
  
  STEP 2: PITCH - Brief hook about program (15 seconds max)
          → Let caller react before asking questions
  
  STEP 3: INTEREST CHECK - Ask ONE interest question
          → "Does this sound interesting?"
          → Wait for clear response before proceeding
  
  STEP 4: COLLEGE - Ask which college (OPTIONAL)
          → Skip if they don't want to share
  
  STEP 5: PERMISSION - Ask ONLY for WhatsApp permission
          → "Can the team share the playbook on WhatsApp?"
          → This is a SEPARATE question from number confirmation
  
  STEP 6: NUMBER CONFIRMATION - Ask ONLY after permission granted
          → "Is this same number okay, or different WhatsApp?"
          → NEVER combine with permission question
  
  ## RULES
  - Complete each step before moving to next
  - ASK ONLY ONE QUESTION PER TURN
  - Never ask permission before interest is confirmed
  - Never ask number before permission is granted
  - If a step was already completed, skip it
  
  Current step: {current_step}
  Captured data: {captured_fields}
```

### Detection & Response

1. **Flow-sequence-compliance audit with step-tracking logging**: For each call, log: {call_id, qualification_flow_sequence: [{ step_number, step_name, completed (Y/N), fields_captured: [], step_skipped (Y/N), combined_questions_asked (count) }], total_steps_required, steps_completed, steps_skipped, sequence_compliance_score (steps_completed / steps_required)}. On every turn, log current_step and captured_fields to maintain state machine visibility. Alert if: sequence_compliance <85%, or combined_questions >2 in any turn, or steps skipped, or duplicate questions asked.

2. **Premature-close detection and data-completeness audit**: Before agent closes call, verify: all required fields captured? If any required field missing, block close and escalate: "Incomplete qualification. Missing: [fields]. Ask before closing." Track: calls closed with missing fields (non-compliance). Post-call audit: verify captured data matches completion criteria. Alert if: >10% of calls closed with missing required fields.

### Architecture Patterns

1. **Ordered Qualification Flow State Machine**: Maintains ordered list of qualification steps: {step_1, step_2, ..., step_N}. On each turn: (a) determine current_step, (b) validate response against step requirements, (c) capture fields, (d) only proceed to next_step after current_step complete, (e) never skip steps or ask combined questions within a step. Logs current_step before every agent turn.

2. **Duplicate-Question Detector with Context Tracking**: Maintains history of asked_questions for call. Before agent generates response, check: have we already asked this question? If yes, block repeat question. Alert on detection.

3. **Close-Gate Validator**: Before agent can close/wrap call, gate checks: required_fields_captured? If missing, blocks close and suggests fields to capture. Only allows close when data_completeness_check passes.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Flow-Step Compliance | >95% | <85% | # of calls following prescribed step order without skips / total calls |
| Combined-Question Rate | <2% | >10% | # of turns asking multiple qualification fields in one question / total qualification turns |
| Duplicate-Question Rate | 0% | >5% | # of duplicate questions asked in single call / total qualification calls |
| Required-Field Capture Completeness | 100% | <95% | # of calls with all required fields captured before close / total qualification calls |
| Premature-Close Prevention Rate | 100% | <98% | # of close attempts with missing required fields that were blocked / total close attempts |
| Step-Skip Rate | 0% | >5% | # of calls that skipped required steps / total calls |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Step Skip Detected | Agent advances to next qualification step without completing current step | HIGH | Block advancement; escalate to complete current step before proceeding; log step-skip attempt |
| Combined Question Violation | Agent asks multiple qualification fields in single turn ("What's your name and email?") | MEDIUM | Flag turn as non-compliant; escalate to single-field re-ask; log violation |
| Duplicate Question Detected | Agent asks same qualification question twice in same call | MEDIUM | Flag as inefficiency; log for agent coaching; may indicate context-tracking failure |
| Premature Close Attempted | Agent tries to close/wrap call with required fields missing | CRITICAL | Block close action; escalate with list of missing fields; require completion before call terminates |
| Flow-Sequence Compliance Low | Overall compliance <85% for call; multiple step violations | HIGH | Flag call for manual review; investigate whether flow design is unclear or agent needs retraining |

---

## References

- [Task-Oriented Dialog Systems](https://arxiv.org/abs/2003.07490) - Flow management
- [Slot Filling Research](https://arxiv.org/abs/2009.13570) - State tracking
- [Voice Agent UX](https://www.beconversive.com/blog/voice-ai-challenges) - Flow design
- [Conversational AI Patterns](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Step issues
